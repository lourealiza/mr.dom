#!/usr/bin/env python3
"""
Teste simples para verificar se as dependências estão funcionando.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Testa se as dependências podem ser importadas."""
    print("🧪 Testando importações...")
    
    try:
        import fastapi
        print("✅ FastAPI importado")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI importado")
    except ImportError as e:
        print(f"❌ OpenAI: {e}")
        return False
    
    try:
        import agno
        print("✅ Agno importado")
    except ImportError as e:
        print(f"❌ Agno: {e}")
        return False
    
    return True

def test_agentos_basic():
    """Testa funcionalidade básica do AgentOS."""
    print("\n🤖 Testando AgentOS básico...")
    
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        from agno.os import AgentOS
        
        print("✅ Classes AgentOS importadas")
        
        # Verifica se tem API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("sk-"):
            print("⚠️ OPENAI_API_KEY não configurada")
            print("   Configure no arquivo .env:")
            print("   OPENAI_API_KEY=sk-sua_chave_aqui")
            return False
        
        print("✅ OPENAI_API_KEY configurada")
        
        # Tenta criar um agente simples
        try:
            agent = Agent(
                id="test-agent",
                model=OpenAIChat(id="gpt-3.5-turbo")
            )
            print("✅ Agente criado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar agente: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar AgentOS: {e}")
        return False

def test_api_structure():
    """Testa se a estrutura da API está correta."""
    print("\n🌐 Testando estrutura da API...")
    
    api_path = Path("api")
    if not api_path.exists():
        print("❌ Diretório api/ não encontrado")
        return False
    
    required_files = [
        "api/main.py",
        "api/services/agent_os_integration.py",
        "api/routers/agents.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} não encontrado")
            return False
    
    return True

def main():
    """Função principal."""
    print("🚀 TESTE SIMPLES - MrDom SDR + AgentOS")
    print("=" * 40)
    
    # Teste 1: Importações
    imports_ok = test_imports()
    
    # Teste 2: AgentOS básico
    agentos_ok = test_agentos_basic() if imports_ok else False
    
    # Teste 3: Estrutura da API
    api_ok = test_api_structure()
    
    # Resultado final
    print(f"\n📊 RESULTADO:")
    print(f"Importações: {'✅' if imports_ok else '❌'}")
    print(f"AgentOS: {'✅' if agentos_ok else '❌'}")
    print(f"Estrutura API: {'✅' if api_ok else '❌'}")
    
    if imports_ok and agentos_ok and api_ok:
        print("\n🎉 TUDO FUNCIONANDO!")
        print("\nPróximos passos:")
        print("1. Configure OPENAI_API_KEY no .env")
        print("2. Execute: python examples/agentos_integration_example.py")
        print("3. Teste: curl http://localhost:8000/api/v1/agents/status")
    else:
        print("\n⚠️ Alguns problemas encontrados")
        print("\nPara resolver:")
        print("1. Instalar dependências: pip install -r requirements.txt")
        print("2. Configurar OPENAI_API_KEY no .env")
        print("3. Verificar versões das bibliotecas")

if __name__ == "__main__":
    main()
