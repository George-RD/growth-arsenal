# Issue tracker: GitHub

Specs and implementation tickets for Growth Arsenal live in GitHub Issues in `George-RD/growth-arsenal`.

## Conventions

- Publish one spec as one GitHub issue.
- Publish each implementation slice as its own GitHub issue.
- Put `## Parent` in each implementation ticket with a reference to the spec issue.
- Put `## Blocked by` in every implementation ticket. Use `None (can start immediately)` or explicit issue references.
- Apply `ready-for-agent` when the repository has that label. If it is unavailable, include `Status: ready-for-agent` in the issue body instead; do not create label-management work just for this workflow.
- A future `/implement` session should choose the first open ticket whose blockers are closed, then implement only that ticket.
- PRs are implementation output, not a feature-request surface.

Use the available GitHub integration when the agent has one; otherwise use the `gh` CLI equivalents.

## When a skill says "publish to the issue tracker"

Create a GitHub issue in this repository.

## When a skill says "fetch the relevant ticket"

Read the full issue body and comments before acting.
