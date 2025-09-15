# Serviços e Clientes

Esta seção documenta os clientes e integrações disponíveis em `api/services/`.

## ChatwootClient — `api/services/chatwoot_client.py`

Classe principal para integração com a API do Chatwoot.

### Configuração

- `CHATWOOT_BASE_URL` (ex.: `https://app.chatwoot.com`)
- `CHATWOOT_ACCESS_TOKEN`
- `CHATWOOT_ACCOUNT_ID`

### API

- `async test_connection() -> Dict[str, Any]`
- `async get_conversation(account_id: str, conversation_id: int) -> Dict[str, Any]`
- `async set_attributes(account_id: str, conversation_id: int, **attributes: Any) -> Dict[str, Any]`
- `async reply(account_id: str, conversation_id: int, content: str, private: bool = False) -> Dict[str, Any]`
- `async set_status(account_id: str, conversation_id: int, status: str) -> Dict[str, Any]`

### Exemplo de uso

```python
import asyncio
from api.services.chatwoot_client import chatwoot_client

async def main():
    await chatwoot_client.test_connection()
    conv = await chatwoot_client.get_conversation("<ACCOUNT_ID>", 123)
    await chatwoot_client.set_attributes("<ACCOUNT_ID>", 123, etapa="qualificacao")
    await chatwoot_client.reply("<ACCOUNT_ID>", 123, "Olá! Como posso ajudar?")
    await chatwoot_client.set_status("<ACCOUNT_ID>", 123, "open")

asyncio.run(main())
```

---

## N8N — `api/services/n8n_client.py`

Existem duas interfaces:

- Função simples `trigger(slug: str, payload: dict)` para webhooks públicos/privados.
- Classe `N8NClient` para disparo via API autenticada por chave.

### Configuração

- `N8N_BASE_URL`
- Autenticação alternativa:
  - `N8N_API_KEY`, ou
  - `N8N_BASIC_AUTH_USER`/`N8N_BASIC_AUTH_PASSWORD` (apenas para `trigger` por webhook, se necessário)

### API (função)

- `async trigger(slug: str, payload: dict) -> dict`

### API (classe)

- `async test_connection() -> Dict[str, Any]`
- `async trigger_workflow(workflow_name: str, data: Dict[str, Any]) -> Dict[str, Any]`
- `async get_workflow_status(execution_id: str) -> Dict[str, Any]`
- `async list_workflows() -> Dict[str, Any]`
- Atalhos específicos:
  - `async trigger_lead_qualification(conversation_id: int, message_content: str, contact_info: Dict[str, Any])`
  - `async trigger_initial_qualification(conversation_id: int, contact_info: Dict[str, Any])`
  - `async trigger_follow_up(contact_id: int, follow_up_type: str, scheduled_time: Optional[str] = None)`
  - `async trigger_crm_sync(contact_data: Dict[str, Any], action: str = "create_or_update")`
  - `async trigger_email_sequence(contact_email: str, sequence_name: str, custom_variables: Optional[Dict[str, Any]] = None)`

### Exemplo de uso (webhook)

```python
from api.services.n8n_client import trigger

await trigger("create_lead", {"nome": "Ana", "email": "ana@ex.com"})
```

### Exemplo de uso (API com chave)

```python
import asyncio
from api.services.n8n_client import N8NClient

async def main():
    n8n = N8NClient()
    await n8n.test_connection()
    res = await n8n.trigger_workflow("lead-qualification", {"lead_id": 42})
    print(res)

asyncio.run(main())
```

---

## OpenAIClient — `api/services/openai_client.py`

Client assíncrono para operações com OpenAI.

### Configuração

- `OPENAI_API_KEY` (obrigatório)
- `OPENAI_MODEL` (padrão: `gpt-3.5-turbo`)

### API

- `async analyze_message_intent(message: str) -> Dict[str, Any]`
- `async generate_response(message: str, context: Optional[Dict[str, Any]] = None) -> str`
- `async handle_objection(objection: str, product_context: str) -> str`
- `async qualify_lead(conversation_history: List[Dict[str, str]]) -> Dict[str, Any]`
- `async generate_follow_up_message(lead_info: Dict[str, Any], follow_up_type: str) -> str`
- `async extract_contact_info(message: str) -> Dict[str, Any]`

### Exemplo de uso

```python
import asyncio
from api.services.openai_client import OpenAIClient

async def main():
    client = OpenAIClient()
    analysis = await client.analyze_message_intent("Tenho interesse em uma demonstração")
    reply = await client.generate_response("Quais os planos?", {"intent": "question"})
    print(analysis, reply)

asyncio.run(main())
```

> Observação: todos os métodos são assíncronos.