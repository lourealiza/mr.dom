from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from ..domain.bot_logic import BotLogic


class PreviewRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    dry_run: Optional[bool] = False


class PreviewResponse(BaseModel):
    ok: bool
    reply: str
    used_openai: bool


router = APIRouter()


@router.post("/assistant/preview", response_model=PreviewResponse)
async def assistant_preview(req: PreviewRequest) -> PreviewResponse:
    """Lightweight preview endpoint to exercise assistant responses.

    - When `dry_run=true`, generates a deterministic fallback reply without calling OpenAI.
    - Otherwise, leverages BotLogic/OpenAI to generate a response.
    """
    try:
        bot = BotLogic()

        if req.dry_run:
            # Deterministic fallback reply using internal logic only
            reply = (
                "Obrigado pela sua mensagem! Nosso assistente está em modo de pré-visualização. "
                "Compartilhe mais detalhes e, em produção, responderemos com base no contexto."
            )
            return PreviewResponse(ok=True, reply=reply, used_openai=False)

        # Use OpenAI-backed generation with optional context
        analysis = await bot.analyze_message(req.message)
        reply = await bot.generate_response(analysis)
        return PreviewResponse(ok=True, reply=reply, used_openai=True)

    except Exception as e:
        # Ensure consistent error surface
        raise HTTPException(status_code=500, detail=str(e))

