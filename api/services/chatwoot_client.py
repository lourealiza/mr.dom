import httpx
import os
import logging
from typing import Dict, Any, Optional
 # Removed import of ChatwootMessage, ChatwootConversation (not present in models.py)

logger = logging.getLogger(__name__)

class ChatwootClient:
    def __init__(self):
        self.base_url = os.getenv("CHATWOOT_BASE_URL", "https://app.chatwoot.com").rstrip('/')
        self.access_token = os.getenv("CHATWOOT_ACCESS_TOKEN")
        self.account_id = os.getenv("CHATWOOT_ACCOUNT_ID")
        if not self.access_token or not self.account_id:
            raise ValueError("CHATWOOT_ACCESS_TOKEN e CHATWOOT_ACCOUNT_ID são obrigatórios")
        self.headers = {
            # Chatwoot Account API expects api_access_token header
            "api_access_token": self.access_token,
            "Content-Type": "application/json",
        }


    async def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com Chatwoot"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/accounts/{self.account_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return {"status": "connected", "account": response.json()}
            except Exception as e:
                logger.error(f"Erro ao testar conexão: {str(e)}")
                raise

    async def get_conversation(self, account_id: str | int, conversation_id: str | int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}",
                headers=self.headers,
            )
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and data.get('payload') is not None:
                return data['payload']
            return data

    async def set_attributes(self, account_id: str | int, conversation_id: str | int, **attrs: Any) -> Dict[str, Any]:
        body_variants = [
            {"custom_attributes": attrs},
            attrs,
        ]
        async with httpx.AsyncClient() as client:
            last_exc = None
            for body in body_variants:
                try:
                    r = await client.post(
                        f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes",
                        headers=self.headers,
                        json=body,
                    )
                    if r.status_code < 300:
                        try:
                            return r.json()
                        except Exception:
                            return {"ok": True}
                except Exception as e:
                    last_exc = e
            if last_exc:
                raise last_exc
            return {"ok": False}

    async def set_status(self, account_id: str | int, conversation_id: str | int, status: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.patch(
                f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}",
                headers=self.headers,
                json={"status": status},
            )
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return {"ok": True}

    async def reply(self, account_id: str | int, conversation_id: str | int, content: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages",
                headers=self.headers,
                json={"content": content, "message_type": "outgoing", "private": False},
            )
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return {"ok": True}



chatwoot_client = ChatwootClient()
