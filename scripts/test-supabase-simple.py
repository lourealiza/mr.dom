#!/usr/bin/env python3
"""
Script simples para testar a conexão com o Supabase
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    
    print("Testando conexao com Supabase...")
    print("=" * 50)
    
    try:
        from supabase import create_client, Client
        from app.core.settings import settings
        
        print("Dependencias importadas com sucesso!")
        
        # Verificar configurações
        print(f"SUPABASE_URL: {settings.SUPABASE_URL}")
        print(f"SUPABASE_ANON_KEY: {'Configurado' if settings.SUPABASE_ANON_KEY and settings.SUPABASE_ANON_KEY != 'your_anon_key_here' else 'Nao configurado'}")
        
        if not settings.SUPABASE_URL:
            print("ERRO: SUPABASE_URL nao configurada")
            return False
            
        if not settings.SUPABASE_ANON_KEY or settings.SUPABASE_ANON_KEY == "your_anon_key_here":
            print("ERRO: SUPABASE_ANON_KEY nao configurada")
            print("Configure as credenciais no config.env")
            return False
        
        # Criar cliente
        print("Criando cliente Supabase...")
        supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        
        print("Cliente criado com sucesso!")
        print("Conexao com Supabase funcionando!")
        
        return True
        
    except ImportError as e:
        print(f"ERRO: Dependencia nao encontrada: {e}")
        print("Execute: pip install supabase")
        return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    print("Teste de Conexao Supabase - MrDom SDR")
    print("=" * 50)
    
    success = test_supabase_connection()
    
    if success:
        print("\nSUCESSO: Conexao testada com sucesso!")
        print("Proximo passo: Configure as credenciais reais no config.env")
    else:
        print("\nFALHA: Teste de conexao falhou")
        print("Configure as credenciais no config.env e tente novamente")
