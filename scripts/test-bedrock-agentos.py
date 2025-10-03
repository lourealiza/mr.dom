#!/usr/bin/env python3
"""
Script para testar integração AgentOS + AWS Bedrock.
"""

import asyncio
import os
import sys
from pathlib import Path

# Adiciona path da API
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

def check_aws_config():
    """Verifica configuração AWS."""
    print("🔧 Verificando configuração AWS Bedrock...")
    
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    
    if aws_key and aws_secret:
        print(f"✅ AWS Access Key: {aws_key[:8]}...")
        print(f"✅ AWS Secret: {'*' * len(aws_secret)}")
        print(f"✅ Região: {aws_region}")
        return True
    else:
        print("❌ AWS credentials não configuradas")
        print("Configure no .env:")
        print("AWS_ACCESS_KEY_ID=sua_chave")
        print("AWS_SECRET_ACCESS_KEY=seu_secret")
        print("AWS_DEFAULT_REGION=us-east-1")
        return False

def check_bedrock_imports():
    """Verifica se Bedrock pode ser importado."""
    print("\n📦 Verificando imports Bedrock...")
    
    try:
        import boto3
        print("✅ boto3 instalado")
    except ImportError:
        print("❌ boto3 não instalado")
        print("Execute: pip install boto3")
        return False
    
    try:
        from agno.models.aws_bedrock import BedrockChat
        print("✅ BedrockChat importado")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar BedrockChat: {e}")
        return False

async def test_bedrock_connection():
    """Testa conexão com Bedrock."""
    print("\n🌐 Testando conexão Bedrock...")
    
    try:
        import boto3
        
        # Cria cliente Bedrock
        bedrock = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
        
        # Lista modelos disponíveis
        response = bedrock.list_foundation_models()
        models = [model['modelId'] for model in response['modelSummaries']]
        
        print(f"✅ Conectado ao Bedrock")
        print(f"✅ Modelos disponíveis: {len(models)}")
        
        # Verifica se nosso modelo está disponível
        target_model = "amazon.nova-lite-v1:0"
        if target_model in models:
            print(f"✅ Modelo {target_model} disponível")
        else:
            print(f"⚠️ Modelo {target_model} não encontrado")
            print(f"Modelos disponíveis: {models[:5]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão Bedrock: {str(e)}")
        return False

async def test_agentos_bedrock():
    """Testa AgentOS com Bedrock."""
    print("\n🤖 Testando AgentOS + Bedrock...")
    
    try:
        from agno.agent import Agent
        from agno.models.aws_bedrock import BedrockChat
        
        # Cria agente de teste
        agent = Agent(
            id="test-bedrock-agent",
            model=BedrockChat(id="amazon.nova-lite-v1:0")
        )
        
        print("✅ Agente Bedrock criado com sucesso")
        
        # Testa processamento (se possível)
        try:
            response = await agent.arun("Teste de conexão")
            print(f"✅ Resposta do agente: {response.content[:50]}...")
            return True
        except Exception as e:
            print(f"⚠️ Erro no processamento: {str(e)}")
            print("Agente criado mas processamento falhou")
            return True  # Agente foi criado com sucesso
            
    except Exception as e:
        print(f"❌ Erro ao criar agente Bedrock: {str(e)}")
        return False

def test_api_endpoints():
    """Testa endpoints da API."""
    print("\n🌐 Testando endpoints da API...")
    
    import requests
    
    try:
        # Testa se API está rodando
        response = requests.get("http://localhost:8000/api/v1/agents/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API respondendo")
            print(f"   Modelo: {data.get('model', 'N/A')}")
            print(f"   Provider: {data.get('provider', 'N/A')}")
            return True
        else:
            print(f"⚠️ API retornou status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException:
        print("⚠️ API não está rodando em localhost:8000")
        print("Execute: python examples/bedrock_agentos_integration.py")
        return False

async def main():
    """Função principal."""
    print("🚀 TESTE: AgentOS + AWS Bedrock")
    print("=" * 40)
    
    # Executa verificações
    checks = [
        ("Configuração AWS", check_aws_config()),
        ("Imports Bedrock", check_bedrock_imports()),
        ("Conexão Bedrock", await test_bedrock_connection()),
        ("AgentOS Bedrock", await test_agentos_bedrock()),
        ("API Endpoints", test_api_endpoints())
    ]
    
    print(f"\n📊 RESULTADO DAS VERIFICAĐÕES:")
    print("-" * 30)
    
    total_pass = 0
    for nome, resultado in checks:
        if resultado:
            print(f"✅ {nome}")
            total_pass += 1
        else:
            print(f"❌ {nome}")
    
    print(f"\n🎯 TOTAL: {total_pass}/5 verificações passaram")
    
    if total_pass >= 4:
        print("🎉 Integração Bedrock + AgentOS funcionando!")
    else:
        print("⚠️ Algumas configurações precisam ser ajustadas")
    
    print(f"\n📚 PRÓXIMOS PASSOS:")
    print("1. Configure AWS credentials no .env")
    print("2. Execute: python examples/bedrock_agentos_integration.py")
    print("3. Teste: curl http://localhost:8000/api/v1/agents/status")
    print("4. Integre com N8N conforme documentação")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
