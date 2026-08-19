# Agent Docs Coordination

Use this reference when a sidecar-enabled project also uses Agent Docs or Agent Workspace.

## Ownership Model

Agent Workspace belongs to the main repository. It owns manifest-declared local tooling, runtime profiles, local/raw/quarantine state, and conformance checks.

Agent Docs belongs to the main development project. It owns durable project knowledge, agent workflow, reusable failure memory, developer documentation, and promotion rules.

Agent Project Sidecar belongs beside the main repository. It owns plan/RM-bound items, decisions, executable plans, run records, validation summaries, and handoffs.

## Sidecar Is Not Agent Docs

Do not describe a sidecar as a minimal Agent Docs workspace. Sidecar documentation may borrow Agent Docs principles, but its lightweight structure belongs to the Agent Project Sidecar contract.

Agent Docs should not adapt its full contract for sidecars. If Agent Docs is run inside a repository with `plan.config.json` and `sidecarKind: agent-project-sidecar`, it should report that the repository is out of scope and route the user to Agent Project Sidecar.

## Sidecar Is Not Agent Workspace

Do not initialize `.agent-workspace/` inside a sidecar by default. Runtime profiles, local/raw/quarantine state, and workspace conformance belong to the main repository.

Consider Agent Workspace for a sidecar only if that sidecar becomes a real development project with its own runtime, tooling, and conformance needs.

## execution-log.md vs runs/

Use sidecar `runs/` for plan/RM-bound execution traceability:

- item/RM ID;
- linked plan;
- source commit;
- changed paths;
- validation commands and outcomes;
- skipped checks and reasons;
- residual risks;
- follow-up or handoff.

Use main-repo `docs/agents/execution-log.md` only for reusable project learning:

- stable maintenance lessons;
- recurring failure patterns;
- lasting validation or tool-routing rules;
- context for `memory.json`, `failure-index.md`, or `runtime-playbook.md`.

Do not copy run records into `execution-log.md`. Link a sidecar item or run only when it explains reusable learning.

## decisions/ Promotion

Use sidecar `decisions/` for planning decisions, demand/RM tradeoffs, execution priority, split strategy, and temporary direction.

Promote a sidecar decision only after it becomes durable project knowledge:

- product architecture, implementation, configuration, deployment, or maintenance behavior -> `docs/developers/*`;
- agent workflow, validation, tooling, or disclosure behavior -> `AGENTS.md` or `docs/agents/*`;
- machine-readable stable constraints or recurring failure indexes -> `docs/agents/memory.json`.

## Language

Keep sidecar `AGENTS.md` in English by default because it is an agent-facing operational contract.

Make plan/RM documents and templates language-configurable. For Chinese-first projects, generate Chinese `README.md`, `WORKFLOW.md`, item, plan, decision, run, and handoff templates while preserving English keywords such as `status`, `sourceCommit`, `validation`, `Plan-Item`, and `Related-Plan`.
