"""CineMatch AI Backend — Core Configuration."""

from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ─── Application ───
    APP_NAME: str = "CineMatch AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    API_PREFIX: str = "/api/v1"

    # ─── Database ───
    DATABASE_URL: str = "postgresql+asyncpg://cinematch:cinematch_secret@localhost:5432/cinematch_db"

    # ─── Redis ───
    REDIS_URL: str = "redis://localhost:6379/0"

    # ─── JWT Auth ───
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ─── TMDB API ───
    TMDB_API_KEY: str = ""
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"

    # ─── Rate Limiting ───
    RATE_LIMIT_PER_MINUTE: int = 60

    # ─── CORS ───
    CORS_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # ─── ML Models ───
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    FAISS_INDEX_PATH: str = "./data/faiss_index.bin"
    TFIDF_MATRIX_PATH: str = "./data/tfidf_matrix.pkl"
    SIMILARITY_MATRIX_PATH: str = "./data/similarity_matrix.pkl"

    # ─── Enterprise ───
    ENTERPRISE_API_KEY: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
