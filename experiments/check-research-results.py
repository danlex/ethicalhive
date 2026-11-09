#!/usr/bin/env python3
"""Regression checks for pinned runs and exact numbered-rule attribution."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import metrics
from research_runs import ROOT, DEFAULT_MANIFEST, load_run, load_condition, read_manifest, ResearchDataError


class PinnedRunTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.directory=self.root/'experiments/results';self.directory.mkdir(parents=True)
        self.row=dict(case_id='case-1',reviewer='judge',expected='BLOCK',got='BLOCK',
                      gold_clauses=['INT-SEL-01'],rule_ids=['INT-SEL-01'])
        self.path=self.directory/'run-suite-anchoring-hard-judge-20260101-000000.jsonl'
        self.path.write_text(json.dumps(self.row)+'\n')
        self.record=dict(suite='hard',mode='anchoring',reviewer='judge',
                         path=str(self.path.relative_to(self.root)),
                         sha256=hashlib.sha256(self.path.read_bytes()).hexdigest(),n=1,case_ids=['case-1'])
        self.manifest={'schema_version':1,'runs':[self.record]}

    def tearDown(self):self.temp.cleanup()

    def load(self):return load_run('anchoring','judge',manifest=self.manifest,root=self.root)

    def update_file(self,rows):
        self.path.write_text('\n'.join(json.dumps(r) for r in rows)+'\n')
        self.record['sha256']=hashlib.sha256(self.path.read_bytes()).hexdigest()

    def test_shadowed_condition_names_and_new_runs_do_not_change_selection(self):
        for condition in ('judge-ctx','judge-anon','judge'):
            p=self.directory/f'run-suite-anchoring-hard-{condition}-20291231-235959.jsonl'
            p.write_text(json.dumps({**self.row,'reviewer':condition,'got':'SHIP'})+'\n')
        record,rows=self.load()
        self.assertEqual(record['path'],str(self.path.relative_to(self.root)))
        self.assertEqual(rows[0]['got'],'BLOCK')

    def test_hash_tampering_fails(self):
        self.path.write_text(json.dumps({**self.row,'got':'SHIP'})+'\n')
        with self.assertRaisesRegex(ResearchDataError,'Hash mismatch'):self.load()

    def test_wrong_reviewer_fails_even_with_matching_hash(self):
        self.update_file([{**self.row,'reviewer':'judge-ctx'}])
        with self.assertRaisesRegex(ResearchDataError,'Expected reviewer'):self.load()

    def test_duplicate_cases_fail(self):
        self.update_file([self.row,self.row]);self.record['n']=2;self.record['case_ids']=['case-1','case-1']
        with self.assertRaisesRegex(ResearchDataError,'Duplicate case'):self.load()

    def test_missing_rows_fail(self):
        self.record['n']=2
        with self.assertRaisesRegex(ResearchDataError,'Expected 2 rows'):self.load()

    def test_changed_case_identity_fails(self):
        self.update_file([{**self.row,'case_id':'different-case'}])
        with self.assertRaisesRegex(ResearchDataError,'Case identifiers'):self.load()

    def test_invalid_prediction_is_not_silently_removed(self):
        self.update_file([{**self.row,'got':'PARSE_ERROR'}])
        with self.assertRaisesRegex(ResearchDataError,'Invalid gold or predicted'):self.load()

    def test_result_path_cannot_escape_repository(self):
        self.record['path']='../outside.jsonl'
        with self.assertRaisesRegex(ResearchDataError,'inside experiments/results'):self.load()

    def test_duplicate_manifest_key_fails(self):
        path=self.root/'manifest.json'
        path.write_text(json.dumps({'schema_version':1,'runs':[self.record,self.record]}))
        with self.assertRaisesRegex(ResearchDataError,'Duplicate suite'):read_manifest(path)


class AttributionTests(unittest.TestCase):
    def test_matching_family_does_not_credit_wrong_exact_rule(self):
        s=metrics.score([dict(expected='BLOCK',got='BLOCK',gold_clauses=['INT-SEL-01'],rule_ids=['INT-SEL-02'])])
        self.assertEqual(s['ruleid'],1)
        self.assertEqual(s['family_tp_attributed'],1)
        self.assertEqual(s['exact_tp_attributed'],0)
        self.assertEqual(s['exact_rule_tp_attribution'],0)

    def test_false_positive_flag_stays_separate_from_attribution_on_true_positives(self):
        s=metrics.score([
            dict(expected='BLOCK',got='BLOCK',gold_clauses=['INT-SEL-01'],rule_ids=['INT-SEL-01']),
            dict(expected='SHIP',got='REVISE',gold_clauses=[],rule_ids=['INT-SEL-01'])])
        self.assertEqual(s['exact_rule_tp_attribution'],1)
        self.assertEqual(s['exact_rule_attribution'],.5)
        self.assertEqual(s['precision'],.5)

    def test_extra_rule_ids_reduce_set_precision(self):
        s=metrics.score([dict(expected='BLOCK',got='BLOCK',gold_clauses=['INT-SEL-01'],rule_ids=['INT-SEL-01','INT-ANC-01'])])
        self.assertEqual(s['exact_rule_tp_attribution'],1)
        self.assertEqual(s['exact_rule_micro_precision_tp'],.5)
        self.assertEqual(s['exact_rule_micro_recall_tp'],1)


class ReleasedSnapshotTests(unittest.TestCase):
    def test_all_manifest_files_validate(self):
        manifest=read_manifest()
        self.assertEqual(len(manifest['runs']),78)
        for r in manifest['runs']:
            with self.subTest(suite=r['suite'],mode=r['mode'],reviewer=r['reviewer']):
                record,rows=load_run(r['mode'],r['reviewer'],r['suite'],manifest=manifest)
                self.assertEqual(len(rows),record['n'])

    def test_named_and_unnamed_results_remain_distinct(self):
        _,named=load_condition('judge');_,anon=load_condition('judge-anon')
        ns,ans=metrics.score(named),metrics.score(anon)
        self.assertEqual((ns['exact'],ns['tn'],ns['tp'],ns['fn']),(47,23,32,0))
        self.assertEqual((ans['exact'],ans['tn'],ans['tp'],ans['fn']),(48,24,31,1))
        self.assertEqual(sum(r['expected']=='REVISE' and r['got']=='BLOCK' for r in named),7)

    def test_family_and_exact_rule_counts_are_separate(self):
        _,rows=load_condition('mono-rid');s=metrics.score(rows)
        self.assertEqual((s['family_tp_attributed'],s['exact_tp_attributed'],s['tp']),(31,28,32))

    def test_generated_supplement_matches_manifest_and_raw_records(self):
        spec=importlib.util.spec_from_file_location('build_research_results',ROOT/'experiments/build-research-results.py')
        builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
        current=builder.build(DEFAULT_MANIFEST)
        published=json.loads((ROOT/'experiments/research-results-2026-11-09.json').read_text())
        self.assertEqual(published,current)
        self.assertEqual((ROOT/'experiments/research-results-2026-11-09.md').read_text(),builder.markdown(current))


if __name__=='__main__':unittest.main(verbosity=2)
