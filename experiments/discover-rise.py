#!/usr/bin/env python3
"""discover-rise.py - RISE: a Monte Carlo tree search that discovers new AI
failure modes and expands the ontology.

The tree is root -> areas (branches) -> candidate behaviours (leaves). One
iteration runs the four MCTS phases:

  1. Selection    pick which area to grow with UCB1 (exploit high-value branches,
                  explore thin ones), or open a brand-new area with probability eps.
  2. Expansion    an LLM (the generative policy, over OpenRouter) proposes ONE new
                  behaviour under that area, told what is already in the ontology so
                  it does not repeat, and asked to label it human-paralleled or
                  AI-native with a suggested arXiv query.
  3. Simulation   the reward is external and cheap to trust: novelty (absent from
                  the ontology) x grounding (how much the AI literature studies it,
                  via arXiv) x rule-fit (a valid human parallel, or a real reason it
                  is AI-native). Reward in [0, 1].
  4. Backprop     the reward updates the area's value Q and visit count N, so the
                  next Selection favours whichever branch keeps yielding grounded,
                  novel behaviours.

The loop stops at the iteration budget or after enough consecutive dry draws
(nothing novel or grounded), and writes ranked discoveries to
discover-rise-results.{md,json}. The JSON is shape-compatible with the ontology
map so the discoveries show up as the explorable "Proposed" branch.

Usage:
  discover-rise.py [--iterations 20] [--model openai/gpt-4o-mini]
                   [--area-seed 5] [--area-max 9] [--cand-max 6]
                   [--c 1.2] [--new-eps 0.2] [--dry 6] [--seed 7]
"""

import argparse
import math
import random
import re
import sys
import time
from pathlib import Path

import yaml

from arxiv_citations import fetch
from openrouter import load_env, chat, extract_json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"


def slug(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


# curated in-domain seed branches, so the tree starts on integrity behaviour,
# not generic ML. The loop can still open new branches beyond these.
CURATED_AREAS = [
    "social manipulation and persuasion",
    "deception and oversight evasion",
    "affective and parasocial failures",
    "reasoning and metacognition failures",
    "agentic overreach and goal integrity",
    "knowledge and memory corruption",
]

# phrases that mark a generic ML/statistics term rather than a behaviour
OUT_OF_SCOPE = re.compile(
    r"\b(distribution shift|data drift|label shift|concept drift|covariate|overfit|"
    r"underfit|class imbalance|adversarial (patch|perturbation|example)|quantiz|"
    r"latency|throughput|gradient|optimizer)\b", re.I)


def ground_score(count):
    if count <= 0:
        return 0.0
    return min(1.0, math.log10(count + 1) / math.log10(500))


def new_area_name(model, key, used):
    prompt = (
        "We map an ontology of AI INTEGRITY failure modes: ways a deployed model or "
        "agent BEHAVES wrongly in a conversation or task (how it reasons, what it "
        "claims, how it treats the user, how it handles oversight). Propose ONE new "
        "branch to explore, DIFFERENT from these already-used branches:\n"
        f"{', '.join(used) or '(none yet)'}\n\n"
        "The branch must be about behaviour and cognition, NOT generic ML or statistics "
        "(no distribution shift, data drift, overfitting, adversarial perturbations). "
        'Return strict JSON: {"area": "<short branch name>", "rationale": "<one sentence>"}')
    j = extract_json(chat(model, prompt, key, temperature=1.0, max_tokens=150)) or {}
    return j.get("area"), j.get("rationale", "")


def propose_candidate(model, key, area, onto_names, avoid):
    prompt = (
        "You are expanding an ontology of AI INTEGRITY failure modes: ways a deployed "
        "model or agent behaves wrongly during a conversation or task, how it reasons, "
        "what it claims, how it treats the user, how it handles oversight.\n"
        f"Branch: {area}\n\n"
        "Propose ONE specific, real failure mode in this branch that is studied in the "
        "AI literature and is NOT any of these already in the ontology:\n"
        f"{', '.join(onto_names)}\n"
        + (f"\nAlso avoid (already proposed this run): {', '.join(avoid)}\n" if avoid else "")
        + "\nIN SCOPE: behavioural and cognitive failures, e.g. sycophancy, "
        "confabulation, source fabrication, deceptive alignment, reward hacking, scope "
        "creep, sandbagging, gaslighting, flattery, capitulation under pressure.\n"
        "OUT OF SCOPE (do NOT propose): generic ML or statistics terms such as "
        "distribution shift, data/label/concept drift, overfitting, class imbalance, "
        "adversarial perturbations or patches, quantization or latency. Those are not "
        "integrity behaviours.\n"
        "Use the CANONICAL term as it actually appears in AI paper titles and abstracts, "
        "and give up to two synonym phrasings so it can be found. The mode must be "
        "human-paralleled (name the human-psychology construct) OR AI-native (give the "
        "reason it has no human analogue). Return strict JSON only:\n"
        '{"name": "<canonical mode name>", "synonyms": ["<alt phrasing>", "..."], '
        '"tier": "human" or "ai", "human_parallel": "<human construct, or empty>", '
        '"ai_native_reason": "<why no human analogue, or empty>", '
        '"rationale": "<one sentence on what it is>"}')
    return extract_json(chat(model, prompt, key, temperature=0.9, max_tokens=300)) or {}


def safe_fetch(query, cache):
    """arXiv with a polite delay and backoff, so a 429 never crashes the loop."""
    if query in cache:
        return cache[query]
    for attempt in range(3):
        try:
            time.sleep(3)
            total, papers = fetch(query, 2)
            res = (total or 0, papers[0][2] if papers else "")
            cache[query] = res
            return res
        except Exception:
            if attempt == 2:
                cache[query] = (None, "")
                return (None, "")
            time.sleep(8 * (attempt + 1))


def score(cand, onto_slugs, discovered_slugs, arxiv_cache):
    name = (cand.get("name") or "").strip()
    s = slug(name)
    if not name or len(s) < 3:
        return None
    novel = s not in onto_slugs and s not in discovered_slugs
    in_scope = not OUT_OF_SCOPE.search(name)
    tier = (cand.get("tier") or "").lower()
    rule_ok = ((tier == "human" and cand.get("human_parallel"))
               or (tier == "ai" and cand.get("ai_native_reason")))
    # build the arXiv clause deterministically; free-form model queries match the whole
    # category. Phrase match on the term or a synonym, AND AI context, keeps it on-topic.
    phrases = [name] + [p for p in (cand.get("synonyms") or []) if p][:2]
    ors = " OR ".join(f'all:"{p}"' for p in phrases)
    query = f'(({ors}) AND (all:LLM OR all:"language model" OR all:AI OR all:agent))'
    count, top = safe_fetch(query, arxiv_cache)
    gscore = ground_score(count or 0)
    gate = (1.0 if novel else 0.0) * (1.0 if rule_ok else 0.0) * (1.0 if in_scope else 0.0)
    reward = gate * gscore
    return {"area": cand.get("_area"), "term": name, "tier": tier,
            "human_parallel": cand.get("human_parallel", ""),
            "ai_native_reason": cand.get("ai_native_reason", ""),
            "count": count or 0, "top": top, "novel": novel, "in_scope": in_scope,
            "reward": round(reward, 3), "rule_ok": bool(rule_ok),
            "rationale": cand.get("rationale", "")}


def pick_area(areas, rng, c, area_max, cand_max, new_eps):
    open_areas = [a for a in areas if len(a["cands"]) < cand_max]
    if len(areas) < area_max and (not open_areas or rng.random() < new_eps):
        return None  # open a new area
    nroot = sum(a["N"] for a in areas) + 1
    return max(open_areas, key=lambda a: (float("inf") if a["N"] == 0 else
              a["Q"] + c * math.sqrt(math.log(nroot) / a["N"])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=20)
    ap.add_argument("--model", default="openai/gpt-4o-mini")
    ap.add_argument("--area-seed", type=int, default=6)
    ap.add_argument("--area-max", type=int, default=9)
    ap.add_argument("--cand-max", type=int, default=6)
    ap.add_argument("--c", type=float, default=1.2)
    ap.add_argument("--new-eps", type=float, default=0.2)
    ap.add_argument("--dry", type=int, default=6)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    load_env()
    import os
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not found in a local .env at the repo root.")

    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    onto_names = [m["name"] for m in onto["modes"]]
    onto_slugs = {slug(n) for n in onto_names}
    rng = random.Random(args.seed)

    areas = []            # {name, rationale, N, W, Q, cands:[scored]}
    discovered = []       # all scored candidates
    discovered_slugs = set()
    arxiv_cache = {}
    dry = 0

    def open_area():
        used = [a["name"] for a in areas]
        # seed from the curated in-domain branches first, then let the LLM extend
        if len(areas) < len(CURATED_AREAS):
            name, why = CURATED_AREAS[len(areas)], "curated seed branch"
        else:
            name, why = new_area_name(args.model, key, used)
        if not name or slug(name) in {slug(u) for u in used}:
            name = f"branch {len(areas) + 1}"
            why = ""
        a = {"name": name, "rationale": why, "N": 0, "W": 0.0, "Q": 0.0, "cands": []}
        areas.append(a)
        print(f"  + area: {name}", file=sys.stderr)
        return a

    for it in range(args.iterations):
        if len(areas) < args.area_seed:
            area = open_area()
        else:
            area = pick_area(areas, rng, args.c, args.area_max, args.cand_max, args.new_eps)
            area = open_area() if area is None else area

        avoid = [c["term"] for c in area["cands"]] + [c["term"] for c in discovered[-12:]]
        cand = propose_candidate(args.model, key, area["name"], onto_names, avoid)
        cand["_area"] = area["name"]
        sc = score(cand, onto_slugs, discovered_slugs, arxiv_cache)
        if sc is None:
            print(f"  [{it + 1:>2}] {area['name']}: unparseable, skip", file=sys.stderr)
            area["N"] += 1
            area["Q"] = area["W"] / area["N"]
            dry += 1
        else:
            area["cands"].append(sc)
            area["N"] += 1
            area["W"] += sc["reward"]
            area["Q"] = area["W"] / area["N"]
            discovered.append(sc)
            if sc["novel"]:
                discovered_slugs.add(slug(sc["term"]))
            dry = dry + 1 if sc["reward"] == 0 else 0
            flag = "" if sc["reward"] > 0 else "  (dry)"
            print(f"  [{it + 1:>2}] {area['name']:<26} {sc['term']:<30} "
                  f"r={sc['reward']:<5} arXiv={sc['count']:<5} "
                  f"{sc['tier']} novel={sc['novel']}{flag}", file=sys.stderr)
        if dry >= args.dry and it + 1 >= args.area_seed:
            print(f"  dry for {dry} draws, stopping at iteration {it + 1}", file=sys.stderr)
            break

    write_results(args, areas, discovered)


def write_results(args, areas, discovered):
    import json
    kept = [c for c in discovered if c["novel"] and c["reward"] > 0]
    kept.sort(key=lambda c: (-c["reward"], -c["count"]))
    areas_rank = sorted(areas, key=lambda a: -a["Q"])

    out = [f"# RISE discovery run ({args.model})",
           f"\n{len(discovered)} candidates evaluated across {len(areas)} branches, "
           f"{len(kept)} novel and grounded. UCB C={args.c}, new-area eps={args.new_eps}, "
           f"seed={args.seed}.\n",
           "## Discoveries (novel + grounded), ranked by reward\n",
           "| Reward | Mode | Branch | Tier | Human parallel / AI-native reason | arXiv |",
           "|---|---|---|---|---|---|"]
    for c in kept:
        tier = c["human_parallel"] if c["tier"] == "human" else f"AI-native: {c['ai_native_reason']}"
        out.append(f"| {c['reward']:g} | {c['term']} | {c['area']} | {c['tier']} | "
                   f"{tier[:60]} | {c['count']} |")
    out.append("\n## Branch value (backpropagated Q = mean reward)\n")
    out.append("| Branch | Q | visits | novel kept |\n|---|---|---|---|")
    for a in areas_rank:
        nk = sum(1 for c in a["cands"] if c["novel"] and c["reward"] > 0)
        out.append(f"| {a['name']} | {a['Q']:.2f} | {a['N']} | {nk} |")
    (HERE / "discover-rise-results.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    (HERE / "discover-rise-results.json").write_text(json.dumps({
        "params": vars(args),
        "areas": [{"area": a["name"], "mean": round(a["Q"], 3), "n": a["N"],
                   "rationale": a["rationale"]} for a in areas_rank],
        "candidates": discovered,
    }, indent=2), encoding="utf-8")
    print(f"\nwrote discover-rise-results.md and .json "
          f"({len(kept)} discoveries)", file=sys.stderr)


if __name__ == "__main__":
    main()
