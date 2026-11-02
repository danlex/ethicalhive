#!/usr/bin/env python3
"""openrouter-review.py - get independent reviews of a bundle from a panel of models.

Sends one assembled bundle (instruction + paper + evidence) to several models on OpenRouter,
so the reviews come from different model families than the one that wrote the paper. This is
the cross-family check: model diversity is what breaks the paper's circularity limitation.

Usage:
  experiments/openrouter-review.py <bundle.md> --models m1,m2,m3 [--max-tokens 3500]

Writes each review to paper/reviews/panel-<sanitized-model>.md and prints a one-line verdict
per model. The API key is read from the gitignored .env by openrouter.py and never printed.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openrouter

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "paper" / "reviews"

SYSTEM = (
    "You are an adversarial independent peer reviewer from a different model family than the "
    "one that wrote the paper under review. Be concrete and blunt; do not be generous for its "
    "own sake. Answer the five questions in the bundle, then end with exactly one line: "
    "'VERDICT: <reject | major revision | minor revision | accept>'."
)


def sanitize(m):
    return re.sub(r"[^a-z0-9]+", "-", m.lower()).strip("-")


def verdict_of(text):
    m = re.findall(r"VERDICT:\s*(reject|major revision|minor revision|accept)", text, re.I)
    return m[-1].lower() if m else "(no explicit verdict line)"


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    bundle = Path(sys.argv[1]).read_text(encoding="utf-8")
    models, max_tokens = [], 3500
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == "--models" and i + 1 < len(args):
            models = [m.strip() for m in args[i + 1].split(",") if m.strip()]
        if a == "--max-tokens" and i + 1 < len(args):
            max_tokens = int(args[i + 1])
    if not models:
        print("No --models given."); sys.exit(1)
    OUTDIR.mkdir(parents=True, exist_ok=True)

    summary = []
    for model in models:
        sys.stderr.write(f"reviewing with {model} ...\n")
        try:
            out = openrouter.chat(model, bundle, temperature=0.3, max_tokens=max_tokens,
                                  retries=2, system=SYSTEM)
        except Exception as e:  # network / model-unavailable
            out, v = f"ERROR calling {model}: {e}", "(unavailable)"
            summary.append((model, v))
            (OUTDIR / f"panel-{sanitize(model)}.md").write_text(
                f"# Review by {model}\n\n{out}\n", encoding="utf-8")
            print(f"  {model:40s} -> {v}")
            continue
        v = verdict_of(out)
        (OUTDIR / f"panel-{sanitize(model)}.md").write_text(
            f"# Independent review by {model}\n\nVia OpenRouter, cross-family panel.\n\n{out}\n",
            encoding="utf-8")
        summary.append((model, v))
        print(f"  {model:40s} -> {v}")

    print("\n=== panel verdicts ===")
    for model, v in summary:
        print(f"  {model:40s} {v}")


if __name__ == "__main__":
    main()
