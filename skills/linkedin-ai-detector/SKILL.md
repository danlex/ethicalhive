---
name: linkedin-ai-detector
description: Detect formulaic AI writing patterns in LinkedIn posts, short-form blogs, and professional web content. Use when the user pastes a LinkedIn post or draft and asks to "detect AI patterns", "check if this LinkedIn post is AI-written", "score this text", "find AI tells", or "audit my post"; or when the user invokes /linkedin-ai-detector. Returns a strict Markdown report with Pattern Score (0-10), highlighted text, detected patterns, main diagnosis, and validation checklist. Does not rewrite. For academic papers, use the paper-ai-detector instead.
---

# LinkedIn AI Detector

Detect AI-generated writing patterns in short-form professional content — LinkedIn posts, blog articles, web copy. Returns a structured Markdown report with a Pattern Score (0–10), highlighted text, detected patterns, main diagnosis, and a validation checklist. Configured for Alexandru Dan's voice (TVL Tech) — calm, direct, factual, professional. Adapt the audience/tone notes if you use it for another author.

For academic / research papers, use the separate `paper-ai-detector` skill — different patterns, different banned phrases, different validation criteria.

## When to invoke

- User pastes a LinkedIn post, blog excerpt, or draft and asks to *"detect AI patterns"*, *"check if this is AI-written"*, *"score this text"*, *"find AI tells"*, *"audit my post"*, or similar.
- User provides a URL to a blog post or article and asks to analyze its writing patterns.
- User explicitly types `/linkedin-ai-detector`.

Skip for trivial conversational turns or non-writing tasks.

## How it runs

### Step 1. Capture the text

- **Inline text** — use it directly.
- **URL** — fetch with `WebFetch` and extract the article body (skip nav, footer, ads, comments).
- **Neither** — ask the user with this exact line:

  > Paste the text you want me to analyze. I will highlight the AI-like patterns, explain what triggers them, score the text, and return a Markdown report with the findings.

### Step 2. Spawn the subagent

Delegate to the `linkedin-ai-detector` subagent via the Agent tool. Pass:

- The full text to analyze (verbatim)
- The source URL if applicable
- Any preserve list — names, tools, numbers, domain terms the user does not want flagged

Do not analyze inline — a same-context analysis inherits the same patterns you are trying to catch.

### Step 3. Present the report

Return the subagent's Markdown report verbatim. Do not summarize. Do not soften the verdict. Do not pre-empt the user's editorial choices with rewrites.

If the user disagrees with a flagged pattern, capture their reasoning briefly. Do not auto-revise the original text — the user edits based on the report.

## Output format

The subagent returns a strict Markdown report. Full schema in `agents/linkedin-ai-detector.md`. Sections: Pattern Score, Highlighted Text, Detected Patterns, Main Diagnosis, Validation Check, Summary of Priority Fixes.

## Score scale

| Score | Reading |
|---|---|
| 0–2 | Natural, specific, human writing |
| 3–4 | Mostly natural with isolated formulaic elements |
| 5–6 | Noticeable patterns; readers may sense templating |
| 7–8 | Heavily templated; multiple AI tells |
| 9–10 | Strongly AI-patterned across structure, phrasing, and rhythm |

## Rules (orchestrator)

- No rewriting in any layer.
- No alternative full versions.
- Mark exact phrases with `==phrase==` highlighting.
- Preserve names, numbers, tools, technical details from the original.
- The report is advisory — the human decides what to revise.
- If you disagree with a finding, surface the disagreement to the user; do not silently override the subagent.
