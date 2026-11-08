"""Shared source classification; bibliography is distinct from AI evidence."""
PAPER_TYPES = {'journal-article', 'proceedings-article', 'posted-content'}


def definition_sources(mode):
    seen = set()
    for record in [mode, *mode.get('research_notes', [])]:
        for source in record.get('definition_sources', []):
            if source['url'] not in seen:
                seen.add(source['url'])
                yield source


def research_papers(mode):
    return [source for source in definition_sources(mode)
            if source.get('publication', {}).get('type') in PAPER_TYPES]


def source_coverage(mode):
    papers = research_papers(mode)
    ai = (mode.get('arxiv') or {}).get('papers') or []
    references = [s for s in definition_sources(mode) if s not in papers]
    contributions = mode.get('research_provenance', {}).get('contributions', [])
    status = ('paper-links-available' if papers or ai else
              'reference-sources-only' if references else
              'supplied-attributions-only' if contributions else 'no-linked-source')
    return {'id': mode['id'], 'num': mode['num'], 'name': mode['name'],
            'ai_paper_links': len(ai), 'human_related_paper_links': len(papers),
            'reference_source_links': len(references), 'coverage_status': status,
            'source_check': mode.get('source_check', ''),
            'ai_evidence_status': mode.get('ai_evidence_status', ''),
            'ai_paper_urls': ['https://arxiv.org/abs/' + p['id'] for p in ai],
            'human_related_paper_urls': [s['url'] for s in papers],
            'reference_source_urls': [s['url'] for s in references]}
