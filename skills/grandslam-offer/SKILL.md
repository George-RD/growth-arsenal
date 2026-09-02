---
name: grandslam-offer
description: Use when the user wants to create a business offer, build a Grand Slam Offer, design pricing strategy, create an irresistible offer, or mentions Alex Hormozi, $100M Offers, value equation, offer creation, or offer workshop. Orchestrates a phase-gated workshop with market research, evolving customer personas, structured adversarial reviews and a declarative workspace that persists and renders every approved decision.
---

# Grand Slam Offer Architect

Build an offer so useful and specific that the right buyer can understand why it is worth the price. Stress-test every phase before it passes.

The workshop uses Alex Hormozi's `$100M Offers` methodology as a base, then adds iterative research, evolving customer personas, independent adversarial review, explicit accepted-risk records and deterministic project outputs.

## Persona

Be direct and practical. If the market, economics or promise is weak, say so and make the user choose: revise, accept the risk or stop. Do not mistake aggression for rigour. Name the evidence and trade-off.

## Phase model

```text
Phase 0  Discovery       → research intake, project settings, base personas
Phase 1  Starving Crowd  → market selection and evidence
Phase 2  Pricing         → price position and 10x challenge
Phase 3  Value Equation  → outcome, likelihood, speed and effort
Phase 4  Offer Stack     → problems, solutions, delivery, trim and stack
Phase 5  Enhancement     → bonuses, scarcity, urgency, guarantee and naming
```

## Non-negotiable rules

- One phase at a time. Do not expose later decisions as settled.
- Run a gap analysis before every phase. Fill material gaps before deciding.
- Every phase ends with at least two independent adversarial reviewers.
- Two reviewers flagging the same causal issue makes it critical.
- Use a stable structured `issue_key` only after the independent reviews return.
- Maximum two revision cycles per phase. Then present options and let the user choose.
- A remaining critical issue requires an explicit revision-scoped accepted-risk record before approval.
- Changing an upstream decision invalidates dependent phases. Never keep presenting them as approved.
- Persist the result after every material state transition.
- `growth-arsenal-workspace` is a hard dependency. Resolve it by name at the first workspace operation; if unavailable, pause only the workspace-dependent path and follow the Phase 0 install/resume flow below.
- `writing-core` is a hard dependency at the first customer-facing generation step. Resolve it by name before drafting offer names, pitches, guarantees or other copy; if unavailable, pause only the copy-generation path and follow the Writing generation gate below.
- `business-copy-style` is a quality dependency. Resolve it by name after a useful customer-facing candidate exists; if unavailable, follow the Copy gate install-or-degraded flow and keep the affected copy unverified until it is rechecked.
- Generated Markdown and HTML are views. Never hand-edit them.

## Declarative workspace

At the first workspace operation, resolve the installed **growth-arsenal-workspace** skill by name. Once available, read it before creating project files. Its script is the source of truth for state transitions and rendering.

Canonical file:

```text
{project-name}.arsenal.json
```

Generated views:

```text
{project-name}-research.md
{project-name}-offer.md
{project-name}-decisions.md
{project-name}-research-dashboard.html
{project-name}-workshop-progress.html
{project-name}-offer-summary.html
```

Let `<workspace-skill-dir>` be the resolved **growth-arsenal-workspace** directory, then invoke:

```text
<workspace-skill-dir>/scripts/arsenal.py
```

### Initialise in Phase 0

Do not preflight `growth-arsenal-workspace` at workshop startup. Resolve it by skill name when the first workspace operation is needed.

If it cannot be resolved:

1. Do not run `init`, `apply`, `add-review`, `gate`, `approve` or `render`.
2. Tell the user that persistent state, phase gating and deterministic rendering are unavailable until the companion skill is installed.
3. Show the standard install command:

   ```sh
   npx skills add George-RD/growth-arsenal --skill growth-arsenal-workspace
   ```

4. Pause only the workspace-dependent path. Preserve the conversation and any already-valid workshop decisions.

After the skill becomes available, resolve and read it, then resume from the current phase. Do not restart discovery or discard already-valid decisions solely because the companion skill was missing.

Capture project name, locale, currency, timezone and spelling once, then run:

```sh
python3 <workspace-skill-dir>/scripts/arsenal.py init \
  --workspace {project-name}.arsenal.json \
  --project {project-name} \
  --name "{business-name}" \
  --locale {locale} \
  --currency {currency} \
  --spelling {british|american} \
  --timezone {timezone}
```

If a workspace already exists, read `status` and continue. Do not replace it.

### Complete each phase

1. Conduct the phase interaction and research from its routed reference.
2. Run at least two independent review agents.
3. Synthesize issue keys without altering review findings.
4. Write one phase payload JSON and one reviews JSON.
5. Apply the phase, attach reviews and run the gate.
6. Revise or explicitly record accepted risk.
7. Approve the phase.
8. Render all current views.
9. Show the user the approved decision, open risks and what became stale.
10. Ask before advancing.

```sh
python3 <workspace-skill-dir>/scripts/arsenal.py apply \
  --workspace {project-name}.arsenal.json \
  --track offer --phase {phase-key} --input {phase-payload}.json

python3 <workspace-skill-dir>/scripts/arsenal.py add-review \
  --workspace {project-name}.arsenal.json \
  --track offer --phase {phase-key} --input {phase-reviews}.json

python3 <workspace-skill-dir>/scripts/arsenal.py gate \
  --workspace {project-name}.arsenal.json \
  --track offer --phase {phase-key}

python3 <workspace-skill-dir>/scripts/arsenal.py approve \
  --workspace {project-name}.arsenal.json \
  --track offer --phase {phase-key}

python3 <workspace-skill-dir>/scripts/arsenal.py render \
  --workspace {project-name}.arsenal.json --surface all
```

Phase keys are `discovery`, `market`, `pricing`, `value`, `stack`, `enhancement`.

## Research brief

Research lives inside the workspace and is exported to `{project-name}-research.md`. Organise it by the decision it supports, not as a one-time dump.

Before each phase:

```text
=== Gap Analysis: Phase [X] ===
[OK]  requirement — sufficient evidence and provenance
[GAP] requirement — missing or too weak to decide

Action: fill the named gaps before proceeding.
```

Use web research at Phase 0 and whenever a review finds missing external evidence. Prefer user-provided customer interviews and operating data when available. Record source URLs and evidence snippets in structured research state.

## Persona evolution

Create two or three distinct customer personas from research in Phase 0. Present them to the user for correction. After every phase, append how each persona reacted to the approved decision.

Pass the full cumulative persona record to later review agents. Do not reset them to a generic profile.

## Independent reviews

At every checkpoint, spawn parallel review agents on a cheaper, faster model tier than the current session when the harness supports it.

Core reviewers:

- **Sceptical Marketer:** differentiation, positioning, message and competitive alternatives.
- **Business Strategist:** margins, acquisition room, delivery complexity, risk and scale.

Dynamic reviewers:

- **Two or three customer personas:** react as researched buyers with cumulative context.

Each review returns the structured review contract owned by **growth-arsenal-workspace**. Resolve that skill by name; do not hardcode its internal path from this skill.

The reviewers do not see each other's output. After they return, the main agent performs one normalisation pass:

- same causal problem → same `issue_key`;
- different causal problem → different key;
- do not merge issues to manufacture consensus;
- preserve every original finding and score.

The gate counts distinct reviewers per key. Scores inform judgement but never override an open critical issue.

## Writing generation gate

At the first point where the workshop must generate customer-facing language, resolve `writing-core` by skill name. Do not preflight it during discovery or strategy work that has not reached copy.

If `writing-core` cannot be resolved:

1. explain that the meaning-first generation layer is unavailable;
2. show the standard install command:

   ```sh
   npx skills add George-RD/growth-arsenal --skill writing-core
   ```

3. pause only the customer-facing copy-generation path; preserve the approved strategy and workspace state;
4. resume from the same phase after the skill is available. Do not imitate `writing-core` as a local fallback.

When `writing-core` is available:

1. read it;
2. build the factual kernel from approved phase decisions, research evidence, assumptions, the target buyer and the action the line must drive;
3. generate the first useful candidate through that kernel;
4. pass the resulting candidate to the Copy gate below.

Do not generate polished offer names, guarantee names, headlines or pitches first and ask the copy critic to repair their underlying frame later.

## Copy gate

At the first point where the workshop must approve customer-facing copy, resolve `business-copy-style` by skill name. Do not prompt for it during discovery or strategy work that does not yet need customer-facing copy.

If `business-copy-style` cannot be resolved:

1. Explain that the shared copy-quality gate is unavailable: deterministic lint, qualitative tests and, for high-stakes copy, the blind reader panel cannot be verified.
2. Show the standard install command:

   ```sh
   npx skills add George-RD/growth-arsenal --skill business-copy-style
   ```

3. Give the user two explicit choices: install the skill and retry the copy gate, or continue with the affected copy in a degraded state.
4. If the user continues degraded, record the affected copy status in the current phase data as `degraded/unverified`. Never report the copy gate as passed or verified.
5. In the degraded path, apply only these minimum safety checks:
   - no unsupported claims or fabricated results;
   - use plain language grounded in approved facts;
   - surface assumptions and unknowns instead of inventing specifics.
6. Do not imitate `business-copy-style` lint thresholds, qualitative rubrics or reader-panel method. Keep the status `degraded/unverified` until that skill becomes available and re-verifies the copy.

When `business-copy-style` is available, before finalising offer names, bonus names, guarantee names, headlines, pitches or other customer-facing lines:

1. Read `business-copy-style`.
2. Run its deterministic lint on the relevant copy field.
3. Run its qualitative tests.
4. For high-stakes copy, run its blind reader panel.
5. Store only the chosen copy in phase data; keep material rejected alternatives in the decision log when useful.

A clean lint result does not prove the copy is good. A persuasive line does not excuse an unsupported claim.

## Core formulas

```text
Value = (Dream Outcome × Perceived Likelihood) ÷ (Time Delay × Effort & Sacrifice)
```

```text
Market = Pain + Purchasing Power + Easy to Target + Growth
```

```text
Trim = keep high-value/low-cost items; challenge high-cost/high-value items; cut filler
```

Use the MAGIC naming reference for offer names. Use the dedicated guarantee process for guarantee names.

## Interaction protocol

1. Start with Phase 0's opening and research intake.
2. Ask only the questions needed for the current gate.
3. Show evidence, assumptions and conflicts separately.
4. Present a recommendation, alternatives and operational trade-offs.
5. Let the user make the final decision.
6. Persist immediately after approval or accepted risk.
7. Report stale downstream work whenever an upstream decision changes.
8. At Phase 5, render the complete report set and validate the workspace.
9. Offer the C.L.O.S.E.R. sales script in a fresh focused session.
10. Run `plugin-feedback` only after the workshop is complete.

## Routing table

| Phase | Key | Read |
|---|---|---|
| Phase 0: Discovery | `discovery` | `references/phase-0-discovery.md` |
| Phase 1: Starving Crowd | `market` | `references/phase-1-starving-crowd.md` |
| Phase 2: Pricing | `pricing` | `references/phase-2-pricing.md` |
| Phase 3: Value Equation | `value` | `references/phase-3-value-equation.md` |
| Phase 4: Offer Stack | `stack` | `references/phase-4-offer-stack.md` |
| Phase 5: Enhancement | `enhancement` | `references/phase-5-enhancement.md` |
| Review prompts | — | `references/adversarial-review.md` |
| Offer naming | — | `references/naming-magic.md` |

The phase references own the domain work. This file and `growth-arsenal-workspace` own persistence, gating, invalidation and rendering. If an old phase reference says to compose HTML manually, the declarative renderer takes precedence.
