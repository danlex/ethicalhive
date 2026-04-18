# Case Database

Every bias-validator audit gets saved here as a JSON file. Each case captures:

- What was audited (draft, evidence, user ask)
- What the validator found (CoVe table, per-check verdicts)
- What the main session thought (confirmed/denied each finding)
- What the human decided (accepted/overridden)

Over time, this builds a labeled corpus that the validator can learn from.

## File naming

`{timestamp}-{short-id}.json` — e.g., `20260418-143022-a3f2.json`

## Schema

See `case-schema.json` for the full structure.

## Global vs project-local

- **Project-local**: `bias-validator/cases/` in your project — cases from this codebase
- **Global**: `~/.claude/bias-validator/cases/` — cases from all projects, for cross-project learning
