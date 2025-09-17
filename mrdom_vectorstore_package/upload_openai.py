#!/usr/bin/env python3
import os, argparse, sys
from pathlib import Path
from openai import OpenAI

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="mrdom-knowledge-pt-br")
    ap.add_argument("--path", default="./files")
    ap.add_argument("--assistant-id", default="")
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Defina a variável de ambiente OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = OpenAI()

    # 1) Criar vector store
    vs = client.beta.vector_stores.create(name=args.name)
    print(f"Created vector store: {vs.id}")

    # 2) Fazer upload dos arquivos
    folder = Path(args.path)
    file_ids = []
    for p in folder.glob("*"):
        if not p.is_file():
            continue
        with open(p, "rb") as f:
            uploaded = client.files.create(file=f, purpose="assistants")
            file_ids.append(uploaded.id)
            print(f"Uploaded: {p.name} -> {uploaded.id}")
    # 3) Adicionar arquivos ao vector store
    if file_ids:
        batch = client.beta.vector_stores.file_batches.create(vector_store_id=vs.id, file_ids=file_ids)
        print(f"Batch created: {batch.id}. Status: {batch.status}")

    # 4) Anexar ao assistente, se fornecido
    if args.assistant_id:
        client.beta.assistants.update(args.assistant_id, tool_resources={"file_search": {"vector_store_ids": [vs.id]}})
        print(f"Attached vector store {vs.id} to assistant {args.assistant_id}")

    print("Done.")

if __name__ == "__main__":
    main()
