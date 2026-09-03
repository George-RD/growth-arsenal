---
name: business-case
description: "Build or review an internal business case, investment case, pilot case or decision proposal. Use before presentation copy. Creates the decision model first: options, costs, benefits, assumptions, scenarios, sensitivity and switching values, then hands the approved meaning to writing-core and executive-writing."
---

# Business Case

A business case is a decision model under uncertainty, not a proof dossier.

Do the economics and decision logic before writing the deck.

Before analysis, copy [`templates/decision-model.md`](templates/decision-model.md) and fill it as the model develops. The template is the deterministic decision record; later prose may expose only the fields the audience needs.

## Sequence

1. **Name the decision**
   Fill the template's Decision section: what is being decided now, by whom, the decision window, and what remains a later decision.

   *Done when:* approval of this case cannot be confused with approval of a later scale-up.

2. **Define the counterfactual and options**
   Describe the current state if nothing changes. Use neutral names and compare at least:
   - do nothing / hold;
   - minimum or slower change;
   - a named change option under appraisal.

   Add another option only when it changes the decision. Compare each option on the same criteria, including certain negative effects such as training load, parallel running, temporary productivity loss or transition disruption. Keep those **dis-benefits** separate from risks: a dis-benefit is expected to occur; a risk may occur.

   *Done when:* every option is compared against the same criteria and material dis-benefits are visible rather than hidden inside generic risk language.

3. **Build the assumption ledger**
   For every material input record:
   - value or range;
   - unit and period;
   - claim status: observed, estimate, assumption or scenario;
   - source: the named evidence/provenance, or `UNAVAILABLE` when no source exists;
   - owner: the person or role responsible for confirming, replacing or managing the input, when applicable;
   - why the assumption is reasonable;
   - what evidence would change it.

   Source and owner are different fields. An owner cannot substitute for evidence provenance.

   Use a best current estimate for the base case. Do not choose assumptions because they make the case positive.

   *Done when:* a sceptic can replace any assumption without rebuilding the model, and every material claim has explicit provenance or `UNAVAILABLE`.

4. **Choose one appraisal horizon and model low, base and high cases**
   Put every option on the same appraisal horizon and period convention before comparing value. Record the period anchor/date, interval and whether cash flows occur at period start, mid-period or period end. Schedule upfront CAPEX, recurring OPEX, quantified dis-benefits and benefits in the periods where they occur. If timing is material or Finance requires it, use the approved discount rate and compare NPV. Do not compare one year of benefit with lifecycle cost.

   Use ranges where uncertainty is material. Keep the base case as the best current estimate, not automatically the most conservative value. Cash-flow timing may vary across Low/Base/High when implementation delay, benefit ramp, cost slippage or another timing change is itself an explicit scenario assumption; keep the horizon and period convention consistent so the scenarios remain comparable.

   Separate:
   - primary financial outcome;
   - secondary benefits that may overlap;
   - material dis-benefits and transition impacts;
   - historical sunk cost;
   - future incremental cost.

   Quantify a dis-benefit when a defensible cost or time measure exists. Keep the monetary fields non-overlapping: if an effect is already inside future incremental cost, do not also record it as a separate quantified dis-benefit. Otherwise keep it visible as a non-financial negative effect in the option comparison. Never count the same effect twice.

   Read [`references/economic-model.md`](references/economic-model.md) for appraisal-horizon, payback, break-even, switching and attribution rules.

   *Done when:* every option and scenario uses the same horizon and cost/value basis, intended timing assumptions are explicit, certain negative effects are included once, and the recommendation can be tested across plausible conditions.

5. **Calculate payback, break-even and switching values for a candidate**
   Name the change option being tested; this is not yet the recommendation. Calculate all three:
   - **Payback:** when the candidate option's cumulative incremental cash flow or present value versus the named counterfactual recovers its incremental burden.
   - **Break-even:** where the candidate option's incremental net value versus the chosen counterfactual reaches zero for the tested driver.
   - **Switching value:** where the candidate option and a named competing option have equal net value and the preferred option changes beyond that point.

   Use the same appraisal basis for payback as the option economics: cumulative net cash flow when discounting is not material, or cumulative present value when discounted payback is the approved basis. Start at the first period containing an incremental economic burden, ignoring any leading periods where both options have zero economics. If that period aggregates burden and benefit and is already non-negative versus the counterfactual, report immediate or first-period payback. Retain the calculation through the full horizon and disclose any later reversal separately. If there is no incremental burden, start at the first non-zero incremental period. If payback does not occur within the horizon, record `NO PAYBACK WITHIN HORIZON`. If inputs are missing, record `UNKNOWN` and the evidence needed.

   The counterfactual for break-even and payback is usually Hold / do nothing. The competing option for switching may instead be the minimum/slower-change path. For each threshold, name the scenario and full appraisal basis including period convention, and hold non-tested assumptions at that scenario's values unless explicit exceptions are recorded. Use a shortcut formula only when every non-tested benefit difference is zero or cancels; otherwise solve the complete option models. Break-even and switching may be recorded as `SAME` only when the option comparison, tested driver/assumption, appraisal basis and equality being solved are all identical. The same option pair with a different driver is still a different threshold.

   Ask:
   - When does the candidate option recover its incremental economic burden versus the counterfactual?
   - How much benefit is required to cover that burden on the chosen horizon?
   - Which single assumption matters most?
   - How far must that assumption move before the preferred option changes?

   A fragile case depends on a narrow set of favourable assumptions. A robust case survives a large error in the uncertain inputs.

   *Done when:* the template records payback status/period, the full-horizon cumulative calculation and any later reversal; both threshold roles; the named candidate, counterfactual and competing option; each threshold's tested driver, scenario, full appraisal basis and held-constant assumptions; and the headroom from the base case.

6. **Separate programme value from component attribution**
   When several interventions create the outcome, model the programme result first. Then test whether the component being funded needs only a smaller attributable contribution to justify its incremental cost.

   Do not assign a programme-level recovery rate to one dashboard, antenna, team or procedure without evidence.

   *Done when:* programme economics and component economics cannot be double-counted.

7. **Test delivery feasibility and set governance**
   Fill the template's Commercial and delivery feasibility section for every material candidate. Test each proposed path against vendors or partners, hardware and infrastructure, licences and contracts, procurement, delivery capacity and skills, operational support, lead times and sequencing. Record missing evidence as `UNKNOWN` or `UNAVAILABLE`; an attractive economic result does not prove an option can be delivered.

   Name the executive, delivery, benefits and operational support owners. Add the material milestones and decision gates with their dates or windows, required evidence and exit conditions.

   *Done when:* every candidate's material commercial, capacity, support and timing constraints are evidenced or explicitly open, the feasible paths have credible owners, and later commitments cannot be confused with the current decision.

8. **Derive the recommendation**
   Compare the completed option economics, Low/Base/High cases, dis-benefits, non-financial benefits, payback, break-even, switching values, risks and delivery feasibility. Fill the template's Recommendation section from that evidence.

   Select any option the model supports. Record the selected option separately from its `RECOMMEND`, `CONDITIONAL` or `UNKNOWN` status. Every conditional or unknown result names the deciding condition or missing evidence. A proposed change or pilot is a candidate, not a predetermined winner.

   *Done when:* the selected option, status and deciding condition or missing evidence can be traced to the completed model without changing an assumption to produce the desired answer.

9. **Decide what the next phase proves**
   If the selected or conditional path includes a pilot, phased rollout or further evidence stage, use it to reduce uncertainty in the assumptions most likely to change the next decision. When the current model already supports investment, prefer:
   > The current case supports X. The pilot will replace assumptions A and B with measured data before scale.

   Fill the template's Next evidence section so each proposed measurement states which decision it could change. Every `CONDITIONAL` or `UNKNOWN` recommendation must map its deciding condition or missing evidence to a row. Record `N/A` only for a settled recommendation with no further evidence stage.

   *Done when:* every proposed measure maps to a decision-driving assumption, feasibility constraint or operational risk; every unresolved recommendation condition has an evidence row; or a settled recommendation records why no further evidence stage is required.

10. **Hand off to writing when prose is requested**
    The decision model can run standalone. When the user wants a memo, report or presentation, resolve `writing-core` and `executive-writing` independently by skill name at this point.

    For each missing companion:

    - keep the completed decision model intact;
    - show only that companion's install command:
      - missing `writing-core` → `npx skills add George-RD/growth-arsenal --skill writing-core`
      - missing `executive-writing` → `npx skills add George-RD/growth-arsenal --skill executive-writing`

    Pause only the prose handoff until both required companions are available. Do not recreate a missing skill locally.

    When both are available, pass the completed decision model, assumptions and selected evidence to `writing-core`, then `executive-writing`. Mark the model as already completed so `writing-core` does not re-enter this workflow. Use `business-copy-style` only after the first useful prose exists.

    *Done when:* the presentation is an expression of the model rather than the place where the model is invented.

## Evidence posture

Use estimates when exact data are impractical or unavailable. Label them and show sensitivity. Perfect data are not required for a business decision; hidden assumptions are the problem.

Reasonable assumptions should come from, in order:

1. measured internal data;
2. comparable internal work;
3. named subject-matter estimate;
4. commercial/financial proxy;
5. external benchmark;
6. explicit scenario assumption.

If the only positive result requires a favourable scenario chosen to justify the project, the case is weak.

## Output contract

The completed output is a filled copy of [`templates/decision-model.md`](templates/decision-model.md). Do not drop a section because the answer is unknown; record `UNKNOWN`, `UNAVAILABLE`, `N/A`, `NO PAYBACK WITHIN HORIZON`, or the appropriate open state so omissions are visible.

The workflow or user may keep that model private and publish only the decision-relevant parts.
