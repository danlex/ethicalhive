#!/usr/bin/env python3
"""Extract the supplied HTML's literal JSON data without executing its JavaScript."""
import argparse
import hashlib
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('html', type=Path)
args = parser.parse_args()
raw = args.html.read_bytes()
text = raw.decode('utf-8')
data, _ = json.JSONDecoder().raw_decode(text.split('const DATA = ', 1)[1])
legend = text.split('const SRCS = {',1)[1].split('\n};',1)[0]
source_field_notes = {m.group(1):json.loads(m.group(2)) for m in re.finditer(r'^\s*([A-P]):("(?:[^"\\]|\\.)*")', legend, re.MULTILINE)}
assert len(source_field_notes) == 16
assert len(data['rows']) == 145
assert [r['n'] for r in data['rows']] == list(range(1, 146))
payload = dict(original_filename='Candidate Behaviours.html', received_on='2026-11-06',
               original_sha256=hashlib.sha256(raw).hexdigest(),
               extraction='Literal JSON decoded; source scripts were not executed.',
               original_disclosure='Rows 1–100: general knowledge, no source checked. Rows 101–145: web search reported by the supplied document, mainly secondary sources. No original book was read by its authoring process.',
               unverified_input_claims=['41 clearly new', '104 close to an existing mode', '45 checked through search', '399 ontology mode names and synonyms checked'],
               note='Those are claims made by the attachment, not independently established facts. Raw rows are preserved; the integrated page applies explicit reconciliation and review records.',
               source_field_notes=source_field_notes, **data)
out = Path(__file__).resolve().parents[1]/'references/candidate-behaviours-upload-2026-11-06.json'
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
print(f'Extracted {len(data["rows"])} rows; original SHA-256 {payload["original_sha256"]}')
