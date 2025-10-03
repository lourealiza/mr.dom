#!/usr/bin/env python3
"""
Sandbox de Conversa - MrDom SDR AgentOS + Bedrock
Interface interativa para testar agentes antes de integrar com N8N.
"""

import os
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
import sys
from pathlib import Path

# Adiciona path da API
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

class ConversationSandbox:
    """Sandbox interativo para testar conversas com agentes."""
    
    def __init__(self):
        self.conversation_history = []
        self.agents = {
            "lead-qualifier": {
                "name": "Lead Qualifier",
                "description": "Especialista em qualificação BANT",
                "system_prompt": """Você é um especialista em qualificação de leads BANT 
                (Budget, Authority, Need, Timeline). Sua função é fazer perguntas inteligentes 
                para determinar se um lead é qualificado para uma proposta comercial.
                
                Pergunte sobre:
                - Budget: Qual o investimento disponível?
                - Authority: Você tem poder de decisão?
                - Need: Qual o problema principal?
                - Timeline: Quando precisa resolver?"""
            },
            "sales-sdr": {
                "name": "Sales SDR",
                "description": "Especialista em agendamento de demos",
                "system_prompt": """Você é um SDR experiente focado em gerar interesse 
                e agendar reuniões de vendas. Use técnicas de vendas consultivas para 
                identificar necessidades e criar urgência.
                
                Foque em:
                - Identificar necessidades específicas
                - Criar urgência para agendamento
                - Oferecer valor na demo
                - Confirmar dados para contato"""
            },
            "customer-success": {
                "name": "Customer Success",
                "description": "Especialista em suporte e sucesso",
                "system_prompt": """Você é especialista em sucesso do cliente, focado em 
                resolver problemas, aumentar satisfação e identificar oportunidades de 
                upselling.
                
                Priorize:
                - Resolver problemas rapidamente
                - Explicar soluções claramente
                - Identificar oportunidades de melhoria
                - Escalar quando necessário"""
            }
        }
        
        # Simula dados de contexto do CRM
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
    
    def print_header(self):
        """Imprime cabeçalho do sandbox."""
        print("🤖 SANDBOX DE CONVERSA - MrDom SDR AgentOS + Bedrock")
        print("=" * 60)
        print("📋 Agentes disponíveis:")
        for agent_id, agent in self.agents.items():
            print(f"   {agent_id}: {agent['name']} - {agent['description']}")
        print("\n💡 Comandos especiais:")
        print("   /help - Mostra ajuda")
        print("   /agents - Lista agentes")
        print("   /context - Mostra contexto atual")
        print("   /history - Mostra histórico")
        print("   /clear - Limpa histórico")
        print("   /switch <agent> - Troca agente")
        print("   /quit - Sair")
        print("=" * 60)
    
    def print_context(self):
        """Mostra contexto atual."""
        print("\n📊 CONTEXTO ATUAL:")
        print("-" * 30)
        for key, value in self.mock_context.items():
            print(f"   {key}: {value}")
    
    def print_history(self):
        """Mostra histórico da conversa."""
        print("\n📜 HISTÓRICO DA CONVERSA:")
        print("-" * 40)
        
        if not self.conversation_history:
            print("   Nenhuma mensagem ainda.")
            return
        
        for i, entry in enumerate(self.conversation_history, 1):
            timestamp = entry.get('timestamp', 'N/A')
            agent = entry.get('agent', 'N/A')
            user_msg = entry.get('user_message', '')
            agent_response = entry.get('agent_response', '')
            
            print(f"\n   {i}. [{timestamp}] Agente: {agent}")
            print(f"      👤 Usuário: {user_msg}")
            print(f"      🤖 Agente: {agent_response[:100]}{'...' if len(agent_response) > 100 else ''}")
    
    def clear_history(self):
        """Limpa histórico da conversa."""
        self.conversation_history = []
        print("✅ Histórico limpo!")
    
    def switch_agent(self, agent_id: str):
        """Troca agente atual."""
        if agent_id in self.agents:
            self.current_agent = agent_id
            print(f"✅ Agente trocado para: {self.agents[agent_id]['name']}")
        else:
            print(f"❌ Agente '{agent_id}' não encontrado.")
            print("Agentes disponíveis:", list(self.agents.keys()))
    
    def suggest_agent(self, message: str) -> str:
        """Sugere melhor agente baseado na mensagem."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["preço", "custo", "orçamento", "investimento", "quanto"]):
            return "lead-qualifier"
        elif any(word in message_lower for word in ["demo", "reunião", "agendar", "apresentação", "meeting"]):
            return "sales-sdr"
        elif any(word in message_lower for word in ["problema", "bug", "erro", "suporte", "ajuda", "não funciona"]):
            return "customer-success"
        else:
            return "lead-qualifier"  # default
    
    async def simulate_agent_response(self, agent_id: str, message: str, context: Dict) -> str:
        """Simula resposta do agente (sem AgentOS real)."""
        agent = self.agents[agent_id]
        
        # Simula diferentes tipos de resposta baseado no agente
        if agent_id == "lead-qualifier":
            if "preço" in message.lower():
                return "Entendo que você quer saber sobre investimento. Para te dar uma proposta adequada, preciso entender melhor: qual o tamanho da sua empresa e quantas pessoas trabalham no time de vendas?"
            elif "empresa" in message.lower():
                return "Ótimo! E quantas pessoas trabalham no seu time de vendas hoje? Isso me ajuda a entender melhor o cenário."
            else:
                return "Olá! Sou especialista em qualificação de leads. Para te ajudar melhor, me conte: qual é o principal desafio que vocês enfrentam nas vendas hoje?"
        
        elif agent_id == "sales-sdr":
            if "demo" in message.lower() or "reunião" in message.lower():
                return "Perfeito! Tenho 2 horários disponíveis esta semana: terça às 14h ou quinta às 10h. Qual funciona melhor para você? Vou precisar do seu email para enviar o link da reunião."
            else:
                return "Entendo seu interesse! Uma demo de 30 minutos seria ideal para mostrar como podemos resolver seus desafios. Você tem disponibilidade esta semana?"
        
        elif agent_id == "customer-success":
            if "problema" in message.lower():
                return "Entendo que você está enfrentando dificuldades. Vou te ajudar a resolver isso rapidamente. Pode me dar mais detalhes sobre o que está acontecendo?"
            else:
                return "Olá! Estou aqui para te ajudar com qualquer questão. Como posso te auxiliar hoje?"
        
        return "Obrigado pela sua mensagem! Como posso te ajudar?"
    
    async def process_message(self, message: str, agent_id: str = None) -> Dict[str, Any]:
        """Processa mensagem com agente específico."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Escolhe agente se não especificado
        if not agent_id:
            agent_id = self.suggest_agent(message)
        
        # Simula resposta do agente
        agent_response = await self.simulate_agent_response(agent_id, message, self.mock_context)
        
        # Salva no histórico
        entry = {
            "timestamp": timestamp,
            "agent": self.agents[agent_id]["name"],
            "agent_id": agent_id,
            "user_message": message,
            "agent_response": agent_response,
            "context": self.mock_context.copy()
        }
        
        self.conversation_history.append(entry)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "agent_name": self.agents[agent_id]["name"],
            "response": agent_response,
            "timestamp": timestamp
        }
    
    def handle_command(self, command: str) -> bool:
        """Processa comandos especiais. Retorna True se deve continuar."""
        cmd = command.strip().lower()
        
        if cmd == "/help":
            self.print_header()
        elif cmd == "/agents":
            print("\n🤖 AGENTES DISPONÍVEIS:")
            for agent_id, agent in self.agents.items():
                print(f"   {agent_id}: {agent['name']}")
                print(f"      {agent['description']}")
        elif cmd == "/context":
            self.print_context()
        elif cmd == "/history":
            self.print_history()
        elif cmd == "/clear":
            self.clear_history()
        elif cmd.startswith("/switch "):
            agent_id = cmd.split(" ", 1)[1]
            self.switch_agent(agent_id)
        elif cmd == "/quit":
            print("👋 Saindo do sandbox...")
            return False
        else:
            print(f"❌ Comando desconhecido: {command}")
            print("Use /help para ver comandos disponíveis.")
        
        return True
    
    async def run(self):
        """Executa o sandbox interativo."""
        self.print_header()
        
        # Agente inicial
        self.current_agent = "lead-qualifier"
        print(f"\n🎯 Agente inicial: {self.agents[self.current_agent]['name']}")
        print("💬 Digite sua mensagem ou comando:")
        
        while True:
            try:
                # Lê entrada do usuário
                user_input = input("\n👤 Você: ").strip()
                
                if not user_input:
                    continue
                
                # Verifica se é comando
                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue
                
                # Processa mensagem
                print("🤖 Processando...")
                result = await self.process_message(user_input, self.current_agent)
                
                if result["success"]:
                    print(f"\n🤖 {result['agent_name']}: {result['response']}")
                    
                    # Sugere próximo agente se necessário
                    suggested = self.suggest_agent(user_input)
                    if suggested != self.current_agent:
                        print(f"\n💡 Sugestão: Use '/switch {suggested}' para trocar para {self.agents[suggested]['name']}")
                else:
                    print(f"❌ Erro: {result.get('error', 'Desconhecido')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Saindo do sandbox...")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
        
        # Mostra resumo final
        print(f"\n📊 RESUMO DA SESSÃO:")
        print(f"   Mensagens trocadas: {len(self.conversation_history)}")
        print(f"   Agentes usados: {set(entry['agent_id'] for entry in self.conversation_history)}")

def check_environment():
    """Verifica configuração do ambiente."""
    print("🔧 Verificando configuração...")
    
    # Verifica AWS credentials
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if aws_key and aws_secret:
        print("✅ AWS Bedrock configurado")
    else:
        print("⚠️ AWS credentials não configuradas")
        print("   Executando em modo simulação")
    
    # Verifica AgentOS
    try:
        import agno
        print("✅ AgentOS disponível")
    except ImportError:
        print("⚠️ AgentOS não disponível - usando simulação")
    
    return True

async def main():
    """Função principal."""
    print("🚀 Iniciando Sandbox de Conversa...")
    
    # Verifica ambiente
    check_environment()
    
    # Cria e executa sandbox
    sandbox = ConversationSandbox()
    await sandbox.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sandbox interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
