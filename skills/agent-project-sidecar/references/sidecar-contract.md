# Sidecar Contract

## Boundary

A project sidecar is an adjacent repository that stores development-process state for a main source repository.

Default layout:

```text
parent/
  project/
  project.plan/
```

The main repository owns:

- product source and deployable artifacts;
- public product documentation;
- runtime configuration templates;
- tests, CI, migrations, and generated type sources;
- project-specific agent instructions.

The sidecar owns:

- planning board index;
- work item details;
- decision records;
- executable plans;
- execution and validation records;
- handoffs between agents or maintainers.

## Required Files

```text
project.plan/
  AGENTS.md
  README.md
  WORKFLOW.md
  plan.config.json
  index.json
  items/
  decisions/
  plans/
  runs/
  handoffs/
  templates/
```

`plan.config.json` is the machine-readable contract. Keep paths relative where possible.

Recommended shape:

```json
{
  "projectName": "project",
  "mainRepo": "../project",
  "sidecarKind": "agent-project-sidecar",
  "statusCommand": "pnpm --silent plan:status --json",
  "itemPrefix": "PROJ",
  "language": "zh",
  "itemStatuses": ["discussing", "needs-decision", "decided", "ready", "running", "blocked", "done"],
  "executableStatuses": ["ready", "running"],
  "commitTrailers": ["Plan-Item", "Related-Plan", "Source-Commit"]
}
```

`index.json` is the fast-loading board index. It should contain item metadata and paths, not full plans or raw logs.

## Main Repository Integration

Add a short sidecar section to the main repository's agent instructions:

- sidecar path;
- status command, if available;
- executable status gate;
- disclosure boundary;
- commit trailer convention;
- rule to avoid standalone planning churn commits unless requested.

If the main repository has a package script system, expose a status command there. Keep it a thin wrapper around the sidecar index so agents do not need to remember sidecar internals.

## Templates And Language

Keep `AGENTS.md` in English by default because it is the agent-facing operational contract.

Use `templates/` to standardize item, plan, decision, run, and handoff writing. The initializer supports `--language zh|en`; for Chinese-first projects, generate Chinese planning templates while preserving English machine-readable field names and keywords.

## Commit Linkage

Use `Plan-Item: <id>` when a main-repo commit directly executes a sidecar item.

Use `Related-Plan: <id>` when a main-repo commit is related to an item but does not directly execute it.

Use `Source-Commit: <sha>` in sidecar commits when the related main-repo commit is already known.

Do not put private local paths, identities, raw logs, or secret values in commit messages.

## Customization

Projects may add extra directories, statuses, or commands, but should preserve the core boundary:

- sidecar for planning and execution records;
- main repository for product source and public docs;
- ignored/private storage for local or raw observations.

Do not add `.agent-workspace/manifest.json` to a sidecar by default. Agent Workspace belongs to the main development repository unless the sidecar becomes a real development project.
