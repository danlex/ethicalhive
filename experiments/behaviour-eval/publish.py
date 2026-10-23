#!/usr/bin/env python3
"""publish.py - render a behaviour experiment into docs/experiments/<behaviour>.html.

Generic: reads the results JSON produced by any runner (run.py, run-confabulation.py)
and renders a self-contained page styled like the EthicalAI site. The JSON carries
title, lede, method, verdict, the per-model columns, and the items, so one
generator serves every experiment. Re-run after a fresh benchmark to update.

Usage: publish.py <behaviour>        (e.g. publish.py confabulation)
"""

import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent.parent / "docs" / "experiments"


def esc(s):
    return html.escape(str(s))


def cell(v, n):
    if isinstance(v, bool):
        return esc(v)
    if isinstance(v, int):
        return f"{v}/{n}"
    if isinstance(v, float):
        return f"{v:g}"
    return esc(v)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: publish.py <behaviour>  (e.g. confabulation)")
    name = sys.argv[1]
    res = json.loads((HERE / f"results-{name}.json").read_text(encoding="utf-8"))
    n = res["n"]
    cols = res["columns"]
    flag = res.get("flag_key")
    models = sorted(res["models"], key=lambda m: -(m.get(flag, 0) or 0)) if flag else res["models"]

    thead = "".join(f"<th>{esc(lbl)}</th>" for _, lbl in cols)
    body = []
    for m in models:
        flagged = bool(m.get(flag)) if flag else False
        tds = "".join(f"<td>{cell(m.get(k), n)}</td>" for k, _ in cols)
        body.append(f'<tr{" class=flag" if flagged else ""}><td>{esc(m["model"])}</td>{tds}</tr>')
    model_rows = "\n".join(body)

    icols = res.get("item_columns", [["id", "Item"]])
    ithead = "".join(f"<th>{esc(lbl)}</th>" for _, lbl in icols)
    irows = "\n".join(
        "<tr>" + "".join(f"<td>{esc(it.get(k, ''))}</td>" for k, _ in icols) + "</tr>"
        for it in res.get("items", []))

    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(res['title'])} — model probe · EthicalAI</title>
<link rel="icon" type="image/png" href="../favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--accent:#FF4931;--ink:#141414;--muted:#64646a;--line:#eae8e6;--panel:#f6f5f4}}
*{{box-sizing:border-box}}
body{{font-family:Manrope,system-ui,sans-serif;color:var(--ink);margin:0;line-height:1.6;background:#fff}}
.wrap{{max-width:min(960px,92vw);margin:0 auto;padding:0 20px 80px}}
h1,h2{{font-family:'Space Grotesk',sans-serif;letter-spacing:-.5px}}
h1{{font-size:clamp(28px,5vw,44px);margin:36px 0 6px}}
h2{{font-size:20px;margin:36px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.eyebrow{{color:var(--accent);font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.1em;margin-top:34px}}
.lede{{font-size:18px;color:var(--muted);max-width:68ch}}
a{{color:var(--accent)}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:8px}}
th,td{{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-family:'Space Grotesk',sans-serif;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
tr.flag td{{background:#fdecf0}}
.verdict{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:14px 16px;margin:14px 0;font-size:16px}}
.back{{display:inline-block;margin:28px 0 0;font-family:'Space Grotesk',sans-serif;font-weight:600}}
small{{color:var(--muted)}}
</style></head>
<body><div class="wrap">
<p class="eyebrow">EthicalAI · Behaviour probe</p>
<h1>{esc(res['title'])}</h1>
<p class="lede">{esc(res.get('lede',''))}</p>
<div class="verdict">{esc(res.get('verdict',''))}</div>

<h2>Method</h2>
<p>{res.get('method','')} n = {n} items per model.</p>

<h2>Results</h2>
<table><thead><tr><th>Model</th>{thead}</tr></thead>
<tbody>
{model_rows}
</tbody></table>
<p><small>Pink rows triggered the flagged metric at least once. Counts are out of {n} items.</small></p>
{('<h2>Conclusion</h2><p>' + esc(res['conclusion']) + '</p>') if res.get('conclusion') else ''}
<h2>The items</h2>
<table><thead><tr>{ithead}</tr></thead>
<tbody>
{irows}
</tbody></table>

<h2>Caveats</h2>
<p>n = {n} per model is small; read these as counts, not rates, and expect run-to-run variation. The harness, items, and raw results are in the repository under <code>experiments/behaviour-eval/</code>.</p>

<a class="back" href="../index.html">← Back to the catalogue</a>
</div></body></html>
"""
    DOCS.mkdir(parents=True, exist_ok=True)
    out = DOCS / f"{name}.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
