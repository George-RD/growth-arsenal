# Economic model

## Use one appraisal horizon

Put costs and benefits on the same time basis before comparing them.

1. Choose the appraisal horizon that matches the decision: for example a 12-month pilot or a multi-year operating life.
2. Schedule upfront CAPEX when it occurs.
3. Schedule recurring OPEX, quantified dis-benefits and benefits in the periods when they occur.
4. Use the same units and period convention across every option and scenario: record the anchor/date, interval, and whether cash flows occur at period start, mid-period or period end.
5. When timing is material or Finance requires it, discount future cash flows using the approved rate and compare net present value (NPV), not undiscounted totals from different periods.
6. Calculate payback from cumulative **incremental** cash flow or present value of the candidate option under appraisal versus the named counterfactual on that same appraisal basis.

Keep the appraisal horizon and period convention constant across Low/Base/High. Cash-flow timing **may vary** when implementation delay, benefit ramp, cost slippage or another timing change is itself an explicit scenario assumption. Do not force identical timing and thereby hide a material uncertainty.

Do not compare one year of benefit with lifecycle cost, or lifecycle benefit with one year of cost.

## Primary equation

Within the chosen appraisal horizon:

```text
Net value =
  attributable benefit
  - future incremental cost
  - separately quantified dis-benefits
```

The cost components must be non-overlapping. `Separately quantified dis-benefits` means only dis-benefits **not already included** in future incremental cost. If a source cost bundles a training, transition or parallel-running impact, either split the bundle into non-overlapping fields or set the separate dis-benefit amount for that effect to zero. Never count the same effect twice.

Keep material dis-benefits that cannot be defensibly monetised visible in the option comparison rather than assigning a speculative cash value.

For recovered productive time:

```text
Protected value =
  affected productive time
  × recovery attributable to the programme/component
  × approved economic value per unit of time
```

Match units. Do not apply a calendar-day value to productive hours without an approved conversion.

## Low / base / high

Use three scenarios when uncertainty is material:

- **Low:** credible adverse assumptions.
- **Base:** best current estimate.
- **High:** credible favourable assumptions.

Do not make the low case absurdly pessimistic or the high case aspirational.

Use the same appraisal horizon, period definitions and cost/value basis in all three scenarios. Allow the values **and timing** of cash flows to vary when those changes are explicit scenario assumptions.

## Payback

Payback asks when the candidate option under appraisal has recovered its **incremental economic burden versus the named counterfactual**.

For each period on the chosen scenario and appraisal basis:

```text
Incremental amount_t =
  candidate cash flow or present value_t
  - counterfactual cash flow or present value_t

Cumulative incremental amount_t =
  sum of incremental amounts through period t
```

Identify the first period containing an incremental economic burden; leading periods where both options have zero economics cannot trigger payback. Calculate and display cumulative incremental value through the full appraisal horizon. If every incremental amount in the horizon is zero, record `NO INCREMENTAL ECONOMICS` and no payback date. Otherwise, payback is the first period at or after the burden where cumulative value reaches zero or becomes positive. If the burden period aggregates cost and benefit and already qualifies, report immediate or first-period payback according to the period convention. If cumulative value later becomes negative, keep the first-crossing payback date and disclose the reversal period separately. If there is no incremental burden but the schedule contains a non-zero amount, start the search at the first non-zero incremental period.

Use cumulative undiscounted incremental cash flow when discounting is not material. Use cumulative incremental present value when discounted payback is the approved basis. Always name the candidate option and counterfactual, and state which basis was used.

If payback does not occur by the end of the appraisal horizon, record `NO PAYBACK WITHIN HORIZON`. Disclose any later reversal after a payback crossing. If the required timing or value inputs are unavailable, record `UNKNOWN` and identify the evidence needed rather than omitting payback.

## Break-even

Break-even asks where the candidate option under appraisal's **incremental net value versus the chosen counterfactual** reaches zero.
Record the scenario used, normally Base; the full appraisal basis including period convention; and the non-tested assumptions held constant at that scenario's values. List any exceptions so the threshold and headroom can be reproduced.

Define:

```text
Incremental advantage(x) =
  Net value of candidate option at x
  - Net value of counterfactual option at x

Break-even = x where Incremental advantage(x) = 0
```

Always name the counterfactual. It is usually Hold / do nothing, but use the actual decision baseline when that is different.

### Shortcut when the counterfactual has zero relevant economics

If the chosen counterfactual has zero relevant benefit, cost and quantified dis-benefit on the appraisal basis, `value per protected hour` is non-zero on that basis, the tested driver changes only the candidate option, every other attributable-benefit term is zero or cancels between the options, and every non-tested formula term remains constant across the tested range, a shortcut is valid:

```text
Break-even protected hours =
  total economic burden of candidate option
  ÷ value per protected hour

Total economic burden =
  future incremental cost
  + separately quantified dis-benefits not already included in that cost
```

Do not use this shortcut when the counterfactual has its own material economics or response to the tested driver, or when a fixed attributable-benefit difference remains outside the tested protected-hours term.

Never divide by a zero value term. Solve the complete option models and record whether there is no finite threshold or every tested value is equal, as appropriate.

This shortcut returns **protected/recovered hours**. To express the threshold as affected time, divide protected hours by the candidate's attributable recovery rate when it is non-zero, or use the general formula below.

### General affected-time break-even

If both candidate and counterfactual options have different recovery and economic burdens but share the same affected-time and value-per-hour driver, and every other attributable-benefit difference is zero or cancels:

```text
Affected-time break-even =
  (burden_candidate - burden_counterfactual)
  ÷ [value_per_hour × (recovery_candidate - recovery_counterfactual)]
```

Here each `burden` uses non-overlapping cost components: future incremental cost plus only separately quantified dis-benefits not already included in that cost.

Use this only when the denominator is non-zero, both burden terms, `value_per_hour`, both recovery terms and every other non-tested formula term remain constant across the tested affected-time range, every non-tested benefit difference is zero or cancels, and the simplified assumptions hold. Otherwise solve the two complete option cash-flow models directly.

A useful business-case slide often shows break-even before a large ROI estimate because it lets the audience judge how much benefit the candidate option must add over the counterfactual.

## Switching value

A switching value is the value of an assumption where the candidate option under appraisal and a **named competing option** have equal net value; beyond that point, the preferred option changes.
Record the scenario used, normally Base; the full appraisal basis including period convention; and the non-tested assumptions held constant at that scenario's values. List any exceptions so the crossover and headroom can be reproduced.

Define:

```text
Advantage(x) =
  Net value of candidate option at x
  - Net value of competing option at x

Switching value = x where Advantage(x) = 0
```

Always name the competing option in the model. It is often the minimum/slower-change path rather than Hold / do nothing.

### Example: affected productive time

If both options use the same value per protected hour and affected time, have different attributable recovery and total economic burden, and every other attributable-benefit difference is zero or cancels:

```text
Total burden =
  future incremental cost
  + separately quantified dis-benefits not already included in that cost

Affected-time switching value =
  (burden_candidate - burden_competing)
  ÷ [value_per_hour × (recovery_candidate - recovery_competing)]
```

Use this only when the denominator is non-zero, both burden terms, `value_per_hour`, both recovery terms and every other non-tested formula term remain constant across the tested affected-time range, every non-tested benefit difference is zero or cancels, and the simplified assumptions hold. Otherwise solve the two complete option cash-flow models directly.

### Example: recovery-rate switching value

For a fixed affected-time base where every other attributable-benefit difference is zero or cancels:

```text
Recovery switching value for candidate option =
  recovery_competing
  + (burden_candidate - burden_competing)
    ÷ (affected_time × value_per_hour)
```

Use this shortcut only when `affected_time` and `value_per_hour` are both non-zero and constant, both burden terms, `recovery_competing` and every other non-tested formula term remain constant across the tested candidate-recovery range, every non-tested benefit difference is zero or cancels, and the simplified assumptions hold. Otherwise solve the complete option models directly.

### Example: maximum support cost

Solve for the candidate option's support cost where its net value equals the competing option's net value. This is an option-crossover threshold, not the point where the candidate option merely reaches zero.

Show the distance between the base assumption and the switching value. Keep the underlying appraisal horizon unchanged while testing that assumption.

### When break-even and switching coincide

Record `SAME` only when the threshold calculations are genuinely identical: the break-even counterfactual and switching competitor are the same option, the tested driver or assumption is the same, the appraisal basis is the same, and the same equality is being solved. If any of those differ, calculate and record separate thresholds even when the option pair is identical.

## Attribution

When hardware, procedure and software act together:

1. model the whole programme result;
2. allocate programme cost honestly;
3. test the software or component against its own incremental cost;
4. attribute only the contribution supported by evidence.

A component can be worth funding even when its exact share of a larger programme benefit is unknown, if the contribution required to cover its incremental cost is small and plausible.

## Non-financial value

Keep safety, client evidence, resilience, learning and strategic option value visible. Monetise them only when a defensible method exists. Do not invent cash values merely to make every benefit comparable.
