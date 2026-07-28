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
    ArsenalError,
    TRACKS,
    compute_gate,
    deep_merge,
    get_phase,
    invalidate_downstream,
    load_workspace,
    new_workspace,
    read_json,
    record_event,
    save_workspace,
    upstream_revisions,
    utc_now,
    validate_review,
    validate_workspace,
)


def command_init(args: argparse.Namespace) -> dict:
    path = Path(args.workspace)
    if path.exists() and not args.force:
        raise ArsenalError(f"Workspace exists: {path}")
    state = new_workspace(args.project, args.name, args.locale, args.currency, args.spelling, args.timezone)
    record_event(state, "workspace.initialised", project=state["project"]["slug"])
    save_workspace(path, state)
    return {"ok": True, "workspace": str(path), "project": state["project"], "next": "offer:discovery"}


def command_apply(args: argparse.Namespace) -> dict:
    state = load_workspace(args.workspace)
    payload = read_json(args.input)
    if not isinstance(payload, dict):
        raise ArsenalError("Phase payload must be an object")
    phase = get_phase(state, args.track, args.phase)
    phase.update(
        revision=phase["revision"] + 1,
        status="draft",
        summary=str(payload.get("summary", "")).strip(),
        data=copy.deepcopy(payload.get("data", payload.get("phase_data", {}))),
        evidence_refs=copy.deepcopy(payload.get("evidence_refs", [])),
        reviews=[],
        approved_at=None,
        input_revisions=upstream_revisions(state, args.track, args.phase),
        stale_reason=None,
    )
    from workspace import checksum
    phase["data_hash"] = checksum(phase["data"])
    if isinstance(payload.get("research_patch"), dict):
        state["research"] = deep_merge(state.get("research", {}), payload["research_patch"])
    invalidated = invalidate_downstream(state, args.track, args.phase)
    state["tracks"][args.track]["current_phase"] = args.phase
    record_event(state, "phase.applied", track=args.track, phase=args.phase, revision=phase["revision"], invalidated=invalidated)
    save_workspace(args.workspace, state)
    return {"ok": True, "track": args.track, "phase": args.phase, "revision": phase["revision"], "invalidated": invalidated}


def command_add_review(args: argparse.Namespace) -> dict:
    state = load_workspace(args.workspace)
    payload = read_json(args.input)
    reviews = payload if isinstance(payload, list) else [payload]
    phase = get_phase(state, args.track, args.phase)
    for review in reviews:
        validate_review(review)
        item = copy.deepcopy(review)
        item["reviewer"] = item["reviewer"].strip()
        item["submitted_at"] = item.get("submitted_at") or utc_now()
        phase.setdefault("reviews", []).append(item)
    phase["status"] = "in_review"
    record_event(state, "review.added", track=args.track, phase=args.phase, count=len(reviews))
    save_workspace(args.workspace, state)
    return {"ok": True, "added": len(reviews), "gate": compute_gate(state, args.track, args.phase)}


def command_accept_risk(args: argparse.Namespace) -> dict:
    state = load_workspace(args.workspace)
    gate = compute_gate(state, args.track, args.phase)
    if args.issue_key not in {item["issue_key"] for item in gate["issues"]}:
        raise ArsenalError(f"Unknown issue_key: {args.issue_key}")
    if not args.reason.strip():
        raise ArsenalError("Accepted risk needs a reason")
    state.setdefault("accepted_risks", []).append(
        {
            "track": args.track,
            "phase": args.phase,
            "issue_key": args.issue_key,
            "reason": args.reason.strip(),
            "confirmed_by": args.confirmed_by,
            "accepted_at": utc_now(),
        }
    )
    record_event(state, "risk.accepted", track=args.track, phase=args.phase, issue_key=args.issue_key)
    save_workspace(args.workspace, state)
    return {"ok": True, "issue_key": args.issue_key, "gate": compute_gate(state, args.track, args.phase)}


def command_approve(args: argparse.Namespace) -> dict:
    state = load_workspace(args.workspace)
    phase = get_phase(state, args.track, args.phase)
    gate = compute_gate(state, args.track, args.phase)
    if not phase["revision"]:
        raise ArsenalError("Cannot approve an untouched phase")
    if not gate["can_approve"]:
        raise ArsenalError("Blocked by: " + ", ".join(item["issue_key"] for item in gate["critical_open"]))
    from workspace import checksum, phase_order
    phase.update(status="approved", approved_at=utc_now(), input_revisions=upstream_revisions(state, args.track, args.phase), data_hash=checksum(phase.get("data", {})), stale_reason=None)
    order = phase_order(args.track)
    index = order.index(args.phase)
    next_phase = order[index + 1] if index + 1 < len(order) else None
    state["tracks"][args.track]["current_phase"] = next_phase or args.phase
    record_event(state, "phase.approved", track=args.track, phase=args.phase, revision=phase["revision"], next_phase=next_phase)
    save_workspace(args.workspace, state)
    return {"ok": True, "track": args.track, "phase": args.phase, "next": next_phase}


def command_render(args: argparse.Namespace) -> dict:
    state = load_workspace(args.workspace)
    findings = validate_workspace(state)
    output_dir = args.output_dir or str(Path(args.workspace).parent)
    outputs = render_all(state, output_dir, args.surface, args.allow_invalid)
    state["render"].update(last_rendered_at=utc_now(), outputs=outputs)
    save_workspace(args.workspace, state)
    return {"ok": True, "outputs": outputs, "validation_findings": findings}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a declarative growth-arsenal workspace")
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
    render.add_argument("--surface", default="all", choices=["all", "offer-summary", "workshop-progress", "research-dashboard", "leads-blueprint", "tracking-dashboard"])
    render.add_argument("--output-dir")
    render.add_argument("--allow-invalid", action="store_true")
    return parser


def emit(value: dict) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
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
            result = {"ok": not any(item["level"] == "error" for item in findings), "project": state.get("project", {}), "current": {key: value.get("current_phase") for key, value in state.get("tracks", {}).items()}, "findings": findings}
            code = 0 if result["ok"] else 1
        elif args.command == "validate":
            findings = validate_workspace(load_workspace(args.workspace))
            result = {"ok": not any(item["level"] == "error" for item in findings), "findings": findings}
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
