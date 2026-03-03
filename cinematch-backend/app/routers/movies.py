"""Movies Router — CRUD, streaming, hidden gems."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.movie import Movie
from app.models.rating import Rating
from app.schemas.streaming import StreamingAvailability
from app.schemas.recommendation import HiddenGemResponse
from app.services.streaming_service import StreamingService
from app.services.hidden_gem_service import HiddenGemService

router = APIRouter(prefix="/movies", tags=["Movies"])

_streaming_service = StreamingService()
_hidden_gem_service = HiddenGemService()


@router.get("", response_model=List[dict])
async def list_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """List movies with pagination and optional filters."""
    query = select(Movie)

    if genre:
        query = query.where(Movie.genres.contains(genre))
    if year:
        query = query.where(Movie.release_year == year)

    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    movies = result.scalars().all()

    return [
        {
            "id": m.id,
            "title": m.title,
            "overview": m.overview,
            "genres": m.genres,
            "release_year": m.release_year,
            "imdb_rating": m.imdb_rating,
            "poster_path": m.poster_path,
        }
        for m in movies
    ]


@router.get("/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single movie by ID."""
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {
        "id": movie.id,
        "tmdb_id": movie.tmdb_id,
        "title": movie.title,
        "overview": movie.overview,
        "genres": movie.genres,
        "director": movie.director,
        "cast_members": movie.cast_members,
        "release_year": movie.release_year,
        "runtime": movie.runtime,
        "imdb_rating": movie.imdb_rating,
        "poster_path": movie.poster_path,
        "backdrop_path": movie.backdrop_path,
    }


@router.post("/{movie_id}/rate")
async def rate_movie(
    movie_id: int,
    score: float = Query(ge=0.5, le=5.0),
    review: Optional[str] = None,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Rate a movie (creates or updates rating)."""
    # Verify movie exists
    movie_result = await db.execute(select(Movie).where(Movie.id == movie_id))
    if not movie_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Movie not found")

    # Check existing rating
    rating_result = await db.execute(
        select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
    )
    existing = rating_result.scalar_one_or_none()

    if existing:
        existing.score = score
        existing.review = review
        await db.flush()
        return {"message": "Rating updated", "score": score}

    new_rating = Rating(user_id=user_id, movie_id=movie_id, score=score, review=review)
    db.add(new_rating)
    await db.flush()

    return {"message": "Rating created", "score": score}


@router.get("/{movie_id}/streaming", response_model=StreamingAvailability)
async def get_streaming(
    movie_id: int,
    country: str = Query("IN", max_length=5),
):
    """Get streaming availability for a movie."""
    return await _streaming_service.get_providers(movie_id, country)


@router.get("/hidden-gems", response_model=List[HiddenGemResponse])
async def get_hidden_gems(
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Get hidden gem movies."""
    return await _hidden_gem_service.get_hidden_gems(db, limit)
