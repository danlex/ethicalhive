#!/usr/bin/env python3
"""Fetch reproducible literature-match totals and candidate citations.

Search totals come from the provider's result metadata, never from the length
of the selected-citation list or a paper's cited_by_count. Raw search results
are cached outside the repository; selecting references is a separate step.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

FIELDS='id,doi,title,publication_year,type,authorships,primary_location,abstract_inverted_index,ids,is_retracted'
LOCK=threading.Lock()
LAST_REQUEST=0.0
STOP=threading.Event()

def fetch(record,cache,interval,limit):
    global LAST_REQUEST
    path=cache/(str(record['num'])+'.json')
    if path.exists():
        data=json.loads(path.read_text())
        if data.get('query')==record['query'] and data.get('filters')==record['filters']:
            return data
    endpoint='https://api.openalex.org/works?'+urlencode({
        'search':record['query'],'filter':record['filters'],
        'per-page':limit,'select':FIELDS})
    for attempt in range(4):
        if STOP.is_set():raise RuntimeError('Search paused after a provider-wide failure; cached results are retained')
        with LOCK:
            pause=LAST_REQUEST+interval-time.monotonic()
            if pause>0:time.sleep(pause)
            LAST_REQUEST=time.monotonic()
        try:
            with urlopen(Request(endpoint,headers={'User-Agent':'EthicalAI-literature-map/1.0 (https://ethicalai.alexandrudan.com)'}),timeout=35) as response:
                payload=json.load(response)
            total=payload['meta']['count']
            assert type(total) is int and total>=0
            result=dict(num=record['num'],id=record['id'],query=record['query'],filters=record['filters'],
                database='OpenAlex',endpoint=endpoint,count=total,
                retrieved_at=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                provider_meta=payload['meta'],results=payload['results'])
            temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');temporary.replace(path)
            return result
        except HTTPError as error:
            detail=error.read().decode(errors='replace')[:1200]
            if error.code==503 and 'Anonymous search is paused' in detail:
                # Some cached searches remain available during this partial
                # outage. Do not repeatedly retry this unavailable query.
                raise RuntimeError('Provider temporarily paused this anonymous search: '+detail) from error
            if error.code==429 and ('budget' in detail.lower() or 'credit' in detail.lower()):
                STOP.set();raise RuntimeError('Provider budget exhausted: '+detail) from error
            if error.code not in (429,502,503,504) or attempt==3:raise
            delay=int(error.headers.get('Retry-After',str(3*(attempt+1))))
            if delay>60:raise RuntimeError('Provider requested a longer pause; resume this cached job later') from error
            # Retry-After applies to this client's whole request stream.
            with LOCK:LAST_REQUEST=max(LAST_REQUEST,time.monotonic()+max(1,delay))
    raise RuntimeError('Search did not return a valid count')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--ids',help='Optional comma-separated stable reference numbers')
    parser.add_argument('--interval',type=float,default=.7)
    parser.add_argument('--max-results',type=int,default=12)
    args=parser.parse_args()
    args.cache.mkdir(parents=True,exist_ok=True)
    plan=json.loads(args.plan.read_text())['records']
    if args.ids:
        wanted={int(n) for n in args.ids.split(',')};plan=[r for r in plan if r['num'] in wanted]
    failures=[]
    with ThreadPoolExecutor(max_workers=1) as pool:
        futures={pool.submit(fetch,r,args.cache,args.interval,args.max_results):r for r in plan}
        for future in as_completed(futures):
            record=futures[future]
            try:
                result=future.result()
                print(record['num'],result['count'],[p['title'][:100] for p in result['results'][:3]],flush=True)
            except Exception as error:
                failures.append(record['num']);print(record['num'],'FAILED',str(error),flush=True)
    print(json.dumps({'completed':len(plan)-len(failures),'failed':failures}),flush=True)
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
