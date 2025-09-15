## Domínio

### Modelos (Pydantic) — `api/domain/models.py`
- `State`: estado conversacional persistido nos `custom_attributes` do Chatwoot.
- `MessageAnalysis`: resultado da análise de intenção.
- `LeadQualification`: dados de qualificação.
- `AgentBotResponse`, `ConversationContext`, `ContactInfo`, `BotConfiguration`.
- Enums: `IntentType`, `ActionType`, `InterestLevel`, `UrgencyLevel`.

### Lógica do Bot — `api/domain/bot_logic.py`
- `BotLogic`: orquestra regras de decisão e integra OpenAI.
  - `analyze_message(message) -> MessageAnalysis`
  - `determine_action(analysis) -> ActionType`
  - `generate_response(analysis) -> str`
  - `qualify_lead(history) -> LeadQualification`
  - `handle_objection(objection, context) -> str`
  - `generate_follow_up_message(lead_info, follow_up_type) -> str`
  - utilitários: `is_business_hours()`, `get_welcome_message()`

- `extract_name(text) -> str|None`: heurística simples para extrair nome.
- `step_transition(state, user_text) -> (state, reply_text, action)`:
  - Fluxo guiado por perguntas: nome → empresa → cargo → ferramentas → dor → handoff.

### Exemplos
```python
from api.domain.models import State
from api.domain.bot_logic import step_transition

state = State()
state, reply, action = step_transition(state, "Oi, sou a Maria")
# reply: pergunta próxima (empresa)

state, reply, action = step_transition(state, "MrDom Tech")
# reply: pergunta cargo
```

