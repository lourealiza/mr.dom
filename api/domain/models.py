# api/models.py
from datetime import datetime
import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class QualifyPayload(BaseModel):
    # Config: permite criar a partir de objetos e garante serialização limpa
    model_config = ConfigDict(from_attributes=True)

    nome: str
    sobrenome: str
    empresa: str
    cargo: str
    email: EmailStr
    celular: str
    time_vendas: int = Field(ge=1)
    ferramentas: str
    dor_principal: Literal[
        "pos_nao_venda",
        "integracao_mkt_vendas",
        "automacao",
        "mensageria",
        "outro",
    ]
    # Use datetime para validar ISO 8601 e timezone (ex.: 2025-09-04T14:30:00-03:00)
    horario1: datetime
    horario2: datetime

    # --- Validadores ---
    @field_validator("celular")
    @classmethod
    def validar_celular(cls, v: str) -> str:
        # aceita formatos como +55 11 99999-9999 ou 5511999999999
        digits = re.sub(r"\D", "", v)
        if len(digits) < 10:
            raise ValueError("celular inválido: informe DDD/DDD e apenas números (+DD opcional).")
        return v

    @field_validator("horario1", "horario2")
    @classmethod
    def exigir_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError("horário deve incluir timezone (ex.: -03:00 para America/Sao_Paulo).")
        return v


class ChatInput(BaseModel):
    message: str
    # evita default mutável com Field(default_factory=dict)
    context: dict = Field(default_factory=dict)


class State(BaseModel):
    """Conversational state stored in Chatwoot custom_attributes.

    Only include the fields that are read/written by the bot:
    """
    nome: str | None = None
    sobrenome: str | None = None
    empresa: str | None = None
    cargo: str | None = None
    email: EmailStr | None = None
    celular: str | None = None
    time_vendas: int | None = None
    horario1: datetime | None = None
    horario2: datetime | None = None
    ferramentas: str | None = None
    dor_principal: str | None = None

    model_config = ConfigDict(from_attributes=True)


# --- Additional simple models/enums used by bot_logic.py ---
from enum import Enum
from typing import Optional, Dict, Any


class IntentType(str, Enum):
    UNKNOWN = "unknown"
    GREETING = "greeting"
    QUESTION = "question"
    INTEREST = "interest"
    COMPLAINT = "complaint"


class BusinessIntent(str, Enum):
    AGENDAR = "agendar"
    PRECO = "preco"
    SUPORTE = "suporte"
    PERGUNTA_GERAL = "pergunta_geral"


class FitPrimario(str, Enum):
    ELEGIVEL = "elegivel"
    INELEGIVEL = "inelegivel"


class ActionType(str, Enum):
    NO_ACTION = "no_action"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    SEND_AUTOMATED_RESPONSE = "send_automated_response"
    TRIGGER_N8N_WORKFLOW = "trigger_n8n_workflow"
    SCHEDULE_FOLLOW_UP = "schedule_follow_up"


class InterestLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MessageAnalysis(BaseModel):
    intent: IntentType = IntentType.UNKNOWN
    interest_level: InterestLevel = InterestLevel.LOW
    objection_type: Optional[str] = None
    next_steps: str = ""
    urgency: UrgencyLevel = UrgencyLevel.LOW
    confidence: float = 0.5
    extracted_info: Optional[Dict[str, Any]] = None


class LeadQualification(BaseModel):
    qualification_score: int = 50
    budget_indication: str = "unknown"
    authority_level: str = "unknown"
    need_level: str = "unknown"
    timeline: str = "unknown"
    next_best_action: str = "manual_review"
    risk_factors: list = Field(default_factory=list)
    opportunity_size: str = "unknown"


class AgentBotResponse(BaseModel):
    text: str
    action: Optional[str] = None


class ConversationContext(BaseModel):
    last_seen: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class BotConfiguration(BaseModel):
    welcome_message: str = ""
    escalation_keywords: list = Field(default_factory=list)
    auto_response_enabled: bool = True
    qualification_questions: list = Field(default_factory=list)
    business_hours: dict = Field(default_factory=dict)
    timezone: str = "UTC"
