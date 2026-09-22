# CSCI 493 — AI for Theological Inquiry (Fall 2026)

A mentored research seminar at Wheaton College. Students learn to use **agentic AI**
— systems that plan, use tools, retrieve sources, and act over multiple steps — as
instruments of theological and religious-studies research, while critically examining
the theological and ethical questions autonomous AI raises.

**Three technical pillars:** Agentic AI · Retrieval-Augmented Generation (RAG) · Evaluation.

> Instructor: Huihuo Zheng. 14 weeks, one 100-minute session/week.

### Start here

| | |
| --- | --- |
| 📘 **Syllabus (canonical)** | [`AI_for_Theology_syllabus.md`](AI_for_Theology_syllabus.md) · [PDF](AI_for_Theology_syllabus.pdf) · [LaTeX source](AI_for_Theology_syllabus.tex) |
| 📄 Short syllabus overview | [`syllabus.md`](syllabus.md) |
| 🗓️ Week-by-week schedule | [jump to the table](#week-by-week-schedule) |
| 📚 Week-by-week readings | [jump to the list](#readings-by-week) |
| 💻 Hands-on tutorials | [`tutorials/`](tutorials/) |

---

## Week-by-week schedule

Weekly session shape (100 min): ~40 min concept & discussion · ~40 min hands-on lab ·
~20 min project touchpoint.

> **On numbering:** slide decks are numbered by **session delivered**, which has drifted
> one ahead of the **syllabus week** since the opencode/vibe-coding bridge was inserted
> after Week 2. So syllabus Week 3 is deck `lecture04`. The table below is keyed to
> **syllabus weeks**; the Slides column names the actual file.

### Phase 1 — Foundations

| Week | Topic | Slides | Instructor notes | Hands-on lab | Readings |
| :--: | --- | --- | --- | --- | --- |
| 1 | Framing: "AI for Theology" — instrument vs. subject | [`lecture01.pdf`](slides/lecture01.pdf) · [`.tex`](slides/lecture01.tex) | [`Lecture01_notes.md`](Lecture01_notes.md) | VS Code + Claude Code / Codex setup | [W1](#week-1) |
| 2 | From LLMs to *agents* · **[Agentic AI]** | [`lecture02.pdf`](slides/lecture02.pdf) · [`.tex`](slides/lecture02.tex) | [`Lecture02_notes.md`](Lecture02_notes.md) | [`week02_alcf_inference/`](tutorials/week02_alcf_inference/) — ALCF endpoint, temperature sweep, hallucination demo | [W2](#week-2) |
| — | *Bridge session:* coding agents on an open model & vibe coding | [`lecture03.pdf`](slides/lecture03.pdf) · [`.tex`](slides/lecture03.tex) | [`Lecture_opencode_vibe_notes.md`](Lecture_opencode_vibe_notes.md) | [`opencode_vibe_coding/`](tutorials/opencode_vibe_coding/) — opencode + ALCF, vibe-coding ladder, Luther-corpus capstone | — |
| 3 | Sources and the theological corpus | [`lecture04.pdf`](slides/lecture04.pdf) · [`.tex`](slides/lecture04.tex) | [`Lecture04_notes.md`](Lecture04_notes.md) | Locate and load your term corpus | [W3](#week-3) |

### Phase 2 — Technical Core: Agentic AI · RAG · Evaluation

| Week | Topic | Slides | Instructor notes | Hands-on lab | Readings |
| :--: | --- | --- | --- | --- | --- |
| 4 | Retrieval-Augmented Generation · **[RAG]** | *not yet written* | *not yet written* | [`bible_rag/`](tutorials/week02_alcf_inference/bible_rag/) — full RAG over 31,100 KJV verses | [W4](#week-4) |
| 4½ | *Segment (~30–40 min):* packaging a RAG system as a chatbot | [`packaging_chatbot.pdf`](slides/packaging_chatbot.pdf) · [`.tex`](slides/packaging_chatbot.tex) | [`Packaging_chatbot_notes.md`](Packaging_chatbot_notes.md) | [`CHATBOT.md`](tutorials/week02_alcf_inference/bible_rag/CHATBOT.md) · [`DEPLOY.md`](tutorials/week02_alcf_inference/bible_rag/DEPLOY.md) | — |
| 5 | Building a research agent · **[Agentic AI]** | *not yet written* | *not yet written* | Extend Week-4 RAG into planning + reflection; add a fact-checker | [W5](#week-5) |
| 6 | Evaluation: how do you know it works? · **[Evaluation]** | *not yet written* | *not yet written* | Golden Q&A set; groundedness + citation-existence checks; LLM-as-judge scorecard | [W6](#week-6) |
| 7 | Research design & proposal — **midpoint gate** | *not yet written* | *not yet written* | **Deliverable:** 1–2 page proposal + 5-min pitch (must include an eval plan) | [W7](#week-7) |

### Phase 3 — Domain Deep-Dives + Project Launch

| Week | Topic | Slides | Instructor notes | Hands-on lab | Readings |
| :--: | --- | --- | --- | --- | --- |
| 8 | AI and hermeneutics | *not yet written* | *not yet written* | Projects formally begin; first evaluated agent runs | [W8](#week-8) |
| 9 | Theology *of* agentic AI | *not yet written* | *not yet written* | Mentored project check-in | [W9](#week-9) |
| 10 | Ethics, bias, and the limits of autonomy | *not yet written* | *not yet written* | Add an explicit verification/oversight step to your eval plan | [W10](#week-10) |

### Phase 4 — Mentored Research Execution

| Week | Topic | Slides | Instructor notes | Hands-on lab | Readings |
| :--: | --- | --- | --- | --- | --- |
| 11 | Build sprint (studio) | *not yet written* | *not yet written* | Studio: build + structured trace debugging | — |
| 12 | Evaluate & critique · **[Evaluation, applied]** | *not yet written* | *not yet written* | **Deliverable:** preliminary results + evaluation report | — |
| 13 | Write-up & communication | *not yet written* | *not yet written* | Draft final paper + slides | — |
| 14 | **Symposium** | *not yet written* | *not yet written* | **Deliverable:** final paper + presentation | — |

---

## Readings by week

The reading PDFs are copyrighted and **intentionally excluded** from this repository
(`readings/*.pdf` is gitignored). Obtain them through the publisher or the Wheaton
library; links below go to the publisher or author's copy.

<a id="week-1"></a>
### Week 1 — Framing
- A survey on AI & religion — e.g. Beth Singler (selection).
- Course intro notes — [`Lecture01_notes.md`](Lecture01_notes.md).

<a id="week-2"></a>
### Week 2 — From LLMs to agents
- Wolfram, [*What Is ChatGPT Doing … and Why Does It Work?*](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/) (2023, selections).
- Anthropic, [*Building Effective Agents*](https://www.anthropic.com/engineering/building-effective-agents) (2024).
- Weng, [*LLM-Powered Autonomous Agents*](https://lilianweng.github.io/posts/2023-06-23-agent/) (2023).
- *Optional:* Yao et al., [*ReAct: Synergizing Reasoning and Acting in Language Models*](https://arxiv.org/abs/2210.03629) (2022).
- *Background:* Ji et al., [*Survey of Hallucination in Natural Language Generation*](https://doi.org/10.1145/3571730), ACM Computing Surveys (2023).

<a id="week-3"></a>
### Week 3 — Sources and the theological corpus
- Claire Clivaz on digital humanities & biblical studies (selection).

<a id="week-4"></a>
### Week 4 — RAG
- Lewis et al., [*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401), NeurIPS (2020) — the idea, not the math.

<a id="week-5"></a>
### Week 5 — Building a research agent
- Shinn et al., [*Reflexion: Language Agents with Verbal Reinforcement Learning*](https://arxiv.org/abs/2303.11366) (2023, concept).
- Wang et al., [*A Survey on LLM-based Autonomous Agents*](https://arxiv.org/abs/2308.11432) (2023, selections).

<a id="week-6"></a>
### Week 6 — Evaluation
- Es et al., [*RAGAS: Automated Evaluation of Retrieval Augmented Generation*](https://arxiv.org/abs/2309.15217) (2023).
- Liu et al., [*G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*](https://arxiv.org/abs/2303.16634) (2023).
- Zheng et al., [*Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*](https://arxiv.org/abs/2306.05685) (2023, selections).

<a id="week-7"></a>
### Week 7 — Research design & proposal
- Research-methods primer (course notes).
- One exemplar agentic digital-humanities study.

<a id="week-8"></a>
### Week 8 — AI and hermeneutics
- Gadamer, *Truth and Method* (selections).
- A piece on machine "understanding."

<a id="week-9"></a>
### Week 9 — Theology *of* agentic AI
- Herzfeld, *The Artifice of Intelligence* (2023, selections).
- Dorobantu on AI & personhood.
- Vatican, *Rome Call for AI Ethics* (2020) / *Antiqua et Nova* (2025, selections).

<a id="week-10"></a>
### Week 10 — Ethics, bias, and the limits of autonomy
- Bender et al., [*On the Dangers of Stochastic Parrots*](https://doi.org/10.1145/3442188.3445922), FAccT (2021).
- Crawford, *Atlas of AI* (2021, selections).

> Weeks 11–14 are studio / project-execution sessions with no assigned readings.
> Of the above, only the Ji (2023) and Lewis (2020) PDFs are currently staged in the
> instructor's local `readings/` folder.

---

## Repository layout

| Path | What it is |
| --- | --- |
| `AI_for_Theology_syllabus.md` / `.tex` / `.pdf` | Full course syllabus (canonical) |
| `syllabus.md` | Short syllabus overview |
| `Lecture01_notes.md` | Week 1 — course framing, agentic AI, toolkit setup |
| `Lecture02_notes.md` | Week 2 — from LLMs to agents (instructor notes) |
| `Lecture_opencode_vibe_notes.md` | Coding agents on an open model & vibe coding (instructor notes; slides `lecture03`) |
| `Lecture04_notes.md` | Week 3 — sources & the theological corpus (instructor notes) |
| `Packaging_chatbot_notes.md` | ~30–40 min **segment** — packaging a RAG system as a chatbot (slides `packaging_chatbot`) |
| `slides/` | Beamer decks (`lectureNN.tex` + compiled `lectureNN.pdf`), shared `preamble.tex` / `titlepage.tex`, logos, images |
| `tutorials/` | Hands-on student materials (see below) |
| `readings/` | Assigned papers — **not tracked** (copyright); cited above |

### Tutorials

- **`tutorials/week02_alcf_inference/`** — Getting onto the **ALCF inference endpoint**
  and driving an open-weight LLM directly.
  - `README.md` — one-page student handout (auth → list models → client → experiments).
  - `01_hello_alcf.py` — minimal OpenAI-compatible client against ALCF.
  - `02_simple_rag.py` — retrieve → ground → generate over a tiny corpus.
  - `alcf_inference_demo.ipynb` — guided notebook: hello → temperature sweep →
    hallucination demo → grounding by hand → **simple RAG**.
  - `bible_rag/` — the **full RAG system** over all 31,100 KJV verses, and its
    packaging into a chatbot.
    - `get_bible.py` → `kjv.json`; `build_index_local.py` caches local embeddings.
    - `ask_bible.py` / `ask_bible_local.py` — the CLI: **without RAG vs with RAG**,
      BM25 or local sentence-transformers retrieval, grounded answers that quote,
      cite, and refuse. *This is the asset; everything below only wraps it.*
    - `chat_bible.py` (Streamlit) and `chat_bible_gradio.py` (Gradio) — two
      interchangeable chatbot UIs that **import** the same three functions and
      always display the retrieved verses under each answer.
    - `CHATBOT.md` — student handout for the packaging segment.
    - `DEPLOY.md` — the deployment ladder, the ~48 h personal-token wall, and the
      disclosure checklist for letting other people use your bot.
- **`tutorials/opencode_vibe_coding/`** — Wiring an open **ALCF model into a coding
  agent** ([opencode](https://opencode.ai)), then **vibe coding** — and the discipline
  it demands.
  - `README.md` — one-page student handout (token → `opencode.json` → `/models` →
    vibe-code → the integrity tension).
  - `opencode.json` — ready-to-use ALCF provider config (OpenAI-compatible), with a
    menu of chat models selectable via `/models`, including Inkling BF16 and
    Nemotron 3 Ultra (Minerva), plus Nemotron 3 Super 120B (Sophia).
  - [Desktop app setup](tutorials/opencode_vibe_coding/desktop_setup.md) — connect
    OpenCode to Sophia/Metis/Minerva, refresh credentials, and troubleshoot authentication.
  - `examples.md` — graded hands-on ladder: plot sin(x) → sort + test → count words →
    the factual trap → **capstone**: download Martin Luther's writings and build a
    vector database (RAG with citations).
  - `solutions/` — reference implementations (`plot_sin.py`, `sort_and_test.py`) as
    answer key / projector fallback.
  - `set_alcf_token.sh` — `source` it to export a fresh `ALCF_TOKEN` before launch.
  - `sample.txt` — tiny verse corpus so the vibe-coding demo runs out of the box.

---

## Building the slides

The decks use XeLaTeX (metropolis theme, FontAwesome icons):

```bash
cd slides
xelatex lecture02.tex && xelatex lecture02.tex   # run twice for the nav bar
```

Compiled PDFs are committed for convenience, so students without a LaTeX toolchain
can read them directly.

## Running the tutorials

Students need an **ALCF account** (already provisioned) and Python with `openai`:

```bash
pip install openai
# one-time auth (Globus browser flow; token good ~48h):
wget https://raw.githubusercontent.com/argonne-lcf/inference-endpoints/refs/heads/main/inference_auth_token.py
python inference_auth_token.py authenticate
python tutorials/week02_alcf_inference/01_hello_alcf.py
```

See `tutorials/week02_alcf_inference/README.md` for the full walkthrough and a
troubleshooting table. Model IDs on the endpoint rotate — confirm the current
served model with `list-endpoints` before class.

---

## OpenCode terminal setup for students

Follow the [coding-agent lab README](tutorials/opencode_vibe_coding/README.md)
for the complete setup. The tested setup uses:

1. The **official OpenCode 1.18.31 binary**, installed with the pinned command in
   the lab README. Check the executable path as well as its version; the Homebrew
   1.18.30 build encountered a startup crash in our September 15, 2026 check.
2. A fresh **`ALCF_TOKEN`**, exported using `inference_auth_token.py` in the same
   terminal that launches OpenCode.
3. The lab's **`opencode.json`** in the project folder, followed by the short
   `opencode run` verification in step 4.

After refreshing a token, restart OpenCode. For the standalone desktop app, use
[the desktop setup guide](tutorials/opencode_vibe_coding/desktop_setup.md), which
also covers launching from the Dock/Finder.


### Coding with Inkling and Nemotron

The lab configuration includes **Inkling BF16**, **Nemotron 3 Ultra**, and
**Nemotron 3 Super 120B**. After completing the token setup above, run these
commands from the repository root:

```bash
cd tutorials/opencode_vibe_coding
# First choice to try for coding:
opencode --model alcf_minerva/inkling-bf16
# Alternative on Minerva:
opencode --model alcf_minerva/nemotron-3-ultra
# Nemotron variant on Sophia:
opencode --model alcf/nvidia/nemotron-3-super-120b
```

Run one OpenCode command at a time, or switch models with `/models` inside the
app. Each provider uses the same `ALCF_TOKEN`.

**Why try Inkling first?** Thinking Machines' published coding evaluations favor
Inkling over Nemotron 3 Ultra. This is a recommendation based on the
[Inkling model card](https://huggingface.co/thinkingmachines/Inkling#5-evaluations),
not a completed comparison on our ALCF deployment. Verify file editing and tool
use on a small task before using either model for a larger assignment.

For the benchmark comparison, configuration details, and switching instructions,
see [Advanced models: Inkling and Nemotron](tutorials/opencode_vibe_coding/README.md#advanced-models-inkling-and-nemotron).
The introductory lab still defaults to Llama 3.1 8B.

---

## License / use

Course materials © Huihuo Zheng. Code samples are provided for educational use.
(Add an explicit LICENSE file before wider distribution.)
