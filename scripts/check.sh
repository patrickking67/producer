#!/usr/bin/env bash
# Run every check CI runs. Usage: npm run check (or bash scripts/check.sh).
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

claude_bin="${CLAUDE_BIN:-claude}"
if ! command -v "$claude_bin" >/dev/null 2>&1; then
  echo "check: the claude CLI is required for plugin validation." >&2
  echo "Install it with: npm install -g @anthropic-ai/claude-code@2.1.309" >&2
  exit 1
fi

echo "==> Repository check (manifests, frontmatter, bundle, docs, Max for Live scripts)"
python3 scripts/check-repository.py

echo "==> Marketplace manifest (strict)"
"$claude_bin" plugin validate --strict .

echo "==> Plugin manifest and components (strict)"
"$claude_bin" plugin validate --strict plugins/producer

echo "All checks passed."
