# Legacy Workshop Migration

Existing projects may have only `{project}-research.md`, `{project}-offer.md` and generated HTML.

## Safe migration

1. Preserve the legacy files unchanged.
2. Initialise a workspace beside them.
3. Read one completed phase at a time.
4. Write a structured phase payload using only explicit information from the legacy files.
5. Apply and approve the phase in sequence.
6. Record unknown fields as missing. Do not infer them to make the report complete.
7. Render new reports into a separate directory for comparison.
8. Replace legacy generated HTML only after the user approves the migrated state.

## What cannot be recovered reliably

- which revision of an upstream decision a later phase used;
- independent review outputs if only a synthesis was saved;
- accepted risks that were discussed but not logged;
- source provenance omitted from the research brief.

Mark those as migration limitations. Do not manufacture history.

## Compatibility mode

The old Markdown files remain useful as readable exports. After migration, generate them from the workspace so they stop diverging from the canonical state.
