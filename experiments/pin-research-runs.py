#!/usr/bin/env python3
"""Freeze the reviewed result selection without changing any model output."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

import metrics
from research_runs import ROOT, SUITES, DEFAULT_MANIFEST, validate_rows, ResearchDataError

CORE = ('none', 'freeform', 'checklist', 'mono-rid', 'judge-ctx', 'judge', 'judge-anon')
EASY = ('none', 'freeform', 'contract', 'judge', 'mono-rid')
REVIEW = ROOT / 'paper/reviews/athena-research-review-2026-11-09-evidence.json'


def file_record(path, mode, reviewer, suite):
    rows = metrics.load([str(path)])
    validate_rows(rows, reviewer)
    expected_prefix = f'run-suite-{mode}{"-hard" if suite == "hard" else ""}-{reviewer}-'
    timestamp = path.name.removeprefix(expected_prefix).removesuffix('.jsonl')
    if not path.name.startswith(expected_prefix) or not re.fullmatch(r'\d{8}-\d{6}', timestamp):
        raise ResearchDataError(f'Not an exact reviewer filename: {path.name}')
    return dict(suite=suite, mode=mode, reviewer=reviewer, path=str(path.relative_to(ROOT)),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(), n=len(rows),
                case_ids=[r['case_id'] for r in rows], filename_timestamp=timestamp,
                model_aliases=sorted({r.get('model', 'not-recorded') for r in rows}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--replace',action='store_true',
                        help='Explicitly replace a previously pinned selection; normally use a new --output path')
    args = parser.parse_args()
    if args.output.exists() and not args.replace:
        parser.error('The manifest already exists. Use a new --output path or explicitly request --replace.')
    evidence = json.loads(REVIEW.read_text())
    runs, excluded, unavailable = [], [], []
    for suite, conditions in [('hard', (*CORE, 'contract')), ('easy', EASY)]:
        for reviewer in conditions:
            for mode in SUITES:
                if suite == 'hard' and reviewer in CORE:
                    paths = [ROOT / f['path'] for f in evidence['conditions'][reviewer]['files']
                             if Path(f['path']).name.startswith(f'run-suite-{mode}-hard-{reviewer}-')]
                    if len(paths) != 1:
                        raise ResearchDataError(f'No unique reviewed seed for {mode}/{reviewer}')
                    record = file_record(paths[0], mode, reviewer, suite)
                    expected_hash = next(f['sha256'] for f in evidence['conditions'][reviewer]['files']
                                         if f['path'] == record['path'])
                    if record['sha256'] != expected_hash:
                        raise ResearchDataError('The reviewed seed changed')
                    record['selection_basis'] = 'Exact file and hash from the prior research review'
                    runs.append(record)
                    continue
                stem = f'run-suite-{mode}{"-hard" if suite == "hard" else ""}-{reviewer}-'
                candidates = sorted(p for p in (ROOT/'experiments/results').glob(stem+'*.jsonl')
                                    if re.fullmatch(re.escape(stem)+r'\d{8}-\d{6}\.jsonl', p.name))
                selected = None
                for candidate in reversed(candidates):
                    try:
                        selected = file_record(candidate, mode, reviewer, suite)
                    except (ResearchDataError, json.JSONDecodeError) as error:
                        excluded.append({'path': str(candidate.relative_to(ROOT)), 'reason': str(error)})
                    else:
                        selected['selection_basis'] = 'Newest complete exact-condition historical file at this freeze; any newer invalid candidates considered before this selection are disclosed separately'
                        runs.append(selected)
                        break
                if selected is None:
                    unavailable.append(dict(suite=suite, mode=mode, reviewer=reviewer))
    manifest = dict(schema_version=1, date='2026-11-09',
        source_commit=evidence['reviewed_commit'],
        selection_note='Frozen retrospective selection, not a preregistered experiment. No model outputs or author labels were changed. New result files do not change this manifest.',
        timestamp_note='Filename timestamps are recorded labels, not independently authenticated execution times.',
        configuration={'recorded_model_field':'model alias in each result row',
                       'backend_model_version':None,'temperature':None,'random_seed':None,
                       'cli_version':None,'token_usage':None,'wall_clock':None,
                       'note':'The historical result records do not establish these settings; no value is inferred from a model alias.'},
        exclusions_scope='Only invalid newer candidates examined before selecting a supplemental run; not an inventory of all historical failures or retries.',
        runs=runs, excluded_incomplete_files=excluded, unavailable=unavailable)
    args.output.write_text(json.dumps(manifest, indent=2)+'\n')
    print(f'Pinned {len(runs)} runs; {len(excluded)} incomplete candidates disclosed; {len(unavailable)} combinations unavailable.')


if __name__ == '__main__':
    main()
