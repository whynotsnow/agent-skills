# Agent Guide

Read this file before changing the project.

## Start here

1. Read `README.md` for project purpose and setup.
2. Use `docs/README.md` to find audience-specific documentation.
3. Read `docs/agents/workflow.md` before non-trivial work.
4. Read `docs/agents/project-map.md` before architecture or data-flow changes.
5. Read relevant memory and playbooks before repeating known failures.

## Documentation boundaries

- Keep mandatory agent rules in this file concise.
- Keep detailed agent knowledge under `docs/agents/`.
- Keep human-facing development guidance under `docs/developers/`.
- Do not persist secrets, personal identities, absolute user-home paths, or raw logs in tracked documentation.
- Update documentation only when behavior, ownership, constraints, or reusable knowledge changes.

## Validation

Run the narrowest project checks relevant to the change. Never claim a command passed unless it actually ran successfully.
