import os
import logging
from typing import Dict, Any

import httpx

logger = logging.getLogger(__name__)


class ChatwootClient:
    def __init__(self):
        # Load config lazily so app can boot without Chatwoot vars
        self.base_url = os.getenv("CHATWOOT_BASE_URL", "https://app.chatwoot.com").rstrip("/")
        self.access_token = os.getenv("CHATWOOT_ACCESS_TOKEN")
        self.account_id = os.getenv("CHATWOOT_ACCOUNT_ID")
        self.headers = None  # built on demand

    def _ensure_config(self) -> None:
        if not self.base_url or not self.access_token or not self.account_id:
            raise RuntimeError(
                "Chatwoot não configurado. Defina CHATWOOT_BASE_URL, CHATWOOT_ACCESS_TOKEN e CHATWOOT_ACCOUNT_ID"
            )
        # Build headers if needed
        if not self.headers:
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

    async def test_connection(self) -> Dict[str, Any]:
        self._ensure_config()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/accounts/{self.account_id}",
                headers=self.headers,
                timeout=15.0,
            )
            response.raise_for_status()
            return {"status": "connected", "account": response.json()}

    async def get_conversation(self, account_id: str, conversation_id: int) -> Dict[str, Any]:
        self._ensure_config()
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}"
            r = await client.get(url, headers=self.headers, timeout=15.0)
            r.raise_for_status()
            return r.json()

    async def set_attributes(self, account_id: str, conversation_id: int, **attributes: Any) -> Dict[str, Any]:
        self._ensure_config()
        payload = {"custom_attributes": attributes}
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}"
            r = await client.patch(url, headers=self.headers, json=payload, timeout=15.0)
            r.raise_for_status()
            return r.json()

    async def reply(self, account_id: str, conversation_id: int, content: str, private: bool = False) -> Dict[str, Any]:
        self._ensure_config()
        payload = {
            "content": content,
            "message_type": "outgoing",
            "private": private,
        }
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
            r = await client.post(url, headers=self.headers, json=payload, timeout=15.0)
            r.raise_for_status()
            return r.json()

    async def set_status(self, account_id: str, conversation_id: int, status: str) -> Dict[str, Any]:
        self._ensure_config()
        allowed = {"open", "resolved", "snoozed", "pending"}
        if status not in allowed:
            raise ValueError(f"status inválido: {status}")
        payload = {"status": status}
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}"
            r = await client.patch(url, headers=self.headers, json=payload, timeout=15.0)
            r.raise_for_status()
            return r.json()


chatwoot_client = ChatwootClient()
