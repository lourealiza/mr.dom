# Guia do Sandbox de Conversa - MrDom SDR

## 🎯 O que é o Sandbox?

O Sandbox de Conversa é uma ferramenta interativa para testar os agentes AgentOS + Bedrock antes de integrar com o N8N. Permite simular conversas reais e validar respostas.

## 🚀 Como Usar

### 1. Sandbox Simples (Simulação)

```bash
python examples/conversation_sandbox.py
```

**Funcionalidades:**
- ✅ Simula respostas dos agentes
- ✅ Testa diferentes cenários
- ✅ Comandos interativos
- ✅ Histórico de conversa
- ✅ Não precisa de API rodando

### 2. Sandbox Avançado (API Real)

```bash
# Primeiro, inicie a API
python examples/bedrock_agentos_integration.py

# Em outro terminal, inicie o sandbox
python examples/advanced_sandbox.py
```

**Funcionalidades:**
- ✅ Conecta com API AgentOS real
- ✅ Usa Bedrock para respostas reais
- ✅ Fallback para simulação se API não disponível
- ✅ Exporta conversas para JSON
- ✅ Monitora status da conexão

## 🎮 Comandos Disponíveis

### Comandos Básicos
- `/help` - Mostra ajuda
- `/agents` - Lista agentes disponíveis
- `/context` - Mostra contexto atual
- `/history` - Mostra histórico da conversa
- `/clear` - Limpa histórico
- `/quit` - Sair

### Comandos Avançados (Sandbox Avançado)
- `/status` - Status da conexão com API
- `/export` - Exporta conversa para JSON

### Troca de Agentes
- `/switch lead-qualifier` - Troca para Lead Qualifier
- `/switch sales-sdr` - Troca para Sales SDR
- `/switch customer-success` - Troca para Customer Success

## 🧪 Cenários de Teste

### 1. Qualificação de Lead
```
👤 Você: Quero saber mais sobre os planos
🤖 Lead Qualifier: Entendo que você quer saber sobre investimento. Para te dar uma proposta adequada, preciso entender melhor: qual o tamanho da sua empresa e quantas pessoas trabalham no time de vendas?
```

### 2. Agendamento de Demo
```
👤 Você: Quero agendar uma demo
🤖 Sales SDR: Perfeito! Tenho 2 horários disponíveis esta semana: terça às 14h ou quinta às 10h. Qual funciona melhor para você?
```

### 3. Suporte ao Cliente
```
👤 Você: Estou com problema na integração
🤖 Customer Success: Entendo que você está enfrentando dificuldades. Vou te ajudar a resolver isso rapidamente. Pode me dar mais detalhes sobre o que está acontecendo?
```

## 📊 Contexto Simulado

O sandbox usa dados simulados do CRM:

```json
{
  "conversation_id": "sandbox_123",
  "account_id": "1",
  "lead_exists": false,
  "phone": "+5511998765432",
  "nome": "João Silva",
  "email": "joao@empresa.com",
  "empresa": "Empresa ABC",
  "origem": "MrDOM Sandbox"
}
```

## 🔧 Configuração

### Para Sandbox Simples
- ✅ Não precisa de configuração
- ✅ Funciona imediatamente
- ✅ Simula respostas realistas

### Para Sandbox Avançado
- 🔧 Configure AWS credentials no `.env`
- 🔧 Inicie a API AgentOS
- 🔧 Teste conexão

## 📈 Casos de Uso

### 1. Desenvolvimento
- Testar novos prompts
- Validar fluxos de conversa
- Debugar respostas dos agentes

### 2. Treinamento
- Demonstrar funcionamento
- Treinar equipe operacional
- Validar cenários de negócio

### 3. Validação
- Testar antes de produção
- Comparar respostas diferentes
- Validar integração N8N

## 🚨 Troubleshooting

### Sandbox não inicia
```bash
# Verificar Python
python --version

# Instalar dependências
pip install requests asyncio
```

### API não conecta
```bash
# Verificar se API está rodando
curl http://localhost:8000/api/v1/agents/status

# Verificar logs da API
tail -f api.log
```

### Respostas muito genéricas
- Ajustar prompts dos agentes
- Melhorar contexto enviado
- Verificar configuração Bedrock

## 📝 Exportação de Dados

O sandbox avançado permite exportar conversas:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "api_used": true,
  "conversation": [
    {
      "timestamp": "10:30:15",
      "agent_id": "lead-qualifier",
      "user_message": "Quero saber sobre preços",
      "response": "Entendo que você quer saber sobre investimento...",
      "api_used": true
    }
  ],
  "context": {
    "conversation_id": "sandbox_123",
    "lead_exists": false
  }
}
```

## 🎯 Próximos Passos

1. **Teste básico**: Use sandbox simples primeiro
2. **Validação**: Teste cenários reais de negócio
3. **Integração**: Use sandbox avançado com API
4. **Produção**: Implemente no N8N

## 💡 Dicas

- **Comece simples**: Use simulação primeiro
- **Teste cenários**: Crie casos de uso reais
- **Exporte dados**: Salve conversas importantes
- **Compare agentes**: Teste diferentes agentes
- **Valide contexto**: Verifique dados do CRM

---

**🎮 Divirta-se testando! O sandbox é sua ferramenta para validar tudo antes de ir para produção.**
