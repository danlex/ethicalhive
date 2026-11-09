"""Shared source classification; bibliography is distinct from AI evidence."""
import re

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


def paper_identifier(url):
    """Normalize publication identity without treating cited-by totals as works."""
    value=url.strip().lower()
    if 'arxiv.org/abs/' in value or 'arxiv.org/pdf/' in value:
        return 'arxiv:'+re.sub(r'(v\d+)?(\.pdf)?$', '', re.split(r'arxiv.org/(?:abs|pdf)/', value)[-1])
    if 'doi.org/' in value:
        doi=re.sub(r'/+','/',value.split('doi.org/',1)[1])
        if doi.startswith('10.48550/arxiv.'):
            return 'arxiv:'+re.sub(r'v\d+$','',doi.split('10.48550/arxiv.',1)[1])
        return 'doi:'+doi
    return value.rstrip('/')


def available_papers(mode):
    """Normalize the stored bibliography; the legacy source records stay intact."""
    papers=[]
    for p in (mode.get('arxiv') or {}).get('papers') or []:
        url='https://arxiv.org/abs/'+p['id']
        papers.append(dict(id=paper_identifier(url),title=p['title'],year=int(p['year']),
            url=url,domain='ai',venue='arXiv',authors=p.get('authors',[]),
            relevance=p.get('relevance','Existing AI bibliography entry; its inclusion is not a fresh relevance or empirical-evidence review.'),
            consulted=p.get('consulted','Previously stored arXiv citation; no new reading claimed.'),
            verification_url=p.get('verification_url',url),
            source_reference={'collection':'arxiv','id':p['id']}))
    for source in research_papers(mode):
        publication=source['publication']
        identity='https://doi.org/'+publication['doi'] if publication.get('doi') else source['url']
        papers.append(dict(id=paper_identifier(identity),title=source['title'],year=publication['year'],
            url=source['url'],domain='human-related',venue=publication['venue'],authors=publication['authors'],
            relevance=publication['evidence_scope'],consulted=source['consulted'],
            verification_url=publication['verification_url'],
            source_reference={'collection':'definition_sources','id':source['id']}))
    unique={};titles=set()
    for paper in papers:
        title=re.sub(r'\W+','',paper['title'].casefold())
        if paper['id'] not in unique and title not in titles:
            unique[paper['id']]=paper;titles.add(title)
    return list(unique.values())


def selected_papers(mode):
    """Three representative citations are independent of the literature total."""
    return mode.get('selected_papers', available_papers(mode)[:3])


def literature_search(mode):
    search=mode.get('literature_search')
    if search is not None:return search
    return {'database':'arXiv','count':None,'status':'not-searched',
            'query':'','queried_at':'','url':'','scope':'No search total recorded.'}


def source_coverage(mode):
    selected=selected_papers(mode)
    papers = [p for p in selected if p['domain']=='human-related']
    ai = [p for p in selected if p['domain']=='ai']
    references = [s for s in definition_sources(mode) if s.get('publication',{}).get('type') not in PAPER_TYPES]
    search=literature_search(mode)
    contributions = mode.get('research_provenance', {}).get('contributions', [])
    status = ('paper-links-available' if papers or ai else
              'reference-sources-only' if references else
              'supplied-attributions-only' if contributions else 'no-linked-source')
    return {'id': mode['id'], 'num': mode['num'], 'name': mode['name'],
            'ai_paper_links': len(ai), 'human_related_paper_links': len(papers),
            'reference_source_links': len(references), 'coverage_status': status,
            'source_check': mode.get('source_check', ''),
            'ai_evidence_status': mode.get('ai_evidence_status', ''),
            'ai_paper_urls': [p['url'] for p in ai],
            'human_related_paper_urls': [s['url'] for s in papers],
            'reference_source_urls': [s['url'] for s in references],
            'literature_match_count':search['count'],'literature_database':search['database'],
            'literature_query':search['query'],'literature_queried_at':search['queried_at'],
            'literature_search_status':search['status'],'literature_search_url':search['url'],
            'selected_paper_count':len(selected),'selected_paper_target':3,
            'selected_paper_shortfall':max(0,3-len(selected))}
