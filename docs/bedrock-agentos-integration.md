# Integração AgentOS + AWS Bedrock - MrDom SDR

Este documento explica como integrar AgentOS com AWS Bedrock (em vez de OpenAI) no projeto MrDom SDR.

## 🎯 Por que Bedrock?

Baseado no workflow N8N atual, vocês já estão usando:
- **Modelo Principal**: AWS Bedrock (amazon.nova-lite-v1:0)
- **Modelo Fallback**: OpenAI GPT-4.1-nano

A integração AgentOS com Bedrock mantém consistência com sua infraestrutura atual.

## 🔧 Configuração

### 1. Dependências

```bash
# Instalar AgentOS (já feito)
pip install agno>=0.1.0

# Instalar boto3 se não tiver
pip install boto3
```

### 2. Variáveis de Ambiente

Configure no arquivo `.env`:

```bash
# AWS Bedrock (principal)
AWS_ACCESS_KEY_ID=sua_chave_aws_aqui
AWS_SECRET_ACCESS_KEY=seu_secret_aws_aqui
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL=amazon.nova-lite-v1:0

# OpenAI (opcional - fallback)
OPENAI_API_KEY=sk-sua_chave_openai_aqui
OPENAI_MODEL=gpt-4

# Configurações AgentOS
AGENT_MAX_TOKENS=1000
AGENT_TEMPERATURE=0.7
AGENTOS_ENABLED=true
```

### 3. Permissões AWS

Certifique-se que sua conta AWS tem permissões para:
- `bedrock:InvokeModel`
- `bedrock:ListFoundationModels`

## 🚀 Como Usar

### Exemplo Básico com Bedrock

```python
from agno.agent import Agent
from agno.models.aws_bedrock import BedrockChat
from agno.os import AgentOS

# Cria agentes usando Bedrock
agentes_bedrock = [
    Agent(
        id="lead-qualifier",
        model=BedrockChat(
            id="amazon.nova-lite-v1:0",
            sistema_prompt="Você é especialista em qualificação BANT..."
        )
    ),
    Agent(
        id="sales-sdr", 
        model=BedrockChat(
            id="amazon.nova-lite-v1:0",
            sistema_prompt="Você é um SDR experiente..."
        )
    )
]

# Integra com AgentOS
agent_os = AgentOS(
    agents=agentes_bedrock,
    base_app=app
)

app = agent_os.get_app()
```

### Executar Demonstração

```bash
# Configurar AWS credentials no .env
python examples/bedrock_agentos_integration.py

# Testar
python scripts/test-bedrock-agentos.py
```

## 🔄 Integração com N8N

### Modificação do Workflow

Substitua o **Agente de IA1** atual por:

```json
{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:8000/api/v1/agents/process-best",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={\n  \"message\": \"{{ $('Normalizador único (lead + flags + conversation)1').item.json.content }}\",\n  \"context\": {\n    \"conversation_id\": \"{{ $('Edit Fields').item.json.conversation_id }}\",\n    \"account_id\": \"{{ $('Edit Fields').item.json.account_id }}\",\n    \"lead_exists\": {{ $('If').item.json.id ? 'true' : 'false' }},\n    \"lead_data\": {{ $('GetComments').item.json || 'null' }},\n    \"phone\": \"{{ $('arruma o telefone1').item.json.telefone }}\",\n    \"model_provider\": \"AWS Bedrock\",\n    \"model\": \"amazon.nova-lite-v1:0\"\n  }\n}",
    "options": {
      "timeout": 30000
    }
  },
  "type": "n8n-nodes-base.httpRequest",
  "name": "AgentOS Bedrock API"
}
```

## 📊 Vantagens do Bedrock

### ✅ Benefícios

1. **Consistência**: Mesmo modelo do workflow atual
2. **Custo**: Bedrock pode ser mais econômico que OpenAI
3. **Latência**: Menor latência se AWS estiver próxima
4. **Compliance**: Dados ficam na AWS
5. **Escalabilidade**: Infraestrutura AWS robusta

### 🔄 Fluxo Otimizado

```
Chatwoot → N8N → AgentOS Bedrock API → amazon.nova-lite-v1:0 → Resposta → Chatwoot
```

## 🧪 Testes

### 1. Teste de Conexão

```bash
python scripts/test-bedrock-agentos.py
```

### 2. Teste de Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/agents/process-best \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quero saber mais sobre os planos",
    "context": {
      "lead_exists": false,
      "model_provider": "AWS Bedrock"
    }
  }'
```

### 3. Teste Integração N8N

```bash
python scripts/test-n8n-agentos-integration.py
```

## 🚨 Troubleshooting

### Problemas Comuns

**Bedrock não conecta**:
- Verificar AWS credentials
- Confirmar região (us-east-1)
- Verificar permissões IAM

**Modelo não disponível**:
- Verificar se amazon.nova-lite-v1:0 está habilitado
- Tentar outros modelos Bedrock

**Latência alta**:
- Usar região mais próxima
- Otimizar prompts
- Implementar cache

### Logs Importantes

```bash
# Logs da API AgentOS
tail -f api.log | grep -i bedrock

# Logs AWS
aws logs describe-log-groups --log-group-name-prefix bedrock
```

## 📈 Monitoramento

### Métricas Importantes

- **Tempo de resposta**: < 5 segundos
- **Taxa de erro**: < 1%
- **Custo por requisição**: Monitorar AWS billing
- **Uso de tokens**: Otimizar prompts

### Alertas Recomendados

- Bedrock API errors > 5%
- Latência > 10 segundos
- Custo diário > limite
- Modelo indisponível

## 🔄 Migração do OpenAI

Se quiser migrar do OpenAI atual:

1. **Configurar Bedrock**: Credentials e permissões
2. **Testar modelo**: Validar qualidade das respostas
3. **Migrar gradualmente**: Começar com um agente
4. **Monitorar performance**: Comparar resultados
5. **Desativar OpenAI**: Quando Bedrock estiver estável

## 📚 Referências

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AgentOS Bedrock Models](https://docs.agno.ai/models/bedrock)
- [N8N HTTP Request Node](https://docs.n8n.io/integrations/builtin/cluster-nodes/n8n-nodes-base.httprequest/)

---

**💡 Dica**: Comece testando com um agente simples antes de migrar todo o sistema para Bedrock.
