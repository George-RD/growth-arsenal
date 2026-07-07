# growth-arsenal

Claude Code plugin (and OMP/codex/opencode/agents.md-compatible skill pack): business growth workshops with adversarial agent teams.

## Structure

| Directory | Skill | Description |
|-----------|-------|-------------|
| `skills/grandslam-offer/` | grandslam-offer | $100M Offers workshop with adversarial agent teams |
| `skills/hundred-million-leads/` | hundred-million-leads | $100M Leads workshop with adversarial agent teams |
| `skills/business-copy-style/` | business-copy-style | Plain-language + de-AI copy rules, consumed by both workshops |

## Key Files

- `.claude-plugin/marketplace.json` — this repo's own plugin registry (single root-plugin entry)
- `.claude-plugin/plugin.json` — plugin manifest
- `install.sh` — POSIX `sh` symlink installer for non-plugin harnesses (`omp`, `claude`, `codex`, `opencode`, `agents`)
- `scripts/bump-version.sh` — keeps `plugin.json` and `marketplace.json` versions in sync (`--check` mode)

## Conventions

- **Skills one level deep**: every skill lives at `skills/<name>/SKILL.md` — no nesting. This satisfies both Claude Code plugin auto-discovery and the OMP/other-harness one-level-deep rule.
- **SKILL.md < 500 lines** (progressive disclosure). Per-phase deep content lives in `references/`, loaded on demand — never inline the whole workshop in the top-level file.
- **Deterministic output templates** live in `templates/`; SKILL.md instructs "copy the template, fill the brackets" rather than freeform generation, for repeatable output shape.
- **Copy-style wiring**: any copy-emitting instruction in a workshop skill (offer names, outreach scripts, ad copy, bonus/guarantee copy) must reference `business-copy-style` by skill name, not by path.
- **No build step** — this repo is pure Markdown (skills, templates, references) plus POSIX shell scripts.
- **Before release**: run `scripts/bump-version.sh --check`, and markdownlint if configured (`.markdownlint.json` disables MD013, MD024, MD029, MD033, MD036, MD060).
- **Eval workflow**: skills are measured, not just written. See `skills/<name>/evals/evals.json` for quality-eval prompts/assertions, and `skill://skill-creator` (or the vendored `~/.omp/agent/skills/skill-creator/` engine) for the with-skill-vs-baseline quality loop and the `run_loop.py` description-optimization loop.
- **Commits**: conventional commits — `feat(scope):`, `fix(scope):`, `chore(scope):`.

## Gotchas

- `install.sh` symlinks skills into a target harness's user skills root; `git pull` in this repo propagates updates automatically to every installed target. Windows users must copy the `skills/<name>` dirs manually instead (no reliable native symlink support).
- The `business-copy-style` skill has no path-relative links into the workshop skills' dirs — cross-skill references are by name only, since skill install order/location varies per harness.
