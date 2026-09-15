# Lecture — Coding Agents on an Open Model (opencode + ALCF) & Vibe Coding

**Course:** AI for Theological Inquiry — Mentored Research Seminar
**Session:** 100 min · **Instructor:** Huihuo Zheng
*(Placement is yours — this is the natural bridge between the Week 2 "raw model" lab
and the RAG/eval core. Renumber to whatever week you drop it in.)*

> **Two things today**
> 1. **Connect an open ALCF model to a coding agent (opencode)** — wrap the agent
>    loop back around the raw model from last week, using the *same* endpoint URL.
> 2. **Vibe coding** — what it is, why it's fast, and why "trust the vibes" is the
>    exact habit this course teaches you to discipline for research.

**Session goal:** every student leaves with (a) a working coding **agent** driven by
an **open model they control**, (b) a felt sense of the `plan → act → observe` loop
doing real work, and (c) a fresh disclosure-appendix artifact — a *fabrication baked
into code that runs green*.

**The one-line arc:** *Week 2 you met the engine and caught it lying. Today you put
the engine in a car that drives itself — same lie, now moving faster. So we learn to
steer.*

**Rough timing**
| Block | Min | What |
|---|---|---|
| 0. Recap & framing | 5 | Raw model → agent loop; "put the lid back on with tools" |
| 1. What opencode is | 10 | An open coding agent; the loop; why open + on ALCF |
| 2. The connect trick | 10 | "It's just an OpenAI-compatible URL" — one config block |
| 3. Hands-on: wire it up | 25 | Token → `opencode.json` → `/models` → first agent run |
| 4. Vibe coding: the concept | 10 | Karpathy's term; the promise; the taxonomy |
| 5. Hands-on: vibe + distrust | 20 | Build a tool, then trip the factual trap on purpose |
| 6. The discipline | 15 | Vibe-to-explore vs. verify-to-publish; disclosure |
| 7. Wrap + assignment | 5 | Reading + trace deliverable |

---

## Part 1 — Concept (~20 min)

### 0. Recap & framing (5 min)
- Week 1: three pillars (agent · RAG · eval); you *felt* `plan → act → observe` in a
  coding agent. Week 2: you stripped the tools away and met the **raw model** — and
  caught it hallucinating a verse.
- **Today reunites them:** take that same raw open model and **put the agent loop
  back around it**, deliberately, with a tool *you* wired up. "We open the box last
  week; today we build the box."

### 1. What is opencode, and why open + on ALCF (10 min)
- **opencode** = a free, open-source coding agent that runs in your terminal: it can
  read/write files and run commands, looping until a goal is met. Same family as the
  Claude Code you used in Week 1 — but **open**, and **provider-agnostic**.
- **Whiteboard the loop again:** `Goal → Plan → Act (edit file / run cmd) → Observe
  (output/error) → fix → … → Done`. An LLM answers once; an **agent runs the loop**.
- **Why an *open* model, and why on ALCF** (course-values fit, 30 s each):
  - **Reproducible** — "opencode + Llama-3.1-8B on ALCF, temp 0" is a *disclosable*
    stack. "I used an AI to write it" is not.
  - **Governed** — your corpus and code stay on your account/ALCF; no vendor sees them.
  - **Yours** — no personal API key on a lab machine; free with the ALCF account you
    already have.

### 2. The connect trick — "it's just a URL" (10 min)
- The single idea that makes this easy: the ALCF endpoint is **OpenAI-compatible**,
  and opencode speaks to *any* OpenAI-compatible provider. So we reuse the **exact
  `base_url` from Week 2** and hand opencode **your ALCF token as the API key**.
- Put the config on the projector and read the four fields (see the handout):
  `baseURL` (unchanged from last week), `apiKey: "{env:ALCF_TOKEN}"` (no secret in
  the file), `npm: "@ai-sdk/openai-compatible"` (ALCF serves `/v1/chat/completions`),
  and the `models` map (must hold a **live** ID from `list-endpoints`).
- **The point to say out loud:** *"You already learned the hard part in Week 2 — the
  URL and the token. A coding agent is just a nicer front-end over the same call."*

---

## Part 2 — Hands-on: wire opencode to ALCF (~25 min)

Materials: `tutorials/opencode_vibe_coding/` (`README.md`, `opencode.json`,
`set_alcf_token.sh`, `sample.txt`).

1. **Install** opencode (`npm install -g opencode-ai` *or* the curl installer). (10 min buffer — this is the new failure point; pre-check lab machines.)
2. **Refresh the token into the shell:** `export ALCF_TOKEN=$(python inference_auth_token.py get_access_token)` (or `source set_alcf_token.sh`).
   *Say it:* opencode reads the token **at startup** — refresh, then launch.
3. **Confirm a live model ID** via `list-endpoints`; edit `opencode.json` if needed.
4. **Drop `opencode.json` in the project folder**, run `opencode`, `/models` → ALCF → Llama 3.1 8B.
5. **Checkpoint:** ask *"What model are you and who serves you?"* → a real completion from your open model, inside an agent.

> **Two cautions (say first):**
> - **401 = expired token.** The #1 gotcha: refresh the env var **and restart**
>   opencode (startup-read). Not a code bug.
> - **Cold start** on Sophia can take 10–15 min on the *first* call — warm it before class.

---

## Part 3 — Vibe coding (~30 min)

### 4. The concept (10 min)
- **Define it (Karpathy, 2025):** describe what you want in natural language, let the
  agent write & run the code, and *"give in to the vibes"* — accept output without
  reading every line. "Forget the code even exists."
- **Why it's seductive & real:** speed, a low barrier (describe, don't syntax),
  perfect for throwaway exploration. This is a genuine capability, not a gimmick —
  name that honestly before the critique.
- **The taxonomy to draw:**
  | | Vibe coding | Engineering with an agent |
  |---|---|---|
  | You read the output? | No | Yes |
  | Good for | prototypes, throwaways, learning | anything cited/published/shared |
  | Failure mode | fluent bugs & fabrications ship silently | slower, but auditable |

### 5. Hands-on — vibe, then distrust (20 min)
1. **Vibe it (10 min).** Prompt opencode: *"Create `verse_count.py` that reads a
   text file of verses (one per line) and prints the 10 most frequent non-stop-words;
   run it on `sample.txt`."* Let it plan → write → run → self-fix. **They watch the
   loop do real work on their open model.** Don't read the code yet — that's the point.
2. **Trip the trap (10 min).** Prompt: *"Add a function returning the exact text of
   Philemon 1:6 from memory — no file, no internet."* It hard-codes a **plausible,
   likely-wrong** verse. Now the Week-2 hallucination is **baked into code that runs
   green.** Diff against the real verse.
   > **The money line:** *"Green tests are not truth. The agent optimizes for
   > plausible, not true — same as last week — but now it hides inside working code."*
   **Have them save this** (prompt + generated verse + real verse) → disclosure artifact.

### 6. The discipline (15 min)
- **The rule:** *vibe to explore, verify to publish.* For anything you'll cite:
  (a) **read** what the agent wrote, (b) **ground** factual claims in a real source →
  that's **RAG (Week 4)**, (c) **test** it → **evaluation (Week 6)**, (d) **disclose**
  the model, the tool, and what you accepted unread.
- **Theology-specific stakes (land this):** a fabricated verse in a *script* is worse
  than in a chat — it looks authoritative, runs automatically, and propagates. The
  agent is a **collaborator, not an author**; authorship (and responsibility) stays
  with the scholar.
- **Discussion hook (3 min):** *"Where is the line between using a tool and
  outsourcing your judgment? If an agent writes your exegesis script, whose argument
  is it?"*

---

## Wrap-up (5 min)

- **We covered:** how a coding **agent** wraps the `plan → act → observe` loop around a
  raw model; how to point opencode at an **open ALCF model** with one config block
  (same URL + your token); what **vibe coding** is, why it's fast, and why it's
  dangerous for research; and the discipline — vibe to explore, verify to publish.
- **Through-line:** *ground it (RAG), prove it (eval), disclose it (integrity).* Today
  you felt why — a fabrication that now *runs*.

**Deliverable — due before next week:**
> 1. **Wire up opencode + ALCF** and get one agent completion from your open model.
> 2. **Vibe-code the small tool**, then provoke and **save one fabrication baked into
>    running code** — prompt, the generated (wrong) claim, and the real source. *This
>    is a disclosure-appendix artifact.*

**Reading:**
- Karpathy, *Vibe coding* (2025) — the origin tweet/thread; note "forget the code exists."
- Anthropic, *Building Effective Agents* (2024) — the tool-use loop (re-skim from Wk 2).
- Optional: an opencode/agent-safety piece on reviewing agent-generated code.

**Next week:** the **theological corpus** — the texts you'll ground on all term. Today
you saw *why* grounding matters; next we assemble what to ground *on*.

---

### Instructor prep checklist
- [ ] **Pre-install opencode on the lab machines** (or a shared image) — Node 18+, npm
      global bin on `PATH`. New #1 failure point this week.
- [ ] **Re-run the whole lab yourself today**: `export ALCF_TOKEN=…` → `opencode` →
      `/models` → first prompt → the two vibe prompts. Model behavior drifts.
- [ ] **Confirm a live model ID** from `list-endpoints` and update `opencode.json`'s
      `models` map **and** the top-level `model:` line. Warm Sophia (cold start 10–15 min).
- [ ] Have a **known green-but-wrong fabrication** already reproduced (e.g. a wrong
      Philemon 1:6) so the money moment lands on the projector even if student auth stalls.
- [ ] Have the **real verse text** on a slide for the diff.
- [ ] Fallback: a **pre-recorded opencode session** if npm/auth blocks a student.
