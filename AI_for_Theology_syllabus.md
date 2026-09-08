# AI for Theological Inquiry — Mentored Research Seminar

**Format:** 14 weeks · one 100-minute session/week
**Type:** Mentored research seminar (students produce an original agentic-AI research project)
**Organizing idea:** AI as a *scholarly instrument* **and** as a *theological subject* — both "agentic AI **for** studying theology" and "what theology says **about** agentic AI."
**Three technical pillars:** **Agentic AI · Retrieval-Augmented Generation (RAG) · Evaluation.**

---

## 1. Course description

This seminar teaches students to use **agentic AI** — systems that plan, use tools, retrieve
sources, and act over multiple steps — as instruments of theological and religious-studies
research, while critically examining the theological and ethical questions autonomous AI raises.
Students learn to *design a research process*: an agent that retrieves primary sources
(**RAG**), cross-references them, drafts with citations, critiques its own output, and — crucially —
is **evaluated** so its claims are checked rather than trusted. Each student (or pair) develops,
executes, evaluates, and defends an original project.

The three pillars build on each other: **agentic AI** is the system, **RAG** is how it stays
grounded in real texts, and **evaluation** is how you know whether any of it is trustworthy —
especially vital where a fabricated scripture reference is a scholarly (and pastoral) failure.

## 2. Learning objectives

By the end of the course a student can:

1. **[Agentic AI]** Explain what turns an LLM into an agent (tool use, memory, plan→act→observe,
   autonomy) and build a multi-step, self-critiquing research agent.
2. **[RAG]** Build a retrieval-augmented pipeline over a theological corpus so the agent cites
   *real* sources, and diagnose where grounding fails.
3. **[Evaluation]** Design and run an evaluation of a RAG/agent system — retrieval quality,
   groundedness/faithfulness, answer relevance, task success, and cost — using golden datasets,
   LLM-as-judge, and human review, while knowing each method's limits.
4. Design a researchable theological question with a matching agentic method **and eval plan**.
5. Analyze the theological questions autonomy raises — personhood, *imago Dei*, agency,
   responsibility, spiritual authority — and report AI-assisted scholarship **honestly**.

## 3. Track decision — Hybrid (low-code default, optional light-code)

Low-code by default: students build with provided notebook templates and a config-driven builder,
keeping the focus on theology and research design. A parallel **light-code (Python) path** offers
the same milestones for technically inclined students. Every lab ships with a working scaffold —
no one writes agents or eval harnesses from scratch.

## 4. Standardized toolkit

| Layer | Default (low-code) | Light-code option |
| --- | --- | --- |
| Model access | Hosted chat model with tool-use (instructor-provided) | Same, via API |
| Agent scaffold | Notebook templates ("research agent," "researcher + fact-checker") | Minimal Python agent loop |
| Retrieval (RAG) | Prebuilt vector-search over the class corpus | Student-assembled components |
| **Evaluation** | Provided eval notebook (golden Q&A set, groundedness + citation checks, LLM-as-judge template) | Same, extensible (e.g. a RAG-eval library) |
| Corpus/sources | Curated digital primary sources (see Week 3) | Same |
| Documentation | Shared trace log + prompt/tool/eval journal | Same |

> **Guest session recommended** around Week 5–6: "How real agentic systems are built *and
> evaluated*" from a practitioner.

## 5. Weekly session shape (100 min)

~40 min concept & discussion · ~40 min hands-on lab · ~20 min project touchpoint (peer review or
mentor check-in). Continuous mentoring, not just in Phase 4.

---

## Phase 1 — Foundations (Weeks 1–3)

### Week 1 — Framing: "AI for Theology"
- **Objective:** Locate the field; articulate a personal research interest.
- **Topics:** Instrument vs. subject; digital humanities, computational text study, AI ethics;
  survey of the AI/religion intersection; preview the three pillars.
- **Hands-on:** Map "questions I care about"; a deliberately naive chatbot query on a doctrine
  question — note what feels off (previews *why* we need RAG + evaluation).
- **Deliverable:** One-paragraph interest statement.
- **Readings:** A survey on AI & religion (e.g. Beth Singler); course intro notes.

### Week 2 — From LLMs to *agents*  [Pillar: Agentic AI]
- **Objective:** Build the core mental model of an agent.
- **Topics:** Next-token prediction, embeddings, hallucination; the step to agency — tool use,
  memory, the plan→act→observe loop, autonomy.
- **Hands-on:** Watch an agent decompose a question and call a tool; diagnose where it errs.
- **Readings:** Wolfram, *What Is ChatGPT Doing …?* (selections); Anthropic, "Building Effective
  Agents" (2024); Weng, "LLM-Powered Autonomous Agents" (2023). *Optional:* Yao et al., "ReAct".

### Week 3 — Sources and the theological corpus
- **Objective:** Understand the data landscape and its theological freight.
- **Topics:** Digital primary sources (original-language scripture, patristics, Qur'anic corpora,
  Talmud, translations, hymnody, sermons); copyright, canon, translation politics; "the data is
  theologically loaded" — and why that shapes both retrieval and evaluation.
- **Hands-on:** Locate and load the corpus each student will use all term.
- **Readings:** Claire Clivaz on digital humanities & biblical studies (selection).

## Phase 2 — Technical Core: Agentic AI · RAG · Evaluation (Weeks 4–7)

### Week 4 — Retrieval-Augmented Generation  [Pillar: RAG]
- **Objective:** Make an agent cite *real* texts, not invented ones.
- **Topics:** Embeddings and semantic search; chunking; the retrieve→augment→generate loop; RAG as
  the agent's key tool; failure modes (bad chunking, wrong retrieval, ignored context).
- **Hands-on:** Build an "ask-your-corpus" RAG agent over a Week-3 text.
- **Readings:** Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
  (2020, the idea, not the math).

### Week 5 — Building a research agent  [Pillar: Agentic AI]
- **Objective:** Turn a RAG tool into a multi-step, self-critiquing research agent.
- **Topics:** Agent design patterns — planning, reflection/self-critique; a two-agent setup
  ("researcher" + "critic/fact-checker") to catch fabricated references; text-analysis techniques
  (semantic search, concept-tracing of *hesed*/*agape*/*grace*) reframed as **tools the agent
  wields**.
- **Hands-on:** Extend Week-4's RAG into a planning + reflection agent; add a fact-checker.
- **Readings:** Shinn et al., "Reflexion" (2023, concept); Wang et al., "A Survey on LLM-based
  Autonomous Agents" (2023, selections). *Guest slot.*

### Week 6 — Evaluation: how do you know it works?  [Pillar: Evaluation]  ★ new
- **Objective:** Measure whether a RAG/agent system is trustworthy.
- **Topics:**
  - **RAG evaluation** — retrieval precision/recall, **groundedness/faithfulness** (is the answer
    supported by retrieved text?), answer relevance, and **citation verification** (does the cited
    verse/passage actually exist and say that?).
  - **Agent evaluation** — task success, trajectory / tool-use correctness, cost & latency
    efficiency, robustness.
  - **Methods** — golden/reference datasets, **LLM-as-judge** and its pitfalls (bias, inconsistency),
    human evaluation, and when to use which.
  - **Theology-specific angles** — doctrinal fidelity, translation sensitivity, and **bias across
    traditions** (whose theology is the "correct answer"?).
- **Hands-on:** Build a small golden Q&A set for your corpus; run groundedness + citation-existence
  checks and an LLM-as-judge pass on Week-5's agent; report a scorecard.
- **Readings:** Es et al., "RAGAS" (2023); Liu et al., "G-Eval" (2023); Zheng et al., "Judging
  LLM-as-a-Judge / MT-Bench" (2023, selections).

### Week 7 — Research design & proposal  (midpoint gate)
- **Objective:** Convert curiosity into a researchable question + agent design + **eval plan**.
- **Topics:** Scope, method, evidence, what counts as a finding; which agent steps and tools; how
  you will **evaluate** and verify claims (metrics, golden set, human check); reproducibility and
  documenting agentic-AI use (prompts, tools, traces, eval).
- **Deliverable:** 1–2 page proposal + 5-min pitch. **Must include an evaluation plan.**
- **Readings:** Research-methods primer (notes); one exemplar agentic-DH study.

## Phase 3 — Domain Deep-Dives + Project Launch (Weeks 8–10)

### Week 8 — AI and hermeneutics
- **Objective:** Interrogate whether an agent can "interpret."
- **Topics:** Multi-step reasoning vs. genuine understanding; authorial intent, tradition, the
  interpretive community; higher stakes when an agent *acts* on interpretation.
- **Hands-on:** Projects formally begin; first evaluated agent runs on the student's question.
- **Readings:** Gadamer, *Truth and Method* (selections); a piece on machine "understanding."

### Week 9 — Theology *of* agentic AI
- **Objective:** Examine personhood and autonomy theologically.
- **Topics:** *Imago Dei*, personhood, consciousness; **agency and autonomy** — moral status,
  responsibility, delegation when a system *acts*; AI and idolatry; eschatology.
- **Hands-on:** Mentored project check-in.
- **Readings:** Herzfeld, *The Artifice of Intelligence* (2023) selections; Dorobantu on AI &
  personhood; Vatican, *Rome Call for AI Ethics* (2020) / *Antiqua et Nova* (2025) selections.

### Week 10 — Ethics, bias, and the limits of autonomy
- **Objective:** Adopt a critical, human-in-the-loop stance (connects back to evaluation).
- **Topics:** Training-data bias (whose theology dominates?); fabricated citations; agentic-specific
  risks — compounding errors across steps, over-trust in an autonomous "researcher,"
  pastoral/spiritual-authority harms; designing human oversight; **bias-aware evaluation**.
- **Hands-on:** Each project adds an explicit verification/oversight step to its eval plan.
- **Readings:** Bender et al., "On the Dangers of Stochastic Parrots" (2021); Crawford, *Atlas of
  AI* (2021, selections).

## Phase 4 — Mentored Research Execution (Weeks 11–13)

### Week 11 — Build sprint (studio)
- **Objective:** Execute the agentic pipeline; troubleshoot traces.
- **Format:** Studio — students build, mentors circulate; structured trace debugging.

### Week 12 — Evaluate & critique  [Pillar: Evaluation, applied]
- **Objective:** Run a real evaluation of your *own* project and defend it.
- **Format:** Students apply Week-6 methods to their systems (scorecard: groundedness, citation
  checks, task success, bias spot-checks); peer-review swap + mentor stress-test of claims and
  AI-reliance.
- **Deliverable:** Preliminary results + **evaluation report** (early-warning checkpoint).

### Week 13 — Write-up & communication
- **Objective:** Turn results into an honest argument.
- **Topics:** Presenting agentic work with integrity — goals, tools, traces, **eval results**,
  failures, human oversight. Draft final paper + slides.

## Week 14 — Symposium
Final presentations (cohort + invited faculty), Q&A, and a closing reflection: **what did the
agent reveal, what did it distort, how well did it hold up under evaluation, and what did this
teach us theologically?**
- **Deliverable:** Final paper + presentation.

---

## 6. Assessment

| Component | Weight | Due |
| --- | --- | --- |
| Participation & project touchpoints | 15% | Weekly |
| Interest statement | 5% | Week 1 |
| Research proposal + pitch (incl. eval plan) | 20% | Week 7 (gate) |
| Preliminary results + evaluation report | 15% | Week 12 |
| Final paper | 30% | Week 14 |
| Final presentation | 15% | Week 14 |

## 7. Rubrics

### Research proposal (Week 7)
- **Question (20%)** — theologically substantive, researchable, well-scoped.
- **Agent design (20%)** — steps, tools, and RAG grounding fit the question.
- **Evaluation plan (25%)** — credible metrics + golden set / human check; awareness of failure
  modes and bias.
- **Feasibility & sources (20%)** — corpus available; scope achievable.
- **Communication (15%)** — clear pitch and writing.

### Final paper (Week 14)
- **Scholarly contribution (25%)** — a real finding or a well-argued negative result.
- **Method & agent design (20%)** — sound, well-documented, reproducible RAG/agent pipeline.
- **Evaluation & critical stance (25%)** — claims measured *and* checked; groundedness/citations
  verified; bias and limits addressed; human-in-the-loop evident.
- **Theological/ethical reflection (15%)** — engages the "AI as subject" questions (Weeks 8–10).
- **Communication (15%)** — structure, clarity, honest reporting of AI use.

### Agentic-AI use disclosure (required in every deliverable)
An appendix in every submission: models/tools used, key prompts, representative **traces**,
**evaluation results/scorecard**, where the agent failed, and how the student verified results.
Undisclosed or unevaluated AI reliance is penalized.

---

## 8. Notes for the instructor
- **Readings are starting points from the instructor's knowledge — verify current editions,
  availability, and access before distributing.** Swap in tradition-appropriate sources
  (Christian / Jewish / Islamic / comparative) to match the cohort.
- **The three pillars are cumulative** — RAG (W4) grounds the agent (W5), and evaluation (W6)
  judges both; keep labs building on the *same* corpus and agent so students see the through-line.
- **Evaluation is the highest-leverage theology-specific skill here** — a fabricated citation is a
  scholarly failure, so budget real time for the golden-set + citation-verification lab.
- **Decide access early:** hosted model + tool-use quota; whether the light-code path needs an
  optional extra lab.
- **Corpus curation is the top prep task** — a clean, rights-clear, well-scoped corpus makes every
  RAG and eval lab work.
