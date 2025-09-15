# Domínio e Modelos

Esta seção cobre a lógica de domínio do bot e os modelos Pydantic utilizados ao longo do projeto.

## `api/domain/models.py`

Modelos e enums principais:

- `State`: estado conversacional persistido em `custom_attributes` no Chatwoot. Campos: `nome`, `sobrenome`, `empresa`, `cargo`, `email`, `celular`, `horario1`, `horario2`, `ferramentas`, `dor_principal`.
- `QualifyPayload`: payload para qualificação de leads com validações (e.g., timezone obrigatório em `horario1/2`).
- `ChatInput`: entrada de chat com `message` e `context`.
- Enums: `IntentType`, `ActionType`, `InterestLevel`, `UrgencyLevel`.
- Estruturas auxiliares: `MessageAnalysis`, `LeadQualification`, `AgentBotResponse`, `ConversationContext`, `ContactInfo`, `BotConfiguration`.

### Exemplo de uso do `State`

```python
from api.domain.models import State

state = State(nome="Ana")
state.empresa = "Empresa X"
```

---

## `api/domain/bot_logic.py`

Contém a classe `BotLogic` e funções auxiliares para análise e respostas:

- `BotLogic.analyze_message(message_content) -> MessageAnalysis`
- `BotLogic.determine_action(analysis) -> ActionType`
- `BotLogic.generate_response(analysis) -> str`
- `BotLogic.qualify_lead(conversation_history) -> LeadQualification`
- `BotLogic.handle_objection(objection, product_context) -> str`
- `BotLogic.generate_follow_up_message(lead_info, follow_up_type) -> str`
- `BotLogic.is_business_hours() -> bool`
- Contexto por conversa: `get_conversation_context`, `update_conversation_context`

Funções utilitárias:

- `extract_name(text: str) -> str | None`
- `step_transition(state: State, user_text: str) -> tuple[State, str, str]`

### Exemplo — fluxo `step_transition`

```python
from api.domain.models import State
from api.domain.bot_logic import step_transition

state = State()
state, reply, action = step_transition(state, "Oi, sou a Ana")
# -> pergunta nome/empresa, progride etapas, define action (ex.: handoff)
```

> Observação: `step_transition` é um fluxo simples de exemplo e pode ser trocado por lógicas mais ricas do `BotLogic`.