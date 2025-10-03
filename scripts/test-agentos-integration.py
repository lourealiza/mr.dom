#!/usr/bin/env python3
"""
Script para testar a integração do AgentOS com o projeto MrDom SDR.
"""

import asyncio
import os
import sys
from pathlib import Path

# Adiciona o path da API
project_root = Path(__file__).parent.parent
api_path = project_root / "api"
sys.path.insert(0, str(api_path))

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from services.agent_os_integration import agent_integration


async def test_agentos_integration():
    """Testa a integração básica do AgentOS."""
    
    print("🤖 Testando Integração AgentOS - MrDom SDR")
    print("=" * 50)
    
    # Verifica se AgentOS está disponível
    if not agent_integration.is_agent_os_available():
        print("❌ AgentOS não está disponível")
        print("   Certifique-se de que OPENAI_API_KEY está configurada no .env")
        return
    
    print("✅ AgentOS está disponível!")
    
    # Lista agentes disponíveis
    agentes = agent_integration.get_available_agents()
    print(f"\n📋 Agentes disponíveis: {agentes}")
    
    # Testa com diferentes tipos de mensagens
    casos_teste = [
        {
            "mensagem": "Qual o preço do seu serviço?",
            "context_type": "lead_qualification"
        },
        {
            "mensagem": "Quero agendar uma demo para amanhã", 
            "context_type": "sales_demo"
        },
        {
            "mensagem": "Estou com problema na integração",
            "context_type": "customer_support"
        }
    ]
    
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n🧪 Teste {i}: {caso['mensagem']}")
        
        # Sugere melhor agente
        agentes_sugeridos = await agent_integration.get_best_agent_suggestions(caso['mensagem'])
        print(f"   Agente sugerido: {agentes_sugeridos[0] if agentes_sugeridos else 'N/A'}")
        
        # Processa com o primeiro agente sugerido (se disponível)
        if agentes_sugeridos:
            agent_escolhido = agentes_sugeridos[0]
            
            resultado = await agent_integration.process_with_agent(
                agent_id=agent_escolhido,
                message=caso['mensagem'],
                context={"type": caso['context_type']}
            )
            
            if resultado["success"]:
                print(f"   ✅ Resposta ({agent_escolhido}): {resultado['response'][:100]}...")
            else:
                print(f"   ❌ Erro: {resultado['error']}")
        else:
            print("   ⚠️ Nenhum agente sugerido")


async def test_full_endpoint_simulation():
    """Simula chamadas para endpoints da API."""
    
    print("\n🌐 Simulando Endpoints da API")
    print("=" * 30)
    
    # Simula GET /api/v1/agents/status
    print("\n📊 Status dos Agentes:")
    print(f"   Disponível: {agent_integration.is_agent_os_available()}")
    print(f"   Total: {len(agent_integration.get_available_agents())}")
    
    # Simula POST para processamento com melhor agente
    mensagem_teste = "Preciso de ajuda para implementar automação de vendas"
    
    print(f"\n🎯 Processando: '{mensagem_teste}'")
    
    # Encontra melhor agente
    agentes_sugeridos = await agent_integration.get_best_agent_suggestions(mensagem_teste)
    
    if agentes_sugeridos:
        melhor_agente = agentes_sugeridos[0]
        print(f"   Melhor agente: {melhor_agente}")
        
        resultado = await agent_integration.process_with_agent(
            agent_id=melhor_agente,
            message=mensagem_teste
        )
        
        if resultado["success"]:
            print(f"   Resposta: {resultado['response']}")
        else:
            print(f"   Erro: {resultado['error']}")


async def main():
    """Função principal."""
    
    print("🚀 Iniciando testes da integração AgentOS")
    
    await test_agentos_integration()
    await test_full_endpoint_simulation()
    
    print("\n✨ Testes concluídos!")
    print("\nPróximos passos:")
    print("1. Configure OPENAI_API_KEY no arquivo .env")
    print("2. Execute: python -m uvicorn api.main:app --reload")
    print("3. Teste os endpoints: /api/v1/agents/*")


if __name__ == "__main__":
    asyncio.run(main())
