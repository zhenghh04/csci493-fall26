#!/usr/bin/env python3
"""
Week 2 lab — the smallest possible RAG (Retrieval-Augmented Generation).

RAG = three steps, all against the SAME OpenAI-compatible ALCF client:
  1. INDEX    — embed each passage into a vector (meaning as geometry).
  2. RETRIEVE — embed the question, find the nearest passages by cosine similarity.
  3. GROUND   — answer using ONLY those passages (the cure for hallucination).

This is the shape of every "chat with your documents" system; Week 4 just swaps
this six-verse list for a real corpus and a real vector database.

Before running:
  1. pip install openai
  2. python inference_auth_token.py authenticate      # browser login, ~48h token
  3. (optional) list served models and set the model IDs below to current ones:
       tok=$(python inference_auth_token.py get_access_token)
       curl -s https://inference-api.alcf.anl.gov/resource_server/list-endpoints \
         -H "Authorization: Bearer $tok"

Run:
  python 02_simple_rag.py
"""

import math

from openai import OpenAI
from inference_auth_token import get_access_token

BASE_URL = "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1"

# Confirm both IDs against `list-endpoints`; the served set changes over time.
CHAT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"

client = OpenAI(api_key=get_access_token(), base_url=BASE_URL)

# A tiny "library" — six passages on clearly different themes.
CORPUS = [
    {"ref": "Romans 7:24-25",
     "text": "Wretched man that I am! Who will deliver me from this body of death? "
             "Thanks be to God through Jesus Christ our Lord!"},
    {"ref": "Psalm 23:1-2",
     "text": "The Lord is my shepherd; I shall not want. He makes me lie down in "
             "green pastures. He leads me beside still waters."},
    {"ref": "Luke 15:4 (the lost sheep)",
     "text": "What man of you, having a hundred sheep, if he has lost one of them, "
             "does not leave the ninety-nine and go after the one that is lost?"},
    {"ref": "1 Corinthians 13:4",
     "text": "Love is patient and kind; love does not envy or boast; it is not "
             "arrogant or rude."},
    {"ref": "Micah 6:8",
     "text": "What does the Lord require of you but to do justice, to love kindness, "
             "and to walk humbly with your God?"},
    {"ref": "Genesis 1:1",
     "text": "In the beginning, God created the heavens and the earth."},
]

RAG_SYSTEM = ("You are a careful study assistant. Answer ONLY using the passages "
              "provided, and cite the reference(s) you used. If the answer is not "
              "in them, reply exactly: 'Not found in the provided text.'")


def embed(texts):
    """Embed a list of strings via the same client (OpenAI /embeddings path)."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def cosine(a, b):
    """Cosine similarity — 'how close in meaning' two vectors are."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)


def _lex(query, text):
    """Keyword-overlap fallback (used only if no embedding model is served)."""
    q, t = set(query.lower().split()), set(text.lower().split())
    return len(q & t) / (len(q) + 1e-9)


def retrieve(query, doc_vectors, use_embeddings, k=2, show=True):
    """Return the k passages closest to the query (the 'R' in RAG)."""
    if use_embeddings:
        qv = embed([query])[0]
        scored = [(cosine(qv, dv), d) for dv, d in zip(doc_vectors, CORPUS)]
    else:
        scored = [(_lex(query, d["text"]), d) for d in CORPUS]
    scored.sort(key=lambda s: s[0], reverse=True)
    if show:
        print(f"Query: {query}\nRanked passages (similarity):")
        for score, d in scored:
            print(f"  {score:5.3f}  {d['ref']}")
        print("-" * 70)
    return [d for _, d in scored[:k]]


def rag_answer(query, doc_vectors, use_embeddings, k=2):
    """Full RAG: retrieve the k best passages, then answer grounded in them."""
    hits = retrieve(query, doc_vectors, use_embeddings, k=k, show=False)
    context = "\n\n".join(f"[{d['ref']}] {d['text']}" for d in hits)
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": RAG_SYSTEM},
            {"role": "user", "content": f"Passages:\n{context}\n\nQuestion: {query}"},
        ],
        temperature=0,
    )
    print(f"RETRIEVED: {', '.join(d['ref'] for d in hits)}")
    print(resp.choices[0].message.content)
    print("=" * 70)


def main() -> None:
    # 1. INDEX (with automatic fallback so the demo always runs).
    use_embeddings = True
    try:
        doc_vectors = embed([d["text"] for d in CORPUS])
        print(f"Indexed {len(CORPUS)} passages with embeddings ({EMBED_MODEL}).\n")
    except Exception as e:  # embedding model not served -> lexical fallback
        use_embeddings = False
        doc_vectors = None
        print(f"[embeddings unavailable: {e}]\nFalling back to keyword overlap.\n")

    # 2. RETRIEVE — watch the geometry pick the right text (nothing hard-coded).
    retrieve("Who rescues me from this body of death?", doc_vectors, use_embeddings)

    # 3. GROUND — answer only from what was retrieved.
    #    Fact IS in the corpus -> grounded, cited answer:
    rag_answer("Who delivers the speaker from the body of death?",
               doc_vectors, use_embeddings)
    #    Fact is NOT in the corpus -> the model refuses instead of hallucinating:
    rag_answer("In what year was the Epistle to the Romans written?",
               doc_vectors, use_embeddings)


if __name__ == "__main__":
    main()
