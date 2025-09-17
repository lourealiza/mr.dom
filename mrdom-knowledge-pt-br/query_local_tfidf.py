#!/usr/bin/env python3
import json, sys
from pathlib import Path
import joblib
from sklearn.metrics.pairwise import cosine_similarity

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_local_tfidf.py \"your query here\"")
        return
    query = sys.argv[1]
    pkg = Path(__file__).resolve().parent
    model = joblib.load(pkg / "mrdom_tfidf.joblib")
    mapping = json.loads((pkg / "mrdom_index_mapping.json").read_text(encoding="utf-8"))
    vec = model["vectorizer"].transform([query])
    sims = cosine_similarity(vec, model["matrix"]).ravel()
    topk = sims.argsort()[::-1][:5]
    for rank, idx in enumerate(topk, start=1):
        meta = mapping["metadatas"][idx]
        score = float(sims[idx])
        print(f"#{rank} score={score:.4f} file={meta['filename']} chunk={meta['chunk_index']} len={meta['chunk_char_len']}")

if __name__ == "__main__":
    main()
