#!/usr/bin/env python3
"""CLI for declarative growth-arsenal workspaces."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render import render_all
from workspace import (
    TRACKS,
    ArsenalError,
    checksum,
    compute_gate,
    deep_merge,
    get_phase,
    invalidate_downstream,
    load_workspace,
    new_workspace,
    phase_order,
    read_json,
    record_event,
    require_predecessors_approved,
    save_workspace,
    upstream_revisions,
    utc_now,
    validate_review,
    validate_workspace,
)


def command_init(args: argparse.Namespace) -> dict:
    """Initialise a workspace without overwriting an existing file by default."""

    path = Path(args.workspace)
    if path.exists() and not args.force:
        raise ArsenalError(f"Workspace exists: {path}")
    state = new_workspace(
        args.project,
        args.name,
        args.locale,
        args.currency,
        args.spelling,
        args.timezone,
    )
    record_event(state, "workspace.initialised", project=state["project"]["slug"])
    save_workspace(path, state)
    return {
        "ok": True,
        "workspace": str(path),
        "project": state["project"],
        "next": "offer:discovery",
    }


def command_apply(args: argparse.Namespace) -> dict:
    """Apply a new phase revision after verifying prerequisite approvals."""

    state = load_workspace(args.workspace)
    require_predecessors_approved(state, args.track, args.phase)
    payload = read_json(args.input)
    if not isinstance(payload, dict):
        raise ArsenalError("Phase payload must be an object")
    data = payload.get("data", payload.get("phase_data", {}))
    if not isinstance(data, dict):
        raise ArsenalError("Phase data must be an object")
    evidence_refs = payload.get("evidence_refs", [])
    if not isinstance(evidence_refs, list) or not all(isinstance(item, str) for item in evidence_refs):
        raise ArsenalError("evidence_refs must be a list of strings")

    phase = get_phase(state, args.track, args.phase)
    phase.update(
        revision=phase["revision"] + 1,
        status="draft",
        summary=str(payload.get("summary", "")).strip(),
        data=copy.deepcopy(data),
        evidence_refs=copy.deepcopy(evidence_refs),
        reviews=[],
        approved_at=None,
        input_revisions=upstream_revisions(state, args.track, args.phase),
        stale_reason=None,
    )
    phase["data_hash"] = checksum(phase["data"])
    if isinstance(payload.get("research_patch"), dict):
        state["research"] = deep_merge(state.get("research", {}), payload["research_patch"])
    invalidated = invalidate_downstream(state, args.track, args.phase)
    state["tracks"][args.track]["current_phase"] = args.phase
    record_event(
        state,
        "phase.applied",
        track=args.track,
        phase=args.phase,
        revision=phase["revision"],
        invalidated=invalidated,
    )
    save_workspace(args.workspace, state)
    return {
        "ok": True,
        "track": args.track,
        "phase": args.phase,
        "revision": phase["revision"],
        "invalidated": invalidated,
    }


def command_add_review(args: argparse.Namespace) -> dict:
    """Attach one or more independent reviews to the current phase revision."""

    state = load_workspace(args.workspace)
    payload = read_json(args.input)
    reviews = payload if isinstance(payload, list) else [payload]
    phase = get_phase(state, args.track, args.phase)
    if not phase.get("revision"):
        raise ArsenalError("Cannot review an untouched phase")
    if phase.get("status") not in {"draft", "in_review"}:
        raise ArsenalError("Re-apply stale or approved content before reviewing it")

    for review in reviews:
        validate_review(review)
        item = copy.deepcopy(review)
        item["reviewer"] = item["reviewer"].strip()
        item["revision"] = phase["revision"]
        item["submitted_at"] = item.get("submitted_at") or utc_now()
        for issue in item.get("issues", []):
            issue["issue_key"] = str(issue["issue_key"]).strip()
        phase.setdefault("reviews", []).append(item)
    phase["status"] = "in_review"
    record_event(
        state,
        "review.added",
        track=args.track,
        phase=args.phase,
        revision=phase["revision"],
        count=len(reviews),
    )
    save_workspace(args.workspace, state)
    return {
        "ok": True,
        "added": len(reviews),
        "gate": compute_gate(state, args.track, args.phase),
    }


def command_accept_risk(args: argparse.Namespace) -> dict:
    """Record an explicit risk acceptance for the current phase revision."""

    state = load_workspace(args.workspace)
    phase = get_phase(state, args.track, args.phase)
    if not phase.get("revision") or phase.get("status") != "in_review":
        raise ArsenalError("Risk can only be accepted for a reviewed current revision")
    gate = compute_gate(state, args.track, args.phase)
    issue_key = args.issue_key.strip()
    if issue_key not in {item["issue_key"] for item in gate["issues"]}:
        raise ArsenalError(f"Unknown issue_key: {issue_key}")
    if not args.reason.strip():
        raise ArsenalError("Accepted risk needs a reason")
    if not str(args.confirmed_by).strip():
        raise ArsenalError("Accepted risk needs confirmed_by")
    duplicate = any(
        isinstance(risk, dict)
        and risk.get("track") == args.track
        and risk.get("phase") == args.phase
        and risk.get("revision") == phase["revision"]
        and risk.get("issue_key") == issue_key
        for risk in state.get("accepted_risks", [])
    )
    if duplicate:
        raise ArsenalError(f"Risk already accepted for this revision: {issue_key}")
    state.setdefault("accepted_risks", []).append(
        {
            "track": args.track,
            "phase": args.phase,
            "revision": phase["revision"],
            "issue_key": issue_key,
            "reason": args.reason.strip(),
            "confirmed_by": str(args.confirmed_by).strip(),
            "accepted_at": utc_now(),
        }
    )
    record_event(
        state,
        "risk.accepted",
        track=args.track,
        phase=args.phase,
        revision=phase["revision"],
        issue_key=issue_key,
    )
    save_workspace(args.workspace, state)
    return {
        "ok": True,
        "issue_key": issue_key,
        "gate": compute_gate(state, args.track, args.phase),
    }


def command_approve(args: argparse.Namespace) -> dict:
    """Approve a reviewed, current revision whose prerequisites and gate pass."""

    state = load_workspace(args.workspace)
    require_predecessors_approved(state, args.track, args.phase)
    phase = get_phase(state, args.track, args.phase)
    if not phase.get("revision"):
        raise ArsenalError("Cannot approve an untouched phase")
    if phase.get("status") == "stale" or phase.get("stale_reason"):
        raise ArsenalError("Cannot approve stale content; re-apply and re-review the phase")
    if phase.get("status") != "in_review":
        raise ArsenalError("Phase must be in review before approval")
    expected_inputs = upstream_revisions(state, args.track, args.phase)
    if phase.get("input_revisions", {}) != expected_inputs:
        raise ArsenalError("Phase inputs changed; re-apply and re-review the phase")
    if phase.get("data_hash") != checksum(phase.get("data", {})):
        raise ArsenalError("Phase data changed outside the apply flow")
    gate = compute_gate(state, args.track, args.phase)
    if not gate["review_requirement_met"]:
        raise ArsenalError(
            f"Need {gate['minimum_reviewers']} independent reviewers before approval"
        )
    if not gate["can_approve"]:
        raise ArsenalError(
            "Blocked by: " + ", ".join(item["issue_key"] for item in gate["critical_open"])
        )

    phase.update(status="approved", approved_at=utc_now(), stale_reason=None)
    order = phase_order(args.track)
    index = order.index(args.phase)
    next_phase = order[index + 1] if index + 1 < len(order) else None
    state["tracks"][args.track]["current_phase"] = next_phase or args.phase
    record_event(
        state,
        "phase.approved",
        track=args.track,
        phase=args.phase,
        revision=phase["revision"],
        next_phase=next_phase,
    )
    save_workspace(args.workspace, state)
    return {"ok": True, "track": args.track, "phase": args.phase, "next": next_phase}


def command_render(args: argparse.Namespace) -> dict:
    """Validate and render selected deterministic workspace views."""

    state = load_workspace(args.workspace)
    findings = validate_workspace(state)
    output_dir = args.output_dir or str(Path(args.workspace).parent)
    outputs = render_all(state, output_dir, args.surface, args.allow_invalid)
    state["render"].update(last_rendered_at=utc_now(), outputs=outputs)
    save_workspace(args.workspace, state)
    return {"ok": True, "outputs": outputs, "validation_findings": findings}


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface shared by supported harnesses."""

    parser = argparse.ArgumentParser(
        description="Manage a declarative growth-arsenal workspace"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--workspace", required=True)
    init.add_argument("--project", required=True)
    init.add_argument("--name")
    init.add_argument("--locale", default="en-GB")
    init.add_argument("--currency", default="USD")
    init.add_argument("--spelling", choices=["british", "american"], default="british")
    init.add_argument("--timezone", default="UTC")
    init.add_argument("--force", action="store_true")
    for name in ("apply", "add-review", "gate", "approve", "accept-risk"):
        command = commands.add_parser(name)
        command.add_argument("--workspace", required=True)
        command.add_argument("--track", default="offer", choices=sorted(TRACKS))
        command.add_argument("--phase", required=True)
        if name in {"apply", "add-review"}:
            command.add_argument("--input", required=True)
        if name == "accept-risk":
            command.add_argument("--issue-key", required=True)
            command.add_argument("--reason", required=True)
            command.add_argument("--confirmed-by", default="user")
    for name in ("status", "validate"):
        command = commands.add_parser(name)
        command.add_argument("--workspace", required=True)
    render = commands.add_parser("render")
    render.add_argument("--workspace", required=True)
    render.add_argument(
        "--surface",
        default="all",
        choices=["all", "offer-summary", "workshop-progress", "research-dashboard"],
    )
    render.add_argument("--output-dir")
    render.add_argument("--allow-invalid", action="store_true")
    return parser


def emit(value: dict) -> None:
    """Write a stable JSON result to stdout."""

    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    """Dispatch the requested CLI command and return a process exit code."""

    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            result, code = command_init(args), 0
        elif args.command == "apply":
            result, code = command_apply(args), 0
        elif args.command == "add-review":
            result, code = command_add_review(args), 0
        elif args.command == "gate":
            result = compute_gate(load_workspace(args.workspace), args.track, args.phase)
            code = 0 if result["can_approve"] else 1
        elif args.command == "accept-risk":
            result, code = command_accept_risk(args), 0
        elif args.command == "approve":
            result, code = command_approve(args), 0
        elif args.command == "status":
            state = load_workspace(args.workspace)
            findings = validate_workspace(state)
            result = {
                "ok": not any(item["level"] == "error" for item in findings),
                "project": state.get("project", {}),
                "current": {
                    key: value.get("current_phase")
                    for key, value in state.get("tracks", {}).items()
                },
                "findings": findings,
            }
            code = 0 if result["ok"] else 1
        elif args.command == "validate":
            findings = validate_workspace(load_workspace(args.workspace))
            result = {
                "ok": not any(item["level"] == "error" for item in findings),
                "findings": findings,
            }
            code = 0 if result["ok"] else 1
        elif args.command == "render":
            result, code = command_render(args), 0
        else:
            raise ArsenalError(f"Unknown command: {args.command}")
        emit(result)
        return code
    except (ArsenalError, RuntimeError) as exc:
        emit({"ok": False, "error": str(exc)})
        return 2


load_state = load_workspace
atomic_write_text = __import__("workspace").atomic_write
validate_state = validate_workspace


if __name__ == "__main__":
    raise SystemExit(main())
