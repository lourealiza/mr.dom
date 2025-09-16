from __future__ import annotations

from typing import Optional, Tuple
import re

from redis.asyncio import Redis  # type: ignore

from app.core.settings import settings


_redis: Optional[Redis] = None


def _normalize_redis_url(raw: str) -> str:
    """Normalize various Redis URL forms to a standard redis://host:port/db.

    Accepts:
    - Full URLs: redis://host:port/db or rediss://host:port/db (unchanged)
    - redis://host:port (appends /0)
    - redis:host:port[:db]
    - host:port[:db]
    - host (defaults to :6379/0)
    """
    if not raw:
        return ""
    s = raw.strip()
    low = s.lower()

    if low.startswith("redis://") or low.startswith("rediss://"):
        # If missing db path, append /0
        if re.match(r"^rediss?://[^/]+$", s, flags=re.IGNORECASE):
            return s + "/0"
        return s

    if low.startswith("redis:"):
        rest = s.split(":", 1)[1]
        parts = rest.split(":")
        host = parts[0] if parts and parts[0] else "localhost"
        port = parts[1] if len(parts) >= 2 and parts[1] else "6379"
        db = parts[2] if len(parts) >= 3 and parts[2].isdigit() else "0"
        return f"redis://{host}:{port}/{db}"

    if low.startswith("rediss:"):
        rest = s.split(":", 1)[1]
        parts = rest.split(":")
        host = parts[0] if parts and parts[0] else "localhost"
        port = parts[1] if len(parts) >= 2 and parts[1] else "6379"
        db = parts[2] if len(parts) >= 3 and parts[2].isdigit() else "0"
        return f"rediss://{host}:{port}/{db}"

    parts = s.split(":")
    if len(parts) >= 2 and parts[1].isdigit():
        host = parts[0]
        port = parts[1]
        db = parts[2] if len(parts) >= 3 and parts[2].isdigit() else "0"
        return f"redis://{host}:{port}/{db}"

    # Only host provided
    return f"redis://{s}:6379/0"


async def get_redis() -> Optional[Redis]:
    global _redis
    if not settings.REDIS_URL:
        return None
    if _redis is None:
        url = _normalize_redis_url(settings.REDIS_URL)
        _redis = Redis.from_url(url, decode_responses=True)
    return _redis


async def dedupe_once(key: str, ttl_seconds: int) -> bool:
    """Return True if this is the first time the key is seen within TTL.

    Uses Redis SET NX with expiration to guarantee one-time processing per key.
    If Redis is unavailable or not configured, returns True (do not block).
    """
    r = await get_redis()
    if not r:
        return True
    try:
        ok = await r.set(key, "1", ex=ttl_seconds, nx=True)
        return bool(ok)
    except Exception:
        # Fail-open in case of Redis error
        return True


async def rate_limit(bucket: str, limit: int, window_seconds: int) -> Tuple[bool, int]:
    """Simple fixed-window rate limiter.

    Returns (allowed, remaining). If Redis isn't available, allow request.
    """
    r = await get_redis()
    if not r:
        return True, limit
    try:
        count = await r.incr(bucket)
        if count == 1:
            await r.expire(bucket, window_seconds)
        allowed = count <= limit
        remaining = max(limit - count, 0)
        return allowed, remaining
    except Exception:
        # Fail-open on error
        return True, limit


__all__ = ["get_redis", "dedupe_once", "rate_limit"]
