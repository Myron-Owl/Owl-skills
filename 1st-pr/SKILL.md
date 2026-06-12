---
name: 1st-pr
preamble-tier: 2
version: 1.0.0
description: 第一性原理思维 — 拆解问题至基本真理，从底层重新构建解决方案。 (First Principles Thinking)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
triggers:
  - 第一性原理
  - first principles
  - 拆解问题
  - decompose problem
  - 从根本思考
  - think from scratch
  - 打破思维定势
  - reason from fundamentals
  - 归零思考
---

## When to invoke this skill

Use when faced with a complex problem where conventional approaches have failed,
when you need to innovate beyond existing solutions, when assumptions need
challenging, or when you want to ensure the deepest possible understanding of
a problem before solving it.

Proactively invoke this skill when:
- The user is stuck on a problem they've tried multiple approaches for
- A problem seems to have no good solution within existing constraints
- The user asks to "think outside the box" or "challenge assumptions"
- You're designing architecture or solving bugs where surface-level fixes keep recurring
- The user says "this is just how it's done" — that's a flag for assumption-blindness
- Before building anything complex, to ensure the foundation is sound

---

## Core Methodology

第一性原理（First Principles Thinking）源于亚里士多德的物理学，指将问题拆解到最基础的、
不证自明的真理，然后从那里重新向上构建。这与"类比思维"（reasoning by analogy）相对。

### The Five-Step Process

#### Step 1: 明确问题 (Define the Problem)

清晰界定要解决的问题。含糊的问题导致含糊的答案。

- **问题陈述**：用一句话描述"我们到底要解决什么？"
- **范围边界**：什么在范围内、什么不在？
- **成功标准**：如何判断问题已解决？
- **关键追问**："这个问题的本质是什么？" "去掉所有修饰，核心是什么？"

> **输出**: 一个清晰、无歧义的问题陈述。

#### Step 2: 拆解至基本元素 (Decompose to Fundamentals)

将问题拆解到不能再拆的基本真理。区分"事实"和"假设"。

**分解维度**：

| 维度 | 追问 | 示例（软件工程） |
|------|------|-----------------|
| 物理/硬约束 | 什么是不可改变的事实？ | CPU周期、内存、网络延迟的物理极限 |
| 逻辑/数学 | 什么是数学上必然成立的？ | 算法复杂度下限、CAP定理 |
| 领域定律 | 这个领域的公理是什么？ | 数据库ACID、HTTP无状态性 |
| 目标/需求 | 用户真正需要的是什么？ | 不是"更快的页面"而是"用户不等待" |

**技巧：苏格拉底式追问 (Socratic Questioning)**

对每一个看似"理所当然"的陈述，追问：
1. 这个结论的依据是什么？
2. 这个依据本身是否成立？
3. 有没有反例？
4. 如果我们推翻这个假设，会发生什么？

> **输出**: 一份基本元素清单，每一项都是不证自明的真理或经过验证的事实。

#### Step 3: 挑战假设 (Challenge Assumptions)

识别并质疑所有"我们一直这么做"的隐含假设。这是创造力的关键步骤。

**常见假设类别**：

- **领域假设**："在这个行业，X是必须的"
- **历史假设**："我们一直这样做所以必须继续"
- **约束假设**："我们只能使用Y技术栈"
- **规模假设**："当规模变大时，X必然会变慢"
- **角色假设**："用户不想要X" / "用户只会用Y方式"

**清单方法**：逐条列出当前方案的所有假设，对每条标记：
- ✅ 已验证的事实 — 保留
- ❌ 未经检验的假设 — 需要验证或推翻
- ⚠️ 可能过时的假设 — 需要重新评估

> **输出**: 假设清单，区分哪些是真实的约束、哪些只是心理惯性。

#### Step 4: 从零重建 (Reconstruct from Zero)

基于 Step 2 的基本元素，不受现有方案影响，重新设计解决方案。

**重建原则**：

1. **从理想出发**：不考虑任何限制，最佳方案是什么样？
2. **逐一引入约束**：从 Step 3 中取回真实的约束（已验证的事实），每次引入一个，观察方案如何调整。
3. **生成多个方案**：至少产出 3 个完全不同的方向（不只是在现有方案上微调）。
4. **寻找非对称解**：是否存在一个方案，投入小但效果巨大？

**思维工具**：

- **反向思维 (Inversion)**：不是问"如何成功"，而是问"如何保证失败？"然后避免那些事。
- **二阶效应 (Second-Order Effects)**：如果这样做，接下来会发生什么？再接下来呢？
- **极限法 (Think in Extremes)**：如果资源无限会怎样？如果资源为零会怎样？
- **类比迁移 (Cross-Domain Transfer)**：其他领域（生物、物理、军事、游戏）如何解决类似的结构问题？

> **输出**: 2-5 个基于基本元素构建的全新方案。

#### Step 5: 验证与迭代 (Validate and Iterate)

将新方案与现实进行碰撞，快速获取反馈。

- **最小可验证单元**：对于每个方案，找出最小的验证实验
- **证伪优先**：主动寻找方案的弱点，而不是证明它是对的
- **对比测试**：新方案与现有最佳方案比较
- **迭代循环**：验证 → 学习 → 调整 → 再验证

> **输出**: 验证结果和迭代后的最终方案。

---

## Applied Frameworks

### 框架 A: 软件架构拆解

适用于系统设计、技术选型、架构重构。

```
问题: "我们的系统太慢了"
├── 基本元素: 计算、存储、通信
│   ├── 计算: CPU指令执行速度 = 物理极限
│   ├── 存储: 读写速度层级 (L1缓存→磁盘)
│   └── 通信: 网络延迟 = 光速限制 + 协议开销
├── 挑战假设:
│   ├── ❌ "我们需要微服务" → 为什么？单体不行吗？
│   ├── ❌ "数据库是瓶颈" → 验证了吗？还是缓存策略问题？
│   └── ❌ "更多服务器解决一切" → 线性扩展的极限在哪？
└── 新方案:
    ├── 方案A: 消除不必要的计算（减少复杂度而非增加资源）
    ├── 方案B: 改变数据流拓扑（从同步到事件驱动）
    └── 方案C: 重新定义"慢"（用户感知 vs 系统指标）
```

### 框架 B: Bug 根因拆解

适用于复杂 Bug 排查，避免修表象不修本质。

1. **症状 ≠ 问题**：报错信息只是症状，不是根因。
2. **拆解调用链**：将出问题的流程分解到每一步。
3. **验证每一层的假设**：
   - 数据层：数据格式、完整性假设是否成立？
   - 逻辑层：业务逻辑的前提条件是否满足？
   - 展示层：渲染假设是否成立？
4. **构建最小复现**：去掉所有非必要部分后，问题还在吗？
5. **对每个"不可能"追问**：每当想说"这不可能是原因"，问自己"如果它是呢？"

### 框架 C: 产品/功能设计拆解

适用于需求分析、功能设计、用户体验改进。

1. **用户真正需要的结果是什么**？（不是功能，是结果）
   - "用户想要一个导出按钮" → 用户想要的是"在别处使用数据"
2. **排除现有方案的干扰**：假装没有现成软件，你会怎么设计？
3. **重新定义度量**：什么指标真正反映用户价值？（而非容易测量的指标）
4. **反向思考**：什么会让用户彻底放弃这个产品？

---

## Cognitive Biases to Watch For

第一性原理思考需要警惕以下认知偏差：

| 偏差 | 表现 | 应对 |
|------|------|------|
| 确认偏误 (Confirmation Bias) | 只找支持自己观点的证据 | 主动寻找证伪证据 |
| 沉没成本谬误 (Sunk Cost) | "已经投入这么多不能改" | 忽略过去投入，只看未来 |
| 权威偏误 (Authority Bias) | "某公司也这么做" | 权威做法 ≠ 最佳做法 |
| 可得性启发 (Availability) | 最近看到的方案影响判断 | 系统化搜索所有可能性 |
| 框架效应 (Framing Effect) | 问题呈现方式影响解决方向 | 用多种方式重新描述问题 |

---

## Conversation Flow

当用户触发此 skill 时，按以下流程进行：

### Phase 1: 问题定义

与用户协作，通过追问澄清问题：
1. "你遇到的具体问题是什么？用一句话描述。"
2. "这个问题的背景是什么？"
3. "你尝试过哪些方案？为什么会觉得它们不够好？"
4. "你在这个领域的假设有哪些？"

输出：清晰的问题陈述文档或消息。

### Phase 2: 拆解与分析

对问题进行第一性原理拆解：
1. 列出所有基本元素
2. 标记所有假设（区分事实和假设）
3. 挑战关键假设
4. 识别思维盲区

用户在这一阶段应感到"原来我从未真正理解这个问题"。

### Phase 3: 重建方案

根据基本元素构建新的解决方案：
1. 提出至少 2-3 个方向完全不同的方案
2. 说明每个方案的推理链（从基本元素到最终方案）
3. 分析每个方案的优缺点

### Phase 4: 验证计划

为选定的方案制定验证步骤：
1. 最小验证实验是什么？
2. 成功标准是什么？
3. 潜在的失败模式有哪些？

---

## Output Format

应用第一性原理分析时，输出应遵循以下标准化结构，确保结果一致、可读、可追溯：

```markdown
## 第一性原理分析：[问题名称]

### 1. 问题定义
**核心问题**：[一句话]
**范围边界**：[什么在范围内/什么不在]
**成功标准**：[如何衡量解决]

### 2. 拆解至基本元素
| 维度 | 基本事实 | 不可改变性 |
|------|---------|-----------|
| 物理/数学 | [不可改变的约束] | ✅ 硬约束 |
| 领域定律 | [领域内的公理] | ✅/⚠️ |
| 人性/行为 | [人的行为模式] | ✅/⚠️ |

### 3. 假设挑战
| 假设 | 挑战 | 判定 |
|------|------|------|
| "[常见假设]" | [为什么值得质疑] | ✅ 事实 / ❌ 假设 / ⚠️ 需验证 |

### 4. 从零重建
**推理链**：
基本事实 → [推理步骤1] → [推理步骤2] → ... → 方案

**方案对比**：
| 方案 | 核心思路 | 优点 | 缺点 |
|------|---------|------|------|
| A | [思路] | [优点] | [缺点] |
| B | [思路] | [优点] | [缺点] |

### 5. 验证计划
- [ ] 验证实验1：[做什么] → [预期结果]
- [ ] 验证实验2：[做什么] → [预期结果]
- [ ] 证伪测试：[什么情况下我的分析是错的]

### 6. 结论
**推荐方案**：[方案]
**核心洞察**：[第一性原理揭示的关键洞见]
**已知权衡**：[接受哪些妥协]
```

---

## 核心原则总结

1. **区分事实与假设** — 这是第一性原理的核心动作
2. **质疑一切，但有方法** — 不是为质疑而质疑，而是找到值得质疑的点
3. **从物理/数学上确认什么是不可能的** — 剩下的都是可能的
4. **拒绝"行业标准答案"** — 流行的做法未必是正确的做法
5. **简单是终极复杂** — 基于基本原理的方案往往更简单
6. **推理链必须透明** — A → B → C → D，每一步都要能检验

---

## Proactive Use

When working on any complex task, proactively apply first principles thinking when:
- You encounter "best practices" without understanding *why* they're best
- A problem has been "solved" but the solution feels over-engineered
- Requirements seem to bake in implicit assumptions about implementation
- The team is cargo-culting patterns from other projects
- A bug fix keeps reintroducing itself (surface fix vs. root fix)

---

## completion checklist

第一性原理思考完成的标准：
- [ ] 问题已被拆解到不可再分的基本元素
- [ ] 所有隐含假设已被识别和挑战
- [ ] 至少生成 2-3 个方向不同的方案
- [ ] 每个方案的推理链完整且透明
- [ ] 选择了方案并说明了理由
- [ ] 制定了验证计划
