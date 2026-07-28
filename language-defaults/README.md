# 语言默认值分析器 (Language Defaults Analyzer)

> 一个 Claude Code skill — 基于英汉语法默认值的认知差异框架，提供文本分析、名词化解冻、语言对比、L1 干扰诊断与概念讲解五种模式。

## 概述

这个 skill 让 Claude 能够**使用"语言默认值"框架分析英中文本的深层认知结构**。它不是教语法，而是提供一套分析语言认知框架的元工具：

1. **analyze（文本分析）** — 分析任何英中段落中运作的语言默认值
2. **thaw（名词化解冻）** — 将名词密集的英文"解冻"，恢复施事和动词化表达
3. **contrast（翻译对照）** — 分析中英翻译对中两套默认值的张力
4. **diagnose（L1 干扰诊断）** — 诊断中文母语者英文中的默认值转移
5. **explain（概念讲解）** — 讲解框架中的六个默认值概念

## 使用方法

在 Claude Code 中调用：

```
/language-defaults analyze 这段英文/中文
/language-defaults thaw 「The implementation of the policy resulted in a reduction...」
/language-defaults contrast 「中英翻译对」
/language-defaults diagnose 「中文母语者的英文段落」
/language-defaults explain 「什么是语法隐喻」
```

## 六种语言默认值

| # | 默认值 | 说明 |
|---|--------|------|
| 1 | **主语强制** (Subject Obligation) | 英语每个定式分句必须有主语；汉语允许无主句 |
| 2 | **冠词个体化** (Article Individualization) | 英语强制标记有定/无定和可数/不可数；汉语无冠词 |
| 3 | **时间外置** (Externalized Time) | 英语强制时态标记；汉语使用体标记（了/着/过） |
| 4 | **名词化/语法隐喻** (Nominalization) | 英语学术文体将动词凝固为名词；汉语保持动词形式 |
| 5 | **话题优先 vs 主语优先** (Topic-Prominence) | 汉语话题-评论结构；英语主语-谓语结构 |
| 6 | **系动词统一** ("be" Convergence) | 英语一个 "be" 覆盖是/有/在/很；汉语分开对应 |

## 核心原则

- **描述差异，不评价优劣**：不说"汉语 lacks 英语 has"，说"英语 obligates 汉语 permits"
- **学术锚定**：每个主张来源清晰（Benveniste / Li & Thompson / Halliday / Biber）
- **默认值不是牢笼**：就像怀特海用英语写出了过程哲学——换得动，只是换的成本不落在记忆量上
- **词汇量是内容；默认值这一层，从来不出现在任何一张卷子上**

## 基于

刚老师《下雨了》原文框架：[知乎专栏](https://zhuanlan.zhihu.com/p/2064716290741351136)

> *"It's raining 里的 it 不指任何东西，但它必须在。语法书讲到这里就停了：记住这个用法，别把 it 漏掉。至于英语为什么非要有个东西在那儿，我没见过哪本教材问。"*

## 目录结构

```
language-defaults/
├── SKILL.md                       # 技能定义（完整框架 + 五种模式）
├── README.md                      # 本文件
```

## 边界

- 不做语法检查器（不改拼写/主谓一致）
- 不做翻译工具（分析翻译但不生成翻译）
- 不做强 Whorfian 框架（不说"语言决定思维"）
- 不处理非自然语言输入（代码、数学）
- 6 个默认值是英中对照特化，不适用于所有语言对

## License

MIT
