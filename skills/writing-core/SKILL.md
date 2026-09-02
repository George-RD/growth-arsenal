---
name: writing-core
description: Proactive foundation for human-readable prose. Use before writing or substantially rewriting wiki pages, research notes, analyses, reports, documentation, presentation copy, emails, proposals, social copy, or other prose. Separates meaning from delivery: build a factual kernel first, then expand only where the reader needs context, causality, consequence, or action.
---

# Writing Core

Write from meaning, not from a polished first draft.

This skill owns the **generation layer**. It should run before genre-specific writing skills and before `business-copy-style`. A downstream workflow can change the audience, format or tone, but it should inherit the same facts, terms and causal structure.

## Companion resolution

Check a companion only when its capability is first needed.

- **`executive-writing` is a hard dependency for executive, manager or presentation delivery.** If it is missing, keep the factual kernel, show `npx skills add George-RD/growth-arsenal --skill executive-writing`, and pause only that delivery path until it is available.
- **`business-case` is a hard dependency when the task needs an investment/decision model and no completed model has been supplied.** If it is missing, keep the source evidence and kernel work, show `npx skills add George-RD/growth-arsenal --skill business-case`, and pause only the business-case modelling path.
- **`business-copy-style` is a quality dependency for customer-facing short copy.** If it is missing, explain that the final de-slop/copy-quality gate cannot be verified, show `npx skills add George-RD/growth-arsenal --skill business-copy-style`, and ask whether to install it or continue degraded. If the user continues degraded, label the affected copy `degraded/unverified` and do not imitate the missing skill's full method.

Do not duplicate a missing companion's method as a local fallback.

## Sequence

1. **Build the factual kernel**
   Write the minimum complete meaning as rough statements before prose:
   - subject or owner;
   - action, state or claim;
   - object or consequence;
   - number, date or example when material;
   - **claim status**: observed, estimated, assumed or unknown;
   - **provenance**: the named source, source type or `UNAVAILABLE`.

   Status and provenance are separate. A sourced estimate remains `ESTIMATED`; its source is recorded independently. An observed claim can also have a source.

   Use one topic per statement. Keep the same term for the same thing. Do not add transitions, slogans or rhetorical framing yet.

   Read [`references/factual-kernel.md`](references/factual-kernel.md) when the source is technical, uncertain, long or contradictory.

   *Done when:* another competent reader could reconstruct the argument without any stylistic prose, and every material claim has both status and provenance.

2. **Choose the reader and genre**
   Decide what the reader already knows, what they need to understand, and what they should do next. Pick only the guidance needed for this surface:
   - private wiki/research: preserve reasoning, provenance and uncertainty;
   - technical documentation: optimise for precision and unambiguous action;
   - executive/business writing: resolve `executive-writing`;
   - business case: if no completed `business-case` decision model has been supplied, resolve `business-case` before prose; if a completed model is already the input, use it and do not re-enter that workflow;
   - personal or public voice: use the user's approved voice profile if one exists;
   - customer-facing short copy: run `business-copy-style` after drafting.

   *Done when:* audience, purpose and required action are explicit.

3. **Turn the kernel into prose**
   Expand a kernel statement only when the extra words do one useful job:
   - provide context the reader lacks;
   - explain cause or mechanism;
   - show consequence;
   - state a decision or action;
   - connect two ideas whose relationship is not obvious.

   Prefer concrete nouns and ordinary verbs. Use active voice when the actor matters. Repeat the exact technical noun when synonym variation would blur meaning. Keep technical terms when they are the precise language of the audience.

   Use controlled-English principles as a clarity aid, not as a compliance target: one main thought per sentence, stable terminology, direct construction, conditions before the action or consequence when order matters, and common words for the grammatical glue around technical terms.

   *Done when:* every added sentence makes the meaning easier to use, not merely smoother.

4. **Make it sound spoken by a competent person**
   Read it aloud without headings or layout. Rewrite any sentence that exists mainly for symmetry, cadence, polish or a neat conclusion. Vary sentence shape because the meaning varies, not to simulate randomness. A short sentence is useful when the point is short. A longer sentence is useful when the relationship genuinely needs it.

   Do not optimise for an AI detector. Do not manufacture mistakes. Human texture comes from specificity, point of view, uneven information density and real examples.

   *Done when:* the prose can be said aloud without mentally translating it.

5. **Run the relevant downstream review**
   - `executive-writing` for manager, decision or presentation surfaces;
   - `business-copy-style` for final de-slop and short-copy quality checks;
   - domain-specific workflow checks for facts, evidence and format.

   Readability scores are diagnostics, not universal gates. Make a reasonable effort to lower unnecessary complexity, but keep a specific technical word when it is the right word for the audience.

   *Done when:* the content survives both meaning review and the relevant delivery review.

## Core rules

- **Meaning before wording.** If the direction changes, return to the kernel instead of synonym-editing generated prose.
- **Specific before general.** Name the vessel, customer, system, number, event or decision when it matters.
- **Stable terms.** Repetition is better than elegant variation when two words might imply two concepts.
- **Causality must be earned.** Use `because`, `so`, `if`, `when` or an explicit mechanism only when the source supports that relationship.
- **Uncertainty is data.** Separate the claim, its status and its provenance.
- **Compression has a floor.** Shorten until the next cut would remove meaning or make the reader infer a missing relationship.
- **Technical language is allowed.** Simplify the sentence around a necessary term instead of replacing the term with a vague one.
- **No universal cadence.** Lists, short sentences, long sentences, fragments and rhetorical questions are all tools; none is a default template.

## Composition contract

Workflow skills that produce prose should invoke this skill at the **first generation step**. Review skills should not recreate this method. The normal stack is:

```text
evidence / reasoning
      ↓
writing-core        ← factual kernel + reader
      ↓
genre skill         ← executive-writing, proposal, report, etc.
      ↓
business-copy-style ← final adversarial copy review when relevant
      ↓
render / publish
```

Raw source capture is exempt: preserve source text verbatim before deriving prose from it.
