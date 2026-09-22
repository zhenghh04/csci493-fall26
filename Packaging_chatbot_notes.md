# Packaging: from a CLI to a chatbot — instructor notes

**Slides:** `slides/packaging_chatbot.tex` → `packaging_chatbot.pdf` (11 slides)
**Student materials:** `tutorials/week02_alcf_inference/bible_rag/` —
`chat_bible.py`, `chat_bible_gradio.py`, `CHATBOT.md`, `DEPLOY.md`
**Length:** ~30–40 minutes. This is a **segment, not a session.**

## Where to put it

Two good homes; pick one:

- **Tail of the Week 4 RAG lab.** Students have just built the retriever and are
  sitting in front of a working CLI. Wrapping it in a UI is the payoff, takes
  30 minutes, and makes every later demo shareable. *Recommended.*
- **Opening of the Week 11 build sprint.** As the "ship it so a human can use
  it" step before the evaluation push.

The deck is deliberately not numbered `lectureNN` so it can slot into either.
Rename it if you decide it is permanently part of one session.

## The three claims

Everything in the segment serves one of these. If you are short on time, cut
slides, not claims.

1. **Packaging is thin.** The hard part already exists; the UI file *imports*
   it. Anyone who copy-pastes the retrieval code into the UI now has two systems
   that will disagree — and the one they evaluated is not the one they demo.
2. **A good UI shows its work.** A chat bubble looks equally confident whether
   the answer came from the text or from the model's memory. Packaging can make
   a system *less* honest than the CLI it replaced. Ours shows the retrieved
   verses under every answer — that panel *is* the disclosure appendix, live.
3. **Every rung of deployment adds a person you are answerable to.** This is
   where the technical segment turns theological, and it is the part worth
   protecting from the clock.

## Timing

| Time | Slide(s) | What happens |
| --- | --- | --- |
| 0–4 | 2–3 | You built something real; nobody else can use it. Packaging is thin (the "do not touch" box on the diagram is the whole slide). |
| 4–9 | 4 | The design rule: a UI must show its work. Push on *"a polished chatbot can be less honest than a CLI."* |
| 9–13 | 5 | The code. Import · cache · render. Walk it line by line — it is genuinely short, and that is the argument. |
| 13–33 | 6 | **Hands-on.** Launch, ask the three questions, turn the knobs. |
| 33–38 | 7–9 | Streamlit vs Gradio (fast), the deploy ladder, the auth wall. |
| 38–45 | 10–11 | Who is answerable. Wrap. |

Overruns come out of slide 7, never slide 10.

## Talking points

**Slide 3 — "do not touch."** The dashed box around corpus→retriever→answer is
the message. Ask: *if I swap Streamlit for Gradio, how many lines of your RAG
code change?* (Zero. That is how you know the packaging was thin enough. Both
files in the repo prove it.)

**Slide 4 — the honesty inversion.** Worth stating plainly: *the CLI printed the
retrieved verses because printing was all it could do. A chat interface has to
choose to show them.* Most commercial chatbots choose not to. Ask why.

**Slide 6 — the lab.** Watch for the *k* slider moment: cranking k from 2 to 10
makes answers noticeably vaguer. Students usually expect "more context = better"
and are surprised. Let them find it rather than telling them.

The **Hezekiah 3:16** question is the one to do together on the projector. There
is no book of Hezekiah; the grounded side must answer *"Not found in the provided
verses,"* and the ungrounded side will usually invent something. It is the Week 2
lesson, reproduced live, in the interface they just built.

**Slide 9 — the auth wall.** Do not soften this. Students will ask about hosting;
the true answer is that their ALCF credential is a personal ~48 h browser login
and cannot back a hosted app. Saying so is more useful than a workaround that
breaks on Thursday. `DEPLOY.md` says the same thing in writing.

**Slide 10 — the turn.** The line to land: *same code, different moral
situation.* A CLI answers you, who know its limits. A public bot answers a
stranger at 2 a.m. who may read a fluent paragraph with a verse reference as
counsel. Then the corollary: **users read polish as reliability**, so
accountability has to rise *with* usability. Their disclosure has to work harder
precisely as their interface gets better.

If discussion catches fire here, let it. This is the segment's reason to exist,
and it feeds Week 10 (bias-aware evaluation) and the Week 14 disclosure
appendix directly.

## Prep checklist

- [ ] `pip install -r requirements-chatbot.txt` on the teaching machine
      (streamlit + gradio), and **rehearse the launch** — first run downloads
      things you do not want to watch in front of the room.
- [ ] Re-run `python inference_auth_token.py authenticate`. **The token is ~48 h.
      If you authenticated when you prepped, it is dead by class.** This is the
      single most likely way the demo fails.
- [ ] `python build_index_local.py` beforehand if you plan to demo the semantic
      toggle — otherwise it embeds 31,100 verses live, on the projector.
- [ ] Confirm `CHAT_MODEL` in `ask_bible_local.py` is still served (the ALCF set
      rotates). A 404 mid-demo looks like your code failing.
- [ ] Have the screenshot/PDF fallback ready in case the endpoint is down.
- [ ] Decide in advance whether you will demo rung 1 (classroom network). If yes,
      check the room's Wi-Fi allows client-to-client connections — guest networks
      often do not.

## Assignment (as on slide 11)

- Get the chatbot running **on your own corpus** (Week 3), retitled honestly.
- Add a **one-line disclosure** in the sidebar/description: what corpus, whose
  canon, "student project."
- Bring it to the build sprint; demo on rung 1 or 2.

## Known rough edges

- **Gradio API drift.** Gradio 6 removed the `type=` argument to
  `ChatInterface`; the file omits it so it works on 5.x and 6.x. Verified
  against gradio 6.28.0 and streamlit 1.64.0. If a student's copy breaks after
  a future release, that is a teachable instance of the same rot that hits
  `CHAT_MODEL`.
- **No shared deployment.** By design — see the auth wall. If a student's final
  project genuinely needs a hosted bot, it needs a different model backend and a
  separate conversation.
