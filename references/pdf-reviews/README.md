# Sequential PDF corpus review

The manifest in `../pdf-corpus-2026-11-26.json` lists the supplied files in a
stable reading order. Each numbered JSON record documents one PDF. A separate
commit is pushed after that file's review and any supported ontology changes.

Read the complete extracted text, including limitations and references, before
claiming a full-text review. Disclose unread supplements, figures not visually
inspected, extraction failures and other access limits. Reading a review does
not mean its cited primary studies were read. Short quotations have both PDF
and printed-page locators. Source bytes are identified by SHA-256; PDFs, private
download links and full extracted text are not published in this repository.

Check every proposed concept against current names, aliases, definitions and
boundaries. Reuse or enrich an existing entry where appropriate. A new subtype
must explain its distinction from the parent. Human responses to AI do not
establish an intrinsic AI mechanism: proposed AI analogues and tests remain
explicit. Do not create harm edges, validation claims or additional citations
just to fill a field. A paper can add no new entry.

Verify apparent duplicates by complete-file checksum. A duplicate record points
to the already-read matching PDF and makes no claim to an independent reading
or replication. Different bytes require separate inspection.

`experiments/pdf-corpus-review.py` checks identity, queue order, page coverage
declarations and quoted passages before applying a manually authored review.
It does not read or interpret papers, establish semantic novelty automatically,
or prove that a reader understood every page. The `lookup` command is only a
lexical aid; a human or agent must assess conceptual overlap.

```bash
python3 experiments/pdf-corpus-review.py status
python3 experiments/pdf-corpus-review.py pages /path/to/paper.pdf --start 1 --end 5
python3 experiments/pdf-corpus-review.py lookup 'proposed term'
python3 experiments/pdf-corpus-review.py apply /tmp/review.json --pdf /path/to/paper.pdf
python3 experiments/validate-ontology.py
```
