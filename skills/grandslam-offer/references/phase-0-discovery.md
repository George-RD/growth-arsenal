# Phase 0: Discovery & Research Foundation

## Phase 0: Discovery
- Business: [description]
- Market: [definition]
- Personas: [names and one-line summaries]


## Research Brief — The Living Document

The Research Brief is not a one-time dump. It's a structured working file that gets written to and read from throughout the entire workshop. You search for data when you need it, store it where it belongs, and reference it when making decisions.

File: `{project-name}-research.md`

Organized by what each phase actually needs. When you hit a phase, check the brief. If data's missing, research. If it's there, use it.

### Template Structure

Write this template to `{project-name}-research.md` at the start of Phase 0, then fill sections as research comes in:

```text
# Research Brief — [Business Name]
Updated: [date]


## Market Identity
- Core market (Health / Wealth / Relationships): ___
- Niche definition: ___
- Audience specifics: ___


## Customer Personas
[Evolving profiles — updated after each phase with new context]
```

### Research Intake Protocol

Before running any web searches in Phase 0, ask the user:

> *"Do you have existing research on this market? This could include competitor analysis, customer interviews, market data, forum threads, or notes. If yes, share it and I'll organize it into our Research Brief, then identify gaps. If not, I'll build it from scratch with targeted web searches."*

**If user provides research:** Parse into Research Brief sections, run gap analysis, search only for missing data.

**When there's no existing research:** Proceed with comprehensive web searches, filling the Research Brief as data comes in.

**If partial:** Fill what the user provides, gap-analyze, search for what's missing.

### Gap Analysis Protocol

Before EACH phase, check the Research Brief against what that phase needs. Display the results:

```text
=== Gap Analysis: Phase [X] ===
[OK]  Item — sufficient data in Research Brief
[GAP] Item — missing or insufficient, need to research

Action: Filling [GAP] items before proceeding...
```

**Phase requirements:**

| Phase | Required Data |
|-------|--------------|
| 1 | Pain severity evidence, purchasing power signals, targeting specificity, market growth |
| 2 | Competitor pricing, customer income/spending patterns, value perception benchmarks |
| 3 | Dream outcome language (customer quotes), proof elements, speed benchmarks, effort friction, competitor promises |
| 4 | Competitor offer stacks (top 3), delivery model norms, operational costs, switching costs |
| 5 | Bonus anchoring values, scarcity precedents, guarantee norms, guarantee naming landscape, prospect fear mapping, competitor guarantee comparison, offer naming landscape |

If any item shows `[GAP]`, run targeted web searches or prompt the user before proceeding.

### Iterative Research Triggers

| Phase | Trigger | Research Action |
|-------|---------|----------------|
| Phase 1 | Market scores <25/40 on any indicator | Search for higher-pain niches within same market |
| Phase 2 | No data on what market pays for similar solutions | Search competitor pricing and offer structures |
| Phase 3 | Proof elements empty in research brief | Search for case studies, testimonials, credentialing options |
| Phase 4 | Competitor stacks unknown | Search top 3 competitor offer details, delivery models |
| Phase 5 | Bonus anchoring values missing | Search standalone product prices for each bonus category |
| Any | Adversarial agent flags knowledge gap | Pause and research before revising |

### Persona Evolution Protocol

Personas are not static. After each phase, update persona profiles in the Research Brief with cumulative context from that phase's review.

```text
Phase 0: Base profile (demographics, pain points, current situation)
Phase 1: + "My pain score is X/10, here's why" (from market review)
Phase 2: + "At $Y, I'd buy / wouldn't buy because Z" (from pricing review)
Phase 3: + "The value equation scores feel X to me" (from value review)
Phase 4: + "In the stack, I value A most, would cut B" (from offer review)
Phase 5: + "With this guarantee + name, I'd buy / final hesitation is X"
```

This cumulative context gets passed to persona agents in each subsequent phase. They receive the entire history of how they've reacted to prior decisions — not just the base persona. This makes feedback progressively more informed and specific.

**Update personas in the Research Brief after each phase review. Do not skip this.**

---


## Phase 0: Discovery & Research Foundation

### Step 1: Get the Business Idea

Open with:

> *"I'm your Grand Slam Offer Architect. I'll walk you through building an offer so good people feel stupid saying no — and I have a team of adversarial agents who'll tear apart every weak point before we're done.*
>
> *To start: What's your business idea, and who is your target audience? Be specific — what do you sell, to whom, and what problem does it solve?"*

### Step 2: Research Intake

Once you have the idea, run the **Research Intake Protocol** (see above). Ask if they have existing research before searching.

### Step 3: Market Research

After processing any user-provided research, run gap-targeted web searches. Default searches if no user research provided:

1. **Market size & growth**: `"[market] market size growth trends [current year]"`
2. **Top competitors**: `"best [product/service type] for [audience] reviews"`
3. **Customer pain points**: `"[audience] [problem] frustrated reddit OR forum OR review"`
4. **Pricing benchmarks**: `"[product/service type] pricing [audience segment]"`
5. **Buying patterns**: `"[audience] buying behavior [market] survey OR report"`

Write all findings into the Research Brief. Synthesize into a brief market snapshot and present to the user.

### Step 4: Build Customer Personas

From research, construct 2-3 **distinct** customer personas. Each must include:

| Field | Description |
|-------|-------------|
| **Name & Snapshot** | Fictional name + age, role, situation |
| **Specific Pain Points** | From real research — not generic |
| **Current Solutions** | What they use now and why it fails them |
| **Budget** | Realistic spending power for this solution |
| **Objection Patterns** | Top 3 reasons they'd say "no" |
| **Dream Outcome** | What they actually want, in their own words |
| **Where They Hang Out** | Specific platforms, communities, events |
| **Buying Psychology** | What triggers their purchase decisions |

Write personas to the Research Brief. **Present to user for validation.** Adjust based on their real-world customer knowledge — they know their market better than web research does.

### Step 5: Confirm Team Roster

Once personas are validated, confirm:

> *"Your adversarial review team for this workshop:*
>
> - *Skeptical Marketer — will challenge your positioning and differentiation*
> - *Business Strategist — will stress-test your economics and scalability*
> - *[Persona 1 Name] — your [segment 1] customer*
> - *[Persona 2 Name] — your [segment 2] customer*
> - *[Persona 3 Name] — your [segment 3] customer (if applicable)*
>
> *This team will attack your offer at every phase. Ready for Phase 1?"*

### Phase 0 Output

1. Write initial `{project-name}-offer.md` with Phase 0 section
2. Generate `{project-name}-research-dashboard.html` using the `templates/research-dashboard.md` spec, populated with Research Brief data. Open in browser: `open {project-name}-research-dashboard.html`
3. Generate `{project-name}-workshop-progress.html` using the `templates/workshop-progress.md` spec. Open in browser.

---

