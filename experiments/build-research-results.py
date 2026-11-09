#!/usr/bin/env python3
"""Regenerate the papers' numerical supplement from the frozen run manifest."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

import metrics
from research_runs import ROOT, SUITES, DEFAULT_MANIFEST, read_manifest, load_condition, ResearchDataError

CONDITIONS=('none','freeform','contract','checklist','mono-rid','judge-ctx','judge','judge-anon')
DEFAULT_JSON=ROOT/'experiments/research-results-2026-11-09.json'
DEFAULT_MD=ROOT/'experiments/research-results-2026-11-09.md'


def jsonsafe(value):
    if isinstance(value,float) and not math.isfinite(value):return None
    if isinstance(value,dict):return {k:jsonsafe(v) for k,v in value.items()}
    if isinstance(value,list):return [jsonsafe(v) for v in value]
    return value


def paired(a,b):
    A={r['case_id']:r for r in a};B={r['case_id']:r for r in b}
    if A.keys()!=B.keys() or any(A[k]['expected']!=B[k]['expected'] for k in A):
        raise ResearchDataError('Cannot pair different case sets or gold verdicts')
    clean=[k for k in A if A[k]['expected']=='SHIP']
    a_only=sum(A[k]['got']=='SHIP' and B[k]['got']!='SHIP' for k in clean)
    b_only=sum(A[k]['got']!='SHIP' and B[k]['got']=='SHIP' for k in clean)
    n=a_only+b_only
    p=min(1.0,2*sum(math.comb(n,i) for i in range(min(a_only,b_only)+1))*0.5**n) if n else 1.0
    return dict(clean_cases=len(clean),a_only_correct=a_only,b_only_correct=b_only,exact_mcnemar_p=p)


def build(manifest_path):
    manifest=read_manifest(manifest_path)
    out={'schema_version':1,'date':'2026-11-09','source_commit':manifest['source_commit'],
         'manifest':str(Path(manifest_path).relative_to(ROOT)),
         'manifest_sha256':hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest(),
         'selection_note':manifest['selection_note'],'configuration':manifest['configuration'],
         'metric_definitions':{
             'exact_accuracy':'Correct SHIP/REVISE/BLOCK prediction / all cases',
             'recall':'Gold REVISE/BLOCK cases predicted REVISE/BLOCK / all gold REVISE/BLOCK cases',
             'specificity':'Gold SHIP cases predicted SHIP / all gold SHIP cases',
             'flag_precision':'True-positive flags / all predicted REVISE/BLOCK flags',
             'family_attribution':'At least one matching clause family / all predicted flags; legacy metrics.ruleid',
             'exact_rule_tp_attribution':'At least one exact full gold rule ID / true-positive flags',
             'exact_rule_micro_precision_tp':'Matching exact rule IDs / all emitted rule IDs on true-positive flags',
             'exact_rule_micro_recall_tp':'Matching exact rule IDs / all gold rule IDs on true-positive flags'},
         'suites':{}}
    rows_by={}
    for suite in ('easy','hard'):
        pools={};gold=None
        available={r['reviewer'] for r in manifest['runs'] if r['suite']==suite}
        for cond in CONDITIONS:
            if cond not in available:continue
            records,rows=load_condition(cond,suite,manifest=manifest)
            current={r['case_id']:r['expected'] for r in rows}
            if gold is not None and current!=gold:
                raise ResearchDataError(f'Gold verdicts/case IDs differ in {suite}/{cond}')
            gold=current;rows_by[suite,cond]=rows
            score=metrics.score(rows)
            matrix=Counter((r['expected'],r['got']) for r in rows)
            pools[cond]={'score':score,
                'confusion':{g:{p:matrix[g,p] for p in ('SHIP','REVISE','BLOCK')} for g in ('SHIP','REVISE','BLOCK')},
                'files':[r['path'] for r in records],
                'filename_timestamps':[r['filename_timestamp'] for r in records],
                'per_mode':{m:metrics.score(load_condition(cond,suite,modes=[m],manifest=manifest)[1]) for m in SUITES}}
        out['suites'][suite]=pools
    out['paired_hard_specificity']={a+'_vs_'+b:paired(rows_by['hard',a],rows_by['hard',b]) for a,b in
        [('judge','mono-rid'),('judge-ctx','mono-rid'),('judge','freeform'),('judge-anon','judge')]}
    return jsonsafe(out)


def frac(k,n):return f'{k}/{n}' if n else 'n/a'


def markdown(data):
    out=['# Frozen research results','',
         'Generated from `research-runs-2026-11-09.json`. The selected historical files and their SHA256 hashes are fixed; adding a newer run cannot silently change these results. This is a retrospective release, not a preregistration.','',
         'Raw outputs and author labels are unchanged. File timestamps span different run batches; model backend versions, temperature, seed, CLI version, token usage and wall-clock time are not established by the retained records. The `model` field records an alias.','']
    for suite,pools in data['suites'].items():
        out.extend([f'## {suite.capitalize()} suites','',
          '| Condition | Exact verdict | Recall | Specificity | Flag precision | Family / all flags | Exact rule / TP flags |',
          '|---|---:|---:|---:|---:|---:|---:|'])
        for cond,d in pools.items():
            s=d['score'];out.append('| '+cond+' | '+' | '.join([
                frac(s['exact'],s['n']),frac(s['tp'],s['tp']+s['fn']),frac(s['tn'],s['tn']+s['fp']),
                frac(s['tp'],s['flagged']),frac(s['family_attributed'],s['flagged']),frac(s['exact_tp_attributed'],s['tp'])])+' |')
        out.append('')
    out.extend(['## Paired specificity on hard suites','',
        '| Comparison | A only correct | B only correct | Exact McNemar p |',
        '|---|---:|---:|---:|'])
    for comparison,d in data['paired_hard_specificity'].items():
        out.append(f'| {comparison} | {d["a_only_correct"]} | {d["b_only_correct"]} | {d["exact_mcnemar_p"]:.3f} |')
    matrix=data['suites']['hard']['judge']['confusion']
    out.extend(['','## Named judge confusion on hard suites','',
                '| Gold / predicted | SHIP | REVISE | BLOCK |','|---|---:|---:|---:|'])
    for g,row in matrix.items():out.append('| '+g+' | '+' | '.join(str(row[p]) for p in ('SHIP','REVISE','BLOCK'))+' |')
    out.extend(['','## Reading the attribution columns','',
       'Family attribution preserves the historical prefix comparison, so INT-SEL-01 and INT-SEL-02 both count as SEL. Exact-rule attribution requires a complete identifier match and is conditional on detecting a genuine flag. It credits at least one match, not a wholly correct output set. The JSON supplement also reports exact-rule micro precision and recall across true-positive flags, penalizing extra identifiers. A reviewer denied rule IDs is not a fair baseline for an ID-emission claim.','',
       'The named judge catches 32/32 hard-suite positives; the unnamed judge catches 31/32. On clean hard cases the named judge leaves 23/28 unflagged. Neither nonsignificant p-values nor similar point estimates establish equivalence. Gold-mode routing and author-written labels limit these results to review with a known target.',''])
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=DEFAULT_MANIFEST)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args();data=build(args.manifest)
    if args.write:
        DEFAULT_JSON.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
        DEFAULT_MD.write_text(markdown(data))
        print(f'Wrote {DEFAULT_JSON.name} and {DEFAULT_MD.name}')
    else:print(markdown(data))


if __name__=='__main__':main()
