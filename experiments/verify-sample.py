#!/usr/bin/env python3
"""verify-sample.py - emit a representative sample of grounded modes for an
adversarial verification sweep.

For each sampled mode it outputs the mode name and, per example, the sentence and
the arXiv id it is tagged with. A verifier can then fetch that paper and check
whether the quoted figures and claims actually appear in it.

Usage:
  experiments/verify-sample.py [N]     # systematic sample of ~N modes (default 50)

Prints a JSON array to stdout.
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
ADDITIONS = ROOT / "experiments" / "ontology-additions.yaml"

TAG = re.compile(r"\[arXiv:(\d{4}\.\d{4,5})\]")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    grounded = [m for m in o["modes"] if len(m.get("examples") or []) >= 3]

    # the AI-native modes added this session, forced into the sample
    add = yaml.safe_load(ADDITIONS.read_text(encoding="utf-8"))
    new_ids = {m["id"] for sec in ("human_paralleled", "ai_native")
               for m in (add.get(sec) or [])
               if m["id"] in {"library-drift", "tool-over-privilege",
                              "unsafe-autonomous-execution", "semantic-override",
                              "alignment-hallucination"}}

    forced = [m for m in grounded if m["id"] in new_ids]
    rest = [m for m in grounded if m["id"] not in new_ids]
    # systematic sample over the remainder, by catalogue order
    rest.sort(key=lambda m: m.get("num", 10**6))
    step = max(1, len(rest) // max(1, n - len(forced)))
    sampled = forced + rest[::step]
    sampled = sampled[:n]

    out = []
    for m in sampled:
        exs = []
        for e in m["examples"]:
            tag = TAG.search(e)
            exs.append({"text": TAG.sub("", e).strip(), "arxiv": tag.group(1) if tag else None})
        out.append({"mode": m["name"], "num": m.get("num"), "examples": exs})
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
