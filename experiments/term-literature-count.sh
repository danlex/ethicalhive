#!/usr/bin/env bash
# term-literature-count.sh — count arXiv preprints per failure-mode term.
#
# For each row in a terms TSV (label<TAB>arxiv_clause), query the arXiv API for
# the number of preprints matching the clause within the AI categories
# (cs.AI OR cs.CL OR cs.LG) and print a Markdown table.
#
# This is a PROXY for "AI papers on term X": it counts arXiv preprints in three
# CS categories whose text matches a keyword. It is not all AI papers, and a
# keyword match is not a topic match. Coined in-house terms (narrativity drift,
# selective evidence) are expected to score low precisely because the LITERATURE
# does not use that phrasing. Read the counts as "how established is this term",
# not "how important is this failure mode".
#
# Usage:
#   experiments/term-literature-count.sh [terms.tsv]
# Default terms file: the terms.tsv next to this script.
#
# arXiv asks for <= 1 request / 3s; we sleep 3s between queries.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERMS_FILE="${1:-$SCRIPT_DIR/terms.tsv}"
CATEGORY_FILTER='(cat:cs.AI OR cat:cs.CL OR cat:cs.LG)'
API='https://export.arxiv.org/api/query'

if [[ ! -f "$TERMS_FILE" ]]; then
  echo "terms file not found: $TERMS_FILE" >&2
  exit 1
fi

arxiv_count() {
  # $1 = full search_query. Echoes the integer total, or "ERR".
  local query="$1" xml total
  xml="$(curl -sSL --max-time 30 -G "$API" \
          --data-urlencode "search_query=$query" \
          --data-urlencode 'max_results=1' 2>/dev/null)" || { echo "ERR"; return; }
  if grep -q '<id>https://arxiv.org/api/errors</id>' <<<"$xml"; then
    echo "ERR"; return
  fi
  total="$(grep -o '<opensearch:totalResults[^>]*>[0-9]*' <<<"$xml" | grep -o '[0-9]*$' | head -1)"
  echo "${total:-ERR}"
}

echo "| Term | arXiv clause | Count (cs.AI/CL/LG) |"
echo "|---|---|---|"

while IFS=$'\t' read -r label clause; do
  [[ -z "${label// }" ]] && continue
  [[ "$label" == \#* ]] && continue
  count="$(arxiv_count "$clause AND $CATEGORY_FILTER")"
  printf '| %s | `%s` | %s |\n' "$label" "$clause" "$count"
  sleep 3
done < "$TERMS_FILE"
