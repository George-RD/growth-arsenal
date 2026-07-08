#!/bin/sh
# Compose a [FEEDBACK] issue body for the growth-arsenal plugin.
# Outputs Markdown to stdout. Does NOT contact GitHub and never submits.
# Usage: compose-feedback.sh --favorite "..." --hated "..." [--log path]
set -eu

favorite=""
hated=""
log=""

while [ $# -gt 0 ]; do
  case "$1" in
    --favorite) favorite="$2"; shift 2 ;;
    --hated) hated="$2"; shift 2 ;;
    --log) log="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

cat <<EOF
## What I liked

$favorite

## What was frustrating or broken

$hated
EOF

if [ -n "$log" ] && [ -f "$log" ]; then
  echo
  echo "## Decision log (redacted by user before posting)"
  echo
  cat "$log"
fi

echo
echo "---"
echo "Submitted via the growth-arsenal plugin-feedback module."
