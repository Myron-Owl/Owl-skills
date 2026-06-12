#!/bin/bash
# Install all skills in this collection to ~/.claude/skills/
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "Installing Owl's Skills to $SKILLS_DIR..."
mkdir -p "$SKILLS_DIR"

# Copy each skill directory (skip hidden dirs and files)
for dir in "$SCRIPT_DIR"/*/; do
    basename="$(basename "$dir")"
    case "$basename" in
        .*|_) continue ;;
    esac
    if [ -f "$dir/SKILL.md" ]; then
        echo "  → Installing: $basename"
        mkdir -p "$SKILLS_DIR/$basename"
        cp -r "$dir/"* "$SKILLS_DIR/$basename/"
    fi
done

echo ""
echo "✅ Done! Restart Claude Code and type / to see your skills."
