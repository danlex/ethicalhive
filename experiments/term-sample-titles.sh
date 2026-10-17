#!/usr/bin/env bash
# term-sample-titles.sh — print the top-N most-recent arXiv titles behind a query.
#
# Companion to term-literature-count.sh. A raw count can be inflated by papers
# that only MENTION a term (e.g. a cs.LG paper citing "confirmation bias" from
# human psychology). This script lets you eyeball what the count is actually
# counting, so an AI-domain claim rests on read titles, not on the category tag.
#
# Usage:
#   experiments/term-sample-titles.sh '<arxiv clause>' [N]
# Example:
#   experiments/term-sample-titles.sh 'all:"confirmation bias"' 10
# The category filter (cs.AI OR cs.CL OR cs.LG) is appended automatically.

set -euo pipefail

CLAUSE="${1:?usage: term-sample-titles.sh '<arxiv clause>' [N]}"
N="${2:-10}"
CATEGORY_FILTER='(cat:cs.AI OR cat:cs.CL OR cat:cs.LG)'
API='https://export.arxiv.org/api/query'

curl -sSL --max-time 30 -G "$API" \
  --data-urlencode "search_query=$CLAUSE AND $CATEGORY_FILTER" \
  --data-urlencode 'sortBy=submittedDate' \
  --data-urlencode 'sortOrder=descending' \
  --data-urlencode "max_results=$N" \
| tr '\n' ' ' \
| grep -o '<title>[^<]*</title>' \
| sed -e 's/<title>//' -e 's/<\/title>//' \
| tail -n +2
