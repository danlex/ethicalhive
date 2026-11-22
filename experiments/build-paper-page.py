#!/usr/bin/env python3
"""build-paper-page.py - render the resource paper to a styled HTML page on the site.

Reads paper/ontology-paper.md and writes docs/paper/ontology-paper.html, matching the site's look
(same palette and type as the other generated pages). No markdown library is available in
this repo, so this does a small, explicit conversion of the subset the paper uses:
headings, paragraphs (hard-wrapped lines joined), bullet lists, pipe tables, bold, inline
code, and markdown links. Bracketed citations like [Malberg et al. 2024] are left as plain
text (they are not markdown links). Run after editing the paper; it is idempotent.

Usage: python3 experiments/build-paper-page.py
"""
import re
from pathlib import Path
import yaml
from ethical_framework import render_framework

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "paper" / "ontology-paper.md"
OUT = ROOT / "docs" / "paper" / "ontology-paper.html"


def read_manuscript(path):
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'{path.name} needs canonical YAML front matter')
    _,header,body=text.split('---\n',2)
    return yaml.safe_load(header),body


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def render(md,heading_offset=0):
    lines = md.splitlines()
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # raw HTML figure block: pass through verbatim (e.g. an inline <figure><svg>...)
        if line.lstrip().startswith("<figure"):
            block = []
            while i < n:
                block.append(lines[i])
                done = "</figure>" in lines[i]
                i += 1
                if done:
                    break
            out.append("\n".join(block))
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            lvl = min(6,len(m.group(1))+heading_offset)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        # pipe table: a | row followed by a |---| separator
        if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2  # skip header + separator
            body = []
            while i < n and lines[i].lstrip().startswith("|"):
                body.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in header)
            trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in body)
            out.append(f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')
            continue
        # bullet list
        if line.lstrip().startswith("- "):
            items = []
            while i < n and lines[i].lstrip().startswith("- "):
                # join soft-wrapped continuation lines of a bullet
                buf = lines[i].lstrip()[2:]
                i += 1
                while i < n and lines[i].strip() and not lines[i].lstrip().startswith("- ") \
                        and not lines[i].lstrip().startswith("|") and not re.match(r"^#{1,3}\s", lines[i]):
                    buf += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{inline(buf)}</li>")
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        # paragraph: join consecutive plain lines
        buf = [line.strip()]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^#{1,3}\s", lines[i]) \
                and not lines[i].lstrip().startswith("- ") and not lines[i].lstrip().startswith("|"):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://ethicalai.alexandrudan.com/{canonical}">
<link rel="icon" type="image/png" href="{base}favicon.png">
<style>
:root{{--accent:#FF4931;--accent-d:#c2341a;--ink:#141414;--muted:#64646a;--line:#e7e5e2;--panel:#f6f5f4}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Manrope,system-ui,sans-serif;color:var(--ink);line-height:1.6;background:#fff}}
.wrap{{max-width:800px;margin:0 auto;padding:40px 22px 90px}}
a{{color:var(--accent-d)}}
h1{{font-size:clamp(24px,4vw,34px);line-height:1.2;margin:22px 0 4px}}
h2{{font-size:22px;margin:38px 0 10px;padding-top:10px;border-top:1px solid var(--line)}}
h3{{font-size:17px;margin:26px 0 8px}}
p{{margin:0 0 14px;max-width:72ch}}
ul{{max-width:72ch}} li{{margin:4px 0}}
.back{{font-size:13px;display:inline-block;margin-bottom:10px}}
.eyebrow{{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0}}
code{{background:var(--panel);padding:1px 5px;border-radius:4px;font-size:.9em}}
.tablewrap{{overflow-x:auto;margin:16px 0}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}}
th,td{{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}}
th{{background:var(--panel);font-weight:700}}
</style></head>
<body><div class="wrap">
<a class="back" href="{base}index.html#paper">&larr; EthicalAI</a>
<p class="eyebrow">Working paper</p>
{frontmatter}
<p><a href="{base}paper.pdf">Download catalogue paper · PDF</a> &middot; <a href="{base}methods-paper.pdf">Download advisory auditing paper · PDF</a></p>
{body}
</div></body></html>
"""

# Figure 1: the distribution of citation-failure classes (the finding's shape), injected after
# the typology table in the rendered page. Counts match the Section 3.1 table (sum 35).
_BARS = [("Surface-match", 14, "#c0392b"), ("Scope-mismatch", 12, "#8a8a8a"),
         ("Misfiling", 4, "#8a8a8a"), ("Polarity-reversal", 3, "#8a8a8a"),
         ("Wrong-population", 2, "#8a8a8a")]
_rows = "".join(
    f'<text x="182" y="{34+i*38}" text-anchor="end" font-size="15" fill="#222">{name}</text>'
    f'<rect x="192" y="{22+i*38}" width="{cnt*30}" height="22" fill="{col}" rx="2"/>'
    f'<text x="{200+cnt*30}" y="{38+i*38}" font-size="14" fill="#444">{cnt}</text>'
    for i, (name, cnt, col) in enumerate(_BARS))
TYPOLOGY_FIG = (
    '<figure style="margin:2rem 0">'
    f'<svg viewBox="0 0 680 210" role="img" aria-label="Distribution of the five citation-failure classes" '
    'style="max-width:100%;height:auto">{rows}</svg>'
    '<figcaption style="font-size:.9rem;color:#555;margin-top:.5rem">Figure 1. How the 35 logged '
    'citation mismatches fail, by class (counts approximate, sum 35). Surface-match, a right-term, '
    'wrong-phenomenon citation, dominates; polarity-reversal, the opposite result, is rarest but the '
    'most dangerous because a title or abstract skim ratifies it.</figcaption></figure>'
).replace("{rows}", _rows)


def main():
    (ROOT/"docs"/"paper").mkdir(parents=True, exist_ok=True)
    data,body=read_manuscript(SRC)
    title=esc(data['title'])
    abstract=' '.join(data['abstract'].split())
    frontmatter='<h1>'+title+'</h1><p>'+esc(str(data['author']))+' · '+esc(str(data['date']))+'</p><h2>Abstract</h2><p>'+inline(abstract)+'</p>'
    description=esc(abstract[:180]).replace('"','&quot;')
    rendered=render(body,1)
    OUT.write_text(PAGE.format(body=rendered,title=title,description=description,frontmatter=frontmatter,canonical="paper/ontology-paper.html",base="../"), encoding="utf-8")
    # Also render the benchmark/method paper to its own live page.
    methods,mbody=read_manuscript(ROOT/'paper/benchmark-paper.md')
    m_title=esc(methods['title']);m_abs=' '.join(str(methods.get('abstract','')).split())
    m_fm='<h1>'+m_title+'</h1><p>'+esc(str(methods['author']))+' · '+esc(str(methods['date']))+'</p><h2>Abstract</h2><p>'+inline(m_abs)+'</p>'
    (ROOT/'docs/paper/benchmark-paper.html').write_text(
        PAGE.format(body=render(mbody,1),title=m_title,description=esc(m_abs[:180]).replace('"','&quot;'),frontmatter=m_fm,canonical="paper/benchmark-paper.html",base="../"),encoding="utf-8")
    section=f'''<section class="framework" id="paper">
    <p class="research-baseline-note"><strong>Research scope:</strong> the catalogue study describes the historical 207-record release. Its measurements and the auditing pilot do not validate the 227 later analogies in the current 434-record catalogue.</p>
    <h2>Research papers</h2>
    <p>Two working papers examine the catalogue's evidence and the use of named obligations to review coding-agent drafts. Revised {esc(str(data['date']))}.</p>
    <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))">
      <article class="card"><h3>{title}</h3><p>A resource study of definitions, source support, construction errors and category use. The historical study and the expanded bibliography have separate evidence scopes.</p><p><a href="paper/ontology-paper.html">Read the catalogue paper</a> &middot; <a href="paper.pdf">Download PDF</a></p></article>
      <article class="card"><h3>{esc(methods['title'])}</h3><p>A pilot of reviewing one known obligation on project-authored coding cases. It reports detection, false alarms, exact-rule references and unresolved severity errors.</p><p><a href="paper/benchmark-paper.html">Read the auditing paper</a> &middot; <a href="methods-paper.pdf">Download PDF</a></p></article>
    </div>
    <p><a href="papers.html">Paper versions and changelog</a> &middot; <a href="https://github.com/danlex/ethicalhive/blob/main/experiments/research-runs-2026-11-09.json">Frozen run manifest</a> &middot; <a href="https://github.com/danlex/ethicalhive/blob/main/experiments/research-results-2026-11-09.md">Reproduce the results</a> &middot; <a href="#catalogue">Browse the catalogue</a></p>
  </section>'''
    home=ROOT/'docs/index.html';text=home.read_text(encoding='utf-8')
    principles,evaluation=render_framework()
    text,count=re.subn(r'<section class="cx-sec" id="principles">.*?</section>',lambda _:principles,text,count=1,flags=re.S)
    if count!=1:raise ValueError('Homepage principles section not found exactly once')
    if 'id="evaluation-categories"' in text:
        text,count=re.subn(r'<section class="cx-sec" id="evaluation-categories">.*?</section>',lambda _:evaluation,text,count=1,flags=re.S)
        if count!=1:raise ValueError('Homepage evaluation section not found exactly once')
    else:
        text=text.replace(principles,principles+'\n\n'+evaluation,1)
    text,count=re.subn(r'<section class="framework" id="paper">.*?</section>',lambda _:section,text,count=1,flags=re.S)
    if count!=1:raise ValueError('Homepage paper section not found exactly once')
    home.write_text(text,encoding='utf-8')
    print(f"wrote {OUT.relative_to(ROOT)} from {SRC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
