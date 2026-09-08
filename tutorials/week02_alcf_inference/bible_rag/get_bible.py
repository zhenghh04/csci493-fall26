#!/usr/bin/env python3
"""
Step 0 for the "chat with the whole Bible" lab — download the corpus ONCE.

Fetches the King James Version (public domain) as a single JSON file and
flattens it into one verse per record:  {"ref", "book", "chapter", "verse", "text"}.
Writes  kjv.json  (~4.5 MB, 31,100 verses) next to this script.

Run once (needs internet; no ALCF token required):
  python get_bible.py
"""

import json
import os
import urllib.request

# Public-domain KJV, one file, one list of 66 books.
SOURCE_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kjv.json")


def flatten(books):
    """books -> flat list of verse records with human-readable references."""
    verses = []
    for book in books:
        name = book["name"]
        for ci, chapter in enumerate(book["chapters"], start=1):
            for vi, text in enumerate(chapter, start=1):
                # KJV marks translator-supplied words with {braces}; drop the
                # markers but keep the words, so the RAG context reads cleanly.
                clean = text.replace("{", "").replace("}", "").strip()
                verses.append({
                    "ref": f"{name} {ci}:{vi}",
                    "book": name,
                    "chapter": ci,
                    "verse": vi,
                    "text": clean,
                })
    return verses


def main():
    print(f"Downloading KJV from {SOURCE_URL} ...")
    with urllib.request.urlopen(SOURCE_URL, timeout=60) as r:
        raw = r.read().decode("utf-8-sig")   # source carries a BOM
    books = json.loads(raw)

    verses = flatten(books)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(verses, f, ensure_ascii=False)

    print(f"Wrote {len(verses):,} verses from {len(books)} books -> {OUT}")
    print(f"First: [{verses[0]['ref']}] {verses[0]['text']}")
    print(f"Last:  [{verses[-1]['ref']}] {verses[-1]['text']}")


if __name__ == "__main__":
    main()
