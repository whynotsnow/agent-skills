#!/usr/bin/env python3
"""Operate on Agent Workspace Spec repositories without owning their tools."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_workspace(start: Path) -> Path | None:
    current = start.resolve()
    while True:
        if (current / ".agent-workspace" / "manifest.json").is_file():
            return current
        if current.parent == current:
            return None
        current = current.parent


def load_manifest(root: Path) -> dict:
    with (root / ".agent-workspace" / "manifest.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return json.load(handle)


def reject_absolute(value: str, label: str) -> None:
    if os.path.isabs(value):
        raise SystemExit(f"[agent-workspace-skill] {label} must be repository-relative")


def resolve_tool(root: Path, manifest: dict) -> tuple[str, Path]:
    tooling = manifest.get("tooling") or {}
    entry = tooling.get("entry")
    runtime = tooling.get("runtime")
    if not entry or not runtime:
        raise SystemExit("[agent-workspace-skill] manifest has no tooling entry/runtime")
    reject_absolute(entry, "tooling.entry")
    path = root / entry
    if not path.exists():
        raise SystemExit(f"[agent-workspace-skill] tooling entry not found: {entry}")
    return str(runtime), path


def command_for(runtime: str, entry: Path, args: list[str]) -> list[str]:
    if runtime == "node" or entry.suffix == ".mjs":
        node = shutil.which("node")
        if not node:
            raise SystemExit("[agent-workspace-skill] node runtime is unavailable")
        return [node, str(entry), *args]
    if runtime == "python" or entry.suffix == ".py":
        return [sys.executable, str(entry), *args]
    if runtime in {"bash", "sh"} or entry.suffix == ".sh":
        return [runtime if runtime in {"bash", "sh"} else "sh", str(entry), *args]
    return [str(entry), *args]


def status(args: argparse.Namespace) -> int:
    root = find_workspace(Path.cwd())
    if root is None:
        print("[agent-workspace-skill] No .agent-workspace/manifest.json found")
        return 1
    manifest = load_manifest(root)
    print(
        json.dumps(
            {
                "workspace_root": str(root),
                "spec": manifest.get("spec"),
                "spec_version": manifest.get("spec_version"),
                "conformance": manifest.get("conformance", []),
                "public_instructions": manifest.get("public_instructions"),
                "public_knowledge": manifest.get("public_knowledge"),
                "local_state": manifest.get("local_state"),
                "tooling": manifest.get("tooling", {}),
            },
            indent=2,
        )
    )
    return 0


def run(args: argparse.Namespace) -> int:
    root = find_workspace(Path.cwd())
    if root is None:
        print("[agent-workspace-skill] No .agent-workspace/manifest.json found")
        return 1
    manifest = load_manifest(root)
    runtime, entry = resolve_tool(root, manifest)
    command = command_for(runtime, entry, args.tool_args)
    result = subprocess.run(command, cwd=root)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("tool_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command == "status":
        return status(args)
    if args.command == "run":
        tool_args = args.tool_args
        if tool_args and tool_args[0] == "--":
            tool_args = tool_args[1:]
        args.tool_args = tool_args
        return run(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
