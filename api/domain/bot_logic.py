import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

from .models import (
    MessageAnalysis, LeadQualification, AgentBotResponse,
    ActionType, IntentType, InterestLevel, UrgencyLevel,
    ConversationContext, ContactInfo, BotConfiguration,
)
from services.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class BotLogic:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.config = self._load_configuration()
        self.conversation_contexts: Dict[int, ConversationContext] = {}

    def _load_configuration(self) -> BotConfiguration:
        """Carregar configuração do bot"""
        return BotConfiguration(
            welcome_message=os.getenv(
                "BOT_WELCOME_MESSAGE", 
                "Olá! 👋 Sou o assistente virtual da MrDom. Como posso ajudá-lo hoje?"
            ),
            escalation_keywords=json.loads(
                os.getenv("ESCALATION_KEYWORDS", '["falar com humano", "atendente", "supervisor"]')
            ),
            auto_response_enabled=os.getenv("AUTO_RESPONSE_ENABLED", "true").lower() == "true",
            qualification_questions=json.loads(
                os.getenv("QUALIFICATION_QUESTIONS", '["Qual é o seu principal desafio?", "Qual o tamanho da sua empresa?"]')
            ),
            business_hours=json.loads(
                os.getenv("BUSINESS_HOURS", '{"start": "09:00", "end": "18:00"}')
            ),
            timezone=os.getenv("TIMEZONE", "America/Sao_Paulo")
        )

    async def analyze_message(self, message_content: str) -> MessageAnalysis:
        """Analisar mensagem do cliente"""
        try:
            # Usar OpenAI para análise de intenção
            analysis_data = await self.openai_client.analyze_message_intent(message_content)
            
            # Extrair informações de contato se necessário
            contact_info = await self.openai_client.extract_contact_info(message_content)
            
            return MessageAnalysis(
                intent=IntentType(analysis_data.get("intent", "unknown")),
                interest_level=InterestLevel(analysis_data.get("interest_level", "low")),
                objection_type=analysis_data.get("objection_type"),
                next_steps=analysis_data.get("next_steps", ""),
                urgency=UrgencyLevel(analysis_data.get("urgency", "low")),
                confidence=analysis_data.get("confidence", 0.5),
                extracted_info=contact_info
            )
            
        except Exception as e:
            logger.error(f"Erro ao analisar mensagem: {str(e)}")
            # Retornar análise padrão em caso de erro
            return MessageAnalysis(
                intent=IntentType.UNKNOWN,
                interest_level=InterestLevel.LOW,
                next_steps="Requer análise manual",
                urgency=UrgencyLevel.LOW,
                confidence=0.1
            )

    def determine_action(self, analysis: MessageAnalysis) -> ActionType:
        """Determinar ação baseada na análise"""
        try:
            # Verificar se deve escalar para humano
            if self._should_escalate(analysis):
                return ActionType.ESCALATE_TO_HUMAN
            
            # Verificar se deve enviar resposta automatizada
            if self._should_auto_respond(analysis):
                return ActionType.SEND_AUTOMATED_RESPONSE
            
            # Verificar se deve disparar workflow N8N
            if self._should_trigger_workflow(analysis):
                return ActionType.TRIGGER_N8N_WORKFLOW
            
            # Verificar se deve agendar follow-up
            if self._should_schedule_follow_up(analysis):
                return ActionType.SCHEDULE_FOLLOW_UP
            
            return ActionType.NO_ACTION
            
        except Exception as e:
            logger.error(f"Erro ao determinar ação: {str(e)}")
            return ActionType.ESCALATE_TO_HUMAN

    def _should_escalate(self, analysis: MessageAnalysis) -> bool:
        """Verificar se deve escalar para humano"""
        # Escalar se confiança baixa
        if analysis.confidence < 0.3:
            return True
        
        # Escalar se urgência alta
        if analysis.urgency == UrgencyLevel.HIGH:
            return True
        
        # Escalar se for reclamação
        if analysis.intent == IntentType.COMPLAINT:
            return True
        
        # Escalar se houver objeção complexa
        if analysis.objection_type and analysis.objection_type not in ["price", "timing"]:
            return True
        
        return False

    def _should_auto_respond(self, analysis: MessageAnalysis) -> bool:
        """Verificar se deve enviar resposta automatizada"""
        if not self.config.auto_response_enabled:
            return False
        
        # Responder se for saudação
        if analysis.intent == IntentType.GREETING:
            return True
        
        # Responder se for pergunta simples
        if analysis.intent == IntentType.QUESTION and analysis.confidence > 0.7:
            return True
        
        # Responder se interesse médio/alto
        if analysis.interest_level in [InterestLevel.MEDIUM, InterestLevel.HIGH]:
            return True
        
        return False

    def _should_trigger_workflow(self, analysis: MessageAnalysis) -> bool:
        """Verificar se deve disparar workflow N8N"""
        # Disparar se interesse alto
        if analysis.interest_level == InterestLevel.HIGH:
            return True
        
        # Disparar se for qualificação de lead
        if analysis.intent == IntentType.INTEREST:
            return True
        
        # Disparar se houver informações de contato
        if analysis.extracted_info and any(analysis.extracted_info.values()):
            return True
        
        return False

    def _should_schedule_follow_up(self, analysis: MessageAnalysis) -> bool:
        """Verificar se deve agendar follow-up"""
        # Agendar se interesse médio
        if analysis.interest_level == InterestLevel.MEDIUM:
            return True
        
        # Agendar se timeline não é imediata
        if "não tenho pressa" in analysis.next_steps.lower():
            return True
        
        return False

    async def generate_response(self, analysis: MessageAnalysis) -> str:
        """Gerar resposta baseada na análise"""
        try:
            # Gerar resposta usando OpenAI
            response = await self.openai_client.generate_response(
                analysis.next_steps,
                {
                    "intent": analysis.intent.value,
                    "interest_level": analysis.interest_level.value,
                    "objection_type": analysis.objection_type
                }
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return self._get_fallback_response(analysis)

    def _get_fallback_response(self, analysis: MessageAnalysis) -> str:
        """Resposta de fallback quando IA falha"""
        if analysis.intent == IntentType.GREETING:
            return self.config.welcome_message
        
        if analysis.intent == IntentType.QUESTION:
            return "Obrigado pela sua pergunta! Vou conectar você com um de nossos especialistas que poderá ajudá-lo melhor."
        
        if analysis.interest_level == InterestLevel.HIGH:
            return "Interessante! Parece que você tem um interesse genuíno. Vou conectar você com um consultor especializado."
        
        return "Obrigado pela sua mensagem! Um de nossos especialistas entrará em contato em breve."

    async def get_welcome_message(self) -> str:
        """Obter mensagem de boas-vindas"""
        return self.config.welcome_message

    async def qualify_lead(
        self, 
        conversation_history: List[Dict[str, str]]
    ) -> LeadQualification:
        """Qualificar lead baseado no histórico"""
        try:
            qualification_data = await self.openai_client.qualify_lead(conversation_history)
            
            return LeadQualification(
                qualification_score=qualification_data.get("qualification_score", 0),
                budget_indication=qualification_data.get("budget_indication", "unknown"),
                authority_level=qualification_data.get("authority_level", "unknown"),
                need_level=qualification_data.get("need_level", "unknown"),
                timeline=qualification_data.get("timeline", "unknown"),
                next_best_action=qualification_data.get("next_best_action", "follow_up"),
                risk_factors=qualification_data.get("risk_factors", []),
                opportunity_size=qualification_data.get("opportunity_size", "unknown")
            )
            
        except Exception as e:
            logger.error(f"Erro ao qualificar lead: {str(e)}")
            return LeadQualification(
                qualification_score=50,
                budget_indication="unknown",
                authority_level="unknown",
                need_level="unknown",
                timeline="unknown",
                next_best_action="manual_review",
                risk_factors=["qualification_failed"],
                opportunity_size="unknown"
            )

    async def handle_objection(self, objection: str, product_context: str) -> str:
        """Lidar com objeção específica"""
        try:
            return await self.openai_client.handle_objection(objection, product_context)
        except Exception as e:
            logger.error(f"Erro ao lidar com objeção: {str(e)}")
            return "Entendo sua preocupação. Vou conectar você com um especialista que poderá esclarecer melhor essa questão."

    async def generate_follow_up_message(
        self, 
        lead_info: Dict[str, Any],
        follow_up_type: str
    ) -> str:
        """Gerar mensagem de follow-up"""
        try:
            return await self.openai_client.generate_follow_up_message(lead_info, follow_up_type)
        except Exception as e:
            logger.error(f"Erro ao gerar follow-up: {str(e)}")
            return f"Olá! Gostaria de saber se você ainda tem interesse em nossa solução. Posso ajudá-lo com alguma dúvida?"

    def get_conversation_context(self, conversation_id: int) -> Optional[ConversationContext]:
        """Obter contexto da conversa"""
        return self.conversation_contexts.get(conversation_id)

    def update_conversation_context(
        self, 
        conversation_id: int, 
        context: ConversationContext
    ):
        """Atualizar contexto da conversa"""
        self.conversation_contexts[conversation_id] = context

    def is_business_hours(self) -> bool:
        """Verificar se está em horário comercial"""
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            start_time = self.config.business_hours.get("start", "09:00")
            end_time = self.config.business_hours.get("end", "18:00")
            
            return start_time <= current_time <= end_time
        except Exception as e:
            logger.error(f"Erro ao verificar horário comercial: {str(e)}")
            return True  # Assumir horário comercial em caso de erro

    def should_escalate_immediately(self, analysis: MessageAnalysis) -> bool:
        """Verificar se deve escalar imediatamente"""
        # Escalar imediatamente se:
        # 1. Fora do horário comercial
        # 2. Urgência muito alta
        # 3. Reclamação
        # 4. Confiança muito baixa
        
        if not self.is_business_hours():
            return True
        
        if analysis.urgency == UrgencyLevel.HIGH and analysis.confidence < 0.5:
            return True
        
        if analysis.intent == IntentType.COMPLAINT:
            return True
        
        return False
