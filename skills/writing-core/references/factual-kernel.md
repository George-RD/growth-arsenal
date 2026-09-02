# Factual kernel

Use this reference when the source is technical, uncertain, long or contradictory.

## Purpose

The kernel is a semantic intermediate representation. It separates **what the text means** from **how the text sounds** so later prose does not inherit a polished but weak frame.

Write fragments or terse sentences. Do not optimise style.

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

Kernel:

- Holocron shows live GNSS interference to the ROC. `OBSERVED` · source: live system / project record
- ROC operators use it during vessel work. `OBSERVED` · source: ROC operating evidence
- Live evidence may reduce time spent diagnosing events. `ESTIMATED` · source: operator hypothesis; measurement unavailable
- Live evidence may support earlier restart after the signal stabilises. `ESTIMATED` · source: operator hypothesis; measurement unavailable

Only after the kernel is correct should a genre skill decide what belongs in the final prose.
