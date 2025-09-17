import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

import chromadb  # type: ignore
from chromadb.utils import embedding_functions  # type: ignore
from dotenv import load_dotenv  # type: ignore

from apichunker import ingest_folder


load_dotenv()


def _resolve_dir(preferred: Path, fallback: Path) -> Path:
    if preferred.exists():
        return preferred
    if fallback.exists():
        return fallback
    # Ensure preferred by default
    preferred.mkdir(parents=True, exist_ok=True)
    return preferred


# Resolve raw and chroma directories with flexibility:
# - Env vars RAW_PATH / CHROMA_PATH have priority
# - If not set, prefer top-level 'raw/' and 'chroma/'
# - Fallback to 'data/raw' and 'data/chroma'
_repo_root = Path(__file__).resolve().parent

def _first_existing(*paths: Path) -> Path | None:
    for p in paths:
        if p and p.exists():
            return p
    return None

_raw_env = os.getenv("RAW_PATH")
_chroma_env = os.getenv("CHROMA_PATH")

_raw_default = _first_existing(
    _repo_root / "raw",
    _repo_root / "mrdom-knowledge-pt-br",
    _repo_root / "data" / "raw",
)
_chroma_default = _first_existing(
    _repo_root / "chroma",
    _repo_root / "data" / "chroma",
)

RAW_PATH = Path(_raw_env) if _raw_env else (_raw_default or _resolve_dir(_repo_root / "raw", _repo_root / "data" / "raw"))
CHROMA_PATH = Path(_chroma_env) if _chroma_env else (_chroma_default or _resolve_dir(_repo_root / "chroma", _repo_root / "data" / "chroma"))

client = chromadb.PersistentClient(path=str(CHROMA_PATH))

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
)


def _get_collection():
    return client.get_or_create_collection(
        name=os.getenv("CHROMA_COLLECTION", "mrdom_knowledge"),
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"},
    )


COLL = _get_collection()


def rebuild_index() -> int:
    """Rebuild the vector index from RAW_PATH. Returns total chunks ingested."""
    coll_name = os.getenv("CHROMA_COLLECTION", "mrdom_knowledge")
    try:
        client.delete_collection(coll_name)
    except Exception:
        pass
    coll = client.get_or_create_collection(name=coll_name, embedding_function=openai_ef)

    docs = ingest_folder(Path(RAW_PATH))
    ids: List[str] = []
    texts: List[str] = []
    metas: List[Dict[str, Any]] = []
    for i, d in enumerate(docs):
        ids.append(f"doc-{i}")
        texts.append(d["text"])
        metas.append(d["meta"]) 

    if texts:
        # upsert in batches
        batch = 128
        for j in range(0, len(texts), batch):
            coll.add(
                ids=ids[j : j + batch],
                documents=texts[j : j + batch],
                metadatas=metas[j : j + batch],
            )
    return len(texts)


def retrieve(query: str, k: int = 6) -> List[Tuple[str, Dict[str, Any]]]:
    res = COLL.query(query_texts=[query], n_results=k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return list(zip(docs, metas))

if __name__ == "__main__":
    total = rebuild_index()
    print(f"Ingeridos {total} chunks.")
