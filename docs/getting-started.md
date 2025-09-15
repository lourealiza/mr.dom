# Guia de Início Rápido

## Pré‑requisitos

- Python 3.11+
- (Opcional) Docker e Docker Compose
- Credenciais para integrações: OpenAI, Chatwoot e N8N (opcional)

## Configuração de ambiente

1. Copie o exemplo e edite credenciais:

```bash
cp env.example .env
# Edite .env com suas chaves/URLs
```

2. Variáveis importantes (ver `env.example`):

- Chatwoot: `CHATWOOT_BASE_URL`, `CHATWOOT_ACCESS_TOKEN`, `CHATWOOT_ACCOUNT_ID`, `CHATWOOT_HMAC_SECRET`
- OpenAI: `OPENAI_API_KEY`, `OPENAI_MODEL`
- N8N: `N8N_BASE_URL`, `N8N_API_KEY` ou `N8N_BASIC_AUTH_USER`/`N8N_BASIC_AUTH_PASSWORD`
- Redis (opcional): `REDIS_URL`

## Executar localmente

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger/OpenAPI: `http://localhost:8000/docs`
- Métricas: `http://localhost:8000/metrics`

## Executar com Docker

```bash
cd compose
docker-compose up -d --build
```

O serviço expõe a API e integrações. Ajuste as variáveis no `.env` conforme necessário.

## Testes

```bash
pytest
```

## Troubleshooting

- 401 no webhook: valide o `CHATWOOT_HMAC_SECRET` e a assinatura `X-Chatwoot-Signature`.
- 503 em readiness: verifique conectividade com Chatwoot e N8N e credenciais.
- OpenAI errors: confira `OPENAI_API_KEY` e limites de uso.