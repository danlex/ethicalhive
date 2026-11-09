"""Read official arXiv Atom records, with a shared polite request interval."""
import json
from pathlib import Path
import time
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import xml.etree.ElementTree as ET
from arxiv_citations import NS

def feed(url):
    # Shared by the total refresher and bibliography lookup, so independent jobs
    # cannot each consume the provider's full request allowance.
    import fcntl
    with Path('/tmp/ethicalai-arxiv-api-rate.lock').open('a+') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX);stream.seek(0)
        previous=float(stream.read() or 0);pause=previous+3.3-time.time()
        if pause>0:time.sleep(pause)
        stream.seek(0);stream.truncate();stream.write(str(time.time()));stream.flush()
        fcntl.flock(stream,fcntl.LOCK_UN)
    try:
        with urlopen(Request(url,headers={'User-Agent':'EthicalAI-literature-map/1.0'}),timeout=40) as response:
            root=ET.fromstring(response.read())
    except HTTPError as error:
        if error.code==429:
            delay=max(3,int(error.headers.get('Retry-After','40')))
            with Path('/tmp/ethicalai-arxiv-api-rate.lock').open('a+') as stream:
                fcntl.flock(stream,fcntl.LOCK_EX);stream.seek(0)
                next_time=max(float(stream.read() or 0),time.time()+delay)
                stream.seek(0);stream.truncate();stream.write(str(next_time));stream.flush()
                fcntl.flock(stream,fcntl.LOCK_UN)
            detail=error.read().decode(errors='replace')[:350]
            print('arXiv temporarily rate-limited; shared pause',delay,'seconds;',detail,flush=True)
        raise
    total=root.findtext('opensearch:totalResults',default='',namespaces=NS)
    records=[]
    for entry in root.findall('atom:entry',NS):
        url=entry.findtext('atom:id',default='',namespaces=NS).strip()
        if 'arxiv.org/api/errors' in url:raise ValueError('arXiv returned an error feed')
        records.append(dict(id=url.rsplit('/abs/',1)[-1],url=url,
            title=' '.join(entry.findtext('atom:title',default='',namespaces=NS).split()),
            year=entry.findtext('atom:published',default='',namespaces=NS)[:4],
            authors=[a.findtext('atom:name',default='',namespaces=NS) for a in entry.findall('atom:author',NS)],
            abstract=' '.join(entry.findtext('atom:summary',default='',namespaces=NS).split()),
            doi=entry.findtext('{http://arxiv.org/schemas/atom}doi',default='')))
    return (int(total) if total else None),records
