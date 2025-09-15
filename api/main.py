
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env'))

# Import routers
from .routers.chatwoot_agentbot import router as chatwoot_router
from .routers.health import router as health_router

# Import core configuration
from app.core.logging import configure_logging
from app.core.middlewares import add_middlewares

# Configure logging
configure_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Mr. DOM SDR API",
    version="1.0.0",
    description="SDR Automation API with Chatwoot and OpenAI integration"
)

# Add middlewares
add_middlewares(app)

# Include routers with proper prefixes and tags
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["platform"]
)
app.include_router(
    chatwoot_router,
    prefix="/api/v1/webhooks",
    tags=["webhooks"]
)

# Setup Prometheus metrics
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False
)
def health():
    return {"ok": True}
