#!/usr/bin/env python3
"""
Script de validação rápida para nova pessoa assumir operação AgentOS.
Execute este script para verificar se tudo está funcionando corretamente.
"""

import asyncio
import os
import sys
import requests
import json
from pathlib import Path

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status="info"):
    """Imprime status com cores."""
    emoji = {"ok": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}
    colors = {"ok": Colors.GREEN, "error": Colors.RED, "warning": Colors.YELLOW, "info": Colors.BLUE}
    
    print(f"{colors[status]}{emoji[status]} {message}{Colors.END}")

async def check_environment():
    """Verifica configuração do ambiente."""
    print_status("Verificando configuração do ambiente...", "info")
    
    # Verifica arquivo .env
    env_file = Path(".env")
    if not env_file.exists():
        print_status("Arquivo .env não encontrado - usando env.example", "warning")
        env_example = Path("env.example")
        if env_example.exists():
            print_status("Copie env.example para .env e configure OPENAI_API_KEY", "warning")
        else:
            print_status("Arquivo env.example não encontrado", "error")
            return False
    
    # Verifica OPENAI_API_KEY
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-"):
        print_status("OPENAI_API_KEY configurada", "ok")
    else:
        print_status("OPENAI_API_KEY não configurada ou inválida", "error")
        print_status("Configure uma chave válida da OpenAI", "warning")
        return False
    
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print_status("Verificando dependências...", "info")
    
    required_packages = ["fastapi", "agno", "openai"]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_status(f"{package} instalado", "ok")
        except ImportError:
            missing.append(package)
            print_status(f"{package} não instalado", "error")
    
    if missing:
        print_status(f"Instale as dependências: pip install {' '.join(missing)}", "warning")
        return False
    
    return True

async def check_agentos_service():
    """Verifica se o serviço AgentOS está funcionando."""
    print_status("Verificando serviço AgentOS...", "info")
    
    try:
        # Adiciona path da API
        api_path = Path(__file__).parent.parent / "api"
        sys.path.insert(0, str(api_path))
        
        # Import service
        try:
            from services.agent_os_integration import agent_integration
        except ImportError as e:
            print_status(f"Erro ao importar agent_os_integration: {e}", "error")
            return False
        
        # Verifica se está disponível
        if agent_integration.is_agent_os_available():
            print_status("AgentOS está disponível", "ok")
            
            # Lista agentes
            agentes = agent_integration.get_available_agents()
            print_status(f"Agentes disponíveis: {', '.join(agentes)}", "ok")
            
            return True
        else:
            print_status("AgentOS não está disponível", "error")
            print_status("Verifique OPENAI_API_KEY e configurações", "warning")
            return False
            
    except Exception as e:
        print_status(f"Erro ao verificar AgentOS: {str(e)}", "error")
        return False

def check_api_endpoints():
    """Verifica se a API está respondendo."""
    print_status("Verificando endpoints da API...", "info")
    
    base_url = "http://localhost:8000"
    
    try:
        # Testa endpoint principal
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print_status("API principal respondendo", "ok")
        else:
            print_status(f"API principal retornou {response.status_code}", "warning")
    except requests.exceptions.RequestException:
        print_status("API não está rodando em localhost:8000", "warning")
        print_status("Execute: python examples/agentos_integration_example.py", "info")
        return False
    
    # Testa endpoints específicos de agentes se disponível
    try:
        response = requests.get(f"{base_url}/api/v1/agents/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print_status(f"Status agentes: {status.get('agent_os_available', False)}", "ok")
        else:
            print_status("Endpoints de agentes não disponíveis", "warning")
    except requests.examples.RequestException:
        print_status("Endpoints de agentes não respondendo", "warning")
    
    return True

async def test_agent_processing():
    """Testa processamento com agentes."""
    print_status("Testando processamento com agentes...", "info")
    
    try:
        api_path = Path(__file__).parent.parent / "api"
        sys.path.insert(0, str(api_path))
        
        from services.agent_os_integration import agent_integration
        
        if not agent_integration.is_agent_os_available():
            print_status("AgentOS não disponível para teste", "warning")
            return False
        
        # Testa sugestão de agente
        agentes_sugeridos = await agent_integration.get_best_agent_suggestions("Qual o preço?")
        print_status(f"Agente sugerido para 'Qual o preço?': {agentes_sugeridos[0] if agentes_sugeridos else 'N/A'}", "ok")
        
        return True
        
    except Exception as e:
        print_status(f"Erro no teste de processamento: {str(e)}", "error")
        return False

def print_next_steps():
    """Imprime próximos passos."""
    print_status("Próximos passos para operacional:", "info")
    print()
    print(f"{Colors.BOLD}1. Configuração Inicial:{Colors.END}")
    print("   - Copie env.example para .env")
    print("   - Configure OPENAI_API_KEY válida")
    print("   - Execute: pip install agno")
    print()
    print(f"{Colors.BOLD}2. Execução:{Colors.END}")
    print("   - python examples/agentos_integration_example.py")
    print("   - Ou configure no main.py e execute: uvicorn api.main:app --reload")
    print()
    print(f"{Colors.BOLD}7. Testes:{Colors.END}")
    print("   - python scripts/test-agentos-integration.py")
    print("   - curl http://localhost:8000/api/v1/agents/status")
    print()
    print(f"{Colors.BOLD}4. Documentação:{Colors.END}")
    print("   - README-AGENTOS.md")
    print("   - docs/operational-handover-guide.md")
    print("   - docs/agentos-integration.md")

async def main():
    """Função principal."""
    print(f"{Colors.BOLD}{Colors.BLUE}🤖 VALIDAÇÃO RÁPIDA AGENTOS - MrDom SDR{Colors.END}")
    print("=" * 50)
    print()
    
    # Executa verificações
    checks = [
        ("Ambiente", check_environment()),
        ("Dependências", check_dependencies()),
        ("AgentOS Service", await check_agentos_service()),
        ("API Endpoints", check_api_endpoints()),
        ("Processamento", await test_agent_processing())
    ]
    
    print(f"\n{Colors.BOLD}RESULTADO DAS VERIFICAĐÕES:{Colors.END}")
    print("-" * 30)
    
    total_pass = 0
    for nome, resultado in checks:
        if resultado:
            print_status(nome, "ok")
            total_pass += 1
        else:
            print_status(nome, "error")
    
    print(f"\n{Colors.BOLD}TOTAL: {total_pass}/5 verificações passaram{Colors.END}")
    
    if total_pass >= 4:
        print_status("🎉 Sistema pronto para operação!", "ok")
    else:
        print_status("⚠️ Algumas configurações precisam ser ajustadas", "warning")
    
    print_next_steps()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_status("\nValidação interrompida pelo usuário", "warning")
    except Exception as e:
        print_status(f"Erro inesperado: {str(e)}", "error")
