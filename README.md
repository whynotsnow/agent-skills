# Agent Skills

Open-source baseline for reusable Codex skills maintained by whynotsnow.

This repository currently contains three skills:

- `agent-docs`: maintain Agent Docs for real development projects.
- `agent-workspace`: operate Agent Workspace Spec projects and their local tooling boundary.
- `agent-project-sidecar`: create and maintain adjacent planning sidecar repositories.

## Repository Shape

```text
skills/
  agent-docs/
  agent-workspace/
  agent-project-sidecar/
scripts/
  validate-skills.sh
```

Each skill folder keeps the Codex skill layout:

```text
SKILL.md
agents/openai.yaml
references/
scripts/
assets/
```

Not every skill needs every optional directory, but the files committed here are intended to be enough for a working public skill installation.

## Source Of Truth

The files in this repository are the public baseline for these skills. The local Codex installation under `~/.codex/skills` should keep core files aligned with this repository when changes are intentionally released.

Local Codex copies do not need to be byte-for-byte identical forever. A user may install these skills, then change local instructions, add private defaults, or adapt scripts for their own workflow. Treat this repository as the upstream open-source version, and treat local installed skills as editable working copies.

## Validate

Run:

```bash
./scripts/validate-skills.sh
```

The script checks required skill entrypoints and compiles bundled Python helpers. It does not replace behavioral review of skill instructions.

## Install Locally

Copy a skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/agent-project-sidecar ~/.codex/skills/
```

Restart Codex or reload skills after installing or updating local copies.
