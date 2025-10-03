# 📋 Checklist de Transição - AgentOS MrDom SDR

## ✅ Para a Pessoa que Você Está Passando

### 📞 Primeiro Contato (15 min)
- [ ] Enviar este checklist: `docs/operational-handover-guide.md`
- [ ] Agendar uma call de 30min para explicação rápida
- [ ] Disponibilizar acesso ao repositório/ambiente

### 🚀 Setup Inicial (30 min)
- [ ] Executar validação rápida: `python scripts/quick-validation.py`
- [ ] Seguir diagnóstico automático do script
- [ ] Instalar dependências necessárias
- [ ] Configurar variáveis de ambiente

### 🧪 Teste Operacional (20 min)
- [ ] Rodar servidor: `python examples/agentos_integration_example.py`
- [ ] Testar todos endpoints: `/api/v1/agents/*`
- [ ] Verificar integração Chatwoot funcionando
- [ ] Documentar qualquer problema encontrado

### 📚 Estudar Documentação (45 min distribuídos)
- [ ] Ler: [README-AGENTOS.md](README-AGENTOS.md)
- [ ] Revisar: [docs/operational-handover-guide.md](docs/operational-handover-guide.md)
- [ ] Entender: [docs/agentos-integration.md](docs/agentos-integration.md)

---

## 📝 Informações Essenciais

### 🔑 Acesso Necessário
- **Repositório**: [branch `agentes`]
- **OpenAI API**: Chave válida em `OPENAI_API_KEY`
- **Ambiente**: Desenvolvimento local

### 📞 Em Caso de Emergência
1. **Sistema não funciona**: Restart + check logs
2. **Agentes não respondem**: Verificar API key OpenAI
3. **Chatwoot quebrou**: Verificar webhooks

### 🎯 Responsabilidades Operacionais
- Monitorar agentes funcionando ✅
- Responder a problemas técnicos ❌
- Escalar quando necessário 📞
- Documentar melhorias 📝

### 📊 Relatórios Diários (5min)
- Status agentes
- Qtd conversas automáticas
- Principais problemas
- Sugestões melhorias

---

## 🚨 Problema? Chama o Próximo

### ❌ Quando Chamar Você (Arquitetura/Mudanças):
- Implementar novo agente
- Mudança em arquitetura
- Decisões de infraestrutura
- Budget OpenAI/custos

### ✅ Essa Pessoa Resolve Sozinha (Operacional):
- Agentes não respondem
- Restart serviços
- Configurar novo contexto
- Ajustar respostas simples

---

## 📱 Meios de Contato

- **Slack/Discord**: [seu contato]
- **Emergência**: [seu celular]
- **Email**: [seu email]

### Horários Disponíveis
- **Suporte rápido**: Seg-Ter, 9-17h
- **Emergência**: Contato direto
- **Plantão**: Ver definir

---

## ✅ Você Está Pronto Quando...

- [ ] Consegue rodar sistema sem ajuda
- [ ] Identifica quando algo não funciona
- [ ] Sabe quando escalar problema
- [ ] Tem documentação de referência
- [ ] Consulteu dúvidas básicas

**⏰ Prazo esperado**: 1 semana para operação independente
