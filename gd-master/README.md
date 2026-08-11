# 全球游戏设计大师 · 知识库与分析引擎（gd-master）

## 概述

**命令**：`/gd-master`

收录 23 位有**已发售实际产品验证**的游戏设计大师的设计哲学、方法论与代表作品。提供六透镜设计分析系统，支持按需设计拆解、跨大师视角合成、设计风险评估和涌现叙事分析。

默认输出对话分析；生成或修改 CC战棋 项目策划文档时，切换为项目文档模式，并遵循《策划文档 AI 协作规范》v1.16（2026-08-07）。项目中的现行规范更新时，以现行版本为准。

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

## 使用方法

```yaml
/gd-master 帮我分析一下这个战斗系统设计...
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
