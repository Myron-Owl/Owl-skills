# Owl's Skills 🦉

我的 Claude Code 自用 skill 集合包。

## 已收录

| Skill | 命令 | 说明 |
|-------|------|------|
| [1st-pr](1st-pr/README.md) | `/1st-pr` | 第一性原理思维 — 拆解问题至基本真理，从底层重建解决方案 |
| [mao-thought](mao-thought/SKILL.md) | `/mao-thought` | 毛泽东思想分析框架 — 将实事求是、矛盾论等方法论应用于现代问题分析 |
| [wealth-master](wealth-master/README.md) | `/wealth-master` | 全周期理财大师（2026中国版）— 五阶段财富框架，从0到2000万+ |
| [reality-tunnel](reality-tunnel/README.md) | `/reality-tunnel` | 现实隧道分析器 — 受 Robert Anton Wilson 启发的认知决策工具。区分事实与解释，暴露隐藏假设，生成多机制竞争模型，将认知重构转化为可证伪验证与低成本行动。适用于拆解信念、复杂决策、团队冲突和游戏体验分析 |
| [gd-master](gd-master/README.md) | `/gd-master` | 全球游戏设计大师知识库 + 六透镜分析引擎 — 收录23位大师的设计哲学、方法论与代表作品，支持多维度设计拆解与风险评估 |
| [gdd-writer](gdd-writer/README.md) | `/gdd-writer` | GDD（Game Design Document）策划文档撰写 — 严格遵循策划文档规范，按模板和规则生成 CC战棋 项目策划文档 |

> 每个 skill 目录内有详细的 README 说明。点上面的 skill 名称查看。

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

仓库里新建目录，包含 `SKILL.md`（给 Claude 读）和 `README.md`（给人看），install 脚本会自动识别安装：

```
Owl-skills/
├── 1st-pr/                  ← 现有
│   ├── SKILL.md             ← 技能指令（Claude 读）
│   ├── README.md            ← 技能说明（人读）
│   └── examples/
├── your-skill/              ← 新 skill
│   ├── SKILL.md
│   └── README.md
├── install.sh
├── install.ps1
├── LICENSE
└── README.md                ← 合集介绍
```

## LICENSE

MIT
