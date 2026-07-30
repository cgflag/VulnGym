# Issue #6 修复说明（entry-00099 / 00100 / 00176）

对照 [Issue #6](https://github.com/Tencent/VulnGym/issues/6) 的交付要求：每条写清原问题、改到哪里、为什么选、为什么不选其它点；并附 diff。

本 PR **只交这 3 条**。官方优先列表里的 `00103 / 00511 / 00512` 还没做完，不装作已经覆盖。Issue 也写了：不要求一次改完所有 n8n 样本，但交出去的必须靠得住。

未改 `verify`（仍为 0）。未改仓库里的 `data/entries.jsonl`，只提供 `out/entries.fixed.jsonl` 片段。

每条节点的 `{file,line,code}` 都在对应 commit 上用 `verify_nodes.py` 对过源码。

---

## entry-00099（GHSA-5XRP-6693-JJX9，commit `8ab4492e`）

**原问题**  
`critical_operation` 标在 `PrototypeSanitizer` 的函数定义上。这是 AST 防御钩子，不是表达式真正跑起来的地方。Issue 里点名过：RCE 样本的 critical 落在 sanitizer 上不合理。

**改动**  
- `entry_point`：仍用 `workflows.controller.ts:539` 的 `@Post('/:workflowId/run')`（外网可达入口，够用）。  
- `critical_operation`：改为 `expression-evaluator-proxy.ts:19-21` 的 `evaluateExpression`（内部绑到 `tournamentEvaluator.execute`）。  
- `trace`：保留「剥表达式 → `.constructor` 正则 → 注册钩子 → 只处理 MemberExpression 的缺口 → renderExpression」；把 sanitizer **定义**从 critical 挪进 trace，并写明不是 critical。

**为什么选 evaluateExpression**  
CVE-2026-1470 的利用是 `with` + 裸 `constructor` Identifier，逃过 MemberExpression 检查后，代码仍要在 Tournament 里执行。`evaluateExpression` 是这条链上公开、稳定的执行出口。

**为什么不选**  
- `PrototypeSanitizer` 定义：缺口在「没处理 WithStatement / 没拦 Identifier」，但那是防御缺位，不是 sink。修复版 `n8n@2.5.1` 加的是 `visitWithStatement()`，也说明问题在 visitor 覆盖，不等于该把 critical 钉在函数签名上。  
- Tournament 构造处（有人 PR 这么标）：构造沙箱 ≠ 用户表达式拿到 RCE。  
- 单独把正则漏检当 critical：只是上游漏检，放进 trace。

参考：[JFrog 对 CVE-2026-1470 的说明](https://research.jfrog.com/post/achieving-remote-code-execution-on-n8n-via-sandbox-escape/)。

---

## entry-00100（同一 advisory，同一 commit）

**原问题**  
`critical_operation` 标在 `sanitizer` 函数体上。这是运行时属性键检查的实现；逃逸成功时往往根本走不到这里。

**改动**  
- `entry_point`：仍用 `expression.ts:368` `resolveSimpleParameterValue`（参数求值入口；和 00099 的 HTTP 入口互补）。  
- `critical_operation`：与 00099 相同，落到 `evaluateExpression`。  
- `trace`：`defineProperty(__sanitize)`、正则、sanitizer 定义（降为上下文）、`renderExpression`。

**为什么两条 entry 可以共用同一个 critical**  
数据集里同一 GHSA 拆两条，本来就允许不同入口视角。sink 相同不矛盾；差别应在 entry / trace，而不是硬拆两个「假不同」的 critical。

**为什么不选**  
- sanitizer 定义：见上。  
- `Object.defineProperty(__sanitize)`：防御装配，不是执行点。  
- 把 entry 也改成 HTTP run：会和 00099 撞车，信息量更少。

---

## entry-00176（GHSA-MMGG-M5J7-F83H，commit `3af90952` / 2.9.2）

**原问题**  
`critical_operation` 标在 `constants.py` 里 `BLOCKED_ATTRIBUTES = {`。这是静态集合字面量，Issue 明确说不要把 critical 放在静态列表上。

**改动**  
- `entry_point`：`Code.node.ts:206`，在 Python 分支用 `getNodeParameter` 读用户脚本。  
- `critical_operation`：`task_analyzer.py:66-69`，`node.attr in BLOCKED_ATTRIBUTES` 时是否报违例。  
- `trace`：构造 sandbox、集合定义（写明「缺 `__objclass__`，非 critical」）、name-mangle 启发式（对纯 `__objclass__` 不触发）。

**为什么选成员判断而不是集合字面量**  
补丁（如 `n8n@2.10.1`）确实是往集合里加 `__objclass__`，但「放没放过」发生在 `visit_Attribute` 的成员判断。集合是数据，判断才是校验。

**为什么不选 name-mangle 当 critical**  
`split("__", 1)` 后对纯双下划线名首段为空，这条启发式本来就拦不住 `__objclass__`，只能当旁证。

---

## 和其它 #6 PR 的关系

[#54](https://github.com/Tencent/VulnGym/pull/54) 已经把 00099/100/176 推到相近结论（evaluateExpression / task_analyzer）。本 PR 不是「发明新 sink」，而是：

1. 把理由和拒绝项写清楚，方便人工复核；  
2. 源码对齐可复现（`run_verify_batch.py`）；  
3. 不把 `verify` 改成 1（[#77](https://github.com/Tencent/VulnGym/pull/77) 那样做我认为不合适）；  
4. 不把 Tournament 构造标成 critical。

若维护者更想一次合入 6 条整表，优先看 #54；本 PR 适合当「3 条带校验脚本的核对稿」。

---

## 怎么复现

```bash
python tools/semantic_rebuild/run_verify_batch.py entry-00099 entry-00100 entry-00176
python tools/semantic_rebuild/build_deliverables.py
```

产物：`out/entries.fixed.jsonl`、`out/semantic_diff.csv`、本说明。
