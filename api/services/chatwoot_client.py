import httpx
import os
import logging
from typing import Dict, Any, Optional
 # Removed import of ChatwootMessage, ChatwootConversation (not present in models.py)

logger = logging.getLogger(__name__)

class ChatwootClient:
    def __init__(self):
        self.base_url = os.getenv("CHATWOOT_BASE_URL", "https://app.chatwoot.com")
        self.access_token = os.getenv("CHATWOOT_ACCESS_TOKEN")
        self.account_id = os.getenv("CHATWOOT_ACCOUNT_ID")
        if not self.access_token or not self.account_id:
            raise ValueError("CHATWOOT_ACCESS_TOKEN e CHATWOOT_ACCOUNT_ID são obrigatórios")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
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



chatwoot_client = ChatwootClient()
