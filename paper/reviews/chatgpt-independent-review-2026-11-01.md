# Independent review of the resource paper (ChatGPT, GPT-6.1 Sol, 2026-11-01)

Cross-family peer review obtained via the browser (ChatGPT, GPT-6.1 Sol, medium
reasoning, with live web verification against airisk.mit.edu, arXiv, ACL Anthology,
PubMed). Deliberately a different model family than the drafter, to address the paper's
own circularity limitation. The reviewer saw only `paper/REVIEW-REQUEST.md` (the paper
plus the five questions), not the YAML, benchmark, audit logs, or companion method paper,
so its checks are of the paper in isolation, which is the realistic reviewer situation.

## Verdict

**Reject in its current form at a top-tier venue.** A potentially useful resource, but the
draft claims more validation and conceptual coherence than it demonstrates.

## 1. The contribution

Real contribution: a versioned catalogue connecting existing failure labels to definitions,
obligations, examples, and literature, plus an audit of errors introduced during its
construction. It is NOT yet a demonstrated scientific ontology or an established account of
AI cognitive mechanisms. Three weak novelty signals:
- **207 vs 30**: more labels do not establish more distinct constructs. Malberg also runs
  30,000 tests across 20 models, so "sevenfold extension" is a misleading measure of
  scientific contribution.
- **Human parallels**: resemblance to a human behaviour does not establish a shared mechanism.
- **A relation graph**: edges become a contribution only when their semantics, correctness,
  and usefulness are demonstrated.

## 2. Would researchers cite it?

Possibly, for stable definitions, evidence pointers, crosswalks, annotation labels. Not as
proof that 207 distinct failures exist, that categories reflect AI mechanisms, or that
clause auditing works. Strongest reason to accept: a maintained, inspectable resource
reduces repeated terminology reconciliation and source checking. Strongest reason to reject:
the paper has not shown its distinctions are reliable, necessary, or useful beyond an
informed author's arrangement of existing concepts. Also: the positioning understates the
MIT Risk Repository (it has a causal taxonomy and AI system failures, not just harm
outcomes); describing it only as harm outcomes weakens the niche argument.

## 3. What would make it reference-defining

Demonstrate that the distinctions improve decisions. One convincing experiment beats another
hundred entries. Four work packages:

- **A. Construct validity.** For every retained mode: an observable definition with
  inclusion/exclusion criteria; its nearest confusable neighbour; a minimal example pair
  separating the two; evidence status (incl. contradictory/null); and whether it is a
  behaviour, a mechanism, an attack, or an outcome. Merge labels that cannot be reliably
  distinguished or that lead to the same corrective action. A defensible 120 modes beats an
  inflated 207.
- **B. Independent annotation study.** >=2 human annotators per item, adjudication,
  independently collected cases, catalogue frozen before collection; include ambiguous,
  clean, multi-label, and "none fits" cases. Measure incident-to-mode agreement, neighbour
  confusion, unsupported assignments, annotation time. (Category assignment for 33 named
  definitions is a much easier task than this.)
- **C. Downstream-utility ablation.** Compare freeform review / obligation checklist without
  named modes / flat catalogue / catalogue+evidence / catalogue+evidence+graph, at matched
  model, evidence access, and budget. Measure detection, false alarms on clean cases,
  attribution, repair. Isolates whether the benefit is obligations, names, evidence, or graph.
- **D. Independently measurable provenance.** Release original claims, cited passages,
  checker decisions, corrections, frozen versions; independently recheck the corrected
  release. The 26/186 figure is a checker-identified error proportion, NOT the corrected
  catalogue's residual error rate. Repeat on other catalogues to generalise.

Strongest framing: a tested infrastructure for distinguishing and auditing integrity
failures; importance from reliability and usefulness, not from beating specialist detectors.

## 4. One paper or three?

**Two papers now.** Resource paper (catalogue, construction protocol, provenance audit,
independent annotation, crosswalks) and method paper (clause auditing, benchmark, baselines,
ablations, error analysis). Do NOT split a third benchmark paper: 146 cases across 17 suites
(~9 per suite) is not yet a standalone benchmark contribution. The n=60 "better on four of
six" is preliminary and needs effect sizes, uncertainty, operating-point selection, and an
explanation of how specificity and attribution were scored. One comprehensive paper would
make three partially-supported contributions compete for space.

## 5. Top five weaknesses (prioritised)

1. **The ontology mixes incompatible kinds of things.** Prompt injection is an attack
   technique; overconfidence is a calibration property; source fabrication is an output
   failure. Reward hacking and scope creep plainly DO have human analogues, contradicting the
   AI-native label. An exclusive-label validator does not validate the distinction.
   Fix: separate observable behaviour, hypothesised mechanism, context, and consequence into
   different fields; replace the exclusive human/native split with qualified analogy and
   substrate tags; validate neighbouring distinctions.
2. **Validation tests label recoverability, not construct validity.** Sonnet and Haiku are
   not independent research teams; mode names reveal likely categories; "floor" is
   unjustified (shared assumptions can inflate agreement). Fix: report as model-based
   codebook checks; add blinded human annotation, CIs, confusion matrices; remove "floor" and
   the claim that disagreements establish facts about cognition.
3. **Provenance findings overstated and not reproducible.** "Roughly fifty" cannot support a
   precise rate; a wrong experimental condition need not be "minor"; "only reading catches
   errors" is not demonstrated. Fix: exact denominators, units, sampling, checker identities,
   source locations, severity rules, adjudication; independently audit the corrected release;
   restrict conclusions to this construction process unless externally replicated.
4. **The graph's causal claims exceed the evidence.** A plausible incident sequence does not
   establish injection caused sycophancy caused scope creep; edge typing is unspecified. Fix:
   define node and edge types; separate temporal sequence, association, hypothesised
   causation, demonstrated causation; attach evidence to edges; test whether graph access
   improves diagnosis over a flat catalogue.
5. **Coverage and novelty arguments are too easy to satisfy.** Twelve selected incidents
   (three sharing a legal-citation failure) do not strongly challenge 207 labels; "at least
   one fits" rewards broad labels. Fix: externally sampled incident set, prespecified
   matching rubric; score unsupported matches, specificity, missing modes, actionability
   against competing resources; track supported/contradicted/mixed/untested/illustrative
   separately.

Two sentences to change immediately:
- "These are transcription-level over-reads, not invented findings." Six examples did not
  appear in their cited papers; their origin requires investigation, not an exculpatory label.
- "The incidents validate the graph." They illustrate a possible use; validation needs a
  stronger test.

Recommendation: keep the resource contribution, remove the cognitive-mechanism overreach,
and make independent annotation plus downstream utility the centre of the next version.
