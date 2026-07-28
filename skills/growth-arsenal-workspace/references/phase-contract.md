# Phase and Review Contract

## Phase payload

The smallest useful payload is:

```json
{
  "summary": "One plain-language account of the approved direction.",
  "data": {},
  "research_patch": {},
  "evidence_refs": []
}
```

`summary` is for human scanning. `data` is structured phase truth. `research_patch` is deep-merged into the shared research record. `evidence_refs` points to source identifiers or user-supplied material.

Do not store presentation HTML in phase data.

## Stable fields by offer phase

The renderer accepts aliases and missing fields, but calling skills should converge on these keys:

- `discovery`: `business`, `audience`, `problem`, `personas`
- `market`: `core_market`, `niche`, `pain_score`, `purchasing_power_score`, `targeting_score`, `growth_score`
- `pricing`: `price`, `position`, `ten_x_insight`, `delivery_cost`, `margin_notes`
- `value`: `dream_outcome`, `dream_score`, `perceived_likelihood`, `likelihood_score`, `time_delay`, `time_score`, `effort_sacrifice`, `effort_score`
- `stack`: `core`, `bonuses`, `total_value`, `price`
- `enhancement`: `offer_name`, `elevator_pitch`, `scarcity`, `urgency`, `guarantee`

`guarantee` should contain `name`, `terms`, `type`, `category`, `target_fear` and optional `layers`.

## Review payload

A review is independent. Reviewers do not see each other's output.

```json
{
  "reviewer": "business-strategist",
  "score": 6,
  "top_concern": "The custom delivery model removes the margin.",
  "issues": [
    {
      "issue_key": "fulfilment-margin-at-scale",
      "title": "Fulfilment margin at scale",
      "severity": "critical",
      "finding": "Four specialist hours are required per customer.",
      "evidence": "At the current price this leaves no room for acquisition cost.",
      "recommended_fix": "Standardise onboarding and move support to group delivery.",
      "blocking": false
    }
  ]
}
```

## Issue normalisation

The main workshop agent performs one synthesis pass after independent reviews:

1. Preserve every review verbatim.
2. Compare findings by causal problem, not shared vocabulary.
3. Give semantically equivalent findings the same kebab-case `issue_key`.
4. Keep genuinely different causes separate even when the proposed fix is similar.
5. Never merge findings merely to force consensus.
6. Run the gate only after issue keys are normalised.

Examples:

- “The buyer is everyone” and “I cannot tell who this is for” may share `buyer-not-specific`.
- “The market is small” and “the offer is priced too low” are different issues.

## Gate semantics

An issue blocks when:

- two or more distinct reviewers use the same `issue_key`; or
- a review sets `blocking: true` for a structurally fatal problem.

A high or low average score never overrides an open critical issue.
