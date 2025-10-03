# Integração AgentOS - MrDom SDR

Este projeto demonstra como integrar o AgentOS (sistema de agentes de IA avançados) com o projeto MrDom SDR existente.

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
# Instalar AgentOS
pip install agno>=0.1.0

# Instalar dependências do projeto
pip install -r requirements.txt
```

### 2. Configurar Ambient

Configure o arquivo `.env`:

```bash
OPENAI_API_KEY=sk-sua_chave_openai_aqui
OPENAI_MODEL=gpt-4
AGENT_MAX_TOKENS=1000
AGENT_TEMPERATURE=0.7
AGENTOS_ENABLED=true
```

### 3. Testar Integração

```bash
# Executar script de teste
python scripts/test-agentos-integration.py
```

### 4. Executar Servidor

```bash
# Opção 1: Usar exemplo completo
python examples/agentos_integration_example.py

# Opção 2: Integrar com app existente (descomentar linhas no main.py)
uvicorn api.main:app --reload
```

## 📋 Como Funciona

### Exemplo Completo Seguindo seu Padrão

```python
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# Criar sua app FastAPI customizada
app = FastAPI(title="My Custom App")

# Adicionar suas rotas customizadas
@app.get("/status")
async def status_check():
    return {"status": "healthy"}

# Criar agentes especializados
agentes = [
    Agent(
        id="basic-agent", 
        model=OpenAIChat(id="gpt-4-mini")
    ),
    Agent(
        id="sales-agent",
        model=OpenAIChat(
            id="gpt-4",
            sistema_prompt="Você é um agente de vendas especializado..."
        )
    )
]

# Integrar com sua app
agent_os = AgentOS(
    agents=agentes,
    base_app=app  # Sua app personalizada
)

# Obter a app combinada
app = agent_os.get_app()
```

### Endpoints Disponíveis

Após integração completa, você terá acesso a:

```bash
# Status dos agentes
GET /api/v1/agents/status

# Listar agentes disponíveis  
GET /api/v1/agents/list

# Processar com agente específico
POST /api/v1/agents/process
{
  "agent_id": "lead-qualifier",
  "message": "Qual o preço?"
}

# Processar automaticamente com melhor agente
POST /api/v1/agents/process-best
{
  "message": "Preciso de ajuda"
}
```

## 🧪 Testes

### Testar Conectividade

```bash
curl http://localhost:8000/api/v1/agents/status
```

### Testar Processamento

```bash
curl -X POST http://localhost:8000/api/v1/agents/process-best \
  -H "Content-Type: application/json" \
  -d '{"message": "Quero saber mais sobre seus planos"}'
```

## 🔧 Configuração Avançada

### Agentes Personalizados

Você pode criar seus próprios agentes:

```python
agent_customizado = Agent(
    id="meu-agente-especial",
    model=OpenAIChat(
        id="gpt-4",
        sistema_prompt="Instruções específicas para seu domínio..."
    )
)
```

### Integração com Chatwoot

Para usar com o webhook existente do Chatwoot:

```python
from api.services.agent_os_integration import agent_integration

# No webhook
if agent_integration.is_agent_os_available():
    resultado = await agent_integration.process_with_agent(
        agent_id="sales-sdr",
        message=user_text,
        context={"conversation_id": conversation_id}
    )
    reply_text = resultado["response"]
```

## 📚 Documentação Completa

Para mais detalhes, consulte:
- [docs/agentos-integration.md](docs/agentos-integration.md)
- [examples/agentos_integration_example.py](examples/agentos_integration_example.py)

## 🔍 Troubleshooting

### AgentOS não inicializa

1. Verifique se `OPENAI_API_KEY` está configurada
2. Certifique-se que agno está instalado: `pip install agno`
3. Verifique logs para detalhes específicos

### Agentes não respondem

1. Verifique modelo OpenAI (`gpt-4`, `gpt-3.5-turbo`)
2. Confirme tokens disponíveis na conta OpenAI
3. Teste diretamente com curl nos endpoints

## 🎯 Próximos Passos

1. **Habilite agentes no main.py**: Descomente as linhas comentadas
2. **Personalize agentes**: Ajuste sistema prompts conforme necessidade
3. **Integre com Chatwoot**: Use agentes no webhook existente
4. **Monitore performance**: Adicione métricas específicas por agente

## 🤝 Contribuição

Para contribuir com melhorias:

1. Teste nos ambientes de desenvolvimento
2. Documente novas funcionalidades
3. Adicione testes unitários
4. Mantenha compatibilidade com estrutura existente

---

💡 **Dica**: Comece com o exemplo em `examples/agentos_integration_example.py` para ver toda a integração funcionando antes de modificar o código principal.
