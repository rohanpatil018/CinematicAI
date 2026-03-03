"""Recommendation schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    movie_title: str = Field(min_length=1, max_length=500)
    mood: Optional[str] = None
    context: Optional[str] = None
    country_code: str = Field(default="IN", max_length=5)
    limit: int = Field(default=10, ge=1, le=50)


class StreamingProvider(BaseModel):
    name: str
    logo_url: Optional[str] = None
    brand_color: str
    type: str  # "flatrate", "rent", "buy"
    available: bool = True


class MovieRecommendation(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    genres: List[str] = []
    director: Optional[str] = None
    release_year: Optional[int] = None
    runtime: Optional[int] = None
    imdb_rating: Optional[float] = None
    poster_path: Optional[str] = None
    match_score: float = Field(ge=0, le=100)
    hidden_gem_score: Optional[float] = None
    streaming_providers: List[StreamingProvider] = []
    why_picked: str = ""


class RecommendationResponse(BaseModel):
    query: str
    mood: Optional[str] = None
    total_results: int
    recommendations: List[MovieRecommendation]


class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=10, ge=1, le=50)


class SemanticSearchResult(BaseModel):
    movie_id: int
    title: str
    overview: Optional[str] = None
    similarity_score: float
    poster_path: Optional[str] = None


class SemanticSearchResponse(BaseModel):
    query: str
    results: List[SemanticSearchResult]


class HiddenGemResponse(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    genres: List[str] = []
    release_year: Optional[int] = None
    imdb_rating: Optional[float] = None
    hidden_gem_score: float
    poster_path: Optional[str] = None
    why_hidden_gem: str = ""
