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
   - source: the named evidence/provenance, or `UNAVAILABLE` when no source exists;
   - owner: the person or role responsible for confirming, replacing or managing the input, when applicable;
   - why the assumption is reasonable;
   - what evidence would change it.

   Source and owner are different fields. An owner cannot substitute for evidence provenance.

   Use a best current estimate for the base case. Do not choose assumptions because they make the case positive.

   *Done when:* a sceptic can replace any assumption without rebuilding the model, and every material claim has explicit provenance or `UNAVAILABLE`.

4. **Choose one appraisal horizon and model low, base and high cases**
   Put every option on the same cash-flow timeline before comparing value. Schedule upfront CAPEX, recurring OPEX, quantified dis-benefits and benefits in the periods where they occur. If timing is material or Finance requires it, use the approved discount rate and compare NPV. Do not compare one year of benefit with lifecycle cost.

   Use ranges where uncertainty is material. Keep the base case as the best current estimate, not automatically the most conservative value.

   Separate:
   - primary financial outcome;
   - secondary benefits that may overlap;
   - material dis-benefits and transition impacts;
   - historical sunk cost;
   - future incremental cost.

   Quantify a dis-benefit when a defensible cost or time measure exists. Otherwise keep it visible as a non-financial negative effect in the option comparison. Never count the same effect twice.

   Read [`references/economic-model.md`](references/economic-model.md) for appraisal-horizon, break-even, switching and attribution rules.

   *Done when:* every option and scenario uses the same horizon and cost basis, certain negative effects are included, and the recommendation can be tested across plausible conditions.

5. **Calculate break-even and switching values**
   Calculate both:
   - **Break-even:** where the recommended path reaches zero net value against the counterfactual.
   - **Switching value:** where a named competing option becomes preferable to the recommended path.

   Ask:
   - How much benefit is required to cover incremental cost and quantified dis-benefits on the chosen horizon?
   - Which single assumption matters most?
   - How far must that assumption move before the preferred option changes?

   A fragile case depends on a narrow set of favourable assumptions. A robust case survives a large error in the uncertain inputs.

   *Done when:* the template records both thresholds, the competing option for the switching value, and the headroom from the base case.

6. **Separate programme value from component attribution**
   When several interventions create the outcome, model the programme result first. Then test whether the component being funded needs only a smaller attributable contribution to justify its incremental cost.

   Do not assign a programme-level recovery rate to one dashboard, antenna, team or procedure without evidence.

   *Done when:* programme economics and component economics cannot be double-counted.

7. **Decide what the next phase proves**
   A pilot should reduce uncertainty in the assumptions most likely to change the decision. Do not frame it as `find out whether there is any value` when the current model already supports investment.

   Prefer:
   > The current case supports X. The pilot will replace assumptions A and B with measured data before scale.

   Fill the template's Next evidence section so each proposed measurement states which decision it could change.

   *Done when:* every pilot measure maps to a decision-driving assumption or operational risk.

8. **Hand off to writing when prose is requested**
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

The completed output is a filled copy of [`templates/decision-model.md`](templates/decision-model.md). Do not drop a section because the answer is unknown; record `UNKNOWN`, `UNAVAILABLE`, `N/A`, or the appropriate open state so omissions are visible.

The workflow or user may keep that model private and publish only the decision-relevant parts.
