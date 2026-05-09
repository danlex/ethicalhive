---
name: paper-ai-detector
description: Detect AI-generated writing patterns in academic / research papers. Use when the user provides a paper (PDF, URL, .tex source, Markdown source, or pasted text) and asks to "detect AI patterns", "audit this paper", "score this manuscript", "check this abstract", "find AI tells in this paper", or "review this submission"; or when the user invokes /paper-ai-detector. Returns a strict Markdown report with Pattern Score (0-10), highlighted text, detected patterns, citation audit, main diagnosis, and an 11-item validation checklist. Does not rewrite. For LinkedIn / blog content, use the linkedin-ai-detector instead.
---

# Paper AI Detector

Detect AI-generated writing patterns in academic and research papers. Returns a structured Markdown report with a Pattern Score (0–10), highlighted text, detected patterns, **citation audit**, main diagnosis, and an 11-item validation checklist tailored for academic content.

For LinkedIn posts and short-form blog content, use the separate `linkedin-ai-detector` skill — different patterns, different banned phrases, different validation criteria.

## When to invoke

- User drops a PDF, shares an arxiv / DOI URL, pastes `.tex` / Markdown source, or pastes a section of a paper, and asks to *"detect AI patterns"*, *"audit this paper"*, *"score this manuscript"*, *"check this abstract"*, *"find AI tells"*, *"review this submission"*, or similar.
- User explicitly types `/paper-ai-detector`.
- User asks to verify whether a paper's writing or citations look AI-generated.

Skip for trivial conversational turns or non-paper writing tasks.

## How it runs

### Step 1. Capture the paper

Three input paths:

- **PDF attached.** Use `Read` with the `pages` parameter to extract text. For papers >10 pages, sample by section: abstract (always), introduction (first + last paragraph), methods (first paragraph + a middle one), results (first paragraph), discussion / conclusion (full), references / bibliography (full). The full paper goes into the subagent's input but the highlighted-text section in the report uses the sampled passages.
- **URL.** `WebFetch` arxiv abstract pages, DOI redirects, journal pages, preprint servers (arxiv.org, biorxiv.org, ssrn.com, openreview.net). For arxiv, fetching `.../abs/<id>` gives the abstract page; the PDF lives at `.../pdf/<id>`. Pull the abstract page first.
- **Source paste.** `.tex` source, Markdown export, or plain text. Use as-is.

If neither file, URL, nor text is provided, ask:

> Paste the paper, drop a PDF, or share a URL. I will analyze the writing for AI patterns, score it, check the citations, and return a Markdown report. I will not rewrite the paper.

### Step 2. Spawn the subagent

Delegate to the `paper-ai-detector` subagent via the Agent tool. Pass:

- The full paper text (or sampled key sections for long papers)
- The source: PDF filename, URL, or "pasted source"
- The bibliography section verbatim if available (required for the Citation Audit step)
- Optional preserve list — author names, dataset names, model names, equations, technical jargon

Do not analyze inline — a same-context analysis inherits the same patterns you are trying to catch.

### Step 3. Citation audit (light verification)

The subagent performs format-level citation verification:

- Confirms each in-text citation has a bibliography entry
- Flags entries lacking a DOI or arxiv ID
- Flags suspicious citation clusters (e.g. many citations to the same author across unrelated topics, or a bibliography that is 80%+ recent papers in obscure venues)

The subagent does **not** WebFetch every cited URL — too slow, paywalls block it. It surfaces a list of citations to verify manually.

If the user explicitly asks for **deep citation verification**, the orchestrator can WebFetch a small subset (5–10) of the flagged citations and report whether the URLs resolve to the cited paper. Default is **off** unless requested.

### Step 4. Present the report

Return the subagent's Markdown report verbatim. Do not summarize. Do not soften the verdict. Do not pre-empt the user's editorial choices with rewrites.

If the user disagrees with a flagged pattern, capture their reasoning briefly. Do not auto-revise the paper — the user edits based on the report.

## Output format

The subagent returns a strict Markdown report. Full schema in `agents/paper-ai-detector.md`. Sections: Pattern Score, Source, Highlighted Text, Detected Patterns, **Citation Audit**, Main Diagnosis, Validation Check, Summary of Priority Fixes.

## Score scale

| Score | Reading |
|---|---|
| 0–2 | Rigorous, specific, human academic writing |
| 3–4 | Mostly natural with isolated AI tells |
| 5–6 | Noticeable boilerplate; a careful reviewer would raise eyebrows |
| 7–8 | Heavily AI-templated; suspicious citation patterns |
| 9–10 | Largely AI-generated; multiple fabricated-citation candidates |

## Audience and tone

The skill is configured for: researchers, peer reviewers, journal editors, and authors auditing their own drafts before submission. Academic register — calm, strict, constructive. No marketing language. No drama.

## Rules (orchestrator)

- No rewriting in any layer. No alternative full versions of the paper.
- Preserve author names, dataset names, model names, equations, technical jargon.
- Mark exact phrases with `==phrase==` highlighting in the Highlighted Text section.
- Reference section locations (e.g. *"Abstract, sentence 1"*, *"Methods §3.2, paragraph 2"*) for every detected pattern.
- The report is advisory — the human decides what to revise.
- Citation Audit is light verification only by default; deep verification requires explicit user opt-in.
- If the bibliography is missing from input, mark **Citation Audit: skipped** rather than fabricating one.
