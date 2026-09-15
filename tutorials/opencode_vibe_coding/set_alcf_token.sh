#!/usr/bin/env bash
# Export a fresh ALCF inference token into ALCF_TOKEN so opencode's
# {env:ALCF_TOKEN} picks it up. The token lasts ~48h, so re-source this
# whenever opencode starts returning 401.
#
#   source set_alcf_token.sh      # NOTE: `source`, not `./` — we need the export
#
# Requires inference_auth_token.py in this folder (see the Week 2 handout) and a
# prior `python inference_auth_token.py authenticate` (browser login).

export ALCF_TOKEN="$(python inference_auth_token.py get_access_token)"

if [ -z "$ALCF_TOKEN" ]; then
  echo "ERROR: got an empty token. Run: python inference_auth_token.py authenticate" >&2
else
  echo "ALCF_TOKEN set (${#ALCF_TOKEN} chars). Now run: opencode"
fi
