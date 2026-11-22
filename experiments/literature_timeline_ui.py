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


def timeline_assets(html):
    css='<link rel="stylesheet" href="assets/literature-timelines.css">'
    js='<script defer src="assets/literature-timelines.js"></script>'
    if css not in html: html=html.replace('</head>',css+'\n</head>',1)
    if js not in html: html=html.replace('</body>',js+'\n</body>',1)
    return html
