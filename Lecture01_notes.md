# Lecture 1 — Course Intro, Agentic AI, and Your Toolkit

**Course:** AI for Theological Inquiry — Mentored Research Seminar
**Session:** Week 1 (100 min)
**Instructor:** Huihuo Zheng

> **Two parts today**
> 1. **Lecture** — the course, the syllabus, the mentored-research structure, and a first taste of *agentic AI*.
> 2. **Hands-on** — set up your working environment: **VS Code + Claude Code / Codex**.

**Session goal:** every student leaves with (a) a clear picture of what we will build and how you will be graded, (b) an intuition for what makes an AI system an *agent*, and (c) a working coding environment they can open next week.

**Rough timing**
| Block | Min | What |
|---|---|---|
| 0. Welcome & logistics | 5 | Names, room, how the seminar runs |
| 1. What this course is | 15 | Instrument vs. subject; the three pillars |
| 2. Syllabus walkthrough | 15 | 14 weeks, 4 phases, deliverables |
| 3. Mentored-research structure | 10 | What "mentored research" means for you |
| 4. Agentic AI — the core idea | 20 | LLM → agent; a live demo |
| 5. Hands-on setup | 30 | VS Code + Claude Code / Codex |
| 6. Wrap + Week-1 deliverable | 5 | Interest statement |

---

## Part 1 — Lecture

### 0. Welcome (5 min)
- One-sentence round: name + the tradition / question you care about.
- Housekeeping: meeting time, where materials live, how to reach a mentor.
- Set the tone: **this is a research seminar, not a lecture course.** You will *make something* and *defend it*.

### 1. What this course is (15 min)

**The organizing idea — hold both at once:**
- **AI as a scholarly instrument** — "agentic AI *for* studying theology." A tool that retrieves primary sources, cross-references them, drafts with citations, and critiques itself.
- **AI as a theological subject** — "what theology says *about* agentic AI." Personhood, *imago Dei*, agency, responsibility, spiritual authority.

We refuse to pick one. The best projects use the instrument *and* interrogate it.

**The three technical pillars (they build on each other):**
1. **Agentic AI** — the system that plans, uses tools, and acts over multiple steps.
2. **RAG (Retrieval-Augmented Generation)** — how the agent stays grounded in *real* texts instead of inventing them.
3. **Evaluation** — how you *know* whether any of it is trustworthy.

> **The line to land:** In theology, *a fabricated scripture reference is a scholarly and pastoral failure.* That single fact is why we spend as much time on **evaluation** as on building. We check claims; we do not trust them.

**Discussion hook (2 min):** Ask the room — "If you asked a chatbot 'What does Romans 7 say about sin?' and it gave you a confident, fluent answer with a verse number — how would you know it's right?" Let the discomfort sit. That discomfort is the course.

### 2. Syllabus walkthrough (15 min)

**Shape:** 14 weeks · one 100-min session/week · every week = ~40 min concept + ~40 min lab + ~20 min project touchpoint.

**Four phases:**
- **Phase 1 — Foundations (Wk 1–3):** framing → from LLMs to agents → the theological corpus (the texts *you* will use all term).
- **Phase 2 — Technical core (Wk 4–7):** RAG → building a research agent → **evaluation** → research proposal (**midpoint gate**).
- **Phase 3 — Deep dives + launch (Wk 8–10):** hermeneutics → theology *of* AI → ethics, bias, limits of autonomy. Projects formally begin.
- **Phase 4 — Mentored execution (Wk 11–13):** build sprint → evaluate & critique → write-up. Then **Wk 14 Symposium**.

**Deliverables & weights (say these out loud):**
| Component | Weight | Due |
|---|---|---|
| Participation & project touchpoints | 15% | Weekly |
| Interest statement | 5% | Week 1 |
| Research proposal + pitch (incl. eval plan) | 20% | Week 7 (gate) |
| Preliminary results + evaluation report | 15% | Week 12 |
| Final paper | 30% | Week 14 |
| Final presentation | 15% | Week 14 |

**Two things to emphasize:**
- The **Week-7 proposal must include an evaluation plan** — it's a gate, not a formality.
- **Every deliverable carries an AI-use disclosure appendix:** models/tools, key prompts, representative traces, eval scorecard, where the agent failed, and how you verified it. *Undisclosed or unevaluated AI reliance is penalized.* Honesty is graded.

### 3. The mentored-research structure (10 min)

**What "mentored research" means here:**
- You (solo or in a pair) develop **one original project** across the term: a researchable theological question + an agentic method + an evaluation plan.
- **Mentoring is continuous**, not just at the end. Weekly 20-min touchpoints (peer review or mentor check-in) exist so you never drift for long.
- **Track decision — hybrid, low-code by default.** You build from provided notebook templates and a config-driven builder; the focus stays on *theology and research design*. A parallel **light-code (Python) path** offers the same milestones for the technically inclined. **No one writes an agent or eval harness from scratch** — every lab ships a working scaffold.
- **One corpus, one agent, all term.** RAG (Wk 4) grounds the agent (Wk 5); evaluation (Wk 6) judges both. We keep building on the *same* texts so you see the through-line.

**A concrete picture of where this goes** — a worked example the instructor built:
> A single natural-language session with a coding agent produced a **25-theologian multi-agent RAG system** — 128,739 public-domain text chunks, per-theologian retrieval, three interaction modes (panel Q&A, roundtable, debate), an **LLM-as-judge** evaluation, and an **ablation study**. The ablation is the punchline: vanilla model **5.9/10** on distinctiveness → **+ system prompt 7.5** → **+ RAG 9.3**. Retrieval over primary sources drove the largest gains (textual grounding +93%). That is the *instrument* pillar and the *evaluation* pillar in one artifact.

Your project will be smaller — but the same three moves: **ground it, make it act, prove it works.**

### 4. Agentic AI — the core idea (20 min)

**Start from the LLM.** A large language model is, mechanically, a **next-token predictor**: given text, it predicts the most likely continuation. That's it. It is fluent, it is *not* a database, and it will confidently produce a plausible-but-false verse — a **hallucination**. (This is exactly why Pillars 2 and 3 exist.)

**What turns an LLM into an *agent*?** Four additions:
1. **Tool use** — it can call things: a search index, a calculator, a code runner, a web fetch, *a retriever over your corpus*.
2. **Memory** — it can carry state across steps (what it found, what it decided).
3. **The plan → act → observe loop** — it decomposes a goal, takes an action, *looks at the result*, and decides the next step. It iterates.
4. **Autonomy** — it runs multiple steps toward a goal without a human driving each one.

> **Whiteboard this loop:**
> `Goal → Plan → Act (call a tool) → Observe (read result) → Reflect → Act again … → Answer`
> An LLM answers in one shot. An **agent** runs this loop.

**Why it matters for theology:**
- **Tool use → RAG:** the agent's most important tool is a *retriever* that pulls the actual Greek/Hebrew text, the patristic passage, the confession — so it cites what exists.
- **Reflection → a self-critic:** we can add a *second* agent — a "fact-checker" — whose only job is to catch fabricated references before you ever see them.
- **Autonomy → risk:** more steps means errors can *compound*, and it's tempting to over-trust an autonomous "researcher." Human-in-the-loop is a design requirement, not an afterthought.

**Live demo (do this on the projector, ~7 min):**
- Ask a plain chatbot a doctrine question with a verse in it. Note the fluent, confident answer.
- Then show (or narrate) an *agent* doing the same: it *plans* ("I should retrieve the passage"), *calls a retrieval tool*, *reads* the returned text, and *then* answers with a citation you can click. Point at the difference: **the second one showed its work.**
- If a live agent isn't ready, walk the theologian-agents `demo.ipynb` output instead — the point is to *see* plan→act→observe, not to have it be flawless.

**Reading pointers (Week 2 prep):** Wolfram, *What Is ChatGPT Doing…?* (selections); Anthropic, *Building Effective Agents* (2024); Weng, *LLM-Powered Autonomous Agents* (2023). Optional: Yao et al., *ReAct*.

---

## Part 2 — Hands-on: VS Code + Claude Code / Codex (30 min)

**Goal of this block:** everyone leaves with an editor open and *one* coding agent responding in the terminal. We are not coding today — we are **installing the workshop**.

> **Instructor note — set expectations first (30 sec):**
> - "Claude Code" (Anthropic) and "Codex" (OpenAI) are both **terminal-based coding agents** that live *inside* your editor. They are the *agentic AI* we just discussed, pointed at code and files.
> - You only need **one** to follow the course. We show both so you can choose. The **low-code path uses these agents lightly**; the light-code path leans on them more.
> - Accounts/API access: use the instructor-provided access. **Do not paste personal API keys onto shared machines.**

### Step 1 — Install VS Code (5 min)
1. Download from <https://code.visualstudio.com/> → install for your OS (Windows / macOS / Linux).
2. Open it once. Open the **Terminal**: menu **Terminal → New Terminal** (or `` Ctrl+` `` / `` Cmd+` ``).
3. Optional but recommended: install the **Python** extension (Extensions sidebar → search "Python" → Install). We'll need it when notebooks appear in Week 3–4.

*Checkpoint:* you can see a terminal prompt at the bottom of VS Code.

### Step 2 — Install Node.js (prerequisite for both CLIs, 3 min)
Both agents install via `npm`, which comes with Node.js.
- Download the **LTS** installer from <https://nodejs.org/> and run it.
- Verify in the VS Code terminal:
  ```bash
  node --version
  npm --version
  ```
  Both should print a version number. (Node 18+ is fine.)

### Step 3 — Option A: Claude Code (Anthropic) (7 min)
1. Install the CLI:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. From your project folder, start it:
   ```bash
   claude
   ```
3. First run walks you through **sign-in** (browser). Use the instructor-provided account/access.
4. Try it — type a plain-English request in the `claude` prompt:
   > *"Create a file hello.md that explains in two sentences what retrieval-augmented generation is."*
   Watch it **plan**, **write the file**, and **report back**. That's plan→act→observe on your own machine.
5. VS Code integration: there is a **Claude Code** extension in the Extensions marketplace that adds a side panel — optional; the terminal is enough for us.

*Checkpoint:* `claude` responds and can create a file you can see in the VS Code explorer.

### Step 4 — Option B: Codex (OpenAI) (7 min)
1. Install the CLI:
   ```bash
   npm install -g @openai/codex
   ```
2. Start it from your project folder:
   ```bash
   codex
   ```
3. First run walks you through **sign-in** (ChatGPT account or instructor-provided access).
4. Try the same request:
   > *"Create a file hello.md that explains in two sentences what retrieval-augmented generation is."*
5. VS Code integration: a **Codex** extension is also available in the marketplace (optional).

*Checkpoint:* `codex` responds and can create/edit a file.

> **If installs stall (common fixes):**
> - `npm install -g` permission error on macOS/Linux → re-run the exact command the error suggests, or use the official installer script from each tool's docs. Don't `sudo` blindly on a lab machine — ask a mentor.
> - Corporate/campus network blocks sign-in → use the instructor-provided access method.
> - Nothing prints for `node --version` → Node didn't install; re-run Step 2 and reopen the terminal.

### Step 5 — Feel the agent loop on purpose (3 min)
Pick your installed agent and give it a *two-step* task so you can watch it iterate:
> *"Make a folder `notes/`, then inside it create `week1.md` with a bullet list of the three pillars of this course."*

Notice: it **decomposes** the task, **acts**, **checks** the result, and **continues**. That is the agentic loop — the same idea we'll aim at *theological corpora* starting Week 4.

---

## Wrap-up (5 min)

- **We covered:** what the course is (instrument *and* subject), the three pillars (agentic AI · RAG · evaluation), the 14-week / 4-phase mentored-research arc, what makes an LLM an *agent*, and you installed your toolkit.
- **The through-line to remember:** *ground it (RAG), make it act (agent), prove it works (evaluation).*

**Week-1 deliverable — due before Week 2 (5%):**
> A **one-paragraph interest statement**: the tradition, text, or theological question you'd like your project to engage, and *why*. Draft it with your new agent if you like — but write it in your own voice, and (foreshadowing) note anything the agent got wrong.

**Before next week:** skim the Week-2 readings (agents), and make sure your agent still launches (`claude` or `codex`) — we build on it.

---

### Instructor prep checklist
- [ ] Test the live agent demo (or have `theologian_agents/demo.ipynb` output ready as fallback).
- [ ] Confirm the shared model access / accounts work on the lab machines *before* class.
- [ ] Have Node.js LTS installers on a USB stick / local share in case campus network is slow.
- [ ] Decide: are students on their own laptops or lab machines? (Affects install permissions.)
- [ ] Print or post the deliverables/weights table.
- [ ] Bring one plain-chatbot vs. agent example queued up for the "showed its work" moment.
