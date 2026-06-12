# Owl's Skills 🦉

我的 Claude Code 自用 skill 集合包。

## 已收录

| Skill | 命令 | 说明 |
|-------|------|------|
| 1st-pr | `/1st-pr` | 第一性原理思维 — 拆解问题至基本真理，从底层重建解决方案 |

## 安装

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Myron-Owl/Owl-skills/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/Myron-Owl/Owl-skills/main/install.ps1 | iex
```

### 手动安装

```bash
git clone https://github.com/Myron-Owl/Owl-skills.git
bash Owl-skills/install.sh
```

安装后重启 Claude Code，输入 `/1st-pr` 即可使用。

## 添加新 Skill

仓库里新建目录 + `SKILL.md`，install 脚本会自动识别安装：

```
Owl-skills/
├── 1st-pr/              ← 现有
│   ├── SKILL.md
│   └── examples/
├── your-skill/          ← 新 skill
│   └── SKILL.md
├── install.sh
├── install.ps1
├── LICENSE
└── README.md
```

## LICENSE

MIT
