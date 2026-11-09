#!/usr/bin/env python3
"""Build paper PDFs and standalone LaTeX from canonical Markdown metadata."""
import argparse
from datetime import datetime,timezone
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

import yaml

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'paper'


def metadata(source):
    text=source.read_text()
    if not text.startswith('---\n'):
        raise ValueError(f'{source.name} requires canonical YAML title, author, date and abstract')
    data=yaml.safe_load(text.split('---\n',2)[1])
    for key in ('title','author','date','abstract'):
        if not data.get(key):raise ValueError(f'{source.name}: missing {key}')
    return data


def build(source,compile_pdf=True):
    data=metadata(source)
    env=dict(os.environ)
    epoch=int(datetime.fromisoformat(str(data['date'])).replace(tzinfo=timezone.utc).timestamp())
    env['SOURCE_DATE_EPOCH']=str(epoch);env['FORCE_SOURCE_DATE']='1'
    with tempfile.TemporaryDirectory(prefix='ethicalai-paper-') as folder:
        temp=Path(folder);tex=temp/'main.tex'
        header=temp/'header.tex'
        header.write_text('\\usepackage{xurl}\n\\ifdefined\\pdfinfoomitdate\\pdfinfoomitdate=1\\pdftrailerid{}\\fi\n')
        command=['pandoc',str(source),'--standalone','--to','latex','--resource-path',str(PAPER),
            '--variable','fontsize=10pt','--variable','geometry=margin=19mm',
            '--variable','papersize=a4','--variable','colorlinks=true',
            '--variable','linkcolor=blue','--variable','urlcolor=blue',
            '--include-in-header',str(header),'-o',str(tex)]
        subprocess.run(command,cwd=PAPER,env=env,check=True,capture_output=True,text=True)
        generated=tex.read_text()
        if source.name=='draft.md':
            for destination in (PAPER/'latex',PAPER/'arxiv'):
                (destination/'main.tex').write_text(generated)
        if compile_pdf:
            for _ in range(2):
                result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                    '-file-line-error','-output-directory',str(temp),str(tex)],
                    cwd=PAPER,env=env,capture_output=True,text=True)
                if result.returncode:
                    raise RuntimeError(f'{source.name}: LaTeX compilation failed:\n'+result.stdout[-6500:])
            target=source.with_suffix('.pdf');shutil.copyfile(temp/'main.pdf',target)
            if source.name=='draft.md':
                for destination in (PAPER/'latex',PAPER/'arxiv'):
                    shutil.copyfile(target,destination/'main.pdf')
            print(f'Built {target.relative_to(ROOT)} from canonical Markdown')
        return generated


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',choices=['draft.md','ethicalai-benchmark.md'])
    ap.add_argument('--tex-only',action='store_true')
    ap.add_argument('--arxiv-package',action='store_true')
    args=ap.parse_args()
    for binary in ['pandoc']+([] if args.tex_only else ['pdflatex']):
        if not shutil.which(binary):raise SystemExit(f'Missing build dependency: {binary}')
    names=[args.source] if args.source else ['draft.md','ethicalai-benchmark.md']
    for name in names:build(PAPER/name,not args.tex_only)
    if args.arxiv_package:
        if args.source=='ethicalai-benchmark.md':raise SystemExit('The existing arXiv package contains the methods paper')
        destination=PAPER/'arxiv'/'submission.tar.gz'
        # The current short paper has no figure includes. If that changes, require
        # its explicit assets rather than silently creating an incomplete archive.
        tex=(PAPER/'arxiv'/'main.tex').read_text()
        if '\\includegraphics' in tex:raise SystemExit('Add the referenced figures to the arXiv packaging manifest first')
        with tarfile.open(destination,'w:gz') as archive:
            archive.add(PAPER/'arxiv'/'main.tex',arcname='main.tex')
        print(f'Built {destination.relative_to(ROOT)}; no submission is performed')


if __name__=='__main__':main()
