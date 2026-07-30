# 和其它 #6 PR 的对照

| PR | 做法（据其描述） | 我们怎么看 |
|----|------------------|------------|
| [#54](https://github.com/Tencent/VulnGym/pull/54) | 00099/100→`evaluateExpression`；00176→`task_analyzer` 判断；还改了 00103/511/512 | 主结论同向；它覆盖更全。我们多的是核对脚本和拒绝项说明，不是另起一套 sink。 |
| [#77](https://github.com/Tencent/VulnGym/pull/77) | 00099/100→Tournament 构造；并把 verify 改成 1 | Tournament 构造不宜当 RCE critical；verify=1 应留给人工确认，本 PR 不改。 |

## 本 PR 三条

| entry | 原 critical | 现 critical |
|-------|-------------|-------------|
| 00099 | PrototypeSanitizer 定义 | evaluateExpression |
| 00100 | sanitizer 定义 | evaluateExpression |
| 00176 | BLOCKED_ATTRIBUTES 字面量 | task_analyzer 成员判断 |
