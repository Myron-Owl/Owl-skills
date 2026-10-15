# 游戏设计师 · 知识库与系统设计实务（game-designer）

## 概述

**命令**：`/game-designer`

收录 23 位有**已发售实际产品验证**的游戏设计大师的设计哲学、方法论与代表作品。提供六透镜设计分析系统，支持按需设计拆解、跨大师视角合成、设计风险评估和涌现叙事分析。另提供游戏设计师实务：核心循环、机制规格、经济与成长平衡、玩家反馈与引导、原型和测试迭代。详细流程及模板按需读取 [游戏设计师实务](references/game-designer-practice.md)。

默认输出对话分析；生成或修改 CC战棋 项目策划文档时，切换为项目文档模式，并遵循《策划文档 AI 协作规范》v1.16（2026-08-07）。项目中的现行规范更新时，以现行版本为准。

## 战棋专项

原 `tactical-wargame-design` 已合并为 [战棋设计专项](references/tactical-combat-design.md)，统一通过 `/game-designer` 使用。涉及行动经济、地形与视野、单位职责、任务目标、随机性、敌人压力、遭遇战和战斗 UI 时按需加载；通用设计任务不必读取。

## 游戏哲学参考

新增 [苏茨的游戏哲学与障碍评审](references/bernard-suits-game-philosophy.md)：从目标、手段、构成性规则与游戏态度分析限制，区分游戏成立与体验质量，评审挑战、重复劳动、等待、便利功能与开放式游戏。单列哲学来源、学术解释和可测试的设计推论，保留 23 位大师与六透镜结构。

## 六透镜系统

| Lens | 核心关注 | 代表大师 |
|------|---------|---------|
| **Miyamoto Lens**（教学型设计） | 低认知负担、清晰反馈、直觉学习曲线 | 宫本茂、堀井雄二、Jonathan Blow |
| **Sid Meier Lens**（决策密度） | "Interesting decisions"、策略权衡 | Sid Meier、Will Wright |
| **Miyazaki Lens**（惩罚学习） | 高风险学习、fail-driven progression | 宫崎英高、神谷英树、John Romero |
| **Ueda Lens**（情绪极简） | 减法设计、空间叙事、情感投射 | 上田文人、陈星汉 |
| **Narrative Systems Lens**（叙事系统化） | 叙事机制化、元结构、世界观语法 | 小岛秀夫、Sam Lake、Ken Levine、Cory Barlog、Dan Houser |
| **Tynan Lens**（系统生成叙事） | 涌现叙事、模拟栈、故事生成器 | Tynan Sylvester、Will Wright、Todd Howard |

## 覆盖的 23 位大师

| 区域 | 大师 |
|------|------|
| 🗾 日本 | 宫本茂、宫崎英高、小岛秀夫、神谷英树、坂口博信、堀井雄二、上田文人 |
| 🌍 欧美 | Sid Meier、Todd Howard、Sam Lake、Will Wright、Warren Spector、Ken Levine、Amy Hennig、Neil Druckmann、Cory Barlog、Dan Houser、陈星汉、Tim Schafer、Josef Fares、Jonathan Blow、John Romero、Tynan Sylvester |

## 分析模式

| 模式 | 说明 |
|------|------|
| `breakdown` | 6-Lens 逐项分析 |
| `synthesis` | 跨 Lens 创造性合成 |
| `critique` | 设计风险检测 |
| `prototype` | MVP 原型方案生成 |
| `emergent-story-scan` | 涌现叙事能力专项评估 |
| `design` | 循环、系统与机制规格设计 |
| `balance` | 经济、成长曲线与调参分析 |
| `onboarding` | 玩家提示、反馈与引导设计 |
| `playtest` | 测试计划、观察分析与调参迭代 |
| `mechanism-transfer` | 跨品类机制移植与压力测试 |

## 使用方法

```yaml
/game-designer 帮我分析一下这个战斗系统设计...
Analyze: <game idea / mechanic / system>
Mode: breakdown
Depth: high
Lens: auto
Output: conversation
```

或者在对话中自然描述你的游戏设计想法，技能会自动识别并调用最相关的透镜进行分析。

写入项目文档时使用 `Output: project-document`，并提供目标文档相对路径。技能会先读取现行规范、目标文档的 YAML、`ai_context` 与依赖文档；未经确认的假设、数值和候选方案不会写入。

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| v1.0 | 2026-06-15 | Claude (gstack) | 初始版本：收录 23 位大师、6-Lens 分析系统、分析引擎 v2 |
| v1.1 | 2026-06-16 | Myron-Owl | 发布至 Owl-skills 仓库，补充中文 README 说明 |
| v2.1 | 2026-07-23 | Myron-Owl | 技能命令统一为 gd-master |
| v2.2 | 2026-08-11 | Codex | 适配策划文档规范 v1.16，区分对话与项目文档输出 |
| v2.5 | 2026-10-09 | Codex | 合并游戏设计师实务，新增规格、平衡、引导、测试与跨品类移植模式；保留六透镜及项目文档边界 |
| v2.6 | 2026-10-09 | Codex | 技能更名为 game-designer，同步入口、目录、调用示例与案例引用 |
| v2.7 | 2026-10-09 | Codex | 合并 tactical-wargame-design 为按需战棋专项参考，统一技能入口，保留设计原则与原出处 |
| v2.8 | 2026-10-15 | Codex | 新增苏茨游戏哲学参考与障碍评审；区分原著、研究解释、设计推论和测试证据，澄清理论引用边界 |
