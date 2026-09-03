"""Dependency-free, self-contained HTML and Markdown report rendering."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from workspace import (
    TRACKS,
    atomic_write,
    compute_gate,
    get_phase,
    utc_now,
    validate_workspace,
)

ASSETS = Path(__file__).resolve().parents[1] / "assets"
PLACEHOLDER = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")


def esc(value: Any) -> str:
    """Escape arbitrary values for safe HTML text and attribute insertion."""

    return html.escape("" if value is None else str(value), quote=True)

def display_value(value: Any, default: str = "Not recorded") -> str:
    """Return a readable deterministic string for a report field."""

    if value in (None, "", [], {}):
        return default
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    if isinstance(value, dict):
        return "; ".join(
            f"{key.replace('_', ' ')}: {item}" for key, item in value.items()
        )
    return str(value)



def pick(mapping: Any, *keys: str, default: Any = None) -> Any:
    """Return the first non-empty mapping value among candidate keys."""

    if not isinstance(mapping, dict):
        return default
    for key in keys:
        if mapping.get(key) not in (None, "", [], {}):
            return mapping[key]
    return default


def template(name: str, values: dict[str, str]) -> str:
    """Substitute known template tokens in one pass without rescanning values."""

    text = (ASSETS / "templates" / name).read_text(encoding="utf-8")
    return PLACEHOLDER.sub(
        lambda match: values.get(match.group(1), match.group(0)),
        text,
    )


def status_badge(status: str) -> str:
    """Render a status label using the shared report vocabulary."""

    label = status.replace("_", " ").title()
    return f'<span class="status status--{esc(status)}">{esc(label)}</span>'


def navigation(slug: str, active: str) -> str:
    """Render navigation for the three offer-workshop report surfaces."""

    pages = (
        ("offer-summary", "Offer summary"),
        ("workshop-progress", "Workshop progress"),
        ("research-dashboard", "Research"),
    )
    return "".join(
        f'<a class="report-nav__link{" is-active" if key == active else ""}" '
        f'href="./{esc(slug)}-{key}.html">{label}</a>'
        for key, label in pages
    )


def shell(state: dict[str, Any], active: str, title: str, content: str) -> str:
    """Wrap report content in the self-contained shared HTML shell."""

    project = state["project"]
    return template(
        "base.html",
        {
            "LANG": esc(project["locale"]),
            "TITLE": esc(title),
            "CSS": (ASSETS / "design" / "report.css").read_text(encoding="utf-8"),
            "SCRIPT": (ASSETS / "design" / "report.js").read_text(encoding="utf-8"),
            "PROJECT_NAME": esc(project["name"]),
            "NAV": navigation(project["slug"], active),
            "CONTENT": content,
            "GENERATED_AT": esc(utc_now()),
        },
    )


def money(value: Any, currency: str) -> str:
    """Format numeric values with the workspace currency code."""

    if value in (None, ""):
        return "—"
    if isinstance(value, (int, float)):
        return f"{currency} {value:,.0f}"
    return str(value)


def phase_summaries(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Build compact offer-phase summaries for progress and score views."""

    result = []
    for name, label in TRACKS["offer"]:
        phase = get_phase(state, "offer", name)
        gate = compute_gate(state, "offer", name)
        scores = [
            review.get("score")
            for review in phase.get("reviews", [])
            if isinstance(review.get("score"), (int, float))
        ]
        result.append(
            {
                "name": name,
                "label": label,
                "status": phase["status"],
                "revision": phase["revision"],
                "summary": phase.get("summary", ""),
                "reviews": len(phase.get("reviews", [])),
                "critical": len(gate["critical_open"]),
                "score": round(sum(scores) / len(scores), 1) if scores else None,
            }
        )
    return result


def offer_report(state: dict[str, Any]) -> str:
    """Render the final offer summary from canonical phase state."""

    phases = {key: get_phase(state, "offer", key) for key, _ in TRACKS["offer"]}
    pricing = phases["pricing"].get("data", {})
    value = phases["value"].get("data", {})
    stack = phases["stack"].get("data", {})
    enhancement = phases["enhancement"].get("data", {})
    name = pick(enhancement, "offer_name", "name", default=state["project"]["name"])
    pitch = pick(
        enhancement,
        "elevator_pitch",
        default=phases["enhancement"].get("summary", ""),
    )
    currency = state["project"]["currency"]
    value_rows = "".join(
        f'<div class="instrument-row"><div><span class="instrument-row__label">{label}'
        f'</span></div><strong>{esc(pick(value, *keys, default="—"))}/10</strong></div>'
        for keys, label in (
            (("dream_outcome_score", "dream_score"), "Dream outcome"),
            (("likelihood_score",), "Perceived likelihood"),
            (("time_delay_score", "time_score"), "Time delay"),
            (("effort_score",), "Effort and sacrifice"),
        )
    )
    items = pick(stack, "items", default=[])
    if not items:
        items = []
        core = pick(stack, "core", default=None)
        if isinstance(core, dict):
            items.append({"kind": "Core offer", **core})
        bonuses = pick(stack, "bonuses", default=[])
        if isinstance(bonuses, dict):
            bonuses = list(bonuses.values())
        items.extend(item for item in bonuses if isinstance(item, dict))
    if isinstance(items, dict):
        items = list(items.values())
    stack_rows = "".join(
        f'<article class="stack-item"><div><span class="stack-item__kind">'
        f'{esc(item.get("kind", "Deliverable"))}</span><h3>'
        f'{esc(pick(item, "name", "title", default="Unnamed item"))}</h3><p>'
        f'{esc(pick(item, "description", "summary", default=""))}</p></div><strong>'
        f'{esc(money(pick(item, "value", "anchored_value"), currency))}</strong></article>'
        for item in items
        if isinstance(item, dict)
    ) or '<p class="empty-state">No offer stack has been recorded.</p>'
    guarantee = pick(enhancement, "guarantee", default={})
    if isinstance(guarantee, str):
        guarantee = {"terms": guarantee}
    gate = compute_gate(state, "offer", "enhancement")
    final_score = phase_summaries(state)[-1]["score"]
    content = template(
        "offer-summary.html",
        {
            "STATUS_BADGE": status_badge(phases["enhancement"]["status"]),
            "VERDICT": esc(
                "Clear to test"
                if phases["enhancement"]["status"] == "approved"
                else "Still in qualification"
            ),
            "OFFER_NAME": esc(name),
            "PITCH": esc(pitch),
            "PRICE": esc(
                money(
                    pick(pricing, "price", default=pick(stack, "price")),
                    currency,
                )
            ),
            "TOTAL_VALUE": esc(
                money(pick(stack, "total_value", "anchored_value"), currency)
            ),
            "CONSENSUS": esc(
                f"{final_score}/10" if final_score is not None else "—"
            ),
            "OPEN_CRITICAL": str(len(gate["critical_open"])),
            "VALUE_ITEMS": value_rows,
            "STACK_ITEMS": stack_rows,
            "GUARANTEE_NAME": esc(
                pick(
                    guarantee,
                    "name",
                    default=pick(
                        enhancement,
                        "guarantee_name",
                        default="Guarantee not set",
                    ),
                )
            ),
            "GUARANTEE_TERMS": esc(
                pick(
                    guarantee,
                    "terms",
                    "description",
                    default=pick(
                        enhancement,
                        "guarantee_terms",
                        default="No terms recorded.",
                    ),
                )
            ),
            "GUARANTEE_CATEGORY": esc(
                pick(
                    guarantee,
                    "category",
                    default=pick(
                        enhancement,
                        "guarantee_category",
                        default="Unclassified",
                    ),
                )
            ),
            "SCARCITY": esc(pick(enhancement, "scarcity", default="Not set")),
            "URGENCY": esc(pick(enhancement, "urgency", default="Not set")),
        },
    )
    return shell(state, "offer-summary", f"Offer summary — {name}", content)


def progress_report(state: dict[str, Any]) -> str:
    """Render phase status, reviews, stale state and consensus scores."""

    rows = phase_summaries(state)
    phase_rows = "".join(
        f'<article class="phase-row phase-row--{esc(row["status"])}">'
        f'<div class="phase-row__index">{index:02d}</div>'
        f'<div class="phase-row__body"><div class="phase-row__heading">'
        f'<h3>{esc(row["label"])}</h3>{status_badge(row["status"])}</div>'
        f'<p>{esc(row["summary"])}</p><div class="phase-row__meta">'
        f'<span>Revision {row["revision"]}</span>'
        f'<span>{row["reviews"]} reviews</span>'
        f'<span>{row["critical"]} open critical</span>'
        f'<span>Score {esc(str(row["score"]) if row["score"] is not None else "—")}'
        f'</span></div></div></article>'
        for index, row in enumerate(rows)
    )
    current = state["tracks"]["offer"]["current_phase"]
    content = template(
        "workshop-progress.html",
        {
            "CURRENT_PHASE": esc(dict(TRACKS["offer"]).get(current, current)),
            "APPROVED_COUNT": str(sum(row["status"] == "approved" for row in rows)),
            "TOTAL_PHASES": str(len(rows)),
            "STALE_COUNT": str(sum(row["status"] == "stale" for row in rows)),
            "PHASE_ROWS": phase_rows,
        },
    )
    return shell(
        state,
        "workshop-progress",
        f"Workshop progress — {state['project']['name']}",
        content,
    )


def research_report(state: dict[str, Any]) -> str:
    """Render research identity, gaps, personas and evidence sources."""

    research = state.get("research", {})
    identity = "".join(
        f'<article class="evidence-cell"><span>{esc(key.replace("_", " "))}</span>'
        f'<strong>{esc(value)}</strong></article>'
        for key, value in research.get("market_identity", {}).items()
        if value not in (None, "", [], {})
    ) or '<p class="empty-state">Market identity has not been recorded.</p>'
    gaps = "".join(
        f'<tr><td>{esc(item.get("phase", "—"))}</td>'
        f'<td>{esc(item.get("requirement", ""))}</td>'
        f'<td>{status_badge("approved" if str(item.get("status", "")).lower() in {"ok", "complete", "green"} else "draft")}</td></tr>'
        for item in research.get("gaps", [])
        if isinstance(item, dict)
    ) or '<tr><td colspan="3" class="empty-state">No structured gap analysis recorded.</td></tr>'
    personas = "".join(
        f'<article class="persona-record"><div class="persona-record__head"><div>'
        f'<span>Customer record</span><h3>{esc(item.get("name", "Unnamed persona"))}'
        f'</h3></div><strong>{esc(item.get("pain_score", "—"))}/10 pain</strong>'
        f'</div><p>{esc(pick(item, "snapshot", "summary", default=""))}</p><dl>'
        f'<div><dt>Pain points</dt><dd>{esc(display_value(pick(item, "pain_points", "specific_pain_points")))}</dd></div>'
        f'<div><dt>Current solutions</dt><dd>{esc(display_value(pick(item, "current_solutions", "current_solution")))}</dd></div>'
        f'<div><dt>Budget</dt><dd>{esc(display_value(pick(item, "budget", "spending_power")))}</dd></div>'
        f'<div><dt>Objections</dt><dd>{esc(display_value(pick(item, "objections", "objection_patterns")))}</dd></div>'
        f'<div><dt>Dream outcome</dt><dd>{esc(display_value(pick(item, "dream_outcome", "desired_outcome")))}</dd></div>'
        f'<div><dt>Channels</dt><dd>{esc(display_value(pick(item, "channels", "where_they_hang_out")))}</dd></div>'
        f'<div><dt>Buying psychology</dt><dd>{esc(display_value(pick(item, "buying_psychology", "buying_signals")))}</dd></div>'
        f'</dl></article>'
        for item in research.get("personas", [])
        if isinstance(item, dict)
    ) or '<p class="empty-state">No personas recorded.</p>'
    sources = "".join(
        f'<article class="source-row"><div><strong>'
        f'{esc(item.get("title") or item.get("url") or "Untitled source")}</strong>'
        f'<p>{esc(item.get("evidence", item.get("snippet", "")))}</p></div>'
        f'<span>{esc(item.get("category", "Evidence"))}</span></article>'
        for item in research.get("sources", [])
        if isinstance(item, dict)
    ) or '<p class="empty-state">No sources recorded.</p>'
    content = template(
        "research-dashboard.html",
        {
            "IDENTITY_CELLS": identity,
            "GAP_ROWS": gaps,
            "PERSONA_RECORDS": personas,
            "SOURCE_ROWS": sources,
        },
    )
    return shell(
        state,
        "research-dashboard",
        f"Research dashboard — {state['project']['name']}",
        content,
    )


def fenced_json(value: Any) -> str:
    """Render readable JSON in a fence longer than any backtick run in the data."""

    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}json\n{text}\n{fence}"


def markdown_reports(state: dict[str, Any]) -> tuple[str, str, str]:
    """Render generated offer, research and decision-log Markdown views."""

    lines = [
        f"# {state['project']['name']} — Grand Slam Offer Workshop",
        "",
        f"Generated: {utc_now()}",
        "",
    ]
    for name, label in TRACKS["offer"]:
        phase = get_phase(state, "offer", name)
        lines.extend(
            [
                f"## {label}",
                f"Status: {phase['status']} | Revision: {phase['revision']}",
                "",
            ]
        )
        if phase.get("summary"):
            lines.extend([phase["summary"], ""])
        if phase.get("data"):
            lines.extend([fenced_json(phase["data"]), ""])
    offer = "\n".join(lines).rstrip() + "\n"
    research = (
        f"# Research Brief — {state['project']['name']}\n\n"
        f"Updated: {utc_now()}\n\n{fenced_json(state.get('research', {}))}\n"
    )
    decisions = [f"# Decision Log — {state['project']['name']}", ""]
    for event in state.get("events", []):
        if event.get("type") in {
            "phase.approved",
            "risk.accepted",
            "phase.applied",
        }:
            details = ", ".join(
                f"{key}={value}"
                for key, value in event.items()
                if key not in {"at", "type"}
            )
            decisions.append(
                f"- {event.get('at')} {event.get('type', '').upper()}: {details}"
            )
    if len(decisions) == 2:
        decisions.append("- No decisions recorded.")
    return offer, research, "\n".join(decisions) + "\n"


def render_all(
    state: dict[str, Any],
    output_dir: str | Path,
    surface: str = "all",
    allow_invalid: bool = False,
) -> list[str]:
    """Render requested report surfaces and generated Markdown views."""

    findings = validate_workspace(state)
    if any(item["level"] == "error" for item in findings) and not allow_invalid:
        raise RuntimeError("Workspace validation failed")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    slug = state["project"]["slug"]
    renderers = {
        "offer-summary": offer_report,
        "workshop-progress": progress_report,
        "research-dashboard": research_report,
    }
    selected = list(renderers) if surface == "all" else [surface]
    unknown = [name for name in selected if name not in renderers]
    if unknown:
        raise RuntimeError(f"Unknown report surface: {', '.join(unknown)}")
    written: list[str] = []
    for name in selected:
        path = output / f"{slug}-{name}.html"
        atomic_write(path, renderers[name](state))
        written.append(str(path))
    if surface == "all":
        offer, research, decisions = markdown_reports(state)
        for filename, text in (
            (f"{slug}-offer.md", offer),
            (f"{slug}-research.md", research),
            (f"{slug}-decisions.md", decisions),
        ):
            path = output / filename
            atomic_write(path, text)
            written.append(str(path))
    return written
