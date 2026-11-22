"""Render the charter and evaluation categories from their canonical sources."""
from collections import Counter
from html import escape
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]


def framework():
    charter = (ROOT / 'contracts/ethical-principles.md').read_text()
    ethical = []
    for match in re.finditer(r'^## ([1-6])\. (.+)\n\n(.*?)(?=^## |\Z)', charter, re.M | re.S):
        ethical.append({'name': match[2], 'statement': ' '.join(match[3].split())})
    if len(ethical) != 6:
        raise ValueError('The normative charter must contain six numbered principles')
    ontology = yaml.safe_load((ROOT / 'ontology/ethical-ai.yaml').read_text())
    categories = ontology['principles']
    known = {p['id'] for p in categories}
    counts = Counter()
    for mode in ontology['modes']:
        labels = mode.get('violates', [])
        if len(labels) != 1 or labels[0] not in known:
            raise ValueError(f"Expected one known primary evaluation label: {mode['id']}")
        counts[labels[0]] += 1
    if len(categories) != 7 or sum(counts.values()) != len(ontology['modes']):
        raise ValueError('Evaluation counts must cover the catalogue exactly once')
    return ethical, [{**p, 'count': counts[p['id']]} for p in categories]


def render_framework():
    ethical, categories = framework()
    romans = ('I', 'II', 'III', 'IV', 'V', 'VI')
    cards = '\n'.join(
        f'      <div class="cx-card{" key" if i == 5 else ""}"><p class="idx">{romans[i]}</p>'
        f'<h3>{escape(p["name"])}</h3><p>{escape(p["statement"])}</p></div>'
        for i, p in enumerate(ethical))
    principles = f'''<section class="cx-sec" id="principles">
  <div class="cx-in">
    <span class="cx-badge">The charter</span>
    <h2 class="cx-h2">Six Ethical Principles for AI Systems</h2>
    <p class="cx-sub">These principles state the commitments the project asks AI systems to uphold.</p>
    <div class="cx-cards">
{cards}
    </div>
    <p class="cx-more"><a href="https://github.com/danlex/ethicalhive/blob/main/contracts/ethical-principles.md" target="_blank" rel="noopener">Read the full charter →</a> · <a href="#evaluation-categories">See the seven evaluation categories</a></p>
  </div>
</section>'''
    evaluation_cards = '\n'.join(
        f'      <div class="cx-card" data-principle="{escape(p["id"])}">'
        f'<h3>{escape(p["name"])} ({p["count"]})</h3><p>{escape(p["statement"])}</p></div>'
        for p in categories)
    evaluation = f'''<section class="cx-sec" id="evaluation-categories">
  <div class="cx-in">
    <span class="cx-badge">Evaluation</span>
    <h2 class="cx-h2">Seven Categories for Evaluating AI Behavior</h2>
    <p class="cx-sub">These categories describe what to check in an AI response or action. Counts show catalogue records assigned to each category, using one primary label per record. They are separate from the eleven categories used to browse the catalogue and do not count papers or independently validated mechanisms.</p>
    <div class="cx-cards">
{evaluation_cards}
    </div>
    <p class="cx-more"><a href="paper/ontology-paper.html">Read the ontology paper →</a> · <a href="#catalogue">Browse all {sum(p['count'] for p in categories)} catalogue records</a></p>
  </div>
</section>'''
    return principles, evaluation
