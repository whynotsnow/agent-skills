# Agent Workspace Spec Reference

Agent Workspace Spec defines a repository format for agent-facing instructions, reusable public memory, private local runtime state, and conformance validation. It does not define an agent runtime, model API, or network protocol.

## Required Manifest

A conformant workspace provides `.agent-workspace/manifest.json` with:

- `spec`: `agent-workspace`
- `spec_version`: supported semantic version
- `conformance`: one or more levels
- `public_instructions`: repository-relative instruction entry point
- `public_knowledge`: repository-relative public agent knowledge path
- `local_state`: repository-relative ignored local state path
- `tooling`: optional local implementation descriptor when local commands exist

All paths must be repository-relative. Do not put personal paths, home directories, hostnames, names, emails, tokens, or machine-specific command fragments in the manifest.

## Conformance Levels

- `core`: public instruction entry, version-controlled reusable knowledge, context loading order, and validation command.
- `disclosure`: separation between public, local, raw, quarantine, and secret material.
- `runtime`: public runtime requirements separate from detected machine/session state.
- `team`: opaque developer, machine, and session profiles; Git identity only as local matching input.

## Context Resolution

Resolve context in this order:

1. Public project policy and instructions.
2. Public project knowledge and runtime requirements.
3. Active local developer preferences.
4. Cached local machine state.
5. Current session state and direct capability detection.

Local layers may refine availability and preferences. They must not weaken public safety or disclosure rules.
