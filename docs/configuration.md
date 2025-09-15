## Configuração

Crie um arquivo `.env` na raiz (baseado em `env.example`) e defina as variáveis:

### Chatwoot
- `CHATWOOT_BASE_URL` — ex.: `https://app.chatwoot.com`
- `CHATWOOT_ACCESS_TOKEN`
- `CHATWOOT_ACCOUNT_ID`
- `CHATWOOT_HMAC_SECRET` ou `HMAC_SECRET` — validação do webhook (`X-Chatwoot-Signature`).

### OpenAI
- `OPENAI_API_KEY`
- `OPENAI_MODEL` — default: `gpt-3.5-turbo`.

### N8N
- `N8N_BASE_URL` — ex.: `http://localhost:5678`
- `N8N_API_KEY` — para chamadas de API.
- `N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD` — se usar webhooks privados.

### App/Core
- `ALLOWED_ORIGINS` — CSV de origens CORS.
- `REDIS_URL` — usado no readiness e em workers de exemplo.

### Dicas
- Não commitar `.env` ao repositório.
- Rotacione segredos e use cofre/secret manager em produção.
- Habilite métricas Prometheus via `/metrics` e monitore disponibilidade.

