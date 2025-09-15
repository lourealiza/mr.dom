# API HTTP (FastAPI)

A API expõe endpoints REST para saúde do serviço, readiness (checagens externas), webhooks do Chatwoot e métricas para Prometheus. A documentação interativa está disponível em `/docs` e o schema em `/openapi.json`.

Base URL (local): `http://localhost:8000`

## Health

- Método: GET
- Caminho: `/api/v1/health`
- Resposta 200:

```json
{"status": "ok"}
```

## Readiness

- Método: GET
- Caminho: `/api/v1/readiness`
- Descrição: checa conectividade com Chatwoot, N8N e Redis (se configurados)
- Exemplo de resposta 200:

```json
{
  "status": "ready",
  "services": {
    "chatwoot": "connected|not_configured",
    "n8n": "connected|not_configured",
    "redis": "connected|not_configured|unavailable|error"
  }
}
```

- Respostas de erro: 503 (dependência indisponível), 500 (erro interno)

## Webhook — Chatwoot AgentBot

- Método: POST
- Caminho: `/api/v1/webhooks/agentbot`
- Autenticação: HMAC SHA‑256 via header `X-Chatwoot-Signature`
- Variáveis: `CHATWOOT_HMAC_SECRET` (ou `HMAC_SECRET`), `CHATWOOT_ACCOUNT_ID`
- Conteúdo: JSON do evento do Chatwoot (ex.: `message_created`)
- Comportamento:
  - Ignora mensagens de saída (`message_type == "outgoing"`).
  - Carrega `State` da conversa via Chatwoot API.
  - Aplica `step_transition(state, user_text)` para avançar o fluxo e decidir ação.
  - Persiste `State` atualizado em `custom_attributes`.
  - Executa ações: `handoff` (abre conversa), `create_lead`/`schedule` (dispara N8N) e responde ao usuário.

### Exemplo de requisição (curl)

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

### Como calcular a assinatura HMAC

```python
import hmac, hashlib
secret = b"$CHATWOOT_HMAC_SECRET"
raw_body = b"...corpo_bruto_da_requisicao..."
sign = hmac.new(secret, msg=raw_body, digestmod=hashlib.sha256).hexdigest()
# envie sign em X-Chatwoot-Signature
```

### Exemplo de resposta

```json
{"ok": true}
```

## Métricas Prometheus

- Método: GET
- Caminho: `/metrics`
- Descrição: métricas padrão do FastAPI/Starlette. Não aparece no schema OpenAPI.

## Códigos de status

- 200: sucesso
- 401: assinatura HMAC inválida no webhook
- 503: dependência externa indisponível (readiness)
- 500: erro interno