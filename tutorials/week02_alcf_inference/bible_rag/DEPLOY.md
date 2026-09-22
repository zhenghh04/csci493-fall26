# Letting other people use your chatbot

Your chatbot runs on your laptop. This page is about the step after that: making
it reachable by someone who is not you — a classmate, the class, the internet.

Read the **ladder** first, then the **auth wall**, then the **checklist**. The
auth wall is the part that will actually stop you, and no amount of clever
configuration removes it.

---

## The ladder

Each rung adds one more person who can reach your bot — and one more problem
that is now yours.

| Rung | Who can reach it | How | What it costs you |
| --- | --- | --- | --- |
| **0. Localhost** | you | `streamlit run chat_bible.py` | nothing — **this is the right default all term** |
| **1. Your network** | anyone on the same Wi-Fi | `--server.address 0.0.0.0` | your token serves them all; no password |
| **2. Temporary public link** | anyone with the URL | Gradio `--share`, or a tunnel | *public internet*, no password, your token |
| **3. Hosted** | anyone, permanently | Community Cloud / HF Spaces / institutional host | needs a credential you do not have — see below |

### Rung 1 — the classroom network

```bash
# Streamlit
streamlit run chat_bible.py --server.address 0.0.0.0 --server.port 8501

# Gradio
python chat_bible_gradio.py --lan
```

Then find your machine's address (`ipconfig getifaddr en0` on macOS,
`hostname -I` on Linux, `ipconfig` on Windows) and give classmates
`http://<that-address>:8501`.

This is the **best rung for a demo in the room**: nothing leaves the building,
and you can pull the plug by closing the terminal. Your firewall may prompt you
to allow incoming connections — that prompt is accurate; you *are* opening a
port.

### Rung 2 — a temporary public link

```bash
python chat_bible_gradio.py --share     # prints a https://….gradio.live URL, ~1 week
```

For Streamlit there is no built-in equivalent; use a tunnel
(`cloudflared tunnel --url http://localhost:8501`) if you need one.

**Understand what you just did.** That URL is on the open internet with **no
password**. Anyone who sees it — in a screenshot, in a Slack channel, in a
crawler's logs — can ask your bot questions, on your ALCF token, until you stop
the process. Use it for a demo, then **kill the process**. Do not leave it
running overnight.

### Rung 3 — actually hosted

This is where it stops being a configuration problem.

---

## The auth wall (read this before you plan a deployment)

Your ALCF access is a **personal OAuth token**:

- you get it by **logging in through a browser** (`inference_auth_token.py authenticate`),
- it expires in about **48 hours**,
- and every request made with it is **attributed to you and billed to you**.

Three consequences, in increasing order of importance:

1. **It cannot live in a hosting secret store.** You can technically paste a
   token into Streamlit Community Cloud's `st.secrets` or a HF Spaces secret.
   It will stop working in two days, and you will be re-pasting it forever. The
   credential a hosted app needs is a long-lived *service* credential, and the
   ALCF student endpoint does not issue one.
2. **On rungs 1–3, you are the account behind every stranger's question.** Not
   just quota: attribution. If someone uses your public bot to generate
   something you would not want attached to your name, it is attached to your
   name.
3. **A committed token is a leaked token.** `git` remembers. Never paste one
   into a source file, a notebook cell you will commit, or a screenshot.

**So, the honest recommendation for this course:**

> Live on **rung 0**. Use **rung 1** for demo day, or **rung 2** if remote
> people must see it. Treat **rung 3 as out of scope** — if you genuinely need a
> permanently hosted bot for your final project, come talk to me first, because
> it needs a different model backend (one with a real API key you are allowed to
> budget) and a conversation about who is responsible for it.

---

## If you do host it: the disclosure checklist

A deployed theology chatbot is read by people who did not build it and cannot
see its limits. Before anyone but you can reach it, the interface must say:

- [ ] **What corpus it reads** — "King James Version, all 31,100 verses," not "the Bible."
- [ ] **Whose canon that is** — a 66-book Protestant canon is a *choice*; name it (Week 3).
- [ ] **That it is a student project** — not a pastor, not a scholar, not counsel.
- [ ] **That answers must be checked** — and then actually show the retrieved verses, always.
- [ ] **What it will not do** — it cannot see anything outside the corpus, and it says
      *"Not found in the provided verses"* rather than guessing. Say so, so silence
      reads as honesty rather than failure.

Both apps ship with a one-line version of this. **Edit it to match your own
corpus** — a disclosure that describes someone else's data is worse than none.

## And the harder question

Rung 0 answers *you*, and you know what it cannot do. Rung 2 answers a stranger
who may be in real distress at 2 a.m., and who may read a fluent paragraph with
a verse reference as pastoral counsel.

Same code. Different moral situation.

The finish on your interface is itself a claim about how much the output can be
trusted — users read polish as reliability. So accountability has to rise *with*
usability: the better your chatbot looks, the harder your disclosure has to
work. That tension is not an obstacle to the assignment; it **is** the
assignment.

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Classmates get "connection refused" on rung 1 | You bound to `localhost`. Re-launch with `--server.address 0.0.0.0` / `--lan`, and allow the firewall prompt. |
| Rung 1 works for you, not for them | You gave them `localhost:8501` (their own machine) instead of your IP address. |
| `--share` prints a link that 404s after a while | Gradio share links are temporary (~1 week) and die with the process. Re-launch. |
| Everything worked yesterday, all answers now 401 | Your ~48 h token expired. `python inference_auth_token.py authenticate`. This will keep happening — it is the auth wall, not a bug. |
| Hosted app works for 2 days then breaks | Same wall. See above; it does not have a configuration fix. |
