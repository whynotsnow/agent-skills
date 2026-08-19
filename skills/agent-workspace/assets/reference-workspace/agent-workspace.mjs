import { existsSync } from "node:fs";
import { dirname, join, parse } from "node:path";

const [command] = process.argv.slice(2);

function fail(message) {
	console.error(`[agent-workspace] ${message}`);
	process.exit(1);
}

function findWorkspaceRoot(start) {
	let current = start;
	while (true) {
		if (existsSync(join(current, ".agent-workspace", "manifest.json"))) {
			return current;
		}
		const parent = dirname(current);
		if (parent === current || current === parse(current).root) return null;
		current = parent;
	}
}

const root = findWorkspaceRoot(process.cwd());
if (!root) fail("No .agent-workspace/manifest.json found in this directory tree.");
process.chdir(root);

if (command === "validate") {
	console.log("[agent-workspace] Add project-specific validation here.");
} else {
	fail("Usage: validate");
}
