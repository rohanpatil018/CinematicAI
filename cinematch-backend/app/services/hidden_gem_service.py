"""Hidden Gem Detector Service."""

import json
import logging
from typing import List
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie
from app.services.cache_service import CacheService
from app.schemas.recommendation import HiddenGemResponse

logger = logging.getLogger(__name__)

CACHE_TTL = timedelta(hours=6)


class HiddenGemService:
    """
    Detect hidden gems using the formula:
    HGS = (imdb_rating * 0.35) + (rt_score * 0.25) +
          (content_similarity * 0.25) - (popularity_rank * 0.15)

    Only returns movies where vote_count < 100000 AND rating > 7.5
    """

    async def get_hidden_gems(
        self, db: AsyncSession, limit: int = 20
    ) -> List[HiddenGemResponse]:
        """Fetch and score hidden gems."""
        cache = await CacheService.get_instance()
        cache_key = f"hidden_gems:{limit}"

        cached = await cache.get(cache_key)
        if cached:
            return [HiddenGemResponse(**g) for g in cached]

        # Query movies matching hidden gem criteria
        result = await db.execute(
            select(Movie).where(
                Movie.imdb_rating > 7.5,
                Movie.vote_count < 100000,
                Movie.vote_count > 0,
            )
        )
        movies = result.scalars().all()

        if not movies:
            return []

        # Score and sort
        gems: List[HiddenGemResponse] = []
        max_pop = max((m.popularity or 1) for m in movies) or 1

        for movie in movies:
            imdb = movie.imdb_rating or 0.0
            rt = movie.rt_score or 0.0
            popularity = movie.popularity or 0.0

            # Normalize values to 0-1 range
            norm_imdb = imdb / 10.0
            norm_rt = rt / 100.0
            norm_pop = popularity / max_pop

            # Content similarity placeholder (would use FAISS in production)
            content_sim = 0.5

            # Hidden Gem Score
            hgs = (
                (norm_imdb * 0.35)
                + (norm_rt * 0.25)
                + (content_sim * 0.25)
                - (norm_pop * 0.15)
            )

            genres = json.loads(movie.genres) if movie.genres else []

            gems.append(
                HiddenGemResponse(
                    id=movie.id,
                    title=movie.title,
                    overview=movie.overview,
                    genres=genres,
                    release_year=movie.release_year,
                    imdb_rating=movie.imdb_rating,
                    hidden_gem_score=round(hgs * 100, 1),
                    poster_path=movie.poster_path,
                    why_hidden_gem=(
                        f"With a {imdb}/10 IMDB rating and only {movie.vote_count:,} votes, "
                        f"this {genres[0] if genres else 'film'} is criminally underwatched."
                    ),
                )
            )

        # Sort by hidden gem score descending
        gems.sort(key=lambda g: g.hidden_gem_score, reverse=True)
        gems = gems[:limit]

        # Cache
        await cache.set(cache_key, [g.model_dump() for g in gems], ttl=CACHE_TTL)

        return gems
