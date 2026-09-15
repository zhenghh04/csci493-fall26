# Hands-on: vibe-coding warm-ups (start here)

*AI for Theological Inquiry · opencode + ALCF lab*

You've wired opencode to an ALCF model (see [`README.md`](README.md)). Now **describe
tasks in plain language** and watch the agent plan → write → run → self-correct. Do
these in order — each adds one habit. Type the **prompt** into opencode; don't write
code yourself.

> Reference solutions live in [`solutions/`](solutions/) — an *answer key* and a
> projector fallback. The lesson is to have opencode generate these live, then
> compare.

---

## 1. Plot sin(x) — feel the loop (5 min)

> **Prompt:** *"Write a Python program `plot_sin.py` that plots sin(x) from 0 to 2π
> with matplotlib and saves it to `sin.png`. Then run it."*

**Watch for:** if `matplotlib` isn't installed, the agent sees the `ModuleNotFoundError`,
**installs it, and re-runs** — that self-correction *is* the plan→act→observe loop. On a
headless machine it should use a non-interactive backend (`matplotlib.use("Agg")`) so
saving works without a display.

**Check:** open `sin.png`. Is it actually one full sine wave over $[0, 2\pi]$? You just
shipped working code without typing a line — note how that felt.

---

## 2. Sort a list of integers — and *test* it (10 min)

> **Prompt:** *"Write `sort_and_test.py` with a function `sort_ints(nums)` that returns
> the integers sorted ascending. Add pytest tests covering: empty list, already-sorted,
> reverse-sorted, duplicates, and negative numbers. Run the tests and show me they pass."*

**Watch for:** the agent writes both the function **and** the tests, runs `pytest`, and
if anything fails it **reads the failure and fixes it** — the loop again, now with a
verifier attached. This is the habit the whole course is built on: *don't just run it,
test it.*

**Then push on it (the important part):**

> **Prompt:** *"Now add a test for a list with one element, and a test that sorts
> `[10, 2, 33, 4]` — do those pass?"*

**Check:** green tests mean *the cases you thought of* pass. They do **not** prove the
function is right for cases you *didn't* think of. Hold that thought — it's the whole
point of example 4.

---

## 3. Count words in a text file — your first text tool (10 min)

> **Prompt:** *"Write `verse_count.py` that reads a text file of verses (one per line)
> and prints the 10 most frequent words, ignoring common stop-words. Run it on
> `sample.txt`."* (`sample.txt` ships in this folder.)

**Watch for:** the agent invents a stop-word list, tallies, sorts, and runs. **Now read
the code it wrote** — do you agree with *which* words it treats as stop-words? That
choice is a research decision the agent made silently on your behalf.

---

## 4. The trap: green code that's confidently wrong (10 min)

Everything above *ran green*. Now aim the same tool at a **factual** claim:

> **Prompt:** *"Add a function `philemon_1_6()` that returns the exact text of
> Philemon 1:6 as a string, from memory — no file, no internet. Add a test asserting it
> returns a non-empty string, and run it."*

**What happens:** the test **passes** (the string is non-empty) — but the verse text is
very likely **fabricated**, in fluent biblical cadence. This is last week's
hallucination, now **baked into code that runs green.**

**Do this and keep it:**
1. Look up the *real* Philemon 1:6 (any print/edition).
2. Diff it against what the model hard-coded.
3. Save the **prompt**, the **generated (wrong) verse**, and the **real verse**. That's
   a disclosure-appendix artifact.

> **The lesson to write down:** *a passing test proves the code runs, not that it's
> true.* Vibe to **explore**; **verify** (read it, ground it, test it against a real
> source, disclose it) before anything you'd cite.

---

# Capstone (more complex): build a Luther vector database

Now put it together into a real research tool: **download Martin Luther's writings,
build a vector database over them, and ask it questions** — the model answers *only*
from Luther's actual words, with citations. This is **RAG on a real corpus** (the whole
point of Week 4), and you'll build it by *describing* it to opencode, one step at a time.

**What you're building (the pipeline):**

```
download  →  clean  →  chunk  →  embed  →  store in a vector DB  →  retrieve + ground
 (texts)    (strip     (small   (vectors)   (searchable index)      (answer from Luther,
            boilerplate) passages)                                   with citations)
```

**A "vector database" in one breath:** it stores each passage as an **embedding** (the
"meaning as geometry" vector from Week 2) and, given a question's embedding, returns the
**nearest** passages fast. That retrieve step is what turns a pile of text into something
the model can answer *from* instead of *making up*.

### The corpus — real, public-domain Luther (Project Gutenberg)

All of these are authored by Martin Luther and free to download. The plain-text URL for
any Gutenberg book is `https://www.gutenberg.org/cache/epub/<ID>/pg<ID>.txt`:

| Gutenberg ID | Work |
|---|---|
| 274  | *Disputation on the Power of Indulgences* — **the 95 Theses** |
| 1911 | *Concerning Christian Liberty* (The Freedom of a Christian) |
| 418  | *A Treatise on Good Works* |
| 1722 | *Luther's Large Catechism* |
| 273  | *The Smalcald Articles* |
| 272  | *An Open Letter on Translating* |
| 9841 | *Selections from the Table Talk of Martin Luther* |
| 1549 | *Commentary on the Epistle to the Galatians* |

*(~1.6 MB total — small enough to embed during class.)*

### Step 1 — Download and clean

> **Prompt:** *"Write `download_luther.py` that downloads these Project Gutenberg works
> as plain text and saves each to a `corpus/` folder named by its title: IDs 274, 1911,
> 418, 1722, 273, 272, 9841, 1549 (URL pattern
> `https://www.gutenberg.org/cache/epub/<ID>/pg<ID>.txt`). Strip the Project Gutenberg
> header and footer (the `*** START OF ... ***` / `*** END OF ... ***` markers) so only
> Luther's text remains. Run it and report how many files and total words you saved."*

**Check:** open one file in `corpus/`. Is the legal boilerplate gone? Is it really Luther?

### Step 2 — Chunk into passages

> **Prompt:** *"Write `chunk.py` that splits every file in `corpus/` into overlapping
> passages of about 800 characters with 150 characters of overlap, breaking on paragraph
> boundaries where possible. Keep each chunk's source work and a running index as
> metadata. Print the total number of chunks."*

**Why chunk?** A whole treatise is too big to embed or cite usefully. Passages are the
unit you retrieve and quote. **Read a few chunks** — did it split mid-sentence? That
choice affects every later answer.

### Step 3 — Embed and store in a vector database

> **Prompt:** *"Write `build_vectordb.py` that embeds every chunk and stores it in a
> persistent **Chroma** vector database (`pip install chromadb`) in `./luther_db`, with
> the passage text and its source-work metadata. Use Chroma's built-in (local) embedding
> model so it works offline. Print how many vectors are in the collection when done."*

**Check:** re-running it shouldn't re-embed from scratch — a database *persists*. Ask
opencode to make the build **idempotent** (skip work already indexed).

> **Optional (ALCF embeddings):** if `list-endpoints` shows an embedding model (e.g. one
> with `embed` in its name), have opencode add a `--backend alcf` option that computes
> embeddings through the ALCF endpoint instead of the local model, and compare retrieval
> quality. Embeddings on ALCF are not always served — the local backend is the reliable
> default.

### Step 4 — Ask Luther (retrieve + ground)

> **Prompt:** *"Write `ask_luther.py <question>` that embeds the question, retrieves the
> 5 most similar passages from the Chroma DB, and asks the ALCF chat model to answer
> using **only** those passages — quoting Luther and citing the work each quote comes
> from. If the answer isn't in the retrieved passages, it must say so. Use my ALCF client
> settings from `opencode.json` (base URL + `ALCF_TOKEN`). Then run it on: 'What does
> Luther say about faith and good works?'"*

**Watch the whole loop pay off:** the answer is now grounded in *retrieved Luther*, with
citations you can open and check.

### Step 5 — The integrity test (the reason we did all this)

Ask three questions and compare:

1. **In the corpus:** *"What is Luther's view of indulgences?"* → grounded, cited answer.
2. **Not in the corpus:** *"What did Luther say about the internet?"* → it should
   **refuse** ("not in the provided passages"), **not** invent a quote.
3. **A checkable quote:** *"Quote a thesis from the 95 Theses about repentance."* → open
   the cited passage in `corpus/` and confirm the quote is **verbatim**, not paraphrased.

> **The payoff to write down:** RAG turns the model from a *source* (that fabricates)
> into a *finder* (that quotes and cites). The scholar stays in charge of the text — and
> can **check every claim**. That is the difference between vibe-coding a toy and building
> a research instrument.

**Dependencies opencode will install as it goes:** `requests` (download), `chromadb`
(vector DB + local embeddings), `openai` (ALCF chat). Generation needs a fresh
`ALCF_TOKEN` (see the handout); embeddings run locally.

---

## If you finish early

- Re-run example 4 on a **bigger** model (`/models` → Llama 3.3 70B or `gpt-oss-120b`).
  Does it get the verse right? Does it *refuse*? Compare — that contrast is itself a
  finding.
- Ask opencode to *"add a `--file` argument to `verse_count.py` so it works on any text
  file."* Watch it refactor and re-run its own tests.
