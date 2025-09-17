from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Iterable

import json
import re

from docx import Document as DocxDocument  # type: ignore
from pypdf import PdfReader  # type: ignore
import tiktoken  # type: ignore


# Use the cl100k_base encoding (compatible with many OpenAI chat models)
ENC = tiktoken.get_encoding("cl100k_base")


def _by_tokens(text: str, max_tokens: int = 350, overlap: int = 60) -> Iterable[str]:
    """Yield token-aware chunks with overlap, avoiding infinite loops.

    - max_tokens: target tokens per chunk
    - overlap: tokens to overlap between consecutive chunks
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be > 0")
    if overlap < 0:
        overlap = 0

    ids = ENC.encode(text or "")
    n = len(ids)
    start = 0
    while start < n:
        end = min(start + max_tokens, n)
        chunk = ENC.decode(ids[start:end])
        yield chunk.strip()

        if end >= n:
            break

        # Ensure forward progress even if overlap is large
        next_start = end - overlap
        if next_start <= start:
            next_start = end
        start = next_start


def load_docx(path: Path) -> List[Dict]:
    doc = DocxDocument(path)
    full = "\n".join(p.text for p in doc.paragraphs if p.text and p.text.strip())
    return [
        {"text": c, "meta": {"source": path.name, "type": "docx"}}
        for c in _by_tokens(full)
        if c
    ]


def load_pdf(path: Path) -> List[Dict]:
    reader = PdfReader(str(path))
    out: List[Dict] = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            for c in _by_tokens(text):
                if not c:
                    continue
                out.append(
                    {
                        "text": c,
                        "meta": {
                            "source": path.name,
                            "page": i + 1,
                            "type": "pdf",
                        },
                    }
                )
    return out


def load_json(path: Path) -> List[Dict]:
    """Load JSON with templates field and chunk string values.

    Expected shape (example):
      { "templates": [ { "id": "...", "whatsapp": { ... }, "email": "..." }, ... ] }
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    chunks: List[Dict] = []
    for tpl in data.get("templates", []) if isinstance(data, dict) else []:
        if not isinstance(tpl, dict):
            continue
        tpl_id = tpl.get("id")
        # Iterate channels/fields
        for ch, val in tpl.items():
            if ch == "id":
                continue
            if isinstance(val, dict):
                for subval in val.values():
                    if isinstance(subval, str) and subval.strip():
                        for c in _by_tokens(subval):
                            chunks.append(
                                {
                                    "text": c,
                                    "meta": {
                                        "source": path.name,
                                        "id": tpl_id,
                                        "channel": ch,
                                        "type": "json",
                                    },
                                }
                            )
            elif isinstance(val, str) and val.strip():
                for c in _by_tokens(val):
                    chunks.append(
                        {
                            "text": c,
                            "meta": {
                                "source": path.name,
                                "id": tpl_id,
                                "channel": ch,
                                "type": "json",
                            },
                        }
                    )
    return chunks


LOADERS = {
    ".pdf": load_pdf,
    ".docx": load_docx,
    ".json": load_json,
    ".jsonl": None,  # will be replaced below
}


def ingest_folder(folder: Path) -> List[Dict]:
    items: List[Dict] = []
    for p in folder.glob("*"):
        if not p.is_file():
            continue
        fn = LOADERS.get(p.suffix.lower())
        if fn:
            items.extend(fn(p))

    # light cleanup
    for it in items:
        it["text"] = re.sub(r"\n{3,}", "\n\n", it.get("text", "")).strip()
    return items


# Add JSONL loader after function definitions to avoid forward ref issues
def _load_jsonl(path: Path) -> List[Dict]:
    out: List[Dict] = []
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                # treat as raw text
                out.append({"text": line, "meta": {"source": path.name, "type": "jsonl"}})
                continue
            text = obj.get("text") if isinstance(obj, dict) else None
            if isinstance(text, str) and text.strip():
                meta = obj.get("metadata", {}) if isinstance(obj, dict) else {}
                if not isinstance(meta, dict):
                    meta = {"source": path.name}
                meta.setdefault("source", path.name)
                meta.setdefault("type", "jsonl")
                out.append({"text": text, "meta": meta})
    except Exception:
        pass
    return out


LOADERS[".jsonl"] = _load_jsonl
