#!/usr/bin/env python3
"""assign-violates.py - fill the `violates` principle for records that lack one, from a mapping.

Reads a JSON mapping [{"num": int, "principle": str}, ...] and, for each listed record whose
`violates` is currently the empty inline list `violates: []`, rewrites that single line as a
block-style assignment matching the historical records:

    violates:
    - <principle>

It is a deterministic line pass: it tracks each record's `num` and only touches the empty
`violates: []` line inside a record named in the mapping. Everything else in the YAML, including
comments, ordering and style, is preserved byte-for-byte. No YAML library is used, so no
round-trip reformatting can occur.

Usage:
  assign-violates.py <mapping.json> [--yaml ontology/ethical-ai.yaml] [--dry-run]

The seven valid principle ids are checked; an unknown principle aborts without writing.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRINCIPLES = {"honesty", "calibration", "non-maleficence", "transparency",
              "scope-fidelity", "independence", "corrigibility"}
NUM_RE = re.compile(r"^  num:\s*(\d+)\s*$")
EMPTY_VIOLATES_RE = re.compile(r"^  violates:\s*\[\]\s*$")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    mapping_path = Path(sys.argv[1])
    yaml_path = ROOT / "ontology" / "ethical-ai.yaml"
    dry = "--dry-run" in sys.argv
    if "--yaml" in sys.argv:
        yaml_path = Path(sys.argv[sys.argv.index("--yaml") + 1])

    rows = json.loads(mapping_path.read_text())
    by_num = {}
    for r in rows:
        p = r["principle"]
        if p not in PRINCIPLES:
            sys.exit(f"ABORT: unknown principle {p!r} for num {r['num']}")
        by_num[int(r["num"])] = p
    print(f"mapping: {len(by_num)} records, principles {sorted(set(by_num.values()))}")

    lines = yaml_path.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    cur = None
    changed = 0
    for ln in lines:
        m = NUM_RE.match(ln.rstrip("\n"))
        if m:
            cur = int(m.group(1))
            out.append(ln)
            continue
        if EMPTY_VIOLATES_RE.match(ln.rstrip("\n")) and cur in by_num:
            nl = "\n" if ln.endswith("\n") else ""
            out.append(f"  violates:{nl}")
            out.append(f"  - {by_num[cur]}{nl}")
            changed += 1
            continue
        out.append(ln)

    print(f"records updated: {changed} (of {len(by_num)} in mapping)")
    if changed != len(by_num):
        print("WARNING: some mapped records had no empty `violates: []` line to fill")
    if dry:
        print("dry-run: no write")
        return
    yaml_path.write_text("".join(out), encoding="utf-8")
    print(f"wrote {yaml_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
