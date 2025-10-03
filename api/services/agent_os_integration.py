"""
Integração do AgentOS com o projeto MrDom SDR.
Este módulo demonstra como incorporar agentes avançados usando AgentOS.
"""

import os
from typing import Dict, Any, Optional, List
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
import logging

logger = logging.getLogger(__name__)


class MrDomAgentIntegration:
    """Classe para gerenciar a integração com AgentOS."""
    
    def __init__(self):
        self.agent_os = None
        self.agents_config = self._load_agents_config()
        self._initialize_agent_os()
    
    def _load_agents_config(self) -> Dict[str, Any]:
        """Carrega a configuração dos agentes a partir das variáveis de ambiente."""
        return {
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
            "max_tokens": int(os.getenv("AGENT_MAX_TOKENS", "1000")),
            "temperature": float(os.getenv("AGENT_TEAMPERATURE", "0.7")),
            "agents": {
                "lead_qualifier": {
                    "id": "lead-qualifier",
                    "model": "gpt-4",
                    "system_prompt": "Você é um especialista em qualificação de leads BANT (Budget, Authority, Need, Timeline)."
                },
                "sales_sdr": {
                    "id": "sales-sdr", 
                    "model": "gpt-4",
                    "system_prompt": "Você é um SDR experiente focado em gerar interesse e agendar reuniões de vendas."
                },
                "customer_success": {
                    "id": "customer-success",
                    "model": "gpt-4", 
                    "system_prompt": "Você é especialista em sucesso do cliente, focado em resolver problemas e aumentar satisfação."
                }
            }
        }
    
    def _initialize_agent_os(self):
        """Inicializa o AgentOS com os agentes configurados."""
        try:
            # Verifica se a chave da OpenAI está disponível
            if not os.getenv("OPENAI_API_KEY"):
                logger.warning("OPENAI_API_KEY não encontrada. AgentOS não será inicializado.")
                return
            
            # Cria os agentes
            agents = []
            for agent_id, config in self.agents_config["agents"].items():
                sistema_prompt = config["system_prompt"]
                
                agente = Agent(
                    id=config["id"],
                    model=OpenAIChat(
                        id=config["model"],
                        sistema_prompt=sistema_prompt,
                    ),
                )
                agents.append(agente)
            
            # Inicializa AgentOS
            self.agent_os = AgentOS(
                agents=agents,
                chat_history=False,  # Desabilita histórico por enquanto
            )
            
            logger.info(f"AgentOS inicializado com {len(agents)} agentes")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar AgentOS: {str(e)}")
            self.agent_os = None
    
    def get_available_agents(self) -> List[str]:
        """Retorna lista de agentes disponíveis."""
        if not self.agent_os:
            return []
        
        return [agent.id for agent in self.agent_os.agents]
    
    async def process_with_agent(self, agent_id: str, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa uma mensagem usando um agente específico.
        
        Args:
            agent_id: ID do agente a ser usado
            message: Mensagem a ser processada
            context: Contexto adicional (opcional)
            
        Returns:
            Dict com resposta do agente e metadados
        """
        if not self.agent_os:
            return {
                "error": "AgentOS não está inicializado",
                "success": False
            }
        
        try:
            # Encontra o agente
            agente = next((a for a in self.agent_os.agents if a.id == agent_id), None)
            if not agente:
                return {
                    "error": f"Agente '{agent_id}' não encontrado",
                    "success": False,
                    "available_agents": self.get_available_agents()
                }
            
            # Prepara o contexto da mensagem
            mensagem_com_contexto = message
            if context:
                contexto_str = ", ".join([f"{k}: {v}" for k, v in context.items()])
                mensagem_com_contexto = f"Contexto: {contexto_str}\n\nMensagem: {message}"
            
            # Processa a mensagem
            response = await agente.arun(mensagem_com_contexto)
            
            return {
                "success": True,
                "agent_id": agent_id,
                "message": message,
                "response": response.content,
                "context_used": context is not None
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem com agente {agent_id}: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "agent_id": agent_id
            }
    
    async def get_best_agent_suggestions(self, message: str) -> List[str]:
        """
        Sugere qual agente seria melhor para processar uma mensagem.
        
        Args:
            message: Mensagem a ser analisada
            
        Returns:
            Lista de IDs de agentes ordenados por relevância
        """
        # Lógica simples baseada em palavras-chave
        message_lower = message.lower()
        
        suggestions = []
        
        if any(word in message_lower for word in ["orçamento", "preço", "custo", "investimento"]):
            suggestions.append("lead-qualifier")
            
        if any(word in message_lower for word in ["reunião", "demo", "agendar", "apresentação"]):
            suggestions.append("sales-sdr")
            
        if any(word in message_lower for word in ["problema", "bug", "erro", "suporte"]):
            suggestions.append("customer-success")
            
        # Se não tem sugestões específicas, volta para todos disponíveis
        if not suggestions:
            suggestions = self.get_available_agents()
            
        return suggestions
    
    def is_agent_os_available(self) -> bool:
        """Verifica se AgentOS está disponível."""
        return self.agent_os is not None


# Instância global para ser usada nos routers
agent_integration = MrDomAgentIntegration()
