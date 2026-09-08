#!/usr/bin/env python3
"""
Week 2 lab — the smallest possible "hello" to the ALCF inference endpoint.

Before running:
  1. pip install openai
  2. wget https://raw.githubusercontent.com/argonne-lcf/inference-endpoints/main/inference_auth_token.py
  3. python inference_auth_token.py authenticate      # browser login, ~48h token
  4. (optional) list served models, then set MODEL below to a current ID:
       tok=$(python inference_auth_token.py get_access_token)
       curl -s https://inference-api.alcf.anl.gov/resource_server/list-endpoints \
         -H "Authorization: Bearer $tok"

Run:
  python 01_hello_alcf.py
"""

from openai import OpenAI
from inference_auth_token import get_access_token

# The ALCF inference endpoint is OpenAI-compatible. Sophia / vLLM base URL:
BASE_URL = "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1"

# Use an exact model ID from `list-endpoints` (see step 4 above). This is a common
# default, but the served set changes — confirm it if you get a "not found" error.
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"


def main() -> None:
    client = OpenAI(api_key=get_access_token(), base_url=BASE_URL)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "What does Romans 7:24 say?"}],
        temperature=0,  # deterministic — the reproducible, disclosable setting
    )

    print(f"[model={MODEL}  temperature=0]\n")
    print(resp.choices[0].message.content)


if __name__ == "__main__":
    main()
