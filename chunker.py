import os
from pathlib import Path
from typing import Iterable, List, Dict, Any

from docx import Document as DocxDocument  # type: ignore
from pypdf import PdfReader  # type: ignore
import tiktoken  # type: ignore
import json


TextDoc = Dict[str, str]


def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for p in reader.pages:
        try:
            pages.append(p.extract_text() or "")
        except Exception:
            # Best-effort extraction
            pass
    return "\n\n".join(pages)


def _read_docx(path: Path) -> str:
    doc = DocxDocument(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def _extract_strings_from_json(obj: Any) -> List[str]:
    out: List[str] = []
    if isinstance(obj, str):
        s = obj.strip()
        if s:
            out.append(s)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(_extract_strings_from_json(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_extract_strings_from_json(v))
    return out


def _read_json(path: Path) -> str:
    # Supports .json (single file) and .jsonl (one json per line)
    try:
        if path.suffix.lower() == ".jsonl":
            texts: List[str] = []
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    texts.append(line)
                    continue
                strings = _extract_strings_from_json(obj)
                if strings:
                    texts.append("\n".join(strings))
            return "\n\n".join(texts)
        else:
            obj = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
            strings = _extract_strings_from_json(obj)
            if strings:
                return "\n".join(strings)
            # Fallback to raw content
            return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return path.read_text(encoding="utf-8", errors="ignore")


def load_documents(data_dir: str | os.PathLike) -> List[TextDoc]:
    """Load .txt, .md, .pdf, .docx files into a list of {id, text, source}."""
    base = Path(data_dir)
    docs: List[TextDoc] = []
    if not base.exists():
        return docs

    for path in base.rglob("*"):
        if not path.is_file():
            continue

        ext = path.suffix.lower()
        text = ""
        try:
            if ext in {".txt", ".md"}:
                text = _read_txt(path)
            elif ext == ".pdf":
                text = _read_pdf(path)
            elif ext in {".docx"}:
                text = _read_docx(path)
            elif ext in {".json", ".jsonl"}:
                text = _read_json(path)
        except Exception:
            # Skip unreadable files
            text = ""

        text = (text or "").strip()
        if not text:
            continue
        docs.append({
            "id": str(path.relative_to(base)),
            "text": text,
            "source": str(path),
        })
    return docs


def chunk_text(
    text: str,
    *,
    chunk_size_tokens: int = 400,
    chunk_overlap_tokens: int = 80,
    encoding_name: str = "cl100k_base",
) -> List[str]:
    """Token-aware chunking using tiktoken.

    Returns a list of text chunks approximately equal to chunk_size_tokens.
    """
    enc = tiktoken.get_encoding(encoding_name)
    tokens = enc.encode(text)
    chunks: List[str] = []

    start = 0
    while start < len(tokens):
        end = min(start + chunk_size_tokens, len(tokens))
        decoded = enc.decode(tokens[start:end])
        chunks.append(decoded)
        if end == len(tokens):
            break
        start = end - chunk_overlap_tokens
        if start < 0:
            start = 0
    return chunks


def chunk_documents(docs: Iterable[TextDoc], **kwargs) -> List[Dict[str, str]]:
    """Expand documents into chunked records with metadata."""
    records: List[Dict[str, str]] = []
    for d in docs:
        parts = chunk_text(d["text"], **kwargs)
        for i, part in enumerate(parts):
            records.append({
                "doc_id": d["id"],
                "chunk_id": f"{d['id']}::chunk-{i}",
                "text": part,
                "source": d.get("source", d["id"]),
            })
    return records
