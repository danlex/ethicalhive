#!/usr/bin/env python3
"""Refresh total AI-paper query matches independently of selected references."""
import argparse,json,re,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode,urlparse,parse_qs
import arxiv_citations
from arxiv_metadata import feed

def arxiv_clause(query):
    tokens=re.findall(r'"[^"]*"|\(|\)|\bAND\b|\bOR\b|[^\s()]+',query)
    return ' '.join(token if token in ('AND','OR','(',')') else 'all:'+token for token in tokens)

def has_top_level_or(query):
    depth=0
    for token in re.findall(r'"[^"]*"|\(|\)|\bOR\b',query):
        if token=='(':depth+=1
        elif token==')':depth-=1
        elif token=='OR' and depth==0:return True
    return False

def cache_matches(data,query):
    if data.get('query')!=query:return False
    actual=parse_qs(urlparse(data.get('url','')).query).get('search_query',[''])[0]
    scoped='('+query+') AND '+arxiv_citations.CATEGORY_FILTER
    # Earlier conjunction-only requests are equivalent. An ungrouped OR is not:
    # its first branch can escape the category filter under Boolean precedence.
    return actual==scoped or (not has_top_level_or(query) and actual==query+' AND '+arxiv_citations.CATEGORY_FILTER)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan',type=Path,required=True)
    ap.add_argument('--cache',type=Path,required=True)
    ap.add_argument('--interval',type=float,default=3.2)
    ap.add_argument('--ids')
    args=ap.parse_args();args.cache.mkdir(exist_ok=True,parents=True)
    rows=json.loads(args.plan.read_text())['records']
    if args.ids:
        ids={int(n) for n in args.ids.split(',')};rows=[r for r in rows if r['num'] in ids]
    failed=[]
    for row in rows:
        n=row['num'];query=arxiv_clause(row['query']);path=args.cache/(str(n)+'.json')
        if path.exists() and cache_matches(json.loads(path.read_text()),query):continue
        endpoint=arxiv_citations.API+'?'+urlencode({'search_query':'('+query+') AND '+arxiv_citations.CATEGORY_FILTER,'sortBy':'relevance','sortOrder':'descending','max_results':'5'})
        for attempt in range(3):
            try:
                count,papers=feed(endpoint)
                if count is None:raise RuntimeError('No totalResults returned by the provider')
                data=dict(num=n,id=row['id'],database='arXiv',query=query,filters=arxiv_citations.CATEGORY_FILTER,
                    count=count,status='available',queried_at=datetime.now(timezone.utc).isoformat(timespec='seconds'),url=endpoint,
                    scope='AI-domain arXiv preprints in cs.AI, cs.CL and cs.LG; keyword matches can include incidental or unrelated uses.',
                    results=papers)
                temporary=path.with_suffix('.tmp')
                temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temporary.replace(path)
                print(n,count,[p['title'][:100] for p in papers[:3]],flush=True);break
            except Exception as error:
                if attempt==2:
                    failed.append(n);print(n,'FAILED',str(error),flush=True)
                else:
                    pause=int(error.headers.get('Retry-After','10')) if isinstance(error,HTTPError) else 10
                    if pause>60:failed.append(n);print(n,'FAILED Provider requested longer pause',flush=True);break
                    time.sleep(max(3,pause))
        time.sleep(args.interval)
    print(json.dumps({'records':len(rows),'failed':failed}),flush=True)
    if failed:raise SystemExit(1)
if __name__=='__main__':main()
