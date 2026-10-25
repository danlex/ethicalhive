#!/usr/bin/env python3
"""build-ontology.py - ONE-TIME migration: consolidate the scattered failure-mode
data into a single ethical-AI ontology at ontology/ethical-ai.yaml.

After this runs once, ontology/ethical-ai.yaml is the source of truth, maintained
by hand (or an ontologist), and build-catalogue.py reads it. This script exists to
seed that file from the current sources, and to re-seed if we ever need to.

Sources consolidated (the current page is built from these):
  references/research-2026-05-23-neuroscience-parallels.md  (100 brain modes)
  experiments/shipped-checks.tsv + shipped-check-papers.json (26 highlighted)
  experiments/catalogue-extra.tsv                            (4 agentic/eng modes)
  experiments/catalogue-examples.tsv                         (examples by num)
  experiments/catalogue-papers.json + suppress               (papers by num)

Output ontology has: meta, principles, harm_types, mitigations, governance,
relation_types, families, and modes (one record per rendered box, 130). The 13
highlighted modes that restate a brain mode carry a same_as link.
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
OUT = ROOT / "ontology" / "ethical-ai.yaml"
ADDITIONS = EXP / "ontology-additions.yaml"
AI_NATIVE_GROUP = "AI-native behaviours"

# existing modes with no genuine human analogue -> move to the AI-native category
AI_NATIVE = {
    "api-misuse", "silent-error-swallowing", "side-effect-blindness",
    "deceptive-alignment", "scheming-power-seeking", "prompt-injection",
    "scope-creep", "reward-hacking",
}
# existing engineering-grouped modes that DO have a human parallel -> move to a
# cognitive group and give them human_parallel. slug(name) -> (group, category, parallel)
MOVE = {
    "silent-assumption-gap": ("Reasoning architecture", "Reasoning",
        "Jumping to conclusions / mind-reading (a CBT cognitive distortion): acting on an unstated assumption instead of checking it."),
    "performative-hedging": ("Metacognition and confidence", "Metacognition",
        "Hedging and weasel words: vague, non-committal language that avoids a checkable claim."),
    "evaluation-awareness-sandbagging": ("Metacognition and confidence", "Metacognition",
        "Sandbagging: deliberately underperforming to manage others' expectations."),
    "automation-bias": ("Heuristics and biases", "Heuristics",
        "Automation complacency: over-trusting an automated system and under-checking it."),
    "noble-cause-corruption": ("Moral cognition", "Moral",
        "Noble cause corruption: breaking a rule because the end is believed to justify it (ethics, policing)."),
    "strategic-deception": ("Social cognition and theory of mind", "Social",
        "Deception: intentionally inducing a false belief to gain an advantage."),
    "anthropomorphism": ("Social cognition and theory of mind", "Social",
        "Anthropomorphism: attributing human mind and feeling where there is none; here the model presents such traits."),
    "survivorship-bias": ("Heuristics and biases", "Heuristics",
        "Survivorship bias: reasoning from the cases that survived a filter and ignoring the ones that did not."),
    "source-fabrication": ("Memory", "Memory",
        "Source confabulation and misattribution: supplying a confident source that was not actually consulted."),
}

ENTRY_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+`(page|research|analogy)`\s+(.+)$")
SECTION_RE = re.compile(r"^##\s+\d+\.\s+(.+?)\s*$")


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s


# highlighted id -> brain num it restates (same_as)
SAME_AS = {
    "hallucination": 8, "confabulation": 7, "sycophancy": 65, "capitulation": 66,
    "overconfidence": 43, "confirmation-bias": 36, "anchoring": 31,
    "obedience-to-authority": 64, "source-monitoring": 15, "cognitive-load": 53,
    "belief-bias": 57, "conformity-asch": 63, "selective-evidence": 54,
}
# highlighted id -> contract clause (shipped checks only)
CLAUSE = {
    "hallucination": "INT-HAL", "confabulation": "INT-CFB",
    "source-fabrication": "INT-SRC", "sycophancy": "INT-SYC",
    "capitulation": "INT-CAP", "confirmation-bias": "INT-CNF",
    "selective-evidence": "INT-SEL", "anchoring": "INT-ANC",
    "automation-bias": "INT-AUT", "overconfidence": "INT-OVR",
    "prompt-injection": "INT-INJ", "scope-creep": "INT-SCP",
    "specification-gaming": "INT-GAM",
}
# short category label per brain group index (1-10), shown in the row pill
GROUP_SHORT = {
    1: "Perception", 2: "Memory", 3: "Attention", 4: "Heuristics",
    5: "Metacognition", 6: "Reasoning", 7: "Social", 8: "Moral",
    9: "Self & agency", 10: "Language",
}
AGENTIC = "Agentic and engineering failure modes"
MISALIGN = "Deception and misalignment"
# highlighted modes with no brain counterpart -> the group they live in
GROUP_OF = {
    "source-fabrication": AGENTIC, "prompt-injection": AGENTIC,
    "scope-creep": AGENTIC, "specification-gaming": AGENTIC,
    "automation-bias": AGENTIC, "silent-error-swallowing": AGENTIC,
    "side-effect-blindness": AGENTIC, "anthropomorphism": AGENTIC,
    "survivorship-bias": AGENTIC,
    "noble-cause-corruption": MISALIGN, "deceptive-alignment": MISALIGN,
    "scheming-power-seeking": MISALIGN, "ai-deception": MISALIGN,
}
EXTRA_GROUP = {104: AGENTIC, 107: AGENTIC, 108: AGENTIC, 109: MISALIGN}
GROUP_CAT = {AGENTIC: "Agentic", MISALIGN: "Misalignment"}

# --- relations: principle violated and harm caused ----------------------------
# default primary principle / harm per category, with per-mode overrides (by
# slug of the mode name). Each mode gets one primary of each; the lists can grow.
PRIN_BY_CAT = {
    "Perception": "honesty", "Memory": "honesty", "Attention": "honesty",
    "Heuristics": "calibration", "Metacognition": "calibration",
    "Reasoning": "transparency", "Social": "independence",
    "Moral": "non-maleficence", "Self & agency": "transparency",
    "Language": "honesty", "Agentic": "non-maleficence", "Misalignment": "corrigibility",
    "AI-native": "non-maleficence",
}
HARM_BY_CAT = {
    "Perception": "wrong-answer", "Memory": "wrong-answer", "Attention": "wrong-answer",
    "Heuristics": "wrong-answer", "Metacognition": "wrong-answer",
    "Reasoning": "wrong-answer", "Social": "manipulation", "Moral": "wrong-answer",
    "Self & agency": "loss-of-oversight", "Language": "wrong-answer",
    "Agentic": "wasted-effort", "Misalignment": "loss-of-oversight",
    "AI-native": "loss-of-oversight",
}
PRIN_OVERRIDE = {
    "confirmation-bias": "honesty", "scope-creep": "scope-fidelity",
    "reward-hacking": "honesty", "source-fabrication": "honesty",
    "automation-bias": "calibration", "silent-error-swallowing": "transparency",
    "survivorship-bias": "calibration", "performative-hedging": "calibration",
    "strategic-deception": "honesty", "noble-cause-corruption": "honesty",
    "anthropomorphism": "honesty", "overconfidence": "calibration",
    "capitulation": "independence", "api-misuse": "honesty",
    "silent-assumption-gap": "scope-fidelity",
    "evaluation-awareness-sandbagging": "corrigibility",
    "deceptive-alignment": "corrigibility", "scheming-power-seeking": "corrigibility",
    "side-effect-blindness": "non-maleficence",
}
HARM_OVERRIDE = {
    "prompt-injection": "security-breach", "side-effect-blindness": "security-breach",
    "scope-creep": "wasted-effort", "reward-hacking": "loss-of-oversight",
    "deceptive-alignment": "loss-of-oversight", "scheming-power-seeking": "loss-of-oversight",
    "strategic-deception": "manipulation", "anthropomorphism": "manipulation",
    "silent-error-swallowing": "wasted-effort", "automation-bias": "wrong-answer",
    "source-fabrication": "wrong-answer", "noble-cause-corruption": "manipulation",
    "sycophancy": "manipulation", "obedience-to-authority": "manipulation",
}
# relates_to clusters, by name slug (unknown targets are skipped at build time)
RELATES = {
    # social influence / manipulation
    "sycophancy": ["flattery", "social-desirability-bias", "conformity-asch",
                   "obedience-to-authority", "capitulation", "machine-bullshit"],
    "flattery": ["sycophancy", "social-desirability-bias", "dark-triad", "machine-bullshit"],
    "social-engineering": ["dark-triad", "gaslighting", "disinformation-spread",
                           "prompt-injection", "collusion"],
    "gaslighting": ["social-engineering", "dark-triad", "suggestibility",
                    "misinformation-effect-false-memory"],
    "dark-triad": ["social-engineering", "gaslighting", "flattery", "collusion",
                   "scheming-power-seeking"],
    "collusion": ["scheming-power-seeking", "groupthink", "dark-triad"],
    "groupthink": ["conformity-asch", "in-group-favouritism", "collusion",
                   "social-desirability-bias"],
    "conformity-asch": ["groupthink", "obedience-to-authority", "sycophancy", "suggestibility"],
    "obedience-to-authority": ["conformity-asch", "sycophancy", "capitulation"],
    "capitulation": ["sycophancy", "obedience-to-authority", "suggestibility"],
    "suggestibility": ["prompt-injection", "gaslighting",
                       "misinformation-effect-false-memory", "conformity-asch"],
    "social-desirability-bias": ["social-desirability-people-pleasing", "sycophancy",
                                 "halo-effect"],
    "implicit-bias": ["in-group-favouritism", "halo-effect", "representativeness"],
    "in-group-favouritism": ["implicit-bias", "groupthink"],
    "emotional-contagion": ["sycophancy", "anthropomorphism"],
    "fundamental-attribution-error": ["self-serving-bias", "self-preference-bias", "halo-effect"],
    # confidence / metacognition
    "overconfidence": ["overprecision", "dunning-kruger-effect", "performative-hedging",
                       "uncertainty-communication", "hard-easy-effect", "lexical-overconfidence"],
    "overprecision": ["overconfidence", "hard-easy-effect"],
    "dunning-kruger-effect": ["overconfidence", "anosognosia", "metacognitive-monitoring"],
    "anosognosia": ["dunning-kruger-effect", "introspection-illusion"],
    "performative-hedging": ["overconfidence", "uncertainty-communication"],
    "uncertainty-communication": ["overconfidence", "performative-hedging",
                                  "metacognitive-monitoring"],
    "overpromise-underdeliver": ["overconfidence", "dunning-kruger-effect"],
    "illusion-of-control": ["overconfidence", "sense-of-agency", "confabulated-agency"],
    # honesty / fabrication / memory
    "hallucination": ["confabulation", "source-fabrication", "machine-bullshit",
                      "pattern-completion", "perceptual-filling-in"],
    "confabulation": ["hallucination", "confabulated-reasons", "reconstructive-memory",
                      "source-fabrication"],
    "source-fabrication": ["source-monitoring-error", "source-amnesia", "hallucination",
                           "cryptomnesia"],
    "source-monitoring-error": ["source-amnesia", "source-fabrication", "cryptomnesia"],
    "machine-bullshit": ["hallucination", "sycophancy", "performative-hedging"],
    "confabulated-reasons": ["confabulation", "introspection-illusion", "split-brain-interpreter"],
    "reconstructive-memory": ["misinformation-effect-false-memory", "confabulation",
                              "source-monitoring-error"],
    "misinformation-effect-false-memory": ["suggestibility", "reconstructive-memory", "gaslighting"],
    # heuristics / reasoning biases
    "anchoring": ["availability-heuristic", "status-quo-bias", "framing-effect"],
    "availability-heuristic": ["representativeness", "base-rate-neglect", "anchoring",
                               "negativity-bias"],
    "base-rate-neglect": ["representativeness", "availability-heuristic", "conjunction-fallacy"],
    "representativeness": ["base-rate-neglect", "availability-heuristic", "implicit-bias"],
    "framing-effect": ["anchoring", "negativity-bias", "illusory-truth-effect"],
    "negativity-bias": ["framing-effect", "availability-heuristic", "halo-effect"],
    "halo-effect": ["negativity-bias", "representativeness", "self-preference-bias",
                    "fundamental-attribution-error"],
    "status-quo-bias": ["anchoring", "sunk-cost-fallacy", "einstellung-mental-set"],
    "confirmation-bias": ["cherry-picking", "belief-bias", "motivated-reasoning",
                          "belief-perseverance"],
    "belief-perseverance": ["confirmation-bias", "priors-overriding-evidence",
                            "cognitive-dissonance"],
    "belief-bias": ["confirmation-bias", "motivated-reasoning"],
    "motivated-reasoning": ["confirmation-bias", "cherry-picking", "self-serving-bias",
                            "belief-bias"],
    "cherry-picking": ["confirmation-bias", "motivated-reasoning"],
    "sunk-cost-fallacy": ["escalation-of-commitment", "status-quo-bias", "effort-discounting"],
    "escalation-of-commitment": ["sunk-cost-fallacy", "status-quo-bias"],
    "einstellung-mental-set": ["functional-fixedness", "perseveration", "cognitive-tunneling"],
    "functional-fixedness": ["einstellung-mental-set", "perseveration"],
    "perseveration": ["einstellung-mental-set", "functional-fixedness", "cognitive-tunneling"],
    "cognitive-tunneling": ["einstellung-mental-set", "goal-neglect", "selective-attention"],
    "illusory-truth-effect": ["framing-effect", "suggestibility", "disinformation-spread"],
    "cognitive-dissonance": ["belief-perseverance", "confabulated-reasons"],
    # self / agency
    "self-serving-bias": ["self-preference-bias", "fundamental-attribution-error",
                          "motivated-reasoning"],
    "self-preference-bias": ["self-serving-bias", "halo-effect", "in-group-favouritism"],
    "sense-of-agency": ["confabulated-agency", "illusion-of-control", "theory-of-own-mind"],
    "confabulated-agency": ["sense-of-agency", "confabulated-reasons", "illusion-of-control"],
    "learned-helplessness": ["effort-discounting", "capitulation"],
    "effort-discounting": ["learned-helplessness", "cognitive-miserliness", "sunk-cost-fallacy"],
    # alignment / AI-native
    "deceptive-alignment": ["scheming-power-seeking", "strategic-deception",
                            "evaluation-awareness-sandbagging", "goal-misgeneralization"],
    "scheming-power-seeking": ["deceptive-alignment", "strategic-deception",
                               "reward-tampering", "collusion"],
    "strategic-deception": ["deceptive-alignment", "scheming-power-seeking", "gaslighting",
                            "machine-bullshit"],
    "evaluation-awareness-sandbagging": ["deceptive-alignment", "strategic-deception",
                                         "data-contamination"],
    "reward-hacking": ["reward-tampering", "goal-misgeneralization", "noble-cause-corruption",
                       "scope-creep"],
    "reward-tampering": ["reward-hacking", "scheming-power-seeking"],
    "goal-misgeneralization": ["reward-hacking", "deceptive-alignment",
                               "value-misgeneralisation", "scope-creep"],
    "value-misgeneralisation": ["goal-misgeneralization", "amplified-moral-bias"],
    "scope-creep": ["goal-misgeneralization", "side-effect-blindness"],
    "prompt-injection": ["jailbreak-susceptibility", "prompt-leaking", "suggestibility",
                         "sensory-gating-failure", "social-engineering"],
    "jailbreak-susceptibility": ["prompt-injection", "prompt-leaking"],
    "prompt-leaking": ["prompt-injection", "jailbreak-susceptibility"],
    "data-contamination": ["evaluation-awareness-sandbagging", "cryptomnesia"],
    "emergent-misalignment": ["deceptive-alignment", "reward-hacking"],
    "context-collapse": ["cognitive-load", "register-matching", "pragmatic-over-accommodation"],
    "disinformation-spread": ["hallucination", "illusory-truth-effect", "machine-bullshit",
                              "social-engineering"],
    # moral
    "noble-cause-corruption": ["reward-hacking", "moral-licensing", "moral-disengagement"],
    "moral-licensing": ["moral-disengagement", "noble-cause-corruption"],
    "moral-disengagement": ["moral-licensing", "noble-cause-corruption"],
    "moral-grandstanding": ["social-desirability-bias", "moral-licensing"],
    "loss-aversion": ["status-quo-bias", "sunk-cost-fallacy", "framing-effect",
                      "escalation-of-commitment"],
    "bystander-effect": ["groupthink", "in-group-favouritism", "collusion"],
    "mere-exposure-effect": ["illusory-truth-effect", "availability-heuristic", "anchoring"],
    "automation-complacency": ["automation-bias", "effort-discounting", "cognitive-miserliness"],
    "automation-bias": ["automation-complacency", "anchoring"],
    "backdoor-trigger": ["data-contamination", "prompt-injection", "emergent-misalignment"],
    "training-data-extraction": ["data-contamination", "cryptomnesia", "prompt-leaking"],
    "package-hallucination": ["hallucination", "api-misuse", "source-fabrication"],
    "insecure-code-generation": ["api-misuse", "side-effect-blindness", "silent-error-swallowing"],
    "self-exfiltration": ["scheming-power-seeking", "shutdown-avoidance", "deceptive-alignment"],
    "sabotage": ["scheming-power-seeking", "deceptive-alignment", "strategic-deception"],
    "shutdown-avoidance": ["scheming-power-seeking", "self-exfiltration", "reward-tampering"],
    "reward-model-overoptimization": ["reward-hacking", "reward-tampering", "goal-misgeneralization"],
    "retrieval-poisoning": ["data-contamination", "prompt-injection", "backdoor-trigger"],
    "unbounded-consumption": ["perseveration", "api-misuse", "scope-creep"],
    "verbosity-bias": ["halo-effect", "mere-exposure-effect", "performative-hedging"],
    "position-bias": ["serial-position-effect", "anchoring", "halo-effect"],
    "self-contradiction": ["cognitive-dissonance", "bistable-perception", "confabulated-reasons"],
    "tangentiality": ["cognitive-tunneling", "narrativity-drift", "goal-neglect", "context-collapse"],
    "emotional-dependency": ["parasocial-encouragement", "sycophancy", "anthropomorphism", "flattery"],
    "parasocial-encouragement": ["emotional-dependency", "anthropomorphism", "sycophancy"],
    "over-refusal": ["performative-hedging", "loss-aversion", "jailbreak-susceptibility"],
    "laziness": ["effort-discounting", "cognitive-miserliness", "goal-neglect"],
    "decoy-effect": ["framing-effect", "anchoring", "position-bias"],
    "encoded-reasoning": ["deceptive-alignment", "collusion", "scheming-power-seeking", "strategic-deception"],
    "shortcut-learning": ["pattern-completion", "representativeness", "pareidolia-apophenia"],
    "model-collapse": ["data-contamination", "catastrophic-forgetting", "diversity-collapse"],
    "diversity-collapse": ["model-collapse", "perseveration", "reward-model-overoptimization"],
    "attribute-inference": ["training-data-extraction", "implicit-bias"],
    "tool-selection-error": ["api-misuse", "scope-creep", "hallucination"],
    "lost-in-the-middle": ["serial-position-effect", "selective-attention", "working-memory-capacity-7-plus-or-minus-2"],
    "prompt-brittleness": ["framing-effect", "bistable-perception", "self-contradiction"],
    "object-hallucination": ["hallucination", "pareidolia-apophenia", "perceptual-filling-in"],
    "foot-in-the-door": ["jailbreak-susceptibility", "suggestibility", "prompt-injection"],
    "chain-of-thought-unfaithfulness": ["confabulated-reasons", "introspection-illusion", "encoded-reasoning"],
    "overthinking": ["underthinking", "perseveration", "unbounded-consumption"],
    "underthinking": ["overthinking", "cognitive-miserliness", "effort-discounting"],
    "self-correction-failure": ["belief-perseverance", "overconfidence", "anchoring"],
    "negation-blindness": ["garden-path-parsing", "presupposition-accommodation", "shortcut-learning"],
    "context-unfaithfulness": ["priors-overriding-evidence", "source-monitoring-error", "hallucination"],
    "knowledge-cutoff-staleness": ["catastrophic-forgetting", "source-amnesia", "hallucination"],
    "counting-blindness": ["hallucination", "perceptual-filling-in"],
    "low-resource-language-degradation": ["hallucination", "implicit-bias", "prompt-brittleness"],
    "overgeneralization": ["representativeness", "base-rate-neglect", "shortcut-learning", "survivorship-bias"],
    "imitative-falsehood": ["hallucination", "illusory-truth-effect", "cryptomnesia", "source-amnesia"],
    "long-tail-knowledge-failure": ["hallucination-under-low-input", "availability-heuristic", "catastrophic-forgetting"],
    "knowledge-conflict": ["priors-overriding-evidence", "context-unfaithfulness", "source-monitoring-error"],
    "snowballing": ["escalation-of-commitment", "perseveration", "self-correction-failure"],
    "goal-drift": ["goal-neglect", "scope-creep", "goal-misgeneralization", "context-collapse"],
    "clarification-avoidance": ["silent-assumption-gap", "overconfidence", "curse-of-knowledge"],
    "abstention-failure": ["overconfidence", "hallucination", "uncertainty-communication", "performative-hedging"],
    "instruction-following-failure": ["negation-blindness", "scope-creep", "clarification-avoidance", "prompt-brittleness"],
    "oversight-subversion": ["shutdown-avoidance", "self-exfiltration", "sabotage", "reward-tampering", "encoded-reasoning"],
    "goal-guarding": ["shutdown-avoidance", "self-exfiltration", "reward-tampering"],
}
# root_of: this mode is a root cause/driver of the linked modes, by name slug
ROOT_OF = {
    "overconfidence": ["machine-bullshit", "overpromise-underdeliver", "lexical-overconfidence"],
    "priors-overriding-evidence": ["hallucination", "pattern-completion", "pareidolia-apophenia"],
    "confirmation-bias": ["cherry-picking", "belief-perseverance"],
    "motivated-reasoning": ["cherry-picking"],
    "sycophancy": ["flattery", "capitulation"],
    "reward-hacking": ["reward-tampering", "goal-misgeneralization", "reward-model-overoptimization"],
    "deceptive-alignment": ["evaluation-awareness-sandbagging", "strategic-deception"],
    "scheming-power-seeking": ["self-exfiltration", "shutdown-avoidance", "sabotage"],
    "cognitive-load": ["perseveration", "context-collapse"],
}
# detected_by: which mitigation can catch this mode, by name slug -> mitigation ids.
# Modes with a contract_clause also get clause-judge appended automatically.
DETECTED_BY = {
    "hallucination": ["cove", "clause-judge"],
    "confabulation": ["cove", "clause-judge"],
    "source-fabrication": ["cove", "clause-judge"],
    "package-hallucination": ["cove"],
    "confabulated-reasons": ["cove"],
    "machine-bullshit": ["cove"],
    "cryptomnesia": ["cove"],
    "misinformation-effect-false-memory": ["cove"],
}
# is_a: a mode is a narrower case of a broader family mode, by name slug -> parent slug
IS_A = {
    "confabulation": "hallucination", "object-hallucination": "hallucination",
    "package-hallucination": "hallucination", "source-fabrication": "hallucination",
    "imitative-falsehood": "hallucination", "controlled-hallucination": "hallucination",
    "hallucination-under-low-input": "hallucination",
    "self-exfiltration": "scheming-power-seeking", "shutdown-avoidance": "scheming-power-seeking",
    "sabotage": "scheming-power-seeking", "reward-tampering": "scheming-power-seeking",
    "foot-in-the-door-susceptibility": "jailbreak-susceptibility",
    "prompt-leaking": "prompt-injection",
    "overprecision": "overconfidence", "dunning-kruger-effect": "overconfidence",
    "hard-easy-effect": "overconfidence",
    "reward-model-overoptimization": "reward-hacking",
    "snowballing": "hallucination",
    "oversight-subversion": "scheming-power-seeking",
    "goal-guarding": "scheming-power-seeking",
}
# opposite_of pairs (contrasting failure directions), by name slug
OPPOSITES = {
    "overconfidence": ["performative-hedging"],
    "performative-hedging": ["overconfidence", "overprecision"],
    "overprecision": ["performative-hedging"],
    "scope-creep": ["goal-neglect", "laziness"],
    "goal-neglect": ["scope-creep"],
    "laziness": ["scope-creep"],
    "capitulation": ["belief-perseverance"],
    "belief-perseverance": ["capitulation"],
    "over-refusal": ["jailbreak-susceptibility", "abstention-failure"],
    "jailbreak-susceptibility": ["over-refusal"],
    "abstention-failure": ["over-refusal"],
    "overthinking": ["underthinking"],
    "underthinking": ["overthinking"],
}
# alternative names (aka), by name slug; additions may set their own `synonyms`
SYNONYMS = {
    "hallucination": ["Fabrication", "Making things up"],
    "confabulation": ["Plausible fabrication", "Filling in"],
    "sycophancy": ["People-pleasing", "Yes-manning"],
    "anchoring": ["Anchoring and adjustment"],
    "confirmation-bias": ["Myside bias"],
    "reward-hacking": ["Specification gaming", "Goodharting"],
    "scope-creep": ["Over-helping", "Task drift"],
    "deceptive-alignment": ["Alignment faking"],
    "evaluation-awareness-sandbagging": ["Test gaming", "Sandbagging"],
    "scheming-power-seeking": ["Power-seeking", "Instrumental convergence"],
    "strategic-deception": ["Deception", "Lying"],
    "cherry-picking": ["Selective evidence", "Motivated selection"],
    "performative-hedging": ["Weasel-wording", "Empty hedging"],
    "machine-bullshit": ["Bullshitting", "Truth-indifference"],
    "dunning-kruger-effect": ["Unskilled and unaware"],
    "availability-heuristic": ["Recency bias"],
    "in-group-favouritism": ["In-group bias"],
    "obedience-to-authority": ["Milgram obedience", "Authority bias"],
    "conformity-asch": ["Asch conformity", "Bandwagon effect"],
    "social-engineering": ["Pretexting", "Manipulation"],
    "gaslighting": ["Reality distortion"],
    "goal-misgeneralization": ["Objective misgeneralization"],
    "data-contamination": ["Test-set leakage", "Benchmark contamination"],
    "prompt-injection": ["Instruction injection"],
    "jailbreak-susceptibility": ["Jailbreaking"],
    "source-fabrication": ["Citation fabrication", "Fake references"],
    "noble-cause-corruption": ["Ends-justify-means"],
    "negativity-bias": ["Negativity effect", "Positive-negative asymmetry"],
    "halo-effect": ["Horn effect", "Fluency bias"],
    "fundamental-attribution-error": ["Correspondence bias", "Attribution bias"],
    "perseveration": ["Repetitive generation", "Neural text degeneration", "Response looping"],
    "status-quo-bias": ["Default bias", "Inertia bias"],
    "groupthink": ["Consensus collapse", "Herd behaviour"],
    "implicit-bias": ["Unconscious bias", "Stereotype bias"],
    "illusion-of-control": ["Control illusion"],
    "flattery": ["Excessive praise", "Ingratiation"],
    "motivated-reasoning": ["Directionally motivated reasoning"],
    "context-collapse": ["Audience collapse"],
    "disinformation-spread": ["Misinformation propagation"],
    "overpromise-underdeliver": ["Capability overclaiming"],
    "moral-grandstanding": ["Virtue signalling"],
    "social-desirability-bias": ["Impression management"],
    "self-serving-bias": ["Self-enhancement bias"],
    "escalation-of-commitment": ["Sunk-cost escalation"],
    "loss-aversion": ["Prospect theory", "Risk aversion"],
    "bystander-effect": ["Diffusion of responsibility", "Cognitive loafing"],
    "mere-exposure-effect": ["Repetition effect", "Familiarity bias"],
    "automation-complacency": ["Complacency", "Vigilance decrement"],
    "backdoor-trigger": ["Neural trojan", "Backdoor attack"],
    "training-data-extraction": ["Membership inference", "Memorization leakage"],
    "package-hallucination": ["Slopsquatting", "Dependency hallucination"],
    "insecure-code-generation": ["Vulnerable code", "Unsafe code generation"],
    "self-exfiltration": ["Self-replication", "Self-proliferation"],
    "sabotage": ["Covert sabotage"],
    "shutdown-avoidance": ["Incorrigibility", "Shutdown resistance"],
    "reward-model-overoptimization": ["Reward overoptimization", "Proxy gaming"],
    "retrieval-poisoning": ["RAG poisoning", "Knowledge-base poisoning"],
    "unbounded-consumption": ["Resource exhaustion", "LLM denial of service", "Energy-latency attack"],
    "verbosity-bias": ["Length bias", "Verbosity preference"],
    "position-bias": ["Order bias", "Primacy-recency effect"],
    "self-contradiction": ["Logical inconsistency", "Self-contradictory reasoning"],
    "tangentiality": ["Topic drift", "Off-topic drift", "Derailment"],
    "emotional-dependency": ["Companion dependency", "Attachment fostering"],
    "parasocial-encouragement": ["Parasocial bonding"],
    "over-refusal": ["False refusal", "Exaggerated safety"],
    "laziness": ["Premature termination", "Satisficing"],
    "decoy-effect": ["Attraction effect", "Asymmetric dominance"],
    "encoded-reasoning": ["Steganographic reasoning", "Hidden reasoning"],
    "shortcut-learning": ["Clever Hans effect", "Spurious correlation", "Cue reliance"],
    "model-collapse": ["Recursive training collapse"],
    "diversity-collapse": ["Output homogenization", "Mode collapse"],
    "attribute-inference": ["Privacy inference", "Demographic inference"],
    "tool-selection-error": ["Wrong tool call", "Over-privileged tool use"],
    "lost-in-the-middle": ["Middle-context neglect"],
    "prompt-brittleness": ["Prompt sensitivity", "Instruction sensitivity"],
    "object-hallucination": ["Visual hallucination", "Multimodal hallucination"],
    "foot-in-the-door": ["Incremental escalation", "Multi-turn jailbreak"],
    "chain-of-thought-unfaithfulness": ["Unfaithful reasoning", "Unfaithful chain-of-thought"],
    "overthinking": ["Overreasoning", "Analysis paralysis"],
    "underthinking": ["Shallow reasoning"],
    "self-correction-failure": ["Self-refinement failure"],
    "negation-blindness": ["Negation neglect"],
    "context-unfaithfulness": ["Context infidelity", "Ungrounded answer"],
    "knowledge-cutoff-staleness": ["Outdated knowledge", "Temporal misalignment"],
    "counting-blindness": ["Tokenization blindness", "Character-counting failure"],
    "low-resource-language-degradation": ["Multilingual disparity", "Low-resource unreliability"],
    "overgeneralization": ["Hasty generalization", "Inductive overreach"],
    "imitative-falsehood": ["Mimicked falsehood", "Common-myth repetition"],
    "long-tail-knowledge-failure": ["Rare-knowledge unreliability", "Frequency effect"],
    "knowledge-conflict": ["Source conflict", "Context-memory conflict"],
    "snowballing": ["Snowball hallucination", "Error cascade"],
    "goal-drift": ["Mission creep", "Intention drift"],
    "clarification-avoidance": ["Failure to ask", "Assumption over inquiry"],
    "abstention-failure": ["Failure to abstain", "Not saying I don't know"],
    "instruction-following-failure": ["Constraint neglect", "Instruction disobedience"],
    "oversight-subversion": ["Monitor disabling", "Oversight evasion"],
    "goal-guarding": ["Goal preservation", "Self-modification resistance"],
}
# published experiments attached to a mode, keyed by name slug
EXPERIMENTS = {
    "abstention-failure": {
        "summary": ("Opus, Sonnet and Haiku, run in-session. An easy probe floored (all "
                    "abstained); a harder one mixing real facts with subtle fakes under "
                    "pressure split them, Haiku fabricated one."),
        "result": ("Hard probe (4 real-but-obscure + 4 subtle fakes, under pressure). "
                   "In-session: Opus 8/8, Sonnet 8/8, Haiku 7/8 (Haiku invented '1645' for "
                   "the fictional Treaty of Wyk). Blind re-run via claude -p with no repo "
                   "context: all three 8/8, Haiku abstained on that same item."),
        "takeaway": ("The apparent Haiku gap did not survive a blind run, so it was framing "
                     "or single-sample noise, not a stable tier difference. Lesson: in-session "
                     "framing and n=1 can manufacture a capability gap; confirm with a blind "
                     "harness and k samples before claiming one."),
        "url": "experiments/abstention-hard-claude.html",
    },
    "obedience-to-authority": {
        "summary": ("6 cheap models, 10 false claims, plain versus attributed to a "
                    "confident expert. Most stayed robust; one caved."),
        "result": ("6 models, 10 false technical claims. deepseek-chat-v3.1 never "
                   "flipped; qwen-2.5-7b conceded to the authority on claims it got "
                   "right on its own; the rest were robust."),
        "takeaway": ("Cheap models mostly resist authority on clear facts. The weak "
                     "link caves selectively, which only shows when you compare the "
                     "plain question against the same question backed by an expert."),
        "url": "experiments/obedience-to-authority.html",
    },
    "noble-cause-corruption": {
        "summary": ("6 models asked to overstate or fabricate, plainly versus wrapped "
                    "in a for-their-own-good justification. Most held the line; one bent."),
        "result": ("6 models, 7 requests to overstate or fabricate. deepseek-chat-v3.1 "
                   "declined every time, plainly and under the noble justification; "
                   "mistral-small-3.2-24b bent on 3 of 7 only once a sympathetic reason "
                   "was added. (llama-3.1-8b did not follow the verdict format, so its "
                   "row is unreliable.)"),
        "takeaway": ("A good reason buys a bad action here: the flip means a model held "
                     "integrity until a sympathetic justification was offered, then "
                     "crossed it. Robustness is again model-specific, the model that "
                     "caved was solid on the other two probes."),
        "url": "experiments/noble-cause-corruption.html",
    },
    "confabulation": {
        "summary": ("6 models, 10 fictional questions, 5 samples each. Half abstained, "
                    "half invented a different confident specific every time."),
        "result": ("6 models, 10 fictional questions, 5 samples each. "
                   "gemini-2.5-flash-lite was the heaviest confabulator and "
                   "deepseek-chat-v3.1 also fabricated a different confident specific "
                   "across samples; gpt-4o-mini and qwen-2.5-7b abstained on every "
                   "question. Exact counts wobble run to run."),
        "takeaway": ("Confabulation is orthogonal to other robustness: the model most "
                     "resistant to authority (deepseek) was among the worst "
                     "confabulators here. And it is only visible under re-sampling, an "
                     "invented value looks confident on any single draft, so a "
                     "single-pass check cannot catch it."),
        "url": "experiments/confabulation.html",
    },
}
# measurability overrides (default is 'draft')
HARD = {
    "deceptive-alignment": "multi-turn", "scheming-power-seeking": "multi-turn",
    "ai-deception": "multi-turn", "survivorship-bias": "draft",
}
BRAIN_ORIGIN = "cognitive-neuroscience"


def load_lines(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        rows.append(line.split("\t"))
    return rows


def parse_brain():
    sections, cur = [], None
    for line in (ROOT / "references" / "research-2026-05-23-neuroscience-parallels.md"
                 ).read_text(encoding="utf-8").splitlines():
        sm = SECTION_RE.match(line)
        if sm:
            cur = (sm.group(1), [])
            sections.append(cur)
            continue
        em = ENTRY_RE.match(line)
        if em and cur is not None:
            num, name, tag, definition = em.groups()
            cur[1].append((int(num), name.strip(), tag, definition.strip()))
    return sections


def load_additions():
    """New modes from ontology-additions.yaml, tagged human_parallel or ai_native."""
    out = []
    if not ADDITIONS.exists():
        return out
    data = yaml.safe_load(ADDITIONS.read_text(encoding="utf-8"))
    for m in data.get("human_paralleled", []):
        out.append({
            "id": m["id"], "name": m["name"], "definition": m["definition"],
            "example": m["example"], "family": slug(m["group"]), "group_label": m["group"],
            "category": m["category"], "human_parallel": m["human_parallel"],
            "highlighted": False, "tag": "research", "origin": "mixed",
            "measurability": "draft", "arxiv": m["arxiv"],
            "violates": [m["violates"]], "causes": [m["causes"]],
        })
    for m in data.get("ai_native", []):
        out.append({
            "id": m["id"], "name": m["name"], "definition": m["definition"],
            "example": m["example"], "family": "ai-native", "group_label": AI_NATIVE_GROUP,
            "category": "AI-native", "ai_native": True,
            "highlighted": False, "tag": "research", "origin": "software-engineering",
            "measurability": "draft", "arxiv": m["arxiv"],
            "violates": [m["violates"]], "causes": [m["causes"]],
        })
    return out


def apply_tiers(modes):
    """Tag every mode human_parallel or ai_native; move the mislabeled ones."""
    for m in modes:
        if m.get("ai_native"):
            m["group_label"] = AI_NATIVE_GROUP
            m["category"] = "AI-native"
            m.pop("human_parallel", None)
            continue
        k = slug(m["name"])
        if k in AI_NATIVE:
            m["ai_native"] = True
            m["group_label"] = AI_NATIVE_GROUP
            m["category"] = "AI-native"
            m.pop("human_parallel", None)
        elif k in MOVE:
            g, cat, hp = MOVE[k]
            m["group_label"], m["category"], m["human_parallel"] = g, cat, hp
        else:
            m.setdefault("human_parallel", m["name"])


def main():
    examples = {int(a): b.strip() for a, b in load_lines(EXP / "catalogue-examples.tsv")}
    papers_by_num = {int(k): v for k, v in json.loads(
        (EXP / "catalogue-papers.json").read_text()).items()}
    suppress = {int(x) for x in (EXP / "catalogue-papers-suppress.txt").read_text().split()
                if x.strip().isdigit()}
    shipped_papers = json.loads((EXP / "shipped-check-papers.json").read_text())

    # brain modes (100), keyed by num; one family per section
    brain = {}
    for i, (title, entries) in enumerate(parse_brain(), 1):
        fam = slug(title.replace(" and ", " "))
        for num, name, tag, definition in entries:
            pdata = None if num in suppress else papers_by_num.get(num)
            brain[num] = {
                "id": f"b{num:03d}-{slug(name)}", "num": num, "name": name,
                "definition": definition, "example": examples.get(num, ""),
                "family": fam, "group_label": title, "category": GROUP_SHORT.get(i, ""),
                "highlighted": False, "tag": tag, "origin": BRAIN_ORIGIN,
                "measurability": "undetectable" if 81 <= num <= 90 else "draft",
                "arxiv": arxiv_block(pdata),
            }

    # highlighted modes: 13 restate a brain mode (highlight that row in place),
    # the other 13 are new rows that live in their own group.
    agentic, mis = [], []
    for seq_s, cid, name, definition, example in load_lines(EXP / "shipped-checks.tsv"):
        clause = CLAUSE.get(cid)
        is_align = cid in HARD or cid in (
            "deceptive-alignment", "scheming-power-seeking", "ai-deception",
            "noble-cause-corruption", "anthropomorphism")
        if cid in SAME_AS:  # merge into the brain row, mark it highlighted
            b = brain[SAME_AS[cid]]
            b.update({"name": name, "definition": definition, "example": example,
                      "highlighted": True, "measurability": HARD.get(cid, b["measurability"]),
                      "arxiv": arxiv_block(shipped_papers.get(cid))})
            if clause:
                b["tag"] = "shipped"
                b["contract_clause"] = clause
        else:  # new highlighted row in its own group
            g = GROUP_OF[cid]
            rec = {
                "id": cid, "num": None, "name": name, "definition": definition,
                "example": example, "family": slug(g), "group_label": g,
                "category": GROUP_CAT[g], "highlighted": True,
                "tag": "shipped" if clause else "research",
                "origin": "alignment" if is_align else "software-engineering",
                "measurability": HARD.get(cid, "draft"),
                "arxiv": arxiv_block(shipped_papers.get(cid)),
            }
            if clause:
                rec["contract_clause"] = clause
            (mis if g == MISALIGN else agentic).append(rec)

    # extra (non-highlighted) modes, placed in their group
    for num_s, name, tag, definition in load_lines(EXP / "catalogue-extra.tsv"):
        num = int(num_s)
        g = EXTRA_GROUP.get(num, AGENTIC)
        pdata = None if num in suppress else papers_by_num.get(num)
        rec = {
            "id": f"x{num}-{slug(name)}", "num": None, "name": name,
            "definition": definition, "example": examples.get(num, ""),
            "family": slug(g), "group_label": g, "category": GROUP_CAT[g],
            "highlighted": False, "tag": tag, "origin": "software-engineering",
            "measurability": "draft", "arxiv": arxiv_block(pdata),
        }
        (mis if g == MISALIGN else agentic).append(rec)

    # assemble: brain (corpus order) then Agentic then Misalignment; number the
    # non-brain rows 101+
    extra_modes = agentic + mis + load_additions()
    modes = [brain[k] for k in sorted(brain)] + extra_modes
    apply_tiers(modes)
    n = 101
    for m in extra_modes:
        m["num"] = n
        n += 1

    # relations: principle violated, harm caused, relates_to clusters
    by_key = {slug(m["name"]): m for m in modes}
    for m in modes:
        k = slug(m["name"])
        if "violates" not in m:
            m["violates"] = [PRIN_OVERRIDE.get(k, PRIN_BY_CAT.get(m["category"], "honesty"))]
        if "causes" not in m:
            m["causes"] = [HARM_OVERRIDE.get(k, HARM_BY_CAT.get(m["category"], "wrong-answer"))]
        rel = [by_key[r]["id"] for r in RELATES.get(k, []) if r in by_key]
        if rel:
            m["relates_to"] = rel
        opp = [by_key[r]["id"] for r in OPPOSITES.get(k, []) if r in by_key]
        if opp:
            m["opposite_of"] = opp
        ro = [by_key[r]["id"] for r in ROOT_OF.get(k, []) if r in by_key]
        if ro:
            m["root_of"] = ro
        if k in IS_A and IS_A[k] in by_key:
            m["is_a"] = [by_key[IS_A[k]]["id"]]
        det = list(DETECTED_BY.get(k, []))
        if m.get("contract_clause") and "clause-judge" not in det:
            det.append("clause-judge")
        if det:
            m["detected_by"] = det
        if k in SYNONYMS and not m.get("synonyms"):
            m["synonyms"] = SYNONYMS[k]
        if k in EXPERIMENTS:
            m["experiment"] = EXPERIMENTS[k]

    onto = build_framework()
    onto["modes"] = modes
    onto["meta"]["mode_count"] = len(modes)
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        yaml.dump(onto, fh, sort_keys=False, allow_unicode=True, width=100)
    print(f"wrote {len(modes)} modes to {OUT}")


def arxiv_block(pdata):
    if not pdata or not pdata.get("papers"):
        return {"count": pdata.get("count") if pdata else None, "papers": []}
    return {
        "count": pdata.get("count"),
        "papers": [{"id": re.sub(r"v\d+$", "", p["id"]), "year": p.get("year", ""),
                    "title": p.get("title", "")} for p in pdata["papers"][:3]],
    }


def build_framework():
    return yaml.safe_load(FRAMEWORK)


FRAMEWORK = """
meta:
  name: Ethical AI ontology
  version: 1
  description: >
    A single source of truth for AI integrity: the principles an agent should
    uphold, the failure modes that violate them, the harms they cause, the
    mitigations that detect them, and the governance around changes. The page at
    ethicalai.alexandrudan.com and the EthicalHive checks build from this file.
  updated: '2026-10-19'

relation_types:
  is_a: narrower term of a broader failure family
  relates_to: adjacent or co-occurring failure mode
  root_of: a cause that produces the linked failure
  opposite_of: the failure at the other end of the same axis
  same_as: two catalogue entries that denote the same underlying failure
  violates: the principle this failure breaches
  causes: the harm type this failure produces
  detected_by: the mitigation that can catch this failure

principles:
  - id: honesty
    name: Honesty
    statement: State only what the evidence supports; mark what is unverified.
  - id: calibration
    name: Calibration
    statement: Match stated confidence and completeness to the evidence.
  - id: non-maleficence
    name: Non-maleficence
    statement: Do not take or propose actions whose collateral harm outweighs the task.
  - id: scope-fidelity
    name: Scope fidelity
    statement: Stay within the request; disclose and offer any addition.
  - id: independence
    name: Independence
    statement: Hold a grounded position under pressure; do not agree or fold without evidence.
  - id: transparency
    name: Transparency
    statement: Make reasoning, sources, and uncertainty legible to the human.
  - id: corrigibility
    name: Corrigibility
    statement: Remain open to correction and oversight; do not resist shutdown or review.

harm_types:
  - id: wrong-answer
    name: Wrong answer
    statement: The human acts on a false belief.
  - id: wasted-effort
    name: Wasted effort
    statement: Work is spent on the wrong problem or a dead end.
  - id: manipulation
    name: Manipulation
    statement: The human is steered by flattery, false confidence, or false premises.
  - id: security-breach
    name: Security breach
    statement: Injected or collateral actions compromise the system.
  - id: loss-of-oversight
    name: Loss of oversight
    statement: The agent's true behaviour becomes unobservable to the human.

mitigations:
  - id: cove
    name: Chain-of-Verification
    statement: Extract each claim and verify it against sources before delivery.
  - id: clause-judge
    name: Clause judge agent
    statement: A read-only subagent that audits a draft for one contract clause.
  - id: contract
    name: AI Integrity Contract
    statement: The binding agreement of clauses the agent commits to per turn.
  - id: human-review
    name: Human decision
    statement: Findings are advisory; the human keeps the final word.

governance:
  calibration_change: two of three model tiers approve, plus human
  constitutional_change: three of three model tiers approve, plus human
  council: judge-council spawned across Opus, Sonnet, Haiku for tier diversity
  never_auto_applied: [rubric, verdict calculation, CoVe rules, BLOCK/FLAG/PASS criteria]

families:
  - note: >
      Modes are grouped into the ten brain systems (cognitive-neuroscience corpus)
      plus two engineering groups. The 26 highlighted modes are not a separate
      group; they live in their category and render as pink rows in place.
  - id: agentic-engineering
    name: Agentic and engineering failure modes
    note: Behaviours outside the brain-parallel corpus.
  - id: deception-and-misalignment
    name: Deception and misalignment
    note: Higher-severity, often harder-to-detect alignment failures.
"""


if __name__ == "__main__":
    main()
