# Lecture 4 — Sources & the Theological Corpus: *what* you ground on

**Course:** AI for Theological Inquiry — Mentored Research Seminar
**Session:** 100 min · **Instructor:** Huihuo Zheng · **Slides:** `slides/lecture04.tex` → `lecture04.pdf`
*(Syllabus Week 3 content — "Sources and the theological corpus" — delivered as the 4th
session, after the opencode/vibe-coding bridge. It sets up RAG next week.)*

> **The one-line arc:** *Last week you saw* **why** *you must ground (a fabrication that
> ran green). Today you assemble* **what** *to ground on — and confront that the data
> itself is theologically loaded.*

**Session goal:** every student leaves with (a) the start of a **term corpus** — 3–6
documented, mostly public-domain sources tied to their interest statement — and (b) the
habit of *seeing* the choices already baked into any text they download (canon,
translation, base text, paratext), and disclosing them.

**Rough timing** *(re-cut to make room for the systematic vibe-coding recap — see the
note below the table)*
| Block | Min | What |
|---|---|---|
| 0. Where we are | 3 | One slide of orientation |
| **0b. Vibe coding, systematically** | **15** | **Recap 1–5: definition · loop · the dial · failure modes · the discipline** |
| 1. The pipeline inherits your sources | 5 | Garbage in → grounded-in-garbage out |
| 2. Where public-domain sources live | 5 | Scripture, the Fathers, originals |
| 3. "The data is theologically loaded" | 12 | The four loaded decisions |
| 4. Canon · translation · text · paratext | 10 | Concrete examples |
| 5. Copyright & licensing | 5 | Why public-domain; fair use for research |
| 6. The source card | 4 | Provenance = disclosure applied to data |
| 7. Hands-on: assemble your corpus | 36 | The lab |
| 8. What's missing + touchpoint + assign | 5 | Bias at the corpus; wrap |

> **Where the 15 minutes came from.** Blocks 1, 2, 5 and 6 each lost 1–3 min and the lab
> lost 4 (36 min is still enough — the corpus is homework either way). **Blocks 3–4 were
> not touched**: the four loaded decisions are the heart of this lecture and the recap is
> not worth trading them for. If you fall behind, cut **Recap 4/5** (the failure taxonomy)
> — it is the one recap slide the rest of the arc does not depend on.

---

## Part 1 — Concept (~59 min, incl. the 15-min vibe-coding recap)

### 0. Where we are (3 min)
- Week 2: caught the raw model inventing a verse. Week 3: watched a fabrication get
  **baked into code that ran green**, and named the rule — *ground it, prove it, disclose
  it*. The Luther-capstone RAG turned the model from a **source** (that fabricates) into a
  **finder** (that quotes & cites).
- Then hand off to the recap: *"Before we go forward — last week you did something we
  only had ten minutes to name. Let's do it properly."*

### 0b. Vibe coding, systematically (15 min) — **the new recap block**

Last week vibe coding got **one** concept slide (a two-column "vibe vs. engineering"
table) before the hands-on. That was enough to run the lab, not enough to *think with*.
These five slides give it a spine. The payoff is not nostalgia — it is that **slide 3
(the dial) turns "don't vibe code" into a disclosure rule students can actually follow**,
and slide 5 hands you today's lab rule.

- **Recap 1/5 — what the term actually means.** Read the Karpathy quote aloud; it is
  funnier and more extreme than students remember ("I 'Accept All' always"). Then the
  move that matters: *the term has already drifted* to mean any AI-assisted coding, but
  the original names something precise — **you do not read the code**.
  > **Say it:** *"The definition is not about what the machine did. It's about what you
  > chose not to look at."*

- **Recap 2/5 — the loop, and where you sit in it.** Re-draw `Prompt → Generate → Run →
  Observe → Accept?`, with the self-fix arrow looping back. The two gold YOU markers are
  the whole slide: **you touch the loop exactly twice.** Vibe coding is when the second
  touch goes automatic.
  > **The trap to name:** the loop terminates on *"it ran"*, never on *"it's right."*

- **Recap 3/5 — it is a dial, not a switch.** The L0–L4 ladder. This is the slide to
  spend time on. Ask the room: *"which rung were you on last week?"* (Answer: L3, by
  design.) Land the rule — **no rung is a sin; landing on one by accident is** — and
  connect it to the appendix: *disclose which rung you were on.* This reframes the whole
  course's AI policy as calibration rather than prohibition, which is both truer and
  easier to comply with.

- **Recap 4/5 — five ways vibes fail.** Fabrication is boxed because it's *ours*; the
  other four are a quick read-down. Do not rush #5, **comprehension debt** — it is the
  one that bites a thesis defence. Close with the theological point: **code launders a
  claim.** Same wrong verse; a chat window makes it a guess, a script makes it a result.
  *(This is the cuttable slide if you're behind.)*

- **Recap 5/5 — the discipline, and today's version of it.** *Vibe to explore, verify to
  publish*, then the four moves that promote L3 → L2 (read · ground · test · disclose),
  with the forward pointers to RAG (Wk 4) and eval (Wk 6). The right-hand box is the
  bridge into today: the agent will happily fetch and clean your texts, but it cannot
  tell you **which canon, which translation, which licence** it just handed you.
  > **Hand-off line:** *"Vibe to fetch. Verify to keep."*

**Pivot to today:** grounding retrieves from *real sources* — so the whole question
becomes **which** sources, **whose** text. *"Next week we build the retriever; this week
we decide what it is allowed to find."*

### 1. The pipeline inherits your sources (5 min)
- Draw/point to: **Sources → Clean → Chunk → Embed → Retrieve.** The corpus is the
  **ceiling** on everything the agent can honestly say.
- **Money line:** *"A perfect retriever over the wrong edition cites the wrong text —
  confidently, with a page number."*

### 2. Where sources live (5 min) — prefer public-domain / open
- **Scripture, open:** World English Bible (public domain), KJV, ASV, Darby, YLT — via
  `bible-api.com`, STEP Bible, or plain text.
- **Classics & the Fathers:** CCEL (ccel.org), Project Gutenberg, Sacred-Texts.
- **Originals / critical text:** Perseus (Greek/Latin), SBLGNT, Open Scriptures Hebrew
  Bible — when the original language *is* the object.
- Say it: open sources are **reproducible, redistributable, disclosable** — the same
  values that put us on an open ALCF model.

### 3–4. "The data is theologically loaded" (22 min) — **the heart of the lecture**
Four decisions are *already made* inside any file you download. None is a bug to "fix";
each is a scholarly choice to **name and disclose**.

- **Canon — which books?** Protestant 66 · Catholic 73 (Tobit, Judith, Wisdom, Sirach,
  1–2 Maccabees…) · Orthodox more. *"Download 'the Bible' and you have quietly chosen a
  canon."*
- **Translation — whose words?** Isaiah 7:14: KJV/ESV *"a **virgin** shall conceive"* vs
  NRSV *"a **young woman**"* (Heb. *almah*). Same verse, different doctrine implied — by
  the translator.
- **Text / manuscript — which base text?** Textus Receptus (KJV) vs the critical text
  (NA28). Disputed passages: longer ending of Mark (16:9–20), *pericope adulterae* (John
  7:53–8:11), *Comma Johanneum* (1 John 5:7). Present, bracketed, or footnoted depending
  on your file.
- **Paratext — the editor's hand.** Chapter/verse numbers are **medieval additions**;
  headings, cross-refs, notes are editorial. Chunk "by verse" and you've adopted a 13th-c.
  editor's boundaries as your unit of meaning — a preview of next week's chunking choice.
- **Land it:** the RAG agent answers *"what does the Bible say about X?"* from the canon
  and translation **you loaded**, with no idea it made a choice. *You* have to know which
  Bible is in the box.

### 5. Copyright & licensing (5 min)
- **Decision:** public-domain / open (WEB, KJV, ASV, the Fathers) → embed, redistribute,
  cite freely. Copyrighted (NIV, ESV, NRSV) → limited quoting, **no bulk embedding** into
  a redistributable index.
- **The course default:** build your vector DB on **open** texts. A copyrighted
  translation baked into a shared index is a *licensing* problem, not just a scholarly one.
- Need a modern translation? Quote short excerpts (fair use), keep it **out of the shared
  index**, **disclose** the edition. When in doubt, ask.

### 6. The source card (4 min)
- A corpus is not a folder of files — it's files **plus a record of what they are**. One
  card per text: work & author · edition/translation · where-from URL + date accessed ·
  license · canon/base-text (if scripture) · known gaps.
- **This *is* the disclosure appendix, applied to the data, before a single query.**
  Provenance you write now is provenance you don't reconstruct in Week 14.

---

## Part 2 — Hands-on: assemble *your* term corpus (~36 min)

1. Start from your **interest statement** (Wk 1): what texts must the agent see?
2. Find **3–6 sources**, public-domain first.
3. Download to `corpus/` as clean `.txt`.
4. Write a **source card** for each.
5. Note **one loaded decision** you inherited (canon / translation / base text / paratext).

- **Let the agent help, then check.** opencode can download & clean (like the Luther
  capstone) — but *you* verify the edition and license. **Vibe to fetch, verify to keep.**
- **Start small.** A tight, well-documented corpus beats a huge, murky one; grow it toward
  the Week 7 proposal.

**Circulate and ask each student:** *which* canon/edition did you pick, and did you notice?

---

## Wrap-up (5 min)

- **What's *not* in your corpus is a claim too.** Silent exclusions — one tradition, one
  century, English-only — and the agent speaks fluently about what it cannot see, never
  saying so. Write the corpus's **scope & limits** into the record. That honesty is graded,
  and it's good scholarship. (Bias enters at the corpus, long before the model — we return
  to bias-aware eval in Week 10.)
- **Touchpoint:** the corpus is the evidence base for the Week 7 proposal. If you can't
  find sources for your question, the question needs reshaping — better to learn that now.

**Deliverable — due before next week:**
> 1. A `corpus/` of **3–6 public-domain sources** + a **source card** for each.
> 2. **One paragraph:** a loaded decision you inherited, and your corpus's scope & limits.

**Reading:** Claire Clivaz on digital humanities & biblical studies (selection) — how the
medium reshapes the text.

**Next week:** **RAG** — retrieve → augment → generate over the corpus you just built.

---

### Instructor prep checklist
- [ ] **Recap block:** have last week's **actual fabrication** (the wrong Philemon 1:6 a
      student or you generated) to hand. Recap 4/5 is far stronger pointed at a real
      artifact from *this* room than at the abstraction.
- [ ] **Recap 3/5 (the dial):** decide in advance what rung *you* will permit for the
      term-project code, so the "name your rung" rule has an answer when someone asks.
- [ ] Have **one live public-domain fetch** ready to demo (e.g. WEB via `bible-api.com`, or
      a Luther work from Gutenberg) in case student network/auth stalls.
- [ ] Put the **Isaiah 7:14** KJV-vs-NRSV comparison on a slide/handout — the cleanest
      "translation is theology" moment. Have one disputed-passage example (Mark 16:9–20 or
      John 7:53–8:11) ready to show bracketed vs not across two editions.
- [ ] Have a **blank source-card template** to hand out (fields listed above).
- [ ] Pre-check that `opencode` + ALCF still works from last week for the fetch-and-clean
      step (token refresh, live model ID).
- [ ] Reserve time to help students whose **interest statement is too broad** to source —
      that reshaping is the real value of the touchpoint.
