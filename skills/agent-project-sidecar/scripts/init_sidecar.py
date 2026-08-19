#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


STATUSES = [
    "discussing",
    "needs-decision",
    "decided",
    "ready",
    "running",
    "blocked",
    "done",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an adjacent project sidecar repository.")
    parser.add_argument("main_repo", help="Path to the main source repository.")
    parser.add_argument("--sidecar-path", help="Path for the sidecar. Defaults to ../<main>.plan.")
    parser.add_argument("--project-name", help="Project name. Defaults to the main repo folder name.")
    parser.add_argument("--item-prefix", help="Work item prefix. Defaults to the uppercased project slug.")
    parser.add_argument(
        "--language",
        choices=["zh", "en"],
        default="zh",
        help="Language for README, WORKFLOW, and plan/RM templates. AGENTS.md remains English.",
    )
    parser.add_argument(
        "--status-command",
        default="",
        help="Main-repo command that prints sidecar status, for example: pnpm --silent plan:status --json.",
    )
    parser.add_argument("--git", action="store_true", help="Run git init in the sidecar when it is newly created.")
    return parser.parse_args()


def write_text(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def copy_templates(sidecar: Path, language: str) -> None:
    source = skill_root() / "assets" / "templates" / language
    target = sidecar / "templates"
    target.mkdir(exist_ok=True)
    if not source.is_dir():
        return
    for template in sorted(source.glob("*.md")):
        destination = target / template.name
        if not destination.exists():
            shutil.copy2(template, destination)


def project_slug(name: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in name.lower()).strip("-") or "project"


def item_prefix(name: str) -> str:
    chars = [ch for ch in name.upper().replace("-", "_") if ch.isalnum() or ch == "_"]
    compact = "".join(chars).strip("_")
    if not compact:
        return "PROJ"
    parts = [part for part in compact.split("_") if part]
    if len(parts) > 1:
        acronym = "".join(part[0] for part in parts)
        return acronym[:12]
    return compact[:12]


def readme_content(project_name: str, language: str) -> str:
    if language == "en":
        return (
            f"# {project_name} Plan Sidecar\n\n"
            f"This repository stores plan/RM items, decisions, executable plans, run records, validation summaries, and handoffs for `{project_name}`.\n\n"
            "Product source, deployable files, runtime configuration, and durable project documentation stay in the main repository referenced by `plan.config.json`.\n"
        )
    return (
        f"# {project_name} Plan Sidecar\n\n"
        f"这个仓库保存 `{project_name}` 的 plan/RM items、decisions、executable plans、run records、validation summaries 和 handoffs。\n\n"
        "产品源码、部署文件、运行配置和长期项目文档保留在 `plan.config.json` 指向的主仓库中。\n"
    )


def workflow_content(language: str) -> str:
    if language == "en":
        return (
            "# Sidecar Workflow\n\n"
            "1. Capture unclear ideas as `discussing`.\n"
            "2. Move unresolved strategic questions to `needs-decision`.\n"
            "3. Record accepted direction as `decided`.\n"
            "4. Write executable work in `plans/` and mark the item `ready`.\n"
            "5. Mark active implementation as `running`.\n"
            "6. Record validation and changed paths in `runs/`.\n"
            "7. Mark complete work as `done`.\n"
        )
    return (
        "# Sidecar Workflow\n\n"
        "1. 将不清晰的想法记录为 `discussing`。\n"
        "2. 将需要维护者判断的问题转为 `needs-decision`。\n"
        "3. 将已接受的方向记录为 `decided`。\n"
        "4. 在 `plans/` 写入可执行计划，并将 item 标记为 `ready`。\n"
        "5. 实施中的工作标记为 `running`。\n"
        "6. 在 `runs/` 记录验证结果和变更路径。\n"
        "7. 工作完成且可追溯后标记为 `done`。\n"
    )


def main() -> int:
    args = parse_args()
    main_repo = Path(args.main_repo).expanduser().resolve()
    if not main_repo.exists() or not main_repo.is_dir():
        raise SystemExit(f"Main repository does not exist or is not a directory: {main_repo}")

    project_name = args.project_name or main_repo.name
    default_sidecar = main_repo.parent / f"{project_slug(project_name)}.plan"
    sidecar = Path(args.sidecar_path).expanduser() if args.sidecar_path else default_sidecar
    if not sidecar.is_absolute():
        sidecar = (Path.cwd() / sidecar).resolve()
    else:
        sidecar = sidecar.resolve()

    if sidecar == main_repo or main_repo in sidecar.parents:
        raise SystemExit("Sidecar must be outside the main repository.")

    created = not sidecar.exists()
    sidecar.mkdir(parents=True, exist_ok=True)

    for dirname in ["items", "decisions", "plans", "runs", "handoffs"]:
        directory = sidecar / dirname
        directory.mkdir(exist_ok=True)
        write_text(directory / ".gitkeep", "")
    copy_templates(sidecar, args.language)

    rel_main = Path("..") / main_repo.name if sidecar.parent == main_repo.parent else main_repo
    status_command = args.status_command or "pnpm --silent plan:status --json"

    config = {
        "projectName": project_name,
        "mainRepo": str(rel_main),
        "sidecarKind": "agent-project-sidecar",
        "statusCommand": status_command,
        "itemPrefix": args.item_prefix or item_prefix(project_name),
        "language": args.language,
        "itemStatuses": STATUSES,
        "executableStatuses": ["ready", "running"],
        "commitTrailers": ["Plan-Item", "Related-Plan", "Source-Commit"],
    }

    write_text(sidecar / "plan.config.json", json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    write_text(
        sidecar / "index.json",
        json.dumps({"projectName": project_name, "items": []}, indent=2, ensure_ascii=False) + "\n",
    )
    write_text(
        sidecar / ".gitignore",
        ".DS_Store\nnode_modules/\n.agent-workspace/local/\n.agent-workspace/raw/\n.agent-workspace/quarantine/\n",
    )
    write_text(
        sidecar / "README.md",
        readme_content(project_name, args.language),
    )
    write_text(
        sidecar / "AGENTS.md",
        f"# Agent Plan Guide\n\n"
        f"This is the sidecar planning repository for `{project_name}`.\n\n"
        "## Repository Boundary\n\n"
        "- Store planning, decision, execution, validation, and handoff records here.\n"
        "- Keep product source, runtime configuration, generated builds, and deployable files in the main repository.\n"
        "- Do not copy credentials, tokens, cookies, private keys, raw logs, local absolute paths, private URLs, hostnames, or personal identity data into tracked files.\n"
        "- Commit routine sidecar changes together with the related main-repo change unless the maintainer explicitly asks for a sidecar checkpoint.\n"
        "- Main-repo commits that directly execute a sidecar item must use `Plan-Item: <id>`. Related non-execution commits may use `Related-Plan: <id>`.\n\n"
        "## Workflow Rules\n\n"
        "- Only items with `status: ready` or `status: running` may trigger implementation in the main repository.\n"
        "- `needs-decision`, `discussing`, `decided`, and `blocked` items must not be implemented directly.\n"
        "- Record sanitized validation evidence in `runs/` after implementation.\n\n"
        "## File Ownership\n\n"
        "- `index.json` is the board index for fast loading.\n"
        "- `items/*.md` owns work item details.\n"
        "- `decisions/*.md` owns decision records.\n"
        "- `plans/*.md` owns executable plans.\n"
        "- `runs/*.md` owns execution and validation records.\n"
        "- `handoffs/*.md` owns continuation context.\n",
    )
    write_text(
        sidecar / "WORKFLOW.md",
        workflow_content(args.language),
    )

    if args.git and created:
        subprocess.run(["git", "init"], cwd=sidecar, check=True)

    print(f"Sidecar ready: {sidecar}")
    print(f"Main repository: {main_repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
