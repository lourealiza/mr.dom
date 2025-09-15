## Visão Geral

O MR.DOM é uma API FastAPI para automação de pré-vendas (SDR), integrando Chatwoot (suporte/omnichannel), N8N (workflows) e OpenAI (IA) para analisar mensagens, qualificar leads e acionar automações.

### Componentes Principais
- API (`api/main.py`): monta os roteadores, middlewares e métricas Prometheus.
- Roteadores:
  - `health` — saúde e readiness.
  - `chatwoot_agentbot` — webhook do AgentBot do Chatwoot.
- Serviços:
  - `ChatwootClient` — operações na API do Chatwoot.
  - `N8NClient` e `trigger` — disparo de webhooks e execuções de workflows.
  - `OpenAIClient` — análise de intenção, respostas, follow-ups, extração de contato.
- Domínio:
  - `models.py` — modelos Pydantic e enums (intenção, níveis etc.).
  - `bot_logic.py` — orquestra lógica de decisão e diálogo passo-a-passo (`step_transition`).

### Fluxo Alto Nível
1) Chatwoot envia evento ao webhook `/api/v1/webhooks/agentbot`.
2) Validação HMAC, leitura do estado atual da conversa.
3) `step_transition` atualiza o `State`, decide próxima mensagem e ação (ex.: handoff, criar lead, agendar).
4) Estado é persistido como `custom_attributes` no Chatwoot e a resposta é enviada via `ChatwootClient`.
5) Integrações como N8N podem ser acionadas conforme a ação definida.

