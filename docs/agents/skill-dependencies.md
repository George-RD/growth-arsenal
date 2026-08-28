# Companion skill dependencies

Growth Arsenal composes skills by name. Until the standard Skills CLI supports native dependency resolution for the relationships we need, use the smallest possible instruction-level shim.

## Runtime contract

Check a companion skill only at the first point where its capability is needed, not at session startup.

1. Resolve the companion skill by name using the host's normal skill discovery.
2. If it is present, use it normally.
3. If a **quality dependency** is missing, tell the user what quality gate or capability will be unavailable, show the standard install command, and ask whether to install it or continue degraded.
4. If the user continues degraded, do not claim the missing quality gate passed. Mark the affected result as degraded or unverified.
5. If a **hard dependency** is missing, stop only the path that needs it, show the standard install command, and resume after it is available.

Do not duplicate a companion skill's full method as a fallback. A fallback may contain only the minimum safety rules needed to avoid misleading or invalid output.

## Current copy dependency

`business-copy-style` is a quality dependency for customer-facing copy produced by Growth Arsenal workflows. While it remains in this repository, the standard install command is:

```bash
npx skills add George-RD/growth-arsenal --skill business-copy-style
```

Do not extract it into a separate repository solely to simulate package dependencies. Revisit that boundary when native cross-repository dependency support exists, or when independent reuse creates a concrete release-management benefit.

## Upstream watchpoint

Before changing dependency behavior, check the current `vercel-labs/skills` documentation, changelog and these upstream proposals:

- https://github.com/vercel-labs/skills/issues/515 — skill `depends_on`
- https://github.com/vercel-labs/skills/issues/860 — skill `depends`
- https://github.com/vercel-labs/skills/issues/2060 — composable/nested packs

If official dependency support has shipped and covers the required relationship, adopt the official mechanism and remove the corresponding dependency shim in the same change.

Do not invent or pre-adopt proposed frontmatter fields. Do not build a custom dependency resolver, recursive `skills-lock.json` installer, post-install hook, or repository-specific package manager.

`skills-lock.json` is useful for project reproducibility and restore. It is not the runtime dependency graph. Skills.sh packs may bundle skills, but they are not the per-skill dependency contract.
