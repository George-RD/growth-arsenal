# Workspace State Contract

## Source of truth

`{project}.arsenal.json` is canonical. Generated Markdown and HTML are projections and must not be parsed back into state.

The workspace records:

- project locale, currency, spelling and timezone;
- track and phase status;
- revisioned phase data;
- the upstream revisions each approved phase consumed;
- independent structured reviews;
- explicit accepted risks;
- research records and provenance;
- an append-only event trail;
- generated output paths.

## Phase status

- `not_started`: no phase payload has been applied.
- `draft`: current phase data exists but has not entered review.
- `in_review`: at least one structured review has been attached.
- `approved`: the gate has no unaccepted critical issue and approval was recorded.
- `stale`: an upstream dependency changed after this phase was produced.

Stale state is preserved for audit and comparison. It is not silently deleted and does not count as approved.

## Revision semantics

Applying a phase increments its own revision and clears its old reviews. All later phases with work are marked stale. Approval stores the current upstream revision map.

`validate` fails when an approved phase's stored upstream revisions differ from current revisions. This catches manual or external state edits that bypassed `apply`.

## Approval gate

`gate` reports eligibility for the next approval transition, not whether the phase was approved in the past. Its existing review fields remain available. The result also includes:

- `review_gate_passed`: the recorded reviews meet the independent-reviewer requirement and have no unaccepted critical issues. This does not check lifecycle readiness.
- `blockers`: a deterministic list of objects with a `code` and an actionable `message`.
- `can_approve`: true only when `blockers` is empty.

Blockers are returned in the following order when applicable. A stale marker takes precedence over the other status blockers.

| Code | Required action |
| --- | --- |
| `predecessors-unapproved` | Complete prerequisite approvals in dependency order. |
| `untouched-phase` | Apply a phase payload before review. |
| `stale-phase` | Re-apply current content and obtain fresh reviews. |
| `already-approved` | Continue the workflow, or re-apply deliberately changed content. |
| `phase-not-in-review` | Submit structured reviews for the applied phase. |
| `upstream-revision-drift` | Re-apply content against current approved inputs and re-review. |
| `phase-data-drift` | Re-apply the edited data through the CLI and re-review. |
| `reviewers-required` | Obtain reviews from at least two distinct reviewers. |
| `critical-issues` | Resolve the findings, or record explicit user acceptance for this revision. |

The gate exits `0` when ready and `1` when blocked, without writing the workspace. An unknown phase, missing workspace or JSON syntax error exits `2`. `approve` evaluates the same gate on the state it loads; a blocked approval exits `2`, returns the first blocker message and leaves the workspace unchanged. A gate result is not a reservation against later state changes.

Already-approved phases return `can_approve: false`; use their recorded status and `validate` to assess existing approvals. Report rendering continues to use the recorded status and review findings, not permission to approve again.

After an upstream change, downstream review history remains inspectable and `review_gate_passed` may still be true. Approving the new upstream revision alone does not revive that downstream work. Re-apply each stale phase in dependency order, obtain fresh reviews, then approve it. Do not clear stale markers or edit hashes to bypass this flow.

## Accepted risks

An accepted risk is a user decision, not a reviewer conclusion. It requires:

- track, phase and phase revision;
- exact `issue_key`;
- reason;
- who confirmed it;
- timestamp.

Acceptance removes that issue from the blocking set for the recorded revision but does not erase the finding from reports or state. Re-applying the phase requires fresh review and, where necessary, fresh user acceptance. Risk acceptance cannot bypass lifecycle blockers.

## Events

Events are append-only operational records. They do not replace phase data. Current event types include:

- `workspace.initialised`
- `phase.applied`
- `review.added`
- `risk.accepted`
- `phase.approved`

Future event types may be added without changing existing meaning.

## Rendering

The renderer is deterministic for a given workspace and asset version, except generated timestamps. It:

- escapes all user and agent text;
- allows only `http://` and `https://` source links;
- does not load network assets;
- inlines the shared CSS and JavaScript;
- produces printable, progressively enhanced HTML;
- never invents missing commercial facts.
