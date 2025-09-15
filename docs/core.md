# Core

Documentação dos módulos em `app/core/` e worker.

## Settings — `app/core/settings.py`

Carrega configuração via Pydantic Settings. Principais campos:

- App: `APP_ENV`, `APP_PORT`, `ALLOWED_ORIGINS`
- DB: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` e `database_url` (propriedade)
- Redis: `REDIS_URL`
- Chatwoot: `CHATWOOT_WEBHOOK_SECRET`
- Observabilidade: `SENTRY_DSN`, `PROMETHEUS_ENABLED`

Uso:

```python
from app.core.settings import settings
print(settings.APP_ENV)
```

## Middlewares — `app/core/middlewares.py`

Registra middlewares comuns na aplicação FastAPI:

- `CorrelationIdMiddleware` para request IDs
- `GZipMiddleware` para respostas grandes
- `CORSMiddleware` configurado via `ALLOWED_ORIGINS`

Uso:

```python
from app.core.middlewares import add_middlewares
add_middlewares(app)
```

## Logging — `app/core/logging.py`

Configura `structlog` com saída JSON e integração com stdlib logging.

- Função: `configure_logging(level: int = logging.INFO) -> None`
- Idempotente: seguro chamar múltiplas vezes

## Worker — `app/workers/worker.py`

Exemplo de worker com RQ + Redis:

- Listas: `listen = ["events"]`
- Conexão: `Redis.from_url(settings.REDIS_URL)`
- Execução: `python -m app.workers.worker`

## Métricas

A API expõe métricas em `/metrics` via `prometheus-fastapi-instrumentator`. Útil para scraping por Prometheus.