#!/usr/bin/env python3
"""list-models.py - list cheap OpenRouter chat models (for picking a test panel).

Reads OPENROUTER_API_KEY from the local .env (via run.load_env) and prints model
ids whose prompt+completion price is under a threshold, so the benchmark panel can
be refreshed when slugs change. Replaces ad-hoc one-off queries.

Usage:
  experiments/behaviour-eval/list-models.py [--max-prompt 1e-6] [--grep llama,mistral]
"""

import argparse
import json
import os
import sys
import urllib.request

from run import load_env

MODELS_URL = "https://openrouter.ai/api/v1/models"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-prompt", type=float, default=2e-6,
                    help="max prompt price per token (default 2e-6)")
    ap.add_argument("--grep", default="", help="comma-separated substrings to match in the id")
    args = ap.parse_args()

    load_env()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not found in .env")

    req = urllib.request.Request(MODELS_URL, headers={"Authorization": f"Bearer {key}"})
    data = json.loads(urllib.request.urlopen(req, timeout=60).read())["data"]
    needles = [g.strip() for g in args.grep.split(",") if g.strip()]

    out = []
    for m in data:
        mid = m["id"]
        if ":free" in mid or ":batch" in mid:
            continue
        try:
            price = float(m.get("pricing", {}).get("prompt", 1))
        except (TypeError, ValueError):
            continue
        if price > args.max_prompt:
            continue
        if needles and not any(n in mid for n in needles):
            continue
        out.append((price, mid))

    for price, mid in sorted(out):
        print(f"{price:>12.9f}  {mid}")
    print(f"\n{len(out)} models under {args.max_prompt} prompt price", file=sys.stderr)


if __name__ == "__main__":
    main()
