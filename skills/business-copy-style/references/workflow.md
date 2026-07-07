# Copy Workflow

The full loop for producing or fixing customer-facing copy. Run it in order. Do
not skip the measure step — that is what separates this skill from "rewrite it
and hope."

```text
BRIEF ──► DRAFT ──► DE-AI PASSES ──► MEASURE ──► JUDGE ──► DECIDE
                         ▲                                    │
                         └──────────── revise ◄──────────────┘
                                                         ship when clean
```

## 1. Brief

Never write blind. Get three things first (copy `templates/copy-brief.md`):

- **What** the copy is (headline, subhead, ad, email opener, lead magnet, README intro, tagline).
- **Who** it is for — one named avatar, not "customers". What do they already believe? What words do they use?
- **Action** you want them to take, and where.

Also capture: reading-level target (default ≤5th grade), length limit, and any brand voice notes. If invoked with copy to fix, the "brief" is the existing copy plus what the user dislikes about it.

## 2. Draft

Write the first version fast, to the brief. Aim for the avatar's own words.
Do not polish yet — you are about to strip it.

Drafting bias:

- One idea per sentence. Short beats clever.
- Say the specific thing the avatar cares about, not a category ("get 12 hours back a week", not "boost productivity").
- Take a position. If every reasonable person nods along, it is filler.

## 3. De-AI passes

Run the checklist in `references/de-ai-prose.md` in order. Each pass is one lens;
do them as separate sweeps, not all at once — you catch more that way.

1. Inflated significance → cut, replace with a fact.
2. Formulaic structure → break the pattern, vary lengths.
3. AI vocabulary (Tier-1 cut on sight, Tier-2 in clusters).
4. Grammar tells (copula avoidance, -ing tails, negative parallelism, synonym cycling, false ranges).
5. Rhythm and style (em dashes → zero in short copy, boldface, transitions, emoji).
6. Hedging, filler, vague attributions.
7. Chatbot artifacts.
8. Personal-copy structural tells (for bios / about-me).
9. Missing human texture → add an opinion, a number, a lived detail.

Plain-language rules run alongside every pass: see `references/plain-language.md`.

## 4. Measure

Prove it, do not eyeball it. Run the deterministic gate:

```sh
scripts/copy-lint.sh path/to/copy.txt
# or pipe: printf '%s' "$copy" | scripts/copy-lint.sh -
```

It reports and hard-gates on: Flesch-Kincaid grade, em dashes, Tier-1 vocab,
average sentence length. Exit code 0 = gates pass, 1 = revise. See
`references/eval-cycle.md` for the gate table and how to read the advisories. If
you cannot run the script, compute Flesch-Kincaid by hand with the formula in
`references/plain-language.md` and count em dashes and Tier-1 words yourself.

## 5. Judge

The script cannot tell if the copy is *good* — only that it is clean. Apply the
qualitative gates in `references/eval-cycle.md`:

- **Position test:** does a line exist someone could disagree with?
- **Read-aloud test:** would a real person say this out loud, or is it press-release voice?
- **Specificity test:** could this copy be pasted onto a competitor by swapping one noun? If yes, it says nothing.

For high-stakes copy, run the optional adversarial reader panel in `eval-cycle.md`.

## 6. Decide

- **Ship** when the deterministic gate passes AND the three judge tests pass.
- **Revise** otherwise: fix the specific failures, then go back to step 4. Do not
  re-draft from scratch unless the direction itself is wrong.

## 7. Deliver

Present the result with the format in `templates/rewrite-output.md`: the clean
copy first, then a short Changes table, then the measurement line (grade, em
dashes, Tier-1). Only list passes where you actually changed something.
