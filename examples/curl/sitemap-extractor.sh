#!/usr/bin/env bash
# Extract sitemap URLs via the Apify API (curl).
# Usage: export APIFY_TOKEN=... ; ./examples/curl/sitemap-extractor.sh
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN (see .env.example)}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INPUT="$(cat "$ROOT/inputs/sitemap-extractor.json")"

# Start a run
RUN=$(curl -sS -X POST \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$INPUT" \
  "https://api.apify.com/v2/acts/innovative_cookie~sitemap-extractor/runs?waitForFinish=120")

echo "$RUN" | python3 -c 'import sys,json; r=json.load(sys.stdin)["data"]; print(json.dumps({"id":r["id"],"status":r["status"],"datasetId":r["defaultDatasetId"]}, indent=2))'
DATASET_ID=$(echo "$RUN" | python3 -c 'import sys,json; print(json.load(sys.stdin)["data"]["defaultDatasetId"])')

# Fetch first items
curl -sS -H "Authorization: Bearer ${APIFY_TOKEN}" \
  "https://api.apify.com/v2/datasets/${DATASET_ID}/items?limit=5&format=json" | python3 -m json.tool
