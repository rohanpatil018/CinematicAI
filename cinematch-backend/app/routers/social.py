"""Social Router — Watch Together / Compatibility."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.dna import CompatibilityRequest, CompatibilityResponse
from app.services.compatibility_service import CompatibilityService

router = APIRouter(prefix="/watch-together", tags=["Social"])

_compatibility_service = CompatibilityService()


@router.post("", response_model=CompatibilityResponse)
async def watch_together(
    payload: CompatibilityRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Calculate Watch Together compatibility between two users."""
    if payload.user2_id == user_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Cannot compare with yourself")

    return await _compatibility_service.calculate_compatibility(
        user1_id=user_id,
        user2_id=payload.user2_id,
        db=db,
    )
