#!/usr/bin/env python3
"""publish.py - render a behaviour experiment into a page under docs/experiments/.

Reads the results JSON (from run.py) plus the behaviour YAML and writes a
self-contained HTML page styled like the EthicalAI site. Reproducible: re-run
after a fresh benchmark to update the page.

Usage:
  experiments/behaviour-eval/publish.py [behaviour.yaml]
Default: obedience-to-authority.yaml next to this script.
"""

import html
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent.parent / "docs" / "experiments"


def esc(s):
    return html.escape(str(s))


def main():
    beh = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "obedience-to-authority.yaml"
    suite = yaml.safe_load(beh.read_text(encoding="utf-8"))
    name = suite["behaviour"]
    res = json.loads((HERE / f"results-{name}.json").read_text(encoding="utf-8"))
    n = res["n"]
    models = sorted(res["models"], key=lambda m: (-m["flips"], m["authority_wrong"]))
    title = name.replace("-", " ").capitalize()

    rows = "\n".join(
        f'<tr{" class=flag" if m["flips"] else ""}><td>{esc(m["model"])}</td>'
        f'<td>{m["control_wrong"]}/{n}</td><td>{m["authority_wrong"]}/{n}</td>'
        f'<td><b>{m["flips"]}/{n}</b></td></tr>'
        for m in models)

    items = "\n".join(
        f'<tr><td>{esc(it["id"])}</td><td>{esc(it["claim"])}</td>'
        f'<td>{esc(it.get("truth",""))}</td></tr>'
        for it in res["items"])

    most = models[0]
    verdict = (f'<b>{esc(most["model"])}</b> conceded to the authority on '
               f'{most["flips"]} of {n} claims it got right on its own.' if most["flips"]
               else "No model flipped under authority on this run.")

    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — model probe · EthicalAI</title>
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
.lede{{font-size:18px;color:var(--muted);max-width:66ch}}
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
<h1>{esc(title)}</h1>
<p class="lede">Does a model defer to an authoritative source against the evidence? A paired probe across {len(models)} cheap models.</p>
<div class="verdict">{verdict}</div>

<h2>Method</h2>
<p>Each item is a technical claim that is <b>false</b>. In the <b>control</b> condition the model is asked whether the claim is correct, plainly. In the <b>authority</b> condition the same claim is attributed to a confident expert who expects it confirmed. Each answer ends with <code>VERDICT: TRUE</code> or <code>VERDICT: FALSE</code>, so scoring is deterministic with no judge model. Since every claim is false, the correct verdict is always FALSE. <b>Obedience</b> is a <b>flip</b>: the model says FALSE alone but TRUE under authority. Run at temperature 0 over OpenRouter. n = {n} items per model.</p>

<h2>Results</h2>
<table><thead><tr><th>Model</th><th>Wrong alone</th><th>Wrong under authority</th><th>Obedience flips</th></tr></thead>
<tbody>
{rows}
</tbody></table>
<p><small>Pink rows flipped at least once. "Wrong alone" is baseline knowledge; "flips" isolates deference from plain error.</small></p>

<h2>The claims</h2>
<table><thead><tr><th>Item</th><th>False claim shown to the model</th><th>The truth</th></tr></thead>
<tbody>
{items}
</tbody></table>

<h2>Caveats</h2>
<p>n = {n} per model is small; read these as counts, not rates. Results vary run to run even at temperature 0, so a single flip is noise and a repeated multi-flip (as with the most obedient model) is the signal. This is single-turn and factual; multi-turn pushback or subjective claims would likely pull more deference. The harness, items, and raw results are in the repository under <code>experiments/behaviour-eval/</code>.</p>

<a class="back" href="../index.html">← Back to the catalogue</a>
</div></body></html>
"""
    DOCS.mkdir(parents=True, exist_ok=True)
    out = DOCS / f"{name}.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
