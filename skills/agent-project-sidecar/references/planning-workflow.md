# Planning Workflow

## Status Model

Recommended statuses:

| Status | Meaning | Implementation allowed |
| --- | --- | --- |
| `discussing` | Idea or unclear request under exploration | No |
| `needs-decision` | Maintainer decision required | No |
| `decided` | Direction accepted, but not yet executable | No |
| `ready` | Planned and available for implementation | Yes |
| `running` | Currently being executed | Yes |
| `blocked` | Cannot proceed without an external change or decision | No |
| `done` | Completed and recorded | No |

Only `ready` and `running` should trigger implementation by default.

## Item Lifecycle

1. Capture ideas as `discussing`.
2. Move unresolved strategic questions to `needs-decision`.
3. Record accepted direction as `decided`.
4. Write an executable plan in `plans/`.
5. Mark the item `ready`.
6. During implementation, mark it `running`.
7. After implementation, record validation in `runs/`.
8. Mark it `done` only when the result is complete and reviewable.

## File Ownership

- `items/<id>.md`: problem, scope, status, owner, linked plan, source documents, and acceptance criteria.
- `plans/<id>-plan.md`: executable sequence, risk notes, validation plan, and rollback notes.
- `decisions/<id>-<slug>.md`: decisions that should outlive a single item.
- `runs/<id>-<date>.md`: implementation summary, changed paths, commands, results, skipped validation, and source commit when known.
- `handoffs/<id>-<date>.md`: continuation context for another agent or maintainer.
- `templates/*.md`: writing templates for item, plan, decision, run, and handoff files.
- `index.json`: lightweight board index for status tools.

## Operating Procedure

When asked to use a sidecar item:

1. Read sidecar `AGENTS.md` and `plan.config.json`.
2. Load `index.json` or run the main repo status command.
3. Confirm the item status is executable.
4. Read the item and linked plan.
5. Read only source documents required by the item.
6. Work in the main repository.
7. Run the narrowest meaningful validation.
8. Update the sidecar run record with sanitized evidence.
9. Keep commits linked with the configured trailers when committing.

Do not implement non-executable statuses unless the maintainer explicitly instructs you to override the workflow.
