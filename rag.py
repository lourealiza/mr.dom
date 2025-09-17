import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import chromadb  # type: ignore
from chromadb.api.models.Collection import Collection  # type: ignore
from openai import OpenAI  # type: ignore

from chunker import load_documents, chunk_documents


EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_MODEL", os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"))


class OpenAIEmbeddingFunction:
    def __init__(self, model: str = EMBED_MODEL) -> None:
        self.client = OpenAI()
        self.model = model

    def __call__(self, texts: List[str]) -> List[List[float]]:  # chromadb expects this
        # Batch create embeddings
        res = self.client.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in res.data]


@dataclass
class RAGConfig:
    data_dir: str = "raw"
    persist_dir: str = "chroma"
    collection: str = "mrdom_docs"
    top_k: int = 5


class RAG:
    def __init__(self, cfg: RAGConfig = RAGConfig()):
        self.cfg = cfg
        Path(cfg.persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=cfg.persist_dir)
        self.collection: Collection = self.client.get_or_create_collection(
            name=cfg.collection,
            embedding_function=OpenAIEmbeddingFunction(),
            metadata={"hnsw:space": "cosine"},
        )
        self.llm = OpenAI()

    def clear(self) -> None:
        self.client.delete_collection(self.cfg.collection)
        self.collection = self.client.create_collection(
            name=self.cfg.collection,
            embedding_function=OpenAIEmbeddingFunction(),
            metadata={"hnsw:space": "cosine"},
        )

    def ingest(self) -> Dict[str, Any]:
        docs = load_documents(self.cfg.data_dir)
        records = chunk_documents(docs)
        if not records:
            return {"ingested": 0, "message": "No documents found"}

        ids = [r["chunk_id"] for r in records]
        texts = [r["text"] for r in records]
        metadatas = [{"doc_id": r["doc_id"], "source": r["source"]} for r in records]

        # Upsert in batches to avoid large payloads
        batch = 128
        for i in range(0, len(ids), batch):
            self.collection.upsert(
                ids=ids[i : i + batch],
                documents=texts[i : i + batch],
                metadatas=metadatas[i : i + batch],
            )
        return {"ingested": len(ids), "documents": len({r['doc_id'] for r in records})}

    def retrieve(self, query: str, top_k: int | None = None) -> Dict[str, Any]:
        k = top_k or self.cfg.top_k
        res = self.collection.query(query_texts=[query], n_results=k)
        docs: List[str] = res.get("documents", [["No results"]])[0]
        metadatas: List[Dict[str, Any]] = res.get("metadatas", [[{}]])[0]
        ids: List[str] = res.get("ids", [[""]])[0]
        return {
            "chunks": [
                {"id": cid, "text": t, "metadata": m}
                for cid, t, m in zip(ids, docs, metadatas)
            ]
        }

    def answer(self, question: str, top_k: int | None = None) -> Dict[str, Any]:
        retrieved = self.retrieve(question, top_k)
        chunks = retrieved["chunks"]
        context = "\n\n".join(f"[Source: {c['metadata'].get('source','')}]\n{c['text']}" for c in chunks)

        system = (
            "You are a helpful assistant. Answer the user's question using the provided context. "
            "If the answer is not in the context, say you don't know."
        )
        user = f"Question: {question}\n\nContext:\n{context}"

        # Use Chat Completions for broad model compatibility
        chat = self.llm.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.1,
        )
        answer = chat.choices[0].message.content or ""

        return {
            "answer": answer,
            "sources": [c["metadata"].get("source", "") for c in chunks],
            "chunks": chunks,
        }


def _ensure_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Define it in your environment or .env")


def main():
    import argparse

    _ensure_api_key()
    parser = argparse.ArgumentParser(description="Simple RAG over local data directory")
    parser.add_argument("command", choices=["ingest", "ask", "clear", "retrieve"]) 
    parser.add_argument("query", nargs="?", help="Question for 'ask' or 'retrieve'")
    parser.add_argument("--data", dest="data_dir", default="data")
    parser.add_argument("--persist", dest="persist_dir", default=".chroma")
    parser.add_argument("--k", dest="top_k", type=int, default=5)
    args = parser.parse_args()

    rag = RAG(RAGConfig(data_dir=args.data_dir, persist_dir=args.persist_dir, top_k=args.top_k))

    if args.command == "clear":
        rag.clear()
        print("Index cleared.")
    elif args.command == "ingest":
        res = rag.ingest()
        print(res)
    elif args.command == "retrieve":
        if not args.query:
            raise SystemExit("Provide a query for retrieve")
        res = rag.retrieve(args.query, args.top_k)
        print(res)
    elif args.command == "ask":
        if not args.query:
            raise SystemExit("Provide a question for ask")
        res = rag.answer(args.query, args.top_k)
        print(res["answer"])  # concise
        print("\nSources:")
        for s in sorted(set(res["sources"])):
            print(" - ", s)


if __name__ == "__main__":
    main()
