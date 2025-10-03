"""
Exemplo de integração completa do AgentOS com o projeto MrDom SDR.
Este arquivo demonstra como incorporar AgentOS seguindo o padrão fornecido.
"""

import os
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# Configuração de ambiente (simulando carregamento do .env)
os.environ.setdefault("OPENAI_API_KEY", "sua_chave_openai_aqui")

# Importações do projeto existente (ajustar paths conforme necessário)
from pathlib import Path
import sys

# Adiciona o path da API ao sys.path para importações
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

# Importa componentes do projeto existente
from routers.chatwoot_agentbot import router as chatwoot_router
from routers.health import router as health_router
from routers.agents import router as agents_router
from services.agent_os_integration import agent_integration

# Configuração de logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria sua aplicação FastAPI customizada
app = FastAPI(
    title="MrDom SDR API com AgentOS",
    version="2.0.0",
    description="Sistema de automação de vendas integrado com agentes avançados usando AgentOS"
)

# Adiciona suas rotas customizadas existentes
@app.get("/status")
async def status_check():
    """Endpoint de status personalizado."""
    return {
        "status": "healthy",
        "agentos_available": agent_integration.is_agent_os_available(),
        "version": "2.0.0"
    }

@app.get("/custom-info")
async def custom_info():
    """Endpoint informativo sobre a integração."""
    available_agents = agent_integration.get_available_agents()
    return {
        "message": "Sistema MrDom SDR com AgentOS integrado",
        "agents": available_agents,
        "features": [
            "Qualificação automática de leads",
            "Agendamento de reuniões",
            "Suporte ao cliente automatizado",
            "SDR intelligence com IA"
        ]
    }

# Inclui os routers existentes
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["platform"]
)

app.include_router(
    chatwoot_router, 
    prefix="/api/v1/webhooks",
    tags=["webhooks"]
)

# Inclui o router de agentes AgentOS
app.include_router(
    agents_router,
    prefix="/api/v1/agents",
    tags=["agents"]
)

# Exemplo de configuração AgentOS mais avançada seguindo seu padrão
# Criação dos agentes especializados
agentes_mrdom = [
    Agent(
        id="lead-qualifier",
        model=OpenAIChat(
            id="gpt-4",
            sistema_prompt="""Você é um especialista em qualificação de leads BANT 
            (Budget, Authority, Need, Timeline). Sua função é fazer perguntas inteligentes 
            para determinar se um lead é qualificado para uma proposta comercial."""
        )
    ),
    
    Agent(
        id="sales-sdr",
        model=OpenAIChat(
            id="gpt-4",
            sistema_prompt="""Você é um SDR experiente focado em gerar interesse 
            e agendar reuniões de vendas. Use técnicas de vendas consultivas para 
            identificar necessidades e criar urgência."""
        )
    ),
    
    Agent(
        id="customer-success",
        model=OpenAIChat(
            id="gpt-4",
            sistema_prompt="""Você é especialista em sucesso do cliente, focado em 
            resolver problemas, aumentar satisfação e identificar oportunidades de 
            upselling."""
        )
    )
]

# Se OPENAI_API_KEY estiver disponível, inicializa AgentOS
if os.getenv("OPENAI_API_KEY"):
    try:
        # Passa sua app para AgentOS
        agent_os = AgentOS(
            agents=agentes_mrdom,
            base_app=app  # Sua app FastAPI personalizada
        )
        
        # Obtém a app combinada com agentes e suas rotas
        app = agent_os.get_app()
        
        logger.info("AgentOS integrado com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar AgentOS: {str(e)}")
        # Continua com a app original se AgentOS falhar

else:
    logger.warning("OPENAI_API_KEY não encontrada. Executando sem AgentOS.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
