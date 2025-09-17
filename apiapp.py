import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv  # type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI  # type: ignore

# Load environment from repo root before importing apirag
_repo_root = Path(__file__).resolve().parent
load_dotenv(_repo_root / ".env")
load_dotenv(_repo_root / "config.env")

from apirag import retrieve

app = FastAPI(title="Mr. DOM RAG API")


SYSTEM_PROMPT = (
    "Você é o Agente SDR IA do DOM360.\n"
    "Responda em PT-BR, tom consultivo, claro e direto.\n"
    "Use APENAS os fatos do CONTEXTO abaixo.\n"
    "Se algo não estiver no contexto, diga que não está nos materiais oficiais e ofereça encaminhar ao especialista.\n\n"
    "Pilares a reforçar quando fizer sentido: CRM completo, Automação de Marketing, Mensageria Omnichannel (WhatsApp, etc.), "
    "BI (Power BI), Método 7 Passos, Implementação guiada, Suporte ilimitado, Evolução contínua.\n"
    "Nunca prometa números específicos de resultado."
)


class Ask(BaseModel):
    question: str = Field(..., description="Pergunta do usuário")
    k: int = Field(6, ge=1, le=20)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True}


@app.post("/ragask")
async def rag_ask(body: Ask) -> Dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada")

    hits = retrieve(body.question, k=body.k)
    if not hits:
        return {"answer": "Não encontrei informações relevantes no contexto.", "sources": []}

    context_blocks: List[str] = []
    for i, (doc, meta) in enumerate(hits, start=1):
        tag = f"{meta.get('source','')}"
        if "page" in meta:
            tag += f" p.{meta['page']}"
        context_blocks.append(f"[{i}] ({tag})\n{doc}")
    context = "\n\n".join(context_blocks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Pergunta: {body.question}\n\nCONTEXTO:\n{context}\n\n"
                "Responda de forma objetiva, cite 2-4 pontos mais fortes e conclua com um CTA curto quando fizer sentido."
            ),
        },
    ]

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(model=model, temperature=0.3, messages=messages)
    answer = (resp.choices[0].message.content or "").strip()

    sources = [{"source": h[1].get("source"), "page": h[1].get("page")} for h in hits]
    return {"answer": answer, "sources": sources}
