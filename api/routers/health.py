from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

import httpx
import os
import importlib.util

# Import redis with fallback
try:
    import redis
    has_redis = True
except ImportError:
    redis = None
    has_redis = False

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Basic health check endpoint"""
    return {"status": "ok"}

@router.get("/readiness")
async def readiness_check() -> Dict[str, str]:
    """Readiness probe that checks external service connectivity"""
    try:
        # Check Chatwoot connection
        chatwoot_url = os.getenv("CHATWOOT_BASE_URL")
        chatwoot_token = os.getenv("CHATWOOT_ACCESS_TOKEN")
        
        if chatwoot_url and chatwoot_token:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {chatwoot_token}"}
                response = await client.get(f"{chatwoot_url}/api/v1/profile", headers=headers)
                response.raise_for_status()
        
        # Check N8N connection if configured
        n8n_url = os.getenv("N8N_BASE_URL")
        n8n_key = os.getenv("N8N_API_KEY")
        
        if n8n_url and n8n_key:
            async with httpx.AsyncClient() as client:
                headers = {"X-N8N-API-KEY": n8n_key}
                response = await client.get(f"{n8n_url}/api/v1/workflows", headers=headers)
                response.raise_for_status()

        # Check Redis connection if REDIS_URL is configured and redis is available
        redis_url = os.getenv("REDIS_URL")
        redis_status = "not_configured"
        
        if redis_url:
            if has_redis and redis:
                try:
                    r = redis.from_url(redis_url)
                    r.ping()
                    redis_status = "connected"
                except Exception:
                    redis_status = "error"
            else:
                redis_status = "unavailable"
        
        return {
            "status": "ready",
            "services": {
                "chatwoot": "connected" if chatwoot_url else "not_configured",
                "n8n": "connected" if n8n_url else "not_configured",
                "redis": redis_status
            }
        }
        
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )
    except Exception as redis_error:
        if "RedisError" in str(type(redis_error).__name__):
            raise HTTPException(
                status_code=503,
                detail=f"Redis connection failed: {str(redis_error)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )