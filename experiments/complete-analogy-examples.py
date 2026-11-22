#!/usr/bin/env python3
"""Insert illustrative `example:` lines into ontology/ethical-ai.yaml for analogy
modes that lack one, matching the existing analogy-example style.

Input: a JSON object mapping mode id -> example string (one concrete sentence,
no citation). Only ids that currently have NO example line are touched; the
example line is inserted immediately before that entry's `tag:` line, 2-space
indented, as a double-quoted scalar (safe for any punctuation).

Usage:
  python3 experiments/complete-analogy-examples.py examples.json           # apply
  python3 experiments/complete-analogy-examples.py examples.json --dry-run # report only
Idempotent: rerunning skips ids that already have an example.
"""
import json, re, sys, io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YAML = ROOT / "ontology" / "ethical-ai.yaml"
ID_RE = re.compile(r"^- id:\s*(\S+)\s*$")
TAG_RE = re.compile(r"^  tag:\s")
EX_RE = re.compile(r"^  example:\s")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    mapping = json.loads(Path(sys.argv[1]).read_text())
    dry = "--dry-run" in sys.argv[2:]
    lines = YAML.read_text().splitlines(keepends=True)

    # split into entry blocks keyed by line index of each `- id:`
    starts = [i for i, l in enumerate(lines) if ID_RE.match(l)]
    starts.append(len(lines))
    inserted, skipped_present, skipped_nomap, missing_tag = [], [], [], []
    out = []
    block_bounds = {starts[k]: starts[k + 1] for k in range(len(starts) - 1)}

    i = 0
    while i < len(lines):
        m = ID_RE.match(lines[i])
        if not m or m.group(1) not in mapping:
            out.append(lines[i]); i += 1; continue
        mid = m.group(1)
        end = block_bounds[i]
        block = lines[i:end]
        if any(EX_RE.match(l) for l in block):
            skipped_present.append(mid); out.extend(block); i = end; continue
        tag_idx = next((j for j, l in enumerate(block) if TAG_RE.match(l)), None)
        if tag_idx is None:
            missing_tag.append(mid); out.extend(block); i = end; continue
        ex_line = "  example: " + json.dumps(mapping[mid], ensure_ascii=False) + "\n"
        block.insert(tag_idx, ex_line)
        inserted.append(mid)
        out.extend(block); i = end

    for mid in mapping:
        if mid not in inserted and mid not in skipped_present:
            skipped_nomap.append(mid)

    print(f"inserted: {len(inserted)}  already-had-example: {len(skipped_present)}  "
          f"missing-tag: {len(missing_tag)}  id-not-found: {len(skipped_nomap)}")
    if missing_tag: print("  missing-tag ids:", missing_tag[:10])
    if skipped_nomap: print("  id-not-found:", skipped_nomap[:10])
    if dry:
        return
    YAML.write_text("".join(out))
    # sanity: still valid YAML, counts unchanged
    import yaml
    d = yaml.safe_load(YAML.read_text())
    print(f"YAML OK: {len(d['modes'])} modes; "
          f"{sum(1 for x in d['modes'] if x.get('example'))} now have examples")


if __name__ == "__main__":
    main()
