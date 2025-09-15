# Exemplos de Integração

## 1) Consumindo a API de Health/Readiness

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/readiness
```

## 2) Simulando o Webhook do Chatwoot

Calcule o HMAC do corpo e envie no header `X-Chatwoot-Signature`.

```python
import hmac, hashlib, json, requests

secret = b"minha_chave_hmac"
body = {
    "event": "message_created",
    "account": {"id": "1"},
    "conversation": {"id": 123},
    "message": {"content": "Oi, sou a Ana", "message_type": "incoming"}
}
raw = json.dumps(body, ensure_ascii=False).encode()
sign = hmac.new(secret, msg=raw, digestmod=hashlib.sha256).hexdigest()

r = requests.post(
    "http://localhost:8000/api/v1/webhooks/agentbot",
    headers={"Content-Type": "application/json", "X-Chatwoot-Signature": sign},
    data=raw,
)
print(r.status_code, r.text)
```

## 3) Usando `ChatwootClient`

```python
import asyncio
from api.services.chatwoot_client import chatwoot_client

async def main():
    await chatwoot_client.reply("<ACCOUNT_ID>", 123, "Olá! Como posso ajudar?")

asyncio.run(main())
```

## 4) Disparando workflow no N8N via webhook

```python
from api.services.n8n_client import trigger

await trigger("create_lead", {"nome": "Ana", "email": "ana@ex.com"})
```

## 5) Usando `OpenAIClient`

```python
import asyncio
from api.services.openai_client import OpenAIClient

async def main():
    client = OpenAIClient()
    text = await client.generate_response("Quais planos vocês oferecem?", {"intent": "question"})
    print(text)

asyncio.run(main())
```