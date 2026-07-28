"""Dependency-free, self-contained HTML and Markdown report rendering."""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from workspace import TRACKS, atomic_write, compute_gate, get_phase, utc_now, validate_workspace

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def pick(mapping: Any, *keys: str, default: Any = None) -> Any:
    if not isinstance(mapping, dict):
        return default
    for key in keys:
        if mapping.get(key) not in (None, "", [], {}):
            return mapping[key]
    return default


def template(name: str, values: dict[str, str]) -> str:
    text = (ASSETS / "templates" / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def status_badge(status: str) -> str:
    label = status.replace("_", " ").title()
    return f'<span class="status status--{esc(status)}">{esc(label)}</span>'


def navigation(slug: str, active: str) -> str:
    pages = (("offer-summary", "Offer summary"), ("workshop-progress", "Workshop progress"), ("research-dashboard", "Research"))
    return "".join(
        f'<a class="report-nav__link{" is-active" if key == active else ""}" href="./{esc(slug)}-{key}.html">{label}</a>'
        for key, label in pages
    )


def shell(state: dict[str, Any], active: str, title: str, content: str) -> str:
    css = (ASSETS / "design" / "report.css").read_text(encoding="utf-8")
    js = (ASSETS / "design" / "report.js").read_text(encoding="utf-8")
    project = state["project"]
    return template(
        "base.html",
        {
            "LANG": esc(project["locale"]),
            "TITLE": esc(title),
            "CSS": css,
            "SCRIPT": js,
            "PROJECT_NAME": esc(project["name"]),
            "NAV": navigation(project["slug"], active),
            "CONTENT": content,
            "GENERATED_AT": esc(utc_now()),
        },
    )


def money(value: Any, currency: str) -> str:
    if value in (None, ""):
        return "—"
    if isinstance(value, (int, float)):
        return f"{currency} {value:,.0f}"
    return str(value)


def phase_summaries(state: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for name, label in TRACKS["offer"]:
        phase = get_phase(state, "offer", name)
        gate = compute_gate(state, "offer", name)
        scores = [r.get("score") for r in phase.get("reviews", []) if isinstance(r.get("score"), (int, float))]
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
    phases = {key: get_phase(state, "offer", key) for key, _ in TRACKS["offer"]}
    pricing = phases["pricing"].get("data", {})
    value = phases["value"].get("data", {})
    stack = phases["stack"].get("data", {})
    enhancement = phases["enhancement"].get("data", {})
    name = pick(enhancement, "offer_name", "name", default=state["project"]["name"])
    pitch = pick(enhancement, "elevator_pitch", default=phases["enhancement"].get("summary", ""))
    currency = state["project"]["currency"]
    value_rows = "".join(
        f'<div class="instrument-row"><div><span class="instrument-row__label">{label}</span></div><strong>{esc(pick(value, *keys, default="—"))}/10</strong></div>'
        for keys, label in ((("dream_outcome_score", "dream_score"), "Dream outcome"), (("likelihood_score",), "Perceived likelihood"), (("time_delay_score", "time_score"), "Time delay"), (("effort_score",), "Effort and sacrifice"))
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
        f'<article class="stack-item"><div><span class="stack-item__kind">{esc(item.get("kind", "Deliverable"))}</span><h3>{esc(pick(item, "name", "title", default="Unnamed item"))}</h3><p>{esc(pick(item, "description", "summary", default=""))}</p></div><strong>{esc(money(pick(item, "value", "anchored_value"), currency))}</strong></article>'
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
            "VERDICT": esc("Clear to test" if phases["enhancement"]["status"] == "approved" else "Still in qualification"),
            "OFFER_NAME": esc(name),
            "PITCH": esc(pitch),
            "PRICE": esc(money(pick(pricing, "price", default=pick(stack, "price")), currency)),
            "TOTAL_VALUE": esc(money(pick(stack, "total_value", "anchored_value"), currency)),
            "CONSENSUS": esc(f"{final_score}/10" if final_score is not None else "—"),
            "OPEN_CRITICAL": str(len(gate["critical_open"])),
            "VALUE_ITEMS": value_rows,
            "STACK_ITEMS": stack_rows,
            "GUARANTEE_NAME": esc(pick(guarantee, "name", default=pick(enhancement, "guarantee_name", default="Guarantee not set"))),
            "GUARANTEE_TERMS": esc(pick(guarantee, "terms", "description", default=pick(enhancement, "guarantee_terms", default="No terms recorded."))),
            "GUARANTEE_CATEGORY": esc(pick(guarantee, "category", default=pick(enhancement, "guarantee_category", default="Unclassified"))),
            "SCARCITY": esc(pick(enhancement, "scarcity", default="Not set")),
            "URGENCY": esc(pick(enhancement, "urgency", default="Not set")),
        },
    )
    return shell(state, "offer-summary", f"Offer summary — {name}", content)


def progress_report(state: dict[str, Any]) -> str:
    rows = phase_summaries(state)
    phase_rows = "".join(
        f'<article class="phase-row phase-row--{esc(row["status"])}"><div class="phase-row__index">{index:02d}</div><div class="phase-row__body"><div class="phase-row__heading"><h3>{esc(row["label"])}</h3>{status_badge(row["status"])}</div><p>{esc(row["summary"])}</p><div class="phase-row__meta"><span>Revision {row["revision"]}</span><span>{row["reviews"]} reviews</span><span>{row["critical"]} open critical</span><span>Score {esc(str(row["score"]) if row["score"] is not None else "—")}</span></div></div></article>'
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
    return shell(state, "workshop-progress", f"Workshop progress — {state['project']['name']}", content)


def research_report(state: dict[str, Any]) -> str:
    research = state.get("research", {})
    identity = "".join(
        f'<article class="evidence-cell"><span>{esc(key.replace("_", " "))}</span><strong>{esc(value)}</strong></article>'
        for key, value in research.get("market_identity", {}).items()
        if value not in (None, "", [], {})
    ) or '<p class="empty-state">Market identity has not been recorded.</p>'
    gaps = "".join(
        f'<tr><td>{esc(item.get("phase", "—"))}</td><td>{esc(item.get("requirement", ""))}</td><td>{status_badge("approved" if str(item.get("status", "")).lower() in {"ok", "complete", "green"} else "draft")}</td></tr>'
        for item in research.get("gaps", [])
        if isinstance(item, dict)
    ) or '<tr><td colspan="3" class="empty-state">No structured gap analysis recorded.</td></tr>'
    personas = "".join(
        f'<article class="persona-record"><div class="persona-record__head"><div><span>Customer record</span><h3>{esc(item.get("name", "Unnamed persona"))}</h3></div><strong>{esc(item.get("pain_score", "—"))}/10 pain</strong></div><p>{esc(pick(item, "snapshot", "summary", default=""))}</p><dl><div><dt>Budget</dt><dd>{esc(item.get("budget", "Not recorded"))}</dd></div></dl></article>'
        for item in research.get("personas", [])
        if isinstance(item, dict)
    ) or '<p class="empty-state">No personas recorded.</p>'
    sources = "".join(
        f'<article class="source-row"><div><strong>{esc(item.get("title") or item.get("url") or "Untitled source")}</strong><p>{esc(item.get("evidence", item.get("snippet", "")))}</p></div><span>{esc(item.get("category", "Evidence"))}</span></article>'
        for item in research.get("sources", [])
        if isinstance(item, dict)
    ) or '<p class="empty-state">No sources recorded.</p>'
    content = template("research-dashboard.html", {"IDENTITY_CELLS": identity, "GAP_ROWS": gaps, "PERSONA_RECORDS": personas, "SOURCE_ROWS": sources})
    return shell(state, "research-dashboard", f"Research dashboard — {state['project']['name']}", content)


def markdown_reports(state: dict[str, Any]) -> tuple[str, str, str]:
    lines = [f"# {state['project']['name']} — Grand Slam Offer Workshop", "", f"Generated: {utc_now()}", ""]
    for name, label in TRACKS["offer"]:
        phase = get_phase(state, "offer", name)
        lines.extend([f"## {label}", f"Status: {phase['status']} | Revision: {phase['revision']}", ""])
        if phase.get("summary"):
            lines.extend([phase["summary"], ""])
        if phase.get("data"):
            lines.extend(["```json", json.dumps(phase["data"], ensure_ascii=False, indent=2, sort_keys=True), "```", ""])
    offer = "\n".join(lines).rstrip() + "\n"
    research = f"# Research Brief — {state['project']['name']}\n\nUpdated: {utc_now()}\n\n```json\n{json.dumps(state.get('research', {}), ensure_ascii=False, indent=2, sort_keys=True)}\n```\n"
    decisions = [f"# Decision Log — {state['project']['name']}", ""]
    for event in state.get("events", []):
        if event.get("type") in {"phase.approved", "risk.accepted", "phase.applied"}:
            details = ", ".join(f"{key}={value}" for key, value in event.items() if key not in {"at", "type"})
            decisions.append(f"- {event.get('at')} {event.get('type', '').upper()}: {details}")
    if len(decisions) == 2:
        decisions.append("- No decisions recorded.")
    return offer, research, "\n".join(decisions) + "\n"


def render_all(state: dict[str, Any], output_dir: str | Path, surface: str = "all", allow_invalid: bool = False) -> list[str]:
    findings = validate_workspace(state)
    if any(item["level"] == "error" for item in findings) and not allow_invalid:
        raise RuntimeError("Workspace validation failed")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    slug = state["project"]["slug"]
    renderers = {"offer-summary": offer_report, "workshop-progress": progress_report, "research-dashboard": research_report}
    selected = list(renderers) if surface == "all" else [surface]
    written: list[str] = []
    for name in selected:
        path = output / f"{slug}-{name}.html"
        atomic_write(path, renderers[name](state))
        written.append(str(path))
    if surface == "all":
        offer, research, decisions = markdown_reports(state)
        for filename, text in ((f"{slug}-offer.md", offer), (f"{slug}-research.md", research), (f"{slug}-decisions.md", decisions)):
            path = output / filename
            atomic_write(path, text)
            written.append(str(path))
    return written
