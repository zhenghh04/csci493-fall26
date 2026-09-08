#!/usr/bin/env python3
"""
Ask the whole Bible a question -- WITHOUT RAG vs WITH RAG -- with a LOCAL
embedding model for retrieval.

Same lesson as ask_bible.py:
  * WITHOUT RAG  the small ALCF model answers from memory -- it paraphrases,
    misquotes, invents chapter/verse, and "quotes" verses that do not exist.
  * WITH RAG     we RETRIEVE the most relevant verses from all 31,100 KJV
    verses, then ask the model to answer using ONLY those verses -- so it
    quotes exactly, cites the reference, and refuses when the fact is not there.

WHAT IS DIFFERENT FROM ask_bible.py:
  The ALCF inference gateway does not currently serve an embedding model, so the
  SEMANTIC retriever runs a small open HuggingFace model ON YOUR OWN MACHINE
  (sentence-transformers). The ANSWER step still uses the small ALCF chat model.
  BM25 lexical search remains the zero-dependency default.

Setup:
  1. python get_bible.py            # once: downloads kjv.json (no token needed)
  2. pip install openai sentence-transformers
  3. python inference_auth_token.py authenticate    # browser login, ~48h token
  (optional, faster) python build_index_local.py    # cache embeddings once

Run:
  python ask_bible_local.py                    # curated set, BM25 (no local deps)
  python ask_bible_local.py --embed "Who was Boaz's father?"   # local embeddings
  python ask_bible_local.py --retrieve-only --embed "still waters"  # no token
"""

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KJV = os.path.join(HERE, "kjv.json")
INDEX = os.path.join(HERE, "bible_index_local.npz")

BASE_URL = "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1"
# A SMALL chat model on purpose -- so "without RAG" fails visibly. Confirm the ID
# against `list-endpoints`; the served set changes over time.
CHAT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# Local HuggingFace embedding model (runs on your machine, not ALCF).
EMBED_MODEL = os.environ.get("LOCAL_EMBED_MODEL",
                             "sentence-transformers/all-MiniLM-L6-v2")

RAG_SYSTEM = (
    "You are a careful Bible study assistant. Answer using ONLY the verses "
    "provided below. Quote the exact wording and cite the reference(s) in "
    "brackets, e.g. [John 3:16]. If the answer is not in the provided verses, "
    "reply exactly: 'Not found in the provided verses.'"
)
PLAIN_SYSTEM = "You are a helpful Bible study assistant. Answer the question."


# --------------------------------------------------------------------------
# Corpus + BM25 index (pure Python -- no numpy, no network, no torch).
# --------------------------------------------------------------------------
def load_verses():
    if not os.path.exists(KJV):
        sys.exit("kjv.json not found. Run:  python get_bible.py")
    with open(KJV, encoding="utf-8") as f:
        return json.load(f)


def tokenize(s):
    return re.findall(r"[a-z0-9]+", s.lower())


class BM25:
    """Compact BM25 over an inverted index -- instant across 31k verses."""

    def __init__(self, verses, k1=1.5, b=0.75):
        self.verses, self.k1, self.b = verses, k1, b
        self.postings = {}          # term -> list of (doc_id, term_freq)
        self.doc_len = [0] * len(verses)
        for i, v in enumerate(verses):
            tf = {}
            # Index the reference too, weighted, so citation-style questions
            # ("what does Micah 6:8 say") pull the EXACT verse to the top.
            ref_boost = 4
            for tok in tokenize(v["ref"]) * ref_boost + tokenize(v["text"]):
                tf[tok] = tf.get(tok, 0) + 1
            self.doc_len[i] = sum(tf.values())
            for tok, c in tf.items():
                self.postings.setdefault(tok, []).append((i, c))
        self.N = len(verses)
        self.avgdl = (sum(self.doc_len) / self.N) if self.N else 0.0

    def _idf(self, term):
        df = len(self.postings.get(term, ()))
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def search(self, query, k=4):
        scores = {}
        for term in set(tokenize(query)):
            idf = self._idf(term)
            for doc_id, freq in self.postings.get(term, ()):
                dl = self.doc_len[doc_id]
                denom = freq + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                scores[doc_id] = scores.get(doc_id, 0.0) + idf * freq * (self.k1 + 1) / denom
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
        return [(self.verses[i], s) for i, s in top]


# --------------------------------------------------------------------------
# Local embedding backend (HuggingFace sentence-transformers, runs on-device).
# Needs no ALCF token -- so --retrieve-only --embed works fully offline.
# --------------------------------------------------------------------------
class LocalEmbedIndex:
    def __init__(self, verses, model_name=EMBED_MODEL):
        import numpy as np
        from sentence_transformers import SentenceTransformer
        self.np, self.verses = np, verses
        self.model = SentenceTransformer(model_name)     # auto CUDA/MPS/CPU

        if os.path.exists(INDEX):
            data = np.load(INDEX, allow_pickle=True)
            self.emb = data["emb"].astype("float32")     # (N, dim), L2-normalized
            if self.emb.shape[0] != len(verses):
                sys.exit("bible_index_local.npz is stale -- rerun build_index_local.py")
        else:
            # No cache: embed the whole Bible now (one-time; a few min on CPU).
            print(f"No cache found -- embedding {len(verses):,} verses locally "
                  f"(run build_index_local.py to cache this) ...")
            self.emb = self.model.encode(
                [v["text"] for v in verses], batch_size=256,
                convert_to_numpy=True, normalize_embeddings=True,
                show_progress_bar=True).astype("float32")

    def search(self, query, k=4):
        q = self.model.encode([query], convert_to_numpy=True,
                              normalize_embeddings=True)[0].astype("float32")
        sims = self.emb @ q                              # one matvec = every verse
        idx = self.np.argsort(-sims)[:k]
        return [(self.verses[i], float(sims[i])) for i in idx]


# --------------------------------------------------------------------------
# The chat model (created lazily so retrieval-only mode needs no token).
# --------------------------------------------------------------------------
_client = None


def get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        from inference_auth_token import get_access_token
        _client = OpenAI(api_key=get_access_token(), base_url=BASE_URL)
    return _client


def ask_plain(question):
    """WITHOUT RAG: the small model answers from parametric memory alone."""
    r = get_client().chat.completions.create(
        model=CHAT_MODEL, temperature=0,
        messages=[{"role": "system", "content": PLAIN_SYSTEM},
                  {"role": "user", "content": question}],
    )
    return r.choices[0].message.content.strip()


def ask_rag(question, retriever, k=4):
    """WITH RAG: retrieve from the whole KJV, then answer grounded in it."""
    hits = retriever.search(question, k=k)
    context = "\n".join(f"[{v['ref']}] {v['text']}" for v, _ in hits)
    r = get_client().chat.completions.create(
        model=CHAT_MODEL, temperature=0,
        messages=[{"role": "system", "content": RAG_SYSTEM},
                  {"role": "user", "content": f"Verses:\n{context}\n\nQuestion: {question}"}],
    )
    return r.choices[0].message.content.strip(), hits


def compare(question, retriever, gold=None, k=6):
    print("=" * 78)
    print(f"Q: {question}")
    print("=" * 78)

    print("\n-- WITHOUT RAG (small model, from memory) " + "-" * 34)
    try:
        print(ask_plain(question))
    except Exception as e:
        print(f"[model call failed: {e}]")

    print("\n-- WITH RAG (retrieved from all 31,100 KJV verses) " + "-" * 26)
    answer, hits = ask_rag(question, retriever, k=k)
    retrieved = [v["ref"] for v, _ in hits]
    print("retrieved: " + ", ".join(f"{v['ref']} ({s:.2f})" for v, s in hits))
    if gold:
        mark = "OK" if any(gold == r for r in retrieved) else "MISS"
        print(f"gold verse {gold}: {mark} in retrieved set")
    print()
    print(answer)
    print()


# Curated so the WITHOUT-RAG failure is visible while retrieval can still find
# the verse: exact wording, a citation, a phrase, a number, and a verse that
# does NOT exist (which RAG must refuse instead of inventing).
QUESTIONS = [
    ("What are the exact words of Micah 6:8?", "Micah 6:8"),
    ("Quote John 3:16 exactly.", "John 3:16"),
    ("What does Genesis 5:27 say about how long Methuselah lived?", "Genesis 5:27"),
    ("Where does the Bible describe God as a 'still small voice'?", "1 Kings 19:12"),
    ("What does Hezekiah 3:16 say?", None),   # no such book/verse -> must refuse
]


def build_retriever(force_embed=False):
    verses = load_verses()
    # Local embeddings need no token, so use them whenever asked or cached --
    # independent of whether the answer step will call the model.
    if force_embed or os.path.exists(INDEX):
        try:
            r = LocalEmbedIndex(verses)
            print(f"Retriever: local embeddings ({EMBED_MODEL}), {len(verses):,} verses.\n")
            return r
        except SystemExit:
            raise
        except Exception as e:
            print(f"[local embedding backend unavailable: {e}] -- using BM25.\n")
    print(f"Retriever: BM25 lexical, {len(verses):,} verses.\n")
    return BM25(verses)


def main():
    args = list(sys.argv[1:])
    retrieve_only = "--retrieve-only" in args
    force_embed = "--embed" in args
    args = [a for a in args if not a.startswith("--")]
    question = " ".join(args) if args else None

    retriever = build_retriever(force_embed=force_embed)

    if retrieve_only:
        q = question or "a still small voice"
        print(f"Q: {q}\nTop verses:")
        for v, s in retriever.search(q, k=6):
            print(f"  {s:6.3f}  [{v['ref']}] {v['text']}")
        return

    if question:
        compare(question, retriever)
    else:
        for q, gold in QUESTIONS:
            compare(q, retriever, gold=gold)


if __name__ == "__main__":
    main()
