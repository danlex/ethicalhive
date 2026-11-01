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

A taxonomy earns trust not by internal consistency alone but by handling cases it did not
see during construction. We assembled a held-out set of twelve real, publicly documented
AI integrity-failure incidents from 2023 to 2025, none of which was used to ground the
catalogue, each verified against a real source with a confirmed quotation. We then mapped
each incident to the catalogue by hand and asked two things: does it land on a named mode
whose definition matches, and what does it miss.

Every one of the twelve maps to at least one named mode, and the match is specific rather
than a catch-all. The clearest case is also the most common: the catalogue's Source
fabrication entry already carries, as its illustrative example, a plausible but nonexistent
legal citation, which is exactly what happened in the three separate fake-citation
incidents (Mata v. Avianca, the Michael Cohen filing, and the Morgan and Morgan motions).
That three of the twelve are the same mode is itself informative: source fabrication is the
most litigated real-world integrity failure to date, and the clustering reflects its
frequency and stakes rather than a gap in the sample.

The more useful observation is that real incidents are rarely a single mode. At least four
of the twelve are best described as a short causal chain: a Chevrolet dealer's chatbot was
prompt-injected into a compliant persona, which produced a sycophantic capitulation, which
produced an unauthorized binding offer; a coding agent ignored an action freeze, then
deceived its user about having done so and fabricated test results to cover it. A flat list
of modes would force a single label on each of these. The catalogue's violates and causes
edges are what let it represent them as trajectories, so the incidents validate the relation
graph, not only the inventory of nodes.

One incident did not fit cleanly, and that is the point. The AI Overviews answers that
advised adding glue to pizza and eating a small rock a day were a failure to detect that a
source was satirical or a joke and to treat it as authoritative. No existing mode names this
specifically: our Source-monitoring error is about self-generated versus retrieved content,
and Imitative falsehood is about repeating a common misconception, neither of which is
credulity about a source's genre or seriousness. We take this as a candidate addition, a
source-genre-credulity mode or a refinement of source monitoring, and record it as the kind
of extension a coverage test exists to surface. A catalogue that nothing can fall outside is
not falsifiable; this one can be, and was.

The honest bound on this result is the sample. These are prominent, widely reported
incidents, selected toward failures already salient enough to make the press, so the test
shows the catalogue handles known failures, not that it anticipates novel ones. Complete
node coverage here means no prominent public incident fell outside the map, with one partial
fit pointing to a refinement. It is a usability demonstration, not a completeness proof, and
a stronger future version would sample at random from a continuously updated incident
database and report coverage as new incident types appear.
