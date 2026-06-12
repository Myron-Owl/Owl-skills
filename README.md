# Owl's Skills 🦉

> 我的 Claude Code 自用 skill 集合包。

## 收录技能

| Skill | Slash 命令 | 说明 |
|-------|-----------|------|
| 第一性原理思维 | `/1st-pr` | 拆解问题至基本真理，从底层重新构建解决方案 |

_更多 skill 陆续添加中..._

## 安装

### 自动安装

```bash
git clone https://github.com/Myron-Owl/Owl-skills.git ~/Owl-skills
bash ~/Owl-skills/install.sh
```

### 手动安装

把需要的 skill 目录复制到 `~/.claude/skills/`：

```bash
cp -r ~/Owl-skills/1st-pr ~/.claude/skills/
```

## 使用

重启 Claude Code，输入 `/` 查看所有可用 skill：

```
/1st-pr 为什么房价会上涨？
```

## 添加新 Skill

在仓库根目录新建一个目录，里面放 `SKILL.md` 即可：

```
Owl-skills/
├── 1st-pr/
│   ├── SKILL.md
│   └── examples/
├── new-skill/              ← 新 skill
│   └── SKILL.md
├── install.sh
├── LICENSE
└── README.md
```

## 许可证

MIT
