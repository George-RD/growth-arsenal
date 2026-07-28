---
name: growth-arsenal-workspace
description: Use when a growth-arsenal workshop needs to initialise, validate, update, gate, approve, invalidate or render its persistent project state. Provides the declarative workspace, structured review contract and deterministic Growth Arsenal reports shared by grandslam-offer and hundred-million-leads. Do not use it to make business judgements; the calling workshop owns research, synthesis and copy.
---

# Growth Arsenal Workspace

This supporting skill separates judgement from mechanics.

- The calling workshop and its review agents decide what is true, useful and persuasive.
- `scripts/arsenal.py` validates state, counts review consensus, records approval, invalidates dependent phases and renders files.
- The JSON workspace is canonical. Markdown and HTML are generated views.
- Never hand-edit generated reports. Change state or the shared assets and render again.

## Core invariant

```text
research + decisions + structured reviews
                  │
                  ▼
       <project>.arsenal.json
                  │
          deterministic build
       ┌──────────┼───────────┐
       ▼          ▼           ▼
   offer.md   progress.html   research.html
```

## Resolve the script

Paths in this skill are relative to this `SKILL.md`. Resolve the installed skill directory once, then use:

```sh
python3 scripts/arsenal.py --help
```

When another skill calls this one, it should resolve `../growth-arsenal-workspace/scripts/arsenal.py` relative to its own skill directory. Do not assume the user's current directory contains the script.

## Standard flow

### 1. Initialise once

```sh
python3 scripts/arsenal.py init \
  --workspace acme.arsenal.json \
  --project acme \
  --name "Acme" \
  --locale en-GB \
  --currency GBP \
  --spelling british \
  --timezone Europe/London
```

Do not replace an existing workspace unless the user explicitly approves `--force`.

### 2. Apply one phase payload

Write a small JSON payload. The agent supplies the meaning; the script supplies the state transition.

```json
{
  "summary": "Independent garages with missed enquiries are the approved market.",
  "data": {
    "market": "Independent garages with 3-20 staff",
    "pain_score": 8,
    "purchasing_power_score": 7,
    "targeting_score": 8,
    "growth_score": 6
  },
  "research_patch": {
    "market_identity": {
      "core_market": "Wealth",
      "niche": "Independent garages losing inbound enquiries"
    }
  },
  "evidence_refs": ["research:source-04", "research:source-11"]
}
```

```sh
python3 scripts/arsenal.py apply \
  --workspace acme.arsenal.json \
  --track offer \
  --phase market \
  --input phase-market.json
```

Applying an upstream phase marks any dependent work stale. Do not suppress that signal.

### 3. Add structured independent reviews

Each reviewer returns the contract in `assets/schemas/review.schema.json`. The orchestrating agent normalises semantically equivalent concerns to the same stable `issue_key`; the script does not infer whether two prose findings mean the same thing.

```sh
python3 scripts/arsenal.py add-review \
  --workspace acme.arsenal.json \
  --track offer \
  --phase market \
  --input market-reviews.json
```

### 4. Gate

```sh
python3 scripts/arsenal.py gate \
  --workspace acme.arsenal.json \
  --track offer \
  --phase market
```

Exit `0` means the phase can be approved. Exit `1` means one or more unaccepted critical issues remain. Two distinct reviewers using the same `issue_key` make that issue critical; an explicitly blocking issue is also critical.

### 5. Resolve or explicitly accept risk

Fix the phase and run the review again. If the user chooses to proceed after the allowed revision cycles, record that choice:

```sh
python3 scripts/arsenal.py accept-risk \
  --workspace acme.arsenal.json \
  --track offer \
  --phase market \
  --issue-key market-too-broad \
  --reason "User will validate the narrower segment during the pilot" \
  --confirmed-by user
```

Never invent acceptance on the user's behalf.

### 6. Approve and render

```sh
python3 scripts/arsenal.py approve \
  --workspace acme.arsenal.json \
  --track offer \
  --phase market

python3 scripts/arsenal.py render \
  --workspace acme.arsenal.json \
  --surface all
```

Rendering writes the three HTML reports plus generated offer, research and decision Markdown views next to the workspace file.

### 7. Validate before handoff

```sh
python3 scripts/arsenal.py validate --workspace acme.arsenal.json
python3 scripts/arsenal.py status --workspace acme.arsenal.json
```

An approved phase whose recorded upstream revisions no longer match current state is invalid. Fix the state rather than editing the report.

## Ownership boundary

The script may calculate or enforce:

- phase order and revision numbers;
- distinct-reviewer consensus by normalised issue key;
- approval and accepted-risk state;
- stale downstream state;
- currency and percentage formatting;
- safe HTML escaping;
- atomic writes and deterministic report rendering.

The script must not decide:

- which market is attractive;
- whether evidence is credible;
- whether two differently worded concerns are the same issue;
- what an offer, guarantee, lead magnet or message should be;
- whether copy is persuasive or honest.

Those remain agent and user decisions.

## References

- `references/state-contract.md` — canonical workspace and event semantics.
- `references/phase-contract.md` — phase payload and review normalisation rules.
- `references/migration.md` — importing or continuing legacy Markdown workshops.
- `assets/schemas/` — machine-readable contracts.
- `assets/design/` and `assets/templates/` — shared Growth Arsenal report system.
