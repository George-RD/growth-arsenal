#!/bin/sh
# install.sh — symlink growth-arsenal skills into a harness's user skills root.
#
# Usage:
#   ./install.sh <target>
#   ./install.sh omp | claude | codex | opencode | agents
#
# Symlinks mean `git pull` updates propagate automatically. Windows users:
# copy the skills/<name> dirs into the target root manually instead.

set -eu

SKILLS_DIR="skills"

usage() {
  echo "Usage: $0 <target>"
  echo ""
  echo "Targets:"
  echo "  omp       -> ~/.omp/agent/skills/"
  echo "  claude    -> ~/.claude/skills/ (also inherited by OMP)"
  echo "  codex     -> ~/.codex/skills/"
  echo "  opencode  -> ~/.config/opencode/skills/"
  echo "  agents    -> ~/.agents/skills/"
  exit 1
}

[ $# -ge 1 ] || usage

case "$1" in
  omp)      ROOT="$HOME/.omp/agent/skills" ;;
  claude)   ROOT="$HOME/.claude/skills" ;;
  codex)    ROOT="$HOME/.codex/skills" ;;
  agents)   ROOT="$HOME/.agents/skills" ;;
  opencode) ROOT="$HOME/.config/opencode/skills" ;;
  *) usage ;;
esac

BASE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$ROOT"

for skill_path in "$BASE/$SKILLS_DIR"/*/; do
  name="$(basename "$skill_path")"
  dest="$ROOT/$name"

  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    echo "Refusing to overwrite non-symlink: $dest" >&2
    exit 1
  fi

  ln -sfn "$BASE/$SKILLS_DIR/$name" "$dest"
  echo "Linked $dest -> $BASE/$SKILLS_DIR/$name"
done
