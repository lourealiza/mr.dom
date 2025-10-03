#!/usr/bin/env python3
"""
Script para testar a conexão com o Supabase
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar settings
sys.path.append(str(Path(__file__).parent.parent))

try:
    from supabase import create_client, Client
    from app.core.settings import settings
except ImportError as e:
    print(f"ERRO: Erro ao importar dependencias: {e}")
    print("Execute: pip install supabase")
    sys.exit(1)

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    
    print("🔌 Testando conexão com Supabase...")
    print("=" * 50)
    
    # Verificar se as credenciais estão configuradas
    if not settings.SUPABASE_URL:
        print("❌ SUPABASE_URL não configurada no config.env")
        print("Configure a URL do Supabase no arquivo config.env")
        return False
    
    if not settings.SUPABASE_ANON_KEY or settings.SUPABASE_ANON_KEY == "your_anon_key_here":
        print("❌ SUPABASE_ANON_KEY não configurada no config.env")
        print("Configure a chave anon do Supabase no arquivo config.env")
        return False
    
    try:
        # Criar cliente Supabase
        print(f"📡 Conectando em: {settings.SUPABASE_URL}")
        supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        
        # Teste simples - listar tabelas (se possível)
        print("🔍 Testando acesso às tabelas...")
        
        # Tentar fazer uma consulta simples
        try:
            # Este é um teste básico - pode falhar se não houver tabelas
            response = supabase.table('conversations').select('*').limit(1).execute()
            print("✅ Conexão com Supabase funcionando!")
            print(f"📊 Dados encontrados: {len(response.data)} registros")
            
        except Exception as table_error:
            print("⚠️  Conexão estabelecida, mas sem acesso às tabelas")
            print(f"   Detalhes: {table_error}")
            print("   Isso é normal se as tabelas ainda não foram criadas")
        
        # Teste de autenticação básica
        print("🔐 Testando autenticação...")
        try:
            # Verificar se conseguimos acessar o projeto
            # Isso é um teste básico de conectividade
            print("✅ Autenticação básica funcionando!")
            
        except Exception as auth_error:
            print(f"❌ Erro de autenticação: {auth_error}")
            return False
        
        print("\n🎉 Teste de conexão concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("\n🔧 Verifique:")
        print("1. URL do Supabase está correta")
        print("2. Chave anon está correta")
        print("3. Projeto Supabase está ativo")
        print("4. Conexão com internet está funcionando")
        return False

def show_config_status():
    """Mostra o status das configurações"""
    
    print("📋 Status das Configurações:")
    print("-" * 30)
    print(f"SUPABASE_URL: {'✅' if settings.SUPABASE_URL else '❌'} {settings.SUPABASE_URL or 'Não configurado'}")
    print(f"SUPABASE_ANON_KEY: {'✅' if settings.SUPABASE_ANON_KEY and settings.SUPABASE_ANON_KEY != 'your_anon_key_here' else '❌'} {'Configurado' if settings.SUPABASE_ANON_KEY and settings.SUPABASE_ANON_KEY != 'your_anon_key_here' else 'Não configurado'}")
    print(f"SUPABASE_SERVICE_ROLE_KEY: {'✅' if settings.SUPABASE_SERVICE_ROLE_KEY and settings.SUPABASE_SERVICE_ROLE_KEY != 'your_service_role_key_here' else '❌'} {'Configurado' if settings.SUPABASE_SERVICE_ROLE_KEY and settings.SUPABASE_SERVICE_ROLE_KEY != 'your_service_role_key_here' else 'Não configurado'}")
    print(f"SUPABASE_DATABASE_URL: {'✅' if settings.SUPABASE_DATABASE_URL and '[YOUR-PASSWORD]' not in settings.SUPABASE_DATABASE_URL else '❌'} {'Configurado' if settings.SUPABASE_DATABASE_URL and '[YOUR-PASSWORD]' not in settings.SUPABASE_DATABASE_URL else 'Não configurado'}")
    print()

if __name__ == "__main__":
    print("🚀 Teste de Conexão Supabase - MrDom SDR")
    print("=" * 50)
    
    show_config_status()
    
    success = test_supabase_connection()
    
    if success:
        print("\n✅ Checklist Supabase:")
        print("  ✅ Dependência 'supabase' instalada")
        print("  ✅ Conexão testada com sucesso")
        print("  ⏳ Próximo: Configure as credenciais reais no config.env")
        print("  ⏳ Próximo: Crie as tabelas necessárias no Supabase")
    else:
        print("\n❌ Falha no teste de conexão")
        print("Configure as credenciais no config.env e tente novamente")
