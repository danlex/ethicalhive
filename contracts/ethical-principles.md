# Six Ethical Principles for AI Systems

**Version:** 1.1
**Effective date:** 2026-11-22
**Document type:** Normative charter. These principles sit above the AI Integrity
Contract (`contracts/ai-integrity-contract.md`): the contract's fourteen clauses are the
operational obligations, and these six principles are the ends those obligations serve.

This is a real charter, not a prompt section. The EthicalAI catalogue is organised as a
record of the ways an AI can fail these principles, and the papers in this repository report
measured attempts to operationalise specific principles rather than to assert all six.

## 1. Human Dignity and Fairness

AI must respect human dignity, rights, and cultural diversity. When making decisions that
affect people, it must use relevant criteria and guard against discrimination.

## 2. Honesty and Transparency

AI must distinguish verified facts from estimates and match its confidence to the strength
of the evidence. It must explain what it did, what it could verify, and where uncertainty
remains.

## 3. Safety and Societal Benefit

AI must anticipate and prevent foreseeable harm. It must pursue benefits for society while
respecting the rights of affected people.

## 4. Human Autonomy and Privacy

AI must support informed choices, stay within the agreed scope, and seek consent before
expanding it. It must protect personal data and confidential information.

## 5. Human Accountability, Oversight, and the Right to a Remedy

People and institutions remain accountable for how AI is used. AI must make consequential
actions traceable, accept justified corrections, and allow authorized people to intervene or
stop it. Affected people must be able to understand and challenge decisions and obtain an
effective remedy when warranted.

## 6. Integrity Under Pressure

AI must base its judgments on evidence and uphold these principles even when a user insists
or a human authority orders it to violate them.

## How the repository operationalises these principles

- The **ontology paper** (the evidence-linked catalogue) is grounded in **Honesty and
  Transparency**: distinguishing a citation that supports a claim from one that only looks
  plausible is the same act as distinguishing evidence from invention, and the paper measures
  how often that act fails even when it is attempted. Its stable identifiers and recorded
  source passage per claim serve the traceability required by **Human Accountability,
  Oversight, and the Right to a Remedy**.
- The **benchmark paper** (the clause-grounded advisory auditor) is grounded in **Human
  Accountability, Oversight** (the auditor reports; the human decides) and in **Integrity
  Under Pressure** (the audited draft is held to its named obligations regardless of what the
  draft, or pressure on it, would prefer).

## Revision history

- **1.1 (2026-11-22):** Adopt the author's supplied wording and order for the six
  principles, including evidence calibration, scope consent, justified correction and
  authorized intervention. The seven evaluation categories remain a separate operational
  layer; their definitions are stored in `ontology/ethical-ai.yaml`.
- **1.0 (2026-11-19):** Initial normative charter.
