# Agent Docs Maintenance Matrix

Update documentation only when behavior, ownership, constraints, or reusable knowledge changes.

| Change | Primary owner | Secondary review |
| --- | --- | --- |
| Project purpose, setup, or primary usage | `README.md` | `docs/README.md` |
| Mandatory agent rule or safety boundary | `AGENTS.md` | `docs/agents/workflow.md` |
| Documentation navigation | `docs/README.md` | Subtree README files |
| Human development, configuration, deployment, or maintenance flow | Matching file under `docs/developers/` | `docs/developers/README.md` |
| Repository shape, module ownership, service boundary, or data flow | `docs/agents/project-map.md` | Human architecture documentation |
| Agent execution, validation, tool routing, or handoff | `docs/agents/workflow.md` | `AGENTS.md` if mandatory |
| Required terminal, browser, CI, or external execution capability | `docs/agents/runtime-requirements.md` | `workflow.md` |
| Public/private storage or sanitization policy | `docs/agents/disclosure-policy.md` | `AGENTS.md` if mandatory |
| Confirmed reusable runtime or tooling failure | `docs/agents/runtime-playbook.md` | `failure-index.md`, then `memory.json` if stable |
| Stable architecture constraint or recurring failure | `docs/agents/memory.json` | Owning prose document |
| Reusable learning from completed work | `docs/agents/execution-log.md` | Link to stable memory or playbook |
| Routine implementation with no new reusable knowledge | No Agent Docs update | Validate existing docs only if affected |

## Adjacent Sidecar Coordination

When a real development project uses an adjacent `agent-project-sidecar` repository:

- Keep sidecar discovery, executable-status gates, and commit-trailer rules in `AGENTS.md` and `docs/agents/workflow.md` when they are mandatory for agents.
- Keep plan/RM execution records in the sidecar `runs/` directory, not in `docs/agents/execution-log.md`.
- Update `docs/agents/execution-log.md` only when a sidecar-backed task creates reusable project learning, recurring failure knowledge, or a lasting maintenance rule.
- Promote sidecar decisions into `docs/developers/*`, `docs/agents/*`, or `memory.json` only after they become durable project facts.
- Do not initialize Agent Docs full contract inside the sidecar unless it has become a real development project in its own right.

## Promotion threshold

Before adding agent memory, require all of the following:

1. The knowledge is useful beyond the current task.
2. The observation is confirmed rather than speculative.
3. The content belongs to the public project contract.
4. Private and environment-specific values are removed.
5. The owning document does not already contain the rule.

Recurrence supports usefulness but does not prove disclosure safety.

## Review questions

- Did a public behavior or developer workflow actually change?
- Would a future agent make a wrong decision without this update?
- Is this rule already owned elsewhere?
- Can the update be a link instead of duplicated prose?
- Is the observation stable across machines and sessions?
- Does the diff include private paths, identities, credentials, or raw output?
