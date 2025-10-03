#!/usr/bin/env python3
"""
Script para criar a tabela n8n_chat_histories no banco PostgreSQL
"""

import psycopg2
import os
from pathlib import Path

def create_n8n_chat_histories_table():
    """Cria a tabela n8n_chat_histories no banco PostgreSQL"""
    
    # Configurações do banco (do config.env)
    db_config = {
        'host': 'localhost',  # ou 'postgres' se estiver no Docker
        'port': 5432,
        'database': 'app',
        'user': 'app',
        'password': 'mrdom2024'
    }
    
    # SQL para criar a tabela
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS public.n8n_chat_histories (
        id SERIAL PRIMARY KEY,
        conversation_id VARCHAR(255) NOT NULL,
        message_id VARCHAR(255) UNIQUE NOT NULL,
        sender_type VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        metadata JSONB,
        n8n_execution_id VARCHAR(255),
        workflow_id VARCHAR(255),
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id)
    );
    """
    
    # SQL para criar índices
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_conversation_id ON public.n8n_chat_histories(conversation_id);",
        "CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_sender_type ON public.n8n_chat_histories(sender_type);",
        "CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_created_at ON public.n8n_chat_histories(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_n8n_execution_id ON public.n8n_chat_histories(n8n_execution_id);"
    ]
    
    # SQL para adicionar comentário
    add_comment_sql = """
    COMMENT ON TABLE public.n8n_chat_histories IS 'Tabela de histórico de conversas processadas pelo N8N';
    """
    
    try:
        print("Conectando ao banco PostgreSQL...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        print("Criando tabela n8n_chat_histories...")
        cursor.execute(create_table_sql)
        
        print("Criando indices...")
        for index_sql in create_indexes_sql:
            cursor.execute(index_sql)
        
        print("Adicionando comentario...")
        cursor.execute(add_comment_sql)
        
        # Commit das alterações
        conn.commit()
        
        print("SUCESSO: Tabela n8n_chat_histories criada com sucesso!")
        
        # Verificar se a tabela foi criada
        cursor.execute("""
            SELECT 
                table_name, 
                column_name, 
                data_type, 
                is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'n8n_chat_histories' 
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nEstrutura da tabela:")
        print("-" * 60)
        for col in columns:
            print(f"  {col[1]:<20} {col[2]:<15} {'NULL' if col[3] == 'YES' else 'NOT NULL'}")
        
        print("-" * 60)
        print(f"Total de colunas: {len(columns)}")
        
    except psycopg2.Error as e:
        print(f"ERRO ao conectar/criar tabela: {e}")
        return False
    except Exception as e:
        print(f"ERRO inesperado: {e}")
        return False
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print("Conexao fechada.")
    
    return True

if __name__ == "__main__":
    print("Iniciando criacao da tabela n8n_chat_histories...")
    print("=" * 60)
    
    success = create_n8n_chat_histories_table()
    
    if success:
        print("\nProcesso concluido com sucesso!")
        print("\nProximos passos:")
        print("1. Configure a conexao no N8N com as credenciais:")
        print("   - Host: localhost (ou postgres se Docker)")
        print("   - Port: 5432")
        print("   - Database: app")
        print("   - User: app")
        print("   - Password: mrdom2024")
        print("2. Teste a conexao no N8N")
        print("3. Configure workflows para usar a tabela")
    else:
        print("\nFalha na criacao da tabela. Verifique as credenciais e conexao.")
