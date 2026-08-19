# Adoption Reference

Use this reference when initializing or migrating a repository to Agent Workspace Spec.

## Before Editing

Inspect existing files first:

- Public instruction files such as `AGENTS.md`, `README.md`, or project-specific agent guides.
- Existing `.agent-workspace/` or older `.agent-os/` directories.
- `.gitignore`
- Existing package-manager scripts, hooks, CI workflows, or maintenance docs.

Do not overwrite project-specific policy. Merge carefully or create a patch that preserves existing rules.

## Recommended Minimal Workspace

Create:

- `.agent-workspace/manifest.json`
- `.agent-workspace/README.md`
- `.agent-workspace/tools/` only when local implementation is desired
- ignored `.agent-workspace/local/`, `.agent-workspace/raw/`, `.agent-workspace/quarantine/`
- public agent docs or references selected by the project

Update `.gitignore` with the ignored local directories.

## Reference Tools

Templates in `assets/reference-workspace/` are generic starting points. They are not mandatory. If a project already has local tools, respect them and update only the manifest or docs needed for clarity.
