# Visão Geral

O MR.DOM é um sistema de automação de vendas (SDR) com integrações a Chatwoot, N8N e OpenAI, focado em qualificação de leads, respostas automatizadas e handoff para humanos quando necessário.

## Arquitetura (alto nível)

- API (FastAPI): endpoints REST para saúde, readiness, webhooks e métricas.
- Routers: `api/routers/health.py` e `api/routers/chatwoot_agentbot.py`.
- Domínio: `api/domain/` com `bot_logic.py` (BotLogic, fluxo de passos) e `models.py` (Pydantic models e enums).
- Serviços/Clientes: `api/services/` com integrações a Chatwoot, N8N e OpenAI.
- Core: `app/core/` com Settings (config), Middlewares e Logging.
- Worker: `app/workers/worker.py` (exemplo de RQ + Redis).
- Observabilidade: métricas Prometheus via `prometheus-fastapi-instrumentator` e logs estruturados (structlog).

## Principais Fluxos

1. Webhook do Chatwoot chama `POST /api/v1/webhooks/agentbot`.
2. O handler valida a assinatura HMAC, carrega `State` da conversa, processa com `step_transition` (ou BotLogic), persiste o novo estado e executa ações (responder, mudar status, disparar N8N).
3. Serviços auxiliares realizam chamadas externas: Chatwoot API, N8N (workflows) e OpenAI (análises, respostas, follow-up).

## Padrões e Tecnologias

- Python 3.11+, FastAPI, Pydantic v2.
- httpx para HTTP assíncrono.
- OpenAI SDK assíncrono.
- Estrutura de variáveis de ambiente via Pydantic Settings.
- Logs estruturados em JSON.
- Métricas compatíveis com Prometheus.

Consulte [Getting Started](./getting-started.md) para instalar e configurar.