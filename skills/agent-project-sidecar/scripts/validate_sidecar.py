#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = ["AGENTS.md", "README.md", "WORKFLOW.md", "plan.config.json", "index.json"]
REQUIRED_DIRS = ["items", "decisions", "plans", "runs", "handoffs", "templates"]
REQUIRED_TEMPLATES = ["item.md", "plan.md", "decision.md", "run.md", "handoff.md"]
SENSITIVE_FILENAME_PARTS = [".env", "cookie", "secret", "private-key", "id_rsa", "credentials"]
ASSIGNMENT_SECRET = re.compile(
    r"(?i)(api[_-]?key|token|password|passwd|secret|cookie|jwt)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"
)
USER_HOME_PATH = re.compile(r"/Users/[^/\s]+|/home/[^/\s]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a project sidecar repository.")
    parser.add_argument("sidecar_path", help="Path to the sidecar repository.")
    return parser.parse_args()


def iter_scannable_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.name == ".gitkeep":
            continue
        if path.suffix.lower() not in {".md", ".json", ".txt", ".yaml", ".yml"} and path.name != ".gitignore":
            continue
        yield path


def main() -> int:
    args = parse_args()
    root = Path(args.sidecar_path).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists() or not root.is_dir():
        errors.append(f"Sidecar path is not a directory: {root}")
    else:
        for filename in REQUIRED_FILES:
            if not (root / filename).is_file():
                errors.append(f"Missing required file: {filename}")
        for dirname in REQUIRED_DIRS:
            if not (root / dirname).is_dir():
                errors.append(f"Missing required directory: {dirname}")
        for template in REQUIRED_TEMPLATES:
            if not (root / "templates" / template).is_file():
                errors.append(f"Missing required template: templates/{template}")
        if (root / ".agent-workspace" / "manifest.json").exists():
            errors.append("Sidecar must not include .agent-workspace/manifest.json by default.")

    config_path = root / "plan.config.json"
    config = {}
    if config_path.is_file():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid plan.config.json: {exc}")

    main_repo = config.get("mainRepo")
    if isinstance(main_repo, str) and main_repo:
        candidate = (root / main_repo).resolve()
        if root == candidate or candidate in root.parents:
            errors.append("plan.config.json mainRepo must not point inside the sidecar.")
        if candidate == root or root in candidate.parents:
            errors.append("Sidecar must not be nested inside the main repository.")
    elif config_path.is_file():
        errors.append("plan.config.json must include mainRepo.")

    if config_path.is_file():
        executable = config.get("executableStatuses")
        if executable != ["ready", "running"]:
            warnings.append("Recommended executableStatuses is exactly ['ready', 'running'].")
        if config.get("sidecarKind") != "agent-project-sidecar":
            errors.append("plan.config.json sidecarKind must be agent-project-sidecar.")

    index_path = root / "index.json"
    if index_path.is_file():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
            items = index.get("items")
            if not isinstance(items, list):
                errors.append("index.json field items must be an array.")
            else:
                allowed_statuses = set(config.get("itemStatuses", []))
                executable_statuses = set(config.get("executableStatuses", ["ready", "running"]))
                for idx, item in enumerate(items):
                    if not isinstance(item, dict):
                        errors.append(f"index.json items[{idx}] must be an object.")
                        continue
                    item_id = item.get("id")
                    status = item.get("status")
                    if not isinstance(item_id, str) or not item_id:
                        errors.append(f"index.json items[{idx}] must include id.")
                    if status not in allowed_statuses:
                        errors.append(f"index.json item {item_id or idx} has invalid status: {status}")
                    if status in executable_statuses and not item.get("plan"):
                        warnings.append(f"Executable item {item_id or idx} should include a linked plan.")
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid index.json: {exc}")

    for run_file in (root / "runs").glob("*.md") if (root / "runs").is_dir() else []:
        if run_file.name == ".gitkeep":
            continue
        content = run_file.read_text(encoding="utf-8", errors="replace")
        for marker in ["Item ID", "Source Commit", "Validation"]:
            if marker not in content:
                warnings.append(f"{run_file.relative_to(root)} should include {marker}.")

    for path in iter_scannable_files(root):
        rel = path.relative_to(root)
        lower_name = path.name.lower()
        if any(part in lower_name for part in SENSITIVE_FILENAME_PARTS):
            errors.append(f"Sensitive-looking filename in sidecar: {rel}")
        text = path.read_text(encoding="utf-8", errors="replace")
        if ASSIGNMENT_SECRET.search(text):
            errors.append(f"Sensitive-looking assignment in {rel}")
        if USER_HOME_PATH.search(text):
            warnings.append(f"Local absolute user-home path found in {rel}")

    if errors:
        print("Sidecar validation failed:")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print("Sidecar validation passed.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
