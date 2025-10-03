-- Script para criar a tabela n8n_chat_histories no banco existente
-- Execute este script se o banco já estiver criado e você quiser adicionar a tabela

-- Conectar ao banco 'app'
\c app;

-- Criar a tabela n8n_chat_histories se não existir
CREATE TABLE IF NOT EXISTS public.n8n_chat_histories (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) UNIQUE NOT NULL,
    sender_type VARCHAR(50) NOT NULL, -- 'user', 'bot', 'agent', 'system'
    content TEXT NOT NULL,
    metadata JSONB, -- Dados adicionais como timestamps, user info, etc.
    n8n_execution_id VARCHAR(255), -- ID da execução no N8N
    workflow_id VARCHAR(255), -- ID do workflow do N8N
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id)
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_conversation_id ON public.n8n_chat_histories(conversation_id);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_sender_type ON public.n8n_chat_histories(sender_type);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_created_at ON public.n8n_chat_histories(created_at);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_n8n_execution_id ON public.n8n_chat_histories(n8n_execution_id);

-- Adicionar comentário
COMMENT ON TABLE public.n8n_chat_histories IS 'Tabela de histórico de conversas processadas pelo N8N';

-- Verificar se a tabela foi criada
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'n8n_chat_histories' 
ORDER BY ordinal_position;
