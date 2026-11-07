#!/usr/bin/env python3
"""Check correction traceability and prevent historical searches becoming fresh proof."""
import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / 'experiments'
record = json.loads((ROOT / 'references/source-corrections-review-2026-11-07.json').read_text())
corrections = {r['bundle_candidate_id']: r for r in record['records']}
assert len(corrections) == 18
assert sum(r['change_type'] == 'source' for r in corrections.values()) == 15
assert sum(r['change_type'] == 'definition' for r in corrections.values()) == 3
onto = yaml.safe_load((ROOT / 'ontology/ethical-ai.yaml').read_text())
modes = {m['num']: m for m in onto['modes']}
assert len(modes) == 434 and len({m['category'] for m in modes.values()}) == 11
md_path = EXP / 'candidate-behaviours-2026-11-06.md'
rows = {int(m[1]): [c.strip().replace('*', '') for c in m[2].split('|')]
        for m in re.finditer(r'^\| (\d+) \|(.*?)\|\s*$', md_path.read_text(), re.M)}
assert len(rows) == 541
def tsv(path):
    records = list(csv.reader(path.open(), delimiter='\t'))
    assert len(records) == 541 and all(len(r) == 8 for r in records)
    return {int(r[0]): r for r in records}
review = tsv(EXP / 'candidate-review-2026-11-06.tsv')
search = tsv(EXP / 'candidate-original-check-2026-11-07.tsv')
for n, r in corrections.items():
    assert rows[n][0] == r['name']
    assert rows[n][1] == r['current_source']
    assert rows[n][2] == r['current_definition']
    assert review[n][3] == 'OK'  # Current source verdict, not an unapplied WRONG correction.
    assert '2026-11-07' in review[n][7]
    assert search[n][:7] == r['previous_text_search_row'][:7]
    assert 'Historical' in search[n][7]
    assert r['ai_evidence_status'] == 'Proposed analogy; not tested in this research'
    assert r['bibliographic_review']['evidence_urls']
    ref = r['catalogue_reference_id']
    if ref:
        m = modes[ref]
        assert m['name'] == r['name'] and m['research_candidate']
        assert m['ai_evidence_status'] == r['ai_evidence_status']
        assert m['research_provenance']['contributions'][0]['supplied_source']
        if r['change_type'] == 'definition':
            assert m['definition'] == r['current_definition']
        elif n != 20:  # The current catalogue already has a separately reviewed definition.
            assert m['definition'] == rows[n][2]
for n in (323, 351, 354):
    assert modes[n]['source_check'] == 'definition-source-consulted'
for n in (330, 392):
    assert modes[n]['definition_sources']
    assert modes[n]['source_check'] == 'pending-definition-source-check'
assert '2013' in modes[322]['research_boundary'] and 'unchecked' in modes[322]['research_boundary']

def html_data(path):
    text = path.read_text()
    assert text.startswith('<!doctype html>')
    assert '<meta charset="utf-8">' in text and 'width=device-width' in text
    data = json.loads(re.search(r'const DATA = (.*?);\nconst SRCS', text, re.S)[1])
    expected = {
        'historical reported term hits': sum(r['oc'] == 'FOUND' for r in data['rows']),
        'flagged in review': sum(bool(r['rv']) and r['rv'] != 'No unresolved flags in the supplied review scope' for r in data['rows']),
    }
    for label, count in expected.items():
        assert re.search(r'class="v(?: acc)?">' + str(count) + r'</div><div class="k">' + label, text)
    for row in data['rows']:
        assert row['src'] == rows[row['n']][1] and row['human'] == rows[row['n']][2]
        if row['n'] in corrections:
            assert row['cr']['definition_review'] == corrections[row['n']]['definition_review']
    return data

all_data = html_data(EXP / 'candidate-behaviours-2026-11-06.html')
shortlist = html_data(EXP / 'candidate-behaviours-new-2026-11-06.html')
assert len(all_data['rows']) == 541
assert [r for r in all_data['rows'] if not r['near']] == shortlist['rows']
book_path = EXP / 'candidate-behaviours-2026-11-06.xlsx'
wb = load_workbook(book_path, read_only=True)
ws = wb['Behaviours']
assert ws.max_row == 542 and ws.max_column == 26
for values in ws.iter_rows(min_row=2, values_only=True):
    n = values[0]
    assert values[3] == rows[n][1] and values[4] == rows[n][2]
    if n in corrections:
        assert values[22] == corrections[n]['bibliographic_review']['status']
        assert values[23] == corrections[n]['definition_review']['status']
wb.close()
# A regeneration must not discard the reviewer's decisions or free-form notes.
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / 'review.xlsx'
    wb = load_workbook(book_path)
    ws = wb['Behaviours']
    ws['J2'], ws['K2'], ws['L2'] = 'Source checked', 'Synonym', 'Keep this manual note.'
    wb.save(out)
    wb.close()
    subprocess.run([sys.executable, str(EXP / 'candidate-behaviours-to-xlsx.py'), str(md_path), str(out)], check=True)
    wb = load_workbook(out, read_only=True)
    values = next(wb['Behaviours'].iter_rows(min_row=2, max_row=2, values_only=True))
    assert values[9:12] == ('Source checked', 'Synonym', 'Keep this manual note.')
    wb.close()
# Re-applying the refreshed source review must leave the corrected markdown intact.
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / 'candidates.md'
    out.write_bytes(md_path.read_bytes())
    subprocess.run([sys.executable, str(EXP / 'apply-candidate-review.py'), str(out), str(EXP / 'candidate-review-2026-11-06.tsv')], check=True)
    assert out.read_bytes() == md_path.read_bytes()
print('PASS: 18 corrections traced through source/review/HTML/XLSX; historical searches preserved; catalogue remains 434; manual decisions survive regeneration.')
