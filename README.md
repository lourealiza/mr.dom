# MrDom SDR MVP

Sistema de automação de vendas (SDR) com integração a Chatwoot, N8N e OpenAI para qualificação e atendimento automatizado de leads.

## Funcionalidades

- Integração Chatwoot: webhooks e respostas automatizadas
- IA com OpenAI: análise de intenções e geração de respostas
- Automação N8N: workflows para qualificação e follow-up
- Qualificação inteligente: análise BANT (Budget, Authority, Need, Timeline)
- Escalação automática: transferência para humano quando necessário
- API RESTful com métricas Prometheus

## Estrutura do Projeto

```
mrdom-sdr-mvp/
├─ api/
│  ├─ main.py                 # FastAPI app
│  ├─ routers/
│  │  ├─ chatwoot_agentbot.py # Webhook Chatwoot
│  │  └─ health.py            # Health/readiness
│  ├─ services/
│  │  ├─ chatwoot_client.py   # Cliente Chatwoot
│  │  ├─ n8n_client.py        # Cliente N8N
│  │  └─ openai_client.py     # Cliente OpenAI
│  └─ domain/
│     ├─ bot_logic.py         # Lógica do bot
│     └─ models.py            # Modelos de dados
├─ app/
│  ├─ core/                   # Config/log/middlewares
│  └─ workers/                # Exemplos de workers
├─ compose/
│  ├─ docker-compose.yml      # Orquestração
│  └─ Dockerfile              # Imagem da API
├─ env.example                # Exemplo de .env
├─ requirements.txt           # Dependências Python
├─ README.md                  # Este arquivo
└─ docs/                      # Documentação abrangente
```

## Instalação

### Pré‑requisitos

- Python 3.11+
- Docker e Docker Compose (opcional)
- Conta OpenAI (API key), instância Chatwoot e N8N (opcional)

### 1. Configuração de ambiente

```
cp env.example .env
# Edite .env com suas credenciais
```

### 2. Rodar local (desenvolvimento)

```
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Rodar com Docker

```
cd compose
docker-compose up -d --build
```

Notas Docker:
- O serviço monta `../api:/app` e `../app:/app/app`; o `PYTHONPATH=/app` garante que `app.core.*` seja resolvido.
- Métricas expostas em `/metrics`.

## Configuração

Defina as variáveis em `.env` (veja `env.example`). Principais:

```
# Chatwoot
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_ACCESS_TOKEN=seu_token
CHATWOOT_ACCOUNT_ID=seu_account_id

# OpenAI
OPENAI_API_KEY=sk-sua_chave
OPENAI_MODEL=gpt-3.5-turbo

# N8N (opcional)
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=seu_api_key
```

## API

- Health: `GET /api/v1/health`
- Readiness: `GET /api/v1/readiness`
- Webhook (Chatwoot AgentBot): `POST /api/v1/webhooks/agentbot`

Para configurar o webhook no Chatwoot, aponte para `https://seu-host/api/v1/webhooks/agentbot` e habilite eventos relevantes (ex.: `message_created`).

## Documentação

A documentação completa está em `docs/`. Pontos de entrada:
- `docs/README.md` (sumário)
- `docs/api.md` (endpoints HTTP)
- `docs/services.md` (clientes Chatwoot/N8N/OpenAI)
- `docs/domain.md` (BotLogic, State e modelos)
- `docs/core.md` (settings, logging, middlewares, worker)
- `docs/examples.md` (exemplos práticos)

## Testes

```
pytest
```

## Observabilidade

- Métricas Prometheus: `GET /metrics`
- Logs estruturados em JSON via structlog

## Segurança

- Validação de webhooks via HMAC (variáveis `CHATWOOT_HMAC_SECRET`/`HMAC_SECRET`)
- Credenciais somente via variáveis de ambiente

## Problemas conhecidos

- Certifique‑se de preencher as variáveis do Chatwoot e OpenAI no `.env` antes de iniciar.

