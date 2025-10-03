# Integração AgentOS - MrDom SDR

Este documento explica como integrar e usar o sistema de agentes avançados AgentOS no projeto MrDom SDR.

## Visão Geral

O AgentOS é uma biblioteca que permite criar agentes de IA especializados usando diferentes modelos de linguagem. No MrDom SDR, estamos integrando três agentes especializados:

- **Lead Qualifier**: Especializado em qualificação de leads BANT (Budget, Authority, Need, Timeline)
- **Sales SDR**: Focado em geração de interesse e agendamento de reuniões
- **Customer Success**: Especialista em sucesso do cliente e resolução de problemas

## Configuração

### 1. Dependências

Adicione a dependência ao `requirements.txt`:

```bash
agno>=0.1.0
```

### 2. Variáveis de Ambiente

Configure no arquivo `.env`:

```bash
# OpenAI (obrigatório para AgentOS)
OPENAI_API_KEY=sk-sua_chave_openai_aqui
OPENAI_MODEL=gpt-4

# Configurações específicas do AgentOS
AGENT_MAX_TOKENS=1000
AGENT_TEMPERATURE=0.7
AGENTOS_ENABLED=true
```

### 3. Instalação

```bash
pip install -r requirements.txt
```

## Estrutura de Arquivos Criados

```
api/
├── services/
│   └── agent_os_integration.py    # Integração principal com AgentOS
├── routers/
│   └── agents.py                   # Endpoints para os agentes
examples/
└── agentos_integration_example.py  # Exemplo completo de integração
scripts/
└── test-agentos-integration.py    # Script de testes
docs/
└── agentos-integration.md         # Esta documentação
```

## Como Usar

### Integração Básica (seguindo seu padrão)

```python
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# Cria sua app FastAPI customizada
app = FastAPI(title="MrDom SDR com AgentOS")

# Suas rotas customizadas
@app.get("/status")
async def status():
    return {"status": "healthy"}

# Agentes especializados
agentes_mrdom = [
    Agent(
        id="lead-qualifier",
        model=OpenAIChat(
            id="gpt-4",
            sistema_prompt="Você é especialista em qualificação BANT..."
        )
    ),
    # ... outros agentes
]

# Integra com AgentOS
agent_os = AgentOS(
    agents=agentes_mrdom,
    base_app=app  # Sua app personalizada
)

# Obtém a app combinada
app = agent_os.get_app()
```

### Usando os Serviços

```python
from api.services.agent_os_integration import agent_integration

# Verificar se AgentOS está disponível
if agent_integration.is_agent_os_available():
    # Listar agentes disponíveis
    agentes = agent_integration.get_available_agents()
    
    # Processar mensagem com agente específico
    resultado = await agent_integration.process_with_agent(
        agent_id="lead-qualifier",
        message="Qual o preço do seu serviço?",
        context={"tipo": "qualificacao"}
    )
    
    # Sugerir melhor agente
    agent_sugerido = await agent_integration.get_best_agent_suggestions(
        "Preciso agendar uma demo"
    )
```

## Endpoints da API

### Status dos Agentes

```bash
GET /api/v1/agents/status
```

Retorna:
```json
{
  "agent_os_available": true,
  "available_agents": ["lead-qualifier", "sales-sdr", "customer-success"],
  "total_agents": 3
}
```

### Listar Agentes

```bash
GET /api/v1/agents/list
```

### Processar com Agente Específico

```bash
POST /api/v1/agents/process
Content-Type: application/json

{
  "agent_id": "lead-qualifier",
  "message": "Qual o preço do serviço?",
  "context": {"cliente": "empresa_x"}
}
```

### Sugerir Melhor Agente

```bash
POST /api/v1/agents/suggest
Content-Type: application/json

{
  "message": "Quero agendar uma demonstração"
}
```

### Processar com Melhor Agente Automaticamente

```bash
POST /api/v1/agents/process-best
Content-Type: application/json

{
  "message": "Preciso de ajuda com integração",
  "context": {"urgente": true}
}
```

## Executando

### 1. Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor de desenvolvimento
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Usando o Exemplo Completo

```bash
cd examples
python agentos_integration_example.py
```

### 3. Testando a Integração

```bash
cd scripts
python test-agentos-integration.py
```

## Testando os Endpoints

### 1. Status

```bash
curl http://localhost:8000/api/v1/agents/status
```

### 2. Processar Mensagem

```bash
curl -X POST http://localhost:8000/api/v1/agents/process-best \
  -H "Content-Type: application/json" \
  -d '{"message": "Quero saber mais sobre seus planos"}'
```

### 3. Sugerir Agente

```bash
curl -X POST http://localhost:8000/api/v1/agents/suggest \
  -H "Content-Type: application/json" \
  -d '{"message": "Tive problema com a integração"}'
```

## Tratamento de Erros

- Se `OPENAI_API_KEY` não estiver configurada, o AgentOS não será inicializado
- Endpoints retornam erro 503 se AgentOS não estiver disponível
- Agentes inexistentes retornam erro 400 com sugestões de agentes válidos

## Integração com Chatwoot

Para integrar com o webhook do Chatwoot, você pode usar os agentes na função `agentbot`:

```python
from api.services.agent_os_integration import agent_integration

# No webhook do Chatwoot
if agent_integration.is_agent_os_available():
    # Processa mensagem usando melhor agente
    agentes_sugeridos = await agent_integration.get_best_agent_suggestions(user_text)
    melhor_agente = agentes_sugeridos[0] if agentes_sugeridos else "lead-qualifier"
    
    resultado = await agent_integration.process_with_agent(
        agent_id=melhor_agente,
        message=user_text,
        context={"conversation_id": conversation_id}
    )
    
    if resultado["success"]:
        reply_text = resultado["response"]
```

## Monitoramento e Logs

- Logs são gerados em `DEBUG` para debugging
- Métricas podem ser adicionadas usando Prometheus
- Health checks já incluem status do AgentOS

## Próximos Passos

1. Adicionar mais agentes especializados (ex: support tech, pricing specialist)
2. Implementar histórico de conversas por agente
3. Adicionar métricas de performance por agente
4. Criar interface web para configurar agentes
5. Implementar aprendizado baseado em feedback
