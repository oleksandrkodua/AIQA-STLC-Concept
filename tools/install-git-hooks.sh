#!/bin/sh
# Point this clone at the versioned hooks in tools/git-hooks (core.hooksPath). Run from anywhere in the repo.
ROOT="$(git rev-parse --show-toplevel)" || exit 1
cd "$ROOT" || exit 1
chmod +x tools/git-hooks/pre-commit
git config core.hooksPath tools/git-hooks
echo "core.hooksPath = $(git config core.hooksPath)"
echo "Check: break a skill's frontmatter, run 'git commit' -> it must stop; restore it -> it must pass."
