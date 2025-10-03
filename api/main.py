
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Load environment variables from repository root .env (if present)
_repo_root = Path(__file__).resolve().parents[1]
_env_path = _repo_root / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

# Import routers
from .routers.chatwoot_agentbot import router as chatwoot_router
from .routers.health import router as health_router
from .routers.assistant_preview import router as assistant_router

# Importar AgentOS routers (comentado - descomentar quando agno estiver instalado)
# from .routers.agents import router as agents_router

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

# Assistant preview (UAT)
app.include_router(
    assistant_router,
    prefix="/api/v1",
    tags=["assistant"]
)

# AgentOS routers (descomentar quando agno estiver instalado e configurado)
# app.include_router(
#     agents_router,
#     prefix="/api/v1/agents",
#     tags=["agents"]
# )

# Setup Prometheus metrics
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False
)
