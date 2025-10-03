"""
Router para endpoints relacionados aos agentes AgentOS.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging

from ..services.agent_os_integration import agent_integration
from ..app.core.settings import Settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Modelos Pydantic
class AgentProcessRequest(BaseModel):
    agent_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class AgentProcessResponse(BaseModel):
    success: bool
    agent_id: str
    message: str
    response: Optional[str] = None
    context_used: Optional[bool] = None
    error: Optional[str] = None

class AgentSuggestionRequest(BaseModel):
    message: str

class AgentSuggestionResponse(BaseModel):
    message: str
    suggested_agents: List[str]
    available_agents: List[str]

# Dependency para verificar se AgentOS está disponível
async def check_agent_os_available():
    if not agent_integration.is_agent_os_available():
        raise HTTPException(
            status_code=503, 
            detail="AgentOS não está disponível. Verifique se OPENAI_API_KEY está configurada."
        )


@router.get("/agents/status")
async def get_agents_status():
    """Verifica o status dos agentes AgentOS."""
    return {
        "agent_os_available": agent_integration.is_agent_os_available(),
        "available_agents": agent_integration.get_available_agents(),
        "total_agents": len(agent_integration.get_available_agents())
    }

@router.get("/agents/list")
async def list_agents(_: None = Depends(check_agent_os_available)):
    """Lista todos os agentes disponíveis."""
    agents = agent_integration.get_available_agents()
    return {
        "agents": [
            {
                "id": agent_id,
                "type": agent_id.replace("-", " ").title(),
                "description": f"Agente especializado em {agent_id.replace('-', ' ')}"
            }
            for agent_id in agents
        ]
    }

@router.post("/agents/process", response_model=AgentProcessResponse)
async def process_with_agent(
    request: AgentProcessRequest,
    _: None = Depends(check_agent_os_available)
):
    """
    Processa uma mensagem usando um agente específico.
    
    Args:
        - agent_id: ID do agente (lead-qualifier, sales-sdr, customer-success)
        - message: Mensagem a ser processada
        - context: Contexto adicional (opcional)
    """
    try:
        resultado = await agent_integration.process_with_agent(
            agent_id=request.agent_id,
            message=request.message,
            context=request.context
        )
        
        if not resultado["success"]:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return AgentProcessResponse(**resultado)
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/suggest", response_model=AgentSuggestionResponse)
async def suggest_agent(request: AgentSuggestionRequest):
    """
    Sugere qual agente seria melhor para processar uma mensagem.
    
    Args:
        - message: Mensagem a ser analisada
    """
    try:
        agentes_sugeridos = await agent_integration.get_best_agent_suggestions(request.message)
        agentes_disponiveis = agent_integration.get_available_agents()
        
        return AgentSuggestionResponse(
            message=request.message,
            suggested_agents=agentes_sugeridos,
            available_agents=agentes_disponiveis
        )
        
    except Exception as e:
        logger.error(f"Erro ao sugerir agente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/process-best")
async def process_with_best_agent(
    request: dict,
    _: None = Depends(check_agent_os_available)
):
    """
    Processa uma mensagem usando automaticamente o melhor agente disponível.
    
    Args:
        - message: Mensagem a ser processada  
        - context: Contexto adicional (opcional)
    """
    try:
        message = request.get("message", "")
        context = request.get("context", None)
        
        if not message:
            raise HTTPException(status_code=400, detail="Campo 'message' é obrigatório")
        
        # Encontra o melhor agente
        agentes_sugeridos = await agent_integration.get_best_agent_suggestions(message)
        melhor_agente = agentes_sugeridos[0] if agentes_sugeridos else "lead-qualifier"
        
        # Processa com o melhor agente
        resultado = await agent_integration.process_with_agent(
            agent_id=melhor_agente,
            message=message,
            context=context
        )
        
        return {
            "success": resultado["success"],
            "selected_agent": melhor_agente,
            "all_suggested_agents": agentes_sugeridos,
            "result": resultado
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar com melhor agente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
