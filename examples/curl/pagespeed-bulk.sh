#!/usr/bin/env bash
# Store: https://apify.com/innovative_cookie/pagespeed-bulk
# Related: https://dev.to/innovative_cookie/bulk-core-web-vitals-with-the-free-pagespeed-insights-api-and-a-small-hosted-option-162g
# Bulk PageSpeed Insights via Apify (needs your Google API key).
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN (see .env.example)}"
: "${GOOGLE_PSI_API_KEY:?Set GOOGLE_PSI_API_KEY}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INPUT=$(python3 -c 'import json,os,pathlib; p=pathlib.Path("'"$ROOT"'/inputs/pagespeed-bulk.json"); d=json.loads(p.read_text()); d["apiKey"]=os.environ["GOOGLE_PSI_API_KEY"]; print(json.dumps(d))')

RUN=$(curl -sS -X POST \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$INPUT" \
  "https://api.apify.com/v2/acts/innovative_cookie~pagespeed-bulk/runs?waitForFinish=180")

echo "$RUN" | python3 -c 'import sys,json; r=json.load(sys.stdin)["data"]; print(json.dumps({"id":r["id"],"status":r["status"],"datasetId":r["defaultDatasetId"]}, indent=2))'
DATASET_ID=$(echo "$RUN" | python3 -c 'import sys,json; print(json.load(sys.stdin)["data"]["defaultDatasetId"])')
curl -sS -H "Authorization: Bearer ${APIFY_TOKEN}" \
  "https://api.apify.com/v2/datasets/${DATASET_ID}/items?limit=5&format=json" | python3 -m json.tool
