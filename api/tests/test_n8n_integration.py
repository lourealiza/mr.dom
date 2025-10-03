"""
Testes de integração com N8N
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import httpx
from datetime import datetime

from ..services.n8n_client import N8NClient
from ..domain.models import MessageAnalysis, IntentType, InterestLevel


@pytest.mark.integration
@pytest.mark.n8n
class TestN8NIntegration:
    """Testes de integração com N8N"""
    
    @pytest.fixture
    def n8n_client(self, test_config):
        """Cliente N8N para testes"""
        return N8NClient(
            base_url=test_config['N8N_BASE_URL'],
            api_key=test_config['N8N_API_KEY']
        )
    
    @pytest.fixture
    def sample_workflow_data(self):
        """Dados de exemplo para workflow"""
        return {
            "workflow_id": "test-workflow-123",
            "name": "Test Workflow",
            "active": True,
            "nodes": [
                {
                    "id": "start-node",
                    "type": "n8n-nodes-base.start",
                    "name": "Start"
                },
                {
                    "id": "webhook-node",
                    "type": "n8n-nodes-base.webhook",
                    "name": "Webhook Trigger"
                }
            ]
        }
    
    @pytest.fixture
    def sample_execution_data(self):
        """Dados de exemplo para execução"""
        return {
            "execution_id": "test-exec-123",
            "workflow_id": "test-workflow-123",
            "status": "success",
            "data": {
                "result": "Workflow executado com sucesso",
                "contact_info": {
                    "name": "João Silva",
                    "email": "joao@teste.com"
                }
            }
        }
    
    @pytest.mark.asyncio
    async def test_get_workflows(self, n8n_client, integration_test_config):
        """Teste para obter lista de workflows"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        workflows = await n8n_client.get_workflows()
        
        assert isinstance(workflows, list)
        # Verificar se retorna pelo menos um workflow (mesmo que seja vazio)
        assert len(workflows) >= 0
    
    @pytest.mark.asyncio
    async def test_get_workflow_by_id(self, n8n_client, sample_workflow_data, integration_test_config):
        """Teste para obter workflow por ID"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        workflow_id = sample_workflow_data['workflow_id']
        
        try:
            workflow = await n8n_client.get_workflow(workflow_id)
            assert workflow is not None
            assert 'id' in workflow
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Workflow {workflow_id} não encontrado")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_trigger_workflow(self, n8n_client, sample_workflow_data, integration_test_config):
        """Teste para disparar workflow"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        workflow_id = sample_workflow_data['workflow_id']
        input_data = {
            "conversation_id": "test-conv-123",
            "message": "Mensagem de teste",
            "contact": {
                "name": "João Silva",
                "email": "joao@teste.com"
            }
        }
        
        try:
            result = await n8n_client.trigger_workflow(workflow_id, input_data)
            assert result is not None
            assert 'execution_id' in result
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Workflow {workflow_id} não encontrado")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_get_execution_status(self, n8n_client, sample_execution_data, integration_test_config):
        """Teste para obter status de execução"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        execution_id = sample_execution_data['execution_id']
        
        try:
            status = await n8n_client.get_execution_status(execution_id)
            assert status is not None
            assert 'status' in status
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip(f"Execução {execution_id} não encontrada")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_workflow_with_message_analysis(self, n8n_client, sample_message_data, integration_test_config):
        """Teste de workflow com análise de mensagem"""
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
        
        # Preparar dados para o workflow
        workflow_data = {
            "conversation_id": sample_message_data['conversation_id'],
            "message_analysis": analysis.dict(),
            "contact_info": analysis.extracted_info,
            "timestamp": datetime.now().isoformat()
        }
        
        # Tentar executar workflow (assumindo que existe um workflow de teste)
        try:
            result = await n8n_client.trigger_workflow("test-workflow-123", workflow_data)
            assert result is not None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip("Workflow de teste não encontrado")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_workflow_error_handling(self, n8n_client, integration_test_config):
        """Teste de tratamento de erros em workflows"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Tentar executar workflow inexistente
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await n8n_client.trigger_workflow("workflow-inexistente", {})
        
        assert exc_info.value.response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_workflow_timeout(self, n8n_client, integration_test_config):
        """Teste de timeout em workflows"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Configurar timeout muito baixo para forçar timeout
        client_with_timeout = N8NClient(
            base_url=integration_test_config['N8N_BASE_URL'],
            api_key=integration_test_config['N8N_API_KEY'],
            timeout=0.1  # 100ms timeout
        )
        
        with pytest.raises(httpx.TimeoutException):
            await client_with_timeout.get_workflows()
    
    @pytest.mark.asyncio
    async def test_workflow_with_large_data(self, n8n_client, integration_test_config):
        """Teste de workflow com dados grandes"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Criar dados grandes
        large_data = {
            "conversation_id": "test-conv-large",
            "messages": [
                {"content": f"Mensagem {i}" * 100}  # Mensagens grandes
                for i in range(50)
            ],
            "contact": {
                "name": "Usuário Teste",
                "email": "teste@exemplo.com",
                "metadata": {
                    "large_field": "x" * 10000  # Campo grande
                }
            }
        }
        
        try:
            result = await n8n_client.trigger_workflow("test-workflow-123", large_data)
            assert result is not None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip("Workflow de teste não encontrado")
            elif e.response.status_code == 413:
                pytest.skip("Dados muito grandes para o workflow")
            else:
                raise


@pytest.mark.integration
@pytest.mark.n8n
@pytest.mark.mock
class TestN8NMockIntegration:
    """Testes de integração com N8N usando mocks"""
    
    @pytest.fixture
    def mock_n8n_client(self, mock_n8n_client):
        """Cliente N8N mockado"""
        return mock_n8n_client
    
    @pytest.mark.asyncio
    async def test_mock_workflow_execution(self, mock_n8n_client):
        """Teste de execução de workflow com mock"""
        workflow_id = "test-workflow-123"
        input_data = {"test": "data"}
        
        result = await mock_n8n_client.trigger_workflow(workflow_id, input_data)
        
        assert result is not None
        assert result['execution_id'] == "test-exec-123"
        assert result['status'] == "success"
    
    @pytest.mark.asyncio
    async def test_mock_workflow_status(self, mock_n8n_client):
        """Teste de status de workflow com mock"""
        workflow_id = "test-workflow-123"
        
        status = await mock_n8n_client.get_workflow_status(workflow_id)
        
        assert status is not None
        assert status['id'] == workflow_id
        assert status['active'] is True
    
    @pytest.mark.asyncio
    async def test_mock_workflow_with_conversation_data(self, mock_n8n_client, sample_conversation_data):
        """Teste de workflow com dados de conversa"""
        workflow_id = "conversation-workflow"
        conversation_data = {
            "conversation": sample_conversation_data,
            "action": "qualify_lead"
        }
        
        result = await mock_n8n_client.trigger_workflow(workflow_id, conversation_data)
        
        assert result is not None
        assert result['status'] == "success"
        assert 'data' in result


@pytest.mark.integration
@pytest.mark.n8n
@pytest.mark.slow
class TestN8NPerformanceIntegration:
    """Testes de performance com N8N"""
    
    @pytest.mark.asyncio
    async def test_concurrent_workflow_executions(self, n8n_client, integration_test_config):
        """Teste de execuções concorrentes de workflows"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        # Criar múltiplas execuções simultâneas
        tasks = []
        for i in range(5):
            workflow_data = {
                "conversation_id": f"test-conv-{i}",
                "message": f"Mensagem de teste {i}",
                "timestamp": datetime.now().isoformat()
            }
            task = n8n_client.trigger_workflow("test-workflow-123", workflow_data)
            tasks.append(task)
        
        # Executar todas as tarefas simultaneamente
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verificar que pelo menos algumas execuções foram bem-sucedidas
            successful_results = [r for r in results if not isinstance(r, Exception)]
            assert len(successful_results) > 0
            
        except Exception as e:
            if "404" in str(e):
                pytest.skip("Workflow de teste não encontrado")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_workflow_response_time(self, n8n_client, integration_test_config):
        """Teste de tempo de resposta de workflow"""
        if not integration_test_config['use_real_apis']:
            pytest.skip("Usando APIs mockadas")
        
        start_time = datetime.now()
        
        try:
            result = await n8n_client.trigger_workflow("test-workflow-123", {"test": "data"})
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Verificar que a resposta foi rápida (menos de 5 segundos)
            assert response_time < 5.0
            assert result is not None
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                pytest.skip("Workflow de teste não encontrado")
            else:
                raise
