-- Script de inicialização do banco de dados principal
-- Este arquivo é executado automaticamente quando o container PostgreSQL é criado

-- Criar schema principal
CREATE SCHEMA IF NOT EXISTS public;

-- Criar tabelas principais (se necessário)
CREATE TABLE IF NOT EXISTS public.conversations (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) UNIQUE NOT NULL,
    contact_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.messages (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    sender_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id)
);

CREATE TABLE IF NOT EXISTS public.contacts (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    company VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.bot_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    conversation_id VARCHAR(255),
    current_step VARCHAR(100),
    state_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id)
);

CREATE TABLE IF NOT EXISTS public.workflow_executions (
    id SERIAL PRIMARY KEY,
    execution_id VARCHAR(255) UNIQUE NOT NULL,
    workflow_id VARCHAR(255),
    conversation_id VARCHAR(255),
    status VARCHAR(50),
    input_data JSONB,
    output_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES public.conversations(conversation_id)
);

-- Tabela para histórico de conversas do N8N
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
CREATE INDEX IF NOT EXISTS idx_conversations_contact_id ON public.conversations(contact_id);
CREATE INDEX IF NOT EXISTS idx_conversations_status ON public.conversations(status);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON public.messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON public.messages(created_at);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON public.contacts(email);
CREATE INDEX IF NOT EXISTS idx_contacts_phone ON public.contacts(phone);
CREATE INDEX IF NOT EXISTS idx_bot_sessions_conversation_id ON public.bot_sessions(conversation_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON public.workflow_executions(status);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_conversation_id ON public.n8n_chat_histories(conversation_id);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_sender_type ON public.n8n_chat_histories(sender_type);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_created_at ON public.n8n_chat_histories(created_at);
CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_n8n_execution_id ON public.n8n_chat_histories(n8n_execution_id);

-- Comentários para documentação
COMMENT ON SCHEMA public IS 'Schema principal da aplicação MrDom SDR';
COMMENT ON TABLE public.conversations IS 'Tabela de conversas do Chatwoot';
COMMENT ON TABLE public.messages IS 'Tabela de mensagens das conversas';
COMMENT ON TABLE public.contacts IS 'Tabela de contatos';
COMMENT ON TABLE public.bot_sessions IS 'Tabela de sessões do bot';
COMMENT ON TABLE public.workflow_executions IS 'Tabela de execuções de workflows do N8N';
COMMENT ON TABLE public.n8n_chat_histories IS 'Tabela de histórico de conversas processadas pelo N8N';
