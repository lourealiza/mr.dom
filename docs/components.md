# Componentes Públicos

Esta seção descreve componentes expostos pela aplicação (app e routers) e como usá-los.

## Aplicação FastAPI — `api/main.py`

- Instância: `app` (FastAPI)
- Rotas inclusas com prefixos:
  - Plataforma: `api/routers/health.py` em `/api/v1` (tags: platform)
  - Webhooks: `api/routers/chatwoot_agentbot.py` em `/api/v1/webhooks` (tags: webhooks)
- Métricas Prometheus expostas em `/metrics`.

Execução local:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Router: Health — `api/routers/health.py`

### `GET /api/v1/health` — `health_check()`

- Verifica se o serviço está operacional.
- Resposta 200: `{ "status": "ok" }`

### `GET /api/v1/readiness` — `readiness_check()`

- Verifica conectividade com Chatwoot, N8N e Redis (se configurados).
- Retorna mapa de serviços com status.

Exemplo:

```bash
curl http://localhost:8000/api/v1/readiness
```

---

## Router: AgentBot (Chatwoot) — `api/routers/chatwoot_agentbot.py`

### `POST /api/v1/webhooks/agentbot` — `agentbot()`

- Requer header `X-Chatwoot-Signature` (HMAC SHA‑256 do corpo bruto) usando `CHATWOOT_HMAC_SECRET`.
- Fluxo:
  1. `verify_request(req)` valida HMAC.
  2. Lê `State` atual via `ChatwootClient.get_conversation()`.
  3. Processa mensagem com `step_transition(state, user_text)`.
  4. Persiste novo `State` e toma ações: `handoff`, `create_lead`, `schedule` (N8N) e `reply`.

Exemplo (curl):

```bash
curl -X POST \
  http://localhost:8000/api/v1/webhooks/agentbot \
  -H "Content-Type: application/json" \
  -H "X-Chatwoot-Signature: <hex_hmac_do_body>" \
  -d '{
    "event": "message_created",
    "account": {"id": "<ACCOUNT_ID>"},
    "conversation": {"id": 123},
    "message": {"content": "Oi, sou a Ana", "message_type": "incoming"}
  }'
```

Cálculo do HMAC (Python):

```python
import hmac, hashlib
secret = b"$CHATWOOT_HMAC_SECRET"
raw_body = b"...corpo_bruto_da_requisicao..."
sign = hmac.new(secret, msg=raw_body, digestmod=hashlib.sha256).hexdigest()
```

> Para detalhes dos modelos usados (`State`, enums), veja [Domínio e Modelos](./domain.md). Para integrações, veja [Serviços](./services.md).