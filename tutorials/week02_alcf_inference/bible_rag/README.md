# Chat with the *whole* Bible — RAG vs. no RAG on a small model

This is the capstone of the Week 2 lab. In `../02_simple_rag.py` you ran RAG over
**six** verses. Here the corpus is the **entire King James Bible — 31,100 verses**,
and the question we care about is:

> When you ask a *small* model a question about Scripture, what changes when you
> let it **retrieve the actual text first**?

**The lesson (this is the whole point).**

| | Without RAG | With RAG |
| --- | --- | --- |
| Where the answer comes from | the model's memory | verses retrieved from the KJV |
| Famous verses | roughly right, often **paraphrased** | **quoted exactly**, with a citation |
| Obscure verses / numbers / genealogies | confidently **wrong** | correct, from the text |
| A verse that doesn't exist | **invents** one | **refuses**: *"Not found in the provided verses."* |

For a scholar this is the difference between a *paraphrase* and *the text itself* —
and between a citation you can trust and one you have to go check.

---

## Setup

```bash
# 0. Download the corpus ONCE (no ALCF token needed; ~6.7 MB, public domain KJV)
python get_bible.py

# 1. The model client
pip install openai numpy
python inference_auth_token.py authenticate      # browser login, ~48h token
```

`get_bible.py` writes `kjv.json` (one record per verse: `ref`, `book`, `chapter`,
`verse`, `text`). If your clone already has `kjv.json`, you can skip step 0.

## Run

```bash
# The headline demo: 5 curated questions, each answered WITHOUT then WITH RAG
python ask_bible.py

# Ask your own question
python ask_bible.py "What does Micah 6:8 require of us?"
python ask_bible.py "Quote John 3:16 exactly."

# See ONLY what retrieval pulls back (no model call, no token needed)
python ask_bible.py --retrieve-only "a still small voice"
```

You control the **small** model on purpose — `Meta-Llama-3.1-8B-Instruct`. A small
model is where the "without RAG" failure is most visible; a frontier model would
paper over it and hide the lesson.

---

## How it works — RAG in three steps

1. **INDEX** — every verse becomes searchable. The default retriever is **BM25**,
   a classic keyword search (pure Python, instant across all 31k verses, *no build
   step, no network*). It also indexes each verse's **reference**, so asking
   *"what does Micah 6:8 say"* pulls that exact verse to the top.
2. **RETRIEVE** — the top few verses most relevant to your question.
3. **GROUND** — the model is asked to answer using **only** those verses, quote
   them exactly, cite the reference, and say *"Not found in the provided verses."*
   when the answer isn't there.

That third step is the cure for the hallucination you saw in §2 of the notebook.

## Optional: the *semantic* retriever (Slide 6, "meaning as geometry")

BM25 matches **words**. It's great when your question shares words with the verse
(or names the reference), but it misses paraphrases — ask *"the greatest commandment"*
and BM25 pulls keyword noise (*"greatest part"*, *"greatest over a thousand"*)
instead of Matthew 22:37.

Embeddings fix that by matching **meaning**. There are two ways to build the
semantic index — pick whichever fits your setup:

### A. Local HuggingFace embeddings — **use this now** (`ask_bible_local.py`)

The ALCF gateway does **not** currently serve an embedding model, so the recommended
path embeds verses with a small open model that runs **on your own machine** (CPU is
fine). Only retrieval is local; the **answer** step still uses the small ALCF chat
model, so the with/without-RAG lesson is unchanged.

```bash
pip install sentence-transformers            # pulls torch; run once
python build_index_local.py                  # writes bible_index_local.npz (~90s on CPU)
python ask_bible_local.py --embed "the greatest commandment"
# retrieval is local, so this needs NO ALCF token:
python ask_bible_local.py --retrieve-only --embed "God beside still waters"
```

Default model: `sentence-transformers/all-MiniLM-L6-v2` (384-dim, ~90 MB). Swap it
with `LOCAL_EMBED_MODEL=BAAI/bge-small-en-v1.5 python build_index_local.py`.
If no cache exists, `ask_bible_local.py --embed` embeds the whole Bible in memory on
first run (a bit slower); `build_index_local.py` just caches that step.

### B. ALCF-served embeddings (`ask_bible.py` + `build_index.py`)

The original path: the **same** `client.embeddings.create` you used on six verses,
now on 31,100. Works only when an embedding model is served on the endpoint
(confirm with `list-endpoints`) — kept for when ALCF offers one again.

```bash
python build_index.py                        # writes bible_index.npz
python ask_bible.py --embed "the greatest commandment"
```

**Honest caveat (a good teaching point):** embeddings win on *paraphrases*
("the greatest commandment" → Matthew 22:37), but BM25 can still win when your
question shares exact words with the verse ("beside the still waters" → Psalm 23:2).
Retrieval quality is a genuine trade-off, not a solved problem.

---

## Files

| File | What it is |
| --- | --- |
| `get_bible.py` | Download + flatten the KJV → `kjv.json` (run once). |
| `ask_bible.py` | **The demo.** Without-RAG vs with-RAG, BM25 by default. |
| `ask_bible_local.py` | **Same demo, LOCAL embeddings** — semantic retrieval with a HuggingFace model on your machine (no ALCF embedding endpoint needed). |
| `build_index.py` | Optional: pre-compute embeddings via the **ALCF** endpoint → `bible_index.npz`. |
| `build_index_local.py` | Optional: pre-compute embeddings with a **local** HuggingFace model → `bible_index_local.npz`. |
| `kjv.json` | The corpus (generated; public domain). |
| `bible_index*.npz` | The embedding caches (generated; git-ignored). |

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `kjv.json not found` | Run `python get_bible.py` first. |
| `401 Unauthorized` on a model call | Token expired — re-run `inference_auth_token.py authenticate`. |
| Model ID not found / 404 | The served set rotates. Run `list-endpoints` and update `CHAT_MODEL` / `EMBED_MODEL` at the top of the scripts. |
| `--retrieve-only` works but model calls fail | Retrieval needs no token; only the *answer* step calls the model. Good sign — just fix auth. |
| Embedding index ignored | `bible_index*.npz` missing or stale → rerun the matching `build_index*.py`. BM25 still works without it. |
| No embedding model served on ALCF (404 on `/embeddings`) | Expected right now — use the local path: `pip install sentence-transformers && python build_index_local.py && python ask_bible_local.py --embed "..."`. |
| `ModuleNotFoundError: sentence_transformers` | `pip install sentence-transformers` (one-time; pulls torch). Only needed for the *local* embedding path; BM25 needs nothing. |
