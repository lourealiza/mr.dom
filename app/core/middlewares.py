from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from asgi_correlation_id import CorrelationIdMiddleware

from app.core.settings import settings


def add_middlewares(app: FastAPI) -> None:
    """Register common middlewares on the FastAPI application."""

    # correlation id (request id) support
    app.add_middleware(CorrelationIdMiddleware)

    # gzip responses for large payloads
    app.add_middleware(GZipMiddleware, minimum_size=1024)

    # CORS
    allow_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


__all__ = ["add_middlewares"]
