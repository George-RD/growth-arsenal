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

## Accepted risks

An accepted risk is a user decision, not a reviewer conclusion. It requires:

- track and phase;
- exact `issue_key`;
- reason;
- who confirmed it;
- timestamp.

Acceptance removes that issue from the blocking set but does not erase the finding from reports or state.

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
