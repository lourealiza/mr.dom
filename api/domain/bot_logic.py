import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

from .models import (
    MessageAnalysis, LeadQualification, AgentBotResponse,
    ActionType, IntentType, InterestLevel, UrgencyLevel,
    ConversationContext, ContactInfo, BotConfiguration,
    State, BusinessIntent, FitPrimario,
)
from ..services.openai_client import OpenAIClient

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


def extract_name(text: str) -> str | None:
    """Extract name from user text or return None."""
    # Very basic name extraction, could be improved with NLP
    words = text.strip().split()
    if not words:
        return None
    # Take first word that's not a greeting
    greetings = {"oi", "olá", "ola", "hey", "hi"}
    for word in words:
        if word.lower() not in greetings:
            return word.title()
    return None


def classify_intent(user_text: str) -> BusinessIntent:
    """Classify user intent into business categories."""
    text = user_text.lower()
    if any(k in text for k in ["agendar", "agenda", "marcar", "diagnostico", "reuniao", "reunião", "call", "meeting"]):
        return BusinessIntent.AGENDAR
    if any(k in text for k in ["preço", "preco", "valor", "custa", "orçamento", "orcamento", "budget"]):
        return BusinessIntent.PRECO
    if any(k in text for k in ["suporte", "atendimento", "erro", "problema", "bug", "ajuda tecnica", "assistencia", "suporte tecnico"]):
        return BusinessIntent.SUPORTE
    return BusinessIntent.PERGUNTA_GERAL


def should_handoff(user_text: str, escalation_keywords: Optional[list[str]] = None) -> bool:
    """Heuristic to decide if conversation should handoff to human."""
    text = user_text.lower()
    neg_words = [
        "reclam", "péssimo", "horrível", "cancelar", "raiva", "insatisfeito", "pior", "terrível", "lento", "indignado",
    ]
    human_words = ["humano", "atendente", "pessoa", "falar com", "suporte humano", "atendimento humano"]
    if any(w in text for w in neg_words + human_words):
        return True
    if escalation_keywords and any(k.lower() in text for k in escalation_keywords):
        return True
    return False


def compute_fit_primary(state: State) -> FitPrimario:
    """Primary fit: elegivel if time_vendas >= 3."""
    try:
        if getattr(state, "time_vendas", None) is not None and int(state.time_vendas) >= 3:
            return FitPrimario.ELEGIVEL
    except Exception:
        pass
    return FitPrimario.INELEGIVEL


def step_transition_v2(state: State, user_text: str) -> tuple[State, str, str]:
    """New SDR flow collecting: nome+empresa -> email/phone -> time_vendas -> ferramentas -> dor_principal.

    Returns (state, reply_text, action)
    """
    # 1) Nome completo e empresa
    if not state.nome or not state.sobrenome:
        words = [w for w in user_text.strip().split() if w]
        if words:
            state.nome = state.nome or words[0].title()
            if len(words) > 1:
                state.sobrenome = state.sobrenome or words[-1].title()
        if not state.sobrenome:
            return state, "Obrigado! Poderia me informar seu sobrenome e o nome da empresa?", None
        if not state.empresa:
            full = ((state.nome or "") + " " + (state.sobrenome or "")).strip()
            return state, f"Perfeito, {full}. Qual é o nome da empresa?", None

    if not state.empresa:
        state.empresa = user_text.strip()
        return state, "Pode me passar seu e-mail e celular/WhatsApp? Pode ser um dos dois.", None

    # 2) E-mail e celular (precisa pelo menos um)
    if not state.email and not state.celular:
        txt = user_text.strip()
        if "@" in txt and "." in txt and " " not in txt:
            state.email = txt
        elif any(ch.isdigit() for ch in txt):
            state.celular = txt
        if not state.email and not state.celular:
            return state, "Para prosseguir, preciso de e-mail ou celular/WhatsApp. Pode enviar um deles?", None
        if not state.email:
            return state, "Obrigado! Qual é o seu e-mail?", None
        if not state.celular:
            return state, "Perfeito. Pode compartilhar seu celular/WhatsApp (BR)?", None

    # 3) Tamanho do time de vendas (int)
    if getattr(state, "time_vendas", None) is None:
        digits = ''.join(ch for ch in user_text if ch.isdigit())
        if digits:
            try:
                state.time_vendas = int(digits)
            except Exception:
                state.time_vendas = None
        if state.time_vendas is None:
            return state, "Quantas pessoas estão no time de vendas? (número)", None
        return state, "Obrigado! Quais ferramentas usam hoje? (CRM, automação, mensageria)", None

    # 4) Ferramentas atuais
    if not state.ferramentas:
        state.ferramentas = user_text.strip()
        return state, "Qual dessas descreve melhor sua principal dor? pos_nao_venda, integracao_mkt_vendas, automacao, mensageria ou outro?", None

    # 5) Dor principal (enum)
    if not state.dor_principal:
        value = user_text.strip().lower().replace(" ", "_")
        allowed = {"pos_nao_venda", "integracao_mkt_vendas", "automacao", "mensageria", "outro"}
        state.dor_principal = value if value in allowed else "outro"
        return state, "Perfeito! Obrigado pelas informações. Vou direcionar para nosso especialista.", "handoff"

    return state, "Como posso ajudar?", None


def step_transition(state: State, user_text: str) -> tuple[State, str, str]:
    """Process user input and return updated state, reply text, and next action.
    
    Args:
        state: Current conversation state with user info
        user_text: Text message from user
    
    Returns:
        tuple:
            - Updated State object
            - Reply text to send to user
            - Action to take (handoff, create_lead, schedule, or None)
    """
    # Welcome/initial state
    if not state.nome:
        state.nome = extract_name(user_text)
        if state.nome:
            return state, "Ótimo! Qual é o nome da sua empresa?", None
        return state, "Olá! Para começar, qual é o seu nome?", None
    
    # Get company name
    if not state.empresa:
        state.empresa = user_text
        return state, "Qual é o seu cargo na empresa?", None
    
    # Get role/position
    if not state.cargo:
        state.cargo = user_text
        return state, "Que ferramentas de vendas você usa hoje?", None
    
    # Get current tools
    if not state.ferramentas:
        state.ferramentas = user_text
        return state, "Qual é sua principal dor hoje?", None
    
    # Get main pain point
    if not state.dor_principal:
        state.dor_principal = user_text
        return state, "Obrigado! Um de nossos consultores entrará em contato.", "handoff"
    
    return state, "Como posso ajudar?", None

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
