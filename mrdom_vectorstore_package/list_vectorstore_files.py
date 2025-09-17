#!/usr/bin/env python3
import os, argparse, sys
from openai import OpenAI

# Uso: python list_vectorstore_files.py --vector-store-id <ID>

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vector-store-id", required=True, help="ID do vector store (ex: vs_xxx)")
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Defina a variável de ambiente OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = OpenAI()
    vs_id = args.vector_store_id

    # Listar arquivos do vector store
    print(f"Arquivos do vector store {vs_id}:")
    files = client.beta.vector_stores.files.list(vector_store_id=vs_id)
    if not files.data:
        print("Nenhum arquivo encontrado.")
        return
    for f in files.data:
        name = getattr(f, 'display_name', None) or getattr(f, 'filename', None) or '(sem nome)'
        print(f"- {f.id}: {name} | status: {f.status}")

if __name__ == "__main__":
    main()
