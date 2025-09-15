import os
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from ..domain.bot_logic import BotLogic, extract_name, step_transition
from ..domain.models import (
    State, MessageAnalysis, ActionType, IntentType, 
    InterestLevel, UrgencyLevel
)
from ..services.openai_client import OpenAIClient

# Mock OpenAI client
@pytest.fixture
def bot(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    
    # Mock OpenAI client methods
    mock_client = AsyncMock(spec=OpenAIClient)
    mock_client.analyze_message_intent.return_value = {
        "intent": "greeting",
        "interest_level": "medium",
        "confidence": 0.8,
        "next_steps": "Follow up",
        "urgency": "low"
    }
    mock_client.extract_contact_info.return_value = {
        "name": "Test User",
        "email": "test@example.com"
    }
    mock_client.generate_response.return_value = "Test response"
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
    
    # Mock the OpenAIClient class
    monkeypatch.setattr("api.services.openai_client.OpenAIClient", Mock(return_value=mock_client))
    
    return BotLogic()

# Test extract_name
def test_extract_name_basic():
    assert extract_name("João") == "João"
    assert extract_name("Maria Silva") == "Maria"
    assert extract_name("") is None

def test_extract_name_with_greetings():
    assert extract_name("Olá João") == "João"
    assert extract_name("Oi Maria") == "Maria"
    assert extract_name("olá oi hey") is None

# Test step_transition
def test_step_transition_initial_state():
    state = State()
    new_state, reply, action = step_transition(state, "João")
    assert new_state.nome == "João"
    assert "empresa" in reply.lower()
    assert action is None

def test_step_transition_get_company():
    state = State(nome="João")
    new_state, reply, action = step_transition(state, "MrDom Tech")
    assert new_state.empresa == "MrDom Tech"
    assert "cargo" in reply.lower()
    assert action is None

def test_step_transition_get_role():
    state = State(nome="João", empresa="MrDom Tech")
    new_state, reply, action = step_transition(state, "Gerente de Vendas")
    assert new_state.cargo == "Gerente de Vendas"
    assert "ferramentas" in reply.lower()
    assert action is None

def test_step_transition_get_tools():
    state = State(
        nome="João", 
        empresa="MrDom Tech",
        cargo="Gerente de Vendas"
    )
    new_state, reply, action = step_transition(state, "Pipedrive, Excel")
    assert new_state.ferramentas == "Pipedrive, Excel"
    assert "dor" in reply.lower()
    assert action is None

def test_step_transition_get_pain():
    state = State(
        nome="João",
        empresa="MrDom Tech",
        cargo="Gerente de Vendas",
        ferramentas="Pipedrive, Excel"
    )
    new_state, reply, action = step_transition(state, "Integração ruim")
    assert new_state.dor_principal == "Integração ruim"
    assert "consultor" in reply.lower()
    assert action == "handoff"

# Test BotLogic class methods
@pytest.mark.asyncio
async def test_analyze_message(bot):
    analysis = await bot.analyze_message("Olá, gostaria de saber mais sobre os preços")
    assert isinstance(analysis, MessageAnalysis)
    assert analysis.intent in IntentType

def test_determine_action(bot):
    # Test with low confidence analysis
    low_confidence_analysis = MessageAnalysis(confidence=0.2)
    action = bot.determine_action(low_confidence_analysis)
    assert action == ActionType.ESCALATE_TO_HUMAN

    # Test with high urgency analysis
    urgent_analysis = MessageAnalysis(urgency=UrgencyLevel.HIGH)
    action = bot.determine_action(urgent_analysis)
    assert action == ActionType.ESCALATE_TO_HUMAN

    # Test with high interest analysis
    interest_analysis = MessageAnalysis(
        interest_level=InterestLevel.HIGH,
        confidence=0.8
    )
    action = bot.determine_action(interest_analysis)
    assert action in [ActionType.SEND_AUTOMATED_RESPONSE, ActionType.TRIGGER_N8N_WORKFLOW]

def test_should_escalate(bot):
    # Test low confidence case
    low_confidence = MessageAnalysis(confidence=0.2)
    assert bot._should_escalate(low_confidence) is True

    # Test high urgency case
    urgent = MessageAnalysis(
        confidence=0.8,
        urgency=UrgencyLevel.HIGH
    )
    assert bot._should_escalate(urgent) is True

    # Test complaint case
    complaint = MessageAnalysis(
        confidence=0.8,
        intent=IntentType.COMPLAINT
    )
    assert bot._should_escalate(complaint) is True

def test_should_auto_respond(bot):
    # Test greeting case
    greeting = MessageAnalysis(
        confidence=0.8,
        intent=IntentType.GREETING
    )
    assert bot._should_auto_respond(greeting) is True

    # Test high interest case
    high_interest = MessageAnalysis(
        confidence=0.8,
        interest_level=InterestLevel.HIGH
    )
    assert bot._should_auto_respond(high_interest) is True

def test_should_trigger_workflow(bot):
    # Test high interest case
    high_interest = MessageAnalysis(
        interest_level=InterestLevel.HIGH
    )
    assert bot._should_trigger_workflow(high_interest) is True

    # Test with contact info
    with_contact = MessageAnalysis(
        extracted_info={"email": "test@example.com"}
    )
    assert bot._should_trigger_workflow(with_contact) is True

@pytest.mark.asyncio
async def test_generate_response(bot):
    analysis = MessageAnalysis(
        intent=IntentType.GREETING,
        confidence=0.8
    )
    response = await bot.generate_response(analysis)
    assert isinstance(response, str)
    assert len(response) > 0

def test_is_business_hours(bot):
    # Note: This test depends on current time
    result = bot.is_business_hours()
    assert isinstance(result, bool)

@pytest.mark.asyncio
async def test_qualify_lead(bot):
    conversation_history = [
        {"role": "user", "content": "Olá, gostaria de saber mais sobre os preços"},
        {"role": "assistant", "content": "Claro! Qual é o tamanho da sua empresa?"},
        {"role": "user", "content": "Temos 50 funcionários"},
    ]
    qualification = await bot.qualify_lead(conversation_history)
    assert qualification.qualification_score >= 0
    assert qualification.qualification_score <= 100

def test_load_configuration(bot):
    config = bot._load_configuration()
    assert isinstance(config.welcome_message, str)
    assert isinstance(config.escalation_keywords, list)
    assert isinstance(config.auto_response_enabled, bool)