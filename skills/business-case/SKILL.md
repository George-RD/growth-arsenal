---
name: business-case
description: Build or review an internal business case, investment case, pilot case or decision proposal. Use before presentation copy. Creates the decision model first: options, costs, benefits, assumptions, scenarios, sensitivity and switching values, then hands the approved meaning to writing-core and executive-writing.
---

# Business Case

A business case is a decision model under uncertainty, not a proof dossier.

Do the economics and decision logic before writing the deck.

## Sequence

1. **Name the decision**
   Write one sentence: what is being decided now, by whom, and what remains a later decision.

   *Done when:* approval of this case cannot be confused with approval of a later scale-up.

2. **Define the counterfactual and options**
   Describe the current state if nothing changes. Compare at least:
   - do nothing / hold;
   - minimum or slower change;
   - recommended path.

   Add another option only when it changes the decision. Compare each option on the same criteria, including certain negative effects such as training load, parallel running, temporary productivity loss or transition disruption. Keep those **dis-benefits** separate from risks: a dis-benefit is expected to occur; a risk may occur.

   *Done when:* every option is compared against the same criteria and material dis-benefits are visible rather than hidden inside generic risk language.

3. **Build the assumption ledger**
   For every material input record:
   - value or range;
   - unit and period;
   - claim status: observed, estimate, assumption or scenario;
   - source or owner, recorded separately from status;
   - why the assumption is reasonable;
   - what evidence would change it.

   Use a best current estimate for the base case. Do not choose assumptions because they make the case positive.

   *Done when:* a sceptic can replace any assumption without rebuilding the model.

4. **Choose one appraisal horizon and model low, base and high cases**
   Put every option on the same cash-flow timeline before comparing value. Schedule upfront CAPEX, recurring OPEX and benefits in the periods where they occur. If timing is material or Finance requires it, use the approved discount rate and compare NPV. Do not compare one year of benefit with lifecycle cost.

   Use ranges where uncertainty is material. Keep the base case as the best current estimate, not automatically the most conservative value.

   Separate:
   - primary financial outcome;
   - secondary benefits that may overlap;
   - material dis-benefits and transition impacts;
   - historical sunk cost;
   - future incremental cost.

   Quantify a dis-benefit when a defensible cost or time measure exists. Otherwise keep it visible as a non-financial negative effect in the option comparison. Never count the same effect twice.

   Read [`references/economic-model.md`](references/economic-model.md) for appraisal-horizon, break-even and attribution rules.

   *Done when:* every option and scenario uses the same horizon and cost basis, certain negative effects are included, and the recommendation can be tested across plausible conditions.

5. **Calculate break-even and switching values**
   Ask:
   - How much benefit is required to cover incremental cost on the chosen horizon?
   - Which single assumption matters most?
   - How far must that assumption move before the preferred option changes?

   A fragile case depends on a narrow set of favourable assumptions. A robust case survives a large error in the uncertain inputs.

   *Done when:* the reader can see what must be true for the investment to be worthwhile without mixing periods or cost bases.

6. **Separate programme value from component attribution**
   When several interventions create the outcome, model the programme result first. Then test whether the component being funded needs only a smaller attributable contribution to justify its incremental cost.

   Do not assign a programme-level recovery rate to one dashboard, antenna, team or procedure without evidence.

   *Done when:* programme economics and component economics cannot be double-counted.

7. **Decide what the next phase proves**
   A pilot should reduce uncertainty in the assumptions most likely to change the decision. Do not frame it as `find out whether there is any value` when the current model already supports investment.

   Prefer:
   > The current case supports X. The pilot will replace assumptions A and B with measured data before scale.

   *Done when:* every pilot measure maps to a decision-driving assumption or operational risk.

8. **Hand off to writing when prose is requested**
   The decision model can run standalone. When the user wants a memo, report or presentation, resolve `writing-core` and `executive-writing` by skill name at this point.

   If either is unavailable:
   - keep the completed decision model intact;
   - show the relevant install command:
     - `npx skills add George-RD/growth-arsenal --skill writing-core`
     - `npx skills add George-RD/growth-arsenal --skill executive-writing`
   - pause only the prose handoff rather than recreating the missing skill locally.

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

Before prose, produce a compact decision model containing:

- decision requested;
- options;
- assumption ledger;
- appraisal horizon and cost basis;
- low/base/high economics;
- material dis-benefits and transition impacts;
- break-even value;
- switching value;
- major risks and ownership;
- recommendation;
- next evidence to replace.

The workflow or user may keep that model private and publish only the decision-relevant parts.
