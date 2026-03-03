"""Redis Cache Service — centralized caching layer with graceful fallback."""

import json
import logging
from typing import Optional, Any
from datetime import timedelta

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class CacheService:
    """Async Redis cache for CineMatch. Falls back to in-memory dict if Redis unavailable."""

    _instance: Optional["CacheService"] = None
    _client: Any = None
    _fallback: dict = {}
    _use_fallback: bool = False

    @classmethod
    async def get_instance(cls) -> "CacheService":
        """Singleton accessor."""
        if cls._instance is None:
            cls._instance = cls()
            try:
                import redis.asyncio as redis
                cls._client = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                )
                # Test connection
                await cls._client.ping()
                logger.info("✅ Redis connected")
            except Exception as e:
                logger.warning(f"⚠️ Redis unavailable ({e}), using in-memory fallback")
                cls._use_fallback = True
                cls._client = None
        return cls._instance

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache, JSON-deserialized."""
        if self._use_fallback:
            val = self._fallback.get(key)
            if val is not None:
                try:
                    return json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    return val
            return None

        try:
            val = await self._client.get(key)
            if val is not None:
                try:
                    return json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    return val
        except Exception:
            pass
        return None

    async def set(
        self, key: str, value: Any, ttl: Optional[timedelta] = None
    ) -> None:
        """Set a value in cache, JSON-serialized."""
        serialized = json.dumps(value, default=str)

        if self._use_fallback:
            self._fallback[key] = serialized
            return

        try:
            if ttl:
                await self._client.setex(key, int(ttl.total_seconds()), serialized)
            else:
                await self._client.set(key, serialized)
        except Exception:
            # Fallback to memory
            self._fallback[key] = serialized

    async def delete(self, key: str) -> None:
        """Delete a key from cache."""
        if self._use_fallback:
            self._fallback.pop(key, None)
            return
        try:
            await self._client.delete(key)
        except Exception:
            pass

    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        if self._use_fallback:
            return key in self._fallback
        try:
            return bool(await self._client.exists(key))
        except Exception:
            return False

    async def increment(self, key: str) -> int:
        """Increment a counter."""
        if self._use_fallback:
            val = int(self._fallback.get(key, 0)) + 1
            self._fallback[key] = str(val)
            return val
        try:
            return await self._client.incr(key)
        except Exception:
            return 0

    async def flush_pattern(self, pattern: str) -> None:
        """Delete all keys matching a pattern."""
        if self._use_fallback:
            keys_to_delete = [k for k in self._fallback if pattern.replace("*", "") in k]
            for k in keys_to_delete:
                del self._fallback[k]
            return
        try:
            async for key in self._client.scan_iter(match=pattern):
                await self._client.delete(key)
        except Exception:
            pass

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._client and not self._use_fallback:
            try:
                await self._client.close()
            except Exception:
                pass
