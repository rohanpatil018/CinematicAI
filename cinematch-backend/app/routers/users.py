"""Users Router — profile, DNA, ratings."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.rating import Rating
from app.schemas.user import UserResponse, UserUpdate, UserProfileResponse
from app.schemas.dna import DNAProfile
from app.services.dna_service import DNAService

router = APIRouter(prefix="/users", tags=["Users"])

_dna_service = DNAService()


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_my_profile(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's full profile with rating stats."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Count ratings
    count_result = await db.execute(
        select(func.count(Rating.id)).where(Rating.user_id == user_id)
    )
    total_ratings = count_result.scalar() or 0

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        avatar_url=user.avatar_url,
        role=user.role.value,
        subscription_tier=user.subscription_tier.value,
        is_active=user.is_active,
        created_at=user.created_at,
        last_login=user.last_login,
        total_ratings=total_ratings,
    )


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    payload: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update the current user's profile."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await db.flush()
    await db.refresh(user)
    return user


@router.get("/dna", response_model=DNAProfile)
async def get_dna_profile(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's Cinematic DNA profile."""
    return await _dna_service.build_dna_profile(user_id, db)
