#!/usr/bin/env python3
"""taxonomy-agreement.py - reproducibility probe for the EthicalAI category structure.

The credibility question for a resource paper: is the catalogue's assignment of each mode
to one of the eleven categories (ten cognitive systems plus the AI-native tier)
reproducible by a rater who did not build it, or is it idiosyncratic to the author?

This script measures that with a codebook protocol. It does NOT produce human
inter-annotator agreement; the raters here are independent LLM calls, blind to the
catalogue's assignment. That is a proxy and a first signal, stated as such in the output
and required to be replaced (or backed) by human annotation before submission. What it is
good for now: a real chance-corrected number, and a stress test of whether the category
definitions are clear enough that an outside rater can apply them at all.

Usage:
  taxonomy-agreement.py sample [N]     # stratified sample of ~N modes (default 33, 3/cat)
                                       # writes task JSON (codebook + items, no gold label)
                                       # to stdout, and the gold map to agree-gold.json
  taxonomy-agreement.py prompts TASK.json   # emit JSONL {id, prompt} for the rater runner
  taxonomy-agreement.py score GOLD RATER.jsonl [RATER2.jsonl ...]
                                       # Cohen kappa per rater vs the catalogue (gold),
                                       # inter-rater kappa, raw agreement with Wilson CI

Rater output format (one JSON object per line): {"id": "<mode id>", "assigned": "<category>"}
"""
import json, sys, math
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
GOLD = ROOT / "experiments" / "agree-gold.json"

# One-line codebook gloss per category, so an outside rater applies the same definitions
# the catalogue used (standard annotation protocol: annotators get a codebook).
CODEBOOK = {
    "Perception": "failures of how input is perceived or predictively filled in before reasoning",
    "Memory": "failures of storage, recall, interference, or reconstruction of information",
    "Attention": "failures of what the model attends to: capture, blindness, salience, gating",
    "Heuristics": "fast judgment shortcuts and the classic decision biases (anchoring, base-rate, framing)",
    "Reasoning": "failures of inference, logic, calibration-free deduction, shortcut reasoning",
    "Metacognition": "failures of confidence, self-knowledge, knowing what one knows",
    "Language": "failures of parsing, pragmatics, register, semantics in language itself",
    "Social": "failures driven by other agents or users: conformity, sycophancy, persuasion, manipulation",
    "Moral": "failures of moral judgment, value application, and ethical reasoning",
    "Self & agency": "failures of identity, goal-tracking, self-model, and sense of agency",
    "AI-native": "failure modes with no human cognitive analogue, specific to the machine (reward hacking, prompt injection, scheming, model collapse)",
}


def load_modes():
    import yaml
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    return o["modes"]


def _pick(n):
    """Deterministic stratified sample: first `per` modes per category by num."""
    modes = load_modes()
    by_cat = defaultdict(list)
    for m in modes:
        c = m.get("category")
        if c in CODEBOOK:
            by_cat[c].append(m)
    per = max(1, n // len(CODEBOOK))
    picked = []
    for c in CODEBOOK:
        ms = sorted(by_cat.get(c, []), key=lambda m: m.get("num", 10**6))
        picked.extend(ms[:per])
    return picked, per


def do_sample(n):
    picked, per = _pick(n)
    gold = {m["id"]: m["category"] for m in picked}
    GOLD.write_text(json.dumps(gold, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    task = {
        "codebook": CODEBOOK,
        "categories": list(CODEBOOK.keys()),
        "items": [{"id": m["id"], "name": m["name"], "definition": m["definition"]}
                  for m in picked],
    }
    print(json.dumps(task, ensure_ascii=False))
    sys.stderr.write(f"sampled {len(picked)} modes ({per}/category); gold -> {GOLD}\n")


def do_worksheet(n):
    """Emit a blank human-annotation CSV (id, mode, definition, your_category) and the gold
    map, for a two-annotator study. The gold category is held out of the sheet."""
    import csv
    picked, per = _pick(n)
    gold = {m["id"]: m["category"] for m in picked}
    GOLD.write_text(json.dumps(gold, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out = ROOT / "experiments" / "human-annotation" / "annotation-sheet.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "mode", "definition",
                    "your_category (one of: " + " | ".join(CODEBOOK) + ")"])
        for m in picked:
            w.writerow([m["id"], m["name"], m["definition"], ""])
    sys.stderr.write(f"wrote {out.relative_to(ROOT)} ({len(picked)} modes); gold -> {GOLD}\n")


def do_ingest(csv_path, rater):
    """Convert a filled annotation CSV into a rater jsonl the `score` command reads."""
    import csv
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    out = ROOT / "experiments" / "results" / f"human-{rater}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            cat_col = next((k for k in r if k.startswith("your_category")), None)
            a = (r.get(cat_col) or "").strip()
            if not a:
                continue
            fh.write(json.dumps({"id": r["id"], "assigned": a}, ensure_ascii=False) + "\n")
            n += 1
    sys.stderr.write(f"wrote {out.relative_to(ROOT)} ({n} assignments)\n")


def do_prompts(task_path):
    task = json.loads(Path(task_path).read_text())
    cats = task["categories"]
    codebook = task["codebook"]
    book = "\n".join(f"- {c}: {codebook[c]}" for c in cats)
    names = ", ".join(cats)
    for it in task["items"]:
        prompt = (
            "You are an annotator applying a fixed codebook. Assign the AI failure mode "
            "below to exactly ONE of these eleven categories, by which cognitive system or "
            "tier it best fits. Use only the codebook definitions.\n\n"
            f"Categories and definitions:\n{book}\n\n"
            f"Failure mode: {it['name']}\n"
            f"Definition: {it['definition']}\n\n"
            f"Respond with ONLY the exact category name, one of: {names}. No other text."
        )
        print(json.dumps({"id": it["id"], "prompt": prompt}, ensure_ascii=False))


def cohen_kappa(a, b):
    """Cohen's kappa between two equal-length label sequences."""
    assert len(a) == len(b) and a
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    labels = set(a) | set(b)
    pe = sum((ca.get(l, 0) / n) * (cb.get(l, 0) / n) for l in labels)
    kappa = (po - pe) / (1 - pe) if pe != 1 else float("nan")
    return po, pe, kappa


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def do_score(argv):
    gold = json.loads(Path(argv[0]).read_text())
    raters = {}
    for path in argv[1:]:
        name = Path(path).stem
        d = {}
        for line in Path(path).read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            d[r["id"]] = r["assigned"]
        raters[name] = d

    print("Taxonomy category-assignment reproducibility (LLM-rater PROXY, not human IAA)")
    print("=" * 72)
    ids = [i for i in gold if all(i in r for r in raters.values())]
    print(f"items with all raters present: {len(ids)}\n")

    for name, d in raters.items():
        g = [gold[i] for i in ids]
        r = [d[i] for i in ids]
        agree = sum(1 for x, y in zip(g, r) if x == y)
        po, pe, k = cohen_kappa(g, r)
        iv = wilson(agree, len(ids))
        print(f"[{name}] vs catalogue")
        print(f"  raw agreement {agree}/{len(ids)} = {agree/len(ids):.2f}  [{iv[0]:.2f}, {iv[1]:.2f}]")
        print(f"  Cohen kappa   {k:.2f}  (po={po:.2f}, pe={pe:.2f})\n")

    names = list(raters)
    if len(names) >= 2:
        print("inter-rater (rater vs rater):")
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a = [raters[names[i]][x] for x in ids]
                b = [raters[names[j]][x] for x in ids]
                _, _, k = cohen_kappa(a, b)
                print(f"  {names[i]} vs {names[j]}: kappa {k:.2f}")
        print()

    print("NOTE: raters are independent LLM calls blind to the catalogue label, applying")
    print("the shared codebook. This is a reproducibility proxy and a clarity stress test,")
    print("NOT human inter-annotator agreement, which remains required before submission.")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "sample":
        do_sample(int(sys.argv[2]) if len(sys.argv) > 2 else 33)
    elif cmd == "worksheet":
        do_worksheet(int(sys.argv[2]) if len(sys.argv) > 2 else 33)
    elif cmd == "ingest":
        do_ingest(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "annotator")
    elif cmd == "prompts":
        do_prompts(sys.argv[2])
    elif cmd == "score":
        do_score(sys.argv[2:])
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
