#!/bin/bash
# Owl's Skills — 一键安装所有 skill 到 ~/.claude/skills/
#
# 用法:
#   本地安装: git clone ... && bash Owl-skills/install.sh
#   远程安装: curl -fsSL https://git.io/... | bash
set -e

REPO="https://github.com/Myron-Owl/Owl-skills.git"
SKILLS_DIR="$HOME/.claude/skills"

# 判断是在本地运行还是远程 pipe
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd 2>/dev/null || pwd)"
if [ -f "$SCRIPT_PATH/README.md" ]; then
    SRC="$SCRIPT_PATH"
else
    echo "→ Cloning repository..."
    TMP_DIR="$(mktemp -d 2>/dev/null || echo "/tmp/owl-skills-$$")"
    git clone --depth 1 "$REPO" "$TMP_DIR"
    SRC="$TMP_DIR"
fi

echo "→ Installing Owl's Skills..."
mkdir -p "$SKILLS_DIR"

for dir in "$SRC"/*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"
    case "$name" in .*|_) continue ;; esac
    [ -f "$dir/SKILL.md" ] || continue
    echo "   • $name"
    mkdir -p "$SKILLS_DIR/$name"
    cp -r "$dir/"* "$SKILLS_DIR/$name/"
done

rm -rf "$TMP_DIR"
echo ""
echo "✅ Installed! Restart Claude Code and type / to see your skills."
