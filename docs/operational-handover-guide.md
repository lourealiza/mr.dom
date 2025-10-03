# Guia de Transição Operacional - AgentOS

Este documento foi criado para facilitar a transição operacional do sistema AgentOS para novos membros da equipe.

## 👋 Olá! Seja Bem-Vindo ao AgentOS

Você está assumindo o controle operacional do sistema de agentes inteligentes do MrDom SDR. Este guia vai te ajudar a entender rapidamente como tudo funciona.

## 🚀 Início Imediato (5 minutos)

### 1. Status Atual - Verificar Agora
```bash
# Depois de configurar o ambiente, teste se está funcionando:
curl http://localhost:8000/api/v1/agents/status
```

**Você deve ver algo como:**
```json
{
  "agent_os_available": true,
  "available_agents": ["lead-qualifier", "sales-sdr", "customer-success"],
  "total_agents": 3
}
```

### 2. Teste Rápido - Agora Mesmo
```bash
curl -X POST http://localhost:8000/api/v1/agents/process-best \
  -H "Content-Type: application/json" \
  -d '{"message": "Quero saber mais sobre os planos"}'
```

## 📋 Checklist de Primeira Semana

### Dia 1: Configuração
- [ ] Instalar AgentOS: `pip install agno>=0.1.0`
- [ ] Configurar `.env` com `OPENAI_API_KEY`
- [ ] Executar script de teste: `python scripts/test-agentos-integration.py`
- [ ] Testar todos os endpoints

### Dia 2-3: Entendimento
- [ ] Estudar [README-AGENTOS.md](../README-AGENTOS.md)
- [ ] Revisar [agentos-integration.md](./agentos-integration.md)
- [ ] Explicar aos colegas como funciona

### Dia 4-5: Operação
- [ ] Monitorar logs de agentes
- [ ] Testar diferentes cenários de chat
- [ ] Documentar problemas encontrados

## 🔧 Comandos Essenciais

### Iniciar Servidor
```bash
# Opção 1: Com agente integrado
python examples/agentos_integration_example.py

# Opção 2: API completa (descomentar agentes no main.py)
uvicorn api.main:app --reload
```

### Testar Funcionalidades
```bash
# Teste completo
python scripts/test-agentos-integration.py

# Teste específico
curl -X POST http://localhost:8000/api/v1/agents/suggest \
  -H "Content-Type: application/json" \
  -d '{"message": "Apresente sua mensagem aqui"}'
```

### Verificar Logs
```bash
# Logs em tempo real (se usando uvicorn)
# Os logs aparecerão automaticamente no terminal
```

## 📊 Monitoramento Diário

### Saúde dos Agentes
```bash
curl http://localhost:8000/api/v1/agents/status
```

### Performance por Agente
- Monitore tempo de resposta
- Verifique taxa de erro
- Observe uso de tokens OpenAI

### Integração Chatwoot
- Verifique webhooks funcionando
- Monitore respostas automáticas
- Confirme escalação para humanos

## 🚨 Problemas Comuns e Soluções

### AgentOS não inicializa
```bash
# Verificar:
echo $OPENAI_API_KEY
pip show agno
```

**Solução:** Configurar API key e reinstalar agno

### Agentes não respondem
```bash
# Testar:
curl -X POST http://localhost:8000/api/v1/agents/process \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "lead-qualifier", "message": "teste"}'
```

**Solução:** Verificar modelo OpenAI e tokens

### Respostas muito genéricas
**Solução:** Ajustar sistema prompts em `agent_os_integration.py`

## 📞 Contatos de Emergência

### Em caso de problemas críticos:

1. **Sistema não funciona**: Revisar logs e restart servidor
2. **Agentes não respondem**: Verificar OpenAI API key
3. **Integração Chatwoot quebrou**: Verificar webhooks e chaves HMAC

### Logs importantes a verificar:
```bash
# Aplicação principal
tail -f api.log

# Erros específicos AgentOS
grep -i "agentos\|agno" logs/app.log
```

## 🎯 Responsabilidades Diárias

### Manhã (15 min)
- [ ] Verificar status de todos os agentes
- [ ] Revisar logs de erro da noite anterior
- [ ] Confirmar integração Chatwoot funcionando

### Durante o dia
- [ ] Monitorar respostas automáticas
- [ ] Intervir quando necessário (escalações)
- [ ] Documentar melhorias necessárias

### Fim do dia (10 min)
- [ ] Verificar relatório de uso
- [ ] Anotar pontos de melhoria
- [ ] Preparar resumo para equipe

## 📈 KPIs Importantes

### Diários
- Qtd de conversas automáticas vs escalações
- Tempo médio de resposta dos agentes
- Taxa de satisfação (se coletada)

### Semanais
- Economia em horas de SDR
- Conversão de leads automáticos
- Melhoria nas respostas dos agentes

## 🔄 Melhorias Contínuas

### Ajustes Frequentes
1. **Sistema Prompts**: Refine baseado no feedback
2. **Fluxos de Conversa**: Aprimore baseado nos dados
3. **Novos Agentes**: Adicione conforme necessidade do negócio

### Solicitações Comuns
- "Precisamos de um agente para suporte técnico"
- "As respostas estão muito longas"
- "Adicionar mais contexto brasileiro"

## 📚 Referências Rápidas

### Arquivos Importantes
- `api/services/agent_os_integration.py` - Configuração principal
- `api/routers/agents.py` - Endpoints da API
- `examples/agentos_integration_example.py` - Como funciona

### Documentação
- [Getting Started](./getting-started.md) - Setup inicial projeto
- [AgentOS Integration](./agentos-integration.md) - Detalhes técnicos
- [Usage Guides](./usage-guides.md) - Integrações existentes

## 💡 Dicas Pro

1. **Monitoramento**: Configure alertas para falhas
2. **Testing**: Sempre teste antes de produção
3; **Backup**: Mantenha configurações em repositório
4. **Comunicação**: Documente tudo que mudar
5. **Feedback**: Coleta dados de usuários para melhorias

---

**🎯 Objetivo**: Você deve conseguir operar o sistema AgentOS de forma independente em 1 semana!

**❓ Dúvidas?** Documente e compartilhe - isso ajuda toda a equipe a crescer junto.
