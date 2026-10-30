# medieval · 中世纪游戏中英本地化

用于中世纪与中世纪奇幻游戏的中英双向翻译、译文审校和术语维护。覆盖装备、身份爵位、战斗规则、物品说明、任务与角色对白。

参考《神界：原罪2 终极版》《Heads Will Roll: Reforged》《Wartales》《Stoneshard》的本机对齐与抽样记录，区分游戏原译、建议译法及项目已确认术语。参考版本与边界见 [reference-games.md](references/reference-games.md)。

## 使用

按仓库安装说明安装后，可直接提出请求：

```text
使用 $medieval 将这些装备名称译成中文，保留材质、结构和等级差异。
使用 $medieval 审校这批技能说明，检查触发条件、数值、变量和术语一致性。
使用 $medieval 将这段士兵对白译成自然英语，保留人物态度。
```

批量输入应保留 ID、原文及上下文；原文中的变量、标签和控制符保持不变。具体工作规则见 [SKILL.md](SKILL.md)。

## 附带资料与脚本

- [glossary.tsv](references/glossary.tsv)：145 条精选术语，保留来源证据、适用范围和状态；`proposed` 表示建议，不能当作项目已批准。
- [domain-guide.md](references/domain-guide.md)：装备、身份、战斗语义与自拟双向例句。
- [reference-games.md](references/reference-games.md)：四款游戏的版本边界、译法案例和迁移限制。
- [corpus.md](references/corpus.md)：可选的私人语料检索配置与格式说明。
- `scripts/check_localization.py`：检查 JSONL 中的字段、ID 冲突、占位符、标签和数值差异。
- `scripts/query_corpus.py`：只读检索自行准备的 SQLite 中英对照库。

脚本要求 Python 3.9 或更新版本，仅使用标准库。从仓库根目录执行格式检查：

```text
python -X utf8 medieval/scripts/check_localization.py translations.jsonl
```

每条输入至少包含 `id`（或 `key`）、`en` 和 `zh`。检查器以退出码 1 报告结构错误；数值、字符长度等问题提示人工复核。它不代替语义审校或游戏内显示验证。

## 私人语料

公开版本只包含规则、精选术语、少量例句和脚本，不附完整游戏文本、数据库、导出文件或编者的本机路径配置。无需私人数据库也可使用翻译规则、术语表与格式检查。

若已自行准备兼容的 SQLite 语料库，可指定路径检索：

```text
python -X utf8 medieval/scripts/query_corpus.py Guard --exact --db <自己的数据库路径>
```

也可按 [corpus.md](references/corpus.md) 创建 `references/local-corpus.json`。该配置和 `corpus/` 目录已加入本技能的 Git 忽略规则。缺少数据库时检索会明确报错，不会自动下载完整语料。
