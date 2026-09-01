# Eval Cycle

Copy ships only when its mechanics are clean and its meaning serves the brief. Existing-copy rewrites add a third requirement: the candidate must outperform the frozen baseline on the dimensions that matter.

## Deterministic gates

Run:

```sh
scripts/copy-lint.sh FILE
```

| Metric | Default gate | Override | Why |
|---|---:|---|---|
| Flesch-Kincaid grade | ≤6 | `--max-grade` | Plain enough for a busy general reader. |
| Em dashes | 0 | `--max-emdash` | A common artificial aside in short copy. |
| Tier-1 AI vocabulary | 0 | none | Strong generic-AI signal. |
| Average words per sentence | ≤15 | `--max-sentence` | Encourages one main idea per sentence. |

Aim around grade 5 when natural for broad consumer copy. Grade is an estimate, not a command to remove true product terms.

Advisories do not fail the build:

- Tier-2 vocabulary;
- en dashes, double hyphens and repeated boldface list labels;
- exact duplicate sentences and repeated two-word sentence openers;
- sentence-length variation and runs of similarly sized sentences;
- repeated content-bearing four-word phrases per 1,000 words;
- paragraphs over the configured word or sentence load;
- first-person sentence-start rate;
- contrast scaffolds, including comma-not contrasts, and page-explaining phrases.

Use `scripts/copy-lint.sh --structure FILE` for an opt-in single-copy summary. The paired comparator always includes the structural fields in its text and JSON reports.

The structural defaults are review prompts, not universal limits. Product names, deliberate refrains, legal copy, short samples and personal writing can all produce false positives. Never use these counts to claim authorship or teach the copy to beat the detector.

For baseline/candidate work, run:

```sh
python3 scripts/copy-compare.py \
  --baseline baseline.txt \
  --candidate candidate.txt \
  --format json
```

The comparison script applies identical thresholds to both versions and reports deltas. It does not choose a winner.

## Ordinary qualitative gates

1. **Sentence merit:** does each sentence do one needed job: fact, decision, action, explanation or boundary?
2. **Paragraph cohesion:** does each paragraph answer one reader question without a polished restatement at the end?
3. **Position:** is there a line a reasonable person could disagree with?
4. **Read-aloud:** would a person say it, or does it sound like a press release or chatbot?
5. **Specificity:** could a competitor use it unchanged by swapping the brand noun?

Any fail means revise from the intended meaning, then re-measure. Do not repair a generated frame by swapping synonyms.

## High-stakes reader panel

Run this when a stranger judges the copy first or the cost of confusion is high: homepage hero, pricing, launch, paid ad, cold outreach or lead magnet.

Readers work blind and independently:

- **Skimmer:** after three seconds, what is this, who is it for and what should I do?
- **Right-fit sceptic:** what is generic, unsupported, unclear or hard to believe?
- **Wrong-fit reader:** does it repel me because I am not the buyer, or because I cannot understand it?
- **Mechanism reader, when relevant:** can I explain how it differs from the normal alternative?

Collect each reader's strongest objection. Repeated causal objections matter more than average sentiment.

## Paired rubric

When a baseline exists, score each variant `0 = fails`, `1 = partial`, `2 = clear`:

- target-audience recognition;
- category clarity;
- mechanism clarity;
- specificity;
- action clarity;
- trust and claim discipline;
- wrong-fit rejection;
- voice and memorability.

The total organises evidence. It does not override factual failure, repeated objections or a load-bearing dimension.

## Decision rules

- **Ship candidate:** it wins the important dimensions and introduces no factual, trust or action regression.
- **Keep baseline:** the rewrite repairs nothing material or damages stronger copy.
- **Hybrid:** each version owns a different load-bearing strength. Preserve named winning lines, then evaluate the hybrid from the start.
- **Revise direction:** both fail the same key job.

Never describe retaining the baseline as a failed rewrite. The evaluation prevented a regression.

## Dogfood loop

```text
freeze baseline
      ↓
produce candidate through current workflow
      ↓
measure both + blind qualitative comparison
      ↓
choose baseline / candidate / hybrid
      ↓
identify process causes
      ↓
change workflow only on material evidence
      ↓
rerun the same comparison
```

Keep at least one evaluation dimension outside the deterministic detector. Otherwise the workflow learns to pass its own test rather than communicate better.
