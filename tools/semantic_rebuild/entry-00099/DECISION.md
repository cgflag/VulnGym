# entry-00099

## 采用

- entry_point：`workflows.controller.ts:539` `@Post('/:workflowId/run')`（原标注可用）
- critical：`expression-evaluator-proxy.ts:19-21` `evaluateExpression`
- verify：0

## 不采用

- `PrototypeSanitizer` 定义：防御钩子，不是执行点；Issue 也不认可 RCE critical 落在 sanitizer 上。
- Tournament 构造：只是挂上钩子，不是用户表达式跑起来的地方。
- `.constructor` 正则：漏检，放进 trace。

## 补丁对照

`n8n@2.5.1` 在 sandboxing 里加了 `visitWithStatement()` 直接抛错，说明漏洞版本缺的是对 `with` 的处理。
