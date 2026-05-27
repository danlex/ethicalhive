# arXiv submission instructions

Step-by-step for the author. The build script `paper/build-arxiv.sh`
produces the submission package; everything below happens in a browser
on https://arxiv.org.

## 1. Build the package

```bash
bash paper/build-arxiv.sh
```

This produces:
- `paper/arxiv/main.tex` and `paper/arxiv/body.tex` (the source)
- `paper/arxiv/main.pdf` (local sanity-check render)
- `paper/arxiv/submission.tar.gz` (the upload to arXiv)

Verify the PDF opens cleanly and the rendering matches `paper/draft.pdf`.

## 2. arXiv account and endorsement

If this is your first arXiv submission, two prerequisites:

1. Register at https://arxiv.org/user/register with your institutional
   email (alexandru.dan@triumviratelabs.ro works; a university email
   speeds endorsement).
2. **Endorsement** is required for first-time submitters to archives
   like cs.AI, cs.LG, cs.CL. The easiest path: start the submission,
   arXiv tells you which categories need endorsement, you ask a
   colleague who has previously submitted to that category to endorse
   you (one-click). Approval is usually under a day.

## 3. Submit

Go to https://arxiv.org/submit and click **Start a new submission**.

### 3.1 License

- **arXiv default** (perpetual non-exclusive) — simplest.
- **CC-BY 4.0** — recommended; lets others cite and reuse cleanly.

### 3.2 Archive and category

- **Primary archive:** `cs`
- **Primary category:** `cs.AI` (Artificial Intelligence) — best fit.
- **Cross-list:** `cs.LG`, `cs.HC`, `cs.CL`.

### 3.3 Metadata

- **Title:** `Contracts Between Humans and AI Agents: An Advisory Integrity Agreement for Agentic Coding`
- **Authors:** `Alexandru Dan` / Triumvirate Labs
- **Abstract:** copy from the YAML abstract block at the top of
  `paper/draft.md`.
- **Comments:** `Pilot-feasibility report. 8 pages plus references.
  Target venue: NeurIPS 2026 workshop (TBD). Code and benchmark at
  https://github.com/danlex/ethicalhive`

### 3.4 Upload

- Click **Choose files**.
- Upload `paper/arxiv/submission.tar.gz`.
- arXiv extracts and recompiles. If the compile fails, the LaTeX log
  appears; fix locally, rebuild via `paper/build-arxiv.sh`, re-upload.

### 3.5 Preview and submit

- Click **Preview**. arXiv renders the PDF.
- Confirm title, authors, abstract, references.
- Click **Submit**. arXiv processes twice daily (08:00 / 20:00 UTC).
  Your paper is live the next business-day announcement with a
  permanent ID like `arXiv:2605.XXXXX`.

## Notes specific to this paper

- **No figures** in the body. Nothing to upload separately.
- **References** are inline in `body.tex` as a `References` section.
  arXiv accepts this; no `.bib` file is needed for v1.
- **AgentVerify citation** lacks a named author. preprints.org
  returned 403 on the WebFetch attempts; either open the URL in
  your browser and patch the author list into `paper/draft.md`
  before rebuilding, or ship v1 as-is and patch in v2.
- **No anonymous variant** for arXiv (preprints are not double-blind).
  Anonymous variant is for workshop submission via
  `bash paper/build-latex.sh --anon`.
