"""Streaming Alert Worker — standalone background process."""

import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models.streaming_alert import StreamingAlert
from app.models.movie import Movie
from app.services.streaming_service import StreamingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_streaming_service = StreamingService()

CHECK_INTERVAL_SECONDS = 3600  # Run every hour


async def check_alerts() -> None:
    """Check all active streaming alerts for new availability."""
    logger.info("🔔 Checking streaming alerts...")

    async with async_session() as db:
        # Get active, un-notified alerts
        result = await db.execute(
            select(StreamingAlert, Movie)
            .join(Movie, StreamingAlert.movie_id == Movie.id)
            .where(
                StreamingAlert.is_active == True,
                StreamingAlert.is_notified == False,
            )
        )
        alerts = result.all()

        if not alerts:
            logger.info("No active alerts to check")
            return

        logger.info(f"Checking {len(alerts)} active alerts...")

        for alert, movie in alerts:
            try:
                if not movie.tmdb_id:
                    continue

                availability = await _streaming_service.get_providers(
                    movie.tmdb_id, alert.country_code
                )

                # Check if movie is now available on a desired platform
                if availability.available:
                    if alert.platform_filter:
                        desired = set(
                            p.strip() for p in alert.platform_filter.split(",")
                        )
                        available_names = {p.provider_name for p in availability.flatrate}
                        if not desired & available_names:
                            continue

                    # Movie is available — mark as notified
                    alert.is_notified = True
                    alert.notified_at = datetime.now(timezone.utc)

                    logger.info(
                        f"🎬 Alert triggered: '{movie.title}' now streaming "
                        f"for user {alert.user_id} in {alert.country_code}"
                    )

                    # In production: send push notification / email here

            except Exception as e:
                logger.error(f"Error checking alert {alert.id}: {e}")

        await db.commit()

    logger.info("✅ Alert check complete")


async def main() -> None:
    """Run the worker in a loop."""
    logger.info("🚀 Streaming Alert Worker started")

    while True:
        try:
            await check_alerts()
        except Exception as e:
            logger.error(f"Worker error: {e}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
