# Community Cases

This directory receives cases submitted by bias-validator agents running in the wild. Each case is a PR that was reviewed and merged by maintainers.

## How cases arrive

1. Someone runs the bias-validator in their project
2. After the audit resolves, the agent asks: "Want to contribute this case?"
3. If approved, the agent sanitizes the case (removes proprietary code, PII, credentials) and creates a PR
4. Maintainers review the PR for:
   - Privacy: no proprietary code leaked?
   - Signal: does the case demonstrate a real pattern?
   - Labels: are the tags accurate?
5. Merged cases become part of the training corpus

## Directory structure

```
community/
├── 2026-04/
│   ├── 20260418-a3f2-groundedness-block.json
│   ├── 20260419-b7c1-sycophancy-revise.json
│   └── ...
├── 2026-05/
│   └── ...
└── index.jsonl    (auto-generated summary of all cases)
```

## Case format

See `../case-schema.json`. Key fields:

- `source`: "anonymous" (default) or contributor handle
- `tags`: classification labels (true-positive, false-positive, per-check tags, pattern tags)
- `input`: sanitized draft + evidence + user ask
- `validator`: what the validator found (CoVe table, checks, verdict)
- `resolution`: what the human decided (accepted, overridden, partial)

## Using cases for training

The accumulated corpus enables:

1. **Benchmark runs** — test new rubric versions against labeled cases
2. **False positive analysis** — identify which checks over-fire and on what patterns
3. **Rubric evolution** — propose changes backed by n≥10 cases (through judge council governance)
4. **Cross-project patterns** — discover failure modes that appear across different codebases

## Contributing manually

You can also submit cases manually:

```bash
# Create a case file
cp ../case-schema.json my-case.json
# Edit with your case details (sanitize!)
# Submit as a PR
```

## Privacy requirements

Every case MUST be sanitized before submission:
- No proprietary code (use pseudocode)
- No internal file paths (generalize)
- No API keys, credentials, or PII
- No customer data
- Preserve the failure pattern — sanitization must not destroy what makes the case valuable
