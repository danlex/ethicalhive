---
name: tvl-tech-bias-validator-mindmap
description: Mermaid mindmap of the 2024-2026 research landscape on LLM confabulation, hallucination, sycophancy, and cognitive bias. Renders in any Markdown viewer that supports Mermaid (GitHub, Obsidian, VS Code with extension).
---

# Research mindmap — generative AI biases (2023–2026)

```mermaid
mindmap
  root((LLM Bias & Hallucination<br/>2023–2026))

    Generation failures
      Hallucination
        Faithfulness<br/>(intrinsic)
          MiniCheck<br/>Tang et al. EMNLP 2024
          FACTS Grounding<br/>DeepMind 2024-12
        Factuality<br/>(extrinsic)
          Factuality of LLMs 2024<br/>arXiv 2402.02420
          Hallucination to Truth review<br/>Springer AIR 2025
      Confabulation
        Semantic Entropy<br/>Farquhar et al. Nature 2024
        Semantic Entropy Probes<br/>Kossen et al. ICLR 2025
        Semantic Energy<br/>Ma et al. 2025
        Narrativity value<br/>Sui and Duede ACL 2024
      Attribution failures
        Post-rationalized citations
        Correctness is not Faithfulness<br/>arXiv 2412.18004
        How Do LLMs Cite?<br/>Springer 2025

    Agreement failures
      Sycophancy
        Towards Understanding Sycophancy<br/>Sharma et al. 2023
        Causes and Mitigations<br/>Malmqvist 2024
        Medical helpfulness backfires<br/>Chen npj DigMed 2025
        ELEPHANT social sycophancy<br/>Cheng et al. ICLR 2026
        Causal separation<br/>arXiv 2509.21305 2025
      Helpfulness pathology
        Compliance with illogical asks
        RLHF reward for agreement
        Shoggoths Sycophancy Psychosis<br/>JMIR 2025

    Reasoning failures
      Confirmation bias
        User-reflection loops<br/>JMIR 2025
        AI amplifies user bias<br/>HBR 2026
      Anchoring
        NEJM AI Cognitive Biases 2024
      Framing and availability
        Bias in religious education<br/>Sci Reports 2025
      Systematic review
        Kumar AI and Ethics 2025<br/>Springer

    Trust failures
      Automation bias
        CRT Nudges study<br/>ScienceDirect 2025
        Forewarning only ~7% effective<br/>PMC 2025
      Adversarial exploitation
        Weaponizing cognitive bias<br/>Frontiers AI 2025
      Human-AI interaction
        Beyond Isolation interactionist<br/>arXiv 2504.18759 2025

    Calibration
      Semantic-level uncertainty
        Farquhar 2024
        Ma 2025
      Token-level entropy (baseline)
      Epistemic vs aleatoric

    Mitigation directions
      Structural audits<br/>(this skill)
      Retrieval grounding
        FACTS Grounding
        MiniCheck
      Uncertainty probes
        Kossen SEPs 2024
      Debate / adversarial review
      RLHF recalibration
        Anti-sycophancy training
      Forewarning<br/>(weak baseline)
```

## How to read this map

- **Five primary branches** correspond to failure families in `glossary.md` (generation, agreement, reasoning, trust, calibration), plus a sixth branch for mitigations.
- Each leaf cites the load-bearing paper for that concept. Citations trace back to `research.md`.
- The **mitigation** branch shows why this skill was built: structural audits sit alongside retrieval grounding and uncertainty probes because forewarning alone is documented to be ~7% effective (PMC 2025).

## Rendering tips

- GitHub renders Mermaid natively in Markdown.
- In Obsidian, enable the Mermaid plugin (bundled).
- In VS Code, use the "Markdown Preview Mermaid Support" extension.
- To export as PNG/SVG, paste into https://mermaid.live (public — do not paste confidential content).
