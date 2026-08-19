#!/usr/bin/env python3
"""Initialize and validate the Agent Docs project documentation contract."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


AGENT_FILES = (
    "README.md",
    "workflow.md",
    "project-map.md",
    "runtime-requirements.md",
    "disclosure-policy.md",
    "runtime-playbook.md",
    "failure-index.md",
    "execution-log.md",
    "memory.json",
)
REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "docs/README.md",
    "docs/developers/README.md",
    *(f"docs/agents/{name}" for name in AGENT_FILES),
)
SIDECAR_KIND = "agent-project-sidecar"
PRIVATE_MARKERS = (
    ".agent-workspace/local/",
    ".agent-workspace/raw/",
    ".agent-workspace/quarantine/",
)
SENSITIVE_PATTERNS = (
    ("macOS user-home path", re.compile(r"/Users/(?!<user>/|\$USER/)[^/\s`]+/")),
    ("Linux user-home path", re.compile(r"/home/(?!<user>/|\$USER/)[^/\s`]+/")),
    ("Windows user-home path", re.compile(r"[A-Za-z]:\\Users\\(?!<user>\\|%USERNAME%\\)[^\\\s`]+\\")),
    ("credential-bearing URL", re.compile(r"https?://[^/\s:@]+:[^@\s]+@")),
    ("private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def detect_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    return Path.cwd().resolve()


def template_root() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "project-template"


def missing_files(root: Path) -> list[str]:
    return [relative for relative in REQUIRED_FILES if not (root / relative).is_file()]


def sidecar_kind(root: Path) -> str | None:
    config = root / "plan.config.json"
    if not config.is_file():
        return None
    try:
        value = json.loads(config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    kind = value.get("sidecarKind")
    return kind if isinstance(kind, str) else None


def is_agent_project_sidecar(root: Path) -> bool:
    return sidecar_kind(root) == SIDECAR_KIND


def print_sidecar_notice(root: Path) -> None:
    print(f"[agent-docs] root: {root}")
    print("[agent-docs] out of scope: detected agent-project-sidecar repository")
    print("[agent-docs] use the agent-project-sidecar skill for sidecar structure, templates, and validation")


def tracked_private_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [
        path
        for path in result.stdout.splitlines()
        if any(path.startswith(marker) for marker in PRIVATE_MARKERS)
    ]


def public_files(root: Path) -> list[Path]:
    files = [root / "README.md", root / "AGENTS.md", root / "docs" / "README.md"]
    for directory in (root / "docs" / "agents", root / "docs" / "developers"):
        if directory.is_dir():
            files.extend(path for path in directory.rglob("*") if path.is_file())
    return [path for path in files if path.is_file()]


def validation_errors(root: Path) -> list[str]:
    errors = [f"Missing required file: {path}" for path in missing_files(root)]

    memory = root / "docs" / "agents" / "memory.json"
    if memory.is_file():
        try:
            value = json.loads(memory.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                errors.append("docs/agents/memory.json must contain a JSON object")
            else:
                declared_version = value.get("schema_version", value.get("version"))
                if not isinstance(declared_version, int) or declared_version < 1:
                    errors.append(
                        "docs/agents/memory.json must declare a positive integer schema_version or version"
                    )
                for key in ("architecture_constraints", "known_failures"):
                    if not isinstance(value.get(key), list):
                        errors.append(f"docs/agents/memory.json field {key} must be an array")
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Invalid docs/agents/memory.json: {error}")

    agent_index = root / "docs" / "agents" / "README.md"
    if agent_index.is_file():
        content = agent_index.read_text(encoding="utf-8")
        for name in AGENT_FILES[1:]:
            if name not in content:
                errors.append(f"docs/agents/README.md does not reference {name}")

    docs_index = root / "docs" / "README.md"
    if docs_index.is_file():
        content = docs_index.read_text(encoding="utf-8")
        for marker in ("agents", "developers"):
            if marker not in content:
                errors.append(f"docs/README.md does not route to docs/{marker}/")

    for path in public_files(root):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SENSITIVE_PATTERNS:
            if pattern.search(content):
                errors.append(f"{path.relative_to(root)} contains a {label}")

    for path in tracked_private_files(root):
        errors.append(f"Private Agent Workspace state is tracked: {path}")
    return errors


def command_status(root: Path) -> int:
    if is_agent_project_sidecar(root):
        print_sidecar_notice(root)
        return 0
    missing = missing_files(root)
    print(f"[agent-docs] root: {root}")
    print(f"[agent-docs] required files: {len(REQUIRED_FILES) - len(missing)}/{len(REQUIRED_FILES)}")
    if missing:
        for path in missing:
            print(f"  missing: {path}")
    else:
        print("[agent-docs] structure: complete")
    return 0


def command_init(root: Path, dry_run: bool) -> int:
    if is_agent_project_sidecar(root):
        print_sidecar_notice(root)
        print("[agent-docs] init skipped: full Agent Docs contract is for real development projects")
        return 0
    source = template_root()
    if not source.is_dir():
        print(f"[agent-docs] template unavailable: {source}", file=sys.stderr)
        return 1
    created: list[str] = []
    skipped: list[str] = []
    for template in sorted(path for path in source.rglob("*") if path.is_file()):
        relative = template.relative_to(source)
        target = root / relative
        if target.exists():
            skipped.append(str(relative))
            continue
        created.append(str(relative))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(template, target)
    action = "would create" if dry_run else "created"
    print(f"[agent-docs] {action} {len(created)} file(s); preserved {len(skipped)} existing file(s)")
    for path in created:
        print(f"  {action}: {path}")
    return 0


def command_validate(root: Path) -> int:
    if is_agent_project_sidecar(root):
        print_sidecar_notice(root)
        print("[agent-docs] validate skipped: this repository is governed by the sidecar contract")
        return 0
    errors = validation_errors(root)
    if errors:
        print(f"[agent-docs] validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"[agent-docs] PASS: {len(REQUIRED_FILES)} required files and disclosure checks")
    return 0


def changed_files(root: Path, staged: bool) -> list[tuple[str, str]]:
    command = ["git", "diff", "--name-status"]
    if staged:
        command.append("--cached")
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    changes: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            changes.append((parts[0], parts[-1]))
    return changes


def command_audit(root: Path, staged: bool) -> int:
    if is_agent_project_sidecar(root):
        print_sidecar_notice(root)
        print("[agent-docs] audit skipped: plan-bound records belong to the sidecar workflow")
        return 0
    try:
        changes = changed_files(root, staged)
    except RuntimeError as error:
        print(f"[agent-docs] audit unavailable: {error}", file=sys.stderr)
        return 1
    if not changes:
        print("[agent-docs] no changed files to audit")
        return 0

    paths = [path for _, path in changes]
    recommendations: set[str] = set()
    if any(status.startswith(("A", "D", "R")) for status, _ in changes):
        if any(not path.startswith("docs/") for path in paths):
            recommendations.add("Review docs/agents/project-map.md for repository-shape or ownership drift.")
    if any(
        path.startswith(("scripts/", ".github/"))
        or path.endswith(("package.json", "pyproject.toml", "Cargo.toml", "go.mod"))
        or "config" in Path(path).name.lower()
        for path in paths
    ):
        recommendations.add("Review workflow.md, runtime-requirements.md, and relevant developer docs.")
    if "AGENTS.md" in paths:
        recommendations.add("Review docs/agents/workflow.md for procedural detail that should not be duplicated in AGENTS.md.")
    if any(path.startswith("docs/") for path in paths):
        recommendations.add("Check docs/README.md and subtree indexes for navigation drift.")

    print(f"[agent-docs] audited {len(changes)} changed file(s)")
    if recommendations:
        for recommendation in sorted(recommendations):
            print(f"  review: {recommendation}")
    else:
        print("[agent-docs] no documentation update is implied by filename-level heuristics")
    print("[agent-docs] audit is advisory; confirm semantic impact before editing documentation")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Project root; defaults to the current Git root or working directory")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status")
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--dry-run", action="store_true")
    subparsers.add_parser("validate")
    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    root = detect_root(args.root)

    if args.command == "status":
        return command_status(root)
    if args.command == "init":
        return command_init(root, args.dry_run)
    if args.command == "validate":
        return command_validate(root)
    if args.command == "audit":
        return command_audit(root, args.staged)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
