# Migration Guide

Use this procedure to add sidecar planning to an existing project.

## 1. Inspect The Main Repository

Read:

- root agent instructions, usually `AGENTS.md`;
- documentation router, if present;
- package scripts or task commands;
- existing planning, roadmap, decision, or execution-log files.

Do not move existing project documentation into the sidecar automatically. Product documentation should usually remain in the main repository.

## 2. Choose The Sidecar Path

Default to `../<main-repo-name>.plan`.

Use another path only when the project already declares one or the maintainer requests it.

## 3. Initialize The Sidecar

Run:

```bash
python3 <skill-dir>/scripts/init_sidecar.py <main-repo-path> --git
```

Useful options:

```bash
--sidecar-path <path>
--project-name <name>
--item-prefix <prefix>
--status-command <command>
--language zh|en
```

If the target sidecar already exists, inspect it instead of overwriting it.

`AGENTS.md` remains English. The selected language controls `README.md`, `WORKFLOW.md`, and the item/plan/decision/run/handoff templates.

## 4. Connect The Main Repository

Add a concise sidecar section to the main repo agent instructions.

If the project has a script runner, add a status command that prints executable board state. For JavaScript projects, a thin `scripts/sidecar-status.mjs` wrapper around `../<project>.plan/index.json` is usually enough.

## 5. Validate

Run:

```bash
python3 <skill-dir>/scripts/validate_sidecar.py <sidecar-path>
```

Then run the main repository's narrow documentation or tooling checks required by its instructions.

## 6. First Item

Create the first item only when the maintainer asks for concrete planning work. Initial sidecar adoption does not need to invent backlog items.

Use the files under `templates/` when creating the first item, plan, decision, run, or handoff.
