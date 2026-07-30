# entry-00100

## 采用

- entry_point：`expression.ts:368` `resolveSimpleParameterValue`（参数侧入口，和 00099 的 HTTP 入口分开）
- critical：同 00099，`evaluateExpression:19-21`
- verify：0

## 不采用

- `sanitizer` 函数定义：防御实现；绕过成功时经常调不到。
- `defineProperty(__sanitize)`：装配防御，不是 sink。
- 把 entry 改成和 00099 一样的 HTTP 路由：两条会挤在一起。

## 和 00099

同一 GHSA。差别在入口和 trace，不在强行换一个「看起来不同」的 critical。
