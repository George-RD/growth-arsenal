"""State model and phase gates for the growth-arsenal workspace."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
TRACKS = {
    "offer": [
        ("discovery", "Discovery"),
        ("market", "Starving Crowd"),
        ("pricing", "Pricing"),
        ("value", "Value Equation"),
        ("stack", "Offer Stack"),
        ("enhancement", "Enhancement"),
    ]
}
VALID_STATUSES = {"not_started", "draft", "in_review", "approved", "stale"}


class ArsenalError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def checksum(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def project_slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        raise ArsenalError("Project slug is empty")
    return result


def read_json(path: str | Path) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ArsenalError(f"No such file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ArsenalError(f"Invalid JSON in {path}: {exc.msg} at line {exc.lineno}") from exc


def atomic_write(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_path = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, target)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def save_workspace(path: str | Path, state: dict[str, Any]) -> None:
    state["project"]["updated_at"] = utc_now()
    state["workspace_revision"] = state.get("workspace_revision", 0) + 1
    atomic_write(path, json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def load_workspace(path: str | Path) -> dict[str, Any]:
    state = read_json(path)
    if not isinstance(state, dict):
        raise ArsenalError("Workspace root must be an object")
    return state


def new_phase(label: str) -> dict[str, Any]:
    return {
        "label": label,
        "status": "not_started",
        "revision": 0,
        "summary": "",
        "data": {},
        "evidence_refs": [],
        "reviews": [],
        "input_revisions": {},
        "data_hash": checksum({}),
        "approved_at": None,
        "stale_reason": None,
    }


def new_workspace(
    project: str,
    name: str | None,
    locale: str,
    currency: str,
    spelling: str,
    timezone_name: str,
) -> dict[str, Any]:
    stamp = utc_now()
    slug = project_slug(project)
    return {
        "schema_version": SCHEMA_VERSION,
        "workspace_revision": 0,
        "project": {
            "slug": slug,
            "name": name or project,
            "created_at": stamp,
            "updated_at": stamp,
            "locale": locale,
            "currency": currency.upper(),
            "spelling": spelling,
            "timezone": timezone_name,
        },
        "tracks": {
            "offer": {
                "current_phase": "discovery",
                "phases": {key: new_phase(label) for key, label in TRACKS["offer"]},
            }
        },
        "research": {"market_identity": {}, "personas": [], "sources": [], "gaps": []},
        "accepted_risks": [],
        "events": [],
        "render": {"theme": "qualification-lab", "last_rendered_at": None, "outputs": []},
    }


def record_event(state: dict[str, Any], event_type: str, **data: Any) -> None:
    state.setdefault("events", []).append({"at": utc_now(), "type": event_type, **data})


def phase_order(track: str) -> list[str]:
    if track not in TRACKS:
        raise ArsenalError(f"Unknown track: {track}")
    return [key for key, _ in TRACKS[track]]


def get_phase(state: dict[str, Any], track: str, phase: str) -> dict[str, Any]:
    try:
        return state["tracks"][track]["phases"][phase]
    except KeyError as exc:
        raise ArsenalError(f"Unknown phase {track}:{phase}") from exc


def upstream_revisions(state: dict[str, Any], track: str, phase: str) -> dict[str, int]:
    order = phase_order(track)
    return {key: get_phase(state, track, key)["revision"] for key in order[: order.index(phase)]}


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def invalidate_downstream(state: dict[str, Any], track: str, changed_phase: str) -> list[str]:
    order = phase_order(track)
    invalidated: list[str] = []
    for key in order[order.index(changed_phase) + 1 :]:
        phase = get_phase(state, track, key)
        if phase["revision"] or phase["status"] != "not_started":
            phase.update(status="stale", stale_reason=f"Upstream phase {changed_phase} changed", approved_at=None)
            invalidated.append(key)
    return invalidated


def validate_review(review: Any) -> None:
    if not isinstance(review, dict) or not str(review.get("reviewer", "")).strip():
        raise ArsenalError("Review needs reviewer")
    score = review.get("score")
    if score is not None and (not isinstance(score, (int, float)) or not 0 <= score <= 10):
        raise ArsenalError("Review score must be 0-10")
    issues = review.get("issues", [])
    if not isinstance(issues, list):
        raise ArsenalError("Review issues must be a list")
    for issue in issues:
        if not isinstance(issue, dict) or not str(issue.get("issue_key", "")).strip():
            raise ArsenalError("Every issue needs issue_key")


def accepted_issue_keys(state: dict[str, Any], track: str, phase: str) -> set[str]:
    return {
        risk["issue_key"]
        for risk in state.get("accepted_risks", [])
        if risk.get("track") == track and risk.get("phase") == phase
    }


def compute_gate(state: dict[str, Any], track: str, phase: str) -> dict[str, Any]:
    grouped: dict[str, dict[str, Any]] = {}
    reviews = get_phase(state, track, phase).get("reviews", [])
    for review in reviews:
        reviewer = str(review.get("reviewer", "unknown"))
        for issue in review.get("issues", []):
            key = str(issue.get("issue_key", "")).strip()
            if not key:
                continue
            group = grouped.setdefault(
                key,
                {
                    "issue_key": key,
                    "title": issue.get("title") or key.replace("-", " ").title(),
                    "reviewers": set(),
                    "findings": [],
                    "blocking": False,
                },
            )
            group["reviewers"].add(reviewer)
            group["blocking"] = group["blocking"] or bool(issue.get("blocking", False))
            group["findings"].append(
                {
                    "reviewer": reviewer,
                    "finding": issue.get("finding", ""),
                    "evidence": issue.get("evidence", ""),
                    "recommended_fix": issue.get("recommended_fix", ""),
                }
            )
    accepted = accepted_issue_keys(state, track, phase)
    issues: list[dict[str, Any]] = []
    critical_open: list[dict[str, Any]] = []
    for key in sorted(grouped):
        group = grouped[key]
        group["reviewers"] = sorted(group["reviewers"])
        group["consensus_count"] = len(group["reviewers"])
        group["accepted_risk"] = key in accepted
        group["is_critical"] = group["blocking"] or group["consensus_count"] >= 2
        issues.append(group)
        if group["is_critical"] and not group["accepted_risk"]:
            critical_open.append(group)
    return {
        "track": track,
        "phase": phase,
        "review_count": len(reviews),
        "issues": issues,
        "critical_open": critical_open,
        "can_approve": not critical_open,
    }


def validate_workspace(state: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if state.get("schema_version") != SCHEMA_VERSION:
        findings.append({"level": "error", "code": "schema-version", "message": f"Expected {SCHEMA_VERSION}"})
    for key in ("slug", "name", "locale", "currency", "spelling", "timezone"):
        if not state.get("project", {}).get(key):
            findings.append({"level": "error", "code": f"project-{key}", "message": f"Missing project.{key}"})
    for track, definitions in TRACKS.items():
        for name, _ in definitions:
            try:
                phase = get_phase(state, track, name)
            except ArsenalError as exc:
                findings.append({"level": "error", "code": f"phase-{name}", "message": str(exc)})
                continue
            if phase.get("status") not in VALID_STATUSES:
                findings.append({"level": "error", "code": f"status-{name}", "message": "Invalid phase status"})
            if phase.get("status") == "approved" and phase.get("input_revisions", {}) != upstream_revisions(state, track, name):
                findings.append(
                    {
                        "level": "error",
                        "code": f"stale-{track}-{name}",
                        "message": f"Approved {track}:{name} has stale upstream revisions",
                    }
                )
            for review in phase.get("reviews", []):
                try:
                    validate_review(review)
                except ArsenalError as exc:
                    findings.append({"level": "error", "code": f"review-{name}", "message": str(exc)})
    return findings
