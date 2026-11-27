#!/usr/bin/env python3
"""Verify access blocks cannot masquerade as completed readings or hide unfinished files."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('corpus',Path(__file__).with_name('pdf-corpus-review.py'))
corpus=importlib.util.module_from_spec(spec);spec.loader.exec_module(corpus)

class AccessBlockTests(unittest.TestCase):
    def setUp(self):
        self.entry={'sequence':2,'file_name':'example.pdf','source_id':'S2','status':'access-blocked','access_record':'access.json'}
        self.note={'sequence':2,'source':{'file_name':'example.pdf','source_id':'S2'},'status':'access-blocked',
          'download_received':False,'content_read':False,'counts_as_full_review':False,
          'counts_as_independent_source':False,'attempted_on':'2026-11-27',
          'attempt':{'tool':'google_drive_fetch','http_status':403,'provider_reason':'cannotDownloadAbusiveFile','message':'Provider refused download'}}

    def test_block_is_unfinished_and_next_pending_remains_visible(self):
        files=[{'sequence':1,'status':'reviewed'},self.entry,{'sequence':3,'status':'pending'}]
        result=corpus.summarize_files(files)
        self.assertEqual((result['processed_files'],result['full_text_reviews'],result['remaining']),(1,1,2))
        self.assertEqual((result['attempted_files'],result['access_blocked_files'],result['pending_files']),(2,1,1))
        self.assertEqual(result['next']['sequence'],3)

    def test_false_reading_and_unavailable_checksum_are_rejected(self):
        for field in ['download_received','content_read','counts_as_full_review','counts_as_independent_source']:
            with self.subTest(field=field):
                note=copy.deepcopy(self.note);note[field]=True
                with self.assertRaises(AssertionError):corpus.check_access_record(note,self.entry)
        note=copy.deepcopy(self.note);note['source']['sha256']='invented'
        with self.assertRaises(AssertionError):corpus.check_access_record(note,self.entry)

    def test_real_findings_require_a_review(self):
        note=copy.deepcopy(self.note);note['findings']=[{'term':'Invented'}]
        with self.assertRaises(AssertionError):corpus.check_access_record(note,self.entry)

    def test_unknown_status_cannot_hide_a_file(self):
        with self.assertRaises(AssertionError):corpus.summarize_files([{'status':'silently-skipped'}])

    def test_pending_and_unrecorded_block_prevent_advancing(self):
        with self.assertRaises(AssertionError):corpus.ensure_queue_order({'files':[{'sequence':1,'status':'pending'}]},3)
        original=corpus.ROOT
        try:
            with tempfile.TemporaryDirectory() as directory:
                corpus.ROOT=Path(directory)
                with self.assertRaises(FileNotFoundError):corpus.ensure_queue_order({'files':[self.entry]},3)
                (corpus.ROOT/'access.json').write_text(json.dumps(self.note))
                corpus.ensure_queue_order({'files':[self.entry]},3)
                note=copy.deepcopy(self.note);note['content_read']=True
                (corpus.ROOT/'access.json').write_text(json.dumps(note))
                with self.assertRaises(AssertionError):corpus.ensure_queue_order({'files':[self.entry]},3)
        finally:corpus.ROOT=original

if __name__=='__main__':unittest.main()
