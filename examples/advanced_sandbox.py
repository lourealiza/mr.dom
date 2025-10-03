#!/usr/bin/env python3
"""
Sandbox Avançado - Conecta com API AgentOS real quando disponível.
"""

import os
import asyncio
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Adiciona path da API
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

class AdvancedSandbox:
    """Sandbox que se conecta com API AgentOS real."""
    
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.conversation_history = []
        self.mock_context = {
            "conversation_id": "sandbox_123",
            "account_id": "1",
            "lead_exists": False,
            "phone": "+5511998765432",
            "nome": "João Silva",
            "email": "joao@empresa.com",
            "empresa": "Empresa ABC",
            "origem": "MrDOM Sandbox"
        }
        
        # Verifica se API está disponível
        self.api_available = self.check_api_availability()
        
        if self.api_available:
            print("✅ Conectado à API AgentOS")
        else:
            print("⚠️ API não disponível - usando simulação")
    
    def check_api_availability(self) -> bool:
        """Verifica se a API AgentOS está disponível."""
        try:
            response = requests.get(f"{self.api_url}/api/v1/agents/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def get_agent_suggestion(self, message: str) -> str:
        """Obtém sugestão de agente da API."""
        if not self.api_available:
            return self.suggest_agent_local(message)
        
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/agents/suggest",
                json={"message": message},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("suggested_agents", ["lead-qualifier"])[0]
            else:
                return self.suggest_agent_local(message)
                
        except:
            return self.suggest_agent_local(message)
    
    def suggest_agent_local(self, message: str) -> str:
        """Sugestão local de agente."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["preço", "custo", "orçamento"]):
            return "lead-qualifier"
        elif any(word in message_lower for word in ["demo", "reunião", "agendar"]):
            return "sales-sdr"
        elif any(word in message_lower for word in ["problema", "bug", "suporte"]):
            return "customer-success"
        else:
            return "lead-qualifier"
    
    async def process_with_api(self, message: str, agent_id: str = None) -> Dict[str, Any]:
        """Processa mensagem usando API AgentOS."""
        try:
            if agent_id:
                # Usa agente específico
                response = requests.post(
                    f"{self.api_url}/api/v1/agents/process",
                    json={
                        "agent_id": agent_id,
                        "message": message,
                        "context": self.mock_context
                    },
                    timeout=30
                )
            else:
                # Usa melhor agente automaticamente
                response = requests.post(
                    f"{self.api_url}/api/v1/agents/process-best",
                    json={
                        "message": message,
                        "context": self.mock_context
                    },
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "agent_id": data.get("selected_agent", agent_id),
                    "response": data.get("result", {}).get("response", ""),
                    "api_used": True
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "api_used": True
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "api_used": True
            }
    
    async def process_with_simulation(self, message: str, agent_id: str = None) -> Dict[str, Any]:
        """Processa mensagem usando simulação local."""
        if not agent_id:
            agent_id = await self.get_agent_suggestion(message)
        
        # Simula resposta baseada no agente
        if agent_id == "lead-qualifier":
            if "preço" in message.lower():
                response = "Entendo que você quer saber sobre investimento. Para te dar uma proposta adequada, preciso entender melhor: qual o tamanho da sua empresa e quantas pessoas trabalham no time de vendas?"
            else:
                response = "Olá! Sou especialista em qualificação de leads. Para te ajudar melhor, me conte: qual é o principal desafio que vocês enfrentam nas vendas hoje?"
        
        elif agent_id == "sales-sdr":
            if "demo" in message.lower():
                response = "Perfeito! Tenho 2 horários disponíveis esta semana: terça às 14h ou quinta às 10h. Qual funciona melhor para você?"
            else:
                response = "Entendo seu interesse! Uma demo de 30 minutos seria ideal para mostrar como podemos resolver seus desafios. Você tem disponibilidade esta semana?"
        
        elif agent_id == "customer-success":
            response = "Entendo que você está enfrentando dificuldades. Vou te ajudar a resolver isso rapidamente. Pode me dar mais detalhes sobre o que está acontecendo?"
        
        else:
            response = "Obrigado pela sua mensagem! Como posso te ajudar?"
        
        return {
            "success": True,
            "agent_id": agent_id,
            "response": response,
            "api_used": False
        }
    
    async def process_message(self, message: str, agent_id: str = None) -> Dict[str, Any]:
        """Processa mensagem (API ou simulação)."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Tenta usar API primeiro
        if self.api_available:
            result = await self.process_with_api(message, agent_id)
        else:
            result = await self.process_with_simulation(message, agent_id)
        
        # Adiciona timestamp
        result["timestamp"] = timestamp
        result["user_message"] = message
        
        # Salva no histórico
        self.conversation_history.append(result)
        
        return result
    
    def print_status(self):
        """Mostra status da conexão."""
        print(f"\n📊 STATUS DO SANDBOX:")
        print(f"   API AgentOS: {'✅ Conectada' if self.api_available else '❌ Indisponível'}")
        print(f"   URL: {self.api_url}")
        print(f"   Modo: {'API Real' if self.api_available else 'Simulação'}")
        print(f"   Mensagens: {len(self.conversation_history)}")
    
    def export_conversation(self, filename: str = None):
        """Exporta conversa para arquivo JSON."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_export_{timestamp}.json"
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "api_used": self.api_available,
            "conversation": self.conversation_history,
            "context": self.mock_context
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Conversa exportada para: {filename}")
    
    async def run(self):
        """Executa o sandbox avançado."""
        print("🤖 SANDBOX AVANÇADO - MrDom SDR AgentOS")
        print("=" * 50)
        
        self.print_status()
        
        print("\n💡 Comandos disponíveis:")
        print("   /status - Mostra status da conexão")
        print("   /export - Exporta conversa para JSON")
        print("   /history - Mostra histórico")
        print("   /clear - Limpa histórico")
        print("   /quit - Sair")
        print("\n💬 Digite sua mensagem:")
        
        while True:
            try:
                user_input = input("\n👤 Você: ").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiais
                if user_input == "/status":
                    self.print_status()
                    continue
                elif user_input == "/export":
                    self.export_conversation()
                    continue
                elif user_input == "/history":
                    print(f"\n📜 Histórico ({len(self.conversation_history)} mensagens):")
                    for i, entry in enumerate(self.conversation_history, 1):
                        print(f"   {i}. [{entry['timestamp']}] {entry['user_message'][:50]}...")
                    continue
                elif user_input == "/clear":
                    self.conversation_history = []
                    print("✅ Histórico limpo!")
                    continue
                elif user_input == "/quit":
                    break
                
                # Processa mensagem
                print("🤖 Processando...")
                result = await self.process_message(user_input)
                
                if result["success"]:
                    mode = "API" if result.get("api_used") else "Simulação"
                    agent = result.get("agent_id", "unknown")
                    response = result.get("response", "")
                    
                    print(f"\n🤖 [{mode}] {agent}: {response}")
                else:
                    print(f"❌ Erro: {result.get('error', 'Desconhecido')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Saindo do sandbox...")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
        
        # Resumo final
        print(f"\n📊 RESUMO DA SESSÃO:")
        print(f"   Mensagens: {len(self.conversation_history)}")
        print(f"   Modo: {'API Real' if self.api_available else 'Simulação'}")
        
        if self.conversation_history:
            agents_used = set(entry.get('agent_id', 'unknown') for entry in self.conversation_history)
            print(f"   Agentes usados: {', '.join(agents_used)}")

async def main():
    """Função principal."""
    print("🚀 Iniciando Sandbox Avançado...")
    
    sandbox = AdvancedSandbox()
    await sandbox.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sandbox interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
