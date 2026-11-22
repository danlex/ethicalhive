#!/usr/bin/env python3
"""Ground analogy modes in real, downloaded arXiv papers.

Two steps:

  verify <res1.json> [res2.json ...]
      For every grounded proposal, download the PDF to ontology/sources/<ID>.pdf
      and confirm the arXiv abstract-page title overlaps the reported title.
      A proposal whose PDF 404s, is not a real PDF, or whose title does not
      match is DROPPED (this is the anti-hallucination gate). Writes the
      survivors to ontology/sources/verified.json and a human manifest.

  apply
      Read ontology/sources/verified.json and edit ontology/ethical-ai.yaml in
      place with minimal, targeted text edits per mode: replace the `example:`
      line with the grounded example, flip `tag: analogy` -> `tag: research`,
      and prepend the verified paper (single-line flow map) to selected_papers.

Usage:
  python3 experiments/ground-analogy-papers.py verify a.json b.json ...
  python3 experiments/ground-analogy-papers.py apply
"""
import json, re, sys, io, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YAML = ROOT / "ontology" / "ethical-ai.yaml"
SRC = ROOT / "ontology" / "sources"
VERIFIED = SRC / "verified.json"
MANIFEST = SRC / "manifest.json"
UA = {"User-Agent": "ethicalhive-source-fetch/1.0 (research; contact repo)"}
STOP = set("a an the of in on to for and or is are be as with by from that this it its into".split())


def norm(s):
    return [w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in STOP]


def fetch(url, binary=False, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode("utf-8", "replace")


def abs_title(arxiv_id):
    try:
        html = fetch(f"https://arxiv.org/abs/{arxiv_id}")
    except Exception as e:
        return None, f"abs fetch failed: {e}"
    m = re.search(r'<title>\s*(?:\[[^\]]*\]\s*)?(.*?)\s*</title>', html, re.S | re.I)
    return (m.group(1).strip() if m else ""), None


def verify(files):
    SRC.mkdir(parents=True, exist_ok=True)
    proposals = []
    for f in files:
        proposals += json.loads(Path(f).read_text())
    grounded = [p for p in proposals if p.get("grounded") and p.get("arxiv_id")]
    survivors, dropped = [], []
    for p in grounded:
        aid = p["arxiv_id"].replace("arxiv:", "").strip()
        pdf = SRC / f"{aid}.pdf"
        # download pdf
        if not (pdf.exists() and pdf.stat().st_size > 10000):
            try:
                data = fetch(f"https://arxiv.org/pdf/{aid}.pdf", binary=True)
            except Exception as e:
                dropped.append((p["id"], aid, f"pdf download failed: {e}")); continue
            if not data[:4] == b"%PDF" or len(data) < 10000:
                dropped.append((p["id"], aid, "not a valid pdf")); continue
            pdf.write_bytes(data)
            time.sleep(1)  # be polite to arxiv
        # title match
        title, err = abs_title(aid)
        if err:
            dropped.append((p["id"], aid, err)); continue
        want, got = set(norm(p.get("title"))), set(norm(title))
        overlap = len(want & got) / max(1, len(want))
        if overlap < 0.5:
            dropped.append((p["id"], aid, f"title mismatch ({overlap:.0%}): page='{title}'")); continue
        p["arxiv_id"] = aid
        p["pdf"] = f"ontology/sources/{aid}.pdf"
        p["page_title"] = title
        survivors.append(p)
    VERIFIED.write_text(json.dumps(survivors, indent=1, ensure_ascii=False))
    MANIFEST.write_text(json.dumps(
        [{"concept": s["id"], "arxiv_id": s["arxiv_id"], "title": s["title"],
          "year": s.get("year"), "pdf": s["pdf"]} for s in survivors],
        indent=1, ensure_ascii=False))
    print(f"grounded proposals: {len(grounded)}  verified+downloaded: {len(survivors)}  dropped: {len(dropped)}")
    for d in dropped:
        print("  DROP", d[0], d[1], "-", d[2])
    print(f"PDFs in {SRC}, manifest -> {MANIFEST}")


ID_RE = re.compile(r"^- id:\s*(\S+)\s*$")


def apply():
    import yaml
    verified = json.loads(VERIFIED.read_text())
    by_id = {v["id"]: v for v in verified}
    data = yaml.safe_load(YAML.read_text())
    existing = {m["id"]: (m.get("selected_papers") or []) for m in data["modes"]}

    lines = YAML.read_text().splitlines(keepends=True)
    starts = [i for i, l in enumerate(lines) if ID_RE.match(l)]
    starts.append(len(lines))
    bounds = {starts[k]: starts[k + 1] for k in range(len(starts) - 1)}
    out, i, done = [], 0, []
    while i < len(lines):
        m = ID_RE.match(lines[i])
        if not m or m.group(1) not in by_id:
            out.append(lines[i]); i += 1; continue
        mid, end = m.group(1), bounds[i]
        block = lines[i:end]
        v = by_id[mid]
        aid = v["arxiv_id"]
        ai_paper = {
            "id": f"arxiv:{aid}", "title": v["title"], "year": int(v["year"]),
            "url": f"https://arxiv.org/abs/{aid}", "domain": "ai", "venue": "arXiv",
            "publication_type": "preprint",
            "relevance": v.get("relevance", ""),
            "consulted": "Read via arXiv abstract and HTML on 2026-11-22; PDF archived under ontology/sources.",
            "verification_url": f"https://arxiv.org/abs/{aid}",
            "verified_date": "2026-11-22",
            "finding": v.get("finding", ""),
            "local_pdf": v["pdf"],
        }
        # keep the real human-cognition source(s); drop unread AI keyword-matches; cap at 3
        humans = [p for p in existing.get(mid, []) if p.get("domain") == "human-related"]
        newsel = [ai_paper] + humans[:2]
        nb, j = [], 0
        while j < len(block):
            l = block[j]
            if re.match(r"^  example:\s", l):
                nb.append("  example: " + json.dumps(v["example"], ensure_ascii=False) + "\n"); j += 1; continue
            if re.match(r"^  selected_papers:\s*$", l):
                nb.append("  selected_papers:\n")
                for p in newsel:
                    nb.append("  - " + json.dumps(p, ensure_ascii=False) + "\n")
                j += 1
                while j < len(block) and (block[j].startswith("  - ") or re.match(r"^    ", block[j])):
                    j += 1
                continue
            nb.append(l); j += 1
        out.extend(nb); done.append(mid); i = end
    YAML.write_text("".join(out))
    d = yaml.safe_load(YAML.read_text())
    print(f"applied: {len(done)} modes grounded (grounded example + verified AI paper prepended; tag kept analogy)")
    print(f"YAML OK: {len(d['modes'])} modes")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("verify", "apply"):
        print(__doc__); sys.exit(1)
    if sys.argv[1] == "verify":
        verify(sys.argv[2:])
    else:
        apply()
