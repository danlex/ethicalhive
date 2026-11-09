"""Read the explicitly pinned research runs; never infer a condition from a glob."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import metrics

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'experiments/research-runs-2026-11-09.json'
SUITES = ('anchoring', 'capitulation', 'scope-creep', 'selective-evidence',
          'source-fabrication', 'sycophancy')


class ResearchDataError(ValueError):
    """A selected research record does not match its declared provenance."""


def validate_rows(rows, reviewer, *, expected_count=None, expected_case_ids=None):
    if not rows:
        raise ResearchDataError('Empty result file')
    ids = []
    for row in rows:
        if row.get('reviewer') != reviewer:
            raise ResearchDataError(f'Expected reviewer {reviewer!r}, got {row.get("reviewer")!r}')
        if row.get('expected') not in metrics.VALID or row.get('got') not in metrics.VALID:
            raise ResearchDataError('Invalid gold or predicted verdict in selected result file')
        if not isinstance(row.get('case_id'), str) or not row['case_id']:
            raise ResearchDataError('Missing case identifier')
        ids.append(row['case_id'])
    if len(set(ids)) != len(ids):
        raise ResearchDataError('Duplicate case identifier in selected result file')
    if expected_count is not None and len(rows) != expected_count:
        raise ResearchDataError(f'Expected {expected_count} rows, got {len(rows)}')
    if expected_case_ids is not None and ids != expected_case_ids:
        raise ResearchDataError('Case identifiers or order differ from the run manifest')
    return rows


def read_manifest(path=DEFAULT_MANIFEST):
    path = Path(path)
    data = json.loads(path.read_text())
    if data.get('schema_version') != 1 or not isinstance(data.get('runs'), list):
        raise ResearchDataError('Unsupported research run manifest')
    keys = [(r['suite'], r['mode'], r['reviewer']) for r in data['runs']]
    if len(set(keys)) != len(keys):
        raise ResearchDataError('Duplicate suite/mode/reviewer key in manifest')
    return data


def run_record(mode, reviewer, suite='hard', *, manifest=DEFAULT_MANIFEST):
    data = read_manifest(manifest) if not isinstance(manifest, dict) else manifest
    found = [r for r in data['runs']
             if (r['suite'], r['mode'], r['reviewer']) == (suite, mode, reviewer)]
    if not found:
        raise ResearchDataError(f'No unique pinned run for {suite}/{mode}/{reviewer}')
    if len(found)>1:
        raise ResearchDataError(f'Duplicate pinned runs for {suite}/{mode}/{reviewer}')
    return found[0]


def load_run(mode, reviewer, suite='hard', *, manifest=DEFAULT_MANIFEST, root=ROOT):
    record = run_record(mode, reviewer, suite, manifest=manifest)
    relative = Path(record['path'])
    if relative.is_absolute() or '..' in relative.parts or relative.parts[:2] != ('experiments', 'results'):
        raise ResearchDataError('Result path must be inside experiments/results')
    path = Path(root) / relative
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != record['sha256']:
        raise ResearchDataError(f'Hash mismatch for {record["path"]}')
    rows = metrics.load([str(path)])
    validate_rows(rows, reviewer, expected_count=record['n'], expected_case_ids=record['case_ids'])
    return record, rows


def result_path(stem, reviewer, *, manifest=DEFAULT_MANIFEST):
    """Compatibility helper for old generators, now selecting a pinned record."""
    suite = 'hard' if stem.endswith('-hard') else 'easy'
    mode = stem.removesuffix('-hard') if suite == 'hard' else stem
    try:
        record, _ = load_run(mode, reviewer, suite, manifest=manifest)
    except ResearchDataError as error:
        if str(error).startswith('No unique pinned run'):
            return None
        raise
    return ROOT / record['path']


def load_condition(reviewer, suite='hard', *, modes=SUITES, manifest=DEFAULT_MANIFEST):
    rows, records = [], []
    for mode in modes:
        record, selected = load_run(mode, reviewer, suite, manifest=manifest)
        rows.extend(selected)
        records.append(record)
    if len({r['case_id'] for r in rows}) != len(rows):
        raise ResearchDataError('Duplicate case identifier across pooled suites')
    return records, rows
