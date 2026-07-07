# Rewrite Output

Copy this shape when delivering finished copy. Lead with the copy, keep the
receipts short.

## [The copy]

> [final headline / subhead / body — clean, no annotations]

## Changes

Only rows where you actually changed something.

| Pass | What changed | Example |
|---|---|---|
| Inflation | Cut significance puffery | "pivotal moment" → deleted |
| Vocabulary | Removed Tier-1 words | "leverage" → "use" |
| Rhythm | Cut em dashes, varied length | 2 em dashes → commas + a 3-word line |
| Position | Added a stance | "most agencies overcharge" |

## Measurement

```text
Flesch-Kincaid grade : [x.x]  (target ≤ 6)
em dashes            : [n]    (target 0)
Tier-1 vocab         : [n]    (target 0)
avg words/sentence   : [x.x]  (target ≤ 15)
```

Judge tests: position [pass/fail] · read-aloud [pass/fail] · specificity [pass/fail]

> Produced with `scripts/copy-lint.sh`; see `references/eval-cycle.md`.
