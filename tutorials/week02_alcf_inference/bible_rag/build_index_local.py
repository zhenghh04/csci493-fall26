#!/usr/bin/env python3
"""
LOCAL embedding index for the whole Bible -- no ALCF embedding endpoint needed.

The ALCF inference gateway does not currently serve an embedding model, so the
semantic retriever ("meaning as geometry", Slide 6) is built here with a small
open HuggingFace model that runs ON YOUR OWN MACHINE (CPU is fine). It embeds
all 31,100 KJV verses ONCE and caches them to bible_index_local.npz;
ask_bible_local.py then auto-uses it.

Only the RETRIEVAL embeddings move local. The ANSWER step still uses the small
ALCF chat model, so the with-RAG vs without-RAG lesson is unchanged.

Setup (one time, before class):
  pip install sentence-transformers          # pulls torch; run once
  python get_bible.py                        # if you have not already
  python build_index_local.py                # a few min on CPU, seconds on GPU
  python ask_bible_local.py "Who was Boaz's father?"

Pick a different model without editing the file:
  LOCAL_EMBED_MODEL=BAAI/bge-small-en-v1.5 python build_index_local.py
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KJV = os.path.join(HERE, "kjv.json")
INDEX = os.path.join(HERE, "bible_index_local.npz")

# Small, fast, widely used sentence-embedding model: 384-dim, ~90 MB, CPU-friendly.
# Alternatives: "BAAI/bge-small-en-v1.5", "nomic-ai/nomic-embed-text-v1.5".
EMBED_MODEL = os.environ.get("LOCAL_EMBED_MODEL",
                             "sentence-transformers/all-MiniLM-L6-v2")
BATCH = 256


def main():
    if not os.path.exists(KJV):
        sys.exit("kjv.json not found. Run:  python get_bible.py")
    with open(KJV, encoding="utf-8") as f:
        verses = json.load(f)

    # Imported here (not at top) so `python -c "import build_index_local"` and
    # the offline tests do not require torch to be installed.
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(EMBED_MODEL)   # auto-uses CUDA/MPS if present
    print(f"Embedding {len(verses):,} verses with {EMBED_MODEL} "
          f"(device={model.device}) ...")

    emb = model.encode(
        [v["text"] for v in verses],
        batch_size=BATCH,
        convert_to_numpy=True,
        normalize_embeddings=True,     # rows L2-normalized -> dot == cosine
        show_progress_bar=True,
    ).astype("float32")

    # float16 halves the file; precision loss is negligible for nearest-neighbor.
    np.savez_compressed(INDEX, emb=emb.astype("float16"),
                        model=EMBED_MODEL, n=len(verses))
    print(f"Saved {emb.shape} embeddings -> {INDEX}")


if __name__ == "__main__":
    main()
