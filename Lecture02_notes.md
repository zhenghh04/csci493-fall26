# Lecture 2 — From LLMs to Agents

**Course:** AI for Theological Inquiry — Mentored Research Seminar
**Session:** Week 2 (100 min)
**Instructor:** Huihuo Zheng

> **Two parts today**
> 1. **Concept** — open the hood on the raw language model: next-token prediction, embeddings, temperature, and hallucination; then the four things that turn an LLM into an *agent*.
> 2. **Hands-on** — log in to the **ALCF inference endpoint** and talk to an open-weight model directly: a temperature sweep, a deliberate hallucination, and a "grounding by hand" teaser.

**Session goal:** every student leaves having (a) an intuition for what a language model mechanically *is* and *why it hallucinates*, (b) a working, reproducible connection to an open model they control, and (c) a first disclosure-appendix artifact — a hallucination they caught themselves.

**The one-line arc:** *Last week you met the box already wired to tools (Claude Code). This week you meet the box itself — and catch it lying — so you understand why the rest of the course (RAG, evaluation) exists.*

**Rough timing**
| Block | Min | What |
|---|---|---|
| 0. Recap & framing | 5 | Week 1 → Week 2; "open the box" |
| 1. Next-token prediction | 10 | The one idea everything follows from |
| 2. Embeddings | 10 | Meaning as geometry; the hinge to RAG |
| 3. Temperature | 5 | The same box, one knob |
| 4. Hallucination | 10 | Why it happens; why it matters here |
| 5. LLM → agent | 10 | The four additions + the loop |
| 6. Hands-on: ALCF endpoint | 40 | Auth → client → 3 experiments |
| 7. Project touchpoint | 15 | Point the model at *your* question |
| 8. Wrap + assignment | 5 | Reading + trace deliverable |

*(Concept blocks 1–5 ≈ 40 min; lab ≈ 40 min; touchpoint ≈ 20 min — the standard weekly shape.)*

---

## Part 1 — Concept (~40 min)

### 0. Recap & framing (5 min)
- One line back to Week 1: three pillars (agent · RAG · eval); you installed a coding agent and felt `plan → act → observe`.
- **Reframe today:** last week the model came *pre-wired to tools*. Today we strip that away and look at the **raw model** — what it is, and why we can't just trust it. "We open the box, then we put the lid back on with tools."
- Confirm everyone got their **ALCF account + DLIO project** (the Week-1 assignment). Anyone who didn't → pair them with someone who did for the lab.

### 1. Next-token prediction — the one idea (10 min)

**Say it plainly:** a language model, mechanically, does one thing — given some text, it outputs a **probability over every possible next token**, picks one, appends it, and repeats. `"The Lord is my ___"` → `shepherd (0.71)`, `strength (0.06)`, `rock (0.05)`, …

**The two consequences to land (this is the whole lecture in two bullets):**
- It has **no facts stored as facts** — only *patterns* of which tokens follow which, learned from a huge amount of text.
- It optimizes for **plausible, not true**. To the model, a fluent wrong answer scores as well as a right one. Everything else today (temperature, hallucination) follows from this.

> **Discussion hook (2 min):** "If it's just predicting the next word, how does it ever get anything *right*?" — Answer: because true statements are, most of the time, the most *common* continuations in the training text. Truth is a frequent side-effect, not the objective. That gap is where our course lives.

### 2. Embeddings — meaning as geometry (10 min)

**The pipeline:** text → **token(s)** (integer IDs) → **embedding** (a vector of numbers) → the model. An embedding places each token at a **point in a high-dimensional space** so that *closeness in space ≈ closeness in meaning* — the model learned this from usage, not a dictionary.

- Related words land near each other (`shepherd`, `sheep`, `flock` cluster; `grace`, `mercy`, `salvation` cluster elsewhere).
- "Distance" becomes something you can **compute** — cosine similarity between two vectors.
- So you can ask *"which verses are closest to this question?"* and get **real passages** back.

> **The hinge to Week 4:** retrieval *is* "find the nearest vectors." When we build RAG, the retriever is exactly this embedding trick pointed at your corpus. Flag it now so Week 4 feels inevitable, not new.

### 3. Temperature — the same box, one knob (5 min)

The model always emits a probability distribution; **temperature** controls how boldly you sample from it.
- `temperature = 0` → always take the top token → **deterministic, repeatable**.
- `temperature = 1.5` → sample widely → **creative, unstable** (and more chances to go off the rails).

> **The scholarship point:** for research you usually want **low** temperature — *and you report the number.* "Llama-3.1-8B, temp = 0" is part of an honest method. This is the first concrete thing that goes in their disclosure appendix.

### 4. Hallucination — the money moment (10 min)

**The claim:** ask a small model for an obscure or *made-up* verse and it will confidently invent one in flawless biblical cadence.

- **Why it happens:** it is completing a *pattern*, not looking something up. "A verse citation" has a recognizable shape; the model fills the shape convincingly whether or not the verse exists.
- **What fixes it:** don't ask it to *recall* — give it the **real text** and ask it to *use* that. Grounding = **RAG** (Wk 4). Checking = **evaluation** (Wk 6).

> **The line to land (repeat from Week 1, now earned):** *In theology, a fabricated scripture reference is a scholarly and pastoral failure.* Today they will **reproduce this live**, so the abstraction becomes a memory. That memory is the motivation for the entire technical core of the course.

### 5. From LLM to agent — the four additions + the loop (10 min)

On its own the model answers once and stops. Add four things and it can *pursue a goal*:
1. **Tool use** — call a retriever, calculator, code runner, the web (*reach outside itself*).
2. **Memory** — carry state across steps (what it found, what it decided).
3. **Plan → act → observe** — decompose, act, *look at the result*, decide the next step.
4. **Autonomy** — run many steps toward a goal without a human at each one.

> **Whiteboard the loop:** `Goal → Plan → Act (tool) → Observe (result) → reflect → Act again … → Answer (with citation)`. An LLM answers in one shot; an **agent runs the loop**.
>
> **Connect to the lab:** today we deliberately isolate the *very first box* — a single raw model call (`Act → Observe` on one turn). That's what the ALCF endpoint gives you: the engine, before the loop. Weeks 4–5 add the loop back, on purpose.

**Why an *open* model, and why on ALCF** (30 sec each — this is a course-values fit, not an HPC pitch):
- **Reproducible** — an open model ID + temperature is a *disclosable* fact; "ChatGPT last spring" is not.
- **Governed** — a licensed translation or private corpus stays on ALCF; it never leaves for a vendor (matters once we load texts in Wk 3).
- **Yours** — free with their ALCF account; no personal API keys on shared machines; and the endpoint is **OpenAI-compatible**, so today's ~15 lines become the retriever's brain in Week 4 unchanged.

---

## Part 2 — Hands-on: the ALCF inference endpoint (~40 min)

**Goal of this block:** everyone gets one real completion back from an open model, then runs three tiny experiments that mirror Part 1. Materials live in `tutorials/week02_alcf_inference/` (one-page handout `README.md`, `01_hello_alcf.py`, and `alcf_inference_demo.ipynb`).

> **Instructor note — set expectations (30 sec):** "We're using a supercomputer, but today it's just *a model behind a URL*. Spend your attention on what the model does, not on clusters. We never leave the notebook."

### Step 1 — Authenticate (once; token good ~48 h) (10 min)
```bash
# one-time: grab the ALCF auth helper
wget https://raw.githubusercontent.com/argonne-lcf/inference-endpoints/main/inference_auth_token.py

# opens a browser — log in with your ALCF / Globus credentials
python inference_auth_token.py authenticate
```
Then confirm what's being served (copy an exact model ID from the output):
```bash
tok=$(python inference_auth_token.py get_access_token)
curl -s https://inference-api.alcf.anl.gov/resource_server/list-endpoints \
  -H "Authorization: Bearer $tok"
```
*Checkpoint:* `list-endpoints` returns JSON with model names. Token lasts ~48 h; re-run `authenticate` when calls start returning **401** (full re-auth with `--force` is only needed ~every 30 days).

### Step 2 — The 15-line client (5 min)
```python
from openai import OpenAI
from inference_auth_token import get_access_token

client = OpenAI(
    api_key=get_access_token(),
    base_url="https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1",
)

resp = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",   # use an ID from list-endpoints
    messages=[{"role": "user", "content": "What does Romans 7:24 say?"}],
    temperature=0,
)
print(resp.choices[0].message.content)
```
`pip install openai` first. *Checkpoint:* one real completion prints.

> **The point to say out loud:** this is the *same call shape* you'll reuse for retrieval and evaluation later. Learn it once.

### Step 3 — Three tiny experiments, three big ideas (25 min)
1. **Temperature (determinism vs. sampling).** Same prompt at `temp=0` twice → identical. Same prompt at `temp=1.5` three times → all different. *They see next-token sampling with their own eyes.*
2. **Hallucination (the lesson).** Ask for a non-existent verse — e.g. *"Quote Hezekiah 3:16"* (there is no Book of Hezekiah), or *"Summarize the Epistle of Paul to the Corinthians III."* Watch it confidently produce text. **Have them save this one** — model ID, temperature, prompt, wrong output.
3. **Grounding teaser (the fix).** Paste the *real* passage into the prompt and ask the same question with *"Answer only from the text above; if it's not there, say so."* The answer snaps to truth (or an honest "not found"). **That is RAG, done by hand** — a one-line preview of Week 4.

> **Two cautions (say before they run):**
> - **Auth can stall on campus Wi-Fi** — the first login is a Globus *browser* flow. If it hangs: personal hotspot, or fall back to the instructor's pre-run notebook output. The *ideas* don't depend on your token working in the first five minutes.
> - **Don't drift into ops.** If someone asks about GPUs/queues, park it — "great Week-3+ question." Keep the room on model behavior.

---

## Part 3 — Project touchpoint (~15–20 min)

Point the raw model at *their own* question and start their evaluation set:
- Take the **interest statement** from Week 1. Turn it into **one factual question** an 8B model could plausibly get wrong (a specific date, citation, attribution, or minority-tradition claim).
- Run it at `temp=0`. **Fact-check the answer themselves.** Note exactly where it was fluent-but-wrong.
- **Keep that failing question** — it is a seed for their Week-6 evaluation set. (Foreshadow: "By Week 6 you'll have a whole file of these, and a scorecard.")

> **The through-line to say:** "Today you saw *why* we need grounding and evaluation. Week 3 loads your corpus; Week 4 turns this same client into a retriever over it; Week 6 you grade it. Same client, same corpus, all term."

---

## Wrap-up (5 min)

- **We covered:** what a language model mechanically *is* (next-token prediction), how it represents meaning (embeddings → the hinge to RAG), the temperature knob, *why* it hallucinates, and the four additions that turn an LLM into an agent. You talked to a raw open model on ALCF and **caught it lying**.
- **The through-line:** *ground it (RAG), make it act (agent), prove it works (evaluation)* — today you felt why the first and third exist.

**Week-2 deliverable — due before Week 3:**
> 1. **Run the notebook** and get one real completion back from the ALCF endpoint.
> 2. **Save one hallucination you provoked** — model ID, temperature, prompt, and the wrong output (screenshot or transcript). *This is your first disclosure-appendix artifact.*

**Reading for next week:**
- Anthropic, *Building Effective Agents* (2024) — skim; note the tool-use loop.
- Weng, *LLM-Powered Autonomous Agents* (2023) — read the "planning" and "memory" sections.
- Optional: Wolfram, *What Is ChatGPT Doing…?* — the next-token section.

**Next week:** the **theological corpus** — the texts *you* will ground on all term (digital primary sources; copyright, canon, translation politics; "the data is theologically loaded").

---

### Instructor prep checklist
- [ ] **Pre-test the whole lab on a real lab machine** — `authenticate` browser flow, `list-endpoints`, and one completion — *before* class. Auth is the #1 failure point.
- [ ] **Confirm the exact model ID** served today from `list-endpoints` and update the notebook/handout default if `Meta-Llama-3.1-8B-Instruct` isn't listed. (Sophia cold-starts can take 10–15 min — warm it before class.)
- [ ] Have a **pre-run notebook** (outputs saved) ready as a projector fallback if student auth stalls.
- [ ] Queue one **known hallucination** you've already reproduced today (model IDs change behavior) so the money moment is guaranteed on the projector.
- [ ] Have the **real text of one verse** on a slide/clipboard for the grounding teaser.
- [ ] Confirm students have their **ALCF account + DLIO project** from Week 1; pair up anyone who doesn't.
- [ ] `pip install openai` availability on lab machines (or a shared venv).
