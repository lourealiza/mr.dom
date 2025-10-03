# Integração AgentOS com Workflow N8N Existente

## 📋 Análise do Workflow Atual

Baseado no arquivo `workflow-n8n.json`, o fluxo atual funciona assim:

### 🔄 Fluxo Principal Atual

1. **Webhook2** → Recebe mensagens do Chatwoot
2. **arruma o telefone1** → Normaliza telefone para E.164 BR
3. **Edit Fields2** → Extrai dados do sender (nome, email, telefone)
4. **Verificar Anexo** → Verifica se há anexos de áudio
5. **Baixar Áudio** → Se houver áudio, baixa e transcreve
6. **Create transcriptionJob** → Transcreve áudio com AWS Transcribe
7. **Normalizador único** → Normaliza dados da conversa
8. **GetIdByPhone** → Busca lead existente no CRM DOM360
9. **If** → Verifica se lead existe
10. **GetComments** → Busca comentários do lead no CRM
11. **Agente de IA1** → **PONTO DE INTEGRAÇÃO AGENTOS**
12. **ResponderChatwoot** → Envia resposta de volta

### 🧠 Agente de IA Atual

O **Agente de IA1** atual usa:
- **Modelo Principal**: AWS Bedrock (amazon.nova-lite-v1:0)
- **Modelo Fallback**: OpenAI GPT-4.1-nano
- **RAG**: Supabase Vector Store com documentos
- **Memory**: Simple Memory (Buffer Window)
- **Tools**: Create_Lead (criar lead no CRM)

## 🚀 Como Integrar AgentOS

### Opção 1: Substituição Direta (Recomendada)

Substitua o **Agente de IA1** atual por uma chamada para nossa API AgentOS:

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
    "jsonBody": "={\n  \"message\": \"{{ $('Normalizador único (lead + flags + conversation)1').item.json.content }}\",\n  \"context\": {\n    \"conversation_id\": \"{{ $('Edit Fields').item.json.conversation_id }}\",\n    \"account_id\": \"{{ $('Edit Fields').item.json.account_id }}\",\n    \"lead_data\": {{ $('GetComments').item.json }},\n    \"phone\": \"{{ $('arruma o telefone1').item.json.telefone }}\",\n    \"nome\": \"{{ $('Edit Fields2').item.json['body.body.payload.conversation.meta.sender.name'] }}\",\n    \"email\": \"{{ $('Edit Fields2').item.json['body.body.payload.conversation.meta.sender.email'] }}\"\n  }\n}",
    "options": {}
  },
  "type": "n8n-nodes-base.httpRequest",
  "name": "AgentOS API Call"
}
```

### Opção 2: Agente Específico por Contexto

Crie diferentes chamadas baseadas no contexto:

```json
{
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $('GetComments').item.json.length }}",
          "operation": "isNotEmpty"
        }
      ]
    }
  },
  "type": "n8n-nodes-base.if",
  "name": "Lead Existe?"
}
```

**Se lead existe** → Use `sales-sdr` agent:
```json
{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:8000/api/v1/agents/process",
    "jsonBody": "={\n  \"agent_id\": \"sales-sdr\",\n  \"message\": \"{{ $json.content }}\",\n  \"context\": {\n    \"lead_exists\": true,\n    \"lead_data\": {{ $('GetComments').item.json }}\n  }\n}"
  },
  "name": "Sales SDR Agent"
}
```

**Se lead não existe** → Use `lead-qualifier` agent:
```json
{
  "parameters": {
    "method": "POST", 
    "url": "http://localhost:8000/api/v1/agents/process",
    "jsonBody": "={\n  \"agent_id\": \"lead-qualifier\",\n  \"message\": \"{{ $json.content }}\",\n  \"context\": {\n    \"lead_exists\": false,\n    \"phone\": \"{{ $('arruma o telefone1').item.json.telefone }}\"\n  }\n}"
  },
  "name": "Lead Qualifier Agent"
}
```

## 🔧 Implementação Prática

### 1. Modificar o Workflow N8N

1. **Remover** o nó "Agente de IA1" atual
2. **Adicionar** nó HTTP Request apontando para nossa API
3. **Manter** toda a lógica de CRM e normalização existente
4. **Ajustar** o nó "ResponderChatwoot" para usar resposta da API

### 2. Configurar Variáveis de Ambiente

No N8N, adicione variáveis:
- `AGENTOS_API_URL`: `http://localhost:8000`
- `AGENTOS_ENABLED`: `true`

### 3. Criar Workflow de Fallback

Se AgentOS não estiver disponível, manter agente atual como backup:

```json
{
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json.error }}",
          "operation": "isNotEmpty"
        }
      ]
    }
  },
  "type": "n8n-nodes-base.if",
  "name": "AgentOS Error?"
}
```

## 📊 Vantagens da Integração

### ✅ Benefícios Imediatos

1. **Agentes Especializados**: 
   - Lead Qualifier para novos prospects
   - Sales SDR para leads existentes
   - Customer Success para suporte

2. **Melhor Contexto**:
   - Dados do CRM DOM360
   - Histórico de conversas
   - Informações do lead

3. **Flexibilidade**:
   - Fácil troca de agentes
   - Ajuste de prompts via API
   - Monitoramento independente

### 🔄 Fluxo Otimizado

```
Chatwoot → N8N → AgentOS API → Agente Específico → Resposta → Chatwoot
```

## 🛠️ Configuração Passo a Passo

### 1. Preparar API AgentOS

```bash
# Instalar dependências
pip install agno>=0.1.0

# Configurar .env
OPENAI_API_KEY=sk-sua_chave_aqui

# Executar API
python examples/agentos_integration_example.py
```

### 2. Testar Integração

```bash
# Testar endpoint
curl -X POST http://localhost:8000/api/v1/agents/process-best \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quero saber mais sobre os planos",
    "context": {
      "conversation_id": "123",
      "lead_exists": false
    }
  }'
```

### 3. Modificar N8N

1. **Importar** workflow atual
2. **Substituir** "Agente de IA1" por HTTP Request
3. **Configurar** URL para `http://localhost:8000/api/v1/agents/process-best`
4. **Mapear** dados do contexto
5. **Testar** com mensagem real

## 🚨 Considerações Importantes

### ⚠️ Pontos de Atenção

1. **Latência**: AgentOS pode ser mais lento que Bedrock local
2. **Disponibilidade**: Manter fallback para agente atual
3. **Custos**: OpenAI pode ser mais caro que Bedrock
4. **Contexto**: Garantir que dados do CRM cheguem corretamente

### 🔧 Troubleshooting

**AgentOS não responde**:
- Verificar se API está rodando
- Conferir OPENAI_API_KEY
- Testar endpoint diretamente

**Resposta muito genérica**:
- Ajustar sistema prompts dos agentes
- Melhorar contexto enviado
- Verificar dados do CRM

**Integração quebrou**:
- Manter agente atual como backup
- Implementar retry logic
- Monitorar logs da API

## 📈 Próximos Passos

### Fase 1: Integração Básica
- [ ] Substituir agente atual por chamada AgentOS
- [ ] Testar com dados reais
- [ ] Implementar fallback

### Fase 2: Otimização
- [ ] Agentes específicos por contexto
- [ ] Melhorar prompts baseado em dados CRM
- [ ] Adicionar métricas de performance

### Fase 3: Expansão
- [ ] Novos agentes especializados
- [ ] Integração com outros sistemas
- [ ] Machine learning para melhorias

---

**💡 Dica**: Comece com a Opção 1 (substituição direta) para validar a integração, depois evolua para agentes específicos conforme necessário.
