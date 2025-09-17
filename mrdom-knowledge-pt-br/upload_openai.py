#!/usr/bin/env python3
import os, argparse, time, sys
from pathlib import Path

# NOTE: Requires openai>=1.0.0
try:
    from openai import OpenAI
except Exception:
    print("Please install: pip install --upgrade openai", file=sys.stderr)
    sys.exit(1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="mrdom-knowledge-pt-br")
    ap.add_argument("--path", default="./files")
    ap.add_argument("--assistant-id", default="")
    args = ap.parse_args()

    client = OpenAI()

    # 1) Create vector store
    vs = client.beta.vector_stores.create(name=args.name)
    print(f"Created vector store: {vs.id}")

    # 2) Upload all files
    folder = Path(args.path)
    file_ids = []
    for p in folder.glob("*"):
        if not p.is_file():
            continue
        with open(p, "rb") as f:
            uploaded = client.files.create(file=f, purpose="assistants")
            file_ids.append(uploaded.id)
            print(f"Uploaded: {p.name} -> {uploaded.id}")
    # 3) Add files to vector store (batch)
    if file_ids:
        batch = client.beta.vector_stores.file_batches.create(vector_store_id=vs.id, file_ids=file_ids)
        print(f"Batch created: {batch.id}. Status: {batch.status}")

    # 4) Optionally attach to an Assistant
    if args.assistant_id:
        client.beta.assistants.update(args.assistant_id, tool_resources={"file_search": {"vector_store_ids": [vs.id]}})
        print(f"Attached vector store {vs.id} to assistant {args.assistant_id}")

    print("Done.")

if __name__ == "__main__":
    main()
