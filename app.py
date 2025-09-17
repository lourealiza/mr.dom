import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv  # type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag import RAG, RAGConfig, _ensure_api_key


# Load .env from project root if present
load_dotenv(Path(__file__).parent / ".env")

app = FastAPI(title="MrDom RAG API", version="0.1.0")


class QueryIn(BaseModel):
    question: str
    top_k: int | None = None


def _rag() -> RAG:
    cfg = RAGConfig(
        data_dir=os.getenv("RAG_DATA_DIR", "raw"),
        persist_dir=os.getenv("RAG_PERSIST_DIR", "chroma"),
        top_k=int(os.getenv("RAG_TOP_K", "5")),
    )
    return RAG(cfg)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True}


@app.post("/ingest")
def ingest() -> Dict[str, Any]:
    try:
        _ensure_api_key()
        rag = _rag()
        return rag.ingest()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query(payload: QueryIn) -> Dict[str, Any]:
    try:
        _ensure_api_key()
        rag = _rag()
        if not payload.question:
            raise HTTPException(status_code=400, detail="question is required")
        return rag.answer(payload.question, payload.top_k)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

