# growth-arsenal landing copy evaluation

Date: 28 July 2026  
Scope: matched marketing copy from the pre-redesign landing page and the qualification-lab redesign. Visual design was considered only where it changes what the copy proves or makes visible.

## Question

For builders, founders, consultants and small-business operators who already use an AI coding agent, which copy better explains what growth-arsenal is, why it differs from a normal chat and what to do next?

## Material compared

- **Variant A:** the pre-redesign page headed “Break your offer before the market does.”
- **Variant B:** the qualification-lab page headed “Your offer should fail here first.”
- **Variant C:** a proposed hybrid hero that keeps B's headline and restores A's immediate category specificity.

The exact matched corpora and deterministic outputs are saved under `evaluations/fixtures/` and `evaluations/*-metrics.json`.

## Deterministic result

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

The current B hero alone estimates at grade 6.5. The proposed C hero estimates at grade 5.1, with shorter average sentences and no mechanical failures.

## Blind-style rubric

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

## Reader-panel synthesis

### Skimmer

- **A takeaway:** a Hormozi-inspired offer and lead-generation toolkit.
- **B takeaway:** a set of workshops that run in my coding agent and try to break business decisions before I ship them.
- **Preference:** B, because it identifies the delivery environment and shows the product working.
- **Line to retain from A:** “Three … workshops” and the immediate offer/lead/script nouns.

### Right-fit sceptic

- **A objection:** “Hormozi-style” is borrowed authority, and “worst objections are already dead” overstates synthetic review.
- **B objection:** “Business growth workshops” is initially broad; the exact three jobs arrive later.
- **Preference:** B, because its limits and outputs are clearer.

### Wrong-fit reader

- **A reaction:** could still think this is a general course or chatbot prompt pack.
- **B reaction:** knows quickly that this is for people using an AI coding agent.
- **Preference:** B, because rejection is based on workflow fit rather than confusion.

## What is objectively better

Within the stated target audience and product truth, B is better on observable jobs:

- it explicitly identifies the AI coding agent as the delivery environment;
- it makes the independent-review mechanism visible rather than only claiming it;
- it shows persistent outputs and installation before asking for trust;
- it bounds the claim by saying the result is ready to test, not proven;
- it gives the visitor a clearer next action.

A remains better at one load-bearing job: immediate category compression. “Three workshops” plus offer, leads and copy tells the reader what is included faster than “business growth workshops”.

## Decision

Keep the qualification-lab page and headline. Do not restore the old editorial identity or put “Hormozi-style” back in the hero. Restore the old page's category specificity through a hybrid lede:

> Run three linked workshops inside your AI coding agent. They build your offer, lead plan and customer copy. Separate reviewers attack the maths, message and plan while each weak spot is still cheap to fix.

Keep the Hormozi attribution in the FAQ, credits and methodology references. That preserves provenance without making borrowed authority the first reason to trust the product.

## Workflow changes derived from the comparison

1. Existing copy becomes a frozen baseline, not disposable raw material.
2. Dogfood evaluations compare baseline, candidate and any hybrid in both directions.
3. Deterministic gates describe mechanical quality but cannot choose positioning.
4. High-stakes comparison uses a blind, provenance-hidden reader panel.
5. The rubric adds category clarity and mechanism clarity; the old three-test set could miss both.
6. Hybrids must be re-evaluated as complete copy, not assumed to inherit only the winning parts.
7. Default readability is reconciled at grade 6, with grade 5 as an aim when it does not distort product language.
8. Workflow changes are rerun on the same comparison before they count as improvements.

## Deferred evidence

Independent humans or agents who did not author the workflow should repeat this comparison. The current result is strong enough to guide the process and hero recommendation, but it is not a conversion test.
