"""
Configurações globais de pytest e fixtures compartilhadas
"""
import os
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from typing import Dict, Any, List
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente de teste
load_dotenv('../test.env')

# Configurações de teste
TEST_CONFIG = {
    'CHATWOOT_BASE_URL': os.getenv('CHATWOOT_BASE_URL', 'https://test.chatwoot.com'),
    'CHATWOOT_ACCESS_TOKEN': os.getenv('CHATWOOT_ACCESS_TOKEN', 'test-token'),
    'CHATWOOT_ACCOUNT_ID': os.getenv('CHATWOOT_ACCOUNT_ID', '1'),
    'N8N_BASE_URL': os.getenv('N8N_BASE_URL', 'http://localhost:5679'),
    'N8N_API_KEY': os.getenv('N8N_API_KEY', 'test-n8n-key'),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', 'test-openai-key'),
    'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
    'REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6380/1'),
    'DATABASE_URL': os.getenv('DATABASE_URL', 'postgresql://test_user:test_password@localhost:5433/mrdom_test'),
}

@pytest.fixture(scope="session")
def event_loop():
    """Criar loop de evento para toda a sessão de testes"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_config():
    """Fixture com configurações de teste"""
    return TEST_CONFIG.copy()

@pytest.fixture
def mock_openai_client():
    """Mock do cliente OpenAI"""
    mock_client = AsyncMock()
    
    # Configurar respostas padrão
    mock_client.analyze_message_intent.return_value = {
        "intent": "greeting",
        "interest_level": "medium",
        "confidence": 0.8,
        "next_steps": "Follow up",
        "urgency": "low",
        "extracted_info": {
            "name": "Test User",
            "email": "test@example.com"
        }
    }
    
    mock_client.extract_contact_info.return_value = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+5511999999999"
    }
    
    mock_client.generate_response.return_value = "Esta é uma resposta de teste gerada pelo OpenAI."
    
    mock_client.qualify_lead.return_value = {
        "qualification_score": 75,
        "budget_indication": "high",
        "authority_level": "decision_maker",
        "need_level": "high",
        "timeline": "immediate",
        "next_best_action": "follow_up",
        "risk_factors": [],
        "opportunity_size": "large"
    }
    
    return mock_client

@pytest.fixture
def mock_chatwoot_client():
    """Mock do cliente Chatwoot"""
    mock_client = AsyncMock()
    
    # Configurar respostas padrão
    mock_client.get_conversation.return_value = {
        "id": "test-conv-123",
        "status": "open",
        "contact": {
            "id": "test-contact-456",
            "name": "Test User",
            "email": "test@example.com"
        },
        "messages": []
    }
    
    mock_client.send_message.return_value = {
        "id": "test-msg-789",
        "content": "Mensagem enviada com sucesso",
        "message_type": "outgoing"
    }
    
    mock_client.create_contact.return_value = {
        "id": "test-contact-456",
        "name": "Test User",
        "email": "test@example.com"
    }
    
    return mock_client

@pytest.fixture
def mock_n8n_client():
    """Mock do cliente N8N"""
    mock_client = AsyncMock()
    
    # Configurar respostas padrão
    mock_client.trigger_workflow.return_value = {
        "execution_id": "test-exec-123",
        "status": "success",
        "data": {
            "result": "Workflow executado com sucesso"
        }
    }
    
    mock_client.get_workflow_status.return_value = {
        "id": "test-workflow-123",
        "active": True,
        "name": "Test Workflow"
    }
    
    return mock_client

@pytest.fixture
def mock_redis_client():
    """Mock do cliente Redis"""
    mock_client = AsyncMock()
    
    # Simular dados em memória
    mock_data = {}
    
    async def mock_get(key):
        return mock_data.get(key)
    
    async def mock_set(key, value, ex=None):
        mock_data[key] = value
        return True
    
    async def mock_delete(key):
        if key in mock_data:
            del mock_data[key]
            return True
        return False
    
    mock_client.get = mock_get
    mock_client.set = mock_set
    mock_client.delete = mock_delete
    
    return mock_client

@pytest.fixture
def sample_conversation_data():
    """Dados de exemplo para conversas"""
    return {
        "conversation_id": "test-conv-123",
        "contact_id": "test-contact-456",
        "contact": {
            "id": "test-contact-456",
            "name": "João Silva",
            "email": "joao@teste.com",
            "phone": "+5511999999999",
            "company": "Empresa Teste Ltda"
        },
        "messages": [
            {
                "id": "msg-1",
                "content": "Olá, gostaria de saber mais sobre os serviços",
                "message_type": "incoming",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "msg-2", 
                "content": "Claro! Como posso ajudá-lo?",
                "message_type": "outgoing",
                "created_at": datetime.now().isoformat()
            }
        ],
        "status": "open",
        "created_at": datetime.now().isoformat()
    }

@pytest.fixture
def sample_message_data():
    """Dados de exemplo para mensagens"""
    return {
        "id": "test-msg-123",
        "conversation_id": "test-conv-123",
        "content": "Esta é uma mensagem de teste",
        "message_type": "incoming",
        "sender": {
            "id": "test-contact-456",
            "name": "João Silva",
            "type": "contact"
        },
        "created_at": datetime.now().isoformat()
    }

@pytest.fixture
def sample_webhook_data():
    """Dados de exemplo para webhooks"""
    return {
        "event": "message_created",
        "data": {
            "id": "test-msg-123",
            "conversation_id": "test-conv-123",
            "content": "Mensagem via webhook",
            "message_type": "incoming",
            "sender": {
                "id": "test-contact-456",
                "name": "João Silva",
                "type": "contact"
            },
            "created_at": datetime.now().isoformat()
        }
    }

@pytest.fixture
def mock_httpx_client():
    """Mock do cliente HTTP"""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    
    # Configurar resposta padrão
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_response.text = '{"status": "success"}'
    
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    mock_client.put.return_value = mock_response
    mock_client.delete.return_value = mock_response
    
    return mock_client

@pytest.fixture
def test_database():
    """Fixture para banco de dados de teste"""
    # Esta fixture pode ser expandida para conectar com PostgreSQL de teste
    return {
        "url": TEST_CONFIG['DATABASE_URL'],
        "tables": ["test_conversations", "test_messages", "test_contacts"]
    }

@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Configurar ambiente de teste automaticamente"""
    # Definir variáveis de ambiente para testes
    for key, value in TEST_CONFIG.items():
        monkeypatch.setenv(key, value)
    
    # Definir outras variáveis de teste
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

@pytest.fixture
def cleanup_test_data():
    """Fixture para limpeza de dados de teste"""
    yield  # Executar testes
    
    # Limpeza após os testes
    # Aqui você pode adicionar código para limpar dados de teste
    pass

# Configurações específicas para testes de integração
@pytest.fixture
def integration_test_config():
    """Configuração para testes de integração"""
    return {
        "use_real_apis": os.getenv("MOCK_EXTERNAL_APIS", "true").lower() == "false",
        "test_timeout": int(os.getenv("TEST_TIMEOUT", "30")),
        "api_timeout": int(os.getenv("API_TIMEOUT", "10"))
    }

# Fixtures para diferentes tipos de teste
@pytest.fixture
def unit_test_config():
    """Configuração para testes unitários"""
    return {
        "mock_all_external": True,
        "use_test_data": True
    }

@pytest.fixture
def e2e_test_config():
    """Configuração para testes end-to-end"""
    return {
        "use_real_apis": True,
        "use_real_database": True,
        "cleanup_after": True
    }
