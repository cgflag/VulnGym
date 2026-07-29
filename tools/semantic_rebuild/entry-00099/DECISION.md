# DECISION — entry-00099

## 采用

- **entry_point**：保留 `workflows.controller.ts:539` `@Post('/:workflowId/run')`
- **critical_operation**：`expression-evaluator-proxy.ts:19-21` `evaluateExpression`
- **verify**：0

## 拒绝

| 候选 | 为何拒绝 |
|------|----------|
| PrototypeSanitizer 定义 :244 | Issue #6 点名：RCE sink 不应落在 sanitizer；补丁加的是 visitWithStatement，说明缺口在 visitor 覆盖，但 critical 应是执行成立点 |
| Tournament 构造 :9-12 | #77 做法；构造沙箱 ≠ 用户表达式获得 RCE |
| 仅 regex :442 | 漏检环节，放 trace |

## 补丁锚点

`n8n@2.5.1` 的 `expression-sandboxing.ts` 出现：

```ts
visitWithStatement() {
  throw new ExpressionWithStatementError();
}
```

证明漏洞窗口缺少对 `with` 的 AST 处置；与 JFrog CVE-2026-1470 一致。
