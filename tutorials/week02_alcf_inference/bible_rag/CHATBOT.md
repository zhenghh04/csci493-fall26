# Package your RAG system as a chatbot

You built a real RAG system in `ask_bible.py` / `ask_bible_local.py` — but it
lives at the command line, one question at a time. This step turns it into a
**web chatbot** anyone can use in a browser.

> **The point of this exercise:** *packaging is thin.* You are not rewriting
> the hard part. The retriever, the grounded prompt, and the model call already
> exist — `chat_bible.py` just **imports** them and puts a UI on top. That is
> what "packaging" means: making working code usable by someone who will never
> read it.

## The one design rule that matters for this course

A chatbot is a black box unless it shows its work. So this UI **always displays
the verses it retrieved**, right under each answer, and can show the
**ungrounded** answer side by side. The interface enforces the Week 2 lesson —
*don't trust, verify* — and gives you exactly what the disclosure appendix in
every deliverable asks for: what the agent retrieved, what it answered, and
where it would have gone wrong without grounding.

## Run it

```bash
# 1. one new dependency (on top of what the RAG lab already needed)
pip install -r requirements-chatbot.txt

# 2. corpus + token (skip if you already did the RAG lab)
python get_bible.py
python inference_auth_token.py authenticate      # browser login, ~48h token

# 3. launch — opens in your browser (default http://localhost:8501)
streamlit run chat_bible.py
```

Ask away. Good first questions:

- *Quote John 3:16 exactly.* — grounded quotes it; ungrounded paraphrases.
- *What does Micah 6:8 require of us?*
- *What does Hezekiah 3:16 say?* — **there is no book of Hezekiah.** A grounded
  system must reply *"Not found in the provided verses."* Watch the ungrounded
  answer invent one.

## The controls (sidebar)

| Control | What it does | Why it's here |
| --- | --- | --- |
| **Semantic retrieval** | BM25 keyword search (off) vs. local embeddings (on) | The retrieval trade-off from the RAG lab, now a live toggle. |
| **Verses to retrieve (k)** | How many verses feed the model | Too few → misses; too many → dilutes. A real tuning knob. |
| **Also show the ungrounded answer** | Runs the *same* model with no retrieval | Makes the with/without-RAG lesson visible on your own questions. |

## How the packaging works (read the code — it's short)

`chat_bible.py` does only three things beyond your existing code:

1. **Imports** your retriever + answer functions from `ask_bible_local.py`.
2. **Caches** the retriever with `@st.cache_resource` so Streamlit doesn't
   rebuild the index on every message.
3. **Renders** the conversation, the answer, and — the important part — the
   retrieved verses.

That's it. If you can read `ask_bible_local.py`, you can read `chat_bible.py`.

## Make it yours (extensions, easy → harder)

- **Rebrand** for *your* corpus: change the title/caption and point
  `ask_bible_local.py` at your own term corpus instead of the KJV.
- **Stream** the answer token-by-token (`stream=True` on the chat call) for a
  more "live" feel.
- **Show the score bar** or highlight the retrieved reference inside the answer.
- **Deploy** so classmates can use it — see **[DEPLOY.md](DEPLOY.md)**. Short
  version: your ALCF token is personal and expires in ~48 h, so a permanently
  hosted bot needs a credential you do not have. Demo on your own network
  instead.

## Alternative front end: Gradio

`chat_bible_gradio.py` is the same chatbot in Gradio. It imports the **identical
three functions** from `ask_bible_local.py` — which is the point of the whole
exercise: the framework is interchangeable because the packaging layer is thin.

```bash
python chat_bible_gradio.py             # http://127.0.0.1:7860
python chat_bible_gradio.py --embed     # semantic retrieval instead of BM25
python chat_bible_gradio.py --share     # temporary PUBLIC link — read DEPLOY.md first
```

| | Streamlit (`chat_bible.py`) | Gradio (`chat_bible_gradio.py`) |
| --- | --- | --- |
| Feel | dashboard: sidebar, live toggles | chat-first, fewer lines |
| Sources shown as | an expander under each answer | a `<details>` block under each answer |
| Settings | always-visible sidebar | a collapsed "Retrieval settings" accordion |
| Sharing | needs a tunnel | `--share` gives a temporary public URL |

Either is a fine choice. Run both once and notice how little of your code had to
change — that is the measure of good packaging.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: streamlit` | `pip install -r requirements-chatbot.txt` |
| `401 Unauthorized` on send | Token expired → `python inference_auth_token.py authenticate` |
| Model ID 404 | Served set rotates → update `CHAT_MODEL` in `ask_bible_local.py` |
| Semantic toggle is slow the first time | It embeds the Bible once; run `python build_index_local.py` beforehand to cache it |
| Browser didn't open | Copy the `http://localhost:8501` URL from the terminal |
| Gradio: `unexpected keyword argument 'type'` | You are editing the file — Gradio 6 removed `type=`; leave it out |
| Classmates can't reach your app | It is bound to localhost by design — see [DEPLOY.md](DEPLOY.md) |
