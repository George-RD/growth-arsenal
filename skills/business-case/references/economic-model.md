# Economic model

## Use one appraisal horizon

Put costs and benefits on the same time basis before comparing them.

1. Choose the appraisal horizon that matches the decision: for example a 12-month pilot or a multi-year operating life.
2. Schedule upfront CAPEX when it occurs.
3. Schedule recurring OPEX, quantified dis-benefits and benefits in the periods when they occur.
4. Use the same units and period definitions across every option and scenario.
5. When timing is material or Finance requires it, discount future cash flows using the approved rate and compare net present value (NPV), not undiscounted totals from different periods.
6. Calculate payback from cumulative **incremental** cash flow or present value of the recommended option versus the named counterfactual on that same appraisal basis.

Keep the appraisal horizon and period definitions constant across Low/Base/High. Cash-flow timing **may vary** when implementation delay, benefit ramp, cost slippage or another timing change is itself an explicit scenario assumption. Do not force identical timing and thereby hide a material uncertainty.

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

Payback asks when the recommended option has recovered its **incremental economic burden versus the named counterfactual**.

For each period on the chosen scenario and appraisal basis:

```text
Incremental amount_t =
  recommended cash flow or present value_t
  - counterfactual cash flow or present value_t

Cumulative incremental amount_t =
  sum of incremental amounts through period t
```

Payback is the first modelled period where the cumulative incremental amount is zero or positive. If it is already non-negative in period 1, report immediate or first-period payback according to the model's period definition. If it begins negative, payback is the first later period where it reaches zero or becomes positive.

Use cumulative undiscounted incremental cash flow when discounting is not material. Use cumulative incremental present value when discounted payback is the approved basis. Always name the counterfactual and state which basis was used.

If payback does not occur before the appraisal horizon ends, record `NO PAYBACK WITHIN HORIZON`. If the required timing or value inputs are unavailable, record `UNKNOWN` and identify the evidence needed rather than omitting payback.

## Break-even

Break-even asks where the recommended path's **incremental net value versus the chosen counterfactual** reaches zero.
Record the scenario used, normally Base; the appraisal basis; and the non-tested assumptions held constant at that scenario's values. List any exceptions so the threshold and headroom can be reproduced.

Define:

```text
Incremental advantage(x) =
  Net value of recommended option at x
  - Net value of counterfactual option at x

Break-even = x where Incremental advantage(x) = 0
```

Always name the counterfactual. It is usually Hold / do nothing, but use the actual decision baseline when that is different.

### Shortcut when the counterfactual has zero relevant economics

If the chosen counterfactual has zero relevant benefit, cost and quantified dis-benefit on the appraisal basis, and the tested driver changes only the recommended option, a shortcut is valid:

```text
Break-even protected hours =
  total economic burden of recommended option
  ÷ value per protected hour

Total economic burden =
  future incremental cost
  + separately quantified dis-benefits not already included in that cost
```

Do not use this shortcut when the counterfactual has its own material benefit, cost, dis-benefit or response to the tested driver.

### General affected-time break-even

If both recommended and counterfactual options have different recovery and economic burdens but share the same affected-time and value-per-hour driver:

```text
Affected-time break-even =
  (burden_recommended - burden_counterfactual)
  ÷ [value_per_hour × (recovery_recommended - recovery_counterfactual)]
```

Here each `burden` uses non-overlapping cost components: future incremental cost plus only separately quantified dis-benefits not already included in that cost.

Use this only when the denominator is non-zero and the simplified assumptions hold. Otherwise solve the two complete option cash-flow models directly.

A useful business-case slide often shows break-even before a large ROI estimate because it lets the audience judge how much benefit the recommended path must add over the counterfactual.

## Switching value

A switching value is the value of an assumption where the recommended option and a **named competing option** have equal net value; beyond that point, the preferred option changes.
Record the scenario used, normally Base; the appraisal basis; and the non-tested assumptions held constant at that scenario's values. List any exceptions so the crossover and headroom can be reproduced.

Define:

```text
Advantage(x) =
  Net value of recommended option at x
  - Net value of competing option at x

Switching value = x where Advantage(x) = 0
```

Always name the competing option in the model. It is often the minimum/slower-change path rather than Hold / do nothing.

### Example: affected productive time

If both options use the same value per protected hour and affected time, but have different attributable recovery and total economic burden:

```text
Total burden =
  future incremental cost
  + separately quantified dis-benefits not already included in that cost

Affected-time switching value =
  (burden_recommended - burden_competing)
  ÷ [value_per_hour × (recovery_recommended - recovery_competing)]
```

Use this only when the denominator is non-zero and the simplified assumptions hold. Otherwise solve the two complete option cash-flow models directly.

### Example: recovery-rate switching value

For a fixed affected-time base:

```text
Recovery switching value for recommended option =
  recovery_competing
  + (burden_recommended - burden_competing)
    ÷ (affected_time × value_per_hour)
```

Use this shortcut only when `affected_time` and `value_per_hour` are both non-zero and the simplified assumptions hold. Otherwise solve the complete option models directly.

### Example: maximum support cost

Solve for the recommended option's support cost where its net value equals the competing option's net value. This is an option-crossover threshold, not the point where the recommended option merely reaches zero.

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
