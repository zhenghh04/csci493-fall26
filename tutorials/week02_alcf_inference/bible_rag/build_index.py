#!/usr/bin/env python3
"""
OPTIONAL (advanced): pre-compute embeddings for the whole Bible.

BM25 (in ask_bible.py) works out of the box and needs no build step. This adds
the SEMANTIC retriever from Slide 5 -- "meaning as geometry" -- so questions
phrased differently from the verse ("Boaz's father" vs KJV's "Salmon begat
Boaz") still find the right text. It embeds all 31,100 verses ONCE via the ALCF
endpoint and caches them to bible_index.npz; ask_bible.py then auto-uses it.

Run this BEFORE class (it makes ~120 embedding requests, a few minutes) -- not
live in front of students:
  python get_bible.py            # if you have not already
  python inference_auth_token.py authenticate
  python build_index.py
  python ask_bible.py "Who was Boaz's father?"    # now uses embeddings
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KJV = os.path.join(HERE, "kjv.json")
INDEX = os.path.join(HERE, "bible_index.npz")

BASE_URL = "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1"
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"   # confirm via list-endpoints
BATCH = 256


def embed_all(texts, client):
    """Embed every verse in batches; return an (N, dim) float32 array."""
    vecs = []
    for start in range(0, len(texts), BATCH):
        batch = texts[start:start + BATCH]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        vecs.extend(d.embedding for d in resp.data)
        print(f"  embedded {min(start + BATCH, len(texts)):,}/{len(texts):,}", end="\r")
    print()
    return np.asarray(vecs, dtype="float32")


def normalize(emb):
    """L2-normalize rows so a dot product == cosine similarity at query time."""
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    return emb / (norms + 1e-9)


def main():
    if not os.path.exists(KJV):
        sys.exit("kjv.json not found. Run:  python get_bible.py")
    with open(KJV, encoding="utf-8") as f:
        verses = json.load(f)

    from openai import OpenAI
    from inference_auth_token import get_access_token
    client = OpenAI(api_key=get_access_token(), base_url=BASE_URL)
    print(f"Embedding {len(verses):,} verses with {EMBED_MODEL} ...")
    emb = normalize(embed_all([v["text"] for v in verses], client))

    # float16 halves the file (~48 MB); precision loss is negligible for search.
    np.savez_compressed(INDEX, emb=emb.astype("float16"),
                        model=EMBED_MODEL, n=len(verses))
    print(f"Saved {emb.shape} embeddings -> {INDEX}")


if __name__ == "__main__":
    main()
