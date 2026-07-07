# Eval Cycle

How to know the copy is done. Two layers: deterministic gates (a script decides)
and qualitative gates (you decide). Copy ships only when both pass.

## Deterministic gates

Run `scripts/copy-lint.sh FILE`. It exits 1 if any hard gate fails, so you can
loop on it. Defaults suit short consumer copy; override per job.

| Metric | Default gate | Flag | Why |
|---|---|---|---|
| Flesch-Kincaid grade | ≤ 6 | `--max-grade` | Plain enough for a busy reader. |
| Em dashes (U+2014) | 0 | `--max-emdash` | The strongest single AI tell in short copy. Use commas or full stops. |
| Tier-1 AI vocabulary | 0 (always) | — | Dead giveaways: delve, leverage, streamline, etc. |
| Avg words / sentence | ≤ 15 | `--max-sentence` | One idea per sentence. |

Advisories are reported but never fail the build — judge them in context:

- **Tier-2 vocab** (robust, seamless, innovative…): fine once, a tell in clusters of 3+.
- **Double-hyphen (` -- `)**: an em dash in disguise. Usually cut.
- **Boldface list items** (`- **X:** …`): mechanical emphasis. Keep at most one.

Tuning examples:

```sh
# a longer lead magnet, allow grade 8 and slightly longer sentences
scripts/copy-lint.sh --max-grade 8 --max-sentence 18 magnet.md
# a technical README intro where a single em dash is acceptable
scripts/copy-lint.sh --max-emdash 1 --max-grade 9 intro.md
```

Keep the script's Tier lists in sync with `references/de-ai-prose.md` if you edit either.

## Qualitative gates

A clean score is necessary, not sufficient. Sterile copy passes the script and
still fails the reader. Apply these three:

1. **Position.** At least one line takes a stance a reasonable person could
   argue with. "We think most agencies overcharge" passes. "We deliver quality"
   fails — nobody disagrees, so it says nothing.
2. **Read-aloud.** Say it out loud. Flag anything that sounds like a press
   release, a chatbot, or a sentence no human would speak.
3. **Specificity.** Swap the brand name for a competitor's. If the copy still
   fits, it is generic. Add the concrete number, the named pain, the real detail.

Score each pass/fail. Any fail → revise and re-run the deterministic gate too.

## Optional: adversarial reader panel

For high-stakes copy (a paid ad, a homepage hero, a launch email), stress-test it
the way the workshops stress-test offers. Spawn 2-3 parallel reader subagents,
each a distinct slice of the avatar, and ask each one blind:

- **The skimmer** — reads for 3 seconds. What did you take away? Would you click?
- **The skeptic** — what claim here do you not believe, and why?
- **The wrong-fit** — does this repel you correctly, or does it try to please everyone?

Collect each reader's single strongest objection. Fix the objections that
recur, then re-run the full cycle. Do not average vibes; act on concrete objections.

## The loop, in one line

Draft → `copy-lint.sh` until exit 0 → three qualitative tests → ship. Any failure
sends you back to the specific fix, not back to a blank page.
