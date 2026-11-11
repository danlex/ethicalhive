#!/usr/bin/env python3
"""lint-ontology-semantics.py - semantic error finder for ontology/ethical-ai.yaml.

The structural validator (validate-ontology.py) checks counts and relation balance. This
finds content errors it does not: broken graph references, malformed or impossible arXiv
identifiers, year/id inconsistencies, count mismatches, citations reused across unrelated
modes, and empty required fields. Read-only; no model calls.

An arXiv id is YYMM.NNNNN. A paper cannot be from the future, so YYMM after the current
month is a fabricated or mistyped id. The stated `year` must match 20YY from the id prefix.

Usage: lint-ontology-semantics.py [ontology/ethical-ai.yaml] [--now YYYY-MM]
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ARXIV = re.compile(r"^(\d{2})(\d{2})\.\d{4,5}$")


def main():
    path = ROOT / "ontology" / "ethical-ai.yaml"
    now_ym = "2611"  # current YYMM ceiling (Nov 2026); override with --now
    args = sys.argv[1:]
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False; continue
        if a == "--now" and i + 1 < len(args):
            y, m = args[i + 1].split("-"); now_ym = f"{y[2:]}{m}"; skip = True
        elif not a.startswith("--"):
            path = Path(a)
    doc = yaml.safe_load(open(path, encoding="utf-8"))
    modes = doc["modes"]
    ids = {m["id"] for m in modes}
    errors, warns = [], []

    # 1. duplicate ids / nums
    seen_id, seen_num = defaultdict(int), defaultdict(int)
    for m in modes:
        seen_id[m["id"]] += 1
        seen_num[m.get("num")] += 1
    for k, c in seen_id.items():
        if c > 1: errors.append(f"[dup-id] '{k}' appears {c} times")
    for k, c in seen_num.items():
        if c > 1: errors.append(f"[dup-num] num {k} appears {c} times")

    # 2. dangling graph references
    for m in modes:
        for field in ("violates", "causes", "is_a", "relates_to", "relates"):
            for tgt in (m.get(field) or []):
                t = tgt if isinstance(tgt, str) else tgt.get("id", "")
                # violates->principles, causes->harms are not mode ids; only check mode-to-mode
                if field in ("is_a", "relates_to", "relates") and t and t not in ids:
                    errors.append(f"[dangling-ref] {m['id']}.{field} -> '{t}' (no such mode)")

    # 3. required fields present and non-empty
    for m in modes:
        for field in ("name", "definition", "example", "category", "family"):
            if not (m.get(field) or "").strip():
                errors.append(f"[empty-field] {m['id']} missing/empty '{field}'")

    # 3b. em/en dashes in prose fields (AI-writing tell; keep hyphens in compounds/ids only)
    for m in modes:
        fields = {"definition": m.get("definition", ""), "example": m.get("example", ""),
                  "human_parallel": m.get("human_parallel", ""), "name": m.get("name", "")}
        for i, e in enumerate(m.get("examples") or []):
            fields[f"examples[{i}]"] = e
        for fn, txt in fields.items():
            txt = str(txt)
            if "—" in txt or "–" in txt:
                errors.append(f"[em-en-dash] {m['id']}.{fn} contains an em/en dash")

    # 4. arxiv integrity
    arxiv_to_modes = defaultdict(list)
    for m in modes:
        ax = m.get("arxiv") or {}
        papers = ax.get("papers") or []
        count = ax.get("count")
        if papers:
            if count is not None and isinstance(count, int) and count < len(papers):
                warns.append(f"[count<papers] {m['id']} count={count} but {len(papers)} papers listed")
            for p in papers:
                pid = str(p.get("id", "")).strip()
                yr = str(p.get("year", "")).strip()
                mobj = ARXIV.match(pid)
                if not mobj:
                    errors.append(f"[bad-arxiv-id] {m['id']} '{pid}' not YYMM.NNNNN")
                    continue
                yy, mm = mobj.group(1), mobj.group(2)
                if not ("01" <= mm <= "12"):
                    errors.append(f"[bad-arxiv-month] {m['id']} '{pid}' month {mm}")
                if (yy + mm) > now_ym:
                    errors.append(f"[future-arxiv] {m['id']} '{pid}' dated {yy}/{mm}, after now ({now_ym}) -> cannot exist")
                # arXiv announces late-month submissions the following month, so a Dec 2025
                # submission gets a 2601 (Jan 2026) id while its stated year is legitimately 2025.
                # Only flag a mismatch larger than that one-year announcement rollover, as a warning.
                if yr and yr.isdigit():
                    if abs(int("20" + yy) - int(yr)) > 1:
                        errors.append(f"[year-mismatch] {m['id']} '{pid}' id-year 20{yy} vs stated {yr} (>1yr)")
                    elif int("20" + yy) != int(yr):
                        warns.append(f"[year-rollover] {m['id']} '{pid}' id-year 20{yy} vs stated {yr} (ok if late-month submission)")
                arxiv_to_modes[pid].append(m["id"])

    # 5. same arXiv paper cited by many unrelated modes (citation-drift smell)
    for pid, ms in arxiv_to_modes.items():
        if len(ms) >= 4:
            warns.append(f"[reused-citation] {pid} cited by {len(ms)} modes: {', '.join(ms[:6])}{'...' if len(ms)>6 else ''}")

    print(f"Checked {len(modes)} modes, {sum(len(m.get('arxiv',{}).get('papers',[])) for m in modes)} citations.")
    print(f"\nERRORS ({len(errors)}):")
    for e in errors: print("  " + e)
    print(f"\nWARNINGS ({len(warns)}):")
    for w in warns: print("  " + w)
    print("\n" + ("PASS - no hard errors" if not errors else f"FAIL - {len(errors)} errors"))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
