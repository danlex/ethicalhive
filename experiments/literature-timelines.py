#!/usr/bin/env python3
"""Collect complete, reproducible annual arXiv search-match counts for catalogue terms.

One polite request stream; cached successes can be resumed. Counts describe
matching publications, not occurrences of words, citations or validated effects.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml
from arxiv_citations import API, CATEGORY_FILTER, NS

ROOT = Path(__file__).resolve().parents[1]
START_YEAR = 1991
PAGE_SIZE = 1000


def modes():
    return yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())['modes']


def search_query(mode):
    source = mode['literature_search']
    # Reuse the actual scoped query, including its original Boolean grouping.
    query = parse_qs(urlparse(source['url']).query).get('search_query', [''])[0]
    if not query or any(c not in query for c in ('cat:cs.AI', 'cat:cs.CL', 'cat:cs.LG')):
        raise ValueError(f"Missing scoped arXiv query for {mode['id']}")
    return query


def fingerprint(query):
    return hashlib.sha256(query.encode()).hexdigest()


def parse_feed(body):
    root = ET.fromstring(body)
    total = root.findtext('opensearch:totalResults', default='', namespaces=NS)
    if not total or not total.isdigit():
        raise ValueError('arXiv did not return a totalResults count')
    rows = []
    for entry in root.findall('atom:entry', NS):
        identity = entry.findtext('atom:id', default='', namespaces=NS)
        if '/api/errors' in identity:
            raise ValueError('arXiv returned an error entry')
        published = entry.findtext('atom:published', default='', namespaces=NS)
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T.*', published):
            raise ValueError('A result lacks its first-submission date')
        rows.append((re.sub(r'v\d+$', '', identity.rsplit('/abs/', 1)[-1]), published))
    return int(total), rows


def annual_counts(rows, start_year, end_year):
    counts = Counter()
    for identity, published in rows:
        year = int(published[:4])
        if not start_year <= year <= end_year:
            raise ValueError(f'Publication date outside the declared interval: {identity}: {published}')
        counts[year] += 1
    return [{'year':year, 'count':counts[year]} for year in range(start_year, end_year+1)]


class ArxivClient:
    def __init__(self, interval=3.4):
        self.interval = interval
        self.previous = 0

    def get(self, url):
        pause = self.previous + self.interval - time.monotonic()
        if pause > 0: time.sleep(pause)
        self.previous = time.monotonic()
        with urlopen(Request(url, headers={'User-Agent':'EthicalAI-annual-literature/1.0 (https://ethicalai.alexandrudan.com)'}), timeout=45) as response:
            return response.read()


def collect(mode, client, cache, end_year, page_size=PAGE_SIZE):
    query = search_query(mode)
    path = cache/(str(mode['num'])+'.json')
    if path.exists():
        old = json.loads(path.read_text())
        if old.get('query_hash') == fingerprint(query) and old.get('end_year') == end_year and old.get('status') == 'complete':
            return old
    checked = datetime.now(timezone.utc).isoformat(timespec='seconds')
    record = {'id':mode['id'], 'num':mode['num'], 'name':mode['name'],
              'database':'arXiv', 'scope':'AI-domain preprints in cs.AI, cs.CL and cs.LG',
              'query':query, 'query_hash':fingerprint(query), 'date_field':'first submission (Atom published)',
              'start_year':START_YEAR, 'end_year':end_year, 'queried_at':checked,
              'status':'unavailable', 'total':None, 'years':None}
    collected = {}; total = None; urls = []
    try:
        start = 0
        while total is None or start < total:
            url = API+'?'+urlencode({'search_query':query, 'start':start, 'max_results':page_size,
                                     'sortBy':'submittedDate', 'sortOrder':'ascending'})
            for attempt in range(3):
                try:
                    declared, rows = parse_feed(client.get(url))
                    break
                except HTTPError as error:
                    if attempt == 2 or error.code not in (429, 500, 502, 503, 504): raise
                    delay = min(60, max(4, int(error.headers.get('Retry-After', '10'))))
                    time.sleep(delay)
                except (TimeoutError, OSError):
                    if attempt == 2: raise
                    time.sleep(5)
            if total is not None and declared != total:
                raise ValueError('Result total changed during pagination; no complete series asserted')
            total = declared; urls.append(url)
            if start == 0 and total > 10000:
                # arXiv limits deep pagination. Annual aggregate queries avoid
                # truncating broad terms or downloading tens of thousands of abstracts.
                years = []
                for year in range(START_YEAR, end_year+1):
                    annual_query = '('+query+') AND submittedDate:['+str(year)+'01010000 TO '+str(year)+'12312359]'
                    annual_url = API+'?'+urlencode({'search_query':annual_query, 'max_results':1})
                    annual_total, _ = parse_feed(client.get(annual_url))
                    years.append({'year':year,'count':annual_total})
                    urls.append(annual_url)
                if sum(point['count'] for point in years) != total:
                    raise ValueError('Annual aggregate totals do not reconcile with the full query')
                record.update(status='complete', total=total, years=years,
                    method='Reconciled provider counts for disjoint first-submission-year ranges',
                    retrieved_records=0, pages=urls)
                path.write_text(json.dumps({**record,'records':[]}, ensure_ascii=False, indent=2)+'\n')
                return record
            if total and not rows:
                raise ValueError('Pagination ended before the declared total')
            for identity, published in rows:
                if identity in collected:
                    raise ValueError('Duplicate publication across result pages')
                collected[identity] = published
            start += len(rows)
            if len(collected) > total:
                raise ValueError('Result rows exceed the declared total')
        if len(collected) != total:
            raise ValueError('Incomplete result coverage')
        record.update(status='complete', total=total, years=annual_counts(collected.items(), START_YEAR, end_year),
                      method='Complete matching-publication metadata grouped by first-submission year',
                      retrieved_records=len(collected), pages=urls,
                      records_sha256=fingerprint(json.dumps(sorted(collected.items()))))
    except Exception as error:
        record.update(status='partial' if collected else 'unavailable', error=str(error),
                      retrieved_records=len(collected), provider_total=total, pages=urls)
    # Retain publication identities/dates in the fetch cache for independent re-scoring.
    cached = {**record, 'records':sorted(collected.items())}
    path.write_text(json.dumps(cached, ensure_ascii=False, indent=2)+'\n')
    return cached


def build(cache, output):
    end_year = datetime.now(timezone.utc).year
    records = []
    for mode in modes():
        path = cache/(str(mode['num'])+'.json')
        record = json.loads(path.read_text()) if path.exists() else {
            'id':mode['id'], 'num':mode['num'], 'name':mode['name'], 'status':'unavailable',
            'query':search_query(mode), 'query_hash':fingerprint(search_query(mode)),
            'total':None, 'years':None, 'start_year':START_YEAR, 'end_year':end_year,
            'error':'No complete annual search snapshot is available.'}
        if record['id'] != mode['id'] or record['query_hash'] != fingerprint(search_query(mode)):
            raise ValueError(f"Cached series does not match the current term/query: {mode['id']}")
        record.pop('records', None)
        record['catalogue_total'] = mode['literature_search']['count']
        record['catalogue_queried_at'] = mode['literature_search']['queried_at']
        records.append(record)
    payload = {'schema_version':1, 'database':'arXiv', 'scope':'cs.AI OR cs.CL OR cs.LG',
               'unit':'Matching publications per year of first arXiv submission',
               'note':'Keyword-query matches, not word occurrences, full-text mentions, citations or validated behaviours. Missing data is not zero.',
               'built_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),
               'start_year':START_YEAR, 'end_year':end_year, 'current_year_partial':True,
               'records':records}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
    with output.with_suffix('.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['id','name','year','matching_publications','status','snapshot_date','partial_year'])
        writer.writeheader()
        for record in records:
            points = record['years'] if record['status']=='complete' else [{'year':'','count':''}]
            for point in points:
                writer.writerow({'id':record['id'],'name':record['name'],'year':point['year'],
                    'matching_publications':point['count'],'status':record['status'],
                    'snapshot_date':record.get('queried_at',''),
                    'partial_year':point['year']==end_year if point['year']!='' else ''})
    print(json.dumps(dict(Counter(r['status'] for r in records))), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inspect','fetch','build'])
    parser.add_argument('--cache', type=Path, default=Path('/tmp/ethicalai-literature-timelines'))
    parser.add_argument('--output', type=Path, default=ROOT/'docs/literature-timelines.json')
    parser.add_argument('--ids', help='Optional comma-separated stable reference numbers')
    parser.add_argument('--interval', type=float, default=3.4)
    args = parser.parse_args()
    if args.interval < 3.3: parser.error('The arXiv request interval must be at least 3.3 seconds')
    if args.action == 'inspect':
        rows = modes(); counts = [m['literature_search']['count'] for m in rows]
        print(json.dumps({'terms':len(rows), 'zero_in_previous_snapshot':sum(c==0 for c in counts),
              'matching_publications_in_previous_snapshot':sum(c for c in counts if isinstance(c,int)),
              'largest_queries':sorted([{'id':m['id'],'count':m['literature_search']['count']} for m in rows],key=lambda x:x['count'] or 0,reverse=True)[:12]},indent=2))
    elif args.action == 'build': build(args.cache, args.output)
    else:
        args.cache.mkdir(parents=True, exist_ok=True)
        wanted = {int(n) for n in args.ids.split(',')} if args.ids else None
        client = ArxivClient(args.interval)
        for mode in modes():
            if wanted is not None and mode['num'] not in wanted: continue
            record = collect(mode, client, args.cache, datetime.now(timezone.utc).year)
            print(mode['num'], mode['name'], record['status'], record['total'], record.get('error',''), flush=True)


if __name__ == '__main__': main()
