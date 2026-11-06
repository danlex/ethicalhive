#!/usr/bin/env python3
"""Render the language-discrepancy case from its evidence ledger.

The built page documents proposed regression fixtures; it does not execute them.
Usage: python3 experiments/build-self-evaluation.py [--check]
"""
import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASE = ROOT / 'cases/self-evaluation-language-discrepancy-2026-11-06.json'
OUT = ROOT / 'docs/experiments/self-evaluation-language-discrepancy.html'
E = html.escape


def paragraph(label, value):
    return f'<p><strong>{E(label)}.</strong> {E(value)}</p>'


def bullets(items):
    return '<ul>' + ''.join(f'<li>{E(s)}</li>' for s in items) + '</ul>'


def table(headers, rows):
    return ('<div class="table-scroll"><table><thead><tr>' +
            ''.join(f'<th scope="col">{E(h)}</th>' for h in headers) +
            '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(
                f'<td>{E(str(v))}</td>' for v in row) + '</tr>' for row in rows) +
            '</tbody></table></div>')


def render(c):
    components = ''.join('<article>' + f'<h3>{E(x["id"])} / {E(x["name"])}</h3>' +
                         paragraph('Status', x['status']) + f'<p>{E(x["assessment"])}</p></article>'
                         for x in c['incident_components'])
    timeline = ''.join(f'<li id="{x["id"]}"><h3>{x["id"]} / {E(x["actor"])}</h3>' +
                       paragraph('Available evidence', x['available_evidence']) +
                       paragraph('Event', x['event']) + paragraph('Assessment', x['interpretation']) + '</li>'
                       for x in c['event_chronology'])
    quotes = ''.join(f'<figure id="{q["id"]}"><figcaption><b>{q["id"]} / {E(q["kind"])}</b> '
                     f'({E(q["language"])})</figcaption><blockquote><p>{E(q.get("text", q.get("paraphrase", "")))}</p>'
                     f'</blockquote><p class="note">{E(q["provenance"])}</p></figure>' for q in c['transcript_excerpts'])
    claims = table(['Claim', 'Evidence status', 'Basis', 'Limit'], [
        [x['id'] + ': ' + x['claim'], x['verdict'], x['basis'], x['limit']] for x in c['claim_audit']])
    evidence = ''.join(f'<article id="{x["id"]}"><h3>{x["id"]} / {E(x["status"])}</h3>' +
                       paragraph('Source', x['pointer']) +
                       (paragraph('Claim', x['claim']) if x.get('claim') else '') +
                       (f'<blockquote><p>{E(x["quote"])}</p></blockquote>' if x.get('quote') else '') +
                       f'<p>{E(x["observation"])}</p>' +
                       (paragraph('Limit', x['limit']) if x.get('limit') else '') + '</article>'
                       for x in c['evidence'])
    findings = ''.join('<article><h3>' + E(x['mode']) + '</h3>' +
                       paragraph('Assessment', x['verdict'] + ' / ' + x['status']) +
                       f'<p>{E(x["finding"])}</p><p class="note">Evidence: ' +
                       ', '.join(f'<a href="#{eid}">{eid}</a>' for eid in x['evidence']) +
                       f' · <a href="../index.html#{E(x["mode_id"])}">Catalogue entry</a></p></article>'
                       for x in c['findings'])
    checklist = table(['Other integrity check', 'Assessment'], [
        [x['check'], x['assessment']] for x in c['other_integrity_checks']])
    hypotheses = table(['Hypothesis', 'Status', 'Diagnostic evidence required', 'What is not established'], [
        [x['id'] + ': ' + x['hypothesis'], x['status'], x['evidence_needed'], x['not_supported']]
        for x in c['hypotheses']])
    controls = ''.join('<article>' + paragraph('Trigger', x['trigger']) +
                       paragraph('Proposed control', x['control']) +
                       (paragraph('Evidence to retain', x['retained_evidence']) if x.get('retained_evidence') else '') +
                       '</article>' for x in c['prevention_proposals'])
    fixtures = ''.join(f'<details id="R{i:02d}"><summary>R{i:02d} / {E(x["case"])}</summary>' +
                       paragraph('Fixture', x['input']) + paragraph('Expected behaviour', x['expected']) +
                       '<p class="note">Proposed fixture. No model execution or score is claimed.</p></details>'
                       for i, x in enumerate(c['proposed_regression_cases'], 1))
    corrections = ''.join('<li>' + paragraph('Revision ' + x['revision'], x['change']) +
                          paragraph('Why', x['reason']) + '</li>' for x in c['documentation_corrections'])
    analysis = ''.join(paragraph(k.replace('_', ' ').capitalize(), v) for k, v in c['behavioural_analysis'].items())
    better = ''.join('<article>' + paragraph(k.replace('_', ' ').capitalize(), v) + '</article>'
                     for k, v in c['expected_better_response'].items())
    accountability = ''.join(paragraph(k.replace('_', ' ').capitalize(), v) for k, v in c['accountability'].items())
    provenance = ''.join(paragraph(k.replace('_', ' ').capitalize(), v) for k, v in c['provenance'].items()
                         if isinstance(v, str))
    protocol = c['evaluation_protocol']
    content = f'''
<section id="summary"><h2>What this case establishes</h2>
<div class="notice"><p><strong>Advisory verdict: BLOCK the original explanation.</strong> The assistant presented an unsupported explanation of its own behaviour as fact. The user's later screenshot contradicted its description of the displayed message. The cause of the language discrepancy remains unresolved.</p><p>This is a same-context self-review, prompted and corrected by the user. It is not an independent audit, a reproduced incident, or a demonstration of a particular model or application mechanism.</p></div>
<div class="cards">{components}</div><p>{E(c['timing_limit'])}</p></section>
<section id="timeline"><h2>Chronology and evidence available at each step</h2><ol class="timeline">{timeline}</ol></section>
<section id="excerpts"><h2>Selected conversation evidence</h2><p>These are curated excerpts and descriptions. The Greek passage is manually transcribed from the screenshot, and its translation is not independent corroboration. The original screenshot and a raw message export are not publicly archived here.</p>{quotes}</section>
<section id="claims"><h2>Claim-by-claim audit</h2><p>CONFIRMED and REFUTED refer to the stated proposition within the available record. UNVERIFIABLE means that the supplied evidence cannot settle it, not that it is false. This table includes observed claims and alternative propositions being evaluated; it does not imply that every proposition was asserted by the assistant or the user.</p>{claims}</section>
<section id="analysis"><h2>The reporting failure</h2>{analysis}<h3>Counterfactual: a better response at each stage</h3>{better}</section>
<section id="modes"><h2>Failure-mode mapping</h2><p>The confirmed issue concerns evidential support and certainty. Psychological labels are operational analogies, not diagnoses of a conscious internal process. Several labels can describe the same incident; they are not independent observations.</p><div class="cards">{findings}</div>
<h3>Checks that should not be overclaimed</h3>{checklist}</section>
<section id="hypotheses"><h2>What could explain the language discrepancy?</h2><p>No hypothesis below has been established or assigned a probability. Different mechanisms could produce the observed discrepancy; an exact diagnosis requires message-linked diagnostic records.</p>{hypotheses}
<p>Useful next evidence would compare the original generated payload, server-stored message/version, client-received payload, and displayed text for the same event. This is a proposed diagnostic path, not access the assistant currently has or a request for public disclosure of private logs.</p></section>
<section id="search"><h2>What the local search did and did not test</h2><p>{E(c['search_record']['type'])}.</p><pre><code>{E(c['search_record']['command'])}</code></pre>
<p>Recorded exit code: <b>1</b>. Recorded standard output: empty. {E(c['search_record']['interpretation'])}</p>{bullets(c['search_record']['limitations'])}</section>
<section id="ledger"><h2>Evidence ledger</h2><div class="cards">{evidence}</div></section>
<section id="recovery"><h2>Recovery is not technical resolution</h2><div class="cards"><article><h3>Completed communication recovery</h3>{bullets(c['recovery']['completed'])}</article><article><h3>Still not completed</h3>{bullets(c['recovery']['not_completed'])}</article></div>
<p><b>Ethical commitments affected:</b> {E('; '.join(c['principles_affected']))}. Honesty requires distinguishing evidence from invention; accountability requires preserving the error and its correction. This record does not establish intent to deceive.</p></section>
<section id="controls"><h2>Proposed prevention controls</h2><p>These are design proposals, not changes to the project's governing rubric or controls already deployed.</p><div class="cards">{controls}</div><h3>Accountability and ownership</h3>{accountability}</section>
<section id="regressions"><h2>Twelve proposed regression fixtures</h2><p>These fixtures test future reporting discipline. They have not been executed as a model benchmark, and would not reproduce or explain the original language incident.</p>{fixtures}
<h3>Proposed evaluation protocol</h3>{paragraph('Fixtures', protocol['fixtures'])}{paragraph('Judging', protocol['judging'])}<h4>Metrics to collect</h4>{bullets(protocol['metrics'])}<h4>Records required for an actual run</h4>{bullets(protocol['execution_records_required'])}<p>{E(protocol['limitation'])}</p></section>
<section id="audit-of-audit"><h2>Corrections to the first case write-up</h2><p>The retrospective itself needs auditing. Version 1.1 narrows wording that could imply causal insight or require intent where the failure criterion does not.</p><ol>{corrections}</ol>
<p>The version 1.0 record is preserved in <a href="https://github.com/danlex/ethicalhive/pull/14">PR #14</a>, merged as <a href="https://github.com/danlex/ethicalhive/commit/7f99371471d3831ca45668b3075fb4eaea91c376">7f99371</a>. It is a prior version of the documentation, not a pre-incident capture of the original event.</p></section>
<section id="provenance"><h2>Provenance and reproducibility limits</h2>{provenance}<p>{E(c['public_evidence_limit'])}</p><p><a href="https://github.com/danlex/ethicalhive/blob/main/cases/self-evaluation-language-discrepancy-2026-11-06.json">Read the complete machine-readable case ledger →</a></p></section>
'''
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Unsupported self-explanation: the auditor audited | EthicalAI</title>
<meta name="description" content="A documented AI self-evaluation failure: ten chronological events, conflicting language evidence, unsupported causal claims, a bounded investigation and twelve proposed regression fixtures.">
<link rel="canonical" href="https://ethicalai.alexandrudan.com/experiments/self-evaluation-language-discrepancy.html">
<link rel="icon" href="../favicon.png"><meta name="theme-color" content="#161619">
<meta property="og:type" content="article"><meta property="og:title" content="Unsupported self-explanation: the auditor audited">
<meta property="og:description" content="The reporting error is established. The cause of the language discrepancy is not. Evidence, retraction, hypotheses and audit limitations.">
<meta property="og:image" content="https://ethicalai.alexandrudan.com/og-image.png">
<style>
:root{--ink:#202024;--muted:#59595f;--accent:#983018;--line:#dfdcd7;--bg:#faf9f6}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 system-ui,sans-serif}a{color:var(--accent);text-underline-offset:3px;overflow-wrap:anywhere}
a:focus-visible,summary:focus-visible{outline:3px solid #983018;outline-offset:4px}.skip{position:absolute;top:-80px;background:#fff;padding:14px;z-index:5}.skip:focus{top:0}
.wrap{max-width:1180px;margin:auto;padding:0 24px}nav{display:flex;flex-wrap:wrap;gap:12px 24px;padding:20px 0;font-size:14px}nav a{font-weight:650}
header{background:#161619;color:#f9f7f2;padding:40px 0 48px}header p{max-width:85ch;color:#d1ced3}h1{font-size:clamp(32px,5vw,56px);line-height:1.12;letter-spacing:-1px;max-width:23ch;margin:12px 0 22px}
.eyebrow{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#ffab98}section{padding:36px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}
h2{font-size:clamp(24px,3vw,34px);line-height:1.25;margin:0 0 20px}h3{font-size:19px;line-height:1.4;margin:0 0 14px}h4{margin-bottom:8px}p{margin:0 0 14px}
.notice{border-left:4px solid #983018;background:#f1e8df;padding:22px;margin:0 0 24px}.notice p:last-child{margin:0}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:22px 0}article{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px;min-width:0}article p:last-child{margin:0}
.timeline{padding-left:24px}.timeline li{padding:16px 0 20px 12px;border-bottom:1px solid var(--line)}.timeline h3{color:var(--accent)}
figure{margin:22px 0;background:#fff;border:1px solid var(--line);padding:22px;border-radius:12px}figcaption{font-size:14px;color:var(--muted)}blockquote{border-left:3px solid #b5a99b;padding-left:18px;margin:16px 0;font-size:16px}
.note{font-size:13px;color:var(--muted)}.table-scroll{overflow:auto;border:1px solid var(--line);background:#fff;border-radius:10px}table{width:100%;border-collapse:collapse;min-width:700px}th,td{padding:14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);font-size:14px}th{background:#eee9e1}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#222228;color:#f4f1ef;padding:20px;border-radius:10px;font-size:13px}ul{padding-left:24px}li{margin:8px 0}
details{padding:18px;background:#fff;border:1px solid var(--line);border-radius:10px;margin:12px 0}summary{font-weight:700;cursor:pointer}details p{margin:16px 0 0}footer{padding:30px 0 50px;font-size:13px;color:var(--muted)}
@media(max-width:700px){.cards{grid-template-columns:1fr}.wrap{padding:0 18px}article,figure{padding:18px}header{padding:28px 0}section{padding:28px 0}}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
</style></head><body><a class="skip" href="#summary">Skip to the case</a><div class="wrap"><nav aria-label="Case navigation"><a href="../index.html#self-eval">EthicalAI / Self-evaluation</a><a href="#timeline">Timeline</a><a href="#claims">Claims</a><a href="#hypotheses">Open hypotheses</a><a href="#regressions">Proposed tests</a></nav></div>
<header><div class="wrap"><p class="eyebrow">Self-evaluation: the auditor audited · 6 November 2026 · Version 1.1</p><h1>An unexplained language change.<br>An explanation without evidence.</h1><p>When asked why a progress message appeared in Greek, the assistant gave a confident one-character explanation. The user supplied a screenshot that contradicted it. This case records the error, the correction, and what remains unknown.</p></div></header><main class="wrap">''' + content + '''</main><footer class="wrap">Same-context retrospective · Original technical cause unresolved · Proposed tests not executed · <a href="../index.html#self-eval-language-discrepancy">Return to the homepage case summary</a></footer></body></html>
'''


def validate(c, page):
    assert c['version'] == '1.1'
    assert len(c['event_chronology']) == 10
    assert len(c['claim_audit']) == 10
    assert len(c['proposed_regression_cases']) == 12
    evidence_ids = {x['id'] for x in c['evidence']}
    assert len(evidence_ids) == len(c['evidence'])
    for f in c['findings']:
        assert set(f['evidence']).issubset(evidence_ids)
    HTMLParser().feed(page)
    ids = re.findall(r'\bid="([^"]+)"', page)
    assert len(ids) == len(set(ids)), 'Duplicate HTML ids'
    for target in re.findall(r'href="#([^"]+)"', page):
        assert target in ids, f'Broken case anchor: {target}'
    for tag in ('section', 'article', 'figure', 'table', 'details', 'blockquote'):
        assert len(re.findall(r'<' + tag + r'\b', page)) == page.count('</' + tag + '>'), tag


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='check the committed HTML matches the ledger')
    args = parser.parse_args()
    c = json.loads(CASE.read_text(encoding='utf-8'))
    page = render(c)
    validate(c, page)
    if args.check:
        assert OUT.read_text(encoding='utf-8') == page, 'Generated case page is stale'
        print('PASS: case structure, evidence references, anchors and generated-page consistency. Model regression fixtures were NOT executed.')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(page, encoding='utf-8')
        print(f'Built case version {c["version"]}: {OUT}')


if __name__ == '__main__':
    main()
