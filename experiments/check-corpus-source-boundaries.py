#!/usr/bin/env python3
"""Check that terminology-only PDF references cannot fill behaviour paper gaps."""
import json
from pathlib import Path

import yaml
from catalogue_sources import available_papers, research_papers, source_coverage

ROOT = Path(__file__).resolve().parents[1]
ontology = yaml.safe_load((ROOT / 'ontology/ethical-ai.yaml').read_text())
modes = {mode['id']: mode for mode in ontology['modes']}
review = json.loads((ROOT / 'references/pdf-reviews/0041.json').read_text())
finding = next(f for f in review['findings'] if f.get('target_id') == 'upload-100')
assert finding['count_as_behaviour_paper'] is False
mode = modes['upload-100']
unrelated_url = review['citation']['url']
assert all(p['url'] != unrelated_url for p in available_papers(mode))
assert all(p['url'] != unrelated_url for p in mode['selected_papers'])
assert unrelated_url in source_coverage(mode)['reference_source_urls']
assert all(p['url'] != unrelated_url for p in research_papers(mode))
for term in ('epistemic-injustice', 'participatory-extraction'):
    assert any(p['url'] == unrelated_url for p in research_papers(modes[term]))
    assert any(p['url'] == unrelated_url for p in modes[term]['selected_papers'])
assert modes['participatory-extraction']['is_a'] == ['epistemic-injustice']
class_review = json.loads((ROOT / 'references/pdf-reviews/0042.json').read_text())
class_url = class_review['citation']['url']
moral = modes['b075-moral-disengagement']
assert all(p['url'] != class_url for p in available_papers(moral))
assert all(p['url'] != class_url for p in moral['selected_papers'])
assert class_url in source_coverage(moral)['reference_source_urls']
print('PASS: homonym reference retained without filling a paper gap; relevant evidence and subtype preserved')
