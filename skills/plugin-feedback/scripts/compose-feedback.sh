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
    --favorite)
      if [ $# -lt 2 ]; then echo "Error: $1 requires a value" >&2; exit 1; fi
      favorite="$2"; shift 2 ;;
    --hated)
      if [ $# -lt 2 ]; then echo "Error: $1 requires a value" >&2; exit 1; fi
      hated="$2"; shift 2 ;;
    --log)
      if [ $# -lt 2 ]; then echo "Error: $1 requires a value" >&2; exit 1; fi
      log="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [ -z "$favorite" ] || [ -z "$hated" ]; then
  echo "Error: --favorite and --hated require non-empty values" >&2
  exit 1
fi

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
