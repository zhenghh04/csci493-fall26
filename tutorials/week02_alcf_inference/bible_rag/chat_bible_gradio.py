#!/usr/bin/env python3
"""
Ask the Bible -- the Gradio version of the same chatbot.

This is the SHORT door into packaging. `chat_bible.py` (Streamlit) and this file
do the identical thing and import the identical three functions from your own
RAG system:

    from ask_bible_local import build_retriever, ask_rag, ask_plain

That is the lesson, made concrete: the UI framework is interchangeable, because
the packaging layer is thin. Your retriever is the asset; this file is a shell.

Streamlit vs Gradio -- pick either:
  * Streamlit  sidebar + expanders, dashboard feel, more controls.
  * Gradio     fewer lines, and `share=True` gives you a temporary public link
               for demo day (read DEPLOY.md BEFORE you use it).

The course rule holds in both: a chatbot is a black box unless it shows its
work, so every answer carries the retrieved verses underneath it -- here as a
collapsible <details> block, since Gradio renders HTML inside Markdown.

Setup (one-time):
  pip install -r requirements-chatbot.txt   # streamlit + gradio
  python get_bible.py                       # writes kjv.json (no token)
  python inference_auth_token.py authenticate   # browser login, ~48h token

Run:
  python chat_bible_gradio.py               # http://127.0.0.1:7860
  python chat_bible_gradio.py --embed       # semantic retrieval
  python chat_bible_gradio.py --share       # TEMPORARY PUBLIC link -- see DEPLOY.md
"""

import argparse
import html

import gradio as gr

# The whole point: reuse the students' own RAG code, don't reimplement it.
from ask_bible_local import (
    build_retriever, ask_rag, ask_plain, CHAT_MODEL, EMBED_MODEL,
)

# Built once at startup (below), then reused for every message. Embedding the
# whole Bible per-question would be unusable.
RETRIEVER = None


def format_sources(hits):
    """Render the grounding: the exact verses the model was allowed to use.

    A <details> block so it does not drown the answer, but is always one click
    away -- never hidden, never omitted. This is the disclosure appendix, live.
    """
    rows = "\n".join(
        f"<li><b>[{html.escape(v['ref'])}]</b> "
        f"<i>(score {score:.3f})</i><br>{html.escape(v['text'])}</li>"
        for v, score in hits
    )
    return (f"\n\n<details><summary><b>Sources retrieved "
            f"({len(hits)} verses -- the grounding)</b></summary>\n"
            f"<ul>{rows}</ul></details>")


def respond(message, history, k, show_plain):
    """One turn. ChatInterface passes (message, history, *additional_inputs)."""
    try:
        answer, hits = ask_rag(message, RETRIEVER, k=int(k))
    except Exception as e:                      # noqa: BLE001 -- show it plainly
        return (f"**Model call failed:** `{e}`\n\n"
                "If this is a 401, your ALCF token expired -- re-run "
                "`python inference_auth_token.py authenticate`.")

    out = answer + format_sources(hits)

    # The Week 2 lesson, on demand: the same model with NO retrieval.
    if show_plain:
        try:
            plain = ask_plain(message)
        except Exception as e:                  # noqa: BLE001
            plain = f"[ungrounded call failed: {e}]"
        out += ("\n\n<details><summary><b>Ungrounded answer (from memory -- "
                "verify it against the sources above!)</b></summary>\n\n"
                + plain + "\n</details>")
    return out


def build_demo():
    """The whole UI. Kept in a function so tests can build it without launching."""
    k = gr.Slider(2, 10, value=6, step=1, label="Verses to retrieve (k)",
                  info="How many verses are fed to the model as grounding.")
    show_plain = gr.Checkbox(
        value=True, label="Also show the UNGROUNDED answer",
        info="Asks the same model with no retrieval, so you can watch it "
             "paraphrase, misquote, or invent verses.")

    # No `type=` argument: Gradio 5 accepts it, Gradio 6 removed it. We never
    # read `history`, so the default works on both. (API drift is real -- if
    # this file breaks in a year, that is the lesson, not a bug.)
    return gr.ChatInterface(
        fn=respond,
        title="Ask the Bible (grounded)",
        description=(
            "A RAG chatbot over the King James Bible (31,100 verses). Every "
            "answer shows the verses it retrieved -- open the **Sources** block "
            "and check it. *Student project; not pastoral advice.*"),
        additional_inputs=[k, show_plain],
        additional_inputs_accordion=gr.Accordion("Retrieval settings", open=False),
        examples=[["Quote John 3:16 exactly."],
                  ["What does Micah 6:8 require of us?"],
                  ["What does Hezekiah 3:16 say?"]],   # no such book -> must refuse
    )


def main():
    global RETRIEVER
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--embed", action="store_true",
                   help="use local semantic embeddings instead of BM25")
    p.add_argument("--share", action="store_true",
                   help="create a TEMPORARY PUBLIC link (no password!) -- read DEPLOY.md")
    p.add_argument("--lan", action="store_true",
                   help="serve to your local network (0.0.0.0) -- read DEPLOY.md")
    args = p.parse_args()

    RETRIEVER = build_retriever(force_embed=args.embed)
    print(f"Chat model: {CHAT_MODEL}")
    print(f"Retriever : {'embeddings — ' + EMBED_MODEL if args.embed else 'BM25 lexical'}")
    if args.share:
        print("\n!! --share publishes this app to the OPEN INTERNET with no "
              "password, and every visitor spends YOUR ALCF token. "
              "Demo day only; see DEPLOY.md.\n")

    build_demo().launch(
        share=args.share,
        server_name="0.0.0.0" if (args.lan or args.share) else "127.0.0.1",
    )


if __name__ == "__main__":
    main()
