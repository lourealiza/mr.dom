from __future__ import annotations

import os
import hmac
import hashlib
import json
from typing import Any, Dict

from fastapi import APIRouter, Request, HTTPException

from app.core.cache import dedupe_once, rate_limit
from app.core.settings import settings


router = APIRouter()


SHARED_SECRET = (
    os.getenv("CHATWOOT_WEBHOOK_SHARED_SECRET")
    or os.getenv("CHATWOOT_WEBHOOK_SECRET")
    or os.getenv("HMAC_SECRET")
    or ""
)

# TTL for idempotency (seconds). Default to global settings if not provided.
IDEMPOTENCY_TTL = int(os.getenv("CHATWOOT_WEBHOOK_IDEMPOTENCY_TTL") or settings.DEDUPE_TTL_SECONDS)

# Per-token rate limit per minute (optional). Fallback to global limit.
TOKEN_RATE_LIMIT = int(os.getenv("CHATWOOT_WEBHOOK_RATE_LIMIT") or settings.RATE_LIMIT_REQUESTS)


def _dedupe_key(body: Dict[str, Any]) -> str:
    mid = body.get("id") or (body.get("message") or {}).get("id")
    acc = (body.get("account") or {}).get("id")
    if acc and mid:
        return f"{acc}:{mid}"
    return ""


@router.post("/token/{token}")
async def cw_token_webhook(token: str, request: Request):
    if not SHARED_SECRET or token != SHARED_SECRET:
        raise HTTPException(status_code=401, detail="invalid token")

    # Rate limit per token (1-minute window)
    allowed, _ = await rate_limit(
        f"rl:token:{token}", TOKEN_RATE_LIMIT, 60
    )
    if not allowed:
        raise HTTPException(status_code=429, detail="rate limited")

    raw = await request.body()

    sig = request.headers.get("X-Chatwoot-Signature")
    if sig:
        mac = hmac.new(SHARED_SECRET.encode(), msg=raw, digestmod=hashlib.sha256)
        if not hmac.compare_digest(sig, mac.hexdigest()):
            raise HTTPException(status_code=401, detail="bad signature")

    try:
        body = json.loads(raw.decode("utf-8"))
    except Exception:
        body = {}

    key = _dedupe_key(body)
    if key:
        first = await dedupe_once(f"dedupe:token:{key}", IDEMPOTENCY_TTL)
        if not first:
            return {"ok": True, "duplicate": True}

    return {"ok": True}

# Alias route that calls the same handler
router.add_api_route(
    "/webhook-test/{token}", cw_token_webhook, methods=["POST"], name="cw_token_webhook_alias"
)
