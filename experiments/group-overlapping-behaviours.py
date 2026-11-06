#!/usr/bin/env python3
"""Apply the recorded operational-overlap review without deleting source records."""
import json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'ontology/ethical-ai.yaml';onto=yaml.safe_load(p.read_text())
review=json.loads((ROOT/'references/semantic-dedup-review-2026-11-06.json').read_text())
by={m['id']:m for m in onto['modes']}
for item in review['groupings']:
    assert item['id'] in by and item['under'] in by
    by[item['id']]['grouped_under']=item['under']
    by[item['id']]['grouping_reason']=item['reason']
    by[item['id']]['grouping_relation']='Operational overlap; not an assertion of psychological synonymy'
assert len(by)==434
assert sum(not m.get('grouped_under') for m in onto['modes'])==425
assert all(not by[m['grouped_under']].get('grouped_under') for m in onto['modes'] if m.get('grouped_under'))
onto['meta']['display_counts']=dict(numbered_entries=434,linked_overlap_records=9)
onto['meta']['count_note']='Record counts are not counts of mutually exclusive or independently established AI mechanisms.'
p.write_text(yaml.safe_dump(onto,allow_unicode=True,sort_keys=False,width=110))
print('434 numbered records; 9 overlap relationships retained as cross-references')
