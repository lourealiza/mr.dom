from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request

# Load environment variables from project root .env
load_dotenv(Path(__file__).parent / ".env")

# Reuse the existing router and handler from the project
from api.routers.chatwoot_token_webhook import (
    router as cw_router,
    cw_token_webhook as cw_handler,
)


app = FastAPI(title="Mr. DOM SDR API – Token Webhook Only")

# Keep the same API prefix used in the main app
app.include_router(cw_router, prefix="/api/v1/webhooks", tags=["webhooks"])


@app.post("/api/v1/webhooks/webhook/{token}")
async def cw_alias(token: str, request: Request):
    """Alias route that delegates to the shared handler."""
    return await cw_handler(token, request)

