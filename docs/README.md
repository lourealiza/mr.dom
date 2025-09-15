# MR.DOM — Documentação

Bem-vindo à documentação do MR.DOM (SDR Automation). Aqui você encontra visão geral, instruções de uso, APIs públicas, clientes (Chatwoot, N8N, OpenAI), domínio (BotLogic e modelos) e exemplos de integração.

## Sumário

- [Visão Geral](./overview.md)
- [Guia de Início Rápido](./getting-started.md)
- [API HTTP (FastAPI)](./api.md)
- [Componentes Públicos (App, Routers)](./components.md)
- [Serviços/Clientes (Chatwoot, N8N, OpenAI)](./services.md)
- [Domínio e Modelos (BotLogic, States, Enums)](./domain.md)
- [Core (Settings, Logging, Middlewares, Worker)](./core.md)
- [Guias de Uso](./usage-guides.md)
- [Exemplos de Integração](./examples.md)

## TL;DR — Subindo localmente

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints úteis:

- OpenAPI/Swagger: `http://localhost:8000/docs`
- Health: `GET http://localhost:8000/api/v1/health`
- Readiness: `GET http://localhost:8000/api/v1/readiness`
- Webhook Chatwoot: `POST http://localhost:8000/api/v1/webhooks/agentbot`
- Métricas Prometheus: `GET http://localhost:8000/metrics`

Consulte os detalhes de cada endpoint em [API HTTP](./api.md).

