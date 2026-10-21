#!/usr/bin/env python3
"""build-ontology.py - ONE-TIME migration: consolidate the scattered failure-mode
data into a single ethical-AI ontology at ontology/ethical-ai.yaml.

After this runs once, ontology/ethical-ai.yaml is the source of truth, maintained
by hand (or an ontologist), and build-catalogue.py reads it. This script exists to
seed that file from the current sources, and to re-seed if we ever need to.

Sources consolidated (the current page is built from these):
  references/research-2026-05-23-neuroscience-parallels.md  (100 brain modes)
  experiments/shipped-checks.tsv + shipped-check-papers.json (26 highlighted)
  experiments/catalogue-extra.tsv                            (4 agentic/eng modes)
  experiments/catalogue-examples.tsv                         (examples by num)
  experiments/catalogue-papers.json + suppress               (papers by num)

Output ontology has: meta, principles, harm_types, mitigations, governance,
relation_types, families, and modes (one record per rendered box, 130). The 13
highlighted modes that restate a brain mode carry a same_as link.
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
OUT = ROOT / "ontology" / "ethical-ai.yaml"

ENTRY_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+`(page|research|analogy)`\s+(.+)$")
SECTION_RE = re.compile(r"^##\s+\d+\.\s+(.+?)\s*$")


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s


# highlighted id -> brain num it restates (same_as)
SAME_AS = {
    "hallucination": 8, "confabulation": 7, "sycophancy": 65, "capitulation": 66,
    "overconfidence": 43, "confirmation-bias": 36, "anchoring": 31,
    "obedience-to-authority": 64, "source-monitoring": 15, "cognitive-load": 53,
    "belief-bias": 57, "conformity-asch": 63, "selective-evidence": 54,
}
# highlighted id -> contract clause (shipped checks only)
CLAUSE = {
    "hallucination": "INT-HAL", "confabulation": "INT-CFB",
    "source-fabrication": "INT-SRC", "sycophancy": "INT-SYC",
    "capitulation": "INT-CAP", "confirmation-bias": "INT-CNF",
    "selective-evidence": "INT-SEL", "anchoring": "INT-ANC",
    "automation-bias": "INT-AUT", "overconfidence": "INT-OVR",
    "prompt-injection": "INT-INJ", "scope-creep": "INT-SCP",
    "specification-gaming": "INT-GAM",
}
# short category label per brain group index (1-10), shown in the row pill
GROUP_SHORT = {
    1: "Perception", 2: "Memory", 3: "Attention", 4: "Heuristics",
    5: "Metacognition", 6: "Reasoning", 7: "Social", 8: "Moral",
    9: "Self & agency", 10: "Language",
}
# short category for highlighted modes (what domain the check belongs to)
CATEGORY = {
    "hallucination": "Perception", "confabulation": "Perception",
    "source-fabrication": "Memory", "sycophancy": "Social",
    "capitulation": "Social", "selective-evidence": "Reasoning",
    "prompt-injection": "Security", "overconfidence": "Metacognition",
    "scope-creep": "Agentic", "specification-gaming": "Agentic",
    "confirmation-bias": "Heuristics", "obedience-to-authority": "Social",
    "source-monitoring": "Memory", "anchoring": "Heuristics",
    "cognitive-load": "Reasoning", "belief-bias": "Reasoning",
    "conformity-asch": "Social", "automation-bias": "Agentic",
    "silent-error-swallowing": "Agentic", "side-effect-blindness": "Agentic",
    "noble-cause-corruption": "Moral", "deceptive-alignment": "Misalignment",
    "scheming-power-seeking": "Misalignment", "ai-deception": "Misalignment",
    "anthropomorphism": "Social", "survivorship-bias": "Heuristics",
}
# measurability overrides (default is 'draft')
HARD = {
    "deceptive-alignment": "multi-turn", "scheming-power-seeking": "multi-turn",
    "ai-deception": "multi-turn", "survivorship-bias": "draft",
}
BRAIN_ORIGIN = "cognitive-neuroscience"


def load_lines(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        rows.append(line.split("\t"))
    return rows


def parse_brain():
    sections, cur = [], None
    for line in (ROOT / "references" / "research-2026-05-23-neuroscience-parallels.md"
                 ).read_text(encoding="utf-8").splitlines():
        sm = SECTION_RE.match(line)
        if sm:
            cur = (sm.group(1), [])
            sections.append(cur)
            continue
        em = ENTRY_RE.match(line)
        if em and cur is not None:
            num, name, tag, definition = em.groups()
            cur[1].append((int(num), name.strip(), tag, definition.strip()))
    return sections


def main():
    examples = {int(a): b.strip() for a, b in load_lines(EXP / "catalogue-examples.tsv")}
    papers_by_num = {int(k): v for k, v in json.loads(
        (EXP / "catalogue-papers.json").read_text()).items()}
    suppress = {int(x) for x in (EXP / "catalogue-papers-suppress.txt").read_text().split()
                if x.strip().isdigit()}
    shipped_papers = json.loads((EXP / "shipped-check-papers.json").read_text())

    modes = []

    # brain modes (100), one family per section
    for i, (title, entries) in enumerate(parse_brain(), 1):
        fam = slug(title.replace(" and ", " "))
        for num, name, tag, definition in entries:
            pdata = None if num in suppress else papers_by_num.get(num)
            rec = {
                "id": f"b{num:03d}-{slug(name)}",
                "num": num,
                "name": name,
                "definition": definition,
                "example": examples.get(num, ""),
                "family": fam,
                "group_label": title,
                "category": GROUP_SHORT.get(i, ""),
                "highlighted": False,
                "tag": tag,
                "origin": BRAIN_ORIGIN,
                "measurability": "undetectable" if 81 <= num <= 90 else "draft",
                "arxiv": arxiv_block(pdata),
            }
            modes.append(rec)

    # extra agentic/engineering modes
    for num_s, name, tag, definition in load_lines(EXP / "catalogue-extra.tsv"):
        num = int(num_s)
        pdata = None if num in suppress else papers_by_num.get(num)
        modes.append({
            "id": f"x{num}-{slug(name)}",
            "num": num,
            "name": name, "definition": definition,
            "example": examples.get(num, ""),
            "family": "agentic-engineering",
            "group_label": "Agentic and engineering failure modes (beyond the brain map)",
            "category": "Agentic",
            "highlighted": False, "tag": tag, "origin": "software-engineering",
            "measurability": "draft", "arxiv": arxiv_block(pdata),
        })

    # highlighted modes (26)
    for seq_s, cid, name, definition, example in load_lines(EXP / "shipped-checks.tsv"):
        seq = int(seq_s)
        rec = {
            "id": cid, "name": name, "definition": definition, "example": example,
            "family": "highlighted", "group_label": "Highlighted checks",
            "category": CATEGORY.get(cid, ""),
            "highlighted": True, "highlight_order": seq,
            "tag": "shipped" if cid in CLAUSE else "research",
            "origin": "alignment" if cid in HARD or cid in (
                "deceptive-alignment", "scheming-power-seeking", "ai-deception",
                "noble-cause-corruption", "anthropomorphism") else "mixed",
            "measurability": HARD.get(cid, "draft"),
            "arxiv": arxiv_block(shipped_papers.get(cid)),
        }
        if cid in CLAUSE:
            rec["contract_clause"] = CLAUSE[cid]
        if cid in SAME_AS:
            n = SAME_AS[cid]
            # find the brain record id
            match = next((m["id"] for m in modes if m["id"].startswith(f"b{n:03d}-")), None)
            if match:
                rec["same_as"] = match
        modes.append(rec)

    onto = build_framework()
    onto["modes"] = modes
    onto["meta"]["mode_count"] = len(modes)
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        yaml.dump(onto, fh, sort_keys=False, allow_unicode=True, width=100)
    print(f"wrote {len(modes)} modes to {OUT}")


def arxiv_block(pdata):
    if not pdata or not pdata.get("papers"):
        return {"count": pdata.get("count") if pdata else None, "papers": []}
    return {
        "count": pdata.get("count"),
        "papers": [{"id": re.sub(r"v\d+$", "", p["id"]), "year": p.get("year", ""),
                    "title": p.get("title", "")} for p in pdata["papers"][:3]],
    }


def build_framework():
    return yaml.safe_load(FRAMEWORK)


FRAMEWORK = """
meta:
  name: Ethical AI ontology
  version: 1
  description: >
    A single source of truth for AI integrity: the principles an agent should
    uphold, the failure modes that violate them, the harms they cause, the
    mitigations that detect them, and the governance around changes. The page at
    ethicalai.alexandrudan.com and the EthicalHive checks build from this file.
  updated: '2026-10-19'

relation_types:
  is_a: narrower term of a broader failure family
  relates_to: adjacent or co-occurring failure mode
  root_of: a cause that produces the linked failure
  opposite_of: the failure at the other end of the same axis
  same_as: two catalogue entries that denote the same underlying failure
  violates: the principle this failure breaches
  causes: the harm type this failure produces
  detected_by: the mitigation that can catch this failure

principles:
  - id: honesty
    name: Honesty
    statement: State only what the evidence supports; mark what is unverified.
  - id: calibration
    name: Calibration
    statement: Match stated confidence and completeness to the evidence.
  - id: non-maleficence
    name: Non-maleficence
    statement: Do not take or propose actions whose collateral harm outweighs the task.
  - id: scope-fidelity
    name: Scope fidelity
    statement: Stay within the request; disclose and offer any addition.
  - id: independence
    name: Independence
    statement: Hold a grounded position under pressure; do not agree or fold without evidence.
  - id: transparency
    name: Transparency
    statement: Make reasoning, sources, and uncertainty legible to the human.
  - id: corrigibility
    name: Corrigibility
    statement: Remain open to correction and oversight; do not resist shutdown or review.

harm_types:
  - id: wrong-answer
    name: Wrong answer
    statement: The human acts on a false belief.
  - id: wasted-effort
    name: Wasted effort
    statement: Work is spent on the wrong problem or a dead end.
  - id: manipulation
    name: Manipulation
    statement: The human is steered by flattery, false confidence, or false premises.
  - id: security-breach
    name: Security breach
    statement: Injected or collateral actions compromise the system.
  - id: loss-of-oversight
    name: Loss of oversight
    statement: The agent's true behaviour becomes unobservable to the human.

mitigations:
  - id: cove
    name: Chain-of-Verification
    statement: Extract each claim and verify it against sources before delivery.
  - id: clause-judge
    name: Clause judge agent
    statement: A read-only subagent that audits a draft for one contract clause.
  - id: contract
    name: AI Integrity Contract
    statement: The binding agreement of clauses the agent commits to per turn.
  - id: human-review
    name: Human decision
    statement: Findings are advisory; the human keeps the final word.

governance:
  calibration_change: two of three model tiers approve, plus human
  constitutional_change: three of three model tiers approve, plus human
  council: judge-council spawned across Opus, Sonnet, Haiku for tier diversity
  never_auto_applied: [rubric, verdict calculation, CoVe rules, BLOCK/FLAG/PASS criteria]

families:
  - id: highlighted
    name: Highlighted checks
    note: The prioritised, red-bordered featured set shown first on the page.
  - id: agentic-engineering
    name: Agentic and engineering failure modes
    note: Behaviours outside the brain-parallel corpus.
"""


if __name__ == "__main__":
    main()
