#!/usr/bin/env bash
# DRAFT. Copies the plugin skills (source of truth) into the repo's .claude/skills as a fallback . Hooks and settings are handled by tools/apply-trusted-changes.sh.
# The copies are GENERATED: never edit them by hand. Does not delete anything.
# .claude/ is a trusted asset: run this yourself after QA Lead approval.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
src="$root/plugins/qabase"
mkdir -p "$root/.claude/skills"
cp -R "$src/skills/." "$root/.claude/skills/"
echo "Synced skills from plugins/qabase into .claude/skills. Hooks and settings: tools/apply-trusted-changes.sh. Review with: git diff --stat"
# Rebuild the navigator index (plugins/qabase/skills-index.json) from the plugin skills; needs Python 3 (python3, python or py -3).
for py in python3 python "py -3"; do
  if $py --version >/dev/null 2>&1; then $py "$root/tools/build-skills-index.py" && break; fi
done || echo "WARNING: navigator index not rebuilt (no Python 3 found or a check failed); run: python3 tools/build-skills-index.py"
