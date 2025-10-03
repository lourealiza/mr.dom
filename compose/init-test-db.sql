-- Script de inicialização do banco de dados para testes
-- Este arquivo é executado automaticamente quando o container PostgreSQL é criado

-- Criar schema de teste
CREATE SCHEMA IF NOT EXISTS test_schema;

-- Criar tabelas de teste (se necessário)
CREATE TABLE IF NOT EXISTS test_schema.test_conversations (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) UNIQUE NOT NULL,
    contact_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_schema.test_messages (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    sender_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES test_schema.test_conversations(conversation_id)
);

CREATE TABLE IF NOT EXISTS test_schema.test_contacts (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    company VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados de teste
INSERT INTO test_schema.test_contacts (contact_id, name, email, phone, company) VALUES
('test-contact-1', 'João Silva', 'joao@teste.com', '+5511999999999', 'Empresa Teste Ltda'),
('test-contact-2', 'Maria Santos', 'maria@teste.com', '+5511888888888', 'Tech Solutions Inc'),
('test-contact-3', 'Pedro Oliveira', 'pedro@teste.com', '+5511777777777', 'Startup Inovadora')
ON CONFLICT (contact_id) DO NOTHING;

INSERT INTO test_schema.test_conversations (conversation_id, contact_id, status) VALUES
('test-conv-1', 'test-contact-1', 'active'),
('test-conv-2', 'test-contact-2', 'active'),
('test-conv-3', 'test-contact-3', 'closed')
ON CONFLICT (conversation_id) DO NOTHING;

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_test_conversations_contact_id ON test_schema.test_conversations(contact_id);
CREATE INDEX IF NOT EXISTS idx_test_messages_conversation_id ON test_schema.test_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_test_contacts_email ON test_schema.test_contacts(email);

-- Comentários para documentação
COMMENT ON SCHEMA test_schema IS 'Schema dedicado para testes automatizados';
COMMENT ON TABLE test_schema.test_conversations IS 'Tabela de conversas para testes';
COMMENT ON TABLE test_schema.test_messages IS 'Tabela de mensagens para testes';
COMMENT ON TABLE test_schema.test_contacts IS 'Tabela de contatos para testes';
