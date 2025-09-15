## Serviços

### ChatwootClient (`api/services/chatwoot_client.py`)
- Configuração via env: `CHATWOOT_BASE_URL`, `CHATWOOT_ACCESS_TOKEN`, `CHATWOOT_ACCOUNT_ID`.
- Métodos:
  - `test_connection() -> {status, account}`
  - `get_conversation(account_id, conversation_id) -> JSON`
  - `set_attributes(account_id, conversation_id, **attributes) -> JSON`
  - `reply(account_id, conversation_id, content, private=False) -> JSON`
  - `set_status(account_id, conversation_id, status)` com `status` em `{open,resolved,snoozed,pending}`

Exemplo:
```python
from api.services.chatwoot_client import chatwoot_client

data = await chatwoot_client.get_conversation("123", 456)
await chatwoot_client.reply("123", 456, "Olá! Como posso ajudar?")
await chatwoot_client.set_attributes("123", 456, empresa="MrDom Tech")
```

### N8N
- Função utilitária `trigger(slug, payload)` para webhooks públicos/privados (env: `N8N_BASE_URL`, auth básica opcional `N8N_BASIC_AUTH_USER`/`N8N_BASIC_AUTH_PASSWORD`).
- Cliente `N8NClient` para API: lista e executa workflows via `N8N_API_KEY`.

Métodos principais `N8NClient`:
- `test_connection()`
- `list_workflows()`
- `trigger_workflow(workflow_name, data)`
- Auxiliares de domínio: `trigger_lead_qualification`, `trigger_initial_qualification`, `trigger_follow_up`, `trigger_crm_sync`, `trigger_email_sequence`, `get_workflow_status`.

Exemplo (webhook):
```python
from api.services.n8n_client import trigger

res = await trigger("create_lead", {"nome": "João", "email": "joao@exemplo.com"})
```

Exemplo (API):
```python
from api.services.n8n_client import N8NClient

n8n = N8NClient()
await n8n.test_connection()
await n8n.trigger_workflow("lead-qualification", {"conversation_id": 456})
```

### OpenAIClient (`api/services/openai_client.py`)
- Requer `OPENAI_API_KEY` e opcional `OPENAI_MODEL` (default: `gpt-3.5-turbo`).
- Funcionalidades:
  - `analyze_message_intent(message) -> dict`
  - `generate_response(message, context=None) -> str`
  - `handle_objection(objection, product_context) -> str`
  - `qualify_lead(conversation_history) -> dict`
  - `generate_follow_up_message(lead_info, follow_up_type) -> str`
  - `extract_contact_info(message) -> dict`

Exemplo:
```python
from api.services.openai_client import OpenAIClient

client = OpenAIClient()
analysis = await client.analyze_message_intent("Quais planos vocês têm?")
response = await client.generate_response("Quero saber preços", {"intent": "question"})
```

