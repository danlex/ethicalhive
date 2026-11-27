#!/usr/bin/env python3
"""Guard the real forthcoming-issue case without admitting unverified future years."""
from copy import deepcopy
from datetime import date
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ontology_validator', ROOT / 'experiments/validate-ontology.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
ontology = yaml.safe_load((ROOT / 'ontology/ethical-ai.yaml').read_text())
mode = next(m for m in ontology['modes'] if m['id'] == 'cognitive-offloading')
paper = next(p for p in mode['selected_papers'] if p['url'].endswith('j.chb.2026.109142'))
as_of = date(2026, 11, 27)
assert paper['year'] == 2027
assert validator.valid_publication_year(paper, as_of)
assert validator.valid_publication_year(paper, date(2027, 1, 1))
for changes in (
    {'publication_status': ''},
    {'verification_url': 'https://example.com/unverified'},
    {'verified_date': '2027-01-01'},
    {'print_issue_date': '2028-01'},
    {'year': 2028, 'print_issue_date': '2028-01'},
    {'year': '2027'},
):
    unsupported = deepcopy(paper)
    unsupported.update(changes)
    assert not validator.valid_publication_year(unsupported, as_of), changes
print('PASS: verified forthcoming print issue accepted; unsupported future citations rejected')
