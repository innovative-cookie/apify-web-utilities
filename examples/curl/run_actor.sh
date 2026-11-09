#!/usr/bin/env bash
# Store: https://apify.com/innovative_cookie/<actor-name>
# Generic curl runner: ./examples/curl/run_actor.sh <actor-name>
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN (see .env.example)}"
ACTOR="${1:?actor short name required, e.g. domain-availability}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INPUT_FILE="$ROOT/inputs/${ACTOR}.json"
[[ -f "$INPUT_FILE" ]] || { echo "Missing $INPUT_FILE"; exit 1; }
INPUT="$(cat "$INPUT_FILE")"

RUN=$(curl -sS -X POST \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$INPUT" \
  "https://api.apify.com/v2/acts/innovative_cookie~${ACTOR}/runs?waitForFinish=180")

echo "$RUN" | python3 -c 'import sys,json; r=json.load(sys.stdin)["data"]; print(json.dumps({"id":r["id"],"status":r["status"],"datasetId":r["defaultDatasetId"]}, indent=2))'
DATASET_ID=$(echo "$RUN" | python3 -c 'import sys,json; print(json.load(sys.stdin)["data"]["defaultDatasetId"])')
curl -sS -H "Authorization: Bearer ${APIFY_TOKEN}" \
  "https://api.apify.com/v2/datasets/${DATASET_ID}/items?limit=5&format=json" | python3 -m json.tool
