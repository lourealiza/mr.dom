"""
Factories para criar dados de teste de forma consistente
"""
import factory
from factory import fuzzy
from datetime import datetime, timedelta
from typing import Dict, Any, List
import random

class ContactFactory(factory.Factory):
    """Factory para criar contatos de teste"""
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: f"test-contact-{n}")
    name = factory.Faker('name', locale='pt_BR')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number', locale='pt_BR')
    company = factory.Faker('company', locale='pt_BR')
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    
    @factory.lazy_attribute
    def custom_attributes(self):
        return {
            "source": "test",
            "lead_score": random.randint(0, 100),
            "industry": random.choice(["Tecnologia", "Varejo", "Serviços", "Indústria"])
        }

class MessageFactory(factory.Factory):
    """Factory para criar mensagens de teste"""
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: f"test-msg-{n}")
    conversation_id = factory.Sequence(lambda n: f"test-conv-{n}")
    content = factory.Faker('text', max_nb_chars=200, locale='pt_BR')
    message_type = factory.Iterator(['incoming', 'outgoing'])
    created_at = factory.LazyFunction(datetime.now)
    
    @factory.lazy_attribute
    def sender(self):
        if self.message_type == 'incoming':
            return {
                "id": f"test-contact-{random.randint(1, 100)}",
                "name": factory.Faker('name', locale='pt_BR').generate(),
                "type": "contact"
            }
        else:
            return {
                "id": "bot-agent",
                "name": "MrDom Bot",
                "type": "agent_bot"
            }

class ConversationFactory(factory.Factory):
    """Factory para criar conversas de teste"""
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: f"test-conv-{n}")
    status = factory.Iterator(['open', 'resolved', 'pending'])
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    
    @factory.lazy_attribute
    def contact(self):
        return ContactFactory()
    
    @factory.lazy_attribute
    def messages(self):
        # Criar algumas mensagens para a conversa
        num_messages = random.randint(2, 8)
        messages = []
        
        for i in range(num_messages):
            msg_type = 'incoming' if i % 2 == 0 else 'outgoing'
            messages.append(MessageFactory(
                conversation_id=self.id,
                message_type=msg_type
            ))
        
        return messages

class WebhookFactory(factory.Factory):
    """Factory para criar dados de webhook de teste"""
    class Meta:
        model = dict
    
    event = factory.Iterator([
        'message_created',
        'conversation_created', 
        'conversation_updated',
        'contact_created',
        'contact_updated'
    ])
    timestamp = factory.LazyFunction(datetime.now)
    
    @factory.lazy_attribute
    def data(self):
        if self.event == 'message_created':
            return MessageFactory()
        elif self.event in ['conversation_created', 'conversation_updated']:
            return ConversationFactory()
        elif self.event in ['contact_created', 'contact_updated']:
            return ContactFactory()
        else:
            return {}

class BotStateFactory(factory.Factory):
    """Factory para criar estados do bot de teste"""
    class Meta:
        model = dict
    
    conversation_id = factory.Sequence(lambda n: f"test-conv-{n}")
    current_step = factory.Iterator(['greeting', 'qualification', 'handoff', 'follow_up'])
    contact_info = factory.SubFactory(ContactFactory)
    qualification_data = factory.LazyFunction(lambda: {
        "budget": random.choice(["low", "medium", "high"]),
        "timeline": random.choice(["immediate", "1-3_months", "6_months_plus"]),
        "authority": random.choice(["decision_maker", "influencer", "user"])
    })
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)

class OpenAIResponseFactory(factory.Factory):
    """Factory para criar respostas do OpenAI de teste"""
    class Meta:
        model = dict
    
    intent = factory.Iterator(['greeting', 'question', 'complaint', 'escalation'])
    confidence = factory.LazyFunction(lambda: round(random.uniform(0.5, 1.0), 2))
    interest_level = factory.Iterator(['low', 'medium', 'high'])
    urgency = factory.Iterator(['low', 'medium', 'high'])
    
    @factory.lazy_attribute
    def extracted_info(self):
        return {
            "name": factory.Faker('name', locale='pt_BR').generate() if random.random() > 0.5 else None,
            "email": factory.Faker('email').generate() if random.random() > 0.7 else None,
            "phone": factory.Faker('phone_number', locale='pt_BR').generate() if random.random() > 0.8 else None
        }
    
    @factory.lazy_attribute
    def next_steps(self):
        if self.intent == 'greeting':
            return "Continue conversation"
        elif self.intent == 'question':
            return "Provide information"
        elif self.intent == 'complaint':
            return "Escalate to human"
        else:
            return "Follow up"

class N8NWorkflowFactory(factory.Factory):
    """Factory para criar workflows do N8N de teste"""
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: f"test-workflow-{n}")
    name = factory.Faker('catch_phrase')
    active = True
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    
    @factory.lazy_attribute
    def nodes(self):
        return [
            {
                "id": "start-node",
                "type": "n8n-nodes-base.start",
                "name": "Start"
            },
            {
                "id": "webhook-node",
                "type": "n8n-nodes-base.webhook",
                "name": "Webhook Trigger"
            },
            {
                "id": "http-node",
                "type": "n8n-nodes-base.httpRequest",
                "name": "HTTP Request"
            }
        ]

class TestDataFactory:
    """Classe utilitária para criar conjuntos de dados de teste"""
    
    @staticmethod
    def create_conversation_scenario(scenario_type: str) -> Dict[str, Any]:
        """Criar cenários específicos de conversa"""
        scenarios = {
            "new_lead": {
                "contact": ContactFactory(),
                "messages": [
                    MessageFactory(content="Olá, gostaria de saber mais sobre os serviços", message_type="incoming"),
                    MessageFactory(content="Claro! Como posso ajudá-lo?", message_type="outgoing")
                ],
                "expected_intent": "greeting",
                "expected_action": "qualify_lead"
            },
            "qualified_lead": {
                "contact": ContactFactory(),
                "messages": [
                    MessageFactory(content="Preciso de uma solução para minha empresa", message_type="incoming"),
                    MessageFactory(content="Qual o tamanho da sua empresa?", message_type="outgoing"),
                    MessageFactory(content="Temos 50 funcionários", message_type="incoming"),
                    MessageFactory(content="Qual o seu orçamento?", message_type="outgoing"),
                    MessageFactory(content="Até R$ 10.000 por mês", message_type="incoming")
                ],
                "expected_intent": "qualification",
                "expected_action": "handoff_to_sales"
            },
            "complaint": {
                "contact": ContactFactory(),
                "messages": [
                    MessageFactory(content="Estou insatisfeito com o atendimento", message_type="incoming"),
                    MessageFactory(content="Lamento pelo problema. Vou escalar para um supervisor", message_type="outgoing")
                ],
                "expected_intent": "complaint",
                "expected_action": "escalate_to_human"
            },
            "escalation_request": {
                "contact": ContactFactory(),
                "messages": [
                    MessageFactory(content="Quero falar com um humano", message_type="incoming"),
                    MessageFactory(content="Vou transferir você para um atendente", message_type="outgoing")
                ],
                "expected_intent": "escalation",
                "expected_action": "escalate_to_human"
            }
        }
        
        return scenarios.get(scenario_type, scenarios["new_lead"])
    
    @staticmethod
    def create_bulk_test_data(count: int = 10) -> List[Dict[str, Any]]:
        """Criar dados em massa para testes de performance"""
        return [
            {
                "conversation": ConversationFactory(),
                "contact": ContactFactory(),
                "messages": [MessageFactory() for _ in range(random.randint(1, 5))]
            }
            for _ in range(count)
        ]
    
    @staticmethod
    def create_error_scenarios() -> List[Dict[str, Any]]:
        """Criar cenários de erro para testes"""
        return [
            {
                "name": "invalid_webhook_data",
                "data": {"invalid": "data"},
                "expected_error": "ValidationError"
            },
            {
                "name": "missing_required_fields",
                "data": {"conversation_id": "test-123"},
                "expected_error": "MissingRequiredField"
            },
            {
                "name": "invalid_api_response",
                "data": {"status": "error", "message": "API Error"},
                "expected_error": "APIError"
            }
        ]
