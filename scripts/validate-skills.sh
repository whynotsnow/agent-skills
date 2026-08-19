#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for skill in agent-docs agent-workspace agent-project-sidecar; do
  dir="$ROOT/skills/$skill"
  test -f "$dir/SKILL.md"
  test -f "$dir/agents/openai.yaml"
  grep -q "^name: $skill$" "$dir/SKILL.md"
  grep -q "^description:" "$dir/SKILL.md"
done

find "$ROOT/skills" -path '*/scripts/*.py' -print0 | xargs -0 -r python3 -m py_compile

if find "$ROOT" \( -name '__pycache__' -o -name '*.pyc' -o -name '.DS_Store' \) | grep -q .; then
  echo "Generated cache files are present." >&2
  exit 1
fi

echo "Skill validation passed."

