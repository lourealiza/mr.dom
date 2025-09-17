from __future__ import annotations

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file.

    Uses Pydantic v2 `BaseSettings` and `SettingsConfigDict` to load values
    from an `.env` file placed at the repository root (or from environment).
    """

    # App
    APP_ENV: str = "dev"
    APP_PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # DB
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "app"
    DB_USER: str = "app"
    DB_PASSWORD: str = "change-me"

    # Redis / Rate limiting / Idempotency
    REDIS_URL: str = "redis://redis:6379/0"
    DEDUPE_TTL_SECONDS: int = 300
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Chatwoot
    CHATWOOT_WEBHOOK_SECRET: str

    # Observability
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True

    # Pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Return a SQLAlchemy-compatible database URL."""
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
