# Paired Copy Evaluation

Use this when revising existing customer-facing copy, dogfooding this skill, or changing a high-stakes page where the incumbent may already contain good decisions.

The purpose is not to prove that the rewrite is better. It is to find out whether it is better.

## The rule

**A candidate earns replacement. Existing copy does not lose merely because a rewrite exists.**

Freeze the baseline before drafting. Evaluate baseline and candidate against the same product truth, audience and action. The result may be:

- keep the baseline;
- adopt the candidate;
- combine specific winning lines into a hybrid;
- reject both and revise the direction.

A hybrid is a new candidate. Run the full evaluation again. Do not splice lines and assume the page remains coherent.

## When paired evaluation is mandatory

- dogfooding `business-copy-style` or another Growth Arsenal workflow;
- homepage hero, pricing, launch, paid ad or lead magnet rewrites;
- a rewrite that changes positioning, audience, offer or primary action;
- copy the user already likes but wants to improve;
- any case where the author of the candidate is also judging it.

For a typo, factual correction or low-stakes internal line, the ordinary eval cycle is enough.

## 1. Freeze the brief and baseline

Save the exact incumbent copy before writing the candidate. Record:

- audience and wrong-fit audience;
- what the reader should understand within three seconds;
- desired action;
- product truth and claims that may not change;
- constraints such as length, spelling and legal wording.

Do not let the candidate silently change the brief. A clearer answer to a different question is still a failed rewrite.

## 2. Produce the candidate

Run the normal workflow: draft, de-AI passes and deterministic lint. Do not edit the baseline to make the comparison easier.

## 3. Compare deterministic signals

```sh
python3 scripts/copy-compare.py \
  --baseline baseline.txt \
  --candidate candidate.txt \
  --format json
```

The script measures both versions using the same thresholds and reports the candidate-minus-baseline delta. It deliberately returns `winner: null`.

Deterministic gates may disqualify a version for a named mechanical failure. They do not select the stronger positioning. A lower reading grade is not automatically a better headline.

## 4. Run a blind qualitative panel

Label the variants A and B. Randomise order when practical. Do not tell readers which is old, new, human-written, AI-written or produced by this skill.

Give every reader the same brief and product truth. Use at least three lenses:

- **Skimmer:** What is this, who is it for and what should I do, after three seconds?
- **Right-fit sceptic:** What is unclear, generic, unproven or hard to believe?
- **Wrong-fit reader:** Does the copy repel me for the correct reason, or merely confuse me?

For product or technical marketing, add a fourth lens when needed:

- **Mechanism reader:** Can I explain how this differs from a normal alternative without repeating the brand's adjectives?

Each reader returns:

1. the variant they would keep;
2. one reason tied to the brief;
3. the strongest objection to each variant;
4. any line from the losing variant worth preserving.

## 5. Score the same rubric

Use `0 = fails`, `1 = partial`, `2 = clear`.

| Dimension | Question |
|---|---|
| Target-audience recognition | Can the right reader identify themselves? |
| Category clarity | Can they tell what kind of thing this is? |
| Mechanism clarity | Can they explain how it works or differs? |
| Specificity | Does it contain product-specific detail a competitor cannot inherit? |
| Action clarity | Is the next action visible and appropriate? |
| Trust and claim discipline | Are claims supported, bounded and honest? |
| Wrong-fit rejection | Does it exclude the wrong reader without confusing the right one? |
| Voice and memorability | Is there a line worth remembering that still sounds human? |

A score is evidence organisation, not mathematical truth. Repeated reader objections carry more weight than a one-point total difference.

## 6. Decide without rewrite bias

- **Keep baseline:** candidate fixes no material failure or damages a stronger dimension.
- **Adopt candidate:** it wins the important dimensions and introduces no factual or trust regression.
- **Build hybrid:** the variants win different load-bearing dimensions. Preserve only named winning lines, then re-evaluate the hybrid as a whole.
- **Revise direction:** both variants fail the same important job.

Factual, legal, safety and unsupported-claim failures override preference scores.

## Dogfooding the workflow itself

Dogfooding has two evaluation directions:

1. **Output evaluation:** Did the skill produce better copy than the frozen baseline?
2. **Process evaluation:** Which instruction, gate or omission caused each material win or loss?

Do not add a rule because one candidate happened to use a phrase you liked. Change the workflow when:

- the same failure repeats across examples;
- a single failure is severe enough to break audience understanding, trust or action;
- a directive conflicts with product truth or another load-bearing instruction.

After changing the workflow, rerun the same baseline/candidate test. A process change is not validated by the rationale that inspired it.

Avoid teaching to the detector. Keep at least one evaluation criterion that the deterministic script cannot score, and periodically use readers who did not author the workflow.

## Evidence record

For durable dogfood work, save:

- the frozen brief;
- baseline, candidate and any hybrid;
- deterministic comparison JSON;
- blind reader responses;
- rubric table;
- final decision and retained lines;
- process changes made, rejected or deferred;
- limitations of the evaluation.
