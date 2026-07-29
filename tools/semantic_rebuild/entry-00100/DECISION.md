# DECISION — entry-00100

## 采用

- **entry_point**：保留 `expression.ts:368` `resolveSimpleParameterValue`（同 advisory 的 API 入口视角）
- **critical_operation**：与 00099 相同 — `evaluateExpression:19-21`
- **verify**：0

## 拒绝

| 候选 | 为何拒绝 |
|------|----------|
| sanitizer 函数定义 :330-336 | 原标注；防御实现，逃逸成功时往往根本不被调用 |
| defineProperty(__sanitize) :434 | 防御装配；可进 trace，不作 critical |
| 改 entry_point 为 HTTP run | 会与 00099 同质化；本条保留参数求值入口更有信息量 |

## 与 00099 的分工

同一 GHSA 两条 entry：00099 强调网络入口 + with/Identifier 缺口；00100 强调参数求值装配链。共享真实 RCE sink。
