# NOTES — Issue #6 语义修复说明（entry-00099 / 00100 / 00176）

> 范围：官方优先样本中的 **3 条高质量定稿**（保底策略）。  
> `entry-00103 / 00511 / 00512` 未纳入本批：避免与 `#4/#5` 定位/顺序问题纠缠；可后续增量。  
> **不修改** `verify`（保持 0）。**不直接改** 主仓 `data/entries.jsonl`（提交片段 + 说明，由维护者择优合入）。

## 通用原则

1. RCE / 沙箱逃逸的 `critical_operation` **不得**落在 sanitizer 定义或静态黑名单字面量上（Issue #6 原文）。  
2. `critical_operation` 指向「漏洞成立的施力/执行点」；防御缺口可进 `trace` 并写明「非 critical」。  
3. 每个节点 `{file,line,code}` 已对对应 commit 跑通 `verify_nodes.py`（见各 `VERIFY.md` / `run_verify_batch.py`）。  
4. 证据：JFrog CVE-2026-1470 分析、GHSA、修复 tag（`n8n@2.5.1` 增加 `visitWithStatement`；`n8n@2.10.1` 增加 `__objclass__`）。

---

## entry-00099 — Expression Sandbox Escape（with + Identifier constructor）

| 项 | 内容 |
|----|------|
| Advisory | GHSA-5XRP-6693-JJX9 / CVE-2026-1470 |
| Commit | `8ab4492e8c0b743455e51fc111441d8d5010a6ad` |
| **原问题** | `critical_operation` 落在 `PrototypeSanitizer` **定义**（expression-sandboxing.ts:244）。这是防御钩子，不是 RCE 执行点。 |
| **修复** | `critical` → `expression-evaluator-proxy.ts:19-21` `evaluateExpression`（Tournament.execute 公共出口）。`entry_point` 保留 HTTP `@Post('/:workflowId/run')`。 |
| **理由** | with 逃逸使 Identifier `constructor` 解析为 `Function` 后，任意代码在此落地。 |
| **拒绝** | PrototypeSanitizer 定义（Issue 点名）；Tournament 构造函数体（#77，基础设施≠sink）；仅 regex 漏检单独作 critical（属上游漏检，放 trace）。 |
| **trace 要点** | 剥离表达式 → `.constructor` 正则漏检 → 钩子注册（无 WithStatement）→ `visitMemberExpression` 缺口上下文 → renderExpression。 |

## entry-00100 — 同 advisory 姊妹条（参数求值路径）

| 项 | 内容 |
|----|------|
| Advisory | 同上 |
| Commit | 同上 |
| **原问题** | `critical_operation` 落在 `sanitizer` **函数定义**（330-336）。防御实现，非执行 sink。 |
| **修复** | `critical` → 同一 `evaluateExpression:19-21`。`entry_point` 保留 `resolveSimpleParameterValue`（相对 00099 的 API 层入口）。 |
| **理由** | 无论 with 路径还是 sanitizer 绑定被绕过，最终执行仍经 Tournament.execute。两条 entry 用不同 entry/trace 区分入口与旁路上下文，共享真实 sink。 |
| **拒绝** | sanitizer 定义作 critical；不把 `Object.defineProperty(__sanitize)` 升为 critical（装配点，非 RCE）。 |
| **trace 要点** | defineProperty 装配 → 正则漏检 → sanitizer 定义（降级上下文）→ renderExpression。 |

## entry-00176 — Python `__objclass__` 沙箱逃逸

| 项 | 内容 |
|----|------|
| Advisory | GHSA-MMGG-M5J7-F83H |
| Commit | `3af9095245be3aaad6bc16622f379f79c6c6068f`（2.9.2） |
| **原问题** | `critical` 落在 `constants.py:126` `BLOCKED_ATTRIBUTES = {` 静态集合。 |
| **修复** | `critical` → `task_analyzer.py:66-69` `node.attr in BLOCKED_ATTRIBUTES` 成员判断。`entry_point` → Code.node.ts:206 读取 `pythonCode`。 |
| **理由** | Issue：critical ≠ 静态声明；补丁虽改集合，施力点是 visit_Attribute 判定。name-mangle 对纯 `__objclass__` 不触发（见 DECISION/PATCH_NOTES）。 |
| **拒绝** | 静态集合作 critical；单独把 name-mangle 作 critical；`verify=1`（学 #77 的做法）。 |

---

## 与竞品差异（摘要）

详见 `CROSS_PR_MATRIX.md`。

- 对齐 #54 的「离开 sanitizer/静态表 → 施力/执行点」方向。  
- **拒绝 #77** 将 Tournament 构造当 critical，以及擅自 `verify=1`。  
- 额外交付：每条 AFTER 的 code 级 VERIFY、补丁锚点、REJECTED 候选理由。
