"""CineMatch AI Backend — Async Database Engine & Session."""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

# ─── Engine kwargs based on driver ───
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

_engine_kwargs = {
    "echo": settings.DEBUG,
}

if not _is_sqlite:
    # Connection pool settings (not supported by aiosqlite)
    _engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    })

# ─── Async Engine ───
engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

# ─── Session Factory ───
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ─── Base Model ───
class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""
    pass


# ─── Dependency ───
async def get_db() -> AsyncSession:
    """Yield an async database session for FastAPI dependency injection."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
