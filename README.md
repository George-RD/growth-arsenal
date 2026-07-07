<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:16213e&height=180&section=header&text=growth-arsenal&fontSize=42&fontColor=e0e0e0&animation=fadeIn&fontAlignY=35&desc=Business%20growth%20workshops%20run%20inside%20your%20AI%20coding%20agent&descSize=15&descAlignY=55">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=180&section=header&text=growth-arsenal&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Business%20growth%20workshops%20run%20inside%20your%20AI%20coding%20agent&descSize=15&descAlignY=55" width="100%" alt="growth-arsenal header">
</picture>

<p align="center">
  <img src="https://img.shields.io/badge/skills-3-blue?style=flat-square" alt="Skills">
  <img src="https://img.shields.io/badge/Claude_Code-compatible-green?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="MIT License">
</p>

<p align="center">
  <b><a href="https://george-rd.github.io/growth-arsenal/">See the live site →</a></b>
</p>

## Build offers and lead gen systems that survive contact with real customers

Three Hormozi-style workshops, run by adversarial AI agent teams. They stress-test every offer, lead magnet, and script before you ship it, not after.

---

## What's inside

| Skill | What it does |
|---|---|
| **grandslam-offer** | Turns a vague idea into a priced, named offer with a real guarantee. A skeptical marketer, a margin-obsessed strategist, and simulated customers tear it apart first. Based on Alex Hormozi's *$100M Offers*. |
| **hundred-million-leads** | Builds your lead magnets, picks your Core Four channels, writes your outreach scripts, and lays out a Rule of 100 plan. Companion to the offer workshop. Based on Alex Hormozi's *$100M Leads*. |
| **business-copy-style** | Checks every customer-facing line against plain-language and de-AI rules before it ships. Both workshops call it automatically. Nothing sounds like a robot wrote it. |

Each workshop saves its work to markdown files as it runs. That way your progress survives a restart and hands off cleanly to the next skill.

---

## Install

Pick the path for your harness. All commands assume you're in a terminal.

| Harness | Command |
|---|---|
| Claude Code (plugin) | `/plugin marketplace add George-RD/growth-arsenal` then `/plugin install growth-arsenal@growth-arsenal` |
| Claude Code (skills only) | `git clone https://github.com/George-RD/growth-arsenal && cd growth-arsenal && ./install.sh claude` |
| Oh My Pi (OMP) | Same clone, then `./install.sh omp` (or `./install.sh claude` — OMP inherits `~/.claude/skills/` automatically) |
| Codex | Same clone, then `./install.sh codex` |
| opencode | Same clone, then `./install.sh opencode` |
| agents.md-style harnesses | Same clone, then `./install.sh agents` |

Updates: `git pull` in the cloned repo — the install is a symlink, so changes show up immediately. Windows: symlinks aren't reliable, copy the `skills/<name>` directories into your harness's skills folder instead.

---

## Quick start

Once installed, just tell your agent what you need:

- *"I run a small bookkeeping firm, help me build an offer I can charge 5x for"* → grandslam-offer takes over.
- *"I sell an online course for new parents, help me build a lead generation system"* → hundred-million-leads takes over.
- *"Rewrite this landing page copy so it doesn't sound like AI wrote it"* → business-copy-style takes over.

The agent teams push back on weak ideas. They ask hard questions about pricing, guarantees, channels, and messaging. That's the point. The stress test happens before you go to market, not after.

---

## FAQ

**Isn't this just a chatbot with extra steps?**
No. A plain chat call skips the adversarial review. Each phase gets torn apart by a skeptical marketer, a strategist, and simulated customers before you move on.

**Does this replace talking to real customers?**
No. It kills the obvious weak spots first, cheaply, before real buyers see them. You still have to talk to real people. They just meet a stronger offer.

**Do I need to know the Hormozi books first?**
No. The workshop asks the questions and builds the offer with you, phase by phase.

**What if I only want the lead-gen piece?**
Each skill runs on its own. The leads workshop suggests the offer workshop first if you skipped it. It won't block you either way.

**Will the copy sound like AI wrote it?**
Every customer-facing line runs through business-copy-style first. Plain language. No AI tells.

---

## Contributing

Found a bug? Got an idea? [Open an issue](https://github.com/George-RD/growth-arsenal/issues). PRs welcome — see `CLAUDE.md` for repo conventions.

## Credits

These workshops implement methodologies from Alex Hormozi's *$100M Offers* and *$100M Leads*.

## License

MIT — see `LICENSE`.

<picture>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:16213e&height=100&section=footer" width="100%" alt="footer">
</picture>
