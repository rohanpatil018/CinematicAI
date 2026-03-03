"""Recommendations Router — hybrid recs + semantic search."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    SemanticSearchRequest,
    SemanticSearchResponse,
)
from app.services.recommendation_engine import RecommendationEngine
from app.services.semantic_search import SemanticSearchService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

_engine = RecommendationEngine()


@router.post("", response_model=RecommendationResponse)
async def get_recommendations(
    payload: RecommendationRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get hybrid movie recommendations."""
    # Initialize engine if needed
    await _engine.initialize()

    recommendations = await _engine.recommend(
        movie_title=payload.movie_title,
        db=db,
        user_id=user_id,
        mood=payload.mood,
        context=payload.context,
        country_code=payload.country_code,
        limit=payload.limit,
    )

    return RecommendationResponse(
        query=payload.movie_title,
        mood=payload.mood,
        total_results=len(recommendations),
        recommendations=recommendations,
    )


@router.post("/semantic-search", response_model=SemanticSearchResponse)
async def semantic_search(payload: SemanticSearchRequest):
    """Semantic search over movie descriptions using FAISS."""
    service = await SemanticSearchService.get_instance()
    await service.initialize()

    results = await service.search(query=payload.query, limit=payload.limit)

    return SemanticSearchResponse(
        query=payload.query,
        results=results,
    )
