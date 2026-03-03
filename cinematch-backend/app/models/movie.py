"""Movie model."""

from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    original_title: Mapped[str] = mapped_column(String(500), nullable=True)
    overview: Mapped[str] = mapped_column(Text, nullable=True)
    tagline: Mapped[str] = mapped_column(String(500), nullable=True)
    genres: Mapped[str] = mapped_column(Text, nullable=True)  # JSON-encoded list
    director: Mapped[str] = mapped_column(String(255), nullable=True)
    cast_members: Mapped[str] = mapped_column(Text, nullable=True)  # JSON-encoded list
    release_year: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    runtime: Mapped[int] = mapped_column(Integer, nullable=True)  # in minutes
    imdb_rating: Mapped[float] = mapped_column(Float, nullable=True, index=True)
    imdb_id: Mapped[str] = mapped_column(String(20), nullable=True)
    rt_score: Mapped[float] = mapped_column(Float, nullable=True)
    vote_count: Mapped[int] = mapped_column(Integer, nullable=True)
    popularity: Mapped[float] = mapped_column(Float, nullable=True, index=True)
    poster_path: Mapped[str] = mapped_column(String(500), nullable=True)
    backdrop_path: Mapped[str] = mapped_column(String(500), nullable=True)
    keywords: Mapped[str] = mapped_column(Text, nullable=True)  # JSON-encoded list
    language: Mapped[str] = mapped_column(String(10), nullable=True)
    budget: Mapped[int] = mapped_column(Integer, nullable=True)
    revenue: Mapped[int] = mapped_column(Integer, nullable=True)
    embedding_vector: Mapped[str] = mapped_column(Text, nullable=True)  # serialized numpy array
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    ratings = relationship("Rating", back_populates="movie", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Movie(id={self.id}, title={self.title}, year={self.release_year})>"
