# Technical sources

Use these primary sources when technical behavior needs confirmation. Access dates and product behavior may change; recheck online for high-risk work.

- Microsoft Learn, `Application.CalculateFullRebuild`: full calculation of all open workbooks and dependency rebuild. https://learn.microsoft.com/en-us/office/vba/api/excel.application.calculatefullrebuild
- Microsoft Learn, `Application.CalculationState`: read-only calculation-state check and `xlDone`. https://learn.microsoft.com/en-us/office/vba/api/excel.application.calculationstate
- Microsoft Learn, `Application.AutomationSecurity`: programmatic-open macro security and restoring the prior setting. https://learn.microsoft.com/en-us/office/vba/api/excel.application.automationsecurity
- Microsoft Learn, `Workbooks.Open`: explicit `UpdateLinks` and `ReadOnly` behavior; programmatic macro warning. https://learn.microsoft.com/en-us/office/vba/api/excel.workbooks.open
- Microsoft Support, workbook link management and storage: relative/absolute path storage and the fact that formula-bar display may differ from stored paths. https://support.microsoft.com/en-us/excel/description-of-workbook-link-management-and-storage-in-excel
- Microsoft Support, create workbook links: source/destination behavior and formula path changes when sources close. https://support.microsoft.com/en-us/excel/create-workbook-links
- Microsoft Learn, Excel calculation performance: calculation-chain restructuring and calculation design. https://learn.microsoft.com/en-us/office/vba/excel/concepts/excel-performance/excel-improving-calculation-performance
- Microsoft Learn, performance obstructions: linked-workbook opening order, bounded ranges, structured references, helper calculations, and volatile-function costs. https://learn.microsoft.com/en-us/office/vba/excel/concepts/excel-performance/excel-tips-for-optimizing-performance-obstructions
