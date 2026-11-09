#!/usr/bin/env python3
"""Regression checks: totals, citation selections and unchanged legacy sources."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import yaml
from catalogue_sources import paper_identifier,selected_papers,literature_search

ROOT=Path(__file__).resolve().parents[1]
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/'experiments'/file)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
builder=module('catalogue_builder','build-catalogue.py')
refresh=module('arxiv_refresh','arxiv-literature-refresh.py')
onto=yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())
audit=json.loads((ROOT/onto['meta']['literature_review']['record']).read_text())
baseline=yaml.safe_load(subprocess.check_output(['git','show',audit['baseline_commit']+':ontology/ethical-ai.yaml'],cwd=ROOT,text=True))
plan={r['num']:r for r in json.loads((ROOT/'references/literature-search-queries-2026-11-09.json').read_text())['records']}
records={r['num']:r for r in audit['records']}
assert len(records)==len(onto['modes'])==434
rejected={r['id'] for r in audit['rejected_matches'] if 'num' not in r}
rejected_bindings={(r['num'],r['id']) for r in audit['rejected_matches'] if 'num' in r}
for old,mode in zip(baseline['modes'],onto['modes']):
    assert {k:v for k,v in mode.items() if k not in ('selected_papers','literature_search')}==old,mode['id']
    papers=selected_papers(mode);search=literature_search(mode);record=records[mode['num']]
    assert len(papers)<=3 and [p['id'] for p in papers]==record['selected_ids']
    assert len({paper_identifier(p['url']) for p in papers})==len(papers)
    assert len({re.sub(r'\W+','',p['title'].casefold()) for p in papers})==len(papers)
    hashes=[hashlib.sha256(json.dumps(p,ensure_ascii=False,sort_keys=True).encode()).hexdigest() for p in papers]
    assert hashes==record['selected_sha256']
    assert record['shortfall']==3-len(papers)
    assert search==record['literature_search']
    assert search['query']==refresh.arxiv_clause(plan[mode['num']]['query'])
    assert refresh.cache_matches(search,search['query']),mode['num']
    for p in papers:
        # A DOI rejected for one mistaken attribution can be relevant elsewhere.
        assert p['id'] not in rejected-{'doi:10.1002/bdm.583'},(mode['num'],p['id'])
        assert (mode['num'],p['id']) not in rejected_bindings
        assert not any(k in p for k in ('review_excerpt','matched_query','manually_reviewed'))
        assert p['url'].startswith('https://') and p['verification_url'].startswith('https://')
        assert not p['id'].startswith(('doi:10.4249/scholarpedia.','doi:10.31525/ct1-'))
assert audit['result']['entries_with_three_selected_papers']==sum(len(selected_papers(m))==3 for m in onto['modes'])
assert audit['result']['entries_with_search_totals']==sum(literature_search(m)['count'] is not None for m in onto['modes'])
assert len(audit['remaining_shortfalls'])==sum(len(selected_papers(m))<3 for m in onto['modes'])

# The number displayed must stay independent of zero, one or three citations.
fixture=copy.deepcopy(onto['modes'][0]);fixture.pop('research_candidate',None)
fixture['selected_papers']=fixture['selected_papers'][:1]
fixture['literature_search']['count']=987654
fixture['literature_search']['status']='available'
builder.MODE_NAME={m['id']:m['name'] for m in onto['modes']}
builder.PRIN_NAME={p['id']:p['name'] for p in onto['principles']}
builder.HARM_NAME={p['id']:p['name'] for p in onto['harm_types']}
builder.MIT_NAME={p['id']:p['name'] for p in onto['mitigations']}
row=builder.box(fixture)
assert '>987,654</span>' in row and 'Selected citations: 1 of 3' in row
fixture['selected_papers']=[dict(fixture['selected_papers'][0],id='fixture:'+str(n),domain='human-related') for n in range(3)]
fixture['literature_search']['count']=None
assert 'pcount-empty' in builder.box(fixture) and 'Selected citations: 3 of 3' in builder.box(fixture)
fixture['literature_search']['count']=0
assert '>0</span>' in builder.box(fixture)
assert paper_identifier('https://arxiv.org/pdf/2311.07954v2.pdf')==paper_identifier('https://doi.org/10.48550/arXiv.2311.07954')
assert paper_identifier('https://doi.org/10.1037//h0040525')=='doi:10.1037/h0040525'
from urllib.parse import urlencode
import arxiv_citations
query='all:"first alternative" OR all:"second alternative"'
wrong={'query':query,'url':arxiv_citations.API+'?'+urlencode({'search_query':query+' AND '+arxiv_citations.CATEGORY_FILTER})}
assert not refresh.cache_matches(wrong,query)
correct={**wrong,'url':arxiv_citations.API+'?'+urlencode({'search_query':'('+query+') AND '+arxiv_citations.CATEGORY_FILTER})}
assert refresh.cache_matches(correct,query)
print('PASS: independent totals (large/zero/unavailable), canonical citations, selection audit, exact queries and all legacy mode fields preserved.')
