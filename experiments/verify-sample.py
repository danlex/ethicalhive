#!/usr/bin/env python3
"""verify-sample.py - emit a representative sample of grounded modes for an
adversarial verification sweep.

For each sampled mode it outputs the mode name and, per example, the sentence and
the arXiv id it is tagged with. A verifier can then fetch that paper and check
whether the quoted figures and claims actually appear in it.

Usage:
  experiments/verify-sample.py [N]            # systematic sample of ~N modes (default 50)
  experiments/verify-sample.py rest DONE.json # all grounded modes whose num is NOT in DONE
  experiments/verify-sample.py all            # all grounded modes

Prints a JSON array to stdout. Example text is truncated to keep workflow args small.
"""

import json
import re
import sys
from pathlib import Path

TRUNC = 210

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
ADDITIONS = ROOT / "experiments" / "ontology-additions.yaml"

TAG = re.compile(r"\[arXiv:(\d{4}\.\d{4,5})\]")


def emit(modes):
    out = []
    for m in modes:
        exs = []
        for e in m["examples"]:
            tag = TAG.search(e)
            txt = TAG.sub("", e).strip()
            if len(txt) > TRUNC:
                txt = txt[:TRUNC].rsplit(" ", 1)[0]
            exs.append({"text": txt, "arxiv": tag.group(1) if tag else None})
        out.append({"mode": m["name"], "num": m.get("num"), "examples": exs})
    print(json.dumps(out, ensure_ascii=False))


def main():
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    grounded = [m for m in o["modes"] if len(m.get("examples") or []) >= 3]

    arg = sys.argv[1] if len(sys.argv) > 1 else "50"

    if arg == "all":
        emit(sorted(grounded, key=lambda m: m.get("num", 10**6)))
        return
    if arg == "only":
        want = {int(x) for x in sys.argv[2].split(",") if x.strip()}
        emit(sorted((m for m in grounded if m.get("num") in want),
                    key=lambda m: m.get("num", 10**6)))
        return
    if arg == "rest":
        done = json.loads(Path(sys.argv[2]).read_text())
        done_nums = {d["num"] for d in done}
        emit(sorted((m for m in grounded if m.get("num") not in done_nums),
                    key=lambda m: m.get("num", 10**6)))
        return

    n = int(arg)
    add = yaml.safe_load(ADDITIONS.read_text(encoding="utf-8"))
    new_ids = {m["id"] for sec in ("human_paralleled", "ai_native")
               for m in (add.get(sec) or [])
               if m["id"] in {"library-drift", "tool-over-privilege",
                              "unsafe-autonomous-execution", "semantic-override",
                              "alignment-hallucination"}}
    forced = [m for m in grounded if m["id"] in new_ids]
    rest = [m for m in grounded if m["id"] not in new_ids]
    rest.sort(key=lambda m: m.get("num", 10**6))
    step = max(1, len(rest) // max(1, n - len(forced)))
    emit((forced + rest[::step])[:n])


if __name__ == "__main__":
    main()
