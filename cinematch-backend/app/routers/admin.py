"""Admin Router — dashboard stats, revenue, usage analytics."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_admin
from app.models.user import User, SubscriptionTier
from app.models.rating import Rating
from app.services.cache_service import CacheService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", dependencies=[Depends(require_admin)])
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get platform statistics — admin only."""
    # Total users
    total_result = await db.execute(select(func.count(User.id)))
    total_users = total_result.scalar() or 0

    # Active users (last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    active_result = await db.execute(
        select(func.count(User.id)).where(User.last_login >= thirty_days_ago)
    )
    active_users = active_result.scalar() or 0

    # Total ratings
    ratings_result = await db.execute(select(func.count(Rating.id)))
    total_ratings = ratings_result.scalar() or 0

    # Subscription distribution
    sub_result = await db.execute(
        select(User.subscription_tier, func.count(User.id)).group_by(User.subscription_tier)
    )
    subscription_dist = {tier.value: count for tier, count in sub_result.all()}

    # API request count (from Redis counter)
    cache = await CacheService.get_instance()
    api_requests = await cache.get("stats:api_requests") or 0

    return {
        "total_users": total_users,
        "active_users_30d": active_users,
        "total_ratings": total_ratings,
        "api_requests": api_requests,
        "subscription_distribution": subscription_dist,
    }


@router.get("/revenue", dependencies=[Depends(require_admin)])
async def get_revenue(db: AsyncSession = Depends(get_db)):
    """Get revenue analytics — admin only."""
    # Count paid users
    pro_result = await db.execute(
        select(func.count(User.id)).where(User.subscription_tier == SubscriptionTier.PRO)
    )
    pro_users = pro_result.scalar() or 0

    enterprise_result = await db.execute(
        select(func.count(User.id)).where(
            User.subscription_tier == SubscriptionTier.ENTERPRISE
        )
    )
    enterprise_users = enterprise_result.scalar() or 0

    # Estimated revenue (placeholder pricing)
    monthly_revenue = (pro_users * 9.99) + (enterprise_users * 49.99)

    return {
        "pro_users": pro_users,
        "enterprise_users": enterprise_users,
        "estimated_mrr": round(monthly_revenue, 2),
        "currency": "USD",
    }


@router.get("/usage", dependencies=[Depends(require_admin)])
async def get_usage(db: AsyncSession = Depends(get_db)):
    """Get usage analytics — admin only."""
    # Ratings in last 7 days
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    recent_result = await db.execute(
        select(func.count(Rating.id)).where(Rating.created_at >= seven_days_ago)
    )
    recent_ratings = recent_result.scalar() or 0

    # Average ratings per user
    avg_result = await db.execute(
        select(func.avg(func.count(Rating.id))).select_from(
            select(Rating.user_id, func.count(Rating.id))
            .group_by(Rating.user_id)
            .subquery()
        )
    )
    avg_ratings_per_user = round(float(avg_result.scalar() or 0), 1)

    return {
        "ratings_last_7_days": recent_ratings,
        "avg_ratings_per_user": avg_ratings_per_user,
    }
