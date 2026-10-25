#!/usr/bin/env python3
"""paper-index.py - the paper <-> behaviour connective tissue.

Reads ontology/ethical-ai.yaml and builds the bipartite link between papers and the
modes they ground. Writes docs/experiments/paper-index.html with:
  - papers that ground 2+ modes (co-citations -> candidate relates_to edges),
  - the full paper -> modes index,
  - coverage gaps (modes with no paper yet).

Usage: experiments/paper-index.py
"""

import html
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY = ROOT / "ontology" / "ethical-ai.yaml"
OUT = ROOT / "docs" / "experiments" / "paper-index.html"


def esc(s):
    return html.escape(str(s))


def main():
    o = yaml.safe_load(ONTOLOGY.read_text(encoding="utf-8"))
    modes = o["modes"]
    papers = {}            # id -> {title, year, modes:set}
    gaps = []
    for m in modes:
        ps = (m.get("arxiv") or {}).get("papers") or []
        if not ps:
            gaps.append(m["name"])
            continue
        for p in ps:
            pid = re.sub(r"v\d+$", "", p.get("id", ""))
            if not pid:
                continue
            rec = papers.setdefault(pid, {"title": p.get("title", ""),
                                          "year": p.get("year", ""), "modes": set()})
            rec["modes"].add(m["name"])

    shared = sorted(((pid, r) for pid, r in papers.items() if len(r["modes"]) >= 2),
                    key=lambda t: -len(t[1]["modes"]))
    allp = sorted(papers.items(), key=lambda t: (-len(t[1]["modes"]), t[1]["year"]))
    grounded = sum(1 for m in modes if (m.get("arxiv") or {}).get("papers"))

    def paper_row(pid, rec):
        modes = ", ".join(sorted(rec["modes"]))
        return (f'<tr><td><a href="https://arxiv.org/abs/{esc(pid)}" target="_blank" '
                f'rel="noopener">{esc(pid)}</a></td><td>{esc(rec["year"])}</td>'
                f'<td>{esc(rec["title"])}</td><td>{esc(modes)}</td></tr>')

    out = [HEAD]
    out.append(f'<p class="lede">{len(modes)} modes · {grounded} grounded in at least one '
               f'paper · {len(papers)} distinct papers · {len(shared)} papers shared by 2+ '
               f'modes.</p>')
    out.append("<h2>Papers shared by two or more modes</h2>")
    out.append('<p>A paper that grounds several modes is evidence those modes co-occur, a '
               'candidate <code>relates_to</code> edge the graph may be missing.</p>')
    out.append('<table><tr><th>arXiv</th><th>Year</th><th>Title</th><th>Modes it grounds</th></tr>')
    out += [paper_row(pid, rec) for pid, rec in shared]
    out.append("</table>")
    out.append("<h2>Full paper index</h2>")
    out.append('<table><tr><th>arXiv</th><th>Year</th><th>Title</th><th>Modes</th></tr>')
    out += [paper_row(pid, rec) for pid, rec in allp]
    out.append("</table>")
    out.append(f"<h2>Coverage gaps ({len(gaps)} modes with no paper yet)</h2>")
    out.append(f'<p class="gaps">{esc(", ".join(sorted(gaps)))}</p>')
    out.append("</div></body></html>")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT}: {len(papers)} papers, {len(shared)} shared, {len(gaps)} gaps")


HEAD = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paper index · EthicalAI</title>
<link rel="icon" type="image/png" href="../favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Manrope,system-ui,sans-serif;color:#141414;line-height:1.55;background:#fff}
.wrap{max-width:1000px;margin:0 auto;padding:40px 22px 80px}
a{color:#c2341a}
h1{font-family:'Space Grotesk',sans-serif;font-size:32px;margin:0 0 6px}
h2{font-family:'Space Grotesk';font-size:19px;margin:30px 0 8px}
.lede{font-size:17px;color:#333}
.back{font-size:13px;display:inline-block;margin-bottom:16px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13px}
th,td{border:1px solid #e7e5e2;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f6f5f4;font-family:'Space Grotesk';font-weight:600;position:sticky;top:0}
td:nth-child(4){color:#555}
.gaps{font-size:13px;color:#64646a}
code{background:#f6f5f4;padding:1px 5px;border-radius:5px}
</style></head>
<body><div class="wrap">
<a class="back" href="../index.html#map">← EthicalAI catalogue</a>
<h1>Paper &harr; behaviour index</h1>"""


if __name__ == "__main__":
    main()
