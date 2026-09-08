# CSCI 493 — AI for Theological Inquiry (Fall 2026)

A mentored research seminar at Wheaton College. Students learn to use **agentic AI**
— systems that plan, use tools, retrieve sources, and act over multiple steps — as
instruments of theological and religious-studies research, while critically examining
the theological and ethical questions autonomous AI raises.

**Three technical pillars:** Agentic AI · Retrieval-Augmented Generation (RAG) · Evaluation.

> Instructor: Huihuo Zheng. 14 weeks, one 100-minute session/week.

---

## Repository layout

| Path | What it is |
| --- | --- |
| `AI_for_Theology_syllabus.md` / `.tex` / `.pdf` | Full course syllabus (canonical) |
| `syllabus.md` | Short syllabus overview |
| `Lecture01_notes.md` | Week 1 — course framing, agentic AI, toolkit setup |
| `Lecture02_notes.md` | Week 2 — from LLMs to agents (instructor notes) |
| `slides/` | Beamer decks (`lectureNN.tex` + compiled `lectureNN.pdf`), shared `preamble.tex` / `titlepage.tex`, logos, images |
| `tutorials/` | Hands-on student materials (see below) |
| `readings/` | Assigned papers — **not tracked** (copyright); cited below |

### Tutorials

- **`tutorials/week02_alcf_inference/`** — Getting onto the **ALCF inference endpoint**
  and driving an open-weight LLM directly.
  - `README.md` — one-page student handout (auth → list models → client → experiments).
  - `01_hello_alcf.py` — minimal OpenAI-compatible client against ALCF.
  - `02_simple_rag.py` — retrieve → ground → generate over a tiny corpus.
  - `alcf_inference_demo.ipynb` — guided notebook: hello → temperature sweep →
    hallucination demo → grounding by hand → **simple RAG**.

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

## Assigned readings (not redistributed here)

The reading PDFs are copyrighted and intentionally excluded from this repository.
Obtain them through the publisher or your library:

- Ji et al. (2023), *Survey of Hallucination in Natural Language Generation*, ACM
  Computing Surveys. https://doi.org/10.1145/3571730
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP
  Tasks*, NeurIPS. https://arxiv.org/abs/2005.11401

---

## License / use

Course materials © Huihuo Zheng. Code samples are provided for educational use.
(Add an explicit LICENSE file before wider distribution.)
