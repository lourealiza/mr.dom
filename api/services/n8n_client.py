import httpx
import os

BASE = os.getenv("N8N_BASE_URL", "").rstrip("/")
USER = os.getenv("N8N_BASIC_AUTH_USER")
PASS = os.getenv("N8N_BASIC_AUTH_PASSWORD")
AUTH = (USER, PASS) if USER else None

async def trigger(slug: str, payload: dict):
    """Dispara um webhook público/privado do n8n e retorna JSON quando houver."""
    if not BASE:
        raise RuntimeError("N8N_BASE_URL não definido")
    url = f"{BASE}/webhook/{slug}"
    async with httpx.AsyncClient(timeout=30.0) as c:
        r = await c.post(url, json=payload, auth=AUTH)
        r.raise_for_status()
        ct = r.headers.get("content-type", "")
        return r.json() if "application/json" in ct else {"status": r.status_code}
import logging
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class N8NClient:
    def __init__(self):
        self.base_url = os.getenv("N8N_BASE_URL", "http://localhost:5678")
        self.api_key = os.getenv("N8N_API_KEY")
        
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            self.headers["X-N8N-API-KEY"] = self.api_key

    async def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com N8N"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/workflows",
                    headers=self.headers
                )
                response.raise_for_status()
                return {"status": "connected", "workflows": response.json()}
            except Exception as e:
                logger.error(f"Erro ao testar conexão N8N: {str(e)}")
                raise

    async def trigger_workflow(
        self, 
        workflow_name: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Disparar um workflow N8N"""
        async with httpx.AsyncClient() as client:
            try:
                # Primeiro, obter o ID do workflow pelo nome
                workflow_id = await self._get_workflow_id_by_name(workflow_name)
                
                if not workflow_id:
                    raise ValueError(f"Workflow '{workflow_name}' não encontrado")
                
                # Disparar o workflow
                payload = {
                    "workflowData": data
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                logger.info(f"Workflow '{workflow_name}' disparado com sucesso")
                return response.json()
                
            except Exception as e:
                logger.error(f"Erro ao disparar workflow: {str(e)}")
                raise

    async def _get_workflow_id_by_name(self, workflow_name: str) -> Optional[str]:
        """Obter ID do workflow pelo nome"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/workflows",
                    headers=self.headers
                )
                response.raise_for_status()
                
                workflows = response.json().get("data", [])
                for workflow in workflows:
                    if workflow.get("name") == workflow_name:
                        return workflow.get("id")
                
                return None
                
            except Exception as e:
                logger.error(f"Erro ao obter workflows: {str(e)}")
                raise

    async def trigger_lead_qualification(
        self, 
        conversation_id: int, 
        message_content: str,
        contact_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Disparar workflow de qualificação de lead"""
        data = {
            "conversation_id": conversation_id,
            "message_content": message_content,
            "contact_info": contact_info,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return await self.trigger_workflow("lead-qualification", data)

    async def trigger_initial_qualification(
        self, 
        conversation_id: int, 
        contact_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Disparar workflow de qualificação inicial"""
        data = {
            "conversation_id": conversation_id,
            "contact_info": contact_info,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return await self.trigger_workflow("initial-qualification", data)

    async def trigger_follow_up(
        self, 
        contact_id: int, 
        follow_up_type: str,
        scheduled_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """Disparar workflow de follow-up"""
        data = {
            "contact_id": contact_id,
            "follow_up_type": follow_up_type,
            "scheduled_time": scheduled_time,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return await self.trigger_workflow("follow-up", data)

    async def trigger_crm_sync(
        self, 
        contact_data: Dict[str, Any],
        action: str = "create_or_update"
    ) -> Dict[str, Any]:
        """Disparar sincronização com CRM"""
        data = {
            "contact_data": contact_data,
            "action": action,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return await self.trigger_workflow("crm-sync", data)

    async def trigger_email_sequence(
        self, 
        contact_email: str, 
        sequence_name: str,
        custom_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Disparar sequência de emails"""
        data = {
            "contact_email": contact_email,
            "sequence_name": sequence_name,
            "custom_variables": custom_variables or {},
            "timestamp": asyncio.get_event_loop().time()
        }
        
        return await self.trigger_workflow("email-sequence", data)

    async def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """Obter status de execução de um workflow"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/executions/{execution_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
            except Exception as e:
                logger.error(f"Erro ao obter status do workflow: {str(e)}")
                raise

    async def list_workflows(self) -> Dict[str, Any]:
        """Listar todos os workflows disponíveis"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/workflows",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
            except Exception as e:
                logger.error(f"Erro ao listar workflows: {str(e)}")
                raise
