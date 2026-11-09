#!/usr/bin/env python3
"""Run any Innovative Cookie Actor via the Apify API.

Store directory: https://apify.com/innovative_cookie
Per-actor Store URL: https://apify.com/innovative_cookie/<name>

Usage:
  export APIFY_TOKEN=...
  python examples/python/run_actor.py sitemap-extractor
  python examples/python/run_actor.py pagespeed-bulk --input inputs/pagespeed-bulk.json

Requires: pip install apify-client
Token is read from APIFY_TOKEN. Never hard-code secrets.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUTS = ROOT / "inputs"

ACTORS = {
    "sitemap-extractor": "innovative_cookie/sitemap-extractor",
    "pagespeed-bulk": "innovative_cookie/pagespeed-bulk",
    "broken-link-checker": "innovative_cookie/broken-link-checker",
    "website-image-extractor": "innovative_cookie/website-image-extractor",
    "domain-availability": "innovative_cookie/domain-availability",
    "logo-favicon": "innovative_cookie/logo-favicon",
    "image-converter": "innovative_cookie/image-converter",
    "dataset-merge-dedup": "innovative_cookie/dataset-merge-dedup",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("actor", choices=sorted(ACTORS), help="Actor short name")
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to input JSON (default: inputs/<actor>.json)",
    )
    parser.add_argument("--timeout", type=int, default=300, help="Wait timeout in seconds")
    args = parser.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print("Set APIFY_TOKEN in the environment (see .env.example).", file=sys.stderr)
        return 1

    input_path = args.input or (DEFAULT_INPUTS / f"{args.actor}.json")
    run_input = json.loads(input_path.read_text(encoding="utf-8"))

    # pagespeed-bulk: prefer GOOGLE_PSI_API_KEY from env over placeholder
    if args.actor == "pagespeed-bulk":
        gkey = os.environ.get("GOOGLE_PSI_API_KEY")
        if gkey:
            run_input["apiKey"] = gkey
        elif str(run_input.get("apiKey", "")).startswith("YOUR_"):
            print(
                "pagespeed-bulk needs a Google PageSpeed API key. "
                "Set GOOGLE_PSI_API_KEY or edit the input JSON.",
                file=sys.stderr,
            )
            return 1

    try:
        from apify_client import ApifyClient
    except ImportError:
        print("Install the client: pip install apify-client", file=sys.stderr)
        return 1

    client = ApifyClient(token)
    actor_id = ACTORS[args.actor]
    print(f"Calling {actor_id} with {input_path} …")
    run = client.actor(actor_id).call(run_input=run_input, timeout_secs=args.timeout)
    dataset_id = run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())
    print(json.dumps({"runId": run["id"], "status": run["status"], "itemCount": len(items), "sample": items[:3]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
