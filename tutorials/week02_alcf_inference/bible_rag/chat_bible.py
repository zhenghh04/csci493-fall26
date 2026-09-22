#!/usr/bin/env python3
"""
Ask the Bible -- a web chatbot around the RAG system you already built.

This is PACKAGING, not new science. Every hard part -- the retriever over all
31,100 KJV verses, the grounded prompt, the small ALCF chat model -- already
lives in `ask_bible_local.py`. This file only wraps it in a browser UI, so we
IMPORT that code instead of copying it:

    from ask_bible_local import build_retriever, ask_rag, ask_plain, ...

The one design choice that matters for THIS course: a chatbot is a black box
unless it shows its work. So the UI always displays the verses it retrieved,
right under the answer. The interface itself enforces the rule from Week 2 --
don't trust, verify -- and gives you the raw material for the disclosure
appendix every deliverable requires.

Setup (one-time):
  pip install streamlit                     # plus the deps ask_bible_local needs
  python get_bible.py                       # writes kjv.json (no token)
  python inference_auth_token.py authenticate   # browser login, ~48h token
  (optional, for semantic search)
  pip install -r requirements-local.txt && python build_index_local.py

Run:
  streamlit run chat_bible.py
  # then open the URL it prints (default http://localhost:8501)
"""

import streamlit as st

# The whole point: reuse the students' own RAG code, don't reimplement it.
from ask_bible_local import (
    build_retriever, ask_rag, ask_plain, CHAT_MODEL, EMBED_MODEL,
)

st.set_page_config(page_title="Ask the Bible (grounded)", page_icon="📖",
                   layout="wide")


# --------------------------------------------------------------------------
# Load the retriever ONCE and keep it. Streamlit reruns this whole script on
# every keystroke/click, so without caching we would rebuild the index (and,
# for embeddings, re-embed the Bible) every single message. @st.cache_resource
# keeps the built object alive across reruns.
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading corpus and building the retriever...")
def load_retriever(use_embeddings: bool):
    # build_retriever prints to the terminal (fine) and returns BM25 or the
    # local-embedding index depending on force_embed / whether a cache exists.
    return build_retriever(force_embed=use_embeddings)


# --------------------------------------------------------------------------
# Sidebar -- the knobs. Deliberately few: retriever, how many verses, and the
# comparison toggle that carries the course's central lesson into the UI.
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("📖 Ask the Bible")
    st.caption("A grounded chatbot over the King James Bible (31,100 verses).")

    use_embeddings = st.toggle(
        "Semantic retrieval (embeddings)",
        value=False,
        help="Off = BM25 keyword search (instant, no setup). "
             "On = local embeddings; needs sentence-transformers and, ideally, "
             "a prebuilt bible_index_local.npz.",
    )
    k = st.slider("Verses to retrieve (k)", min_value=2, max_value=10, value=6,
                  help="How many verses to feed the model as grounding.")
    show_plain = st.toggle(
        "Also show the UNGROUNDED answer",
        value=True,
        help="Ask the same small model with NO retrieval, side by side. "
             "This is the Week 2 lesson made visible: watch it paraphrase, "
             "misquote, or invent verses when it answers from memory alone.",
    )

    st.divider()
    st.caption(f"Chat model: `{CHAT_MODEL}`")
    st.caption(f"Retriever: {'embeddings — ' + EMBED_MODEL if use_embeddings else 'BM25 lexical'}")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Try: *Quote John 3:16 exactly.* · *What does Micah 6:8 "
               "require?* · *What does Hezekiah 3:16 say?* (there is no such "
               "book — a grounded system must refuse.)")


# The toggle can change which retriever we need; cache keys on its argument, so
# flipping it just swaps to (or builds) the other index.
retriever = load_retriever(use_embeddings)


# --------------------------------------------------------------------------
# Conversation state. We keep the retrieved verses on each assistant turn so
# the "sources" panel survives Streamlit's reruns.
# --------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


def render_sources(hits):
    """Show the grounding: the exact verses the model was allowed to use."""
    with st.expander(f"📑 Sources retrieved ({len(hits)} verses — the grounding)",
                     expanded=False):
        for v, score in hits:
            st.markdown(f"**[{v['ref']}]** &nbsp; *(score {score:.3f})*  \n{v['text']}")


# Replay the history on every rerun.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("hits"):
            render_sources(msg["hits"])
        if msg.get("plain"):
            with st.expander("🚫 Ungrounded answer (from memory — verify against the sources!)"):
                st.markdown(msg["plain"])


# --------------------------------------------------------------------------
# The chat input -- the actual conversation loop.
# --------------------------------------------------------------------------
question = st.chat_input("Ask a question about the Bible...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        # 1) GROUNDED answer -- retrieve, then answer from ONLY those verses.
        try:
            with st.spinner("Retrieving verses and answering from the text..."):
                answer, hits = ask_rag(question, retriever, k=k)
        except Exception as e:  # noqa: BLE001 -- surface auth/model errors plainly
            st.error(f"Model call failed: {e}\n\n"
                     "If this is a 401, your ALCF token expired — re-run "
                     "`python inference_auth_token.py authenticate`.")
            st.stop()

        st.markdown(answer)
        render_sources(hits)

        # 2) Optional UNGROUNDED answer -- the same model, no retrieval.
        plain = None
        if show_plain:
            try:
                with st.spinner("Also asking WITHOUT retrieval (from memory)..."):
                    plain = ask_plain(question)
                with st.expander("🚫 Ungrounded answer (from memory — verify against the sources!)"):
                    st.markdown(plain)
            except Exception as e:  # noqa: BLE001
                plain = f"[ungrounded call failed: {e}]"

    st.session_state.messages.append({
        "role": "assistant", "content": answer, "hits": hits, "plain": plain,
    })
