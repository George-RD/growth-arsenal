---
name: business-copy-style
description: Use when the task is to write or polish short, customer-facing marketing text itself, including offer wording, ads, outreach, landing pages, headlines, lead magnets, README intros, bios and taglines. Makes copy plain, specific and human, then verifies it with deterministic and qualitative gates. When revising existing or high-stakes copy, preserves the incumbent as a baseline and runs a paired evaluation rather than assuming the rewrite is better. Not for campaign strategy or technical documentation.
---

# Business Copy Style

Write or fix customer-facing copy so a busy reader understands it, believes only what the evidence supports and does not mistake it for generic AI prose.

This is a workflow, not a bag of banned words. Draft, strip the tells, measure the mechanics, judge the meaning and keep the version that serves the brief best.

## When to use

Offers, headlines, subheads, ads, outreach, lead magnets, landing pages, README intros, bios and taglines. The `grandslam-offer` and `hundred-million-leads` workshops call this skill before finalising customer-facing lines.

Not for business strategy, campaign planning or technical documentation.

## Choose the evaluation path

### Greenfield copy

```text
BRIEF → DRAFT → DE-AI PASSES → MEASURE → JUDGE → DECIDE
                         ▲                           │
                         └──────── revise ◄─────────┘
```

### Existing copy or dogfooding

```text
FREEZE BASELINE ─┐
                 ├→ SAME BRIEF → DRAFT CANDIDATE → MEASURE BOTH
CANDIDATE ───────┘                                  │
                                                   ▼
                                      BLIND PAIRED JUDGEMENT
                                      │        │          │
                                   baseline candidate   hybrid
                                                        │
                                                        └→ re-evaluate
```

Read `references/paired-evaluation.md` whenever existing high-stakes copy is being replaced or the skill is evaluating its own output.

## The ordinary loop

1. **Brief:** capture what the copy is, one audience, what they already believe and the action it should drive. Use `templates/copy-brief.md`.
2. **Draft:** write in the audience's language. One idea per sentence.
3. **De-AI passes:** run `references/de-ai-prose.md` in order.
4. **Measure:** run `scripts/copy-lint.sh`.
5. **Judge:** run the position, read-aloud and specificity tests in `references/eval-cycle.md`.
6. **Reader panel:** for high-stakes copy, run the skimmer, sceptic and wrong-fit readers blind.
7. **Decide:** ship only when the mechanical and qualitative gates pass.

Full detail: `references/workflow.md`.

## Core principles

- **Default hard gate: Flesch-Kincaid grade ≤6.** Aim around grade 5 for broad consumer copy when the product language still sounds natural. Do not damage a true product term merely to lower a score.
- **Take a position.** If every reasonable person agrees with the line, it is probably noise.
- **Be specific.** Prefer the named buyer, problem, action, number or mechanism over a category adjective.
- **Vary sentence length.** Mix short lines with longer explanatory ones.
- **Use zero em dashes in short copy.** Count them rather than relying on impression.
- **Choose one spelling variant and hold it.** Default to British English unless project settings say otherwise.
- **No hedging, filler or unsupported authority.** Name the source or cut the claim.
- **Measure mechanics; judge meaning.** The script can flag clean or dirty copy. It cannot decide which positioning is better.
- **No rewrite bias.** Existing copy stays unless a candidate earns replacement.

## Deterministic checks

Single version:

```sh
scripts/copy-lint.sh path/to/copy.txt
printf '%s' "$copy" | scripts/copy-lint.sh -
```

Add the optional structural summary when cadence or templated phrasing is in question:

```sh
scripts/copy-lint.sh --structure path/to/copy.txt
```

Paired comparison:

```sh
python3 scripts/copy-compare.py \
  --baseline baseline.txt \
  --candidate candidate.txt \
  --format json
```

`copy-lint.sh` exits `0` when hard gates pass and `1` when the copy needs a named mechanical fix. `copy-compare.py` always leaves `winner` unset because lower grade, fewer words or shorter sentences do not prove better copy.

Structural counts cover repeated sentences and openers, sentence-length rhythm, repeated four-word phrases, paragraph load, first-person starts, contrast scaffolds and page-explaining phrases. They are review evidence only. They do not prove AI authorship or replace the qualitative rubric.

## Qualitative gates

Every version must pass:

- **Position:** at least one line says something a reasonable person could challenge.
- **Read-aloud:** it sounds like a person, not a press release or chatbot.
- **Specificity:** a competitor cannot inherit it by swapping one noun.

For high-stakes copy, also test:

- **Audience recognition:** the right reader knows this is for them.
- **Category clarity:** they know what kind of thing this is.
- **Mechanism clarity:** they can explain how it differs.
- **Action clarity:** they know what to do next.
- **Trust discipline:** the claim is bounded by the evidence.
- **Wrong-fit rejection:** the wrong reader leaves for the right reason.

## Output

For an ordinary rewrite, use `templates/rewrite-output.md`: clean copy first, then only the changes actually made and the measurement line.

For a paired evaluation, return:

1. the recommended copy;
2. decision: baseline, candidate, hybrid or revise direction;
3. the two or three load-bearing reasons;
4. any retained line from the losing variant;
5. deterministic comparison;
6. evaluation limitations.

Do not dump a long style audit unless requested.

## Edge cases

- No copy supplied: ask for purpose, audience and action, then use the greenfield loop.
- Existing copy supplied without a clear brief: the current copy is evidence, not a complete brief. Resolve the missing audience/action before judging it.
- Factual or legal wording: preserve the required meaning. Clarity work may not weaken the obligation or claim boundary.
- A hybrid direction: treat it as a new candidate and rerun every gate.

## Routing table

| Need | Read or run |
|---|---|
| End-to-end workflow | `references/workflow.md` |
| Gate thresholds and reader panel | `references/eval-cycle.md` |
| Existing-copy or dogfood comparison | `references/paired-evaluation.md` |
| Full de-AI checklist | `references/de-ai-prose.md` |
| Plain-language rules | `references/plain-language.md` |
| Single-copy deterministic gate | `scripts/copy-lint.sh` |
| Baseline/candidate metrics | `scripts/copy-compare.py` |
| Intake and ordinary output shapes | `templates/copy-brief.md`, `templates/rewrite-output.md` |
