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
  Check it: `opencode --version`.

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
`~/.config/opencode/opencode.json`). The important lines:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "alcf/meta-llama/Meta-Llama-3.1-8B-Instruct",
  "provider": {
    "alcf": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "ALCF Inference Endpoint",
      "options": {
        "baseURL": "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1",
        "apiKey": "{env:ALCF_TOKEN}"
      },
      "models": {
        "meta-llama/Meta-Llama-3.1-8B-Instruct": { "name": "Llama 3.1 8B (ALCF)" }
      }
    }
  }
}
```

Read the four fields out loud so they stop being magic:
- `baseURL` — **identical** to your Week 2 client. Same engine, new frontend.
- `apiKey: "{env:ALCF_TOKEN}"` — pulls the token from your shell; no secret in the file.
- `npm: "@ai-sdk/openai-compatible"` — ALCF serves `/v1/chat/completions`, so this adapter.
- the `models` map — must contain a **real ID** from `list-endpoints` (they rotate!).

> **Confirm the model ID first** (same command as Week 2):
> ```bash
> curl -s https://inference-api.alcf.anl.gov/resource_server/list-endpoints \
>   -H "Authorization: Bearer $ALCF_TOKEN"
> ```
> If `Meta-Llama-3.1-8B-Instruct` isn't listed, edit the ID in `opencode.json`
> (and in the top-level `model:` line) to one that is.

## 4. Launch and select the model

```bash
opencode
```
Inside opencode: type `/models`, pick **ALCF → Llama 3.1 8B**. Confirm with a
throwaway prompt: *"What model are you and who serves you?"* You are now running an
**agent** — it can read/write files and run commands — on an **open model you
control**.

---

## 5. Vibe-code something (20 min)

**"Vibe coding"** (Karpathy, 2025): describe what you want in plain language, let the
agent write and run the code, and *ride the vibes* — accept results without reading
every line. It's genuinely fast. Try it:

> **Prompt:** *"Create a Python script `verse_count.py` that reads a plain-text file
> of Bible verses (one per line) and prints the 10 most frequent words, ignoring
> common stop-words. Then run it on `sample.txt` and show me the output."*

Let opencode plan, write the file, and run it. Watch the **loop**: it proposes,
acts, sees the error/output, and fixes itself. That is the Week-1 `plan → act →
observe` — now doing real work, on your model.

**Then, deliberately, distrust the vibes.** Ask it something with a *factual* trap:

> **Prompt:** *"Add a function that returns the exact text of Philemon 1:6 as a
> string, from memory — no file, no internet."*

It will happily hard-code a **plausible but likely wrong** verse — last week's
hallucination, now baked into *code that runs green*. Green tests ≠ true. **Save
this** (prompt + the generated verse + the real verse) — it is a disclosure-appendix
artifact, exactly like your Week 2 hallucination.

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
