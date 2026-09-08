# Week 2 Lab — Getting onto the ALCF Inference Endpoint

*AI for Theological Inquiry · one-page student handout*

Today you'll talk to a **raw open-weight language model** (Llama / Qwen / …) directly —
no coding agent in front of it. You'll see it be creative (temperature), catch it
inventing a fake verse (hallucination), and then fix it by hand (grounding). That
arc is the whole course in miniature.

You need three things: **(1)** an ALCF account, **(2)** Python with the `openai`
package, **(3)** ~15 lines of code. That's it. We never leave the notebook.

---

## 0. Prerequisites (do this once)

- An **ALCF account** with the **DLIO** project (you applied in Week 1 at
  <https://accounts.alcf.anl.gov>). If you don't have it yet, pair up with someone who does.
- Python 3.9+ and the OpenAI client:
  ```bash
  pip install openai
  ```

## 1. Authenticate (once; token lasts ~48 hours)

Grab ALCF's small auth helper, then log in through your browser:

```bash
# download the helper into your working folder (one time)
wget https://raw.githubusercontent.com/argonne-lcf/inference-endpoints/main/inference_auth_token.py

# opens a browser window — log in with your ALCF / Globus credentials
python inference_auth_token.py authenticate
```

Keep `inference_auth_token.py` in the same folder as your notebook/scripts —
the code imports `get_access_token` from it.

## 2. See what models are being served

The set of available models changes. **Always check, then copy an exact ID.**

```bash
tok=$(python inference_auth_token.py get_access_token)
curl -s https://inference-api.alcf.anl.gov/resource_server/list-endpoints \
  -H "Authorization: Bearer $tok"
```

Pick a chat model from the output (e.g. something like
`meta-llama/Meta-Llama-3.1-8B-Instruct`) and use that exact string as `model=` below.

## 3. Talk to the model (the 15 lines you'll reuse all term)

```python
from openai import OpenAI
from inference_auth_token import get_access_token

client = OpenAI(
    api_key=get_access_token(),
    base_url="https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1",
)

resp = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",   # <-- an ID from step 2
    messages=[{"role": "user", "content": "What does Romans 7:24 say?"}],
    temperature=0,
)
print(resp.choices[0].message.content)
```

This is **OpenAI-compatible**: the same call shape becomes your RAG retriever's
brain in Week 4 and your evaluation harness in Week 6. Learn it once.

- Run `python 01_hello_alcf.py` for a minimal version of the above.
- Open `alcf_inference_demo.ipynb` for the four guided experiments.
- Run `python 02_simple_rag.py` for the standalone RAG example (experiment #4).

---

## The four experiments (in the notebook)

| # | What you do | The idea it shows |
|---|---|---|
| 1 | Same prompt at `temp=0` (twice) vs `temp=1.5` (three times) | **Sampling**: low temp is deterministic; high temp diverges |
| 2 | Ask for a **non-existent** verse (e.g. *"Quote Hezekiah 3:16"*) | **Hallucination**: it completes a *pattern*, not a lookup |
| 3 | Paste the **real** passage in and ask again ("answer only from the text") | **Grounding**: the fix for #2 — retrieval done *by hand* |
| 4 | Let the code **embed → retrieve → ground** over a six-verse corpus | **RAG**: automate the retrieve step; index→retrieve→ground |

**Save your experiment #2 output** — model ID, temperature, prompt, and the wrong
answer. That's your first *disclosure-appendix* artifact (see the syllabus).

### Experiment #4 in one breath — RAG

RAG (Retrieval-Augmented Generation) is just **three steps on the same client**:

1. **Index** — embed each passage into a vector (`client.embeddings.create`).
2. **Retrieve** — embed the *question*, keep the passages with the highest cosine
   similarity ("nearest in meaning" — Slide 5).
3. **Ground** — answer using *only* those passages (experiment #3, now automatic).

You'll see two questions: one whose answer is in the corpus (grounded, cited
answer) and one whose answer is absent (retrieval still returns its closest guess,
but the model *declines* instead of inventing). That decline is the cure for #2.
The notebook falls back to a keyword score automatically if no embedding model is
served, so the lesson runs either way.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Browser login hangs on campus Wi-Fi | Try a personal hotspot; or use the instructor's pre-run notebook as a fallback — the *ideas* don't depend on your token working in the first 5 minutes. |
| `401 Unauthorized` on a call | Your token expired (~48 h). Re-run `python inference_auth_token.py authenticate`. |
| First call takes 10–15 minutes | Cold start on Sophia — the model is spinning up. Wait, or ask the instructor to warm it before class. |
| `ModuleNotFoundError: openai` | `pip install openai` |
| `ImportError: get_access_token` | `inference_auth_token.py` must be in the same folder you're running from. |
| Model ID rejected / not found | The served list changed — re-run step 2 and copy a current ID. |
| Embedding call fails in exp #4 | The `EMBED_MODEL` isn't served — re-run step 2, copy an ID with `embed`/`bge`/`nomic` in it. (The notebook auto-falls back to keyword retrieval, so class continues either way.) |

**Security:** never paste a personal API key onto a shared/lab machine. The ALCF
token flow above uses *your* account and needs no pasted secrets.

**Reference:** ALCF Inference Endpoints docs —
<https://docs.alcf.anl.gov/services/inference-endpoints/>
