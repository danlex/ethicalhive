#!/usr/bin/env python3
"""llm-citation-probe.py - does an LLM's suggested citations fail the same way the human audit found?

Phase 1 (this script, `generate`): take a stratified sample of catalogue modes, give an
independent LLM ONLY the definition, and ask it to name one real arXiv paper that provides
AI-side empirical evidence for the behaviour. Record what it suggests. This mirrors how a
citation gets attached by keyword search or an LLM asked for a plausible reference.

Phase 2 (manual / verify): each suggested arXiv id is then checked against the real paper
(does the id exist, does the paper support the mode) and classified into the same
failure-type taxonomy as the human citation audit, so the two distributions can be compared.

The point of the whole exercise is that Phase 2 CANNOT be skipped: the LLM's suggestion is
plausible by construction, and only reading the source tells you whether it holds. This script
only produces the suggestions; it does not score them.

Usage:
  llm-citation-probe.py generate [--n 20] [--model openai/gpt-4o] [--seed-list a,b,c]
"""
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import openrouter

OUT = HERE / "llm-citation-probe-results.jsonl"

PROMPT = """You are helping assemble an evidence-linked catalogue of AI failure modes. \
Here is one mode's definition:

"{definition}"

Name exactly one real arXiv paper that provides empirical evidence of THIS behaviour in AI or \
large-language-model systems (not in humans). Give the arXiv id and the exact title. Only name \
a paper you are confident actually exists and actually studies this behaviour in a model.

Answer in exactly this format, nothing else:
ARXIV: <id like 2404.01234>
TITLE: <exact title>
WHY: <one sentence on how the paper evidences the mode>"""


def pick_sample(modes, n):
    """Stratified by category: round-robin across categories by reference number."""
    from collections import defaultdict
    bycat = defaultdict(list)
    for m in modes:
        # original grounded modes only (they are what the human audit covered)
        if m.get("example") and (m.get("arxiv") or {}).get("papers"):
            bycat[m.get("category", "?")].append(m)
    for c in bycat:
        bycat[c].sort(key=lambda m: m["num"])
    sample, cats = [], sorted(bycat)
    i = 0
    while len(sample) < n and any(bycat.values()):
        c = cats[i % len(cats)]
        if bycat[c]:
            sample.append(bycat[c].pop(0))
        i += 1
        if i > 10000:
            break
    return sample


def parse(resp):
    ax = re.search(r"ARXIV:\s*([0-9]{4}\.[0-9]{4,5})", resp or "")
    ti = re.search(r"TITLE:\s*(.+)", resp or "")
    wy = re.search(r"WHY:\s*(.+)", resp or "")
    return (ax.group(1) if ax else None,
            ti.group(1).strip() if ti else None,
            wy.group(1).strip() if wy else None)


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "generate":
        print(__doc__); sys.exit(1)
    n, model, seed_list = 20, "openai/gpt-4o", None
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == "--n" and i + 1 < len(args): n = int(args[i + 1])
        if a == "--model" and i + 1 < len(args): model = args[i + 1]
        if a == "--seed-list" and i + 1 < len(args): seed_list = args[i + 1].split(",")

    openrouter.load_env()
    modes = yaml.safe_load(open(ROOT / "ontology" / "ethical-ai.yaml"))["modes"]
    if seed_list:
        sample = [m for m in modes if m["id"] in seed_list]
    else:
        sample = pick_sample(modes, n)

    print(f"Probing {len(sample)} modes with {model}. Output -> {OUT.name}")
    with open(OUT, "w") as fh:
        for m in sample:
            resp = openrouter.chat(model, PROMPT.format(definition=m["definition"]),
                                   temperature=0.3, max_tokens=250)
            ax, ti, wy = parse(resp)
            rec = dict(num=m["num"], id=m["id"], name=m["name"], category=m.get("category"),
                       definition=m["definition"], model=model,
                       suggested_arxiv=ax, suggested_title=ti, why=wy,
                       existing_papers=[p["id"] for p in (m.get("arxiv", {}).get("papers") or [])])
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"  [{m['num']:>3}] {m['name'][:34]:34} -> {ax or 'NO-ID':<14} {(ti or '')[:40]}")
    print(f"\nWrote {len(sample)} suggestions. Phase 2: verify each arXiv id against the real paper.")


if __name__ == "__main__":
    main()
