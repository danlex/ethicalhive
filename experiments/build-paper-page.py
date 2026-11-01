#!/usr/bin/env python3
"""build-paper-page.py - render the resource paper to a styled HTML page on the site.

Reads paper/ethicalai-benchmark.md and writes docs/paper.html, matching the site's look
(same palette and type as the other generated pages). No markdown library is available in
this repo, so this does a small, explicit conversion of the subset the paper uses:
headings, paragraphs (hard-wrapped lines joined), bullet lists, pipe tables, bold, inline
code, and markdown links. Bracketed citations like [Malberg et al. 2024] are left as plain
text (they are not markdown links). Run after editing the paper; it is idempotent.

Usage: python3 experiments/build-paper-page.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "paper" / "ethicalai-benchmark.md"
OUT = ROOT / "docs" / "paper.html"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def render(md):
    lines = md.splitlines()
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
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
<title>EthicalAI: A Grounded Catalogue of AI Integrity Failure Modes</title>
<link rel="icon" type="image/png" href="favicon.png">
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
<a class="back" href="index.html#paper">&larr; EthicalAI</a>
<p class="eyebrow">Working paper</p>
{body}
</div></body></html>
"""


def main():
    md = SRC.read_text(encoding="utf-8")
    OUT.write_text(PAGE.format(body=render(md)), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} from {SRC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
