# Economic model

## Use one appraisal horizon

Put costs and benefits on the same time basis before comparing them.

1. Choose the appraisal horizon that matches the decision: for example a 12-month pilot or a multi-year operating life.
2. Schedule upfront CAPEX when it occurs.
3. Schedule recurring OPEX, quantified dis-benefits and benefits in the periods when they occur.
4. Use the same units and time basis across every option.
5. When timing is material or Finance requires it, discount future cash flows using the approved rate and compare net present value (NPV), not undiscounted totals from different periods.
6. Calculate payback from cumulative net cash flow over that same schedule.

Do not compare one year of benefit with lifecycle cost, or lifecycle benefit with one year of cost.

## Primary equation

Within the chosen appraisal horizon:

```text
Net value =
  attributable benefit
  - future incremental cost
  - quantified dis-benefits
```

If a dis-benefit is already included in future incremental cost, do not subtract it again. Keep material dis-benefits that cannot be defensibly monetised visible in the option comparison rather than assigning a speculative cash value.

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

Use the same appraisal horizon and cash-flow timing in all three scenarios so only the intended assumptions change.

## Break-even

Break-even asks when the recommended path reaches zero net value against the chosen counterfactual.

Example:

```text
Break-even protected hours =
  (annual incremental cost + annualised quantified dis-benefits)
  ÷ value per protected hour
```

If quantified dis-benefits are already included in annual incremental cost, do not add them again. This annual form is valid only when the cost and quantified dis-benefits are annualised consistently with the per-hour benefit rate. For multi-year cases, solve against the scheduled or discounted cash flows instead.

A useful business-case slide often shows this number before a large ROI estimate because it lets the audience judge robustness.

## Switching value

A switching value is **not another break-even calculation**. It is the value of an assumption where the recommended option and a named competing option have equal net value; beyond that point, the preferred option changes.

Define:

```text
Advantage(x) =
  Net value of recommended option at x
  - Net value of competing option at x

Switching value = x where Advantage(x) = 0
```

Always name the competing option in the model.

### Example: affected productive time

If both options use the same value per protected hour and affected time, but have different attributable recovery and total economic burden:

```text
Total burden =
  future incremental cost
  + quantified dis-benefits

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

### Example: maximum support cost

Solve for the recommended option's support cost where its net value equals the competing option's net value. This is an option-crossover threshold, not the point where the recommended option merely reaches zero.

Show the distance between the base assumption and the switching value. Keep the underlying appraisal horizon unchanged while testing that assumption.

## Attribution

When hardware, procedure and software act together:

1. model the whole programme result;
2. allocate programme cost honestly;
3. test the software or component against its own incremental cost;
4. attribute only the contribution supported by evidence.

A component can be worth funding even when its exact share of a larger programme benefit is unknown, if the contribution required to cover its incremental cost is small and plausible.

## Non-financial value

Keep safety, client evidence, resilience, learning and strategic option value visible. Monetise them only when a defensible method exists. Do not invent cash values merely to make every benefit comparable.
