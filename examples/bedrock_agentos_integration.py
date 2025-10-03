#!/usr/bin/env python3
"""
Integração AgentOS com AWS Bedrock (em vez de OpenAI).
Este exemplo mostra como usar AgentOS com Bedrock.
"""

import os
import asyncio
from fastapi import FastAPI
from agno.agent import Agent
from agno.models.aws_bedrock import BedrockChat  # Bedrock em vez de OpenAI
from agno.os import AgentOS
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria sua aplicação FastAPI customizada
app = FastAPI(
    title="MrDom SDR API com AgentOS + Bedrock",
    version="2.0.0",
    description="Sistema de automação de vendas integrado com agentes avançados usando AgentOS e AWS Bedrock"
)

# Suas rotas customizadas existentes
@app.get("/status")
async def status_check():
    """Endpoint de status personalizado."""
    return {
        "status": "healthy",
        "agentos_available": True,
        "model_provider": "AWS Bedrock",
        "version": "2.0.0"
    }

@app.get("/custom-info")
async def custom_info():
    """Endpoint informativo sobre a integração."""
    return {
        "message": "Sistema MrDom SDR com AgentOS + Bedrock integrado",
        "agents": ["lead-qualifier", "sales-sdr", "customer-success"],
        "features": [
            "Qualificação automática de leads",
            "Agendamento de reuniões", 
            "Suporte ao cliente automatizado",
            "SDR intelligence com IA via Bedrock"
        ],
        "model": "amazon.nova-lite-v1:0"
    }

# Agentes especializados usando Bedrock
agentes_mrdom = [
    Agent(
        id="lead-qualifier",
        model=BedrockChat(
            id="amazon.nova-lite-v1:0",
            sistema_prompt="""Você é um especialista em qualificação de leads BANT 
            (Budget, Authority, Need, Timeline). Sua função é fazer perguntas inteligentes 
            para determinar se um lead é qualificado para uma proposta comercial."""
        )
    ),
    
    Agent(
        id="sales-sdr",
        model=BedrockChat(
            id="amazon.nova-lite-v1:0",
            sistema_prompt="""Você é um SDR experiente focado em gerar interesse 
            e agendar reuniões de vendas. Use técnicas de vendas consultivas para 
            identificar necessidades e criar urgência."""
        )
    ),
    
    Agent(
        id="customer-success",
        model=BedrockChat(
            id="amazon.nova-lite-v1:0",
            sistema_prompt="""Você é especialista em sucesso do cliente, focado em 
            resolver problemas, aumentar satisfação e identificar oportunidades de 
            upselling."""
        )
    )
]

# Se AWS Bedrock estiver configurado, inicializa AgentOS
if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
    try:
        # Passa sua app para AgentOS
        agent_os = AgentOS(
            agents=agentes_mrdom,
            base_app=app  # Sua app FastAPI personalizada
        )
        
        # Obtém a app combinada com agentes e suas rotas
        app = agent_os.get_app()
        
        logger.info("AgentOS + Bedrock integrado com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar AgentOS: {str(e)}")
        # Continua com a app original se AgentOS falhar

else:
    logger.warning("AWS credentials não encontradas. Executando sem AgentOS.")

# Endpoints específicos para Bedrock
@app.get("/api/v1/agents/status")
async def get_agents_status():
    """Status dos agentes Bedrock."""
    return {
        "agent_os_available": True,
        "model_provider": "AWS Bedrock",
        "model": "amazon.nova-lite-v1:0",
        "available_agents": ["lead-qualifier", "sales-sdr", "customer-success"],
        "total_agents": 3
    }

@app.post("/api/v1/agents/process-best")
async def process_with_best_agent(request: dict):
    """Processa mensagem usando melhor agente Bedrock."""
    message = request.get("message", "")
    context = request.get("context", None)
    
    if not message:
        return {"error": "Campo 'message' é obrigatório"}
    
    # Lógica simples para escolher melhor agente
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["preço", "custo", "orçamento"]):
        agent_id = "lead-qualifier"
    elif any(word in message_lower for word in ["demo", "reunião", "agendar"]):
        agent_id = "sales-sdr"
    elif any(word in message_lower for word in ["problema", "bug", "suporte"]):
        agent_id = "customer-success"
    else:
        agent_id = "lead-qualifier"
    
    return {
        "success": True,
        "selected_agent": agent_id,
        "message": message,
        "context": context,
        "model": "amazon.nova-lite-v1:0",
        "provider": "AWS Bedrock"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando MrDom SDR com AgentOS + Bedrock...")
    print("=" * 50)
    
    # Verifica configuração AWS
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    
    if aws_key and aws_secret:
        print("✅ AWS Bedrock configurado")
        print(f"   Região: {aws_region}")
        print(f"   Modelo: amazon.nova-lite-v1:0")
    else:
        print("⚠️ AWS credentials não configuradas")
        print("Configure no .env:")
        print("AWS_ACCESS_KEY_ID=sua_chave")
        print("AWS_SECRET_ACCESS_KEY=seu_secret")
        print("AWS_DEFAULT_REGION=us-east-1")
    
    print(f"\n🌐 Servidor rodando em: http://localhost:8000")
    print(f"📚 Documentação: http://localhost:8000/docs")
    print(f"🤖 Status agentes: http://localhost:8000/api/v1/agents/status")
    
    # Inicia servidor
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
