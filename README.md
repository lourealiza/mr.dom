# MrDom SDR MVP

Automação de prospecção (SDR) com FastAPI, integrando Chatwoot, OpenAI e N8N para qualificação e atendimento automatizado de leads.

## Visão Geral

- Fluxo: Chatwoot (webhook) → API (Worker/State Machine) → OpenAI/N8N → resposta no Chatwoot.
- A API expõe um webhook AgentBot do Chatwoot, valida a assinatura HMAC, mantém estado simples da conversa e executa ações (responder, handoff, disparar workflows no N8N).
- Observabilidade via Prometheus em `/metrics` e logs estruturados JSON.

## Estrutura do Projeto

```text
mrdom-sdr-mvp/
├── api/
│   ├── main.py                 # FastAPI app
│   ├── routers/
│   │   ├── chatwoot_agentbot.py# Webhook Chatwoot (HMAC)
│   │   └── health.py           # Health/readiness
│   ├── services/
│   │   ├── chatwoot_client.py  # Cliente Chatwoot
│   │   ├── n8n_client.py       # Cliente/trigger N8N
│   │   └── openai_client.py    # Cliente OpenAI
│   └── domain/                 # Lógica do bot e modelos
├── app/core/                   # Config/log/middlewares
├── compose/                    # Dockerfile & docker-compose
├── env.example                 # Exemplo de .env
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

## Ambiente (.env)

| Variável | Obrigatório/Default | Descrição |
|---|---|---|
| `APP_ENV` | default `dev` | Ambiente de execução (`dev` | `prod`). |
| `APP_PORT` | default `8000` | Porta do servidor Uvicorn. |
| `CHATWOOT_BASE_URL` | required | URL base do Chatwoot (ex.: `https://app.chatwoot.com`). |
| `CHATWOOT_WEBHOOK_SECRET` | required | Segredo HMAC para validar o webhook do Chatwoot. |
| `OPENAI_API_KEY` | required | Chave da API OpenAI (análises e respostas). |
| `N8N_BASE_URL` | opcional | URL base do N8N (ex.: `http://localhost:5678`). |
| `REDIS_URL` | opcional | Redis para caches/deduplicação e rate limit (ex.: `redis://redis:6379/0`). |
| `PROMETHEUS_ENABLED` | default `true` | Habilita métricas em `/metrics`. |
| `DEDUPE_TTL_SECONDS` | default `300` | Janela de idempotência (segundos) para dedupe do webhook. |
| `RATE_LIMIT_REQUESTS` | default `60` | Limite de requisições por janela (por IP) no webhook. |
| `RATE_LIMIT_WINDOW` | default `60` | Janela do rate limit em segundos. |

Outras variáveis úteis: `OPENAI_MODEL`, `CHATWOOT_ACCESS_TOKEN`, `CHATWOOT_ACCOUNT_ID`, `ALLOWED_ORIGINS`, `N8N_API_KEY`, `N8N_WEBHOOK_*` (ver `env.example`).

## Rodar Localmente

1) Instalar dependências e iniciar a API (Uvicorn)

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

2) Docker Compose

```bash
cd compose
docker-compose up -d --build
```

Endpoints úteis:
- Health: `GET http://localhost:8000/api/v1/health`
- Readiness: `GET http://localhost:8000/api/v1/readiness`
- Metrics: `GET http://localhost:8000/metrics`

## Testes, Lint e Typecheck

```bash
# Testes
pytest

# Lint
flake8 .

# Typecheck
mypy api app
```

Opcional (formatação): `black .` e `isort .`.

## Observabilidade

- Métricas: expostas em `GET /metrics` (Prometheus exposition format) via `prometheus_fastapi_instrumentator`.
- Exemplo de scrape no Prometheus:

```yaml
scrape_configs:
  - job_name: mrdom-sdr-api
    scrape_interval: 15s
    static_configs:
      - targets: ['api:8000']   # ajuste para seu host/porta
        labels:
          service: mrdom-sdr
```

Consultas PromQL úteis (exemplos):
- Latência p95 por rota: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))`
- Taxa de erros (4xx/5xx): `sum by (path) (rate(http_request_duration_seconds_count{status=~"4..|5.."}[5m])) / sum by (path) (rate(http_request_duration_seconds_count[5m]))`
- Throughput por rota: `sum by (method, path) (rate(http_request_duration_seconds_count[1m]))`

Consultas PromQL úteis (23 exemplos):
- Throughput por rota: `sum by (method, path) (rate(http_request_duration_seconds_count[1m]))`
- Throughput global: `sum(rate(http_request_duration_seconds_count[1m]))`
- RPS por método: `sum by (method) (rate(http_request_duration_seconds_count[1m]))`
- Latência p50 por rota: `histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))`
- Latência p90 por rota: `histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))`
- Latência p95 por rota: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))`
- Latência p99 por rota: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))`
- Latência média por rota: `sum by (path) (rate(http_request_duration_seconds_sum[5m])) / sum by (path) (rate(http_request_duration_seconds_count[5m]))`
- Latência p95 global: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
- Latência mediana global: `histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
- Top 5 rotas mais lentas (p95): `topk(5, histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path)))`
- Top 5 rotas com mais tráfego: `topk(5, sum by (path) (rate(http_request_duration_seconds_count[1m])))`
- Erros 5xx por rota: `sum by (path) (rate(http_request_duration_seconds_count{status=~"5.."}[5m]))`
- Erros 4xx por rota: `sum by (path) (rate(http_request_duration_seconds_count{status=~"4.."}[5m]))`
- Taxa de erro global: `sum(rate(http_request_duration_seconds_count{status=~"4..|5.."}[5m])) / sum(rate(http_request_duration_seconds_count[5m]))`
- Distribuição de status: `sum by (status) (rate(http_request_duration_seconds_count[5m]))`
- Latência p95 (apenas 2xx): `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{status=~"2.."}[5m])) by (le, path))`
- Latência p95 (apenas 5xx): `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{status=~"5.."}[5m])) by (le, path))`
- SLA 95% < 300ms (global): `sum(rate(http_request_duration_seconds_bucket{le="0.3"}[5m])) / sum(rate(http_request_duration_seconds_count[5m]))`
- Tempo total gasto por rota: `sum by (path) (rate(http_request_duration_seconds_sum[5m]))`
- Tamanho médio da resposta: `sum by (path) (rate(http_response_size_bytes_sum[5m])) / sum by (path) (rate(http_response_size_bytes_count[5m]))`
- Requests por status 2xx: `sum(rate(http_request_duration_seconds_count{status=~"2.."}[5m]))`
- Requests por status 4xx: `sum(rate(http_request_duration_seconds_count{status=~"4.."}[5m]))`
- Requests por status 5xx: `sum(rate(http_request_duration_seconds_count{status=~"5.."}[5m]))`

## Segurança

- CORS restrito: configure origens em `ALLOWED_ORIGINS` (padrão `http://localhost:3000`).
- Rate limit: limitador básico embutido no endpoint do webhook (por IP, janela fixa). Recomenda-se reforçar também no gateway/proxy (Nginx/Envoy/Cloudflare).
- Webhook HMAC: obrigatório `CHATWOOT_WEBHOOK_SECRET` (ver especificação abaixo).
- Logs: estruturados em JSON; evite registrar PII/segredos e desabilite body logs em produção.

## Versionamento

- Prefixo estável: `/api/v1`.
- Breaking changes apenas em nova major (`/api/v2`).
- Depreciação: rotas marcadas serão mantidas por 60 dias com aviso em changelog e, opcionalmente, cabeçalho `Deprecation`.

## Contribuição

- Commits: padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, ...).
- Pre-commit (opcional): configure hooks para `flake8`, `mypy`, `black`, `isort`.
- Rodando testes localmente: `pytest` (ver seção de Testes/Lint/Typecheck).

## Especificação do Webhook (Chatwoot AgentBot)

- Endpoint: `POST /api/v1/webhooks/agentbot`
- Assinatura: cabeçalho `X-Chatwoot-Signature = hex(hmac_sha256(SECRET, raw_body))`
  - O corpo deve ser assinado na forma crua (bytes do request), sem reformatar JSON.
- Content-Type: `application/json`
- Códigos de resposta:
  - `200 OK` (processado/ignorado conforme evento)
  - `401` assinatura inválida
  - `429` rate limited (se configurado no gateway)
  - `5xx` falha inesperada
- Idempotência: deduplicação por `event_id` com TTL (default 300s) — implementado com Redis (`REDIS_URL`).
  - Se `REDIS_URL` não estiver configurado, dedupe e rate limit ficam desabilitados (fail-open).

Exemplo (pseudo) de geração de assinatura no cliente:

```python
import hmac, hashlib
sig = hmac.new(SECRET.encode(), raw_body_bytes, hashlib.sha256).hexdigest()
headers = {"X-Chatwoot-Signature": sig, "Content-Type": "application/json"}
```

Configuração no Chatwoot: aponte o webhook para `https://seu-host/api/v1/webhooks/agentbot` e habilite eventos relevantes (ex.: `message_created`).

---

Para dúvidas ou melhorias, abra uma issue ou PR.
