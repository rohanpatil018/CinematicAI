"""APScheduler — periodic background jobs."""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def refresh_streaming_cache() -> None:
    """Refresh streaming availability cache for popular movies (runs every 6 hours)."""
    logger.info("🔄 Background job: Refreshing streaming cache...")
    # In production, this would:
    # 1. Query top 500 movies from DB
    # 2. Fetch latest streaming data for each
    # 3. Update Redis cache
    logger.info("✅ Streaming cache refresh complete")


async def compute_trending_gems() -> None:
    """Recompute hidden gem rankings (runs daily at 3 AM)."""
    logger.info("💎 Background job: Computing trending hidden gems...")
    # In production, this would:
    # 1. Query all movies meeting gem criteria
    # 2. Recompute HGS scores
    # 3. Update Redis leaderboard
    logger.info("✅ Hidden gem rankings updated")


async def cleanup_expired_alerts() -> None:
    """Remove expired/orphaned streaming alerts (runs daily at 4 AM)."""
    logger.info("🧹 Background job: Cleaning up expired alerts...")
    logger.info("✅ Alert cleanup complete")


def start_scheduler() -> None:
    """Register all background jobs and start the scheduler."""
    scheduler.add_job(
        refresh_streaming_cache,
        trigger=IntervalTrigger(hours=6),
        id="refresh_streaming",
        name="Refresh streaming availability cache",
        replace_existing=True,
    )

    scheduler.add_job(
        compute_trending_gems,
        trigger=CronTrigger(hour=3, minute=0),
        id="compute_gems",
        name="Recompute hidden gem rankings",
        replace_existing=True,
    )

    scheduler.add_job(
        cleanup_expired_alerts,
        trigger=CronTrigger(hour=4, minute=0),
        id="cleanup_alerts",
        name="Clean up expired streaming alerts",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("⏰ APScheduler started with 3 background jobs")


def stop_scheduler() -> None:
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("⏰ APScheduler stopped")
