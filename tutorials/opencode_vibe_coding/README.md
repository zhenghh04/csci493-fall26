# Lab — Wire an Open Model into a Coding Agent (opencode + ALCF), then Vibe-Code

*AI for Theological Inquiry · one-page student handout*

Last week you talked to the **raw model** — one call, one answer, and you caught it
lying. This week you put the **agent loop back around it**: `plan → act (tools) →
observe → act again`. You'll run [**opencode**](https://opencode.ai) — a free,
open-source coding agent that lives in your terminal — driven by the *same open
model on ALCF* you already know. Then you'll **vibe-code** a small tool and, in the
same breath, learn why "trust the vibes" is exactly the habit this course exists to
discipline.

You need three things you already have: **(1)** your ALCF token from Week 2,
**(2)** Node.js, **(3)** ~10 lines of config. The model URL is unchanged.

---

## 0. Prerequisites (once)

- Your **Week 2 ALCF setup**: `inference_auth_token.py` in your working folder and a
  successful `python inference_auth_token.py authenticate` (token good ~48 h).
- **Node.js 18+** (`node --version`). If missing: <https://nodejs.org>.
- **Install opencode** (pick one):
  ```bash
  npm install -g opencode-ai          # via npm
  # or:
  curl -fsSL https://opencode.ai/install | bash
  ```
  Check it: `opencode --version`. *(This one install powers all three front-ends below
  — terminal, browser, and VS Code — so you only install once.)*

## 1. The one idea: the ALCF endpoint is "just an OpenAI-compatible URL"

opencode can talk to **any** OpenAI-compatible provider. ALCF is one. So we don't
need a vendor key — we point opencode at the *same* `base_url` and feed it *your*
ALCF token as the "API key." That's the whole trick.

## 2. Give opencode your token (do this each session)

The token expires (~48 h) and opencode reads it **once at startup**, so refresh it
in your shell *before* launching:

```bash
export ALCF_TOKEN="$(python inference_auth_token.py get_access_token)"
# convenience: `source set_alcf_token.sh` does exactly this and checks it worked
```

## 3. Tell opencode about the ALCF provider

Copy [`opencode.json`](opencode.json) into your **project folder** (opencode reads
it from the directory you launch in; a global copy lives at
`~/.config/opencode/opencode.json`). The shape:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "alcf/meta-llama/Meta-Llama-3.1-8B-Instruct",   // the default at startup
  "provider": {
    "alcf": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "ALCF Inference Endpoint",
      "options": {
        "baseURL": "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1",
        "apiKey": "{env:ALCF_TOKEN}"
      },
      "models": {                                            // every entry here shows up in /models
        "meta-llama/Meta-Llama-3.1-8B-Instruct":  { "name": "Llama 3.1 8B (small, fast)" },
        "meta-llama/Meta-Llama-3.1-70B-Instruct": { "name": "Llama 3.1 70B" },
        "meta-llama/Llama-3.3-70B-Instruct":      { "name": "Llama 3.3 70B (good at code)" },
        "openai/gpt-oss-120b":                    { "name": "gpt-oss 120B" }
        // ...the shipped opencode.json lists 8 models; add or remove freely
      }
    }
  }
}
```

Read the four fields out loud so they stop being magic:
- `baseURL` — **identical** to your Week 2 client. Same engine, new frontend.
- `apiKey: "{env:ALCF_TOKEN}"` — pulls the token from your shell; no secret in the file.
- `npm: "@ai-sdk/openai-compatible"` — ALCF serves `/v1/chat/completions`, so this adapter.
- the `models` map — a **menu**: every ID you list becomes a choice in `/models`. Each
  must be a **real chat model** from `list-endpoints` (they rotate!). *(Embedding models
  can't be picked here — they're not chat models; you'll call those directly for RAG in Week 4.)*

> **JSON has no comments** — the `//` lines above are just for reading. The real
> `opencode.json` in this folder is comment-free and ships with 8 models already
> listed; use it as-is, or trim the list to what's currently served.

> **Confirm the served IDs first** (same command as Week 2), then keep only live ones:
> ```bash
> curl -s https://inference-api.alcf.anl.gov/resource_server/list-endpoints \
>   -H "Authorization: Bearer $ALCF_TOKEN"
> ```
> If an ID in the config isn't listed, edit it (and, if it's the default, the top-level
> `model:` line). A model you list but ALCF isn't serving simply errors when you pick it.

## 4. Launch and select the model

```bash
opencode
```
Inside opencode: type `/models` — **every model from your config's `models` map is
listed**. Pick one (start with **ALCF → Llama 3.1 8B**), and re-run `/models` any time
to **switch mid-session**. Confirm with a throwaway prompt: *"What model are you and
who serves you?"* You are now running an **agent** — it can read/write files and run
commands — on an **open model you control**.

**Which to pick?** Small models (8B) are fast and, for this course, usefully
*fallible* — they'll still fabricate, which is the Week-5 lesson. Bigger models
(70B, `gpt-oss-120b`) code more reliably but cold-start slower. Try the same prompt on
two sizes and compare — that contrast is itself a finding for your disclosure appendix.

## 4b. Prefer a UI? Same setup, three front-ends

The terminal and browser use the CLI installed in step 0. These interfaces share
the provider configuration, but each process needs access to the token when it
starts. Pick whichever you like:

| Front-end | How to launch | Good if… |
|---|---|---|
| **Terminal (TUI)** | `opencode` | you're comfortable in a terminal (default; nothing extra). |
| **Browser UI** ⭐ | `opencode web` | you'd rather click than type. Starts a local server and **opens opencode in your browser**; add `--port 4096` to fix the port. |
| **Desktop app** | Install separately; follow [Desktop app → ALCF setup](desktop_setup.md). | you want a standalone app with credentials that work when launched from the Dock/Finder. |
| **VS Code / Cursor** | install **"opencode"** from the Extensions Marketplace (or run `opencode` once in the IDE terminal — it auto-installs), then **Ctrl+Esc** (Cmd+Esc on Mac) | you already edit code in an IDE; it shares your open file/selection, and `Ctrl+Alt+K` inserts a file reference. |

The **Browser UI** (`opencode web`) is the simplest "app with a UI" — nothing to install
beyond step 0. Its server runs locally (`127.0.0.1`), but prompts and code included
in model requests are sent to ALCF.

> For interfaces launched from your shell, refresh `ALCF_TOKEN` before launching
> and restart after a refresh. Desktop apps launched from the Dock/Finder do not
> inherit that shell variable; the [desktop guide](desktop_setup.md) uses a private
> token file and explains how to refresh it.

---

## 5. Vibe-code something (25 min)

**"Vibe coding"** (Karpathy, 2025): describe what you want in plain language, let the
agent write and run the code, and *ride the vibes* — accept results without reading
every line. It's genuinely fast.

Work through the graded ladder in **[`examples.md`](examples.md)** — each prompt adds
one habit:

1. **Plot sin(x)** → *feel the loop* (watch it install matplotlib and re-run itself).
2. **Sort a list + test it** → *test it, don't just run it* (it writes pytest tests and
   fixes its own failures).
3. **Count words in `sample.txt`** → *read what it wrote* (whose stop-word list is it?).
4. **The trap** → aim the same habit at a **factual** claim and watch green code lie.
5. **Capstone** → download **Martin Luther's writings** and build a **vector database**
   (RAG) that answers only from Luther's actual words, with citations.

Reference solutions are in **[`solutions/`](solutions/)** (`plot_sin.py`,
`sort_and_test.py`) — an answer key and projector fallback; the point is to have
opencode generate them live, then compare.

**The trap, in full** — after the warm-ups, distrust the vibes:

> **Prompt:** *"Add a function `philemon_1_6()` that returns the exact text of Philemon
> 1:6 from memory — no file, no internet. Add a test that it returns a non-empty string,
> and run it."*

The test **passes** — but the verse is almost certainly a **plausible fabrication**:
last week's hallucination, now baked into *code that runs green*. **A passing test
proves the code runs, not that it's true.** **Save this** (prompt + the generated verse +
the real verse) — a disclosure-appendix artifact, exactly like your Week 2 hallucination.

---

## The tension to hold (this is the point)

| Vibe coding gives you | …and quietly costs you |
|---|---|
| Speed: prototype in minutes | You may ship code you don't understand |
| Lower barrier: describe, don't syntax | Bugs & fabrications hide behind fluent output |
| Great for throwaway exploration | Bad for anything you'll *cite* or *publish* |

**The course rule:** vibe to *explore*, verify to *publish*. For research you (a)
read what the agent wrote, (b) ground factual claims in a real source (that's RAG,
Week 4), (c) test it (that's evaluation, Week 6), and (d) **disclose** the model,
the tool, and what you accepted unread. The agent is a collaborator, not an author.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `401` / auth error in opencode | Token expired. Re-run `export ALCF_TOKEN=$(python inference_auth_token.py get_access_token)` **and restart** opencode (it reads the token at startup). |
| Model not in `/models` list | `opencode.json` isn't in the folder you launched from, or JSON is malformed. Validate and relaunch. |
| "model not found" on first prompt | The ID in `opencode.json` isn't currently served — re-check `list-endpoints`, edit the ID. |
| First call takes 10–15 min | Cold start on Sophia — the model is spinning up. Wait once; later calls are fast. |
| `opencode: command not found` | Reinstall (step 0); ensure your npm global bin is on `PATH`. |
| Empty/echoed `apiKey` | You forgot to `export ALCF_TOKEN` **in the same shell** before launching. |

**Security:** never paste a personal vendor API key on a lab machine. The
`{env:ALCF_TOKEN}` flow uses *your* ALCF account and keeps no secret in the file.

**References:** opencode docs <https://opencode.ai/docs/> ·
ALCF Inference Endpoints <https://docs.alcf.anl.gov/services/inference-endpoints/>
