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


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    if value in (None, ""):
        return []
    return [value]


def template(name: str, values: dict[str, str]) -> str:
    text = (ASSETS / "templates" / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def status_badge(status: str) -> str:
    label = status.replace("_", " ").title()
    return f'<span class="status status--{esc(status)}">{esc(label)}</span>'


def navigation(slug: str, active: str) -> str:
    pages = (
        ("offer-summary", "Offer"),
        ("workshop-progress", "Offer progress"),
        ("research-dashboard", "Research"),
        ("leads-blueprint", "Leads"),
        ("tracking-dashboard", "Tracking"),
    )
    return "".join(
        f'<a class="report-nav__link{" is-active" if key == active else ""}" href="./{esc(slug)}-{key}.html">{label}</a>'
        for key, label in pages
    )


def shell(state: dict[str, Any], active: str, title: str, content: str) -> str:
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
    if value in (None, ""):
        return "—"
    return f"{currency} {value:,.0f}" if isinstance(value, (int, float)) else str(value)


def phase_summaries(state: dict[str, Any], track: str) -> list[dict[str, Any]]:
    rows = []
    for name, label in TRACKS[track]:
        phase = get_phase(state, track, name)
        gate = compute_gate(state, track, name)
        scores = [r.get("score") for r in phase.get("reviews", []) if isinstance(r.get("score"), (int, float))]
        rows.append(
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
    return rows


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
        f'<div class="instrument-row"><div><span class="instrument-row__label">{label}</span><p>{esc(pick(value, *descriptions, default=""))}</p></div><strong>{esc(pick(value, *scores, default="—"))}/10</strong></div>'
        for scores, descriptions, label in (
            (("dream_outcome_score", "dream_score"), ("dream_outcome",), "Dream outcome"),
            (("likelihood_score",), ("perceived_likelihood",), "Perceived likelihood"),
            (("time_delay_score", "time_score"), ("time_delay",), "Time delay"),
            (("effort_score",), ("effort_sacrifice",), "Effort and sacrifice"),
        )
    )
    items = as_list(pick(stack, "items", default=[]))
    if not items:
        core = pick(stack, "core", default=None)
        if isinstance(core, dict):
            items.append({"kind": "Core offer", **core})
        items.extend(item for item in as_list(pick(stack, "bonuses", default=[])) if isinstance(item, dict))
    stack_rows = "".join(
        f'<article class="stack-item"><div><span class="stack-item__kind">{esc(item.get("kind", "Deliverable"))}</span><h3>{esc(pick(item, "name", "title", default="Unnamed item"))}</h3><p>{esc(pick(item, "description", "summary", default=""))}</p></div><strong>{esc(money(pick(item, "value", "anchored_value"), currency))}</strong></article>'
        for item in items if isinstance(item, dict)
    ) or '<p class="empty-state">No offer stack has been recorded.</p>'
    guarantee = pick(enhancement, "guarantee", default={})
    if isinstance(guarantee, str):
        guarantee = {"terms": guarantee}
    gate = compute_gate(state, "offer", "enhancement")
    final_score = phase_summaries(state, "offer")[-1]["score"]
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
    rows = phase_summaries(state, "offer")
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
        for key, value in research.get("market_identity", {}).items() if value not in (None, "", [], {})
    ) or '<p class="empty-state">Market identity has not been recorded.</p>'
    gaps = "".join(
        f'<tr><td>{esc(item.get("phase", "—"))}</td><td>{esc(item.get("requirement", ""))}</td><td>{status_badge("approved" if str(item.get("status", "")).lower() in {"ok", "complete", "green"} else "draft")}</td></tr>'
        for item in research.get("gaps", []) if isinstance(item, dict)
    ) or '<tr><td colspan="3" class="empty-state">No structured gap analysis recorded.</td></tr>'
    personas = "".join(
        f'<article class="persona-record"><div class="persona-record__head"><div><span>Customer record</span><h3>{esc(item.get("name", "Unnamed persona"))}</h3></div><strong>{esc(item.get("pain_score", "—"))}/10 pain</strong></div><p>{esc(pick(item, "snapshot", "summary", default=""))}</p><dl><div><dt>Budget</dt><dd>{esc(item.get("budget", "Not recorded"))}</dd></div><div><dt>Channels</dt><dd>{esc(", ".join(str(value) for value in as_list(item.get("discovery_channels", []))))}</dd></div></dl></article>'
        for item in research.get("personas", []) if isinstance(item, dict)
    ) or '<p class="empty-state">No personas recorded.</p>'
    sources = "".join(
        f'<article class="source-row"><div><strong>{esc(item.get("title") or item.get("url") or "Untitled source")}</strong><p>{esc(item.get("evidence", item.get("snippet", "")))}</p></div><span>{esc(item.get("category", "Evidence"))}</span></article>'
        for item in research.get("sources", []) if isinstance(item, dict)
    ) or '<p class="empty-state">No sources recorded.</p>'
    content = template("research-dashboard.html", {"IDENTITY_CELLS": identity, "GAP_ROWS": gaps, "PERSONA_RECORDS": personas, "SOURCE_ROWS": sources})
    return shell(state, "research-dashboard", f"Research dashboard — {state['project']['name']}", content)


def leads_blueprint_report(state: dict[str, Any]) -> str:
    phases = {key: get_phase(state, "leads", key) for key, _ in TRACKS["leads"]}
    discovery = phases["discovery"].get("data", {})
    magnets = phases["lead-magnet"].get("data", {})
    channels = phases["channels"].get("data", {})
    execution = phases["execution"].get("data", {})
    getters = phases["lead-getters"].get("data", {})
    rule = phases["rule-of-100"].get("data", {})
    offer_status = get_phase(state, "offer", "enhancement")["status"]
    magnet_rows = "".join(
        f'<article class="stack-item"><div><span class="stack-item__kind">{esc(item.get("type", "Lead magnet"))}</span><h3>{esc(pick(item, "name", "title", default="Unnamed magnet"))}</h3><p>{esc(pick(item, "narrow_problem", "description", default=""))}</p></div><strong>{esc(item.get("score", "—"))}/10</strong></article>'
        for item in as_list(pick(magnets, "lead_magnets", "magnets", default=[])) if isinstance(item, dict)
    ) or '<p class="empty-state">No lead magnets have been approved.</p>'
    asset_rows = "".join(
        f'<article class="source-row"><div><strong>{esc(pick(item, "name", "title", default=item.get("kind", "Asset")))}</strong><p>{esc(pick(item, "copy", "body", "summary", default=""))}</p></div><span>{esc(item.get("channel", item.get("kind", "Asset")))}</span></article>'
        for item in as_list(pick(execution, "assets", "scripts", default=[])) if isinstance(item, dict)
    ) or '<p class="empty-state">No execution assets recorded.</p>'
    getter_rows = "".join(
        f'<div class="instrument-row"><div><span class="instrument-row__label">{esc(key.replace("_", " "))}</span><p>{esc(value if not isinstance(value, (dict, list)) else json.dumps(value, ensure_ascii=False))}</p></div></div>'
        for key, value in getters.items() if value not in (None, "", [], {})
    ) or '<p class="empty-state">No lead-getter system recorded.</p>'
    content = template(
        "leads-blueprint.html",
        {
            "STATUS_BADGE": status_badge(phases["rule-of-100"]["status"]),
            "AUDIENCE": esc(pick(discovery, "audience", default=state.get("research", {}).get("market_identity", {}).get("niche", "Audience not set"))),
            "OFFER_DEPENDENCY": status_badge(offer_status),
            "PRIMARY_CHANNEL": esc(pick(channels, "primary_channel", "primary", default="Not selected")),
            "SECONDARY_CHANNEL": esc(pick(channels, "secondary_channel", "secondary", default="Not selected")),
            "DAILY_UNITS": esc(pick(rule, "daily_units", "units", default="Not set")),
            "MAGNET_ROWS": magnet_rows,
            "ASSET_ROWS": asset_rows,
            "GETTER_ROWS": getter_rows,
        },
    )
    return shell(state, "leads-blueprint", f"Lead generation blueprint — {state['project']['name']}", content)


def tracking_dashboard_report(state: dict[str, Any]) -> str:
    phases = {key: get_phase(state, "leads", key) for key, _ in TRACKS["leads"]}
    channels = phases["channels"].get("data", {})
    rule = phases["rule-of-100"].get("data", {})
    actions = "".join(
        f'<article class="phase-row"><div class="phase-row__index">{index:02d}</div><div class="phase-row__body"><div class="phase-row__heading"><h3>{esc(pick(item, "action", "name", default="Daily action"))}</h3><span class="status status--draft">{esc(item.get("target", "Set target"))}</span></div><p>{esc(item.get("time_block", item.get("notes", "")))}</p></div></article>'
        for index, item in enumerate(as_list(pick(rule, "daily_actions", "actions", default=[])), 1) if isinstance(item, dict)
    ) or '<p class="empty-state">No daily action plan recorded.</p>'
    metrics = []
    for kind in ("leading_metrics", "lagging_metrics"):
        for item in as_list(rule.get(kind, [])):
            if isinstance(item, dict):
                metrics.append({"kind": kind.replace("_", " "), **item})
    metric_rows = "".join(
        f'<tr><td>{esc(item.get("kind", "Metric"))}</td><td>{esc(pick(item, "name", "metric", default="Unnamed"))}</td><td>{esc(pick(item, "target", "daily_target", default="—"))}</td><td>{esc(item.get("actual", ""))}</td></tr>'
        for item in metrics
    ) or '<tr><td colspan="4" class="empty-state">No tracking metrics recorded.</td></tr>'
    milestones = "".join(
        f'<article class="stack-item"><div><span class="stack-item__kind">{esc(item.get("period", item.get("week", "Milestone")))}</span><h3>{esc(pick(item, "milestone", "name", default="Unnamed milestone"))}</h3><p>{esc(item.get("success_metric", ""))}</p></div></article>'
        for item in as_list(rule.get("milestones", [])) if isinstance(item, dict)
    ) or '<p class="empty-state">No milestones recorded.</p>'
    content = template(
        "tracking-dashboard.html",
        {
            "STATUS_BADGE": status_badge(phases["rule-of-100"]["status"]),
            "PRIMARY_CHANNEL": esc(pick(channels, "primary_channel", "primary", default="Not selected")),
            "DAILY_UNITS": esc(pick(rule, "daily_units", "units", default="Not set")),
            "DAYS": esc(pick(rule, "days", default=100)),
            "ACTION_ROWS": actions,
            "METRIC_ROWS": metric_rows,
            "MILESTONE_ROWS": milestones,
        },
    )
    return shell(state, "tracking-dashboard", f"Lead tracking dashboard — {state['project']['name']}", content)


def track_markdown(state: dict[str, Any], track: str, title: str) -> str:
    lines = [f"# {state['project']['name']} — {title}", "", f"Generated: {utc_now()}", ""]
    for name, label in TRACKS[track]:
        phase = get_phase(state, track, name)
        lines.extend([f"## {label}", f"Status: {phase['status']} | Revision: {phase['revision']}", ""])
        if phase.get("summary"):
            lines.extend([phase["summary"], ""])
        if phase.get("data"):
            lines.extend(["```json", json.dumps(phase["data"], ensure_ascii=False, indent=2, sort_keys=True), "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def offer_markdown_reports(state: dict[str, Any]) -> tuple[str, str, str]:
    offer = track_markdown(state, "offer", "Grand Slam Offer Workshop")
    research = f"# Research Brief — {state['project']['name']}\n\nUpdated: {utc_now()}\n\n```json\n{json.dumps(state.get('research', {}), ensure_ascii=False, indent=2, sort_keys=True)}\n```\n"
    decisions = [f"# Decision Log — {state['project']['name']}", ""]
    for event in state.get("events", []):
        if event.get("type") in {"phase.approved", "risk.accepted", "phase.applied"}:
            details = ", ".join(f"{key}={value}" for key, value in event.items() if key not in {"at", "type"})
            decisions.append(f"- {event.get('at')} {event.get('type', '').upper()}: {details}")
    if len(decisions) == 2:
        decisions.append("- No decisions recorded.")
    return offer, research, "\n".join(decisions) + "\n"


def leads_markdown_reports(state: dict[str, Any]) -> tuple[str, str, str]:
    blueprint = track_markdown(state, "leads", "Lead Generation Blueprint")
    execution = get_phase(state, "leads", "execution").get("data", {})
    scripts = [f"# Outreach and Campaign Assets — {state['project']['name']}", ""]
    for item in as_list(pick(execution, "assets", "scripts", default=[])):
        if isinstance(item, dict):
            scripts.extend([f"## {pick(item, 'name', 'title', default=item.get('kind', 'Asset'))}", "", str(pick(item, "copy", "body", "summary", default="")), ""])
    if len(scripts) == 2:
        scripts.append("No execution assets recorded.\n")
    rule = get_phase(state, "leads", "rule-of-100").get("data", {})
    tracking = f"# Tracking Plan — {state['project']['name']}\n\n```json\n{json.dumps(rule, ensure_ascii=False, indent=2, sort_keys=True)}\n```\n"
    return blueprint, "\n".join(scripts).rstrip() + "\n", tracking


def render_all(state: dict[str, Any], output_dir: str | Path, surface: str = "all", allow_invalid: bool = False) -> list[str]:
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
        "leads-blueprint": leads_blueprint_report,
        "tracking-dashboard": tracking_dashboard_report,
    }
    selected = list(renderers) if surface == "all" else [surface]
    written: list[str] = []
    for name in selected:
        path = output / f"{slug}-{name}.html"
        atomic_write(path, renderers[name](state))
        written.append(str(path))
    if surface == "all":
        offer, research, decisions = offer_markdown_reports(state)
        leads, scripts, tracking = leads_markdown_reports(state)
        for filename, text in (
            (f"{slug}-offer.md", offer),
            (f"{slug}-research.md", research),
            (f"{slug}-decisions.md", decisions),
            (f"{slug}-leads-blueprint.md", leads),
            (f"{slug}-outreach-scripts.md", scripts),
            (f"{slug}-tracking-dashboard.md", tracking),
        ):
            path = output / filename
            atomic_write(path, text)
            written.append(str(path))
    return written
