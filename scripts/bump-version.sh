#!/bin/bash
# bump-version.sh — Bump plugin version in both .claude-plugin/plugin.json and
# .claude-plugin/marketplace.json
#
# Usage:
#   ./scripts/bump-version.sh <new-version>
#   ./scripts/bump-version.sh 1.1.0
#   ./scripts/bump-version.sh --check   # Verify plugin.json and marketplace.json match
#
# This ensures plugin.json and marketplace.json never diverge, which
# causes the plugin cache to serve stale versions.

set -euo pipefail

PLUGIN_JSON=".claude-plugin/plugin.json"
MARKETPLACE=".claude-plugin/marketplace.json"

die() { echo "Error: $1" >&2; exit 1; }

# ── Check mode: verify plugin.json version matches marketplace.json ──
if [[ "${1:-}" == "--check" ]]; then
  name=$(jq -r '.name' "$PLUGIN_JSON")
  pv=$(jq -r '.version' "$PLUGIN_JSON")
  mv=$(jq -r --arg n "$name" '.plugins[] | select(.name == $n) | .version // empty' "$MARKETPLACE")

  if [[ -z "$mv" ]]; then
    die "$name not found in $MARKETPLACE"
  fi

  if [[ "$pv" != "$mv" ]]; then
    echo "MISMATCH: $name — plugin.json=$pv, marketplace.json=$mv"
    echo "Run: ./scripts/bump-version.sh <version>"
    exit 1
  fi

  echo "OK: $name v$pv"
  exit 0
fi

# ── Bump mode ──
[[ $# -ge 1 ]] || die "Usage: $0 <new-version>  (or --check)"

NEW_VERSION="$1"

# Validate semver-ish format
[[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "Version must be semver (e.g., 1.1.0), got: $NEW_VERSION"

NAME=$(jq -r '.name' "$PLUGIN_JSON")
OLD_PV=$(jq -r '.version' "$PLUGIN_JSON")
OLD_MV=$(jq -r --arg n "$NAME" '.plugins[] | select(.name == $n) | .version' "$MARKETPLACE" 2>/dev/null || echo "NOT_FOUND")

echo "Plugin:      $NAME"
echo "plugin.json: $OLD_PV → $NEW_VERSION"
[[ "$OLD_MV" != "NOT_FOUND" ]] && echo "marketplace:  $OLD_MV → $NEW_VERSION"

tmp=$(mktemp)
jq --arg v "$NEW_VERSION" '.version = $v' "$PLUGIN_JSON" > "$tmp" && mv "$tmp" "$PLUGIN_JSON"

if [[ "$OLD_MV" != "NOT_FOUND" ]]; then
  tmp=$(mktemp)
  jq --arg n "$NAME" --arg v "$NEW_VERSION" \
    '(.plugins[] | select(.name == $n)).version = $v' "$MARKETPLACE" > "$tmp" && mv "$tmp" "$MARKETPLACE"
fi

echo ""
echo "Done. Both files updated to v$NEW_VERSION."
echo "Commit with: git add $PLUGIN_JSON $MARKETPLACE && git commit -m 'chore(release): bump v$NEW_VERSION'"
