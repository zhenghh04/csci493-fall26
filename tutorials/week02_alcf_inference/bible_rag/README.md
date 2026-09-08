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

## Optional: the *semantic* retriever (Slide 5, "meaning as geometry")

BM25 matches **words**. It's great when your question shares words with the verse
(or names the reference), but it misses paraphrases — ask *"Who was Boaz's father?"*
and BM25 struggles, because the KJV says *"Salmon begat Boaz"* (no word "father").

Embeddings fix that by matching **meaning**. Build the cache once (before class —
it makes ~120 requests over a few minutes), then `ask_bible.py` uses it automatically:

```bash
python build_index.py                       # writes bible_index.npz (~48 MB)
python ask_bible.py --embed "Who was Boaz's father?"
```

This is the same `client.embeddings.create` you used on six verses — now on 31,100.

---

## Files

| File | What it is |
| --- | --- |
| `get_bible.py` | Download + flatten the KJV → `kjv.json` (run once). |
| `ask_bible.py` | **The demo.** Without-RAG vs with-RAG, BM25 by default. |
| `build_index.py` | Optional: pre-compute embeddings → `bible_index.npz`. |
| `kjv.json` | The corpus (generated; public domain). |
| `bible_index.npz` | The embedding cache (generated; git-ignored, ~48 MB). |

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `kjv.json not found` | Run `python get_bible.py` first. |
| `401 Unauthorized` on a model call | Token expired — re-run `inference_auth_token.py authenticate`. |
| Model ID not found / 404 | The served set rotates. Run `list-endpoints` and update `CHAT_MODEL` / `EMBED_MODEL` at the top of the scripts. |
| `--retrieve-only` works but model calls fail | Retrieval needs no token; only the *answer* step calls the model. Good sign — just fix auth. |
| Embedding index ignored | `bible_index.npz` missing or stale → run `build_index.py`. BM25 still works without it. |
