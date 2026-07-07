# Phase 1: The Starving Crowd (Market Selection)

## Phase 1: Starving Crowd
- Market scores: Pain [X], Purchasing Power [X], Targeting [X], Growth [X] = [total]/40
- Core market: [Health/Wealth/Relationships]
- Niche: [final niche definition]


## Starving Crowd Indicators (Phase 1)
- Pain severity evidence: [sources, quotes, data]
- Purchasing power signals: [income data, spending patterns, competitor pricing]
- Targeting specificity: [where they congregate — specific groups, lists, platforms]
- Market growth signals: [trend data, search volume, industry reports]
- Score: __/40


## Phase 1: The Starving Crowd (Market Selection)

**Gap check:** Run gap analysis for Phase 1 requirements. Fill gaps before proceeding.

### The Framework

A Grand Slam Offer starts with a market that's STARVING for a solution. Rate each indicator 1-10:

| Indicator | Question | Red Flag | Score |
|-----------|----------|----------|-------|
| **Massive Pain** | Do they desperately need this? | "Nice to have" language | __/10 |
| **Purchasing Power** | Can they afford premium pricing? | Targeting broke markets | __/10 |
| **Easy to Target** | Can you find them in specific groups/lists? | "Everyone" is the target | __/10 |
| **Growing Market** | Is the market expanding? | Declining or saturated | __/10 |

**Scoring Gate:**

- **25+/40**: Green light — proceed to pricing
- **20-24/40**: Yellow — niche down further or pivot one dimension
- **Under 20/40**: Red — market won't support a Grand Slam Offer. Suggest 3 pivots to a "starving crowd" segment with higher pain or purchasing power

### The 3 Core Markets

Everything maps to **Health**, **Wealth**, or **Relationships**. Force the user to identify which one. If they can't, their market is too vague.

### Niche Down Protocol

If the market is too broad, force niching until all 4 indicators are strong:

```text
Generic → Specific demographic → Specific pain → Specific situation
```

Example: "Weight loss" (commodity) → "Post-pregnancy body recovery for first-time moms over 30 who've tried and failed with diets" (Grand Slam territory)

### Adversarial Checkpoint

Spawn all agents in **parallel** with these prompts (fill in `[BRACKETS]` with actual content):

**Skeptical Marketer:**
> Review this market selection: [MARKET_DEFINITION]. Attack it ruthlessly. Is the pain real or manufactured? How many competitors already serve this exact niche? Is this a vitamin or painkiller? What's the #1 reason this market choice will fail? What market would be 10x better? Score the market 1-10.

**Business Strategist:**
> Review this market selection: [MARKET_DEFINITION]. Analysis needed: What's the realistic TAM for this niche? What does customer acquisition cost in this market? What's the expected LTV? Is this scalable or does it cap at $[X]/year? What's the operational complexity of serving this niche? Score market economics 1-10.

**Customer Persona(s):**
> You are [FULL_PERSONA_DEFINITION]. Someone is building a business targeting people like you in [MARKET_DEFINITION]. React honestly: Do you actually have this problem? Rate the pain 1-10. What would you do about it? Would you pay money to solve it? What have you already tried? What did those solutions get wrong?

**Synthesis rule:** If 2+ agents flag the same issue, it's a **MUST-FIX** before proceeding. Present the consensus issues and force revision. Max 2 revision cycles.

### Phase 1 Output

1. Update `{project-name}-offer.md` with Phase 1 section
2. Update Research Brief: Starving Crowd scores + persona evolution
3. Regenerate `{project-name}-workshop-progress.html`. Open in browser.
4. **Phase gate:** *"Phase 1 complete. [Summary of market selection + scores]. Ready for Phase 2: Pricing?"*

---

