#!/usr/bin/env python3
"""validate-ontology.py - integrity checks for ontology/ethical-ai.yaml.

Keeps the graph consistent: required fields present, ids unique, every relation
target resolves, every principle and harm is referenced by at least one mode, and
enumerated fields use allowed values. Exit 1 on any failure.

Usage: experiments/validate-ontology.py
"""

import sys
from pathlib import Path

import yaml

ONTOLOGY = Path(__file__).resolve().parent.parent / "ontology" / "ethical-ai.yaml"

REQUIRED = ("id", "name", "definition", "category", "group_label", "tag",
            "violates", "causes")
TAGS = {"shipped", "research", "page", "analogy"}
MEAS = {"draft", "multi-turn", "undetectable"}


def main():
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    modes = o.get("modes", [])
    prin_ids = {p["id"] for p in o.get("principles", [])}
    harm_ids = {h["id"] for h in o.get("harm_types", [])}
    mode_ids = {m["id"] for m in modes}
    errors, warnings = [], []

    seen = set()
    used_prin, used_harm = set(), set()
    for m in modes:
        mid = m.get("id", "<no id>")
        for f in REQUIRED:
            if not m.get(f):
                errors.append(f"{mid}: missing required field '{f}'")
        if mid in seen:
            errors.append(f"duplicate id: {mid}")
        seen.add(mid)
        if m.get("tag") not in TAGS:
            errors.append(f"{mid}: bad tag {m.get('tag')!r}")
        if m.get("measurability") and m["measurability"] not in MEAS:
            errors.append(f"{mid}: bad measurability {m['measurability']!r}")
        for p in m.get("violates", []):
            used_prin.add(p)
            if p not in prin_ids:
                errors.append(f"{mid}: violates unknown principle '{p}'")
        for h in m.get("causes", []):
            used_harm.add(h)
            if h not in harm_ids:
                errors.append(f"{mid}: causes unknown harm '{h}'")
        for r in m.get("relates_to", []):
            if r not in mode_ids:
                errors.append(f"{mid}: relates_to unknown mode '{r}'")
        if m.get("same_as") and m["same_as"] not in mode_ids:
            errors.append(f"{mid}: same_as unknown mode '{m['same_as']}'")

    # coverage: every principle and harm referenced
    for p in prin_ids - used_prin:
        warnings.append(f"principle never violated by any mode: {p}")
    for h in harm_ids - used_harm:
        warnings.append(f"harm never caused by any mode: {h}")

    print(f"modes: {len(modes)}  principles: {len(prin_ids)}  harms: {len(harm_ids)}")
    print(f"relation links: violates={sum(len(m.get('violates', [])) for m in modes)}, "
          f"causes={sum(len(m.get('causes', [])) for m in modes)}, "
          f"relates_to={sum(len(m.get('relates_to', [])) for m in modes)}")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    print("PASS" if not errors else f"FAIL ({len(errors)} errors)")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
