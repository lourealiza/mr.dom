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
    dor_principal: Literal["pos_nao_venda", "integracao_mkt_vendas", "ferramentas"]
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
