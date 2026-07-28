# growth-arsenal landing copy evaluation

Date: 28 July 2026  
Scope: matched marketing copy from the pre-redesign landing page, the qualification-lab redesign and the proposed hybrid. Visual design was considered only where it changes what the copy proves or makes visible.

## Question

For builders, founders, consultants and small-business operators who already use an AI coding agent, which copy better explains what growth-arsenal is, why it differs from a normal chat and what to do next?

## Material compared

- **Variant A:** the pre-redesign page headed “Break your offer before the market does.”
- **Variant B:** the qualification-lab page headed “Your offer should fail here first.”
- **Variant C:** the complete B page with a revised hero that keeps B's headline and restores A's immediate category specificity.

The exact matched corpora and deterministic outputs are saved under `evaluations/fixtures/` and `evaluations/*-metrics.json`.

## Deterministic result

### A versus B, complete matched page copy

| Signal | Variant A | Variant B |
|---|---:|---:|
| Words | 189 | 228 |
| Sentences | 22 | 24 |
| Average words per sentence | 8.6 | 9.5 |
| Estimated Flesch-Kincaid grade | 5.1 | 6.6 |
| Em dashes | 0 | 0 |
| Tier-1 AI vocabulary | 0 | 0 |
| Default hard gate | Pass | Fail on grade |

Variant A is mechanically simpler. That is a real advantage, but it does not settle the positioning question. Variant B contains necessary product terms such as “customer-facing”, “adversarial” and “independently”, and it demonstrates more of the process.

### B versus C, complete matched page copy

| Signal | Variant B | Variant C |
|---|---:|---:|
| Words | 228 | 233 |
| Sentences | 24 | 25 |
| Average words per sentence | 9.5 | 9.3 |
| Estimated Flesch-Kincaid grade | 6.6 | 6.4 |
| Em dashes | 0 | 0 |
| Tier-1 AI vocabulary | 0 | 0 |
| Default hard gate | Fail on grade | Fail on grade |

The full-page grade remains above the default because the corpus combines headings, product terms and several distinct sections. It is useful as a regression signal, not a licence to flatten necessary terminology.

The proposed C hero by itself scores grade 5.1, averages 10.2 words per sentence and passes the default deterministic gate. This leads to a process distinction:

- lint each customer-facing field or coherent block at the threshold appropriate to that job;
- also compare the complete surface for rhythm, repetition and regressions;
- never let one aggregate page score choose the positioning.

## First blind-style pass: A versus B

The variants were scored as A and B against the frozen audience, product truth and action before unblinding. This was a structured single-agent evaluation, not independent human user research; that limitation is material.

| Dimension | A | B | Evidence |
|---|---:|---:|---|
| Target-audience recognition | 1 | 2 | B says the workshops run inside the reader's AI coding agent. A can read like a general marketing course. |
| Category clarity | 2 | 1 | A immediately says there are three workshops and names offers, lead magnets and scripts. B initially says the broader “business growth workshops”. |
| Mechanism clarity | 1 | 2 | A claims adversarial review. B shows Input → Attack → Rebuild → Clear and explains phase gates. |
| Specificity | 2 | 2 | A names concrete outputs; B names reviewers, files, phase gates and the full offer-to-copy chain. |
| Action clarity | 1 | 2 | B puts installation in the first viewport and provides copy controls and harness choices. |
| Trust and claim discipline | 1 | 2 | A says the worst objections are “already dead”. B says “clear to test” and explicitly states real customers still decide. |
| Wrong-fit rejection | 1 | 2 | B clearly requires an AI coding-agent workflow. A's “Hormozi-style” label attracts a method fan but does not define the operating context. |
| Voice and memorability | 2 | 2 | A's market line is strong. B's “fail here first” and qualification-rig language are more ownable. |
| **Total** | **11/16** | **15/16** | B wins the target-audience and product-mechanism decision. |

### A/B reader-panel synthesis

#### Skimmer

- **A takeaway:** a Hormozi-inspired offer and lead-generation toolkit.
- **B takeaway:** a set of workshops that run in my coding agent and try to break business decisions before I ship them.
- **Preference:** B, because it identifies the delivery environment and shows the product working.
- **Line to retain from A:** “Three … workshops” and the immediate offer/lead/script nouns.

#### Right-fit sceptic

- **A objection:** “Hormozi-style” is borrowed authority, and “worst objections are already dead” overstates synthetic review.
- **B objection:** “Business growth workshops” is initially broad; the exact three jobs arrive later.
- **Preference:** B, because its limits and outputs are clearer.

#### Wrong-fit reader

- **A reaction:** could still think this is a general course or chatbot prompt pack.
- **B reaction:** knows quickly that this is for people using an AI coding agent.
- **Preference:** B, because rejection is based on workflow fit rather than confusion.

## Required second pass: B versus complete hybrid C

Variant C was treated as a new candidate, not assumed to inherit only the winning parts. The full C corpus was compared with B using the same audience, product truth, action and complete-page context.

| Dimension | B | C | Evidence |
|---|---:|---:|---|
| Target-audience recognition | 2 | 2 | Both name the AI coding agent in the first viewport. |
| Category clarity | 1 | 2 | C immediately names three linked workshops and the offer, lead plan and customer copy. |
| Mechanism clarity | 2 | 2 | C retains independent reviewers, the qualification rig and phase-gated body. |
| Specificity | 2 | 2 | C's hero now previews the exact three benches shown later. |
| Action clarity | 2 | 2 | Installation remains the primary first-viewport action. |
| Trust and claim discipline | 2 | 2 | C adds no performance claim and retains the “clear to test” limitation. |
| Wrong-fit rejection | 2 | 2 | C remains explicitly for AI coding-agent users. |
| Voice and memorability | 2 | 2 | The ownable “fail here first” line and qualification-lab language remain intact. |
| **Total** | **15/16** | **16/16** | C resolves B's only material category gap without weakening its mechanism or trust. |

### C reader-panel rerun

#### Skimmer

- **Takeaway:** three connected workshops inside my coding agent build the offer, lead plan and copy, then independent reviewers attack the decisions.
- **Action:** install it or watch the test.
- **Result:** category and mechanism both land within the first viewport.

#### Right-fit sceptic

- **Challenge:** “attack each decision” must correspond to actual phase reviews rather than decorative personas.
- **Evidence check:** the workflow requires independent review at every phase and the page demonstrates the review gate.
- **Result:** no new unsupported commercial claim was introduced.

#### Wrong-fit reader

- **Reaction:** a user who does not work through an AI coding agent can reject it immediately for the correct reason.
- **Result:** C does not broaden the page into generic business advice.

#### Mechanism reader

- **Question:** does the hero predict the rest of the page accurately?
- **Finding:** offer, lead plan and customer copy map directly to the Offer, Leads and Copy benches. Independent reviewers map to the visible qualification rig and phase-gate explanation.
- **Result:** the hero compresses the page without promising a capability the body cannot show.

#### Whole-page coherence

- C changes only the first explanation block.
- The later sections still deepen the same sequence: product distinction, phase gate, three workshops, persistent outputs and installation.
- No duplicated promise, contradictory label or missing handoff was introduced.

## What is objectively better

Within the stated target audience and product truth:

- B is better than A at audience recognition, mechanism proof, action clarity and claim discipline.
- A is better than B at immediate category compression.
- C is better than both because it retains B's mechanism and honesty while restoring A's category specificity.

This is not a conversion claim. It is a conclusion against explicit comprehension, fit, proof and action criteria.

## Decision

Use Variant C:

> **Your offer should fail here first.**
>
> Run three linked workshops inside your AI coding agent. They build your offer, lead plan and customer copy. Separate reviewers attack the maths, message and plan while each weak spot is still cheap to fix.

Keep the Hormozi attribution in the FAQ, credits and methodology references. That preserves provenance without making borrowed authority the first reason to trust the product.

## Workflow changes derived from the comparison

1. Existing copy becomes a frozen baseline, not disposable raw material.
2. Dogfood evaluations compare baseline and candidate in both directions.
3. A hybrid is a new candidate and must pass deterministic, reader-panel and whole-surface evaluation again.
4. Deterministic gates describe mechanical quality but cannot choose positioning.
5. Lint coherent fields or blocks at job-appropriate thresholds; use aggregate page metrics as diagnostics, not a single release gate.
6. High-stakes comparison uses a blind, provenance-hidden reader panel.
7. The rubric includes category clarity and mechanism clarity; the old three-test set could miss both.
8. HTML extraction preserves all common block boundaries before analysis.
9. Sentence counting protects decimals, abbreviations, initialisms, URLs and email addresses from false stops.
10. Workflow changes are rerun on the same comparison before they count as improvements.
11. Baseline retention, candidate adoption, a re-evaluated hybrid and revise-direction all remain valid outcomes.

## Deferred evidence

Independent humans or agents who did not author the workflow should repeat this comparison. The current result is sufficient to select the clearer copy and harden the process, but it is not a conversion test.
