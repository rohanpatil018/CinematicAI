"""Streaming Availability Service — TMDB integration."""

import asyncio
from typing import Optional, List
from datetime import timedelta

import httpx

from app.core.config import get_settings
from app.services.cache_service import CacheService
from app.schemas.streaming import StreamingAvailability, StreamingProviderInfo

settings = get_settings()

# ─── Provider Brand Colors ───
PROVIDER_COLORS = {
    "Netflix": "#E50914",
    "Amazon Prime Video": "#00A8E1",
    "Disney Plus": "#032541",
    "Disney+ Hotstar": "#032541",
    "Hotstar": "#032541",
    "Apple TV Plus": "#000000",
    "Apple TV": "#000000",
    "Hulu": "#3DBB3D",
    "HBO Max": "#6B3FA0",
    "Max": "#6B3FA0",
    "Paramount Plus": "#0064FF",
    "Peacock": "#000000",
    "MUBI": "#FF6B00",
    "Tubi": "#00BFA5",
    "Zee5": "#8230C6",
    "SonyLIV": "#121212",
    "JioCinema": "#E8078A",
    "Voot": "#FF2695",
}

CACHE_TTL = timedelta(hours=24)


class StreamingService:
    """Fetch and cache streaming availability from TMDB."""

    def __init__(self) -> None:
        self._http_client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                base_url=settings.TMDB_BASE_URL,
                timeout=10.0,
                params={"api_key": settings.TMDB_API_KEY},
            )
        return self._http_client

    def _map_provider(self, raw: dict) -> StreamingProviderInfo:
        """Map a TMDB provider dict to our schema."""
        name = raw.get("provider_name", "Unknown")
        return StreamingProviderInfo(
            provider_id=raw.get("provider_id", 0),
            provider_name=name,
            logo_path=f"https://image.tmdb.org/t/p/w92{raw.get('logo_path', '')}",
            brand_color=PROVIDER_COLORS.get(name, "#555555"),
            display_priority=raw.get("display_priority", 999),
        )

    async def get_providers(
        self, movie_id: int, country: str = "IN"
    ) -> StreamingAvailability:
        """
        Get streaming providers for a movie in a specific country.
        Results cached in Redis for 24 hours.
        """
        cache = await CacheService.get_instance()
        cache_key = f"streaming:{movie_id}:{country}"

        # Check cache
        cached = await cache.get(cache_key)
        if cached:
            return StreamingAvailability(**cached)

        # Fetch from TMDB
        try:
            client = await self._get_client()
            response = await client.get(f"/movie/{movie_id}/watch/providers")
            response.raise_for_status()
            data = response.json()

            country_data = data.get("results", {}).get(country, {})

            result = StreamingAvailability(
                movie_id=movie_id,
                country=country,
                flatrate=[
                    self._map_provider(p)
                    for p in country_data.get("flatrate", [])
                ],
                rent=[
                    self._map_provider(p)
                    for p in country_data.get("rent", [])
                ],
                buy=[
                    self._map_provider(p)
                    for p in country_data.get("buy", [])
                ],
                available=bool(country_data.get("flatrate")),
                link=country_data.get("link"),
            )

            # Cache result
            await cache.set(cache_key, result.model_dump(), ttl=CACHE_TTL)
            return result

        except httpx.HTTPError:
            return StreamingAvailability(movie_id=movie_id, country=country)

    async def get_bulk_providers(
        self, movie_ids: List[int], country: str = "IN"
    ) -> dict[int, StreamingAvailability]:
        """Fetch streaming data for multiple movies in parallel."""
        tasks = [self.get_providers(mid, country) for mid in movie_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        output: dict[int, StreamingAvailability] = {}
        for mid, result in zip(movie_ids, results):
            if isinstance(result, StreamingAvailability):
                output[mid] = result
            else:
                output[mid] = StreamingAvailability(movie_id=mid, country=country)
        return output

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
