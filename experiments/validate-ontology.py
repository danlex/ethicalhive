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
CATEGORIES = {'Perception','Memory','Attention','Heuristics','Reasoning',
              'Metacognition','Language','Social','Moral','Self & agency','AI-native'}
TERM_RELATIONS = {'broader theory','broader concept','distinct related concept',
                  'negative counterpart','proposed mechanism','narrower variant'}


def main():
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    modes = o.get("modes", [])
    prin_ids = {p["id"] for p in o.get("principles", [])}
    harm_ids = {h["id"] for h in o.get("harm_types", [])}
    mode_ids = {m["id"] for m in modes}
    mit_ids = {m["id"] for m in o.get("mitigations", [])}
    by_id = {m['id']:m for m in modes}
    errors, warnings = [], []

    seen = set()
    used_prin, used_harm = set(), set()
    category_labels = {}
    nums = [m.get('num') for m in modes]
    if any(type(n) is not int for n in nums) or sorted(nums) != list(range(1,len(modes)+1)):
        errors.append('reference numbers must cover 1 through mode count exactly once')
    if o['meta'].get('mode_count') != len(modes):
        errors.append('meta.mode_count must equal the number of retained records')
    for m in modes:
        mid = m.get("id", "<no id>")
        for f in REQUIRED:
            # A proposed human-behaviour analogy need not imply a principle breach
            # or harm. Do not invent graph edges merely to satisfy the schema.
            if m.get('research_candidate') and f in ('violates', 'causes'):
                continue
            if not m.get(f):
                errors.append(f"{mid}: missing required field '{f}'")
        if mid in seen:
            errors.append(f"duplicate id: {mid}")
        seen.add(mid)
        category=m.get('category')
        if category not in CATEGORIES:
            errors.append(f'{mid}: unknown category {category!r}')
        label=m.get('group_label')
        if category in category_labels and category_labels[category] != label:
            errors.append(f'{mid}: category must have one consistent group_label')
        category_labels[category]=label
        aliases={s.casefold().strip() for s in m.get('synonyms',[])}
        for term in m.get('related_terms',[]):
            if not all(term.get(k) for k in ('name','relation','note')):
                errors.append(f'{mid}: related term needs name, relation and note')
            if term.get('relation') not in TERM_RELATIONS:
                errors.append(f'{mid}: unknown terminology relation {term.get("relation")!r}')
            if term.get('name','').casefold().strip() in aliases:
                errors.append(f'{mid}: a related non-synonym cannot also be an alias')
        for source in m.get('terminology_sources',[]):
            if not all(source.get(k) for k in ('title','url','consulted')):
                errors.append(f'{mid}: terminology source must disclose title, URL and access depth')
        if m.get('grouped_under'):
            target=next((x for x in modes if x['id']==m['grouped_under']),None)
            if not target or target is m or target.get('grouped_under'):
                errors.append(f'{mid}: grouping must resolve directly to a primary entry')
            if not m.get('grouping_reason'):
                errors.append(f'{mid}: grouped record needs a review rationale')
        if m.get("tag") not in TAGS:
            errors.append(f"{mid}: bad tag {m.get('tag')!r}")
        if m.get('research_candidate'):
            if m.get('tag') != 'analogy' or not m.get('ai_evidence_status'):
                errors.append(f'{mid}: research candidate must disclose its analogy status')
            if m.get('source_check') not in ('definition-source-consulted','pending-definition-source-check'):
                errors.append(f'{mid}: missing definition-source review status')
            if m.get('source_check') == 'definition-source-consulted' and not m.get('definition_sources'):
                errors.append(f'{mid}: consulted-source status requires source records')
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
        has_hp = bool(m.get("human_parallel"))
        has_ai = bool(m.get("ai_native"))
        if has_hp == has_ai:  # must be exactly one
            errors.append(f"{mid}: must have exactly one of human_parallel / ai_native "
                          f"(has human_parallel={has_hp}, ai_native={has_ai})")
        for r in m.get("relates_to", []):
            if r not in mode_ids:
                errors.append(f"{mid}: relates_to unknown mode '{r}'")
        for r in m.get("opposite_of", []):
            if r not in mode_ids:
                errors.append(f"{mid}: opposite_of unknown mode '{r}'")
        for r in m.get("root_of", []):
            if r not in mode_ids:
                errors.append(f"{mid}: root_of unknown mode '{r}'")
        for r in m.get("is_a", []):
            if r not in mode_ids:
                errors.append(f"{mid}: is_a unknown mode '{r}'")
            if r==mid:
                errors.append(f'{mid}: cannot be its own subtype')
        for d in m.get("detected_by", []):
            if d not in mit_ids:
                errors.append(f"{mid}: detected_by unknown mitigation '{d}'")
        for d in m.get("mitigated_by", []):
            if d not in mit_ids:
                errors.append(f"{mid}: mitigated_by unknown mitigation '{d}'")
        if m.get("same_as") and m["same_as"] not in mode_ids:
            errors.append(f"{mid}: same_as unknown mode '{m['same_as']}'")

    # A subtype hierarchy must not turn into a cycle as new links are added.
    visited,active=set(),set()
    def visit(mid):
        if mid in active:
            errors.append(f'is_a cycle at {mid}')
            return
        if mid in visited:return
        active.add(mid)
        for parent in by_id[mid].get('is_a',[]):
            if parent in by_id:visit(parent)
        active.remove(mid);visited.add(mid)
    for mid in by_id:visit(mid)

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

