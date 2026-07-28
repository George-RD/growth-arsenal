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
MIN_INDEPENDENT_REVIEWERS = 2


class ArsenalError(RuntimeError):
    """Raised when a workspace transition would violate its contract."""


def utc_now() -> str:
    """Return a stable UTC timestamp without microseconds."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical(value: Any) -> str:
    """Serialise a value deterministically for hashing."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def checksum(value: Any) -> str:
    """Return the SHA-256 checksum of a canonically serialised value."""

    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def project_slug(value: str) -> str:
    """Normalise a project name into a non-empty URL-safe slug."""

    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        raise ArsenalError("Project slug is empty")
    return result


def read_json(path: str | Path) -> Any:
    """Read and decode JSON, converting common failures into ArsenalError."""

    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ArsenalError(f"No such file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ArsenalError(f"Invalid JSON in {path}: {exc.msg} at line {exc.lineno}") from exc


def atomic_write(path: str | Path, text: str) -> None:
    """Write a text file atomically in the destination directory."""

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
    """Persist workspace state and increment its global revision."""

    state["project"]["updated_at"] = utc_now()
    state["workspace_revision"] = state.get("workspace_revision", 0) + 1
    atomic_write(path, json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def load_workspace(path: str | Path) -> dict[str, Any]:
    """Load a workspace object from disk."""

    state = read_json(path)
    if not isinstance(state, dict):
        raise ArsenalError("Workspace root must be an object")
    return state


def new_phase(label: str) -> dict[str, Any]:
    """Create the initial state for one workflow phase."""

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
    """Create a new declarative workspace with the offer track initialised."""

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
    """Append a timestamped event without rewriting prior history."""

    state.setdefault("events", []).append({"at": utc_now(), "type": event_type, **data})


def phase_order(track: str) -> list[str]:
    """Return phase keys for a known track in dependency order."""

    if track not in TRACKS:
        raise ArsenalError(f"Unknown track: {track}")
    return [key for key, _ in TRACKS[track]]


def preceding_phase_keys(track: str, phase: str) -> list[str]:
    """Return every phase that must be approved before the target phase."""

    order = phase_order(track)
    if phase not in order:
        raise ArsenalError(f"Unknown phase {track}:{phase}")
    return order[: order.index(phase)]


def get_phase(state: dict[str, Any], track: str, phase: str) -> dict[str, Any]:
    """Return one phase or raise a stable domain error."""

    try:
        return state["tracks"][track]["phases"][phase]
    except (KeyError, TypeError) as exc:
        raise ArsenalError(f"Unknown phase {track}:{phase}") from exc


def upstream_revisions(state: dict[str, Any], track: str, phase: str) -> dict[str, int]:
    """Snapshot the revisions of all upstream phases."""

    return {key: get_phase(state, track, key)["revision"] for key in preceding_phase_keys(track, phase)}


def require_predecessors_approved(state: dict[str, Any], track: str, phase: str) -> None:
    """Reject a transition when any prerequisite phase is not approved."""

    blocked = [
        key
        for key in preceding_phase_keys(track, phase)
        if get_phase(state, track, key).get("status") != "approved"
    ]
    if blocked:
        raise ArsenalError(
            f"Cannot use {track}:{phase} before approved predecessor(s): {', '.join(blocked)}"
        )


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge dictionaries while copying all inserted values."""

    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def invalidate_downstream(state: dict[str, Any], track: str, changed_phase: str) -> list[str]:
    """Mark every populated dependent phase stale after an upstream change."""

    order = phase_order(track)
    invalidated: list[str] = []
    for key in order[order.index(changed_phase) + 1 :]:
        phase = get_phase(state, track, key)
        if phase["revision"] or phase["status"] != "not_started":
            phase.update(
                status="stale",
                stale_reason=f"Upstream phase {changed_phase} changed",
                approved_at=None,
            )
            invalidated.append(key)
    return invalidated


def validate_review(review: Any) -> None:
    """Validate the runtime review contract before it reaches the gate."""

    if not isinstance(review, dict):
        raise ArsenalError("Review must be an object")
    reviewer = review.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ArsenalError("Review needs a non-whitespace reviewer")
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
    """Return risk acceptances that apply to the phase's current revision only."""

    current_revision = get_phase(state, track, phase).get("revision", 0)
    return {
        str(risk["issue_key"])
        for risk in state.get("accepted_risks", [])
        if isinstance(risk, dict)
        and risk.get("track") == track
        and risk.get("phase") == phase
        and risk.get("revision") == current_revision
        and str(risk.get("issue_key", "")).strip()
    }


def compute_gate(state: dict[str, Any], track: str, phase: str) -> dict[str, Any]:
    """Aggregate independent reviews into a deterministic approval gate."""

    grouped: dict[str, dict[str, Any]] = {}
    phase_state = get_phase(state, track, phase)
    reviews = phase_state.get("reviews", [])
    distinct_reviewers: set[str] = set()
    for review in reviews:
        reviewer = str(review.get("reviewer", "")).strip()
        if not reviewer:
            continue
        distinct_reviewers.add(reviewer)
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
    reviewers = sorted(distinct_reviewers)
    review_requirement_met = len(reviewers) >= MIN_INDEPENDENT_REVIEWERS
    return {
        "track": track,
        "phase": phase,
        "review_count": len(reviews),
        "distinct_reviewers": reviewers,
        "minimum_reviewers": MIN_INDEPENDENT_REVIEWERS,
        "review_requirement_met": review_requirement_met,
        "issues": issues,
        "critical_open": critical_open,
        "can_approve": review_requirement_met and not critical_open,
    }


def validate_workspace(state: dict[str, Any]) -> list[dict[str, str]]:
    """Return structural and lifecycle findings without mutating the workspace."""

    findings: list[dict[str, str]] = []
    if state.get("schema_version") != SCHEMA_VERSION:
        findings.append(
            {"level": "error", "code": "schema-version", "message": f"Expected {SCHEMA_VERSION}"}
        )
    if not isinstance(state.get("workspace_revision"), int) or state.get("workspace_revision", -1) < 0:
        findings.append(
            {"level": "error", "code": "workspace-revision", "message": "Invalid workspace_revision"}
        )
    project = state.get("project", {})
    if not isinstance(project, dict):
        findings.append({"level": "error", "code": "project", "message": "project must be an object"})
        project = {}
    for key in ("slug", "name", "locale", "currency", "spelling", "timezone"):
        if not project.get(key):
            findings.append(
                {"level": "error", "code": f"project-{key}", "message": f"Missing project.{key}"}
            )

    for track, definitions in TRACKS.items():
        track_state = state.get("tracks", {}).get(track)
        if not isinstance(track_state, dict):
            findings.append(
                {"level": "error", "code": f"track-{track}", "message": f"Missing track {track}"}
            )
            continue
        valid_phase_keys = {name for name, _ in definitions}
        if track_state.get("current_phase") not in valid_phase_keys:
            findings.append(
                {
                    "level": "error",
                    "code": f"current-phase-{track}",
                    "message": f"Invalid current phase for {track}",
                }
            )
        for name, _ in definitions:
            try:
                phase = get_phase(state, track, name)
            except ArsenalError as exc:
                findings.append(
                    {"level": "error", "code": f"phase-{name}", "message": str(exc)}
                )
                continue
            if phase.get("status") not in VALID_STATUSES:
                findings.append(
                    {"level": "error", "code": f"status-{name}", "message": "Invalid phase status"}
                )
            if not isinstance(phase.get("revision"), int) or phase.get("revision", -1) < 0:
                findings.append(
                    {
                        "level": "error",
                        "code": f"revision-{track}-{name}",
                        "message": "Invalid phase revision",
                    }
                )
            if not isinstance(phase.get("data"), dict):
                findings.append(
                    {
                        "level": "error",
                        "code": f"data-{track}-{name}",
                        "message": "Phase data must be an object",
                    }
                )
            elif phase.get("data_hash") != checksum(phase.get("data", {})):
                findings.append(
                    {
                        "level": "error",
                        "code": f"hash-{track}-{name}",
                        "message": f"{track}:{name} data hash does not match phase data",
                    }
                )
            reviews = phase.get("reviews", [])
            if not isinstance(reviews, list):
                findings.append(
                    {
                        "level": "error",
                        "code": f"reviews-{track}-{name}",
                        "message": "Phase reviews must be a list",
                    }
                )
                reviews = []
            for review in reviews:
                try:
                    validate_review(review)
                except ArsenalError as exc:
                    findings.append(
                        {"level": "error", "code": f"review-{name}", "message": str(exc)}
                    )

            if phase.get("status") == "approved":
                blocked_predecessors = [
                    key
                    for key in preceding_phase_keys(track, name)
                    if get_phase(state, track, key).get("status") != "approved"
                ]
                if blocked_predecessors:
                    findings.append(
                        {
                            "level": "error",
                            "code": f"order-{track}-{name}",
                            "message": f"Approved phase has unapproved predecessors: {', '.join(blocked_predecessors)}",
                        }
                    )
                if phase.get("input_revisions", {}) != upstream_revisions(state, track, name):
                    findings.append(
                        {
                            "level": "error",
                            "code": f"stale-{track}-{name}",
                            "message": f"Approved {track}:{name} has stale upstream revisions",
                        }
                    )
                gate = compute_gate(state, track, name)
                if not gate["review_requirement_met"]:
                    findings.append(
                        {
                            "level": "error",
                            "code": f"reviews-required-{track}-{name}",
                            "message": f"Approved {track}:{name} lacks two independent reviewers",
                        }
                    )
                if gate["critical_open"]:
                    findings.append(
                        {
                            "level": "error",
                            "code": f"critical-open-{track}-{name}",
                            "message": f"Approved {track}:{name} has open critical issues",
                        }
                    )
            if phase.get("status") == "stale" and not str(phase.get("stale_reason", "")).strip():
                findings.append(
                    {
                        "level": "error",
                        "code": f"stale-reason-{track}-{name}",
                        "message": "Stale phase needs stale_reason",
                    }
                )

    accepted_risks = state.get("accepted_risks", [])
    if not isinstance(accepted_risks, list):
        findings.append(
            {"level": "error", "code": "accepted-risks", "message": "accepted_risks must be a list"}
        )
    else:
        for index, risk in enumerate(accepted_risks):
            if (
                not isinstance(risk, dict)
                or not str(risk.get("track", "")).strip()
                or not str(risk.get("phase", "")).strip()
                or not str(risk.get("issue_key", "")).strip()
                or not isinstance(risk.get("revision"), int)
                or risk.get("revision", 0) < 1
            ):
                findings.append(
                    {
                        "level": "error",
                        "code": f"accepted-risk-{index}",
                        "message": "Invalid accepted-risk record",
                    }
                )

    events = state.get("events", [])
    if not isinstance(events, list):
        findings.append({"level": "error", "code": "events", "message": "events must be a list"})
    else:
        for index, event in enumerate(events):
            if not isinstance(event, dict) or not event.get("at") or not event.get("type"):
                findings.append(
                    {
                        "level": "error",
                        "code": f"event-{index}",
                        "message": "Invalid event record",
                    }
                )
    return findings
