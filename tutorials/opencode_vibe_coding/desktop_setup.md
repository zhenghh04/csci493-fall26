# Connect the OpenCode desktop app to ALCF

This guide configures the standalone desktop app to use **Sophia** or **Metis**.
The commands below use macOS/Linux shell syntax; the macOS launch example assumes
OpenCode is installed in `/Applications`. Last checked: September 15, 2026.

## 1. Install and authenticate

Install the desktop app for your operating system from the
[official OpenCode download page](https://opencode.ai/download).
The desktop app is a separate download from the terminal CLI.

You need access to the ALCF inference service. Complete the
[Week 2 authentication setup](../week02_alcf_inference/README.md), including installing
`globus_sdk` and downloading `inference_auth_token.py`. In the directory containing
that helper, run:

```bash
python inference_auth_token.py authenticate
export ALCF_TOKEN="$(python inference_auth_token.py get_access_token)"
```

Use **`ALCF_TOKEN`** consistently throughout this tutorial. ALCF access tokens
expire after about 48 hours. The helper can refresh them, but you may need to
complete browser authentication again when the login session expires.
See the [ALCF authentication documentation](https://docs.alcf.anl.gov/services/inference-endpoints/).

## 2. Make the token available to the desktop app

**Exporting a variable in Terminal does not make it available to an app launched
from the macOS Dock or Finder.** For normal desktop launches, save the token in a
private file outside this repository:

```bash
python - <<'PY'
import os
from pathlib import Path

token = os.environ.get("ALCF_TOKEN", "").strip()
if not token or any(c.isspace() for c in token):
    raise SystemExit("ALCF_TOKEN is missing or malformed; authenticate first.")
path = Path.home() / ".config/opencode/alcf-token"
path.parent.mkdir(parents=True, exist_ok=True)
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as out:
    os.fchmod(out.fileno(), 0o600)
    out.write(token)
print("Saved the token without displaying it.")
PY
```

The file contains a credential: keep it out of Git, screenshots, and shared
configuration. The JSON below contains only its path.

## 3. Configure the providers

Open `~/.config/opencode/opencode.json` in a text editor. If it already exists,
back it up and **merge these provider entries into its existing `provider` object**;
keep your other providers, MCP servers, and settings. Avoid keeping competing
copies of the same settings in both `opencode.json` and `opencode.jsonc`.

For a new configuration, use this complete, comment-free JSON:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "alcf_metis/gpt-oss-120b",
  "provider": {
    "alcf_sophia": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "ALCF Sophia",
      "options": {
        "baseURL": "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1",
        "apiKey": "{file:~/.config/opencode/alcf-token}"
      },
      "models": {
        "meta-llama/Meta-Llama-3.1-8B-Instruct": {
          "name": "Llama 3.1 8B"
        },
        "openai/gpt-oss-120b": {
          "name": "gpt-oss 120B (Sophia)"
        }
      }
    },
    "alcf_metis": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "ALCF Metis",
      "options": {
        "baseURL": "https://inference-api.alcf.anl.gov/resource_server/metis/api/v1",
        "apiKey": "{file:~/.config/opencode/alcf-token}"
      },
      "models": {
        "gpt-oss-120b": {
          "name": "gpt-oss 120B (Metis)"
        }
      }
    }
  }
}
```

The two services use different model IDs: Sophia uses `openai/gpt-oss-120b`, while
Metis uses `gpt-oss-120b`. The leading `alcf_metis/` in the top-level `model` setting
is OpenCode's provider identifier, not part of the model ID sent to ALCF.
Check current availability in [ALCF's endpoint documentation](https://docs.alcf.anl.gov/services/inference-endpoints/).

OpenCode supports both file references and environment references. Global settings
are merged with project settings, which can override them. See
[OpenCode configuration](https://opencode.ai/docs/config/).

**For this repository:** the terminal tutorial's `opencode.json` defines a separate
provider named `alcf` using `{env:ALCF_TOKEN}`. In the desktop app, select **ALCF Metis**
or **ALCF Sophia** from this guide to use the token file. A project default may
select the terminal provider until you change the model.

## 4. Verify the service, then open the app

Run a small request in the shell where you exported `ALCF_TOKEN`:

```bash
curl --fail-with-body --silent --show-error \
  https://inference-api.alcf.anl.gov/resource_server/metis/api/v1/chat/completions \
  -H "Authorization: Bearer $ALCF_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"model":"gpt-oss-120b","messages":[{"role":"user","content":"Reply only OK."}],"max_tokens":128}'
```

A successful response contains `choices`. If this request fails, address the API
error before debugging the desktop UI. A successful model-list request alone is
not sufficient to verify that inference authentication works.

Then:

1. Fully quit OpenCode (on macOS, **Cmd+Q**, not just closing the window).
2. Reopen it normally and open your project folder.
3. Use the model picker (or `/models`, where available) to select
   **ALCF Metis → gpt-oss 120B (Metis)**.
4. Start a new chat and send: **“Reply only OK. Do not use any tools.”**

Check the selected provider/model in the UI; asking a model to identify itself is
not a reliable configuration check. Prompts and any code included in model
requests are sent to ALCF even though the app runs locally.

## 5. Refresh an expired token

When you see `401` or **“Token is either not active or invalid”**:

1. Run `export ALCF_TOKEN="$(python inference_auth_token.py get_access_token)"`
   from the helper's directory. If authentication is required, run
   `python inference_auth_token.py authenticate --force` and export the token again.
2. Repeat the token-file command in step 2.
3. Fully quit and reopen OpenCode, then retry the small test prompt.

Refreshing the shell variable alone does **not** update the token file or a running
app's cached configuration. Likewise, changing a credential under a different
provider name does not repair the provider your chat is actually using.

### Alternative: launch macOS OpenCode with the shell token

If you prefer `{env:ALCF_TOKEN}` over the token file, use that value for `apiKey`
in both providers. Fully quit the app, export a fresh token, and launch its
executable directly from the same shell:

```bash
export ALCF_TOKEN="$(python inference_auth_token.py get_access_token)"
/Applications/OpenCode.app/Contents/MacOS/OpenCode
```

Use this launch method each time; a Dock/Finder launch does not inherit that
terminal's environment. The file-based setup above avoids this dependency.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Terminal works, desktop reports an invalid token | Confirm the desktop's selected provider uses the refreshed token file; fully restart it. |
| API test works, app still fails | Check project overrides, provider selection, and cached settings. A config change may require a full quit/reopen. |
| Provider missing from the picker | Check JSON syntax, the config location, and any `enabled_providers` or `disabled_providers` settings. |
| Model not found | Match the model ID to the selected cluster; do not interchange Sophia and Metis IDs. |
| First Sophia request is slow | The model may need to start; check ALCF service status before changing credentials. |
| Terminal says “Unexpected server error” before any API request | Homebrew OpenCode 1.18.30 has a reported `SystemPrompt.environment` crash. The official 1.18.31 CLI binary worked in our September 15 check. This is separate from token authentication; see the [upstream issue](https://github.com/anomalyco/opencode/issues/48372). |

Return to the [coding-agent lab](README.md).
