# growth-arsenal

Claude Code plugin and cross-agent skill pack: business growth workshops with adversarial agent teams.

## Structure

| Directory | Skill | Description |
|-----------|-------|-------------|
| `skills/grandslam-offer/` | grandslam-offer | $100M Offers workshop with adversarial agent teams |
| `skills/hundred-million-leads/` | hundred-million-leads | $100M Leads workshop with adversarial agent teams |
| `skills/business-copy-style/` | business-copy-style | Plain-language + de-AI copy rules, consumed by both workshops |
| `skills/growth-arsenal-workspace/` | growth-arsenal-workspace | Shared deterministic state, gates and report rendering |
| `skills/plugin-feedback/` | plugin-feedback | End-of-workshop feedback and wrap-up support |

## Key Files

- `.claude-plugin/marketplace.json` — this repo's own Claude Code plugin registry
- `.claude-plugin/plugin.json` — plugin manifest and explicit skill grouping used by compatible skill tooling
- `install.sh` — legacy POSIX symlink installer for source checkouts (`omp`, `claude`, `codex`, `opencode`, `agents`)
- `scripts/bump-version.sh` — keeps `plugin.json` and `marketplace.json` versions in sync (`--check` mode)

## Conventions

- **Skills CLI is the canonical cross-agent install path**: `npx skills add George-RD/growth-arsenal`. Do not add a repository-specific npm installer while the standard Skills CLI covers the requirement.
- **Skills one level deep**: every installable skill lives at `skills/<name>/SKILL.md`. Keep `name` and `description` frontmatter valid so the Skills CLI and agent harnesses can discover it.
- **The full pack is load-bearing**: `grandslam-offer` and `hundred-million-leads` resolve shared skills by name. A complete install must therefore include `growth-arsenal-workspace`, `business-copy-style` and `plugin-feedback` as well as the two workshops.
- **SKILL.md < 500 lines** (progressive disclosure). Per-phase deep content lives in `references/`, loaded on demand — never inline the whole workshop in the top-level file.
- **Deterministic output templates** live in `templates/`; SKILL.md instructs "copy the template, fill the brackets" rather than freeform generation, for repeatable output shape.
- **Copy-style wiring**: any copy-emitting instruction in a workshop skill (offer names, outreach scripts, ad copy, bonus/guarantee copy) must reference `business-copy-style` by skill name, not by path.
- **No build step** — this repo remains skills, templates, references and lightweight scripts. Distribution should not require publishing a second package.
- **Before release**: run `scripts/bump-version.sh --check`, and markdownlint if configured (`.markdownlint.json` disables MD013, MD024, MD029, MD033, MD036, MD060). CI also installs the full pack with a pinned Skills CLI release.
- **Eval workflow**: skills are measured, not just written. See `skills/<name>/evals/evals.json` for quality-eval prompts/assertions, and `skill://skill-creator` (or the vendored `~/.omp/agent/skills/skill-creator/` engine) for the with-skill-vs-baseline quality loop and the `run_loop.py` description-optimization loop.
- **Commits**: conventional commits — `feat(scope):`, `fix(scope):`, `chore(scope):`.

## Gotchas

- The Skills CLI defaults to a project install. Use `-g` for global installation and `--skill '*'` when the complete Growth Arsenal pack is required.
- Installing only `grandslam-offer` or `hundred-million-leads` is incomplete because they call sibling support skills by name. `business-copy-style` is safe to install standalone.
- `install.sh` remains a source-checkout compatibility path; its symlinks mean `git pull` propagates updates automatically.
- The `business-copy-style` skill has no path-relative links into the workshop skills' dirs — cross-skill references are by name only, since skill install order/location varies per harness.
