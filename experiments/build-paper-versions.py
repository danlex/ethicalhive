#!/usr/bin/env python3
"""build-paper-versions.py - archived, navigable paper versions with a per-version changelog.

Reads experiments/paper-versions.json. For each listed version of each paper, renders the
manuscript AT THAT GIT COMMIT to docs/papers/<key>-<version>.html, with the same styling as the
live page plus an archive banner. Then builds docs/papers.html, a navigation index that groups
both papers and lists every version newest-first with its changelog and links.

Usage: build-paper-versions.py
"""
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# Reuse the live page's renderer and template.
_spec = importlib.util.spec_from_file_location("bpp", HERE / "build-paper-page.py")
bpp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bpp)

MANIFEST = HERE / "paper-versions.json"
OUTDIR = ROOT / "docs" / "papers"
INDEX = ROOT / "docs" / "papers.html"
GH = "https://github.com/danlex/ethicalhive"

BANNER = (
    '<div style="background:#fff8e1;border:1px solid #e0c97f;padding:.6rem 1rem;margin:0 0 1.5rem;'
    'border-radius:6px;font-size:.9rem">Archived version <strong>{ver}</strong> '
    '({date}, commit <a href="{gh}/commit/{commit}">{commit}</a>). '
    '<a href="../papers.html">All versions</a>{live}</div>'
)


def render_version(source, commit, ver, date, live_href):
    md = subprocess.run(["git", "show", f"{commit}:{source}"], cwd=ROOT,
                        capture_output=True, text=True).stdout
    if not md.strip():
        return None, None
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as t:
        t.write(md)
        tmp = Path(t.name)
    data, body = bpp.read_manuscript(tmp)
    title = bpp.esc(data["title"])
    abstract = " ".join(str(data.get("abstract", "")).split())
    live = f' &middot; <a href="../{live_href}">Live version</a>' if live_href else ""
    banner = BANNER.format(ver=ver, date=date, commit=commit, gh=GH, live=live)
    fm = (banner + f'<h1>{title}</h1><p>{bpp.esc(str(data["author"]))} &middot; '
          f'{bpp.esc(str(data["date"]))}</p><h2>Abstract</h2><p>{bpp.inline(abstract)}</p>')
    desc = bpp.esc(abstract[:180]).replace('"', "&quot;")
    return bpp.PAGE.format(body=bpp.render(body, 1), title=f"{title} ({ver})",
                           description=desc, frontmatter=fm, base="../", canonical="papers.html"), title


def build_index(man, rendered):
    parts = ['<h1>Paper versions</h1>',
             '<p>Archived, navigable versions of each paper, with a changelog for every version. '
             'The newest version of the catalogue paper is also the live one.</p>']
    for p in man["papers"]:
        parts.append(f'<h2>{bpp.esc(p["title"])}</h2>')
        if p.get("live"):
            parts.append(f'<p><a href="{p["live"]}">Current live version</a></p>')
        for i, v in enumerate(p["versions"]):
            key = f'{p["key"]}-{v["version"]}'
            latest = ' <em>(latest)</em>' if i == 0 else ''
            link = (f'<a href="papers/{key}.html">Read this version</a>'
                    if rendered.get(key) else '<span>(not rendered)</span>')
            parts.append(f'<h3>{bpp.esc(v["version"])} <span style="font-weight:400;color:#666">'
                         f'&middot; {v["date"]}</span>{latest}</h3>')
            parts.append(f'<p>{link} &middot; commit '
                         f'<a href="{GH}/commit/{v["commit"]}">{v["commit"]}</a></p>')
            parts.append('<ul>' + ''.join(f'<li>{bpp.inline(bpp.esc(c))}</li>'
                                          for c in v["changelog"]) + '</ul>')
    body = "\n".join(parts)
    INDEX.write_text(bpp.PAGE.format(body=body, title="Paper versions",
                                     description="Archived, navigable versions of the EthicalAI papers with changelogs.",
                                     frontmatter="", base="", canonical="papers.html"), encoding="utf-8")


def main():
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rendered = {}
    for p in man["papers"]:
        for v in p["versions"]:
            # Each version renders from its own commit; versions committed before a file rename
            # carry a per-version "source" override so `git show <commit>:<old path>` still resolves.
            html, title = render_version(v.get("source", p["source"]), v["commit"], v["version"], v["date"], p.get("live"))
            key = f'{p["key"]}-{v["version"]}'
            if html:
                (OUTDIR / f"{key}.html").write_text(html, encoding="utf-8")
                rendered[key] = True
                print(f"  rendered {key}.html  ({title})")
            else:
                print(f"  SKIP {key} (no file at commit {v['commit']})")
    build_index(man, rendered)
    print(f"wrote {INDEX.relative_to(ROOT)} with {sum(len(p['versions']) for p in man['papers'])} versions")


if __name__ == "__main__":
    main()
