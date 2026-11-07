"""Look up books on the Internet Archive and search inside their scanned full text.

Uses only archive.org (metadata search and the full-text search service), so it works where
the archive's file servers are not reachable. Snippets are printed with the matched words in
[[double brackets]].

Usage:
  python archive-fts.py find "<title words>" ["<author>"]   list matching text items
  python archive-fts.py inside <identifier> "<phrase>"       search one item's full text
  python archive-fts.py anywhere "<phrase>" ["<more words>"] search all scanned texts
"""
import json
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "ethicalhive-source-check/1.0"}
FTS = "https://archive.org/services/search/beta/page_production/?"


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def clean(s):
    s = s.replace("{{{", "[[").replace("}}}", "]]")
    return re.sub(r"\s+", " ", s).strip()


def fts(query, n):
    url = FTS + urllib.parse.urlencode({"service_backend": "fts", "user_query": query,
                                        "hits_per_page": n})
    body = get(url).get("response", {}).get("body", {}).get("hits", {})
    return body.get("total", 0), body.get("hits", [])


def show(hits, snippets):
    for h in hits:
        f = h.get("fields", {})
        print(f"- {f.get('identifier')} | {f.get('title')} | {f.get('year') or f.get('date', '')}"
              f" | {', '.join(f.get('creator') or []) if isinstance(f.get('creator'), list) else f.get('creator', '')}")
        for t in (h.get("highlight", {}).get("text") or [])[:snippets]:
            print(f"    \"{clean(t)[:400]}\"")


cmd = sys.argv[1] if len(sys.argv) > 1 else ""
if cmd == "find" and len(sys.argv) >= 3:
    q = f"title:({sys.argv[2]}) AND mediatype:texts"
    if len(sys.argv) >= 4:
        q += f" AND creator:({sys.argv[3]})"
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": q, "fl[]": ["identifier", "title", "year", "creator"], "rows": 12, "output": "json"},
        doseq=True)
    docs = get(url)["response"]["docs"]
    for d in docs:
        c = d.get("creator", "")
        c = "; ".join(c) if isinstance(c, list) else c
        print(f"- {d['identifier']} | {d.get('title')} | {d.get('year', '')} | {c}")
    if not docs:
        print("no items found")
elif cmd == "inside" and len(sys.argv) >= 4:
    total, hits = fts(f"{sys.argv[3]} AND identifier:{sys.argv[2]}", 1)
    print(f"hits in item: {total}")
    show(hits, 4)
elif cmd == "anywhere" and len(sys.argv) >= 3:
    total, hits = fts(" ".join(sys.argv[2:]), 6)
    print(f"total hits: {total}")
    show(hits, 1)
else:
    print(__doc__)
