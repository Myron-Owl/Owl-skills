#!/bin/bash
# Owl's Skills — 一键安装所有 skill 到 ~/.claude/skills/
#
# 用法:
#   本地安装: git clone ... && bash Owl-skills/install.sh
#   远程安装: curl -fsSL https://git.io/... | bash
set -e

ZIP_URL="https://github.com/Myron-Owl/Owl-skills/archive/refs/heads/main.zip"
SKILLS_DIR="$HOME/.claude/skills"

# 判断是在本地运行还是远程 pipe
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd 2>/dev/null || pwd)"
if [ -f "$SCRIPT_PATH/README.md" ]; then
    SRC="$SCRIPT_PATH"
else
    echo "→ Downloading Owl's Skills..."
    TMP_DIR="$(mktemp -d 2>/dev/null || echo "/tmp/owl-skills-$$")"
    ZIP_FILE="$TMP_DIR/repo.zip"

    if command -v curl &>/dev/null; then
        curl -fsSL "$ZIP_URL" -o "$ZIP_FILE"
    elif command -v wget &>/dev/null; then
        wget -q "$ZIP_URL" -O "$ZIP_FILE"
    else
        echo "❌ Need curl or wget to download."
        exit 1
    fi

    if [ ! -f "$ZIP_FILE" ]; then
        echo "❌ Download failed."
        rm -rf "$TMP_DIR"
        exit 1
    fi

    # 解压 (支持 unzip 或 tar)
    if command -v unzip &>/dev/null; then
        unzip -q "$ZIP_FILE" -d "$TMP_DIR"
    else
        echo "❌ Need unzip to extract."
        rm -rf "$TMP_DIR"
        exit 1
    fi

    # ZIP 解压后目录名: Owl-skills-main
    SRC="$TMP_DIR/Owl-skills-main"
    [ -d "$SRC" ] || SRC=$(find "$TMP_DIR" -maxdepth 1 -type d | tail -1)
fi

echo "→ Installing Owl's Skills..."
mkdir -p "$SKILLS_DIR"

count=0
for dir in "$SRC"/*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"
    case "$name" in .*|_) continue ;; esac
    [ -f "$dir/SKILL.md" ] || continue
    echo "   • $name"
    mkdir -p "$SKILLS_DIR/$name"
    cp -r "$dir/"* "$SKILLS_DIR/$name/"
    count=$((count + 1))
done

rm -rf "$TMP_DIR"
echo ""
if [ "$count" -gt 0 ]; then
    echo "✅ Installed $count skill(s)! Restart Claude Code and type / to see them."
else
    echo "⚠️ No skills found to install."
fi
