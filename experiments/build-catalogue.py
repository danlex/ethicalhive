#!/usr/bin/env python3
"""build-catalogue.py - regenerate the 100-mode catalogue grid on the EthicalAI
page from the neuroscience-parallels corpus, so every entry shows its definition
and nothing is hand-transcribed or invented.

Reads references/research-2026-05-23-neuroscience-parallels.md (the source of
truth for the 100 failure modes, their brain-system grouping, honesty tag, and
one-line definition) and emits the `<div class="cat-grid">...</div>` block.

Usage:
  experiments/build-catalogue.py            # print the grid HTML to stdout
  experiments/build-catalogue.py --write     # splice it into docs/index.html

The splice replaces the existing cat-grid in place (reversible via git).
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "references" / "research-2026-05-23-neuroscience-parallels.md"
PAGE = ROOT / "docs" / "index.html"
CITES = ROOT / "experiments" / "catalogue-citations.tsv"
EXAMPLES = ROOT / "experiments" / "catalogue-examples.tsv"
PAPERS = ROOT / "experiments" / "catalogue-papers.json"
SUPPRESS = ROOT / "experiments" / "catalogue-papers-suppress.txt"
SHIPPED = ROOT / "experiments" / "shipped-check-papers.json"
EXTRA = ROOT / "experiments" / "catalogue-extra.tsv"
EXTRA_GROUP = "Agentic and engineering failure modes (beyond the brain map)"

ENTRY_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+`(page|research|analogy)`\s+(.+)$")
SECTION_RE = re.compile(r"^##\s+\d+\.\s+(.+?)\s*$")


def load_cites():
    """num -> (count:int, arxivid, year, anchor). Empty if the file is absent."""
    cites = {}
    if not CITES.exists():
        return cites
    for line in CITES.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        num = int(parts[0])
        count = int(parts[1])
        arxivid = parts[2].strip()
        year = parts[3].strip() if len(parts) > 3 else ""
        anchor = parts[4].strip() if len(parts) > 4 else ""
        cites[num] = (count, arxivid, year, anchor)
    return cites


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def title_amp(title):
    # match the page's existing header style: " and " -> " & "
    return esc(title).replace(" and ", " &amp; ")


def load_examples():
    """num -> illustrative example string. Empty if the file is absent."""
    ex = {}
    if not EXAMPLES.exists():
        return ex
    for line in EXAMPLES.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        num, text = line.split("\t", 1)
        ex[int(num)] = text.strip()
    return ex


def load_papers():
    """num -> {count, papers:[{id,year,title}]}. Empty if the file is absent."""
    if not PAPERS.exists():
        return {}
    raw = json.loads(PAPERS.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def load_extra():
    """[(num, name, tag, definition)] of behaviours outside the brain corpus."""
    rows = []
    if not EXTRA.exists():
        return rows
    for line in EXTRA.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        rows.append((int(parts[0]), parts[1].strip(), parts[2].strip(), parts[3].strip()))
    return rows


def load_suppress():
    """Set of nums to render as 'no direct paper' (off-topic / homonym queries)."""
    s = set()
    if not SUPPRESS.exists():
        return s
    for line in SUPPRESS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            s.add(int(line))
    return s


def parse():
    sections = []  # list of (title, [ (num, name, tag, definition), ... ])
    current = None
    for line in CORPUS.read_text(encoding="utf-8").splitlines():
        sm = SECTION_RE.match(line)
        if sm:
            current = (sm.group(1), [])
            sections.append(current)
            continue
        em = ENTRY_RE.match(line)
        if em and current is not None:
            num, name, tag, definition = em.groups()
            current[1].append((int(num), name.strip(), tag, definition.strip()))
    return sections


def render_papers(pdata):
    """count + top-3 papers HTML, or an honest 'no paper' note."""
    if not pdata or not pdata.get("papers"):
        return '<p class="cite none">No direct AI paper found yet.</p>'
    count = pdata.get("count")
    cnt = f"{count:,}" if isinstance(count, int) else "?"
    items = []
    for p in pdata["papers"][:3]:
        pid = re.sub(r"v\d+$", "", p.get("id", ""))
        yr = f' ({p["year"]})' if p.get("year") else ""
        items.append(
            f'<li><a href="https://arxiv.org/abs/{pid}" target="_blank" '
            f'rel="noopener">arXiv:{pid}</a>{yr} {esc(p.get("title", ""))}</li>'
        )
    return (
        f'<p class="cite"><b>{cnt}</b> arXiv papers (cs.AI/CL/LG)</p>'
        f'<ul class="papers">{"".join(items)}</ul>'
    )


def papers_block(num, papers, suppress):
    if num in suppress:
        return render_papers(None)
    return render_papers(papers.get(num))


def inject_shipped(html, shipped):
    """Add a Research papers section after the Examples list of each shipped-check
    deep block. Idempotent: skips a block that already has one."""
    done = 0
    for cid, pdata in shipped.items():
        block = f'\n      <h4>Research papers</h4>\n      {render_papers(pdata)}'
        pattern = re.compile(
            r'(<details id="' + re.escape(cid) + r'"[^>]*>.*?<ul class="examples">.*?</ul>)'
            r'(?!\s*<h4>Research papers)',
            re.DOTALL,
        )
        html, n = pattern.subn(lambda m: m.group(1) + block, html, count=1)
        done += n
    return html, done


SHIPPED_CHECKS = ROOT / "experiments" / "shipped-checks.tsv"


def load_shipped_checks():
    """[(seq, id, name, definition, example)] for the prioritised first group."""
    rows = []
    if not SHIPPED_CHECKS.exists():
        return rows
    for line in SHIPPED_CHECKS.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        rows.append((int(parts[0]), parts[1].strip(), parts[2].strip(),
                     parts[3].strip(), parts[4].strip()))
    return rows


def render_shipped(rows, shipped_papers):
    """Prioritised, red-bordered first group of highlighted checks."""
    out = ['      <h3 class="cat-group">Highlighted checks</h3>']
    for seq, cid, name, definition, example in rows:
        n = f"{seq:02d}"
        key = esc(name.lower())
        ex_html = (
            f'<h4>Example</h4><ul class="examples"><li>{esc(example)}</li></ul>'
            if example else ""
        )
        out.append(
            f'      <details class="concept shipped" data-fam="page" data-key="{key}">'
            f'<summary><span class="num">{n}</span>'
            f'<div class="head"><h2>{esc(name)}</h2>'
            f'<p class="one">{esc(definition)}</p>'
            f'<span class="fam">Highlighted check</span></div>'
            f'<span class="chev">▸</span></summary>'
            f'<div class="body">{ex_html}'
            f"<h4>Research papers</h4>{render_papers(shipped_papers.get(cid))}"
            f"</div></details>"
        )
    return "\n".join(out)


def render_numbered(sections, cites, examples, papers, suppress):
    """Render every concept as an expandable .concept box (same design as the
    original shipped-check blocks), grouped by brain system / extra group."""
    out = ['    <div class="cat-grid">']
    for i, (title, entries) in enumerate(sections, 1):
        fam = title_amp(title)
        out.append(f'      <h3 class="cat-group">{i}. {fam}</h3>')
        for num, name, tag, definition in entries:
            n = f"{num:02d}"
            key = esc(name.lower())
            ex = examples.get(num)
            ex_html = (
                f'<h4>Example</h4><ul class="examples"><li>{esc(ex)}</li></ul>'
                if ex
                else ""
            )
            out.append(
                f'      <details class="concept {tag}" data-fam="{tag}" data-key="{key}">'
                f'<summary><span class="num">{n}</span>'
                f'<div class="head"><h2>{esc(name)}</h2>'
                f'<p class="one">{esc(definition)}</p>'
                f'<span class="fam">{fam}</span></div>'
                f'<span class="chev">▸</span></summary>'
                f'<div class="body">{ex_html}'
                f"<h4>Research papers</h4>{papers_block(num, papers, suppress)}"
                f"</div></details>"
            )
    out.append("    </div>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="splice into docs/index.html")
    args = ap.parse_args()

    sections = parse()
    extra = load_extra()
    if extra:
        sections.append((EXTRA_GROUP, extra))
    cites = load_cites()
    examples = load_examples()
    papers = load_papers()
    suppress = load_suppress()
    shipped_rows = load_shipped_checks()
    shipped_papers = json.loads(SHIPPED.read_text(encoding="utf-8")) if SHIPPED.exists() else {}
    total = sum(len(e) for _, e in sections) + len(shipped_rows)
    print(
        f"rendering {total} entries "
        f"({len(shipped_rows)} highlighted, {len(extra)} beyond the brain corpus)",
        file=sys.stderr,
    )
    grid = render_numbered(sections, cites, examples, papers, suppress)
    if shipped_rows:
        grid = grid.replace(
            '    <div class="cat-grid">',
            '    <div class="cat-grid">\n' + render_shipped(shipped_rows, shipped_papers),
            1,
        )

    if not args.write:
        print(grid)
        return

    html = PAGE.read_text(encoding="utf-8")
    # Splice the catalogue grid. Anchor on either the mindmap (first run) or the
    # section close (later runs, after the mindmap is pruned) so it stays idempotent.
    pattern = re.compile(
        r'    <div class="cat-grid">.*?</div>\s*(?=<details class="mm">|</section>)',
        re.DOTALL,
    )
    if not pattern.search(html):
        print("ERROR: could not locate cat-grid to replace", file=sys.stderr)
        sys.exit(1)
    html = pattern.sub(grid + "\n    ", html, count=1)

    # Single uniform style: the 100-entry catalogue is the only concept list.
    # Prune the legacy 14 deep-block section (with its now-orphaned "how a judge"
    # blurb and family filter) and the AI Integrity Contract section. Idempotent:
    # a no-op once they are gone.
    had_main = "<main id=\"list\">" in html
    html = re.sub(
        r'<div class="framework" id="framework">.*?</main>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    had_contract = 'id="contract"' in html
    html = re.sub(
        r'<section class="framework" id="contract">.*?</section>\s*',
        "",
        html,
        flags=re.DOTALL,
    )

    # Remove the Mermaid mindmap (unreadable at 100+ nodes, redundant with the
    # boxes) and its external script, keeping the page self-contained.
    had_mm = 'class="mm"' in html
    html = re.sub(r'\s*<details class="mm">.*?</details>', "", html, flags=re.DOTALL)
    html = re.sub(
        r'\s*<script defer src="https://cdn\.jsdelivr\.net/npm/mermaid[^"]*"></script>',
        "",
        html,
    )
    html = re.sub(
        r'\s*<script>\s*\(function\(\)\{\s*var d=document\.querySelector\("details\.mm".*?</script>',
        "",
        html,
        flags=re.DOTALL,
    )

    PAGE.write_text(html, encoding="utf-8")
    print(
        f"spliced {total} entries; pruned 14-block: {had_main}; "
        f"contract: {had_contract}; mindmap: {had_mm}"
    )


if __name__ == "__main__":
    main()
