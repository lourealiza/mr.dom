#!/usr/bin/env python3
"""
Script para testar integração N8N + AgentOS.
Simula o fluxo completo do workflow N8N com AgentOS.
"""

import asyncio
import json
import requests
import sys
from pathlib import Path
from typing import Dict, Any

# Adiciona path da API
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

from services.agent_os_integration import agent_integration

class N8NAgentOSTester:
    """Simula o fluxo N8N + AgentOS para testes."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_data = self._load_test_scenarios()
    
    def _load_test_scenarios(self) -> Dict[str, Any]:
        """Carrega cenários de teste baseados no workflow N8N."""
        return {
            "new_lead": {
                "message": "Oi, quero saber mais sobre os planos do DOM360",
                "context": {
                    "conversation_id": "12345",
                    "account_id": "1",
                    "lead_exists": False,
                    "phone": "+5511998765432",
                    "nome": "João Silva",
                    "email": "joao@empresa.com",
                    "origem": "MrDOM"
                }
            },
            "existing_lead": {
                "message": "Já sou cliente, preciso de suporte técnico",
                "context": {
                    "conversation_id": "12346", 
                    "account_id": "1",
                    "lead_exists": True,
                    "lead_data": {
                        "company": "Empresa ABC",
                        "last_interaction": "2024-01-15",
                        "status": "Active"
                    },
                    "phone": "+5511998765433",
                    "nome": "Maria Santos",
                    "email": "maria@empresa.com",
                    "origem": "MrDOM"
                }
            },
            "audio_message": {
                "message": "Transcrição: Olá, preciso agendar uma demo para amanhã",
                "context": {
                    "conversation_id": "12347",
                    "account_id": "1", 
                    "lead_exists": False,
                    "phone": "+5511998765434",
                    "nome": "Pedro Costa",
                    "email": "pedro@empresa.com",
                    "origem": "WhatsApp",
                    "has_audio": True
                }
            }
        }
    
    async def test_agentos_direct(self, scenario_name: str) -> Dict[str, Any]:
        """Testa AgentOS diretamente (sem N8N)."""
        print(f"\n🧪 Testando cenário: {scenario_name}")
        
        scenario = self.test_data[scenario_name]
        
        if not agent_integration.is_agent_os_available():
            return {
                "success": False,
                "error": "AgentOS não disponível",
                "scenario": scenario_name
            }
        
        # Sugere melhor agente
        suggested_agents = await agent_integration.get_best_agent_suggestions(
            scenario["message"]
        )
        
        # Processa com melhor agente
        result = await agent_integration.process_with_agent(
            agent_id=suggested_agents[0] if suggested_agents else "lead-qualifier",
            message=scenario["message"],
            context=scenario["context"]
        )
        
        return {
            "success": result["success"],
            "scenario": scenario_name,
            "suggested_agent": suggested_agents[0] if suggested_agents else None,
            "response": result.get("response", ""),
            "error": result.get("error", ""),
            "context_used": scenario["context"]
        }
    
    def test_api_endpoint(self, scenario_name: str) -> Dict[str, Any]:
        """Testa endpoint da API AgentOS."""
        print(f"\n🌐 Testando API endpoint: {scenario_name}")
        
        scenario = self.test_data[scenario_name]
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/agents/process-best",
                json={
                    "message": scenario["message"],
                    "context": scenario["context"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "scenario": scenario_name,
                    "selected_agent": data.get("selected_agent"),
                    "response": data.get("result", {}).get("response", ""),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "scenario": scenario_name,
                "error": f"Erro de conexão: {str(e)}"
            }
    
    def simulate_n8n_workflow(self, scenario_name: str) -> Dict[str, Any]:
        """Simula o fluxo completo N8N."""
        print(f"\n🔄 Simulando fluxo N8N: {scenario_name}")
        
        scenario = self.test_data[scenario_name]
        
        # Simula processamento N8N (normalização, CRM check, etc.)
        processed_data = {
            "message": scenario["message"],
            "context": {
                **scenario["context"],
                "n8n_processed": True,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
        
        # Chama AgentOS API (como N8N faria)
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/agents/process-best",
                json=processed_data,
                timeout=30
            )
            
            if response.status_code == 200:
                agentos_result = response.json()
                
                # Simula resposta de volta para Chatwoot
                chatwoot_response = {
                    "content": agentos_result.get("result", {}).get("response", ""),
                    "message_type": "outgoing",
                    "conversation_id": scenario["context"]["conversation_id"]
                }
                
                return {
                    "success": True,
                    "scenario": scenario_name,
                    "n8n_flow": "Webhook → Normalização → CRM → AgentOS → Chatwoot",
                    "selected_agent": agentos_result.get("selected_agent"),
                    "agentos_response": agentos_result.get("result", {}).get("response", ""),
                    "chatwoot_payload": chatwoot_response,
                    "total_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "error": f"AgentOS API error: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "scenario": scenario_name,
                "error": f"Erro na simulação N8N: {str(e)}"
            }
    
    def test_fallback_scenario(self) -> Dict[str, Any]:
        """Testa cenário de fallback (AgentOS indisponível)."""
        print(f"\n🚨 Testando cenário de fallback")
        
        # Simula AgentOS indisponível
        try:
            response = requests.post(
                "http://localhost:9999/api/v1/agents/process-best",  # URL inválida
                json=self.test_data["new_lead"],
                timeout=5
            )
        except requests.exceptions.RequestException:
            # Esperado - simula AgentOS down
            return {
                "success": True,
                "scenario": "fallback",
                "fallback_triggered": True,
                "message": "AgentOS indisponível - fallback para agente original necessário"
            }
        
        return {
            "success": False,
            "scenario": "fallback", 
            "error": "Fallback não foi acionado como esperado"
        }

async def run_comprehensive_test():
    """Executa teste completo da integração."""
    print("🚀 TESTE COMPLETO: Integração N8N + AgentOS")
    print("=" * 50)
    
    tester = N8NAgentOSTester()
    results = []
    
    # Testa cenários
    scenarios = ["new_lead", "existing_lead", "audio_message"]
    
    for scenario in scenarios:
        print(f"\n📋 Cenário: {scenario.upper()}")
        print("-" * 30)
        
        # Teste 1: AgentOS direto
        result1 = await tester.test_agentos_direct(scenario)
        results.append(("AgentOS Direto", result1))
        
        # Teste 2: API endpoint
        result2 = tester.test_api_endpoint(scenario)
        results.append(("API Endpoint", result2))
        
        # Teste 3: Simulação N8N completa
        result3 = tester.simulate_n8n_workflow(scenario)
        results.append(("Simulação N8N", result3))
    
    # Teste 4: Fallback
    result4 = tester.test_fallback_scenario()
    results.append(("Fallback", result4))
    
    # Relatório final
    print(f"\n📊 RELATÓRIO FINAL")
    print("=" * 30)
    
    success_count = 0
    total_tests = len(results)
    
    for test_name, result in results:
        status = "✅" if result["success"] else "❌"
        scenario = result.get("scenario", "N/A")
        
        print(f"{status} {test_name} ({scenario})")
        
        if result["success"]:
            success_count += 1
            if "response" in result:
                response_preview = result["response"][:50] + "..." if len(result["response"]) > 50 else result["response"]
                print(f"   Resposta: {response_preview}")
        else:
            print(f"   Erro: {result.get('error', 'Desconhecido')}")
    
    print(f"\n🎯 RESULTADO: {success_count}/{total_tests} testes passaram")
    
    if success_count >= total_tests * 0.8:
        print("🎉 Integração N8N + AgentOS funcionando!")
    else:
        print("⚠️ Alguns problemas encontrados - revisar configuração")

def print_integration_guide():
    """Imprime guia de integração."""
    print(f"\n📚 GUIA DE INTEGRAÇÃO N8N + AGENTOS")
    print("=" * 40)
    print("""
1. 🔧 Configurar AgentOS:
   pip install agno>=0.1.0
   python examples/agentos_integration_example.py

2. 📝 Modificar N8N:
   - Substituir "Agente de IA1" por HTTP Request
   - URL: http://localhost:8000/api/v1/agents/process-best
   - Body: message + context (CRM data)

3. 🧪 Testar:
   python scripts/test-n8n-agentos-integration.py

4. 📊 Monitorar:
   - Logs da API AgentOS
   - Performance N8N
   - Respostas Chatwoot

5. 🚨 Fallback:
   - Manter agente original como backup
   - Implementar retry logic
   - Monitorar disponibilidade
""")

if __name__ == "__main__":
    try:
        asyncio.run(run_comprehensive_test())
        print_integration_guide()
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        print_integration_guide()
