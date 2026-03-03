"""
CineMatch AI Backend — Main Application Entry Point.

An AI-powered movie intelligence SaaS platform.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.database import engine, Base
from app.core.rate_limit import limiter
from app.services.cache_service import CacheService
from app.services.semantic_search import SemanticSearchService
from app.services.recommendation_engine import RecommendationEngine
from app.background.scheduler import start_scheduler, stop_scheduler

# ─── Import all models so Base.metadata knows about them ───
from app.models import user, movie, rating, subscription, streaming_alert  # noqa: F401

# ─── Routers ───
from app.routers import auth, users, movies, recommendations, social, admin

settings = get_settings()

# ─── Logging ───
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("cinematch")


# ─── Lifespan (startup + shutdown) ───
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — runs on startup and shutdown."""
    logger.info("🚀 CineMatch AI Backend starting up...")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created")

    # Initialize Redis / Cache
    await CacheService.get_instance()

    # Initialize FAISS / Semantic Search
    try:
        search_service = await SemanticSearchService.get_instance()
        await search_service.initialize()
        logger.info("✅ Semantic search initialized")
    except Exception as e:
        logger.warning(f"⚠️ Semantic search init skipped: {e}")

    # Initialize Recommendation Engine
    try:
        reco_engine = RecommendationEngine()
        await reco_engine.initialize()
        logger.info("✅ Recommendation engine initialized")
    except Exception as e:
        logger.warning(f"⚠️ Recommendation engine init skipped: {e}")

    # Start background scheduler
    start_scheduler()

    logger.info("🎬 CineMatch AI Backend is ready!")

    yield

    # ─── Shutdown ───
    logger.info("👋 Shutting down CineMatch AI Backend...")
    stop_scheduler()
    cache_instance = await CacheService.get_instance()
    await cache_instance.close()
    logger.info("✅ Cleanup complete")


# ─── Create App ───
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered movie intelligence SaaS platform",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ─── Middleware ───

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ─── Global Exception Handler ───
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
        },
    )


# ─── API Request Counter Middleware ───
@app.middleware("http")
async def count_requests(request: Request, call_next):
    """Count total API requests for admin analytics."""
    response = await call_next(request)
    try:
        cache = await CacheService.get_instance()
        await cache.increment("stats:api_requests")
    except Exception:
        pass  # Don't let counter failures break requests
    return response


# ─── Health Check ───
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Docker and load balancers."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# ─── Register Routers ───
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(movies.router, prefix=settings.API_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_PREFIX)
app.include_router(social.router, prefix=settings.API_PREFIX)
app.include_router(admin.router, prefix=settings.API_PREFIX)


# ─── Root ───
@app.get("/", tags=["Root"])
async def root():
    """API info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
        "health": "/health",
    }
