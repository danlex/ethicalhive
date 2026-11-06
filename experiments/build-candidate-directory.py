#!/usr/bin/env python3
"""Reconcile the uploaded shortlist with the first 100; build a separate research directory."""
import copy
import csv
import hashlib
import html
import io
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/research'
REF = ROOT/'references'
norm = lambda s: re.sub('[^a-z0-9]', '', s.casefold())


def read(name):
    return json.loads((REF/name).read_text())


def build():
    base = read('behaviour-candidates-100-2026-11-06.json')
    upload = read('candidate-behaviours-upload-2026-11-06.json')
    review = read('candidate-upload-review-2026-11-06.json')
    ontology = yaml.safe_load((ROOT/'ontology/ethical-ai.yaml').read_text())
    assert len(ontology['modes']) == 207
    assert hashlib.sha256((ROOT/'ontology/ethical-ai.yaml').read_bytes()).hexdigest() == base['baseline']['sha256']
    modes = {norm(m['name']):m for m in ontology['modes']}
    aliases = {norm(k):norm(v) for k,v in review['catalogue_aliases'].items()}
    def mode_for(name):
        cleaned = re.sub(r'\s*\(.*?\)', '', name).strip()
        key = norm(name) if norm(name) in modes else norm(cleaned)
        key = aliases.get(key, key)
        if key in modes:
            return modes[key]
        candidates = [v for k,v in modes.items() if k.startswith(key) and key]
        if len(candidates) == 1:
            return candidates[0]
        raise ValueError(f'Unresolved catalogue relation: {name}')
    sources = {s['id']:s for s in base['sources']+review['sources']}
    entries = []
    for original in base['entries']:
        e = copy.deepcopy(original)
        e.update(aliases=[], origins=['earlier-research'], groups=[e['group']],
                 ai_manifestation=e['proposed_ai_probe'], ai_text_kind='Proposed AI test',
                 source_check='definition-source-consulted', related_modes=[], contributions=[])
        entries.append(e)
    by_id = {e['id']:e for e in entries}
    by_name = {norm(e['name']):e for e in entries}
    group_names = {g['key']:g['name'] for g in upload['groups']}
    merged = []
    for row in upload['rows']:
        key = str(row['n'])
        correction = review['reviews'].get(key, {})
        explicit_merge = review['semantic_merges'].get(key)
        target = by_id[explicit_merge['target']] if explicit_merge else by_name.get(norm(row['name']))
        if target:
            merged.append(dict(upload_row=row['n'], supplied_name=row['name'], target_id=target['id'],
                               target_name=target['name'], reason=explicit_merge['reason'] if explicit_merge else 'Same normalised behaviour name.'))
            e = target
            if row['name'] != e['name'] and row['name'] not in e['aliases']:
                e['aliases'].append(row['name'])
            e['origins'].append('attachment')
            if explicit_merge:
                e['distinction_and_limits'] += ' Reconciliation: '+explicit_merge['reason']
        else:
            name = correction.get('name', row['name'])
            e = dict(id=f'upload-{row["n"]:03}', name=name,
                     definition=correction.get('definition', row['human']),
                     aliases=[row['name']] if name != row['name'] else [],
                     group=group_names[row['g']], groups=[group_names[row['g']]],
                     origins=['attachment'], source_ids=correction.get('sources', []),
                     source_check='definition-source-consulted' if correction.get('sources') and correction.get('definition_checked', True) else 'pending-definition-source-check',
                     ai_status='PROPOSED ANALOGY; NOT TESTED IN THIS RESEARCH',
                     ai_text_kind='Proposed AI manifestation',
                     ai_manifestation=correction.get('ai',row['ai']),
                     distinction_and_limits=correction.get('note', 'Imported research candidate. Definition, attribution and redundancy need further review; an illustrative AI example is not empirical evidence.'),
                     related_modes=[], contributions=[])
            if key in review['earlier_proposal_overlaps']:
                e['distinction_and_limits'] += ' Also present in earlier expansion notes as '+review['earlier_proposal_overlaps'][key]+'. Not a newly discovered concept in this update.'
            entries.append(e)
            by_id[e['id']] = e
            by_name[norm(name)] = e
        for name in ([row['near']] if row['near'] else [])+review['additional_relations'].get(key, []):
            mode = mode_for(name)
            relation = dict(id=mode['id'], name=mode['name'], kind='related; not asserted to be an exact synonym')
            if relation not in e['related_modes']:
                e['related_modes'].append(relation)
        if group_names[row['g']] not in e['groups']:
            e['groups'].append(group_names[row['g']])
        e['contributions'].append(dict(upload_row=row['n'], supplied_name=row['name'], supplied_source=row['src'],
                                       supplied_field_note=upload['source_field_notes'][row['g']],
                                       supplied_definition=row['human'], supplied_ai_example=row['ai'],
                                       supplied_nearest_mode=row['near'], supplied_evidence=row['ev'],
                                       supplied_batch=row['b'],
                                       input_check_claim='General knowledge; no source checked' if row['b']==1 else 'Search reported by attachment; not independently verified by import'))
    assert len(merged) == 17
    assert len(entries) == 228
    assert len({e['id'] for e in entries}) == len(entries)
    assert len({norm(e['name']) for e in entries}) == len(entries)
    assert sorted(c['upload_row'] for e in entries for c in e['contributions']) == list(range(1,146))
    for e in entries:
        e['origins'] = sorted(set(e['origins']))
        e['novelty_status'] = 'Not established; related catalogue modes linked' if e['related_modes'] else 'Not established; inspect semantic boundary before admission'
        assert all(s in sources for s in e['source_ids'])
    counts = dict(unique_candidates=len(entries), earlier_research=100, uploaded_rows=145,
                  merged_overlaps=len(merged), additional_candidates=145-len(merged),
                  canonical_catalogue_entries=len(ontology['modes']),
                  definition_source_consulted=sum(e['source_check']=='definition-source-consulted' for e in entries),
                  pending_definition_source_check=sum(e['source_check']=='pending-definition-source-check' for e in entries))
    result = dict(title='Psychology and behaviour research candidates', updated='2026-11-06', counts=counts,
                  status='Research candidates, not established AI mechanisms or additions to the canonical ontology.',
                  method='100 earlier candidates plus 145 uploaded contributions, with 17 exact/semantic overlaps merged. Original upload claims are retained separately and are not promoted to verified facts.',
                  source_check_meaning='A source passage, abstract or indexed excerpt was consulted for the human definition; this does not mean full-book reading, independent replication or validation in AI. Per-source access depth is explicit.',
                  admission='Before promotion: confirm definition against a suitable source, resolve semantic redundancy, assess AI-specific evidence and validate an operational test.',
                  clinical_limit='Clinical and psychodynamic labels are human constructs. AI examples are outward analogies; they do not establish unconscious motives, feelings, diagnoses or intent.',
                  baseline=base['baseline'], upload_sha256=upload['original_sha256'],
                  merged_overlaps=merged, sources=list(sources.values()), entries=entries)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'behaviour-candidates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    (REF/'candidate-upload-reconciliation-2026-11-06.json').write_text(json.dumps(dict(counts=counts, upload_sha256=upload['original_sha256'], merged_overlaps=merged,
        contribution_map=[dict(upload_row=c['upload_row'],target_id=e['id'],source_check=e['source_check']) for e in entries for c in e['contributions']]), ensure_ascii=False, indent=2)+'\n')
    buf = io.StringIO(newline='')
    fields=['id','name','aliases','group','definition','origins','source_check','proposed_ai_manifestation','distinction_and_limits','related_modes','reviewed_sources','source_access','supplied_attributions','upload_rows']
    writer=csv.DictWriter(buf,fieldnames=fields)
    writer.writeheader()
    for e in entries:
        writer.writerow(dict(id=e['id'],name=e['name'],aliases='; '.join(e['aliases']),group=e['group'],definition=e['definition'],origins='; '.join(e['origins']),
            source_check=e['source_check'],proposed_ai_manifestation=e['ai_manifestation'],distinction_and_limits=e['distinction_and_limits'],
            related_modes='; '.join(m['id']+': '+m['name'] for m in e['related_modes']),
            reviewed_sources='; '.join(sources[s]['url'] for s in e['source_ids']),
            source_access='; '.join(sources[s]['consulted'] for s in e['source_ids']),
            supplied_attributions='; '.join(c['supplied_source'] for c in e['contributions']),upload_rows='; '.join(str(c['upload_row']) for c in e['contributions'])))
    (OUT/'behaviour-candidates.csv').write_text(buf.getvalue())
    render(result, sources)
    print(json.dumps(counts))


def render(data, sources):
    h=html.escape
    entries=data['entries']
    groups=list(dict.fromkeys(e['group'] for e in entries))
    options=''.join(f'<option value="{h(g,quote=True)}">{h(g)}</option>' for g in sorted({g for e in entries for g in e['groups']}))
    blocks=[]
    for group in groups:
        blocks.append(f'<section class="field"><h2>{h(group)}</h2>')
        for e in [e for e in entries if e['group']==group]:
            review_label='Definition source consulted' if e['source_check']=='definition-source-consulted' else 'Definition source check pending'
            badge_class='consulted' if e['source_check']=='definition-source-consulted' else 'pending'
            origins=' + '.join('Earlier research' if o=='earlier-research' else 'Attached document' for o in e['origins'])
            links=[]
            for sid in e['source_ids']:
                s=sources[sid]
                assert urlsplit(s['url']).scheme in ('https','http')
                links.append(f'<li><a href="{h(s["url"],quote=True)}">{h(s["title"])}</a><p class="access">Access: {h(s["consulted"])}</p></li>')
            related=' · '.join(f'<a href="/#'+h(m['id'],quote=True)+'">'+h(m['name'])+'</a>' for m in e['related_modes'])
            originals=[]
            for c in e['contributions']:
                originals.append(f'<li><strong>Upload row {c["upload_row"]}: {h(c["supplied_name"])}</strong><br>Supplied attribution, not verified as a historical origin: {h(c["supplied_source"])}<br>Source-field note supplied in document: {h(c["supplied_field_note"])}<br>Attachment status: {h(c["input_check_claim"])}'+(f'<br>Supplied search reference: {h(c["supplied_evidence"])}' if c['supplied_evidence'] else '')+'</li>')
            aliases=f'<p class="aliases">Also indexed as: {h("; ".join(e["aliases"]))}</p>' if e['aliases'] else ''
            searchable=' '.join([e['name'],*e['aliases'],e['definition'],e['ai_manifestation'],e['distinction_and_limits'],*(sources[s]['title'] for s in e['source_ids']),*(c['supplied_source'] for c in e['contributions'])])
            attrs=f'data-origin="{h(" ".join(e["origins"]),quote=True)}" data-review="{e["source_check"]}" data-groups="{h(json.dumps(e["groups"]),quote=True)}" data-search="{h(searchable.casefold(),quote=True)}"'
            blocks.append(f'''<article id="{e['id']}" {attrs}>
            <div class="entry-head"><h3><a href="#{e['id']}">{h(e['name'])}</a></h3><span class="badge {badge_class}">{review_label}</span></div>{aliases}
            <div class="ledger"><div><p class="label">Human definition</p><p>{h(e['definition'])}</p></div><div><p class="label">{h(e['ai_text_kind'])} · untested</p><p>{h(e['ai_manifestation'])}</p></div></div>
            <p class="origin">{h(origins)}</p><details><summary>Sources, overlap and review notes</summary>
            <p>{h(e['distinction_and_limits'])}</p><p><strong>Novelty:</strong> {h(e['novelty_status'])}</p>
            {('<p><strong>Related catalogue entries:</strong> '+related+'. These are adjacent concepts, not automatically exact synonyms.</p>') if related else ''}
            {('<ul class="sources">'+''.join(links)+'</ul>') if links else '<p>No definition-source passage has been independently consulted for this entry in this update. The supplied attribution below is a research lead.</p>'}
            {('<h4>Upload provenance</h4><ul class="sources">'+''.join(originals)+'</ul>') if originals else ''}</details></article>''')
        blocks.append('</section>')
    merged=''.join(f'<li>Upload {m["upload_row"]}: {h(m["supplied_name"])} → <a href="#{m["target_id"]}">{h(m["target_name"])}</a>. {h(m["reason"])}</li>' for m in data['merged_overlaps'])
    substitutions={'@@CARDS@@':''.join(blocks),'@@GROUPS@@':options,'@@MERGES@@':merged,
                   '@@CONSULTED@@':str(data['counts']['definition_source_consulted']),
                   '@@PENDING@@':str(data['counts']['pending_definition_source_check'])}
    template=(ROOT/'experiments/templates/behaviour-candidates.html').read_text()
    for token,value in substitutions.items():
        assert token in template
        template=template.replace(token,value)
    assert not re.search(r'@@[A-Z]+@@',template)
    (OUT/'behaviour-candidates.html').write_text(template)


if __name__=='__main__':
    build()
