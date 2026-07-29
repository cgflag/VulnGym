# Issue #6 CROSS_PR_MATRIX（骨架 → 随深挖填充）

> 目的：与竞品对话，避免平行宇宙。  
> 状态：初稿 2026-07-30；完整字段对比待 checkout 后补。

## 竞品 PR 清单（#6 关联，抽样）

| PR | 作者 | 策略摘要（来自 PR 描述） | 红队初判 |
|----|------|--------------------------|----------|
| [#54](https://github.com/Tencent/VulnGym/pull/54) | phx3334 | 00176→`task_analyzer` 黑名单判断；00099/100→`evaluateExpression`；00103→`setResponseHeaders`；00511→`apply` 执行点 | 方向「离开防御定义、走向施力/执行点」正确；需用 fix patch 核实 |
| [#77](https://github.com/Tencent/VulnGym/pull/77) | perhaps468 | 00099/100→`Tournament` 构造；00176→`task_analyzer` 判断；自称 validate 把 **verify=1** | **高风险**：Tournament 构造未必是 RCE sink；**擅自 verify=1 可能违反 SCHEMA 语义** |
| [#55](https://github.com/Tencent/VulnGym/pull/55) / [#46](https://github.com/Tencent/VulnGym/pull/46) / [#38](https://github.com/Tencent/VulnGym/pull/38) 等 | 多人 | 同类语义修正 | 深挖时按 entry 填冲突格 |

## 按 entry 对照（P0 优先）

### entry-00176（Python `__objclass__` 沙箱）— **已本地定稿（AFTER 校验通过）**

| 来源 | critical_operation | 立场 |
|------|--------------------|------|
| 原数据 | `constants.py:126 BLOCKED_ATTRIBUTES = {` | **拒绝作 critical**（Issue：非静态声明）。降为 trace「缺 `__objclass__`」 |
| PR #54 / #77 | `task_analyzer` 黑名单判断 | **同向**；我们采用 `66-69` 成员判断 |
| 我们 | 同上 + 证据包 | 2.9.2 无 `__objclass__`；`n8n@2.10.1` 已加；name-mangle 对纯 dunder 不触发；`verify=0`；**不**学 #77 改 verify=1 |

详见 `entry-00176/DECISION.md` + `VERIFY.md`。

### entry-00099 / entry-00100（表达式沙箱 RCE）— **已本地定稿（AFTER 校验通过）**

| 来源 | critical_operation | 立场 |
|------|--------------------|------|
| 原 00099 | `PrototypeSanitizer` 定义 | **拒绝**：防御 hook，不是 RCE sink |
| 原 00100 | `sanitizer` 函数 | **拒绝**：防御实现；Issue 已点名 |
| PR #77 | `Tournament` evaluator 构造 | **拒绝**：构造 ≠ 执行 sink；且擅自 verify=1 |
| PR #54 | `evaluateExpression` | **同向采用**；我们额外：正则漏检 + visitMemberExpression 缺口进 trace；`n8n@2.5.1` visitWithStatement 补丁锚点 |
| 我们 | `evaluateExpression:19-21` | 00099/00100 共享 sink、不同 entry/trace；verify=0 |

## 选拔者视角：我们要比竞品多交出什么

1. 不把 `verify` 改成 `1`（除非维护者明示）。  
2. 每个 REJECTED 候选写清「为何看起来像、为何不是」。  
3. Fix patch / 测试锚定。  
4. 只深挖 2 条，报告密度高于「6 条表格式改写」。

## 更新日志

- 2026-07-30：骨架建立；锁定对 #77 verify=1 与 Tournament-as-critical 的质疑。
