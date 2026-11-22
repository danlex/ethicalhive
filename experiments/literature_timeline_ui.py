"""Progressive timeline placeholders; annual counts are a separate search snapshot."""
from html import escape


def timeline_placeholder(mode):
    return (
        '<section class="literature-timeline" data-timeline-term="'+escape(mode['id'], quote=True)+'">'
        '<h4>Research timeline</h4>'
        '<p class="timeline-description">Matching arXiv publications by year of first submission · cs.AI, cs.CL and cs.LG.</p>'
        '<div class="timeline-mount"></div>'
        '<p class="timeline-downloads"><a href="literature-timelines.csv" download>Download yearly data · CSV</a>'
        ' · <a href="literature-timelines.json" download>JSON and source queries</a></p>'
        '<noscript><p>Enable JavaScript to explore the chart, or download the yearly data above. The catalogue and its sources remain readable.</p></noscript>'
        '</section>'
    )


def overview_placeholder():
    return (
        '<section class="literature-timeline literature-overview" id="research-timeline" aria-labelledby="research-timeline-title">'
        '<h3 id="research-timeline-title">Research over time</h3>'
        '<p>Explore yearly arXiv search matches across the catalogue, or compare individual terms.</p>'
        '<p class="timeline-note">Combined values count paper–term matches: a paper matching several searches is counted in each. '
        'They are not a total of unique publications or a measure of how often AI exhibits a behaviour.</p>'
        '<div class="overview-mount"></div>'
        '<p class="timeline-downloads"><a href="literature-timelines.csv" download>Download yearly data · CSV</a>'
        ' · <a href="literature-timelines.json" download>JSON and source queries</a></p>'
        '<noscript><p>Enable JavaScript to explore the chart, or download the yearly data above.</p></noscript>'
        '</section>'
    )


def timeline_assets(html):
    css='<link rel="stylesheet" href="assets/literature-timelines.css">'
    js='<script defer src="assets/literature-timelines.js"></script>'
    if css not in html: html=html.replace('</head>',css+'\n</head>',1)
    if js not in html: html=html.replace('</body>',js+'\n</body>',1)
    if 'id="research-timeline"' not in html:
        marker='    <div class="cat-legend">'
        if marker not in html: raise ValueError('Cannot find the catalogue timeline position')
        html=html.replace(marker,'    '+overview_placeholder()+'\n'+marker,1)
    return html
