# Agent Docs Migration

Use this workflow for repositories with existing documentation.

1. Run `status` and inventory existing README, agent instruction, architecture, workflow, troubleshooting, and developer documents.
2. Map each existing document to the ownership table in `document-contract.md`.
3. Run `init --dry-run` to preview only missing files.
4. Run `init` to create missing placeholders without overwriting existing content.
5. Move content by responsibility, not by filename similarity.
6. Replace duplicated content with links to the owning document.
7. Preserve project-specific documents outside the fixed structure when they have a clear audience and purpose.
8. Validate the final structure and run the project's existing checks.

Do not delete legacy documents until incoming links, documentation indexes, CI references, and agent instructions have been updated. Keep renames and link repairs in the same coherent change.

When Agent Workspace is present, do not move its manifest, local state, schemas, or project tooling into Agent Docs. Agent Docs governs documentation; Agent Workspace governs the broader workspace contract.
