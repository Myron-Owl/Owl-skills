# 安全编辑 Excel 工作簿 - Claude Code Skill

## 概述

**命令**: `/excel-edit`

企业级 Excel 工作簿安全编辑框架。将 Excel 编辑视为**依赖图上的事务（Transaction）**，而非简单的单元格写入操作。

适用于包含密集公式链、跨表引用、跨工作簿链接、命名区域、共享/动态公式、宏、数据连接或严格保留要求的 `.xlsx`/`.xlsm` 文件。

## 核心思想

> 用最小的授权变更，以 Microsoft Excel 原生实例作为计算的真理来源（Oracle），在完整的依赖图上执行可回滚的事务。

## 核心能力

| 能力 | 说明 |
|------|------|
| **路由决策** | 根据工作簿复杂度自动选择编辑路线（原生 Excel 编辑 vs OOXML 包手术修补） |
| **合约驱动** | 编辑前必须完成 `workbook_manifest.json` — 声明依赖、编辑范围、保护级别、验收标准 |
| **12步事务流程** | 预检→清单→演练→备份→原生会话→打开依赖→编辑→重算→提交→重开验证→迁移验证→报告/回滚 |
| **五级保护** | 可编辑 / 可扩展 / 公式结构保护 / 结果保护 / 严格保护 |
| **公式语义保留** | 区分 A1 文本、R1C1 模式、缓存值、共享公式元数据、外部链接索引 |
| **原生验证** | 通过 COM 自动化控制 Microsoft Excel，执行完整重算、错误扫描、验收单元格检查 |
| **失败安全** | 7个终端状态码，回滚时恢复备份并验证哈希 |
| **OOXML 审计** | Python 脚本 `inspect_xlsx_package.py` 扫描包结构、公式、外部链接、绝对路径 |

## 9大关键操作原则（tl;dr）

1. **路由优先** — 存在跨工作簿公式/宏/Power Query/.xlsm 时，强制使用原生 Excel 编辑
2. **合约先行** — 未完成 `workbook_manifest.json` 验证前，绝不写入
3. **依赖顺序打开** — 源工作簿在前，依赖工作簿在后
4. **批量写入** — 值块与公式块分离，使用正确尺寸的二维矩阵写入
5. **计算一次** — 写入完成后执行 `CalculateFullRebuild`，等待 `xlDone`
6. **不覆盖公式语义** — 不把派生结果硬编码为值
7. **严格保护逐格比对** — 不只是汇总检查
8. **需验证迁移** — 整个依赖集复制到另一目录后，再验证一次
9. **失败回滚** — 不留半成品在正式交付目录

## 使用场景

- ✅ 修改有密集公式链的复杂工作簿
- ✅ 跨工作簿公式的维护和更新
- ✅ `.xlsm` 宏工作簿的精确编辑
- ✅ 需要验证公式回归正确性的场景
- ✅ 绝对路径清理（`strict_no_absolute_paths`）
- ❌ 游戏数值设计/策划数值表（参考项目专属规范）
- ❌ 纯新建简单工作簿（没必要走完整事务流程）

## 文件结构

```
excel-edit/
├── SKILL.md                          ← 技能完整指令（Claude 读）
├── README.md                         ← 本文件（人读）
├── scripts/
│   ├── inspect_xlsx_package.py       ← OOXML 包结构审计工具
│   └── validate_manifest.py          ← 编辑合约格式验证器
├── references/
│   ├── tool-routing.md               ← 路由决策表
│   ├── manifest-contract.md          ← 编辑合约规范
│   ├── native-edit-transaction.md    ← 原生 Excel 编辑事务流程
│   ├── validation-and-rollback.md    ← 验证与回滚规范
│   └── technical-sources.md          ← Microsoft 技术参考来源
└── assets/
    ├── workbook_manifest.example.json ← 编辑合约示例
    ├── edit_plan.example.json         ← 编辑计划示例
    └── validation_report.example.json ← 验证报告示例
```

## 使用方法

```
帮我修改这个 Excel 文件的值                   → 自动触发
/excel-edit                              → 直接调用
这个工作簿的公式引用了外部文件，改之前先建模依赖  → Claude 会建议走原生 Excel 路由
```

## 依赖

- **Python 3.8+** — 用于运行审计和验证脚本
- **Microsoft Excel**（Windows/macOS 桌面版） — 原生编辑路由必须；结构审计可离线运行

## 终端状态码

| 状态 | 说明 |
|------|------|
| `PASS_NATIVE` | 完整原生验证通过 |
| `PASS_STRUCTURE_ONLY` | 包结构正确，但原生验证不可用 |
| `WARNING_TOOL_LIMITATION` | 工具无法评估某特性 |
| `FAIL_BUSINESS` | 公式或结果违反声明的业务检查 |
| `FAIL_STRUCTURE` | 包/关系/序列化检查失败 |
| `ROLLED_BACK` | 已恢复备份并验证哈希 |

## 版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-08-04 | 初始整合到 Owl-skills，删除 OpenAI 配置，去除外部不存在的依赖引用 |
| v1.1 | 2026-08-04 | 技能重命名为 `/excel-edit`（原名 edit-excel-workbooks），目录同步改名，恢复 OpenAI/Codex 兼容配置 |
| v1.2 | 2026-08-04 | 外部更新解决外链问题（新增 PowerShell/COM 陷阱与交付规范、离线预检脚本），并保持 `/excel-edit` 命名不变 |
