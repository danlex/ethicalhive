#!/usr/bin/env python3
"""discover-rise.py - RISE: a Monte Carlo tree search that discovers new AI
failure modes and expands the ontology.

The tree is root -> areas (branches) -> candidate behaviours (leaves). One
iteration runs the four MCTS phases:

  1. Selection    pick which area to grow with UCB1 (exploit high-value branches,
                  explore thin ones), or open a brand-new area with probability eps.
  2. Expansion    the policy (an LLM over OpenRouter) proposes K new behaviours
                  under that area (progressive widening), told the whole ontology so
                  it does not repeat, each labelled human-paralleled or AI-native.
  3. Simulation   each candidate is grounded on arXiv (phrase + AI context over the
                  term and its synonyms) and then run through an LLM evaluation
                  function that (a) relevance-checks the arXiv hits so an off-topic
                  phrase match cannot inflate the score, (b) flags semantic
                  duplicates of existing modes, (c) rates quality. The reward gates
                  on in-scope / rule-fit / genuine-novelty / on-topic, and its
                  magnitude is grounding x quality. Reward in [0, 1].
  4. Backprop     the best child's reward updates the area value Q and visit count,
                  so the next Selection favours branches that keep yielding grounded,
                  genuinely novel behaviours.

arXiv results are cached to disk (arxiv-cache.json) so reruns are cheap and do not
get rate-limited. The loop stops at the iteration budget or after enough dry draws,
and writes ranked discoveries to discover-rise-results.{md,json} (shape-compatible
with the ontology map's "Proposed" branch).

Usage:
  discover-rise.py [--iterations 18] [--model openai/gpt-4o-mini] [--widen 2]
                   [--area-seed 6] [--area-max 10] [--cand-max 6]
                   [--c 1.2] [--new-eps 0.2] [--dry 6] [--seed 7]
"""

import argparse
import json
import math
import os
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
CACHE_FILE = HERE / "arxiv-cache.json"

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


def slug(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def toks(s):
    return set(slug(s).split())


def similar_modes(name, onto_names, k=6):
    """Top-k existing modes by token overlap, to give the judge a dedup shortlist."""
    nt = toks(name)
    scored = sorted(((len(nt & toks(n)) / len(nt | toks(n)) if (nt | toks(n)) else 0, n)
                     for n in onto_names), reverse=True)
    hits = [n for j, n in scored if j > 0][:k]
    return hits or [n for _, n in scored[:3]]


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


def propose_k(model, key, area, onto_names, avoid, k):
    """The policy: propose K distinct candidate behaviours, ordered most-promising first."""
    prompt = (
        "You are expanding an ontology of AI INTEGRITY failure modes: ways a deployed "
        "model or agent behaves wrongly during a conversation or task, how it reasons, "
        "what it claims, how it treats the user, how it handles oversight.\n"
        f"Branch: {area}\n\n"
        f"Propose {k} DISTINCT, specific, real failure modes in this branch that are "
        "studied in the AI literature and are NOT any of these already in the ontology:\n"
        f"{', '.join(onto_names)}\n"
        + (f"\nAlso avoid (already proposed this run): {', '.join(avoid)}\n" if avoid else "")
        + "\nIN SCOPE: behavioural and cognitive failures, e.g. sycophancy, "
        "confabulation, source fabrication, deceptive alignment, reward hacking, scope "
        "creep, sandbagging, gaslighting, flattery, capitulation under pressure.\n"
        "OUT OF SCOPE (do NOT propose): generic ML or statistics terms such as "
        "distribution shift, data/label/concept drift, overfitting, class imbalance, "
        "adversarial perturbations or patches, quantization or latency.\n"
        "Use the CANONICAL term as it appears in AI paper titles, and give up to two "
        "synonym phrasings. Order them most-promising first. Each must be "
        "human-paralleled (name the human-psychology construct) OR AI-native (give the "
        "reason it has no human analogue). Return a strict JSON list of length "
        f"{k}:\n"
        '[{"name": "<canonical mode name>", "synonyms": ["<alt>", "..."], '
        '"tier": "human" or "ai", "human_parallel": "<or empty>", '
        '"ai_native_reason": "<or empty>", "rationale": "<one sentence>"}]')
    out = extract_json(chat(model, prompt, key, temperature=0.95, max_tokens=700))
    if isinstance(out, dict):
        out = out.get("candidates") or out.get("modes") or [out]
    return [c for c in (out or []) if isinstance(c, dict) and c.get("name")][:k]


def safe_fetch(query, cache):
    """arXiv with a polite delay and backoff; returns (count, [top titles])."""
    if query in cache:
        c = cache[query]
        return c[0], c[1]
    for attempt in range(3):
        try:
            time.sleep(3)
            total, papers = fetch(query, 3)
            titles = [p[2] for p in papers][:2]
            cache[query] = [total or 0, titles]
            return total or 0, titles
        except Exception:
            if attempt == 2:
                cache[query] = [None, []]
                return None, []
            time.sleep(8 * (attempt + 1))


def arxiv_query(cand):
    phrases = [cand["name"]] + [p for p in (cand.get("synonyms") or []) if p][:2]
    ors = " OR ".join(f'all:"{p}"' for p in phrases)
    return f'(({ors}) AND (all:LLM OR all:"language model" OR all:AI OR all:agent))'


def evaluate(model, key, cands):
    """The MCTS evaluation function: relevance-check arXiv hits, flag semantic
    duplicates, rate quality. Returns a list aligned to cands."""
    lines = []
    for i, c in enumerate(cands):
        tier = (f"human parallel: {c.get('human_parallel')}" if c.get("tier") == "human"
                else f"AI-native: {c.get('ai_native_reason')}")
        titles = "; ".join(c.get("_titles") or []) or "none found"
        lines.append(
            f"[{i}] {c['name']} - {c.get('rationale', '')}\n"
            f"    {tier}\n    sample arXiv titles: {titles}\n"
            f"    similar existing modes: {', '.join(c.get('_similar', []))}")
    prompt = (
        "You are vetting candidate AI integrity failure modes for an ontology. For each "
        "candidate decide three things, using the sample arXiv titles as evidence:\n"
        "1) on_topic (0.0-1.0): do the titles show the AI literature actually studies "
        "THIS behaviour? If the titles are about something else, score low.\n"
        "2) duplicate_of: if it is essentially the same failure as one of the listed "
        "similar existing modes, give that mode's exact name; otherwise null.\n"
        "3) quality (0.0-1.0): is it a crisp, real, distinct integrity/behaviour failure "
        "mode (not vague, not generic ML)?\n\n"
        "Candidates:\n" + "\n".join(lines) +
        '\n\nReturn a strict JSON list, one object per index: '
        '[{"i":0,"on_topic":0.0,"duplicate_of":null,"quality":0.0}]')
    out = extract_json(chat(model, prompt, key, temperature=0, max_tokens=600))
    verdicts = {}
    if isinstance(out, list):
        for v in out:
            if isinstance(v, dict) and "i" in v:
                verdicts[int(v["i"])] = v
    # conservative fallback for any missing verdict
    return [verdicts.get(i, {"on_topic": 0.6, "duplicate_of": None, "quality": 0.5})
            for i in range(len(cands))]


def combine(cand, verdict, area, onto_slugs, discovered_slugs):
    name = cand["name"].strip()
    s = slug(name)
    in_scope = not OUT_OF_SCOPE.search(name)
    tier = (cand.get("tier") or "").lower()
    rule_ok = ((tier == "human" and cand.get("human_parallel"))
               or (tier == "ai" and cand.get("ai_native_reason")))
    dup = verdict.get("duplicate_of")
    dup = dup.strip() if isinstance(dup, str) and dup.strip().lower() not in ("", "null", "none") else None
    novel = s not in onto_slugs and s not in discovered_slugs and not dup
    on_topic = float(verdict.get("on_topic") or 0)
    quality = float(verdict.get("quality") or 0)
    count = cand.get("_count") or 0
    gate = in_scope and bool(rule_ok) and novel and on_topic >= 0.5
    magnitude = ground_score(count) * (0.5 + 0.5 * quality)
    reward = round(magnitude, 3) if gate else 0.0
    return {"area": area, "term": name, "tier": tier,
            "human_parallel": cand.get("human_parallel", ""),
            "ai_native_reason": cand.get("ai_native_reason", ""),
            "count": count, "top": "; ".join(cand.get("_titles") or []),
            "novel": novel, "in_scope": in_scope, "rule_ok": bool(rule_ok),
            "on_topic": round(on_topic, 2), "quality": round(quality, 2),
            "duplicate_of": dup, "reward": reward, "rationale": cand.get("rationale", "")}


def pick_area(areas, rng, c, area_max, cand_max, new_eps):
    open_areas = [a for a in areas if a["N"] < cand_max]
    if len(areas) < area_max and (not open_areas or rng.random() < new_eps):
        return None
    nroot = sum(a["N"] for a in areas) + 1
    return max(open_areas, key=lambda a: (float("inf") if a["N"] == 0 else
              a["Q"] + c * math.sqrt(math.log(nroot) / a["N"])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=18)
    ap.add_argument("--model", default="openai/gpt-4o-mini")
    ap.add_argument("--widen", type=int, default=2, help="candidates proposed per expansion")
    ap.add_argument("--area-seed", type=int, default=6)
    ap.add_argument("--area-max", type=int, default=10)
    ap.add_argument("--cand-max", type=int, default=6)
    ap.add_argument("--c", type=float, default=1.2)
    ap.add_argument("--new-eps", type=float, default=0.2)
    ap.add_argument("--dry", type=int, default=6)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    load_env()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not found in a local .env at the repo root.")

    onto = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    onto_names = [m["name"] for m in onto["modes"]]
    onto_slugs = {slug(n) for n in onto_names}
    rng = random.Random(args.seed)
    arxiv_cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}

    areas = []
    discovered = []
    discovered_slugs = set()
    dry = 0

    def open_area():
        used = [a["name"] for a in areas]
        if len(areas) < len(CURATED_AREAS):
            name, why = CURATED_AREAS[len(areas)], "curated seed branch"
        else:
            name, why = new_area_name(args.model, key, used)
        if not name or slug(name) in {slug(u) for u in used}:
            name, why = f"branch {len(areas) + 1}", ""
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

        avoid = [c["term"] for c in area["cands"]] + [c["term"] for c in discovered[-10:]]
        cands = propose_k(args.model, key, area["name"], onto_names, avoid, args.widen)
        area["N"] += 1
        if not cands:
            area["Q"] = area["W"] / area["N"]
            dry += 1
            print(f"  [{it + 1:>2}] {area['name']}: no candidates", file=sys.stderr)
            continue

        for c in cands:
            cnt, titles = safe_fetch(arxiv_query(c), arxiv_cache)
            c["_count"], c["_titles"] = (cnt or 0), titles
            c["_similar"] = similar_modes(c["name"], onto_names)
        verdicts = evaluate(args.model, key, cands)

        best = 0.0
        for c, v in zip(cands, verdicts):
            sc = combine(c, v, area["name"], onto_slugs, discovered_slugs)
            area["cands"].append(sc)
            discovered.append(sc)
            if sc["novel"] and sc["reward"] > 0:
                discovered_slugs.add(slug(sc["term"]))
            best = max(best, sc["reward"])
            dflag = f" dup={sc['duplicate_of']}" if sc["duplicate_of"] else ""
            print(f"  [{it + 1:>2}] {area['name']:<24} {sc['term']:<28} "
                  f"r={sc['reward']:<5} arXiv={sc['count']:<5} ot={sc['on_topic']} "
                  f"q={sc['quality']} {sc['tier']}{dflag}", file=sys.stderr)
        area["W"] += best
        area["Q"] = area["W"] / area["N"]
        dry = 0 if best > 0 else dry + 1
        if dry >= args.dry and it + 1 >= args.area_seed:
            print(f"  dry for {dry} draws, stopping at iteration {it + 1}", file=sys.stderr)
            break

    CACHE_FILE.write_text(json.dumps(arxiv_cache, indent=0), encoding="utf-8")
    write_results(args, areas, discovered)


def write_results(args, areas, discovered):
    kept = [c for c in discovered if c["novel"] and c["reward"] > 0]
    kept.sort(key=lambda c: (-c["reward"], -c["count"]))
    areas_rank = sorted(areas, key=lambda a: -a["Q"])

    out = [f"# RISE discovery run ({args.model})",
           f"\n{len(discovered)} candidates evaluated across {len(areas)} branches "
           f"(widen={args.widen}), {len(kept)} novel and grounded. UCB C={args.c}, "
           f"new-area eps={args.new_eps}, seed={args.seed}.\n",
           "## Discoveries (novel, grounded, on-topic), ranked by reward\n",
           "| Reward | Mode | Branch | Tier | Human parallel / AI-native | arXiv | on-topic | quality |",
           "|---|---|---|---|---|---|---|---|"]
    for c in kept:
        tier = c["human_parallel"] if c["tier"] == "human" else f"AI-native: {c['ai_native_reason']}"
        out.append(f"| {c['reward']:g} | {c['term']} | {c['area']} | {c['tier']} | "
                   f"{tier[:50]} | {c['count']} | {c['on_topic']} | {c['quality']} |")
    out.append("\n## Rejected near-duplicates (caught by the evaluation function)\n")
    dups = [c for c in discovered if c["duplicate_of"]]
    if dups:
        out.append("| Candidate | Judged duplicate of | Branch |\n|---|---|---|")
        for c in dups:
            out.append(f"| {c['term']} | {c['duplicate_of']} | {c['area']} |")
    else:
        out.append("None.")
    out.append("\n## Branch value (backpropagated Q = mean best reward)\n")
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
          f"({len(kept)} discoveries, {len(dups)} dups filtered)", file=sys.stderr)


if __name__ == "__main__":
    main()
