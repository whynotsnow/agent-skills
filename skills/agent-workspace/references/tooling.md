# Tooling Boundary

Use this reference before editing `.agent-workspace/tools/` or deciding whether skill logic should run instead of local tooling.

## Boundary

- The skill is the operator.
- `.agent-workspace/manifest.json` is the contract.
- `.agent-workspace/tools/` is the workspace-local implementation.

The skill must discover the workspace and prefer `manifest.tooling.entry` when it exists. Do not hardcode `.agent-workspace/tools/agent-workspace.mjs` unless the manifest declares that exact entry.

## Valid Local Implementations

Projects may implement tooling with Node, Python, Bash, Make, package-manager aliases, CI commands, or another runtime. The manifest must describe the selected entry accurately.

Package-manager aliases are allowed as conveniences, but conformance must not depend on `package.json` scripts.

## Fallback Rules

If the manifest exists and local tooling exists:

- Invoke local tooling.
- Treat unsupported subcommands as workspace capability gaps.
- Do not silently replace local validation with bundled skill validation.

If no manifest exists:

- Use adoption guidance and templates.
- Ask before overwriting existing project instructions or documentation.

If a manifest exists but local tooling is missing:

- Report the gap.
- Offer to install reference tooling only if the user asks to adopt or repair the workspace.
