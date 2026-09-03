# Factual kernel

Use this reference when the source is technical, uncertain, long or contradictory.

## Purpose

The kernel is a semantic intermediate representation. It separates **what the text means** from **how the text sounds** so later prose does not inherit a polished but weak frame.

Write fragments or terse sentences. Do not optimise style.

For multi-claim, uncertain or contradictory work, copy [`../templates/factual-kernel.md`](../templates/factual-kernel.md) and fill every applicable field before drafting prose.

## Record each material claim

| Field | Question |
|---|---|
| Subject | Who or what is this about? |
| State/action | What happened, exists, changes or is proposed? |
| Object | What does the action affect? |
| Consequence | Why does it matter, if the source supports that link? |
| Measure | What number, unit, date, range or example matters? |
| Status | Observed, estimated, assumed or unknown? |
| Provenance | What named source or source type supports it? Use `UNAVAILABLE` when none is available. |
| Decision use | What decision or reader question does this support? |

Every **material** claim requires both Status and Provenance. A sourced estimate is still `ESTIMATED`; provenance records who or what supplied it. Use `UNAVAILABLE` rather than silently leaving provenance blank. Non-material connective notes do not need the full record.

## Controlled-English-inspired checks

ASD-STE100 was designed for technical documentation, not general correspondence. Borrow only its useful clarity principles:

- one main topic per sentence;
- use the same word for the same concept;
- prefer a common verb over a formal synonym;
- use active voice when the actor matters;
- put a condition before an instruction or consequence when the reader needs the condition first;
- use technical names and verbs where the domain requires them;
- avoid ambiguous word forms when a clearer construction exists.

Do not attempt formal STE compliance unless the task explicitly requires it.

## Example

Weak polished draft:

> Holocron provides a robust regional capability that enables faster operational decision-making during GNSS disruption.

Completed kernel:

### Source scope

- **Task / decision:** Explain the current Holocron evidence without overstating impact.
- **Audience / use:** Internal wiki readers deciding what is known and what still needs proof.
- **Sources read:** Receiver A server log dated 18 August 2026; technical-lead estimate; project record.
- **Material source gaps:** Recovery-estimate method and dashboard-attribution evidence.

### Material claims

| ID | Subject | State / action | Object | Consequence | Measure | Status | Provenance | Decision use |
|---|---|---|---|---|---|---|---|---|
| C1 | Receiver A | sent | GNSS messages | NONE | 1,240 messages on 18 August 2026 | OBSERVED | Receiver A server log, 18 August 2026 | Establish observed system activity |
| C2 | Wider mitigation programme | is estimated to recover | GNSS-affected time | May reduce disruption across the programme | About 30%; calculation method unavailable | ESTIMATED | Named technical-lead estimate | Use only as an unverified programme scenario |
| C3 | Holocron | has | an unmeasured share of the programme recovery | Dashboard benefit cannot yet be attributed | NONE | UNKNOWN | Project record; attribution evidence unavailable | Do not claim the 30% recovery for Holocron |
| C4 | System | uses | NMEA 0183 | NONE | NONE | OBSERVED | Technical system record | Preserve the exact protocol name |
| C5 | System | uses | Redis Streams | NONE | NONE | OBSERVED | Technical system record | Preserve the exact component name |

### Relationships and uncertainty

- **Supported causal links:** NONE. C1 does not prove C2 or C3.
- **Conflicts:** NONE.
- **Unknowns that limit the text:** C2 has no recorded calculation method; C3 has no attribution evidence.
- **Terms that must stay exact:** Holocron, GNSS, NMEA 0183 and Redis Streams.

### Handoff

- **Claims to include:** C1, C2, C3, C4 and C5.
- **Claims to omit:** NONE.
- **Reader action / question:** Treat the 30% figure as a programme estimate and collect evidence before attributing any share to Holocron.

Only after this kernel is correct should a genre skill decide what belongs in the final prose.
