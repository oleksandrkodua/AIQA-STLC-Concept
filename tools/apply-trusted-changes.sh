#!/usr/bin/env bash
# Applies the trusted changes to .claude/ (hooks, permission floor, per-machine hooks config).
# RUN BY A HUMAN, after QA Lead approval (CLAUDE.md: trusted assets change only with approval).
# macOS / Linux: any shell. Windows: Git Bash (comes with Git for Windows). NOT VERIFIED on Windows.
# Never deletes anything. Existing settings files are never overwritten: a *.proposed file is written instead.
# Usage: bash tools/apply-trusted-changes.sh [--dry-run] [--yes] [--profile qa|maintainer]
# Profiles: qa (default) = strict, Claude cannot edit repository files (tools/settings.qa.json, deny).
#                   maintainer = ask before editing trusted paths (tools/settings.shared.json). Only for the AI QA Process Lead and other maintainers.
set -euo pipefail

DRY=0; YES=0; PROFILE=qa
while [ $# -gt 0 ]; do case "$1" in
  --dry-run) DRY=1;; --yes) YES=1;;
  --profile) shift; PROFILE="${1:-}";;
  *) echo "unknown option: $1"; exit 2;; esac; shift; done
case "$PROFILE" in qa) PROFILE_FILE="settings.qa.json";; maintainer) PROFILE_FILE="settings.shared.json";; *) echo "unknown profile: $PROFILE (use qa or maintainer)"; exit 2;; esac
echo "Permission profile: $PROFILE ($PROFILE_FILE)"

root="$(cd "$(dirname "$0")/.." && pwd)"
plug="$root/plugins/qabase"; dot="$root/.claude"; tools="$root/tools"
[ -d "$plug/hooks" ] || { echo "ERROR: $plug/hooks not found. Run from a checkout of this repo."; exit 1; }

confirm() { # $1 = question
  [ "$DRY" = 1 ] && { echo "  [dry-run] would ask: $1"; return 1; }
  [ "$YES" = 1 ] && return 0
  read -r -p "$1 [y/N] " ans; [ "$ans" = "y" ] || [ "$ans" = "Y" ]
}

find_python() {
  for cand in "python3" "py -3" "python"; do
    # shellcheck disable=SC2086
    if $cand -c 'import sys; sys.exit(0 if sys.version_info[0]==3 else 1)' >/dev/null 2>&1; then echo "$cand"; return 0; fi
  done
  return 1
}

PY="$(find_python)" || { echo "ERROR: no working Python 3 found (tried python3, py -3, python). Install Python 3 first (docs/REQUIRED-ACCESS-AND-ENVIRONMENT.md, B1.4)."; exit 1; }
echo "Python launcher that works here: $PY"
mkdir -p "$dot/hooks"

echo; echo "== 1. Hook scripts: plugins/qabase/hooks -> .claude/hooks"
changed=()
for f in "$plug"/hooks/*.py "$plug"/hooks/prod-hosts.txt; do
  [ -f "$f" ] || continue; b="$(basename "$f")"
  if [ ! -f "$dot/hooks/$b" ]; then echo "  new: $b"; changed+=("$f")
  elif ! cmp -s "$f" "$dot/hooks/$b"; then echo "  changed: $b"; diff -u "$dot/hooks/$b" "$f" | head -20 || true; changed+=("$f"); fi
done
if [ "${#changed[@]}" -eq 0 ]; then echo "  nothing to do"; elif confirm "Copy ${#changed[@]} file(s) into .claude/hooks?"; then for f in "${changed[@]}"; do cp "$f" "$dot/hooks/"; done; echo "  copied"; fi

echo; echo "== 2. Permission floor: .claude/settings.json"
if [ ! -f "$dot/settings.json" ]; then
  echo "  .claude/settings.json does not exist: the deny/ask rules are NOT active today."
  if confirm "Create .claude/settings.json from tools/$PROFILE_FILE ($PROFILE profile)?"; then cp "$tools/$PROFILE_FILE" "$dot/settings.json"; echo "  created"; fi
elif ! cmp -s "$tools/$PROFILE_FILE" "$dot/settings.json"; then
  echo "  .claude/settings.json exists and differs: wrote .claude/settings.json.proposed, merge by hand."
  [ "$DRY" = 1 ] || cp "$tools/$PROFILE_FILE" "$dot/settings.json.proposed"
else echo "  already up to date"; fi

echo; echo "== 3. Per-machine hooks: .claude/settings.local.json (launcher: $PY)"
rendered="$(sed "s#__PY__#$PY#g" "$tools/hooks.template.json")"
if [ ! -f "$dot/settings.local.json" ]; then
  if confirm "Create .claude/settings.local.json with the hooks for this machine?"; then printf '%s\n' "$rendered" > "$dot/settings.local.json"; echo "  created"; fi
elif [ "$rendered" != "$(cat "$dot/settings.local.json")" ]; then
  echo "  .claude/settings.local.json exists and differs: wrote .claude/settings.local.json.proposed, merge by hand."
  [ "$DRY" = 1 ] || printf '%s\n' "$rendered" > "$dot/settings.local.json.proposed"
else echo "  already up to date"; fi

echo; echo "== 4. .gitignore: keep per-machine files out of git"
for line in ".claude/settings.local.json" ".claude/*.proposed"; do
  if ! grep -qxF "$line" "$root/.gitignore" 2>/dev/null; then
    if confirm "Append '$line' to .gitignore?"; then printf '%s\n' "$line" >> "$root/.gitignore"; echo "  added $line"; fi
  fi
done

echo; echo "== 5. OS sandbox (macOS, Linux, WSL2): user-level settings, never written by this script"
echo "  Proposed keys: tools/sandbox.user.json (network allowlist, no unsandboxed commands, credential deny entries, denyWrite on plugins/qabase/**)."
echo "  Merge them by hand into ~/.claude/settings.json after replacing the placeholder host. NOT TESTED. Native Windows: no OS sandbox."

echo; echo "Done. NOT VERIFIED: that Claude Code fires these hooks. Next: restart Claude Code in this folder and run /onboarding-check hooks (it includes the firing test)."
