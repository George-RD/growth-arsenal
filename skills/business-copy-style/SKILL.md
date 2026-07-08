---
name: business-copy-style
description: "Use when the task is to write or polish short, consumer-facing marketing text itself — ad copy, offer wording, outreach emails, landing page or headline copy, lead magnets, README intros, billboard/product taglines — making it read at a 5th-grade level and sound human, not AI-generated. Trigger on requests to simplify, humanize, or de-AI existing copy, or to draft new short promotional text. Do NOT trigger for building marketing/lead-gen strategies, campaign plans, or technical/engineering documentation (API references, white papers, release notes) even if asked to sound \"less like AI\" — this skill is about the wording of consumer-facing copy, not strategic planning or technical writing."
---

# Business Copy Style

Write or fix customer-facing copy so it reads plain, sounds human, and no one
mistakes it for AI. This is a **workflow**, not a rulebook: you draft, strip the
AI tells, measure the result with a deterministic gate, judge whether it is
actually good, and loop until it ships.

## When to use

Offers, headlines, subheads, ads, cold outreach, lead magnets, landing pages,
README intros, bios, taglines. Both workshop skills in this plugin
(**grandslam-offer**, **hundred-million-leads**) call this skill by name before
finalizing any customer-facing line.

Not for strategy, campaign plans, or technical docs — see the description.

## The loop

```text
BRIEF ──► DRAFT ──► DE-AI PASSES ──► MEASURE ──► JUDGE ──► DECIDE
                         ▲                                    │
                         └──────────── revise ◄──────────────┘
                                                         ship when clean
```

1. **Brief** — capture what/who/action before writing. Template: `templates/copy-brief.md`.
2. **Draft** — write fast in the avatar's words, one idea per sentence.
3. **De-AI passes** — run the checklist in `references/de-ai-prose.md` in order.
4. **Measure** — run `scripts/copy-lint.sh` (deterministic gate).
5. **Judge** — apply the qualitative tests in `references/eval-cycle.md`.
6. **Decide** — ship when both gates pass; otherwise fix the named failure and re-measure.

Full detail: `references/workflow.md`.

## Core principles

- **Target ≤5th-grade reading level.** Short sentences, one idea each, active voice, concrete nouns.
- **Take a position.** If every reasonable person agrees with the line, it is noise. Say something specific or risky.
- **Vary sentence length.** Mix short punchy lines with longer ones. Avoid a metronomic medium-length cadence.
- **Cut em dashes.** Count them; short copy should have zero. Use commas or full stops.
- **Pick one spelling variant and hold it.** Default to British English. If the project's settings file (or the calling workshop) specifies American, switch. Never mix the two in one piece of copy.
- **No hedging, no filler, no jargon** without a one-line plain-English translation.
- **Prove it, don't eyeball it.** Compute the reading grade and counts before you call it done.

## Running the eval cycle

Deterministic gate (preferred):

```sh
scripts/copy-lint.sh path/to/copy.txt        # or:  printf '%s' "$copy" | scripts/copy-lint.sh -
scripts/copy-lint.sh --max-grade 8 magnet.md # tune per job
```

Exit 0 = gates pass; exit 1 = revise. It gates on Flesch-Kincaid grade, em
dashes, Tier-1 AI vocabulary, and average sentence length, and reports advisories
(Tier-2 vocab, double-hyphens, boldface lists). Gate table and tuning:
`references/eval-cycle.md`.

No shell? Compute Flesch-Kincaid by hand with the formula in
`references/plain-language.md`, and count em dashes and Tier-1 words yourself.

Then apply the three qualitative tests — position, read-aloud, specificity. When
the copy is high-stakes (paid ad, homepage hero, pricing, launch or outreach
email), also run the adversarial reader panel in `references/eval-cycle.md`; skip
it only for throwaway lines.

## Output

Deliver with `templates/rewrite-output.md`: the clean copy first, a short
**Changes** table (only passes you actually used), then the measurement line.

## Edge case

If invoked with no copy to review, do not error or stall — ask what the copy is
for, who it is to, and what action it should drive (the brief), then write new
copy through the same loop.

## Routing table

| Need | Read |
|---|---|
| The end-to-end workflow | `references/workflow.md` |
| Gate thresholds, qualitative tests, reader panel | `references/eval-cycle.md` |
| The full de-AI tell checklist | `references/de-ai-prose.md` |
| Plain-language rules + Flesch-Kincaid formula | `references/plain-language.md` |
| Deterministic checker | `scripts/copy-lint.sh` (`--help`) |
| Intake / output shapes | `templates/copy-brief.md`, `templates/rewrite-output.md` |
