"""Cinematic DNA schemas."""

from typing import Optional, List, Dict
from pydantic import BaseModel


class GenreWeight(BaseModel):
    genre: str
    weight: float
    color: str = "#FFBF1F"


class TasteEvolutionPoint(BaseModel):
    period: str  # e.g. "2024-Q1"
    dominant_genre: str
    avg_rating: float


class DNAProfile(BaseModel):
    user_id: int
    archetype: str
    archetype_description: str
    top_genres: List[GenreWeight]
    top_directors: List[str]
    radar_chart_data: Dict[str, float]  # genre -> normalized weight (0-1)
    taste_evolution: List[TasteEvolutionPoint]
    total_movies_rated: int
    avg_rating: float
    ai_description: str = ""


# ─── 8 Archetypes ───
ARCHETYPES = {
    "The Melancholic Visionary": {
        "dominant": ["Drama", "Sci-Fi"],
        "description": "You find beauty in sorrow and meaning in the vast unknown. "
                       "Your taste gravitates toward emotionally layered narratives with visual grandeur.",
    },
    "The Thrill Architect": {
        "dominant": ["Thriller", "Action"],
        "description": "You thrive on tension and adrenaline. "
                       "Complex plots and high-stakes sequences are your cinematic playground.",
    },
    "The Romantic Idealist": {
        "dominant": ["Romance", "Drama"],
        "description": "You believe in love's transformative power. "
                       "Character-driven stories with emotional depth resonate deeply with you.",
    },
    "The Cerebral Explorer": {
        "dominant": ["Sci-Fi", "Mystery"],
        "description": "You crave intellectual stimulation and mind-bending concepts. "
                       "The more a film makes you think, the more you love it.",
    },
    "The Dark Connoisseur": {
        "dominant": ["Horror", "Thriller"],
        "description": "You appreciate the art of fear and suspense. "
                       "Atmospheric dread and psychological horror are your forte.",
    },
    "The Lighthearted Storyteller": {
        "dominant": ["Comedy", "Family"],
        "description": "You value warmth, humor, and genuine human connection. "
                       "Films that make you laugh and feel good are your sanctuary.",
    },
    "The Epic Voyager": {
        "dominant": ["Adventure", "Fantasy"],
        "description": "You're drawn to grand narratives and world-building. "
                       "Epic journeys and mythological themes fuel your imagination.",
    },
    "The Documentary Seeker": {
        "dominant": ["Documentary", "Biography"],
        "description": "You're fascinated by real stories and human achievement. "
                       "Truth is more compelling than fiction in your eyes.",
    },
}


class CompatibilityRequest(BaseModel):
    user2_id: int


class CompatibilityResponse(BaseModel):
    user1_id: int
    user2_id: int
    compatibility_score: float  # 0–100
    both_love: List[str]  # movie titles both rated highly
    compromise_picks: List[str]  # movies that bridge their tastes
    alternating_picks: List[str]  # one from each user's favorites
