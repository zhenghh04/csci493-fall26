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

## If you finish early

- Re-run example 4 on a **bigger** model (`/models` → Llama 3.3 70B or `gpt-oss-120b`).
  Does it get the verse right? Does it *refuse*? Compare — that contrast is itself a
  finding.
- Ask opencode to *"add a `--file` argument to `verse_count.py` so it works on any text
  file."* Watch it refactor and re-run its own tests.
