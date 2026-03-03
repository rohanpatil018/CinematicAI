"""Streaming schemas."""

from typing import Optional, List
from pydantic import BaseModel


class StreamingProviderInfo(BaseModel):
    provider_id: int
    provider_name: str
    logo_path: Optional[str] = None
    brand_color: str = "#555555"
    display_priority: int = 0


class StreamingAvailability(BaseModel):
    movie_id: int
    country: str
    flatrate: List[StreamingProviderInfo] = []
    rent: List[StreamingProviderInfo] = []
    buy: List[StreamingProviderInfo] = []
    available: bool = False
    link: Optional[str] = None


class StreamingAlertCreate(BaseModel):
    movie_id: int
    country_code: str = "IN"
    platform_filter: Optional[str] = None


class StreamingAlertResponse(BaseModel):
    id: int
    movie_id: int
    country_code: str
    platform_filter: Optional[str] = None
    is_notified: bool
    is_active: bool

    model_config = {"from_attributes": True}
