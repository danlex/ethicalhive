#!/usr/bin/env python3
"""Support sequential, manually read PDF reviews; never infer findings from metadata."""
import argparse
import copy
from datetime import datetime, timezone
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urlencode

import yaml
from catalogue_sources import paper_identifier

ROOT=Path(__file__).resolve().parents[1]
ONTOLOGY=ROOT/'ontology/ethical-ai.yaml'
MANIFEST=ROOT/'references/pdf-corpus-2026-11-26.json'
REVIEWS=ROOT/'references/pdf-reviews'
TODAY=lambda:datetime.now(timezone.utc).date().isoformat()


def read_json(path):return json.loads(path.read_text())
def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized(text):
    text=re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',text)
    return ' '.join(text.split()).casefold()
def pdf_pages(path):
    text=subprocess.check_output(['pdftotext','-layout',str(path),'-'],text=True)
    pages=text.split('\f')
    if not pages[-1].strip():pages.pop()
    return ['\n'.join(line.strip() for line in page.splitlines()
            if not line.strip().startswith('Downloaded from www.annualreviews.org.')) for page in pages]
def corpus_entry(sequence):
    return next(f for f in read_json(MANIFEST)['files'] if f['sequence']==sequence)
def record_path(sequence):return REVIEWS/(f'{sequence:04d}.json')


def check_review(review,pdf,ontology):
    entry=corpus_entry(review['sequence'])
    assert review['source']['file_name']==entry['file_name']
    assert review['source']['sha256']==sha(pdf),'PDF checksum does not match the review'
    if review.get('duplicate_of'):
        earlier=read_json(record_path(review['duplicate_of']))
        assert earlier['sequence']<review['sequence']
        assert earlier['source']['sha256']==review['source']['sha256'],'Duplicate bytes must match'
        assert not review.get('findings'),'A duplicate does not supply independent findings'
        return
    pages=pdf_pages(pdf)
    assert review['source']['pdf_pages']==len(pages)
    assert review['reading']['pdf_pages_read']==list(range(1,len(pages)+1)), 'Disclose every page actually read'
    assert review['reading']['status']=='full-extracted-text-read'
    assert all(review['citation'].get(k) for k in ('title','authors','year','url','venue','publication_type'))
    ids={m['id'] for m in ontology['modes']}
    all_ids=ids|{f['id'] for f in review['findings'] if f['decision']=='new-entry'}
    aliases={normalized(n):m['id'] for m in ontology['modes'] for n in [m['name'],*m.get('synonyms',[])]}
    for finding in review['findings']:
        for relation in ('relates_to','is_a'):
            assert all(target in all_ids for target in finding.get(relation,[])), (finding['term'],relation,'Unknown ontology target')
        assert finding['decision'] in ('new-entry','enrich-existing','covered','defer')
        assert finding.get('definition') and finding.get('novelty_rationale')
        if finding['decision']=='new-entry':
            assert finding['id'] not in ids
            assert normalized(finding['term']) not in aliases, 'Existing name or alias cannot become a new mode'
            assert finding.get('ai_proposal') and finding.get('boundary') and finding.get('category')
            ids.add(finding['id']);aliases[normalized(finding['term'])]=finding['id']
        elif finding['decision'] in ('enrich-existing','covered'):
            assert finding['target_id'] in ids
            if finding.get('revised_definition'):
                current=next(m for m in ontology['modes'] if m['id']==finding['target_id'])
                assert current['definition']==finding['previous_definition'],'Definition changed since this review was authored'
                assert finding.get('definition_revision_reason')
        for evidence in finding.get('evidence',[]):
            assert 1<=evidence['pdf_page']<=len(pages)
            assert normalized(evidence['quote']) in normalized(pages[evidence['pdf_page']-1]),(
                finding['term'],evidence['pdf_page'],'Evidence quotation not found on its declared page')
        if finding['decision']!='defer':assert finding.get('evidence')


def citation(review,finding):
    c=copy.deepcopy(review['citation'])
    c.update(id=paper_identifier(c['url']),domain=c.get('domain','human-related'),
             relevance=finding['evidence_scope'],
             consulted=f"Full supplied PDF text read, all {review['source']['pdf_pages']} pages; evidence at PDF pages "+
                 ', '.join(str(e['pdf_page']) for e in finding['evidence'])+
                 ' (source locators: '+', '.join(str(e['printed_page']) for e in finding['evidence'])+')'+
                 '. '+review['reading']['source_scope_note'],
             verification_url=c['url'],verified_date=TODAY(),
             verification_method='Identity and '+('DOI' if 'doi.org/' in c['url'] else 'version identifier')+
                 ' read in the supplied PDF; evidence passages checked against that PDF',
             review_record=str(record_path(review['sequence']).relative_to(ROOT)))
    return c


def source_record(review,finding):
    c=citation(review,finding)
    doi=c['url'].split('doi.org/',1)[-1] if 'doi.org/' in c['url'] else None
    return {'id':f"pdf-review-{review['sequence']:04d}-{finding.get('id',finding.get('target_id'))}",
            'title':c['title'],'url':c['url'],'consulted':c['consulted'],
            'publication':{'type':('posted-content' if c['publication_type'] in ('preprint','posted-content') else
                'proceedings-article' if c['publication_type']=='proceedings-article' else 'journal-article'),
              'authors':c['authors'],'year':c['year'],'venue':c['venue'],
              **({'doi':doi} if doi else {}),'evidence_scope':c['relevance'],
              'verification_url':c['verification_url'],'verified_date':c['verified_date']}}


def new_mode(review,finding,ontology):
    template=next(m for m in ontology['modes'] if m['category']==finding['category'])
    query='all:"'+finding['term']+'"'
    filters='(cat:cs.AI OR cat:cs.CL OR cat:cs.LG)'
    return {'id':finding['id'],'num':len(ontology['modes'])+1,'name':finding['term'],
        'definition':finding['definition'],'category':finding['category'],
        'family':template['family'],'group_label':template['group_label'],
        'tag':'research' if finding.get('ai_native') else 'analogy',
        'origin':finding.get('origin','Human–AI interaction / moral psychology'),
        'human_parallel':'' if finding.get('ai_native') else finding['term'],
        'ai_native':bool(finding.get('ai_native')),'highlighted':False,
        'research_candidate':not finding.get('ai_native',False),'source_check':'definition-source-consulted',
        'ai_evidence_status':finding.get('ai_evidence_status','Human behaviour discussed in a read review; proposed AI analogue not tested here'),
        'proposed_ai_manifestation':finding['ai_proposal'],
        'research_boundary':finding['boundary'],'concept_boundary':finding['boundary'],
        'measurability':finding.get('measurability','multi-turn'),
        'violates':finding.get('violates',[]),'causes':finding.get('causes',[]),
        'synonyms':finding.get('synonyms',[]),'relates_to':finding.get('relates_to',[]),
        **({'is_a':finding['is_a']} if finding.get('is_a') else {}),
        'definition_sources':[source_record(review,finding)],'selected_papers':[citation(review,finding)],
        'literature_search':{'database':'arXiv','status':'not-searched','count':None,'query':query,
          'filters':filters,'url':'https://export.arxiv.org/api/query?'+urlencode({'search_query':query+' AND '+filters,'max_results':5}),
          'queried_at':None,'scope':'No search total measured for this new entry. Selected citations are independent of metadata-query totals.'},
        'research_provenance':{'method':'Sequential reading of a user-supplied PDF; novelty and boundaries reviewed against current ontology',
          'review_record':str(record_path(review['sequence']).relative_to(ROOT))}}


def fill_selected_from_read_reviews(mode):
    """Fill real bibliography gaps, retaining the three existing selections."""
    selected=mode.get('selected_papers')
    if selected is None or len(selected)>=3:return False
    before=len(selected)
    identities={paper_identifier(p['url']) for p in selected}
    titles={normalized(p['title']) for p in selected}
    for note in mode.get('research_notes',[]):
        path=note.get('review_record')
        if not path or not (ROOT/path).is_file():continue
        review=read_json(ROOT/path)
        if review.get('duplicate_of') or review.get('reading',{}).get('status')!='full-extracted-text-read':continue
        finding=next((f for f in review['findings'] if f.get('target_id')==mode['id']
                      and f['decision']=='enrich-existing'),None)
        if finding is None:continue
        paper=citation(review,finding)
        if paper['id'] in identities or normalized(paper['title']) in titles:continue
        selected.append(paper);identities.add(paper['id']);titles.add(normalized(paper['title']))
        if len(selected)>=3:break
    return len(selected)!=before


def save_ontology(original,ontology,changed,new_ids):
    # Preserve every unmodified record byte-for-byte instead of reformatting the catalogue.
    text=original
    for mid in changed:
        mode=next(m for m in ontology['modes'] if m['id']==mid)
        pattern=re.compile(r'^- id: '+re.escape(mid)+r'\n.*?(?=^- id: |\Z)',re.M|re.S)
        block=yaml.safe_dump([mode],sort_keys=False,allow_unicode=True,width=105)
        text,count=pattern.subn(lambda _:block,text,count=1)
        assert count==1,mid
    if new_ids:
        text=text.rstrip()+'\n'+yaml.safe_dump([m for m in ontology['modes'] if m['id'] in new_ids],
             sort_keys=False,allow_unicode=True,width=105)
    end=text.index('\nrelation_types:')
    text=yaml.safe_dump({'meta':ontology['meta']},sort_keys=False,allow_unicode=True,width=105).rstrip()+text[end:]
    ONTOLOGY.write_text(text)


def apply_review(path,pdf):
    review=read_json(path)
    destination=record_path(review['sequence'])
    assert not destination.exists(), 'This PDF already has a committed review; revise explicitly instead'
    original=ONTOLOGY.read_text();ontology=yaml.safe_load(original)
    manifest=read_json(MANIFEST)
    entry=next(f for f in manifest['files'] if f['sequence']==review['sequence'])
    assert all(f['status']!='pending' for f in manifest['files'] if f['sequence']<review['sequence']), 'Review the queue in order'
    check_review(review,pdf,ontology)
    changed=[];new=[]
    for finding in review.get('findings',[]):
        if finding['decision']=='new-entry':
            ontology['modes'].append(new_mode(review,finding,ontology));new.append(finding['id'])
        elif finding['decision']=='enrich-existing':
            mode=next(m for m in ontology['modes'] if m['id']==finding['target_id'])
            if finding.get('revised_definition'):
                mode['definition']=finding['revised_definition'];mode['concept_boundary']=finding['boundary']
                if finding.get('revised_measurability'):mode['measurability']=finding['revised_measurability']
            mode.setdefault('research_notes',[]).append({'id':f"pdf-review-{review['sequence']:04d}",
              'review_record':str(destination.relative_to(ROOT)),
              'name':finding['term'],'definition':finding['definition'],'evidence_scope':finding['evidence_scope'],
              'catalogue_boundary':finding['boundary'],'definition_sources':[source_record(review,finding)]})
            changed.append(mode['id'])
    if new or changed:
        ontology['meta'].update(updated=TODAY(),mode_count=len(ontology['modes']))
        ontology['meta']['display_counts']['numbered_entries']=len(ontology['modes'])
        ontology['meta']['pdf_corpus_review']={'manifest':str(MANIFEST.relative_to(ROOT)),
            'latest_review':str(destination.relative_to(ROOT)),'date':TODAY(),
            'scope':'Sequential PDF reading; human evidence, AI proposals and secondary citations remain distinguished'}
        save_ontology(original,ontology,list(dict.fromkeys(changed)),set(new))
    entry.update(status='duplicate-verified' if review.get('duplicate_of') else 'reviewed',
       sha256=review['source']['sha256'],review=str(destination.relative_to(ROOT)))
    review['reviewed_on']=TODAY();review['ontology_changes']={'added':new,'enriched':list(dict.fromkeys(changed))}
    if any(f.get('revised_definition') for f in review.get('findings',[])):
        review['ontology_changes']['revised_definitions']=[f['target_id'] for f in review['findings'] if f.get('revised_definition')]
    write_json(destination,review);write_json(MANIFEST,manifest)
    # The current review must exist before its citation is eligible for selection.
    sync_citations(changed)
    print(json.dumps({'review':str(destination.relative_to(ROOT)),'added':new,'enriched':changed}))


def sync_citations(only_ids=None):
    original=ONTOLOGY.read_text();ontology=yaml.safe_load(original)
    changed=[m['id'] for m in ontology['modes'] if (only_ids is None or m['id'] in only_ids)
             and fill_selected_from_read_reviews(m)]
    if changed:save_ontology(original,ontology,changed,set())
    print(json.dumps({'read_review_citations_filled':changed}))


def lookup(terms):
    modes=yaml.safe_load(ONTOLOGY.read_text())['modes']
    for term in terms:
        def score(mode):
            values=[mode['name'],*mode.get('synonyms',[])]
            return max(difflib.SequenceMatcher(None,normalized(term),normalized(value)).ratio() for value in values)
        ranked=sorted(modes,key=score,reverse=True)[:5]
        print(json.dumps({'term':term,'closest':[{'id':m['id'],'name':m['name'],
           'definition':m['definition'],'synonyms':m.get('synonyms',[]),'boundary':m.get('concept_boundary','')} for m in ranked]},ensure_ascii=False))


def status():
    files=read_json(MANIFEST)['files'];reviewed=[f for f in files if f['status']!='pending']
    for f in reviewed:
        r=read_json(ROOT/f['review']);assert r['sequence']==f['sequence'] and r['source']['sha256']==f['sha256']
    print(json.dumps({'processed_files':len(reviewed),'full_text_reviews':sum(f['status']=='reviewed' for f in files),
      'verified_duplicate_files':sum(f['status']=='duplicate-verified' for f in files),'remaining':sum(f['status']=='pending' for f in files),
      'next':next((f for f in files if f['status']=='pending'),None)},ensure_ascii=False,indent=2))


def sync_timelines():
    # Extend the existing dated snapshot with unavailable slots; never invent
    # a distribution for a newly indexed term or claim a fresh provider search.
    output=ROOT/'docs/literature-timelines.json'
    previous=read_json(output)
    spec=importlib.util.spec_from_file_location('annual_snapshots',ROOT/'experiments/literature-timelines.py')
    annual=importlib.util.module_from_spec(spec);spec.loader.exec_module(annual)
    with tempfile.TemporaryDirectory(prefix='ethicalai-annual-sync-') as directory:
        cache=Path(directory)
        for record in previous['records']:write_json(cache/(str(record['num'])+'.json'),record)
        annual.build(cache,output)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    p=sub.add_parser('apply');p.add_argument('review',type=Path);p.add_argument('--pdf',type=Path,required=True)
    p=sub.add_parser('lookup');p.add_argument('terms',nargs='+')
    p=sub.add_parser('pages');p.add_argument('pdf',type=Path);p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int)
    sub.add_parser('status')
    sub.add_parser('sync-timelines')
    sub.add_parser('sync-citations')
    args=parser.parse_args()
    if args.action=='apply':apply_review(args.review,args.pdf)
    elif args.action=='lookup':lookup(args.terms)
    elif args.action=='pages':
        pages=pdf_pages(args.pdf)
        for index in range(args.start-1,min(args.end or len(pages),len(pages))):print(f'\n--- PDF page {index+1} ---\n'+pages[index])
    elif args.action=='sync-timelines':sync_timelines()
    elif args.action=='sync-citations':sync_citations()
    else:status()
