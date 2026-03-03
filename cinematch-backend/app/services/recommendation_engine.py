"""Hybrid Recommendation Engine — TF-IDF + Collaborative Filtering + Semantic."""

import os
import json
import pickle
import logging
from typing import Optional, List, Dict, Any
from datetime import timedelta


from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.movie import Movie
from app.models.rating import Rating
from app.services.cache_service import CacheService
from app.services.streaming_service import StreamingService
from app.schemas.recommendation import MovieRecommendation, StreamingProvider

settings = get_settings()
logger = logging.getLogger(__name__)

# ─── Mood Boost Multipliers ───
MOOD_BOOSTS: Dict[str, Dict[str, float]] = {
    "happy": {"Comedy": 1.3, "Family": 1.2, "Animation": 1.15},
    "romantic": {"Romance": 1.4, "Drama": 1.1},
    "motivated": {"Action": 1.3, "Biography": 1.35, "Sport": 1.2},
    "thriller_night": {"Thriller": 1.25, "Mystery": 1.25, "Crime": 1.15},
    "emotional": {"Drama": 1.4, "War": 1.2},
}

# ─── Context Keyword → Genre Mapping ───
CONTEXT_GENRE_MAP: Dict[str, List[str]] = {
    "space": ["Sci-Fi"],
    "love": ["Romance"],
    "scary": ["Horror", "Thriller"],
    "funny": ["Comedy"],
    "war": ["War", "History"],
    "family": ["Family", "Animation"],
    "dark": ["Thriller", "Crime", "Horror"],
    "epic": ["Adventure", "Fantasy"],
    "mind": ["Sci-Fi", "Mystery"],
    "real": ["Documentary", "Biography"],
}

CACHE_TTL = timedelta(minutes=15)


class RecommendationEngine:
    """
    Hybrid recommendation engine combining:
    - Content-based filtering (TF-IDF cosine similarity)
    - Collaborative filtering (user-based)
    - Semantic preference scoring
    """

    def __init__(self) -> None:
        self._tfidf_matrix = None
        self._similarity_matrix = None
        self._movie_index: Dict[str, int] = {}
        self._streaming_service = StreamingService()
        self._initialized = False

    async def initialize(self) -> None:
        """Load TF-IDF and similarity matrices from disk."""
        if self._initialized:
            return

        try:
            # Load TF-IDF matrix
            if os.path.exists(settings.TFIDF_MATRIX_PATH):
                with open(settings.TFIDF_MATRIX_PATH, "rb") as f:
                    data = pickle.load(f)
                self._tfidf_matrix = data.get("matrix")
                self._movie_index = data.get("index", {})
                logger.info("TF-IDF matrix loaded")

            # Load similarity matrix
            if os.path.exists(settings.SIMILARITY_MATRIX_PATH):
                with open(settings.SIMILARITY_MATRIX_PATH, "rb") as f:
                    self._similarity_matrix = pickle.load(f)
                logger.info("Similarity matrix loaded")

            self._initialized = True
            logger.info("RecommendationEngine initialized")

        except Exception as e:
            logger.error(f"Failed to initialize RecommendationEngine: {e}")
            self._initialized = True

    async def recommend(
        self,
        movie_title: str,
        db: AsyncSession,
        user_id: Optional[int] = None,
        mood: Optional[str] = None,
        context: Optional[str] = None,
        country_code: str = "IN",
        limit: int = 10,
    ) -> List[MovieRecommendation]:
        """
        Generate hybrid recommendations.

        Scoring:
            final = 0.4*content + 0.4*collab + 0.2*preference
            then apply mood_boost and context_boost
        """
        cache = await CacheService.get_instance()
        cache_key = f"reco:{movie_title}:{user_id}:{mood}:{context}:{country_code}:{limit}"

        # Check cache
        cached = await cache.get(cache_key)
        if cached:
            return [MovieRecommendation(**r) for r in cached]

        # Fetch all movies from DB
        result = await db.execute(select(Movie).limit(500))
        all_movies = result.scalars().all()

        if not all_movies:
            return []

        # Build scores
        scored_movies: List[Dict[str, Any]] = []

        for movie in all_movies:
            if movie.title.lower() == movie_title.lower():
                continue

            # ── Content score (TF-IDF similarity) ──
            content_score = self._get_content_score(movie_title, movie.title)

            # ── Collaborative score ──
            collab_score = await self._get_collab_score(db, user_id, movie.id) if user_id else 0.0

            # ── Preference score (genre/director matching) ──
            preference_score = await self._get_preference_score(db, user_id, movie) if user_id else 0.0

            # ── Weighted ensemble ──
            if user_id and collab_score > 0:
                final_score = (
                    0.4 * content_score + 0.4 * collab_score + 0.2 * preference_score
                )
            else:
                # No collab data — lean on content
                final_score = 0.7 * content_score + 0.3 * preference_score

            # ── Mood boost ──
            if mood and mood in MOOD_BOOSTS:
                genres = json.loads(movie.genres) if movie.genres else []
                for g in genres:
                    if g in MOOD_BOOSTS[mood]:
                        final_score *= MOOD_BOOSTS[mood][g]

            # ── Context boost ──
            if context:
                genres = json.loads(movie.genres) if movie.genres else []
                for keyword, boost_genres in CONTEXT_GENRE_MAP.items():
                    if keyword in context.lower():
                        for g in genres:
                            if g in boost_genres:
                                final_score *= 1.15

            scored_movies.append(
                {
                    "movie": movie,
                    "score": min(final_score * 100, 99.9),
                }
            )

        # Sort by score
        scored_movies.sort(key=lambda x: x["score"], reverse=True)
        top_movies = scored_movies[:limit]

        # Fetch streaming data in parallel
        movie_ids = [m["movie"].tmdb_id for m in top_movies if m["movie"].tmdb_id]
        streaming_data = await self._streaming_service.get_bulk_providers(
            movie_ids, country_code
        )

        # Build response
        recommendations: List[MovieRecommendation] = []
        for item in top_movies:
            movie = item["movie"]
            genres = json.loads(movie.genres) if movie.genres else []
            streaming = streaming_data.get(movie.tmdb_id)
            providers: List[StreamingProvider] = []

            if streaming:
                for p in streaming.flatrate:
                    providers.append(
                        StreamingProvider(
                            name=p.provider_name,
                            logo_url=p.logo_path,
                            brand_color=p.brand_color,
                            type="flatrate",
                        )
                    )

            recommendations.append(
                MovieRecommendation(
                    id=movie.id,
                    title=movie.title,
                    overview=movie.overview,
                    genres=genres,
                    director=movie.director,
                    release_year=movie.release_year,
                    runtime=movie.runtime,
                    imdb_rating=movie.imdb_rating,
                    poster_path=movie.poster_path,
                    match_score=round(item["score"], 1),
                    hidden_gem_score=self._compute_hidden_gem_score(movie),
                    streaming_providers=providers,
                    why_picked=self._generate_explanation(movie, genres, mood),
                )
            )

        # Cache results
        await cache.set(
            cache_key,
            [r.model_dump() for r in recommendations],
            ttl=CACHE_TTL,
        )

        return recommendations

    def _get_content_score(self, query_title: str, candidate_title: str) -> float:
        """Get TF-IDF cosine similarity between two movies."""
        if self._similarity_matrix is None or self._movie_index is None:
            return 0.5  # Neutral fallback

        q_idx = self._movie_index.get(query_title.lower())
        c_idx = self._movie_index.get(candidate_title.lower())

        if q_idx is not None and c_idx is not None:
            try:
                return float(self._similarity_matrix[q_idx, c_idx])
            except (IndexError, KeyError):
                return 0.0
        return 0.0

    async def _get_collab_score(
        self, db: AsyncSession, user_id: Optional[int], movie_id: int
    ) -> float:
        """User-based collaborative filtering score."""
        if not user_id:
            return 0.0

        # Check if user has enough ratings
        count_result = await db.execute(
            select(func.count(Rating.id)).where(Rating.user_id == user_id)
        )
        rating_count = count_result.scalar() or 0

        if rating_count < 5:
            return 0.0  # Not enough data for CF

        # Get users who rated this movie
        similar_ratings = await db.execute(
            select(Rating)
            .where(Rating.movie_id == movie_id, Rating.user_id != user_id)
            .limit(50)
        )
        ratings = similar_ratings.scalars().all()

        if not ratings:
            return 0.0

        # Simple average of other users' ratings normalized to 0-1
        avg = sum(r.score for r in ratings) / len(ratings)
        return avg / 5.0

    async def _get_preference_score(
        self, db: AsyncSession, user_id: Optional[int], movie: Movie
    ) -> float:
        """Score based on user's genre/director preferences."""
        if not user_id:
            return 0.0

        # Get user's rated movies
        user_ratings = await db.execute(
            select(Rating, Movie)
            .join(Movie, Rating.movie_id == Movie.id)
            .where(Rating.user_id == user_id, Rating.score >= 4.0)
            .limit(50)
        )
        liked = user_ratings.all()

        if not liked:
            return 0.0

        # Build genre frequency
        genre_counts: Dict[str, int] = {}
        director_bonus = 0.0
        for rating, rated_movie in liked:
            genres = json.loads(rated_movie.genres) if rated_movie.genres else []
            for g in genres:
                genre_counts[g] = genre_counts.get(g, 0) + 1
            if rated_movie.director and movie.director:
                if rated_movie.director.lower() == movie.director.lower():
                    director_bonus = 0.3

        # Score based on genre overlap
        movie_genres = json.loads(movie.genres) if movie.genres else []
        if not genre_counts or not movie_genres:
            return director_bonus

        total = sum(genre_counts.values())
        score = sum(genre_counts.get(g, 0) / total for g in movie_genres) / len(movie_genres)

        return min(score + director_bonus, 1.0)

    def _compute_hidden_gem_score(self, movie: Movie) -> float:
        """Compute hidden gem score for a movie."""
        imdb = movie.imdb_rating or 0.0
        rt = movie.rt_score or 0.0
        popularity = movie.popularity or 0.0

        # Normalize popularity to 0-1 range (higher = more popular = lower gem score)
        pop_penalty = min(popularity / 100.0, 1.0)

        score = (imdb * 0.35 / 10) + (rt * 0.25 / 100) + (0.25 * 0.5) - (pop_penalty * 0.15)
        return round(max(score * 100, 0), 1)

    def _generate_explanation(
        self, movie: Movie, genres: List[str], mood: Optional[str]
    ) -> str:
        """Generate a placeholder AI explanation."""
        genre_str = ", ".join(genres[:2]) if genres else "unique storytelling"
        mood_str = f" Perfect for your {mood} mood." if mood else ""

        return (
            f"This {genre_str} film matches your taste for compelling narratives "
            f"and distinctive filmmaking.{mood_str}"
        )
