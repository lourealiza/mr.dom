"""
Testes de integração com Chatwoot
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import httpx
from datetime import datetime

from ..services.chatwoot_client import ChatwootClient
from ..domain.models import MessageAnalysis, IntentType, InterestLevel


@pytest.mark.integration
@pytest.mark.chatwoot
class TestChatwootIntegration:
    """Testes de integração com Chatwoot"""
    
    @pytest.fixture
    def chatwoot_client(self, test_config):
        """Cliente Chatwoot para testes"""
        return ChatwootClient(
            base_url=test_config['CHATWOOT_BASE_URL'],
            access_token=test_config['CHATWOOT_ACCESS_TOKEN'],
            account_id=test_config['CHATWOOT_ACCOUNT_ID']
        )
    
    @pytest.fixture
    def sample_contact_data(self):
        """Dados de exemplo para contato"""
        return {
            "id": "test-contact-123",
            "name": "João Silva",
            "email": "joao@teste.com",
            "phone": "+5511999999999",
            "company": "Empresa Teste Ltda",
            "created_at": datetime.now().isoformat()
        }
    
    @pytest.fixture
    def sample_conversation_data(self):
        """Dados de exemplo para conversa"""
        return {
            "id": "test-conv-123",
            "status": "open",
            "contact": {
                "id": "test-contact-123",
                "name": "João Silva",
                "email": "joao@teste.com"
            },
            "messages": [
                {
                    "id": "msg-1",
                    "content": "Olá, gostaria de saber mais sobre os serviços",
                    "message_type": "incoming",
                    "created_at": datetime.now().isoformat()
                }
            ],
            "created_at": datetime.now().isoformat()
        }
    
    @pytest.mark.asyncio
    async def test_get_account_info(self, chatwoot_client, integration_test_config):
        """Teste para obter informações da conta"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        account_info = await chatwoot_client.get_account_info()
        
        assert account_info is not None
        assert 'id' in account_info
        assert 'name' in account_info
    
    @pytest.mark.asyncio
    async def test_get_conversation(self, chatwoot_client, sample_conversation_data, integration_test_config):
        """Teste para obter conversa por ID"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        conversation_id = sample_conversation_data['id']
        
        try:
            conversation = await chatwoot_client.get_conversation(conversation_id)
            assert conversation is not None
            assert 'id' in conversation
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Conversa {conversation_id} não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_send_message(self, chatwoot_client, sample_conversation_data, integration_test_config):
        """Teste para enviar mensagem"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        conversation_id = sample_conversation_data['id']
        message_content = "Esta é uma mensagem de teste enviada pelo bot"
        
        try:
            result = await chatwoot_client.send_message(conversation_id, message_content)
            assert result is not None
            assert 'id' in result
            assert result['content'] == message_content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Conversa {conversation_id} não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_create_contact(self, chatwoot_client, sample_contact_data, integration_test_config):
        """Teste para criar contato"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        contact_data = {
            "name": sample_contact_data['name'],
            "email": sample_contact_data['email'],
            "phone": sample_contact_data['phone']
        }
        
        try:
            result = await chatwoot_client.create_contact(contact_data)
            assert result is not None
            assert 'id' in result
            assert result['name'] == contact_data['name']
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                pytest.skip("Dados de contato inválidos ou contato já existe")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_update_conversation_status(self, chatwoot_client, sample_conversation_data, integration_test_config):
        """Teste para atualizar status da conversa"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        conversation_id = sample_conversation_data['id']
        new_status = "resolved"
        
        try:
            result = await chatwoot_client.update_conversation_status(conversation_id, new_status)
            assert result is not None
            assert result['status'] == new_status
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Conversa {conversation_id} não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_get_conversation_messages(self, chatwoot_client, sample_conversation_data, integration_test_config):
        """Teste para obter mensagens da conversa"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        conversation_id = sample_conversation_data['id']
        
        try:
            messages = await chatwoot_client.get_conversation_messages(conversation_id)
            assert isinstance(messages, list)
            # Verificar estrutura das mensagens
            for message in messages:
                assert 'id' in message
                assert 'content' in message
                assert 'message_type' in message
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Conversa {conversation_id} não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_conversation_with_message_analysis(self, chatwoot_client, sample_message_data, integration_test_config):
        """Teste de conversa com análise de mensagem"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Criar análise de mensagem
        analysis = MessageAnalysis(
            intent=IntentType.QUESTION,
            confidence=0.8,
            interest_level=InterestLevel.HIGH,
            extracted_info={
                "name": "João Silva",
                "email": "joao@teste.com"
            }
        )
        
        conversation_id = sample_message_data['conversation_id']
        
        # Enviar mensagem baseada na análise
        response_message = f"Baseado na sua pergunta (confiança: {analysis.confidence}), posso ajudá-lo com informações sobre nossos serviços."
        
        try:
            result = await chatwoot_client.send_message(conversation_id, response_message)
            assert result is not None
            assert 'id' in result
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Conversa {conversation_id} não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_error_handling(self, chatwoot_client, integration_test_config):
        """Teste de tratamento de erros"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Tentar obter conversa inexistente
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await chatwoot_client.get_conversation("conversa-inexistente")
        
        assert exc_info.value.response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, chatwoot_client, integration_test_config):
        """Teste de timeout"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Configurar timeout muito baixo para forçar timeout
        client_with_timeout = ChatwootClient(
            base_url=integration_test_config['CHATWOOT_BASE_URL'],
            access_token=integration_test_config['CHATWOOT_ACCESS_TOKEN'],
            account_id=integration_test_config['CHATWOOT_ACCOUNT_ID'],
            timeout=0.1  # 100ms timeout
        )
        
        with pytest.raises(httpx.TimeoutException):
            await client_with_timeout.get_account_info()


@pytest.mark.integration
@pytest.mark.chatwoot
@pytest.mark.mock
class TestChatwootMockIntegration:
    """Testes de integração com Chatwoot usando mocks"""
    
    @pytest.fixture
    def mock_chatwoot_client(self, mock_chatwoot_client):
        """Cliente Chatwoot mockado"""
        return mock_chatwoot_client
    
    @pytest.mark.asyncio
    async def test_mock_send_message(self, mock_chatwoot_client):
        """Teste de envio de mensagem com mock"""
        conversation_id = "test-conv-123"
        message_content = "Mensagem de teste"
        
        result = await mock_chatwoot_client.send_message(conversation_id, message_content)
        
        assert result is not None
        assert result['id'] == "test-msg-789"
        assert result['content'] == "Mensagem enviada com sucesso"
    
    @pytest.mark.asyncio
    async def test_mock_get_conversation(self, mock_chatwoot_client):
        """Teste de obtenção de conversa com mock"""
        conversation_id = "test-conv-123"
        
        conversation = await mock_chatwoot_client.get_conversation(conversation_id)
        
        assert conversation is not None
        assert conversation['id'] == conversation_id
        assert conversation['status'] == "open"
        assert 'contact' in conversation
    
    @pytest.mark.asyncio
    async def test_mock_create_contact(self, mock_chatwoot_client):
        """Teste de criação de contato com mock"""
        contact_data = {
            "name": "João Silva",
            "email": "joao@teste.com",
            "phone": "+5511999999999"
        }
        
        result = await mock_chatwoot_client.create_contact(contact_data)
        
        assert result is not None
        assert result['id'] == "test-contact-456"
        assert result['name'] == contact_data['name']
        assert result['email'] == contact_data['email']


@pytest.mark.integration
@pytest.mark.chatwoot
@pytest.mark.slow
class TestChatwootPerformanceIntegration:
    """Testes de performance com Chatwoot"""
    
    @pytest.mark.asyncio
    async def test_concurrent_message_sending(self, chatwoot_client, integration_test_config):
        """Teste de envio concorrente de mensagens"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Criar múltiplas mensagens simultâneas
        tasks = []
        for i in range(3):  # Reduzido para evitar spam
            message_content = f"Mensagem de teste {i}"
            task = chatwoot_client.send_message("test-conv-123", message_content)
            tasks.append(task)
        
        # Executar todas as tarefas simultaneamente
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verificar que pelo menos algumas mensagens foram enviadas
            successful_results = [r for r in results if not isinstance(r, Exception)]
            assert len(successful_results) > 0
            
        except Exception as e:
            if "404" in str(e):
                pytest.skip("Conversa de teste não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_message_response_time(self, chatwoot_client, integration_test_config):
        """Teste de tempo de resposta de mensagem"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        start_time = datetime.now()
        
        try:
            result = await chatwoot_client.send_message("test-conv-123", "Teste de tempo")
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Verificar que a resposta foi rápida (menos de 3 segundos)
            assert response_time < 3.0
            assert result is not None
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip("Conversa de teste não encontrada")
            else:
                raise
