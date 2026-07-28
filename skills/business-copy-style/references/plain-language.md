# Plain Language Rules

**Default hard gate:** Flesch-Kincaid Grade Level ≤6.  
**Drafting aim:** around grade 5 for broad consumer copy when it remains natural and specific.

The hard gate and the aim are not conflicting targets. Grade 6 is the consistent failure boundary used by the scripts. Grade 5 is a useful direction, not a reason to replace a true product term with vague language.

## Sentence rules

- Average sentence length ≤15 words.
- One main idea per sentence.
- Prefer active voice.
- Use concrete nouns and verbs.
- Split a long sentence before deleting the mechanism or qualification that makes it true.

## Word rules

- Translate necessary jargon once.
- Use “you” and “we” when the relationship is clear.
- Prefer verbs to nominalisations.
- Cut filler such as “in order to”, “due to the fact that” and “at this point in time”.
- Preserve proper nouns, product names, legal terms and necessary technical language.

## Flesch-Kincaid formula

```text
Grade = 0.39 × (words / sentences) + 11.8 × (syllables / words) - 15.59
```

The repository scripts use a syllable heuristic, so the result is a repeatable estimate rather than a linguistic ground truth.

## Example

> We help busy owners get more leads without working nights.

- Words: 10
- Sentences: 1
- Approximate syllables: 14
- Estimated grade: 4.8

## Exceptions and judgement

- A short headline may be memorable and clear even when the formula is unstable.
- Product and technical terms can raise the score while improving category clarity.
- Guarantee or legal terms may need a higher threshold; preserve meaning first.
- A lower grade does not choose the winner in a baseline/candidate comparison.
