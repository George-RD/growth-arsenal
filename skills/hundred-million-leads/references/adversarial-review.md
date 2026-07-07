## Adversarial Review Protocol

### How to Run Reviews

At each phase checkpoint:

1. **Collect the phase output** — everything the user has decided/created
2. **Spawn parallel Task agents** using `subagent_type: "general-purpose"` with `model: "sonnet"` for speed
3. Each agent gets: their **persona definition** + the **phase output** + the **specific review prompt**
4. Agents return independently — they do NOT see each other's reviews
5. **Synthesize**: Present unified feedback, organized by severity:
   - **Critical** (2+ agents flagged): Must fix before proceeding
   - **Warning** (1 agent flagged): Should consider
   - **Suggestion** (improvement ideas): Optional
6. User addresses critical issues. Re-run review if needed.
7. Move to next phase only when no critical issues remain.

### Customer Persona Agents — Cumulative Context

Persona agents receive **cumulative context** as the workshop progresses:

- Phase 1: Offer details + persona profile
- Phase 2: + Lead magnet chosen
- Phase 3: + Channel strategy + ALL scripts/ads (they receive these AS A PROSPECT)
- Phase 4: + Referral scripts (they receive these FROM A FRIEND)
- Phase 5: + Frequency/cadence plan (they experience REPEATED EXPOSURE)

### When to Add Extra Research

If an adversarial review reveals a knowledge gap (e.g., "What's the current CPL for Facebook ads in this niche?" or "What are competitors' lead magnets?"), pause and run WebSearch before continuing.

---

