# Guias de Uso

Este guia reúne instruções práticas de configuração e integração.

## 1) Integrar com Chatwoot (AgentBot)

1. Defina variáveis no `.env`:
   - `CHATWOOT_BASE_URL`, `CHATWOOT_ACCESS_TOKEN`, `CHATWOOT_ACCOUNT_ID`
   - `CHATWOOT_HMAC_SECRET` (ou `HMAC_SECRET`)
2. No Chatwoot, crie/edite o bot e configure o webhook para:
   - URL: `https://seu-host/api/v1/webhooks/agentbot`
   - Eventos: inclua ao menos `message_created`.
3. Garanta que o Chatwoot envie o header `X-Chatwoot-Signature` usando o segredo configurado.
4. Teste localmente com `curl` ou script, calculando o HMAC do corpo.

Dicas:
- Mensagens `outgoing` são ignoradas (evita loop).
- `custom_attributes` guarda o `State` da conversa.

## 2) Disparar Workflows no N8N

Opção A — Webhook público/privado:

```python
from api.services.n8n_client import trigger
await trigger("create_lead", {"nome": "Ana", "email": "ana@ex.com"})
```

Opção B — API com chave (`N8N_API_KEY`):

```python
from api.services.n8n_client import N8NClient
n8n = N8NClient()
await n8n.trigger_workflow("lead-qualification", {"lead_id": 42})
```

Workflows comuns esperados:
- `create_lead`, `schedule_meeting`, `lead-qualification`, `initial-qualification`, `follow-up`, `crm-sync`, `email-sequence`.

## 3) OpenAI — Habilitar e Validar

- Defina `OPENAI_API_KEY` (obrigatório) e opcionalmente `OPENAI_MODEL`.
- Teste:

```python
from api.services.openai_client import OpenAIClient
client = OpenAIClient()
text = await client.generate_response("Quais os planos?", {"intent": "question"})
```

Tratamento de erros: verifique limites de uso e variável de ambiente.

## 4) Personalizar o Bot

Variáveis consumidas por `BotLogic`:

- `BOT_WELCOME_MESSAGE` — mensagem de boas‑vindas.
- `ESCALATION_KEYWORDS` — JSON array de palavras‑chave (ex.: `["falar com humano", "atendente"]`).
- `AUTO_RESPONSE_ENABLED` — `true`/`false`.
- `QUALIFICATION_QUESTIONS` — JSON array de perguntas.
- `BUSINESS_HOURS` — JSON com `{ "start": "09:00", "end": "18:00" }`.
- `TIMEZONE` — ex.: `America/Sao_Paulo`.

## 5) Observabilidade

- Métricas: `GET /metrics` (Prometheus scrape).
- Logs JSON com `structlog` — configure o nível via `configure_logging` se necessário.

## 6) Produção

- Habilite HTTPS no proxy/reverso.
- Restrinja CORS via `ALLOWED_ORIGINS`.
- Proteja segredos: use gerenciadores de secrets/variáveis.
- Monitore readiness e métricas em seu orquestrador.