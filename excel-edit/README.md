# 安全高效编辑 Excel 工作簿

统一调用：`$excel-edit`，保留自动选择。

日常定点修改使用现成编辑器，按实际改动验证。无公式普通 XLSX 使用轻量方式；有公式、外链或 VBA 使用 Microsoft Excel。严格保护、迁移或可搬迁多文件交付使用专项验收。公式或外链本身不触发完整审计。

- 入口与选择：[SKILL.md](SKILL.md)。
- 编辑计划：[references/edit-plan.md](references/edit-plan.md)。
- 严格验收：[references/strict-audit.md](references/strict-audit.md)。
- 本机依赖：[references/python-runtime.md](references/python-runtime.md)。
- 维护验证：[references/maintenance-cases.md](references/maintenance-cases.md)。

所有 Python 操作使用 scripts/excel-python.cmd。原生功能需要 Windows 桌面 Excel、openpyxl、pywin32 和 lxml。暂存文件验收成功且原件未并发变化后才替换；不把未完成验证报告为通过。项目专属数值设计规则仍由项目规范决定。
