# growth-arsenal

Claude Code plugin and cross-agent skill pack: business growth workshops plus composable writing capabilities.

## Structure

| Directory | Skill | Description |
|-----------|-------|-------------|
| `skills/grandslam-offer/` | grandslam-offer | $100M Offers workshop with adversarial agent teams |
| `skills/hundred-million-leads/` | hundred-million-leads | $100M Leads workshop with adversarial agent teams |
| `skills/writing-core/` | writing-core | Proactive meaning-first prose generation used before genre and copy-review skills |
| `skills/executive-writing/` | executive-writing | Business, management and presentation delivery built on writing-core |
| `skills/business-case/` | business-case | Decision modelling with assumptions, scenarios, break-even and switching values before prose |
| `skills/voice-calibration/` | voice-calibration | Derives stable and genre-specific voice guidance from approved writing evidence |
| `skills/business-copy-style/` | business-copy-style | Plain-language + de-AI final copy review |
| `skills/growth-arsenal-workspace/` | growth-arsenal-workspace | Shared deterministic state, gates and report rendering |
| `skills/plugin-feedback/` | plugin-feedback | End-of-workshop feedback and wrap-up support |

## Key Files

- `.claude-plugin/marketplace.json` — this repo's own Claude Code plugin registry
- `.claude-plugin/plugin.json` — plugin manifest and explicit skill grouping used by compatible skill tooling
- `.agents/skills/` — project-local Matt Pocock engineering workflow; provenance is in `docs/agents/matt-pocock-skills.md`
- `docs/agents/` — repository configuration consumed by the engineering workflow
- `CONTEXT.md` — canonical Growth Arsenal domain vocabulary
- `install.sh` — legacy POSIX symlink installer for source checkouts (`omp`, `claude`, `codex`, `opencode`, `agents`)
- `scripts/bump-version.sh` — keeps `plugin.json` and `marketplace.json` versions in sync (`--check` mode)

## Agent skills

### Issue tracker

Specs and implementation tickets live in GitHub Issues for `George-RD/growth-arsenal`. See `docs/agents/issue-tracker.md`.

### Triage status

Implementation-ready work uses `ready-for-agent` when available, with an issue-body fallback. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo: read root `CONTEXT.md` and relevant ADRs under `docs/adr/`. See `docs/agents/domain.md`.

### Development workflow

For non-trivial planned work, use `/grill-with-docs`, then `/to-spec`, then `/to-tickets`. When the user delegates the design decisions, the grill may run in auto mode: resolve factual questions from the repo/upstream sources, choose the simplest recommended branch, record the resulting domain terms, and surface any material unresolved trade-off rather than blocking on routine questions.

A fresh implementation session should inspect open issues, choose the first open `ready-for-agent` ticket whose blockers are closed, and run `/implement` only on that ticket. `/implement` uses `/tdd` where appropriate and `/code-review` before completion.

### Companion skill dependencies

Before changing cross-skill dependency behavior, read `docs/agents/skill-dependencies.md` and check current official `vercel-labs/skills` support. Prefer a shipped native dependency mechanism when it covers the requirement. Do not build a parallel dependency resolver.

## Conventions

- **Skills CLI is the canonical cross-agent install path**: `npx skills add George-RD/growth-arsenal`. Do not add a repository-specific npm installer while the standard Skills CLI covers the requirement.
- **Skills one level deep**: every installable skill lives at `skills/<name>/SKILL.md`. Keep `name` and `description` frontmatter valid so the Skills CLI and agent harnesses can discover it.
- **Selective installs are supported**: the complete pack is the simplest all-in option, not a correctness requirement.
- **Writing stack is composable**: workflow skills that generate human-readable prose should resolve `writing-core` at the first generation step. Add a genre skill such as `executive-writing` when the surface needs it. Run `business-copy-style` after useful prose exists when the copy needs final de-slop or customer-facing review. `business-case` owns the decision model before any business-case deck or memo is written. `voice-calibration` updates a profile; it does not write the deliverable.
- **Meaning and delivery are separate**: do not make the presentation, landing page or report the place where the underlying reasoning is invented. Build the factual/decision model first, then render it for the audience.
- **No universal readability gate**: simplify unnecessary structure and formal vocabulary, but preserve precise technical terms. Genre workflows choose the lint threshold when they use deterministic copy metrics.
- **SKILL.md < 500 lines** (progressive disclosure). Per-phase deep content lives in `references/`, loaded on demand — never inline the whole workshop in the top-level file.
- **Deterministic output templates** live in `templates/`; SKILL.md instructs "copy the template, fill the brackets" rather than freeform generation, for repeatable output shape.
- **Copy-style wiring**: customer-facing copy should be generated through the appropriate writing skill before `business-copy-style` reviews it. The review skill should not become the default first-draft author inside a larger workflow.
- **No build step** — this repo remains skills, templates, references and lightweight scripts. Distribution should not require publishing a second package.
- **Before release**: run `scripts/bump-version.sh --check`, and markdownlint if configured (`.markdownlint.json` disables MD013, MD024, MD029, MD033, MD036, MD060). CI verifies both the complete pack and supported selective Skills CLI installs with a pinned release.
- **Eval workflow**: skills are measured, not just written. See `skills/<name>/evals/evals.json` for quality-eval prompts/assertions, and `skill://skill-creator` (or the vendored `~/.omp/agent/skills/skill-creator/` engine) for the with-skill-vs-baseline quality loop and the `run_loop.py` description-optimization loop.
- **Matt workflow changes are intentional**: the installed subset and reviewed upstream revision live in `docs/agents/matt-pocock-skills.md`. Do not silently expand or auto-update the vendored workflow.
- **Commits**: conventional commits — `feat(scope):`, `fix(scope):`, `chore(scope):`.

## Gotchas

- The Skills CLI defaults to a project install. Use `-g` for global installation and `--skill '*'` for the simplest complete-pack install.
- Installing only one writing capability is supported. Cross-skill composition is instruction-level until the Skills CLI provides a native dependency mechanism that covers this use case.
- `business-copy-style` remains usable standalone, but larger workflows should treat it as a critic after generation rather than as the semantic author.
- Do not turn companion negotiation into recursive `skills-lock.json` behavior or a custom resolver. The dependency watchpoint in `docs/agents/skill-dependencies.md` is the authority for replacing the shim with native Skills CLI support.
- `install.sh` remains a source-checkout compatibility path; its symlinks mean `git pull` propagates updates automatically.
- Skills should not use path-relative links into another skill's directory; cross-skill references are by name only, since skill install order/location varies per harness.
