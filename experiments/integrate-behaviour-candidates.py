#!/usr/bin/env python3
"""One-time, idempotent migration of the reviewed research into the existing catalogue."""
import copy
import json
import re
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
ONTO=ROOT/'ontology/ethical-ai.yaml'
SNAPSHOT=ROOT/'references/behaviour-candidates-integration-input-2026-11-06.json'
norm=lambda s:re.sub('[^a-z0-9]','',s.casefold())
CATEGORIES={
 'Memory and retrieval':'Memory','Attention and cognitive control':'Attention',
 'Learning and conditioning':'Reasoning','Judgment and evaluation':'Heuristics',
 'Social cognition':'Social','Motivation and self-regulation':'Self & agency',
 'Psychotherapy: thought patterns':'Reasoning','Psychotherapy: behaviour and interaction':'Social',
 'Language and perception':'Language','Choice and future preferences':'Heuristics',
 'Defence mechanisms':'Self & agency','Cognitive distortions':'Reasoning',
 'Psychotherapy process errors':'Social','Social influence and group behaviour':'Social',
 'Self-presentation and evasive speech':'Social','Organisational and institutional failure':'Reasoning',
 'Judgment and decision making':'Heuristics','Argument and rhetoric':'Reasoning',
 'Moral psychology':'Moral','Neuropsychology, action slips and conflict communication':'Attention',
 'Transactional analysis games':'Social','Group dynamics':'Social','Rhetoric and argument':'Reasoning',
 'Expert judgment and noise':'Metacognition','Error in complex tasks':'Reasoning',
 'Clinical and personality':'Self & agency'}
OVERRIDES={'candidate-064':'Self & agency','candidate-065':'Metacognition',
 'candidate-088':'Perception','candidate-089':'Perception','candidate-087':'Heuristics',
 'upload-091':'Self & agency','upload-092':'Language','upload-093':'Language',
 'upload-094':'Self & agency','upload-096':'Social','upload-097':'Social',
 'upload-098':'Social','upload-099':'Social','upload-100':'Social'}


def main():
    data=json.loads(SNAPSHOT.read_text())
    onto=yaml.safe_load(ONTO.read_text())
    baseline=[m for m in onto['modes'] if not m.get('research_candidate')]
    assert len(baseline)==207
    groups={}
    for m in baseline:groups.setdefault(m['category'],(m['group_label'],m['family']))
    by_id={m['id']:m for m in onto['modes']}
    aliases={}
    for m in baseline:
        for n in [m['name']]+m.get('synonyms',[]):aliases.setdefault(norm(n),m)
    sources={s['id']:s for s in data['sources']}
    decisions=[]
    for e in data['entries']:
        matches=[aliases[norm(n)] for n in [e['name']]+e.get('aliases',[]) if norm(n) in aliases]
        existing=matches[0] if matches else None
        if existing:
            note=copy.deepcopy(e)
            note['definition_sources']=[sources[s] for s in e['source_ids']]
            note['catalogue_boundary']='This term was already indexed as an alias here. The time-on-task effect and automation-induced complacency are not asserted to be identical mechanisms.'
            if not any(n == note for n in existing.get('research_notes',[])):
                existing['research_notes']=[n for n in existing.get('research_notes',[]) if n['id']!=e['id']]+[note]
            decisions.append(dict(research_id=e['id'],catalogue_id=existing['id'],disposition='enrich existing alias'))
            continue
        if e['id'] in by_id:
            assert by_id[e['id']].get('research_candidate')
            decisions.append(dict(research_id=e['id'],catalogue_id=e['id'],disposition='new analogy entry'))
            continue
        category=OVERRIDES.get(e['id'],CATEGORIES[e['group']])
        label,family=groups[category]
        m=dict(id=e['id'],num=max(x['num'] for x in onto['modes'])+1,name=e['name'],
               definition=e['definition'],category=category,family=family,group_label=label,
               tag='analogy',origin='Psychology / psychotherapy / behavioural research',
               highlighted=False,human_parallel=e['name'],research_candidate=True,
               source_check=e['source_check'],ai_evidence_status='Proposed analogy; not tested in this research',
               proposed_ai_manifestation=e['ai_manifestation'],proposal_kind=e['ai_text_kind'],
               research_boundary=e['distinction_and_limits'],research_field=e['group'],
               definition_sources=[sources[s] for s in e['source_ids']],
               research_provenance=dict(origins=e['origins'],contributions=e['contributions']),
               violates=[],causes=[])
        if e.get('aliases'):m['synonyms']=e['aliases']
        if e['related_modes']:m['relates_to']=[x['id'] for x in e['related_modes']]
        onto['modes'].append(m);by_id[m['id']]=m
        decisions.append(dict(research_id=e['id'],catalogue_id=m['id'],disposition='new analogy entry'))
    assert len(onto['modes'])==434
    assert sum(m.get('research_candidate',False) for m in onto['modes'])==227
    onto['meta'].update(version='1.1',updated='2026-11-06',mode_count=434,
        catalogue_counts=dict(previous_entries=207,added_analogies=227),
        expansion_note='Human-behaviour research is integrated in the same list. New entries are explicitly untested analogies; source review is stated per entry. Existing paper and experiment results describe the 207-entry baseline.')
    ONTO.write_text(yaml.safe_dump(onto,allow_unicode=True,sort_keys=False,width=110))
    manifest=dict(date='2026-11-06',previous_entries=207,research_records=228,
                  added_analogy_entries=227,enriched_existing_entries=1,total_entries=434,
                  decisions=decisions,note='Listing a human behaviour does not establish it as an AI mechanism. No checks, thresholds or judge rubrics were changed.')
    (ROOT/'references/catalogue-integration-2026-11-06.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='decisions'}))


if __name__=='__main__':main()
