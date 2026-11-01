# Validation

Staged draft of the validation section for the map-led resource paper. Slots in as
Section 6. Two sub-studies: category-assignment reproducibility (below) and a coverage
test (to follow). Counts and chance-corrected agreement, no decimals-only, the proxy
nature of the raters stated plainly.

---

## 6.1 Is the category structure reproducible?

The obvious threat to a single-author catalogue is that its structure is idiosyncratic:
that the assignment of each mode to one of the eleven categories (ten cognitive systems
plus the AI-native tier) reflects the author's taste rather than anything a second party
would recover. We probe this with a codebook protocol.

We drew a stratified sample of 33 modes, three from each of the eleven categories. We gave
two independent raters a codebook (one sentence defining each category) and, for each
mode, its name and definition only, with the catalogue's own category hidden. Each rater
assigned every mode to exactly one category. We then measured agreement between each
rater and the catalogue, and between the two raters, using Cohen's kappa, which corrects
for chance agreement.

The raters are independent large-language-model calls, one on the sonnet tier and one on
the haiku tier, blind to the catalogue label. This is deliberately a proxy. It is not
human inter-annotator agreement, and we do not present it as such; human annotation
remains required before this catalogue is treated as validated. What the proxy does buy is
a real chance-corrected number and a stress test of whether the category definitions are
clear enough that an outside rater can apply them at all. If independent raders cannot
recover a category from its definition, neither will human annotators, and the fix belongs
in the codebook now.

The agreement is high. Against the catalogue, the sonnet rater agreed on 30 of 33 modes
(kappa 0.90) and the haiku rater on 28 of 33 (kappa 0.83); the two raters agreed with each
other at kappa 0.93. All three fall in the range conventionally read as almost-perfect
agreement. Because chance agreement across eleven balanced categories is low (expected
agreement 0.09), the raw agreement and the kappa are close.

More informative than the aggregate is where the raters disagreed, because the
disagreements are localized rather than scattered. Three modes account for most of them
and both raters missed the same ones: cognitive miserliness, which the catalogue files
under Reasoning and both raters read as Heuristics; default-mode mind-wandering, filed
under Self and agency and read as Attention; and scope creep, filed in the AI-native tier
and read as Self and agency on a goal-tracking interpretation. These are genuine boundary
cases, not errors. A mode that sits on the seam between two cognitive systems is a fact
about cognition, not a defect in the map, and the value of the probe is that it names
exactly which seams are live so a reader knows where the categories are soft. The catalogue
records single-label assignments; these three are the clearest candidates for a
secondary-category annotation in a future revision.

The honest reading: the category structure is reproducible by an outside rater from the
definitions alone, with a small, identifiable set of boundary modes where single-label
assignment is underdetermined. The next step that would let us drop the proxy caveat is a
two-human-annotator pass over a larger sample with adjudication, which we flag as required
future work rather than claim here.

## 6.2 Coverage: does the catalogue classify failures it was not built from?

(To follow: run a set of held-out, real failure instances not used in the grounding
through the catalogue, report how many map cleanly to an existing mode, and treat the
instances that do not as a feature. A catalogue that cannot be missed by anything is not
falsifiable; the gaps it surfaces are the evidence it is a real, extensible map.)
