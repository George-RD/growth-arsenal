<picture>
  <img src="docs/readme-header.svg" width="100%" alt="growth-arsenal. Your offer should fail here first." />
</picture>

<p align="center">
  <a href="https://george-rd.github.io/growth-arsenal/"><strong>See how it works</strong></a>
  ·
  <a href="#install"><strong>Install</strong></a>
  ·
  <a href="https://ko-fi.com/george_builds"><strong>Support the project</strong></a>
</p>

<p align="center">
  <a href="https://skills.sh/George-RD/growth-arsenal"><img src="https://skills.sh/b/George-RD/growth-arsenal" alt="skills.sh installs" /></a>
</p>

# growth-arsenal

Business growth workshops plus a composable writing stack for AI agents.

The writing stack separates the work that often gets collapsed into one prompt: decide what the text means, adapt it to the reader, then audit the finished copy. The workshop skills use the same idea for offers and lead generation: research and decisions first, delivery second.

## Choose where to start

| You need to | Start with |
|---|---|
| Build any human-readable prose from source material | [`writing-core`](skills/writing-core/) |
| Write for managers, stakeholders or presentations | [`executive-writing`](skills/executive-writing/) after `writing-core` |
| Build an investment or pilot business case | [`business-case`](skills/business-case/) before prose |
| Derive a durable voice profile from approved examples | [`voice-calibration`](skills/voice-calibration/) |
| Review finished customer-facing copy for slop and clarity | [`business-copy-style`](skills/business-copy-style/) |
| Price and package an idea | [`grandslam-offer`](skills/grandslam-offer/) |
| Build a lead plan you can use | [`hundred-million-leads`](skills/hundred-million-leads/) |

The normal prose path is:

```text
evidence / reasoning
      ↓
writing-core
      ↓
genre skill
      ↓
business-copy-style when needed
      ↓
render / publish
```

`business-case` sits before that path because the economic model should exist before the deck or memo.

## Install

### Skills CLI

```bash
npx skills add George-RD/growth-arsenal
```

This is the standard [skills.sh](https://skills.sh/) install path. It discovers the skills in this repository and lets you choose the target agent and install scope.

The simplest all-in option is:

```bash
npx skills add George-RD/growth-arsenal --skill '*' -a codex -y
```

Selective installs are also supported:

```bash
npx skills add George-RD/growth-arsenal --skill writing-core
npx skills add George-RD/growth-arsenal --skill executive-writing
npx skills add George-RD/growth-arsenal --skill business-case
npx skills add George-RD/growth-arsenal --skill voice-calibration
npx skills add George-RD/growth-arsenal --skill business-copy-style
```

Cross-skill composition is by skill name. A workflow that needs a missing companion should resolve it at the point of need rather than reimplementing the other skill's rules.

Add `-g` for a global install instead of the default project install.

### Claude Code plugin

```text
/plugin marketplace add George-RD/growth-arsenal
/plugin install growth-arsenal@growth-arsenal
```

### From source

```bash
git clone https://github.com/George-RD/growth-arsenal
cd growth-arsenal
./install.sh codex   # claude | omp | opencode | agents
```

The source installer is a legacy whole-repository compatibility path and uses symlinks, so `git pull` updates the skills in place. The Skills CLI is the preferred cross-platform install path.

## Writing approach

`writing-core` borrows useful controlled-language principles without forcing controlled English on every genre: one main thought per sentence, stable terminology, direct syntax and common grammatical vocabulary around necessary technical terms.

It also adds a semantic intermediate step: a factual kernel. The agent first records what each material claim means and how certain it is. Only then does another skill decide how much context, explanation or personality belongs in the final surface.

`voice-calibration` can learn from approved user writing and edits. It separates stable preferences from genre-specific variants so chat style does not get copied blindly into an executive deck.

`business-case` treats incomplete data as an uncertainty problem rather than a reason to avoid a recommendation. It uses labelled assumptions, low/base/high scenarios, break-even and switching values, while preventing assumptions from being chosen merely to make the case positive.

## Start with a plain request

```text
Turn these rough research notes into a wiki page. Keep the technical meaning exact.
```

```text
Build the business case from these messy operational figures, then turn it into an executive deck.
```

```text
These are my edits to three AI drafts. Work out what I consistently changed and update my voice guidance.
```

```text
I run a small bookkeeping firm. Help me build an offer I can charge five times more for.
```

## Limits

The writing skills improve process and consistency; they do not prove authorship or make AI detection reliable. Real examples, subject knowledge and user judgement remain stronger evidence than any style detector.

The growth workshops do not replace talking to real customers. Dynamic personas catch obvious gaps, but they are not proof of demand.

## Contributing

Found a bug or a weak part of the workflow? [Open an issue](https://github.com/George-RD/growth-arsenal/issues). Pull requests are welcome. See `CLAUDE.md` for repository conventions.

## Licence

MIT. See `LICENSE`.
