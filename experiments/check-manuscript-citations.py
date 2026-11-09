#!/usr/bin/env python3
"""Fetch official arXiv citation metadata for the manuscripts, without full-text claims."""
import argparse,json,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode

from arxiv_metadata import feed

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ref',default='72ebf8772792fcef0dc92bf72045e40c112341b9')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();ids=set()
    for name in ('paper/draft.md','paper/ethicalai-benchmark.md'):
        text=subprocess.check_output(['git','show',args.ref+':'+name],cwd=ROOT,text=True)
        refs=text.split('# References')[-1] if name.endswith('/draft.md') else text.split('## References')[-1]
        ids.update(re.findall(r'(?:arXiv[: ]+)(\d{4}\.\d{4,5})',refs,re.I))
    records=[]
    for start in range(0,len(ids),15):
        group=sorted(ids)[start:start+15]
        endpoint='https://export.arxiv.org/api/query?'+urlencode({'id_list':','.join(group),'max_results':len(group)})
        _,papers=feed(endpoint)
        for p in papers:
            p.pop('abstract',None)
            p.update(verification_url=endpoint,consulted='Official arXiv bibliographic title, author byline and publication metadata only; full paper not read in this check.')
            records.append(p)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({'checked_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'source_ref':args.ref,'access':'Bibliographic metadata only','records':records},ensure_ascii=False,indent=2)+'\n')
    for p in records:print(p['id'],p['title'],'|','; '.join(p['authors'][:5]),flush=True)


if __name__=='__main__':main()
