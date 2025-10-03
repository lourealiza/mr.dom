#!/usr/bin/env python3
"""
Demonstração funcional sem AgentOS (usando OpenAI diretamente).
Este exemplo mostra como a integração funcionaria.
"""

import os
import asyncio
from fastapi import FastAPI
from openai import AsyncOpenAI
import json

# Configuração
app = FastAPI(title="MrDom SDR Demo - Sem AgentOS")

# Cliente OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-demo"))

# Agentes simulados (sem AgentOS)
AGENTS = {
    "lead-qualifier": {
        "name": "Lead Qualifier",
        "system_prompt": "Você é um especialista em qualificação de leads BANT. Faça perguntas para determinar Budget, Authority, Need e Timeline."
    },
    "sales-sdr": {
        "name": "Sales SDR", 
        "system_prompt": "Você é um SDR experiente focado em gerar interesse e agendar reuniões de vendas."
    },
    "customer-success": {
        "name": "Customer Success",
        "system_prompt": "Você é especialista em sucesso do cliente, focado em resolver problemas e aumentar satisfação."
    }
}

async def process_with_agent(agent_id: str, message: str, context: dict = None):
    """Processa mensagem com agente específico."""
    if agent_id not in AGENTS:
        return {"error": f"Agente '{agent_id}' não encontrado"}
    
    agent = AGENTS[agent_id]
    
    # Prepara contexto
    context_str = ""
    if context:
        context_str = f"\nContexto: {json.dumps(context, ensure_ascii=False)}"
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": agent["system_prompt"]},
                {"role": "user", "content": f"{message}{context_str}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            "success": True,
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "response": response.choices[0].message.content,
            "context_used": context is not None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id
        }

def suggest_best_agent(message: str) -> str:
    """Sugere melhor agente baseado na mensagem."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["preço", "custo", "orçamento", "investimento"]):
        return "lead-qualifier"
    elif any(word in message_lower for word in ["demo", "reunião", "agendar", "apresentação"]):
        return "sales-sdr"
    elif any(word in message_lower for word in ["problema", "bug", "erro", "suporte"]):
        return "customer-success"
    else:
        return "lead-qualifier"  # default

# Endpoints da API
@app.get("/")
async def root():
    return {
        "message": "MrDom SDR Demo - Funcionando sem AgentOS",
        "status": "healthy",
        "agents": list(AGENTS.keys())
    }

@app.get("/api/v1/agents/status")
async def get_agents_status():
    return {
        "agent_os_available": False,  # Simulando sem AgentOS
        "available_agents": list(AGENTS.keys()),
        "total_agents": len(AGENTS),
        "demo_mode": True
    }

@app.get("/api/v1/agents/list")
async def list_agents():
    return {
        "agents": [
            {
                "id": agent_id,
                "name": agent["name"],
                "description": f"Agente especializado em {agent_id.replace('-', ' ')}"
            }
            for agent_id, agent in AGENTS.items()
        ]
    }

@app.post("/api/v1/agents/process")
async def process_with_specific_agent(request: dict):
    agent_id = request.get("agent_id", "lead-qualifier")
    message = request.get("message", "")
    context = request.get("context", None)
    
    if not message:
        return {"error": "Campo 'message' é obrigatório"}
    
    result = await process_with_agent(agent_id, message, context)
    return result

@app.post("/api/v1/agents/process-best")
async def process_with_best_agent(request: dict):
    message = request.get("message", "")
    context = request.get("context", None)
    
    if not message:
        return {"error": "Campo 'message' é obrigatório"}
    
    # Sugere melhor agente
    best_agent = suggest_best_agent(message)
    
    # Processa com melhor agente
    result = await process_with_agent(best_agent, message, context)
    
    return {
        "success": result["success"],
        "selected_agent": best_agent,
        "all_suggested_agents": [best_agent],
        "result": result
    }

@app.post("/api/v1/agents/suggest")
async def suggest_agent(request: dict):
    message = request.get("message", "")
    
    if not message:
        return {"error": "Campo 'message' é obrigatório"}
    
    suggested = suggest_best_agent(message)
    
    return {
        "message": message,
        "suggested_agents": [suggested],
        "available_agents": list(AGENTS.keys())
    }

async def test_agents():
    """Testa os agentes com mensagens de exemplo."""
    print("🧪 Testando agentes...")
    
    test_cases = [
        ("lead-qualifier", "Qual o preço do seu serviço?", {"lead_exists": False}),
        ("sales-sdr", "Quero agendar uma demo", {"lead_exists": True}),
        ("customer-success", "Estou com problema na integração", {"urgent": True})
    ]
    
    for agent_id, message, context in test_cases:
        print(f"\n📝 Testando {agent_id}: '{message}'")
        result = await process_with_agent(agent_id, message, context)
        
        if result["success"]:
            print(f"✅ Resposta: {result['response'][:100]}...")
        else:
            print(f"❌ Erro: {result['error']}")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando MrDom SDR Demo...")
    print("=" * 40)
    
    # Verifica API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-"):
        print("⚠️ OPENAI_API_KEY não configurada")
        print("Configure no arquivo .env:")
        print("OPENAI_API_KEY=sk-sua_chave_aqui")
        print("\nExecutando em modo demo (sem OpenAI)...")
    else:
        print("✅ OPENAI_API_KEY configurada")
    
    print(f"\n🌐 Servidor rodando em: http://localhost:8000")
    print(f"📚 Documentação: http://localhost:8000/docs")
    print(f"🤖 Status agentes: http://localhost:8000/api/v1/agents/status")
    
    # Executa testes se API key estiver configurada
    if api_key and not api_key.startswith("sk-"):
        asyncio.run(test_agents())
    
    # Inicia servidor
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
