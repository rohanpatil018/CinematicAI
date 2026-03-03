"""Cinematic DNA Service — build user taste profiles."""

import json
import logging
from typing import Dict, List, Tuple
from datetime import timedelta
from collections import Counter

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rating import Rating
from app.models.movie import Movie
from app.services.cache_service import CacheService
from app.schemas.dna import (
    DNAProfile,
    GenreWeight,
    TasteEvolutionPoint,
    ARCHETYPES,
)

logger = logging.getLogger(__name__)

CACHE_TTL = timedelta(days=7)

# ─── Genre Colors ───
GENRE_COLORS: Dict[str, str] = {
    "Action": "#FF4136",
    "Adventure": "#FF851B",
    "Animation": "#FFDC00",
    "Comedy": "#2ECC40",
    "Crime": "#85144b",
    "Documentary": "#0074D9",
    "Drama": "#B10DC9",
    "Family": "#39CCCC",
    "Fantasy": "#F012BE",
    "History": "#3D9970",
    "Horror": "#111111",
    "Music": "#01FF70",
    "Mystery": "#7FDBFF",
    "Romance": "#FF69B4",
    "Sci-Fi": "#00CED1",
    "Thriller": "#e74c3c",
    "War": "#556B2F",
    "Western": "#DEB887",
    "Biography": "#DAA520",
}


class DNAService:
    """Build and cache cinematic DNA profiles for users."""

    async def build_dna_profile(self, user_id: int, db: AsyncSession) -> DNAProfile:
        """
        Aggregate user's ratings to build a cinematic DNA profile.
        Requires minimum 5 ratings.
        """
        cache = await CacheService.get_instance()
        cache_key = f"dna:{user_id}"

        # Check cache
        cached = await cache.get(cache_key)
        if cached:
            return DNAProfile(**cached)

        # Get user's ratings with movie data
        result = await db.execute(
            select(Rating, Movie)
            .join(Movie, Rating.movie_id == Movie.id)
            .where(Rating.user_id == user_id)
            .order_by(Rating.created_at.desc())
        )
        rows = result.all()

        total_ratings = len(rows)
        if total_ratings < 5:
            return DNAProfile(
                user_id=user_id,
                archetype="Undiscovered",
                archetype_description="Rate at least 5 movies to unlock your Cinematic DNA.",
                top_genres=[],
                top_directors=[],
                radar_chart_data={},
                taste_evolution=[],
                total_movies_rated=total_ratings,
                avg_rating=0.0,
                ai_description="Keep rating movies to reveal your cinematic personality!",
            )

        # ── Aggregate Genres ──
        genre_scores: Counter = Counter()
        director_scores: Counter = Counter()
        total_score = 0.0

        for rating, movie in rows:
            genres = json.loads(movie.genres) if movie.genres else []
            weight = rating.score / 5.0  # Normalize to 0-1

            for genre in genres:
                genre_scores[genre] += weight

            if movie.director:
                director_scores[movie.director] += weight

            total_score += rating.score

        avg_rating = round(total_score / total_ratings, 2)

        # ── Top Genres ──
        total_genre_weight = sum(genre_scores.values()) or 1
        top_genres = [
            GenreWeight(
                genre=genre,
                weight=round(count / total_genre_weight, 3),
                color=GENRE_COLORS.get(genre, "#FFBF1F"),
            )
            for genre, count in genre_scores.most_common(8)
        ]

        # ── Radar Chart Data ──
        radar_data: Dict[str, float] = {}
        for gw in top_genres[:6]:
            radar_data[gw.genre] = gw.weight

        # ── Top Directors ──
        top_directors = [d for d, _ in director_scores.most_common(5)]

        # ── Determine Archetype ──
        archetype, description = self._match_archetype(genre_scores)

        # ── Taste Evolution (simplified — group by quarters) ──
        evolution = self._compute_taste_evolution(rows)

        # ── AI Description ──
        genre_list = ", ".join(g.genre for g in top_genres[:3])
        ai_desc = (
            f"You've rated {total_ratings} films with an average score of {avg_rating}. "
            f"Your taste leans heavily into {genre_list}. "
            f"{description}"
        )

        profile = DNAProfile(
            user_id=user_id,
            archetype=archetype,
            archetype_description=description,
            top_genres=top_genres,
            top_directors=top_directors,
            radar_chart_data=radar_data,
            taste_evolution=evolution,
            total_movies_rated=total_ratings,
            avg_rating=avg_rating,
            ai_description=ai_desc,
        )

        # Cache for 7 days
        await cache.set(cache_key, profile.model_dump(), ttl=CACHE_TTL)

        return profile

    def _match_archetype(self, genre_scores: Counter) -> Tuple[str, str]:
        """Match user's genre distribution to the closest archetype."""
        if not genre_scores:
            return "Undiscovered", "Keep watching to discover your archetype!"

        top_two = [g for g, _ in genre_scores.most_common(2)]

        best_match = "The Melancholic Visionary"
        best_overlap = 0

        for name, info in ARCHETYPES.items():
            dominant = info["dominant"]
            overlap = len(set(top_two) & set(dominant))
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = name

        return best_match, ARCHETYPES[best_match]["description"]

    def _compute_taste_evolution(self, rows: list) -> List[TasteEvolutionPoint]:
        """Group ratings by quarter and track dominant genre evolution."""
        quarter_data: Dict[str, Counter] = {}
        quarter_ratings: Dict[str, List[float]] = {}

        for rating, movie in rows:
            if not rating.created_at:
                continue
            quarter = f"{rating.created_at.year}-Q{(rating.created_at.month - 1) // 3 + 1}"
            genres = json.loads(movie.genres) if movie.genres else []

            if quarter not in quarter_data:
                quarter_data[quarter] = Counter()
                quarter_ratings[quarter] = []

            for g in genres:
                quarter_data[quarter][g] += rating.score
            quarter_ratings[quarter].append(rating.score)

        evolution: List[TasteEvolutionPoint] = []
        for period in sorted(quarter_data.keys()):
            dominant = quarter_data[period].most_common(1)
            avg = sum(quarter_ratings[period]) / len(quarter_ratings[period])
            evolution.append(
                TasteEvolutionPoint(
                    period=period,
                    dominant_genre=dominant[0][0] if dominant else "Unknown",
                    avg_rating=round(avg, 2),
                )
            )

        return evolution[-8:]  # Last 8 quarters
