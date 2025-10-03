"""
Testes end-to-end do sistema completo
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from ..domain.bot_logic import BotLogic
from ..domain.models import State, MessageAnalysis, IntentType, InterestLevel, ActionType
from ..services.openai_client import OpenAIClient
from ..services.chatwoot_client import ChatwootClient
from ..services.n8n_client import N8NClient


@pytest.mark.e2e
class TestEndToEndWorkflow:
    """Testes end-to-end do fluxo completo"""
    
    @pytest.fixture
    def bot_logic(self, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Instância do BotLogic com mocks"""
        return BotLogic()
    
    @pytest.fixture
    def sample_conversation_flow(self):
        """Fluxo completo de conversa de exemplo"""
        return [
            {
                "step": "greeting",
                "user_message": "Olá, gostaria de saber mais sobre os serviços",
                "expected_intent": IntentType.GREETING,
                "expected_response_contains": ["olá", "ajudar"]
            },
            {
                "step": "qualification",
                "user_message": "Temos uma empresa com 50 funcionários",
                "expected_intent": IntentType.QUESTION,
                "expected_response_contains": ["empresa", "funcionários"]
            },
            {
                "step": "interest",
                "user_message": "Precisamos de uma solução para CRM",
                "expected_intent": IntentType.QUESTION,
                "expected_response_contains": ["CRM", "solução"]
            },
            {
                "step": "handoff",
                "user_message": "Quero falar com um consultor",
                "expected_intent": IntentType.ESCALATION,
                "expected_response_contains": ["consultor", "transferir"]
            }
        ]
    
    @pytest.mark.asyncio
    async def test_complete_conversation_flow(self, bot_logic, sample_conversation_flow, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste do fluxo completo de conversa"""
        
        # Configurar mocks para diferentes etapas
        mock_openai_client.analyze_message_intent.side_effect = [
            # Resposta para saudação
            {
                "intent": "greeting",
                "interest_level": "medium",
                "confidence": 0.9,
                "next_steps": "Continue conversation",
                "urgency": "low",
                "extracted_info": {"name": "João Silva"}
            },
            # Resposta para qualificação
            {
                "intent": "question",
                "interest_level": "high",
                "confidence": 0.8,
                "next_steps": "Qualify lead",
                "urgency": "medium",
                "extracted_info": {"company_size": "50 funcionários"}
            },
            # Resposta para interesse
            {
                "intent": "question",
                "interest_level": "high",
                "confidence": 0.9,
                "next_steps": "Provide information",
                "urgency": "medium",
                "extracted_info": {"need": "CRM"}
            },
            # Resposta para escalação
            {
                "intent": "escalation",
                "interest_level": "high",
                "confidence": 0.95,
                "next_steps": "Escalate to human",
                "urgency": "high",
                "extracted_info": {"escalation_request": True}
            }
        ]
        
        mock_openai_client.generate_response.side_effect = [
            "Olá! Como posso ajudá-lo hoje?",
            "Ótimo! Qual o tamanho da sua empresa?",
            "Entendo que precisam de uma solução CRM. Posso ajudá-los com isso.",
            "Vou transferir você para um consultor especializado."
        ]
        
        # Simular fluxo de conversa
        conversation_state = State()
        
        for step_data in sample_conversation_flow:
            user_message = step_data["user_message"]
            
            # Analisar mensagem
            analysis = await bot_logic.analyze_message(user_message)
            assert isinstance(analysis, MessageAnalysis)
            
            # Determinar ação
            action = bot_logic.determine_action(analysis)
            assert action is not None
            
            # Gerar resposta
            response = await bot_logic.generate_response(analysis)
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Verificar se a resposta contém palavras esperadas
            for expected_word in step_data["expected_response_contains"]:
                assert expected_word.lower() in response.lower()
    
    @pytest.mark.asyncio
    async def test_lead_qualification_workflow(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste do workflow de qualificação de lead"""
        
        # Configurar mock para qualificação
        mock_openai_client.qualify_lead.return_value = {
            "qualification_score": 85,
            "budget_indication": "high",
            "authority_level": "decision_maker",
            "need_level": "high",
            "timeline": "immediate",
            "next_best_action": "handoff_to_sales",
            "risk_factors": [],
            "opportunity_size": "large"
        }
        
        # Simular conversa de qualificação
        conversation_history = [
            {"role": "user", "content": "Olá, gostaria de saber sobre CRM"},
            {"role": "assistant", "content": "Claro! Qual o tamanho da sua empresa?"},
            {"role": "user", "content": "Temos 100 funcionários"},
            {"role": "assistant", "content": "Qual o seu orçamento aproximado?"},
            {"role": "user", "content": "Até R$ 50.000 por mês"},
            {"role": "assistant", "content": "Qual o prazo para implementação?"},
            {"role": "user", "content": "Precisamos para o próximo trimestre"}
        ]
        
        # Executar qualificação
        qualification = await bot_logic.qualify_lead(conversation_history)
        
        assert qualification.qualification_score >= 0
        assert qualification.qualification_score <= 100
        assert qualification.budget_indication in ["low", "medium", "high"]
        assert qualification.authority_level in ["decision_maker", "influencer", "user"]
        assert qualification.need_level in ["low", "medium", "high"]
        assert qualification.timeline in ["immediate", "1-3_months", "6_months_plus"]
    
    @pytest.mark.asyncio
    async def test_escalation_workflow(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste do workflow de escalação"""
        
        # Configurar mock para escalação
        mock_openai_client.analyze_message_intent.return_value = {
            "intent": "escalation",
            "interest_level": "high",
            "confidence": 0.9,
            "next_steps": "Escalate to human",
            "urgency": "high",
            "extracted_info": {"escalation_request": True}
        }
        
        # Simular mensagem de escalação
        escalation_message = "Quero falar com um supervisor"
        
        # Analisar mensagem
        analysis = await bot_logic.analyze_message(escalation_message)
        assert analysis.intent == IntentType.ESCALATION
        
        # Determinar ação
        action = bot_logic.determine_action(analysis)
        assert action == ActionType.ESCALATE_TO_HUMAN
        
        # Verificar se deve escalar
        should_escalate = bot_logic._should_escalate(analysis)
        assert should_escalate is True
    
    @pytest.mark.asyncio
    async def test_n8n_workflow_trigger(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste de trigger de workflow N8N"""
        
        # Configurar mock para trigger de workflow
        mock_openai_client.analyze_message_intent.return_value = {
            "intent": "question",
            "interest_level": "high",
            "confidence": 0.8,
            "next_steps": "Trigger workflow",
            "urgency": "medium",
            "extracted_info": {
                "name": "João Silva",
                "email": "joao@teste.com",
                "company": "Empresa Teste"
            }
        }
        
        mock_n8n_client.trigger_workflow.return_value = {
            "execution_id": "test-exec-123",
            "status": "success",
            "data": {
                "result": "Workflow executado com sucesso",
                "next_action": "follow_up"
            }
        }
        
        # Simular mensagem que deve triggerar workflow
        workflow_message = "Preciso de uma proposta personalizada"
        
        # Analisar mensagem
        analysis = await bot_logic.analyze_message(workflow_message)
        assert analysis.interest_level == InterestLevel.HIGH
        
        # Determinar ação
        action = bot_logic.determine_action(analysis)
        assert action in [ActionType.TRIGGER_N8N_WORKFLOW, ActionType.SEND_AUTOMATED_RESPONSE]
        
        # Verificar se deve triggerar workflow
        should_trigger = bot_logic._should_trigger_workflow(analysis)
        assert should_trigger is True
    
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste de tratamento de erros no workflow"""
        
        # Simular erro na análise de mensagem
        mock_openai_client.analyze_message_intent.side_effect = Exception("API Error")
        
        # Tentar analisar mensagem
        with pytest.raises(Exception):
            await bot_logic.analyze_message("Mensagem de teste")
        
        # Simular erro na geração de resposta
        mock_openai_client.generate_response.side_effect = Exception("Response Error")
        
        analysis = MessageAnalysis(
            intent=IntentType.GREETING,
            confidence=0.8
        )
        
        with pytest.raises(Exception):
            await bot_logic.generate_response(analysis)
    
    @pytest.mark.asyncio
    async def test_business_hours_workflow(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste de workflow considerando horário comercial"""
        
        # Verificar se está em horário comercial
        is_business_hours = bot_logic.is_business_hours()
        assert isinstance(is_business_hours, bool)
        
        # Simular mensagem fora do horário comercial
        mock_openai_client.analyze_message_intent.return_value = {
            "intent": "question",
            "interest_level": "medium",
            "confidence": 0.7,
            "next_steps": "Respond during business hours",
            "urgency": "low",
            "extracted_info": {}
        }
        
        # Analisar mensagem
        analysis = await bot_logic.analyze_message("Mensagem fora do horário")
        
        # Determinar ação baseada no horário
        action = bot_logic.determine_action(analysis)
        assert action is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_conversations(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste de múltiplas conversas simultâneas"""
        
        # Configurar mock para múltiplas conversas
        mock_openai_client.analyze_message_intent.return_value = {
            "intent": "greeting",
            "interest_level": "medium",
            "confidence": 0.8,
            "next_steps": "Continue conversation",
            "urgency": "low",
            "extracted_info": {}
        }
        
        mock_openai_client.generate_response.return_value = "Resposta automática"
        
        # Simular múltiplas conversas simultâneas
        conversations = [
            {"id": "conv-1", "message": "Olá, primeira conversa"},
            {"id": "conv-2", "message": "Oi, segunda conversa"},
            {"id": "conv-3", "message": "Hey, terceira conversa"}
        ]
        
        # Processar todas as conversas simultaneamente
        tasks = []
        for conv in conversations:
            task = bot_logic.analyze_message(conv["message"])
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Verificar que todas as análises foram processadas
        assert len(results) == len(conversations)
        for result in results:
            assert isinstance(result, MessageAnalysis)
    
    @pytest.mark.asyncio
    async def test_data_persistence_workflow(self, bot_logic, mock_openai_client, mock_chatwoot_client, mock_n8n_client):
        """Teste de persistência de dados no workflow"""
        
        # Simular estado de conversa
        conversation_state = State(
            conversation_id="test-conv-123",
            current_step="qualification",
            contact_info={
                "name": "João Silva",
                "email": "joao@teste.com"
            },
            qualification_data={
                "budget": "high",
                "timeline": "immediate"
            }
        )
        
        # Verificar se o estado foi criado corretamente
        assert conversation_state.conversation_id == "test-conv-123"
        assert conversation_state.current_step == "qualification"
        assert conversation_state.contact_info["name"] == "João Silva"
        assert conversation_state.qualification_data["budget"] == "high"
        
        # Simular atualização do estado
        conversation_state.current_step = "handoff"
        conversation_state.qualification_data["score"] = 85
        
        assert conversation_state.current_step == "handoff"
        assert conversation_state.qualification_data["score"] == 85
