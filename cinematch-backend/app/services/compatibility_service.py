"""Watch Together — Compatibility Service."""

import json
import logging
from typing import List, Dict, Set
from collections import Counter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rating import Rating
from app.models.movie import Movie
from app.schemas.dna import CompatibilityResponse

logger = logging.getLogger(__name__)


class CompatibilityService:
    """Calculate taste compatibility between two users."""

    async def calculate_compatibility(
        self, user1_id: int, user2_id: int, db: AsyncSession
    ) -> CompatibilityResponse:
        """
        Compare two users' ratings and return:
        - Compatibility score (0–100)
        - Movies both love
        - Compromise picks
        - Alternating picks
        """
        # Fetch ratings for both users
        u1_ratings = await self._get_user_ratings(user1_id, db)
        u2_ratings = await self._get_user_ratings(user2_id, db)

        # ── Movies both rated ──
        common_movies = set(u1_ratings.keys()) & set(u2_ratings.keys())

        # ── Compatibility Score ──
        if common_movies:
            diffs = [abs(u1_ratings[m]["score"] - u2_ratings[m]["score"]) for m in common_movies]
            avg_diff = sum(diffs) / len(diffs)
            score_from_common = max(0, 100 - (avg_diff * 20))
        else:
            score_from_common = 50  # Neutral if no common movies

        # Genre overlap
        u1_genres = self._get_genre_distribution(u1_ratings)
        u2_genres = self._get_genre_distribution(u2_ratings)
        genre_overlap = self._cosine_similarity(u1_genres, u2_genres) * 100

        # Final score: weighted average
        compatibility_score = round(0.6 * score_from_common + 0.4 * genre_overlap, 1)

        # ── Both Love (rated >= 4 by both) ──
        both_love: List[str] = []
        for movie_id in common_movies:
            if u1_ratings[movie_id]["score"] >= 4.0 and u2_ratings[movie_id]["score"] >= 4.0:
                both_love.append(u1_ratings[movie_id]["title"])

        # ── Compromise Picks (bridge genres) ──
        compromise_picks = await self._find_compromise_picks(
            u1_genres, u2_genres, u1_ratings, u2_ratings, db
        )

        # ── Alternating Picks (top from each user) ──
        u1_top = sorted(u1_ratings.values(), key=lambda x: x["score"], reverse=True)[:3]
        u2_top = sorted(u2_ratings.values(), key=lambda x: x["score"], reverse=True)[:3]

        alternating: List[str] = []
        for i in range(3):
            if i < len(u1_top):
                alternating.append(u1_top[i]["title"])
            if i < len(u2_top):
                alternating.append(u2_top[i]["title"])

        return CompatibilityResponse(
            user1_id=user1_id,
            user2_id=user2_id,
            compatibility_score=compatibility_score,
            both_love=both_love[:10],
            compromise_picks=compromise_picks[:5],
            alternating_picks=alternating[:6],
        )

    async def _get_user_ratings(
        self, user_id: int, db: AsyncSession
    ) -> Dict[int, Dict]:
        """Get all ratings for a user with movie metadata."""
        result = await db.execute(
            select(Rating, Movie)
            .join(Movie, Rating.movie_id == Movie.id)
            .where(Rating.user_id == user_id)
        )
        rows = result.all()

        return {
            movie.id: {
                "score": rating.score,
                "title": movie.title,
                "genres": json.loads(movie.genres) if movie.genres else [],
            }
            for rating, movie in rows
        }

    def _get_genre_distribution(self, ratings: Dict[int, Dict]) -> Counter:
        """Build genre frequency from user ratings."""
        counter: Counter = Counter()
        for data in ratings.values():
            for genre in data["genres"]:
                counter[genre] += data["score"]
        return counter

    def _cosine_similarity(self, c1: Counter, c2: Counter) -> float:
        """Compute cosine similarity between two genre counters."""
        all_genres = set(c1.keys()) | set(c2.keys())
        if not all_genres:
            return 0.0

        dot = sum(c1[g] * c2[g] for g in all_genres)
        mag1 = sum(v ** 2 for v in c1.values()) ** 0.5
        mag2 = sum(v ** 2 for v in c2.values()) ** 0.5

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot / (mag1 * mag2)

    async def _find_compromise_picks(
        self,
        u1_genres: Counter,
        u2_genres: Counter,
        u1_ratings: Dict,
        u2_ratings: Dict,
        db: AsyncSession,
    ) -> List[str]:
        """Find movies that bridge both users' genre preferences."""
        # Find genres that both users like
        shared_genres: Set[str] = set()
        for genre in set(u1_genres.keys()) & set(u2_genres.keys()):
            if u1_genres[genre] > 0 and u2_genres[genre] > 0:
                shared_genres.add(genre)

        if not shared_genres:
            return []

        # Find highly-rated movies in shared genres neither has rated
        rated_ids = set(u1_ratings.keys()) | set(u2_ratings.keys())

        result = await db.execute(
            select(Movie)
            .where(
                Movie.imdb_rating > 7.0,
                Movie.id.notin_(rated_ids) if rated_ids else True,
            )
            .order_by(Movie.imdb_rating.desc())
            .limit(100)
        )
        candidates = result.scalars().all()

        compromise: List[str] = []
        for movie in candidates:
            genres = json.loads(movie.genres) if movie.genres else []
            if set(genres) & shared_genres:
                compromise.append(movie.title)
                if len(compromise) >= 5:
                    break

        return compromise
