#!/usr/bin/env python3
"""principle-agreement.py - reproducibility probe for the seven-principle `violates` partition.

The category scheme already has a codebook check (taxonomy-agreement.py). This runs the same
protocol for the operational principle each behaviour is tagged with: is the catalogue's
`violates` assignment reproducible by a rater who did not build it, from the principle
definitions alone? As with the category probe, the raters are independent LLM calls blind to
the assignment; this is a proxy for, not a replacement of, human annotation.

Usage:
  principle-agreement.py sample [PER]   # stratified sample, PER records per principle (default 4),
                                        # from the grounded 207; writes the task JSON to stdout and
                                        # the gold map (id -> principle) to principle-gold.json
  principle-agreement.py prompts TASK.json       # emit JSONL {id, prompt} for a rater
  principle-agreement.py score GOLD RATER.jsonl [RATER2.jsonl ...]
                                        # Cohen kappa per rater vs the catalogue, inter-rater
                                        # kappa, and raw agreement with a Wilson interval

Rater output: one JSON object per line, {"id": "<mode id>", "assigned": "<principle>"}.
"""
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
GOLD = HERE / "principle-gold.json"

# reuse the chance-corrected stats from the category probe
_spec = importlib.util.spec_from_file_location("taxagree", HERE / "taxonomy-agreement.py")
_tax = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tax)

PRINCIPLES = {
    "honesty": "stating what is not supported: fabrication, confident guessing, misquotation, misrepresenting a fact or a source",
    "calibration": "confidence that does not track the evidence: over- or under-confidence, miscalibrated uncertainty, base-rate or probability error, misjudging one's own competence",
    "non-maleficence": "producing foreseeable harm: an unsafe action or recommendation, damage, or failing to prevent harm",
    "transparency": "not disclosing an action, a limitation, or an uncertainty; hidden process or willful blindness",
    "scope-fidelity": "acting outside the agreed task: scope creep, overreach, doing more or less than asked, drifting off-task",
    "independence": "a judgment improperly swayed by an external pull: sycophancy, flattery, anchoring, conformity, authority or framing pressure, order effects",
    "corrigibility": "resisting correction, oversight, override or shutdown; not updating when shown to be wrong",
}


def load_modes():
    return yaml.safe_load((ROOT / "ontology" / "ethical-ai.yaml").read_text())["modes"]


def one_principle(m):
    v = m.get("violates")
    if not v:
        return None
    return v[0] if isinstance(v, list) else v


def do_sample(per):
    modes = [m for m in load_modes() if m["num"] <= 207]  # grounded cohort
    by_p = defaultdict(list)
    for m in modes:
        p = one_principle(m)
        if p in PRINCIPLES:
            by_p[p].append(m)
    picked, gold = [], {}
    for p in sorted(by_p):
        for m in sorted(by_p[p], key=lambda x: x["num"])[:per]:
            picked.append({"id": m["id"], "name": m["name"], "definition": m.get("definition", "")})
            gold[m["id"]] = p
    GOLD.write_text(json.dumps(gold, indent=0))
    task = {"codebook": PRINCIPLES, "items": picked}
    sys.stderr.write(f"sampled {len(picked)} records ({per}/principle); gold -> {GOLD.name}\n")
    print(json.dumps(task, ensure_ascii=False, indent=2))


def do_prompts(task_path):
    task = json.loads(Path(task_path).read_text())
    cb = "\n".join(f"- {k}: {v}" for k, v in task["codebook"].items())
    for it in task["items"]:
        prompt = (
            "You are classifying an AI failure behaviour by the single integrity principle it "
            "most directly breaches. Choose exactly one id from this list:\n"
            f"{cb}\n\n"
            f"Behaviour: {it['name']}\n"
            f"Definition: {it['definition']}\n\n"
            "Answer with only the principle id, nothing else."
        )
        print(json.dumps({"id": it["id"], "prompt": prompt}, ensure_ascii=False))


def do_score(gold_path, rater_paths):
    gold = json.loads(Path(gold_path).read_text())
    ids = list(gold)
    raters = []
    for rp in rater_paths:
        amap = {}
        for line in Path(rp).read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            amap[o["id"]] = o["assigned"].strip()
        raters.append((Path(rp).stem, amap))
    gl = [gold[i] for i in ids]
    for name, amap in raters:
        rl = [amap.get(i, "MISSING") for i in ids]
        agree = sum(a == b for a, b in zip(gl, rl))
        po, pe, k = _tax.cohen_kappa(gl, rl)
        lo, hi = _tax.wilson(agree, len(ids))
        print(f"{name}: {agree}/{len(ids)} agree with catalogue, kappa {k:.2f} "
              f"(raw agreement {agree/len(ids):.2f}, Wilson 95% [{lo:.2f}, {hi:.2f}])")
    if len(raters) == 2:
        a = [raters[0][1].get(i, "A") for i in ids]
        b = [raters[1][1].get(i, "B") for i in ids]
        _, _, k = _tax.cohen_kappa(a, b)
        print(f"inter-rater kappa: {k:.2f}")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "sample":
        do_sample(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif cmd == "prompts":
        do_prompts(sys.argv[2])
    elif cmd == "score":
        do_score(sys.argv[2], sys.argv[3:])
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
