# Matt Pocock engineering skills

Growth Arsenal vendors the small Matt Pocock engineering workflow needed for planning and implementation as ordinary project-local skills under `.agents/skills/`.

## Source

- Repository: `mattpocock/skills`
- Reviewed revision: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`
- Upstream license: MIT; preserved at `.agents/skills/LICENSE.mattpocock`

## Installed workflow

- `setup-matt-pocock-skills`
- `grill-with-docs`
- `grilling`
- `domain-modeling`
- `to-spec`
- `to-tickets`
- `implement`
- `tdd`
- `code-review`

The repo-specific setup is GitHub Issues plus one root `CONTEXT.md`. The installed skills are upstream workflow sources; `docs/agents/` is Growth Arsenal-owned configuration.

## Update rule

Do not silently track upstream `main`. When intentionally updating this workflow:

1. inspect the current upstream skill files and changelog;
2. compare the selected workflow against this pinned revision;
3. update only the installed subset, the preserved license if needed, and this revision record;
4. run Growth Arsenal's existing tests and a planning smoke check.

Add more Matt Pocock skills only when a Growth Arsenal workflow actually needs them. Avoid turning this repository into a mirror of the upstream skill collection.
