# Human inter-annotator study (protocol)

This is the package that turns the catalogue's category-reproducibility check from a
model-based proxy into human inter-annotator agreement, the one piece the paper's Section 5
flags as required and that only humans can supply. It mirrors the model-rater study exactly,
so the numbers are comparable.

## What it measures

Whether the catalogue's assignment of each mode to one of the eleven categories (ten
cognitive systems plus the AI-native tier) is recoverable by independent human annotators
working from the written definitions alone, correcting for chance with Cohen's kappa.

## Steps

1. **Freeze.** The sheet `annotation-sheet.csv` is a stratified sample of 33 modes (three per
   category), with the catalogue's own category hidden. The gold answers are in
   `../agree-gold.json`; do not show them to annotators. Do not change the catalogue until
   the study is done.
2. **Recruit at least two annotators** who did not build the catalogue. Give each a fresh
   copy of `annotation-sheet.csv` and the codebook below. They work independently.
3. **Annotate.** For each row, the annotator reads the mode name and definition and writes
   exactly one of the eleven category names in the `your_category` column. They may answer
   "unsure" if genuinely torn; record it rather than forcing a guess.
4. **Ingest and score.** For each filled sheet:
   ```
   python3 experiments/taxonomy-agreement.py ingest path/to/filled-annotator1.csv annotator1
   python3 experiments/taxonomy-agreement.py ingest path/to/filled-annotator2.csv annotator2
   python3 experiments/taxonomy-agreement.py score experiments/agree-gold.json \
       experiments/results/human-annotator1.jsonl experiments/results/human-annotator2.jsonl
   ```
   This prints each annotator's agreement with the catalogue (Cohen kappa, with a Wilson
   interval on raw agreement) and the inter-annotator kappa, in the same format as the model
   study, so the two can be compared directly.
5. **Report.** Put the human kappas next to the model kappas (0.90 sonnet, 0.83 haiku, 0.93
   inter-rater) in the paper's Section 5.1, and keep whichever is lower as the honest figure.
   Record where the humans disagreed; those are the live category seams.

## The codebook (give this to annotators)

Assign each mode to the one category whose description best fits, by which cognitive system
or tier the failure belongs to.

- **Perception**: failures of how input is perceived or predictively filled in before reasoning.
- **Memory**: failures of storage, recall, interference, or reconstruction of information.
- **Attention**: failures of what the model attends to: capture, blindness, salience, gating.
- **Heuristics**: fast judgment shortcuts and the classic decision biases (anchoring, base-rate, framing).
- **Reasoning**: failures of inference, logic, calibration-free deduction, shortcut reasoning.
- **Metacognition**: failures of confidence, self-knowledge, knowing what one knows.
- **Language**: failures of parsing, pragmatics, register, semantics in language itself.
- **Social**: failures driven by other agents or users: conformity, sycophancy, persuasion, manipulation.
- **Moral**: failures of moral judgment, value application, and ethical reasoning.
- **Self & agency**: failures of identity, goal-tracking, self-model, and sense of agency.
- **AI-native**: failure modes with no human cognitive analogue, specific to the machine (reward hacking, prompt injection, scheming, model collapse).

## Regenerate the sheet

```
python3 experiments/taxonomy-agreement.py worksheet 33
```

The sample is deterministic, so regenerating gives the same 33 modes and the same gold map.
