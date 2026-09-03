# Business Case Decision Model

## Decision

- **Decision now:** [what is being decided]
- **Decision owner:** [person or role]
- **Later decisions:** [what this decision does not approve]
- **Decision date / window:** [date or period]

## Options

Use neutral option names while building the model. Record the selected option only in Recommendation.

| Option | What changes | Certain dis-benefits | Main risks | Role in appraisal |
|---|---|---|---|---|
| Hold / do nothing | [ ] | [ ] | [ ] | [ ] |
| Minimum / slower change | [ ] | [ ] | [ ] | [ ] |
| [Named change option] | [ ] | [ ] | [ ] | [candidate under appraisal] |

## Assumption ledger

Every material input needs a claim status and evidence provenance. `Owner` is separate from `Source`.

| Input | Value / range | Unit / period | Status | Source | Owner | Why reasonable | Evidence that would change it |
|---|---:|---|---|---|---|---|---|
| [ ] | [ ] | [ ] | OBSERVED / ESTIMATED / ASSUMED / SCENARIO / UNKNOWN | [source or UNAVAILABLE] | [person/role or N/A] | [ ] | [ ] |

## Appraisal basis

- **Horizon:** [e.g. 12 months / 3 years]
- **Period anchor and interval:** [start date / t0; month, quarter or year]
- **Cash-flow timing convention:** [period start / mid-period / period end]
- **Currency / value basis:** [ ]
- **Discount rate / NPV treatment:** [rate or NOT MATERIAL]
- **Sunk costs excluded from next-decision economics:** [ ]
- **Benefit overlap treatment:** [how double counting is avoided]

## Cash-flow schedule

Use one row per **scenario, option and period**. For a one-period appraisal, include Low/Base/High rows for each option. For a multi-period appraisal, repeat each scenario/option across every period needed to reproduce NPV and payback through the full horizon. Keep the appraisal horizon, period anchor, interval and cash-flow timing convention consistent across scenarios; allow timing to differ when implementation delay, benefit ramp, cost slippage or another timing change is itself an explicit scenario assumption.

| Scenario | Period | Option | Attributable benefit | Future incremental cost | Separately quantified dis-benefits not in incremental cost | Net cash flow | Discount factor | Present value |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Low | [ ] | Hold / do nothing | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Low | [ ] | Minimum / slower change | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Low | [ ] | [Named change option] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Base | [ ] | Hold / do nothing | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Base | [ ] | Minimum / slower change | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Base | [ ] | [Named change option] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| High | [ ] | Hold / do nothing | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| High | [ ] | Minimum / slower change | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| High | [ ] | [Named change option] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

## Option economics

Use the same appraisal horizon and cost basis for every row. Totals are undiscounted for a one-period case or NPV when discounting is material. These totals must reconcile to the cash-flow schedule above.

| Option | Scenario | Attributable benefit | Future incremental cost | Separately quantified dis-benefits not in incremental cost | Net value / NPV | Key assumptions changed |
|---|---|---:|---:|---:|---:|---|
| Hold / do nothing | Low | [ ] | [ ] | [ ] | [ ] | [ ] |
| Hold / do nothing | Base | [ ] | [ ] | [ ] | [ ] | [ ] |
| Hold / do nothing | High | [ ] | [ ] | [ ] | [ ] | [ ] |
| Minimum / slower change | Low | [ ] | [ ] | [ ] | [ ] | [ ] |
| Minimum / slower change | Base | [ ] | [ ] | [ ] | [ ] | [ ] |
| Minimum / slower change | High | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named change option] | Low | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named change option] | Base | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named change option] | High | [ ] | [ ] | [ ] | [ ] | [ ] |

### Non-financial and secondary benefits

| Option | Benefit | Evidence / status | Overlap treatment | Decision relevance |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [how it remains separate from quantified value] | [ ] |

### Unquantified dis-benefits

- [certain negative effect that is material but not defensibly monetised]

## Payback

Payback is when the candidate option under appraisal has recovered its **incremental economic burden versus the named counterfactual** on the same cash-flow schedule. Use cumulative incremental net cash flow when discounting is not material; use cumulative incremental present value when discounted payback is the approved basis.

- **Candidate option under appraisal:** [named option; this is not a pre-selected recommendation]
- **Counterfactual:** [normally Hold / do nothing, or state another]
- **Scenario reported:** [Base; add Low/High when decision-relevant]
- **Basis:** [cumulative incremental net cash flow / cumulative incremental present value]
- **Period convention:** [anchor, interval and cash-flow timing]
- **First incremental burden period:** [period/date, or NONE]
- **Payback period / date:** [first period at or after the burden where cumulative value reaches zero or becomes positive; IMMEDIATE / FIRST-PERIOD PAYBACK; NO INCREMENTAL ECONOMICS; NO PAYBACK WITHIN HORIZON; or UNKNOWN]
- **Later reversal:** [NONE, or first later period/date cumulative value becomes negative again]
- **End-of-horizon cumulative amount:** [ ]
- **Calculation / source:** [show the candidate-minus-counterfactual cumulative calculation]
- **Cumulative schedule:** [one row per period from the first modelled period through the final appraisal period; the three rows below illustrate a three-period horizon]

| Scenario | Period | Candidate cash flow / PV | Counterfactual cash flow / PV | Incremental amount | Cumulative incremental amount |
|---|---|---:|---:|---:|---:|
| Base | Period 1 | [ ] | [ ] | [ ] | [ ] |
| Base | Period 2 | [ ] | [ ] | [ ] | [ ] |
| Base | Period 3 / final period | [ ] | [ ] | [ ] | [ ] |

Ignore any leading periods where both options have zero economics when identifying the first burden, but retain every non-zero period and every later period through the full appraisal horizon in this table. If every incremental amount through the horizon is zero, record `NO INCREMENTAL ECONOMICS` and no payback date. Otherwise, payback is the first period at or after the burden where cumulative value reaches zero or becomes positive. If it later becomes negative, keep the first-crossing payback date and disclose the reversal period separately. If there is no incremental burden but the schedule contains a non-zero amount, start the search at the first non-zero incremental period. If required inputs are unavailable, record `UNKNOWN` and name the evidence needed instead of omitting this section.

## Break-even

Break-even is the point where the candidate option under appraisal's **incremental net value versus the chosen counterfactual** reaches zero.

- **Candidate option under appraisal:** [ ]
- **Counterfactual:** [normally Hold / do nothing, or state another]
- **Scenario:** [normally Base; state another when decision-relevant]
- **Appraisal basis:** [horizon, period convention, currency/value basis and NPV treatment]
- **Driver:** [e.g. affected productive time]
- **Assumptions held constant:** [all non-tested inputs held at the named scenario values; list any exceptions]
- **Break-even value:** [ ]
- **Base-case value:** [ ]
- **Headroom:** [ ]
- **Calculation / source:** [show the candidate-vs-counterfactual equality or the valid zero-counterfactual shortcut]

## Switching value

Switching value is the point where a named competing option becomes preferable to the candidate option under appraisal.

- **Candidate option under appraisal:** [ ]
- **Competing option:** [ ]
- **Scenario:** [normally Base; state another when decision-relevant]
- **Appraisal basis:** [horizon, period convention, currency/value basis and NPV treatment]
- **Driver / assumption tested:** [ ]
- **Assumptions held constant:** [all non-tested inputs held at the named scenario values; list any exceptions]
- **Base-case value:** [ ]
- **Switching value:** [ ]
- **Distance / headroom:** [ ]
- **Calculation / source:** [show equality/crossover using both option models]
- **Relationship to break-even:** [different threshold, or SAME only when the counterfactual/competitor, tested driver or assumption, appraisal basis and calculation are all identical]

## Programme and component attribution

- **Programme outcome:** [ ]
- **Component being funded:** [ ]
- **Programme-level effect that must not be assigned wholly to the component:** [ ]
- **Component contribution required to justify its incremental cost:** [ ]

## Commercial and delivery feasibility

| Option | Area | Requirement / dependency | Evidence / status | Owner | Lead time / constraint | Decision impact |
|---|---|---|---|---|---|---|
| [Named option] | Vendors / partners | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named option] | Hardware / infrastructure | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named option] | Licences / contracts / procurement | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named option] | Delivery capacity / skills | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Named option] | Operational support model | [ ] | [ ] | [ ] | [ ] | [ ] |

## Risks and ownership

| Risk | Why it matters | Mitigation / fallback | Owner | Decision trigger |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] |

## Governance and delivery gates

- **Executive owner:** [ ]
- **Delivery owner:** [ ]
- **Benefits owner:** [ ]
- **Operational support owner:** [ ]

| Milestone / decision gate | Owner | Date / window | Evidence required | Decision / exit condition |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] |

## Recommendation

- **Selected option:** [named option, or UNKNOWN]
- **Recommendation status:** [RECOMMEND / CONDITIONAL / UNKNOWN]
- **Deciding condition or missing evidence:** [N/A, or the condition/evidence that would settle the result]
- **Reason:** [why this result follows from option-by-option economics, low/base/high, dis-benefits, payback, break-even, switching values and delivery feasibility]

## Next evidence to replace

Every `CONDITIONAL` or `UNKNOWN` recommendation requires a row for its deciding condition or missing evidence. Record `N/A` only for a settled recommendation with no further evidence stage.

| Assumption / risk | Evidence to collect | Owner | When | Decision it can change |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] |
