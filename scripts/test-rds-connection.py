#!/usr/bin/env python3
"""
Script para testar conexão com AWS RDS PostgreSQL
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

def test_rds_connection():
    """Testa a conexão com o RDS PostgreSQL"""
    
    # Carregar variáveis de ambiente
    load_dotenv('config.env')
    
    # Obter configurações do banco
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    
    print("=" * 50)
    print("  Teste de Conexão AWS RDS PostgreSQL")
    print("=" * 50)
    print()
    
    # Verificar se todas as variáveis estão configuradas
    missing_vars = []
    for key, value in db_config.items():
        if not value:
            missing_vars.append(key)
    
    if missing_vars:
        print("❌ Variáveis de ambiente não configuradas:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("Execute: scripts\\configure-aws-rds.bat")
        return False
    
    print("📋 Configurações:")
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config['port']}")
    print(f"   Database: {db_config['database']}")
    print(f"   User: {db_config['user']}")
    print(f"   Password: {'*' * len(db_config['password'])}")
    print()
    
    # Tentar conectar
    try:
        print("🔄 Conectando ao banco...")
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Testar consulta básica
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print("✅ Conexão bem-sucedida!")
        print(f"   PostgreSQL Version: {version}")
        
        # Testar criação de tabela de teste
        print()
        print("🔄 Testando criação de tabela...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                test_message VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            INSERT INTO test_connection (test_message) 
            VALUES ('Teste de conexão AWS RDS');
        """)
        
        cursor.execute("SELECT COUNT(*) FROM test_connection;")
        count = cursor.fetchone()[0]
        
        print(f"✅ Tabela de teste criada! Registros: {count}")
        
        # Limpar tabela de teste
        cursor.execute("DROP TABLE IF EXISTS test_connection;")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print()
        print("🎉 Todos os testes passaram!")
        print("   O banco está pronto para uso com o MrDom SDR")
        
        return True
        
    except psycopg2.OperationalError as e:
        print("❌ Erro de conexão:")
        print(f"   {e}")
        print()
        print("🔧 Possíveis soluções:")
        print("   1. Verifique se o RDS está rodando")
        print("   2. Confirme o endpoint correto")
        print("   3. Verifique o Security Group (porta 5432)")
        print("   4. Confirme usuário e senha")
        return False
        
    except psycopg2.Error as e:
        print("❌ Erro do PostgreSQL:")
        print(f"   {e}")
        return False
        
    except Exception as e:
        print("❌ Erro inesperado:")
        print(f"   {e}")
        return False

def show_n8n_config():
    """Mostra configurações para N8N"""
    
    load_dotenv('config.env')
    
    print()
    print("=" * 50)
    print("  Configuração para N8N")
    print("=" * 50)
    print()
    print("Use estas configurações no N8N:")
    print()
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"Port: {os.getenv('DB_PORT', '5432')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    print(f"Username: {os.getenv('DB_USER')}")
    print(f"Password: {os.getenv('DB_PASSWORD')}")
    print("SSL Mode: require")
    print()

if __name__ == "__main__":
    try:
        success = test_rds_connection()
        if success:
            show_n8n_config()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Teste cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
