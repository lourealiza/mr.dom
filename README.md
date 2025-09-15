<<<<<<< HEAD
# mr.dom
=======
# MrDom SDR MVP

Sistema de automação de vendas (SDR) com integração Chatwoot, N8N e OpenAI para qualificação e atendimento automatizado de leads.

## 🚀 Funcionalidades

- **Integração Chatwoot**: Recebimento de webhooks e automação de respostas
- **IA com OpenAI**: Análise de intenções e geração de respostas personalizadas
- **Automação N8N**: Workflows para qualificação de leads e follow-up
- **Qualificação Inteligente**: Análise BANT (Budget, Authority, Need, Timeline)
- **Escalação Automática**: Transferência para agentes humanos quando necessário
- **API RESTful**: Interface completa para integração

## 📁 Estrutura do Projeto

```
mrdom-sdr-mvp/
├── api/
│   ├── main.py                    # Aplicação FastAPI principal
│   ├── routers/
│   │   └── chatwoot_agentbot.py  # Rotas para webhooks Chatwoot
│   ├── services/
│   │   ├── chatwoot_client.py    # Cliente para API Chatwoot
│   │   ├── n8n_client.py         # Cliente para N8N
│   │   └── openai_client.py      # Cliente para OpenAI
│   └── domain/
│       ├── bot_logic.py          # Lógica de negócio do bot
│       └── models.py             # Modelos de dados
├── compose/
│   ├── docker-compose.yml        # Orquestração de containers
│   └── Dockerfile               # Imagem da aplicação
├── requirements.txt              # Dependências Python
├── env.example                  # Variáveis de ambiente exemplo
└── README.md                    # Este arquivo
```

## 🛠️ Instalação

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Conta OpenAI com API key
- Instância Chatwoot configurada
- N8N (opcional, pode ser externo)

### 1. Clone o repositório

```bash
git clone <repository-url>
cd mrdom-sdr-mvp
```

### 2. Configure as variáveis de ambiente

```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute com Docker

```bash
cd compose
docker-compose up -d
```

### 5. Execute localmente (desenvolvimento)

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ⚙️ Configuração

### Variáveis de Ambiente Obrigatórias

```env
# Chatwoot
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_ACCESS_TOKEN=seu_token
CHATWOOT_ACCOUNT_ID=seu_account_id

# OpenAI
OPENAI_API_KEY=sk-sua_chave

# N8N (opcional)
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=seu_api_key
```

### Configuração do Chatwoot

1. Acesse sua instância Chatwoot
2. Vá em Settings > Integrations > Webhooks
3. Adicione webhook: `http://seu-dominio/api/v1/chatwoot/webhook`
4. Selecione eventos: `message_created`, `conversation_created`

## 🔧 Uso

### Endpoints Principais

- `POST /api/v1/chatwoot/webhook` - Webhook do Chatwoot
- `GET /api/v1/chatwoot/status` - Status da integração
- `POST /api/v1/chatwoot/test` - Testar integração

### Fluxo de Funcionamento

1. **Cliente envia mensagem** no Chatwoot
2. **Webhook é recebido** pela API
3. **IA analisa** a intenção e contexto
4. **Sistema decide** a ação (responder, escalar, qualificar)
5. **Resposta é enviada** ou **conversa é escalada**

### Tipos de Ações

- **Resposta Automatizada**: Para perguntas simples e saudações
- **Escalação**: Para objeções complexas ou fora do horário
- **Qualificação**: Para leads interessados
- **Follow-up**: Para leads com interesse médio

## 🤖 Configuração do Bot

### Mensagens de Boas-vindas

```env
BOT_WELCOME_MESSAGE="Olá! 👋 Sou o assistente virtual da MrDom. Como posso ajudá-lo hoje?"
```

### Palavras-chave para Escalação

```env
ESCALATION_KEYWORDS=["falar com humano", "atendente", "supervisor"]
```

### Horário Comercial

```env
BUSINESS_HOURS={"start": "09:00", "end": "18:00"}
TIMEZONE=America/Sao_Paulo
```

## 📊 Monitoramento

### Logs

Os logs são estruturados em JSON e incluem:
- Análise de mensagens
- Decisões de ação
- Erros e exceções
- Métricas de performance

### Métricas Disponíveis

- Total de mensagens processadas
- Taxa de escalação
- Tempo de resposta
- Qualificação de leads

## 🔒 Segurança

- Validação de webhooks Chatwoot
- Rate limiting
- Logs de auditoria
- Variáveis de ambiente para credenciais

## 🚀 Deploy

### Produção

1. Configure variáveis de ambiente de produção
2. Use HTTPS para webhooks
3. Configure monitoramento
4. Configure backup de dados

### Docker

```bash
docker-compose -f compose/docker-compose.yml up -d
```

## 🧪 Testes

```bash
# Executar testes
pytest

# Testar integração
curl -X POST http://localhost:8000/api/v1/chatwoot/test
```

## 📈 Roadmap

- [ ] Integração com CRM
- [ ] Dashboard de métricas
- [ ] Machine Learning para melhorar respostas
- [ ] Suporte a múltiplos idiomas
- [ ] Integração com WhatsApp Business

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para suporte, entre em contato:
- Email: suporte@mrdom.com
- Discord: [Link do servidor]
- Issues: [Link do GitHub]
>>>>>>> 7e8863e (Initialize project and add settings)
