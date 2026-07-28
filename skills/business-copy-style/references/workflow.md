# Copy Workflow

The workflow has two paths. Greenfield copy needs one evaluated draft. Existing or high-stakes copy needs a paired evaluation so the rewrite does not win by default.

## 1. Freeze the brief

Get these before writing:

- **What:** headline, subhead, offer line, ad, email, lead magnet, README intro or tagline.
- **Who:** one named audience, what they already believe and what language they use.
- **Action:** what they should do, and where.
- **Truth:** product facts, proof, restrictions and claims that may not change.
- **Constraints:** length, spelling, channel, required wording and reading-level policy.

Use `templates/copy-brief.md`.

If existing copy is supplied, save it unchanged as the baseline before drafting. Do not let the rewrite silently alter the audience, offer or desired action.

## 2. Draft

Write the first candidate quickly to the brief.

Drafting bias:

- one idea per sentence;
- audience language over category jargon;
- concrete result, mechanism or pain over adjectives;
- a real position rather than consensus filler;
- no invented numbers, proof or urgency.

Do not optimise to the lint script while drafting.

## 3. Run de-AI passes

Read `references/de-ai-prose.md` and run each lens separately:

1. inflated significance;
2. formulaic structure;
3. Tier-1 and clustered Tier-2 vocabulary;
4. grammar tells;
5. rhythm, punctuation and mechanical emphasis;
6. hedging, filler and vague attribution;
7. chatbot artefacts;
8. personal-copy structural tells when relevant;
9. missing human texture.

Plain-language rules run alongside every pass.

## 4. Measure mechanics

Single version:

```sh
scripts/copy-lint.sh path/to/copy.txt
```

Existing-copy or dogfood comparison:

```sh
python3 scripts/copy-compare.py \
  --baseline baseline.txt \
  --candidate candidate.txt \
  --format json
```

Default hard gates are:

- Flesch-Kincaid grade ≤6;
- zero em dashes;
- zero Tier-1 AI vocabulary;
- average sentence length ≤15 words.

Grade 5 is a useful aim for broad consumer copy, not a second hidden hard gate. Proper nouns and necessary product terms may raise the estimate. Fix the sentence before replacing a true term with a vague one.

## 5. Judge meaning

Run the ordinary tests:

- position;
- read-aloud;
- specificity.

For high-stakes copy, run blind readers:

- skimmer;
- right-fit sceptic;
- wrong-fit reader;
- mechanism reader when the product's process is the main differentiator.

A mechanical pass is necessary, not sufficient. A persuasive line also fails when it overclaims, obscures the category or attracts the wrong audience.

## 6. Compare when a baseline exists

Read `references/paired-evaluation.md`.

Evaluate baseline and candidate against the same brief without revealing provenance. Decide:

- keep baseline;
- adopt candidate;
- build and re-evaluate a hybrid;
- revise the direction because both fail.

Do not average away repeated objections. Fix the causal problem.

## 7. Decide and loop

### Greenfield

Ship when the deterministic and qualitative gates pass. Otherwise fix the named failure and return to measurement. Do not restart from blank unless the direction is wrong.

### Existing copy

A candidate replaces the baseline only when it wins load-bearing dimensions without introducing a trust, factual or action regression. The baseline may remain unchanged. That is a valid successful evaluation.

A hybrid must run through the full workflow as a new candidate.

## 8. Dogfood the process

After evaluating output, evaluate the workflow itself:

- Which instruction caused a material win?
- Which instruction caused a regression?
- Which failure was invisible to the current detector or rubric?
- Did two directives conflict, and which one better served product truth?

Change the workflow only for repeated failures or one severe failure. Then rerun the same comparison. The explanation for a change is not evidence that it worked.

## 9. Deliver

Ordinary rewrite:

- final copy;
- short Changes table;
- measurement line.

Paired evaluation:

- recommendation and exact copy;
- baseline/candidate/hybrid decision;
- load-bearing evidence;
- deterministic comparison;
- retained lines from the losing variant;
- limitations and next evidence needed.
