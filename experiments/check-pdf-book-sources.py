#!/usr/bin/env python3
"""A consulted chapter stays citable without becoming a journal article or filling a paper quota."""
import copy
import importlib.util
from pathlib import Path

from catalogue_sources import available_papers, research_papers, source_coverage

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pdf_review',root/'experiments/pdf-corpus-review.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review={'sequence':1,'source':{'pdf_pages':1,'verification_url':'https://example.org/chapter'},
    'reading':{'source_scope_note':'Synthetic one-page source fixture;no real reading claim.'},
    'citation':{'title':'Source-classification fixture','authors':['Fixture Author'],'year':2024,
        'url':'https://example.org/chapter','venue':'Edited book,chapter1',
        'publication_type':'book-chapter','domain':'human-related'}}
finding={'term':'Source fixture','id':'source-fixture','definition':'A test-only source classification.',
    'category':'Attention','evidence':[{'pdf_page':1,'printed_page':'1','quote':'fixture'}],
    'evidence_scope':'A source-format regression fixture,not research evidence.',
    'boundary':'Fixture only.','ai_proposal':'Fixture only.',
    'terminology_sources':[{'title':'Partially consulted terminology fixture',
        'url':'https://example.org/terminology','consulted':'One definition passage only;not a full paper review.'}]}
template={'modes':[{'category':'Attention','family':'attention','group_label':'Attention'}]}
mode=module.new_mode(review,finding,template)
assert mode['definition_sources'][0]['publication']['type']=='book-chapter'
assert mode['definition_sources'][0]['count_as_behaviour_paper'] is False
assert mode['selected_papers']==[]
assert mode['terminology_sources']==finding['terminology_sources']
assert not research_papers(mode)
assert not available_papers(mode)
coverage=source_coverage(mode)
assert coverage['reference_source_links']==1
assert coverage['selected_paper_count']==0
assert coverage['selected_paper_shortfall']==3
assert coverage['coverage_status']=='reference-sources-only'
article=copy.deepcopy(review)
article['citation']['publication_type']='journal-article'
article_mode=module.new_mode(article,finding,template)
assert article_mode['definition_sources'][0]['publication']['type']=='journal-article'
assert len(article_mode['selected_papers'])==1
assert len(research_papers(article_mode))==1
assert source_coverage(article_mode)['human_related_paper_links']==1
render_spec=importlib.util.spec_from_file_location('build_catalogue',root/'experiments/build-catalogue.py')
renderer=importlib.util.module_from_spec(render_spec)
render_spec.loader.exec_module(renderer)
body=renderer.research_block(mode)
assert body.count('https://example.org/chapter')==1
assert 'Book and reference sources' in body
assert 'Source check pending' not in body
enriched={'research_notes':[{'name':'Fixture','definition':'Fixture definition',
    'catalogue_boundary':'Fixture boundary','review_record':'references/pdf-reviews/0001.json',
    'definition_sources':mode['definition_sources']}]}
note_body=renderer.research_block(enriched)
assert note_body.count('https://example.org/chapter')==1
assert 'Source check pending' not in note_body
pending=copy.deepcopy(mode)
pending['definition_sources']=[]
pending['source_check']='pending-definition-source-check'
assert 'Source check pending' in renderer.research_block(pending)
print('PASS: chapter and targeted terminology sources remain citable references;journal evidence remains selectable')
