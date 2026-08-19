# Agent Guide

This repository publishes reusable Codex skills. Keep the repository focused on open-source skill content, not local Codex state.

## Rules

- Skill folders live under `skills/<skill-name>/`.
- Keep each skill folder valid as a standalone Codex skill.
- Keep `SKILL.md` and `agents/openai.yaml` aligned with the corresponding local Codex skill when intentionally releasing updates.
- Do not commit private local Codex configuration, account state, credentials, tokens, raw logs, or machine-specific paths.
- Do not add generated caches such as `__pycache__/`, `.DS_Store`, build output, or package-manager caches.
- Prefer small, reviewable changes scoped to one skill unless the change is explicitly cross-skill.
- Run `./scripts/validate-skills.sh` before committing when skill files or scripts change.

## Release Boundary

This repository is the upstream open-source baseline. Local installed copies in `~/.codex/skills` may diverge for user-specific customization. When syncing from local Codex back to this repository, copy only reusable public behavior.

