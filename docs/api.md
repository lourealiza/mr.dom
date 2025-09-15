## Endpoints da API

Prefixo: `/api/v1`

### Saúde da plataforma
- `GET /api/v1/health`
  - Retorna `{ "status": "ok" }`.

- `GET /api/v1/readiness`
  - Verifica integrações configuradas: Chatwoot, N8N e Redis.
  - Respostas típicas:
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

### Webhook do Chatwoot (AgentBot)
- `POST /api/v1/webhooks/agentbot`
  - Cabeçalho de segurança: `X-Chatwoot-Signature` (HMAC SHA256 do corpo, usando `CHATWOOT_HMAC_SECRET` ou `HMAC_SECRET`).
  - Eventos aceitos: `message_created`, `message_updated`, `widget_triggered`.
  - Ignora mensagens `message_type=outgoing`.
  - Fluxo:
    1. Carrega estado salvo nos `custom_attributes` da conversa via `ChatwootClient.get_conversation`.
    2. Executa `step_transition(state, user_text)` para decidir próxima pergunta e/ou ação.
    3. Persiste novo estado com `set_attributes` e envia resposta com `reply`.
    4. Ações suportadas: `handoff`, `create_lead` (N8N `create_lead`), `schedule` (N8N `schedule_meeting`).

#### Exemplo de requisição
```bash
curl -X POST "https://seu-host/api/v1/webhooks/agentbot" \
  -H "Content-Type: application/json" \
  -H "X-Chatwoot-Signature: <hex>" \
  -d '{
    "event": "message_created",
    "account": {"id": 123},
    "conversation": {"id": 456},
    "message": {"content": "Oi, sou o João"}
  }'
```

#### Respostas
- 200 `{ "ok": true }`
- 401 `{ "detail": "invalid signature" }`

### Métricas
- `GET /metrics` (fora do schema): expõe métricas Prometheus via `prometheus-fastapi-instrumentator`.

### Considerações de Segurança
- Configure e rotacione `CHATWOOT_HMAC_SECRET`/`HMAC_SECRET`.
- Não exponha tokens nos logs. Use variáveis de ambiente e secrets do orquestrador.
- Habilite CORS apenas para domínios necessários (`ALLOWED_ORIGINS`).

