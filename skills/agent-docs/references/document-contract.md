# Agent Docs Document Contract

## Scope

Agent Docs full contract applies to real development projects, source repositories, and complete project-knowledge repositories.

It does not apply to adjacent planning sidecars or process-only repositories. If a repository declares `plan.config.json` with `sidecarKind: agent-project-sidecar`, do not treat the missing full Agent Docs tree as drift. Use the Agent Project Sidecar contract for that repository instead.

Sidecars may borrow Agent Docs principles such as clear entry points, ownership boundaries, low duplication, and disclosure safety, but that lightweight structure belongs to the sidecar's own contract, not to Agent Docs.

## Required structure

```text
README.md
AGENTS.md
docs/
├── README.md
├── agents/
│   ├── README.md
│   ├── workflow.md
│   ├── project-map.md
│   ├── runtime-requirements.md
│   ├── disclosure-policy.md
│   ├── runtime-playbook.md
│   ├── failure-index.md
│   ├── execution-log.md
│   └── memory.json
└── developers/
    └── README.md
```

Projects may add any other files or directories under `docs/`. Additional documents must have a defined audience and must not duplicate an existing owner's content.

## Ownership boundaries

| File | Owns | Must not own |
| --- | --- | --- |
| `README.md` | Project identity, value, setup, and primary usage | Agent-only rules and detailed maintenance playbooks |
| `AGENTS.md` | Concise mandatory rules for coding agents | Long tutorials, raw logs, and duplicated architecture guides |
| `docs/README.md` | Documentation navigation and audience routing | Detailed topic documentation |
| `docs/developers/README.md` | Human developer documentation index | Agent-only execution policy |
| `docs/agents/README.md` | Agent knowledge index and on-demand reading rules | Full copies of the indexed documents |
| `workflow.md` | Agent execution, validation, tool routing, and handoff | Project architecture details and failure histories |
| `project-map.md` | Repository shape, ownership, architecture boundaries, and data flow | Step-by-step runtime troubleshooting |
| `runtime-requirements.md` | Public execution capability requirements | Detected state of a particular machine or session |
| `disclosure-policy.md` | Public, local, raw, quarantine, and secret boundaries | Actual private values or runtime observations |
| `runtime-playbook.md` | Confirmed failure patterns, diagnosis, and reusable responses | Unverified guesses and full raw logs |
| `failure-index.md` | Short searchable pointers to known failure patterns | Duplicate copies of complete playbooks |
| `execution-log.md` | Completed work that teaches reusable project knowledge | Routine task history, status updates, or transcripts |
| `memory.json` | Machine-readable stable constraints and recurring failures | Ephemeral state, prose logs, or unreviewed observations |

## Duplication rules

- Put a rule in one owning document and link to it elsewhere.
- Keep mandatory summaries in `AGENTS.md`; put procedural detail in `docs/agents/workflow.md`.
- Keep the agent-facing architecture map concise; link to deeper human-facing architecture documentation when it exists.
- Keep failure descriptions in `runtime-playbook.md`; use `failure-index.md` only as an index and `memory.json` only for structured stable facts.
- If an adjacent sidecar owns plan-bound `runs/`, keep `execution-log.md` limited to reusable project learning and link to sidecar IDs only when that context is useful.
- Keep machine or session detection outside tracked documentation.

## Language

Choose project languages explicitly. Keep each documentation subtree internally consistent. A project may use one language everywhere or separate human and agent audiences by language. Do not translate identifiers, commands, paths, configuration keys, or API names when translation reduces precision.
