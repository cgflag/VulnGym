# Issue #6 修复说明（6 条优先样本）

对照 [Issue #6](https://github.com/Tencent/VulnGym/issues/6)：每条写清原问题、改到哪、为什么选、为什么不选；附 diff。未改 `verify`（仍为 0）。未改仓库 `data/entries.jsonl`，只交 `out/entries.fixed.jsonl`。

节点 `{file,line,code}` 均在对应 commit 上用 `verify_nodes.py` 对过。

---

## entry-00099（GHSA-5XRP-6693-JJX9，`8ab4492e`）

**原问题**：critical 在 `PrototypeSanitizer` 定义上——防御钩子，不是执行点。  
**改动**：critical → `evaluateExpression`；entry 仍用 HTTP `@Post(.../run)`。  
**不选**：sanitizer 定义；Tournament 构造；单独把正则漏检当 critical。

## entry-00100（同一 advisory）

**原问题**：critical 在 `sanitizer` 函数体上。  
**改动**：critical 同 00099；entry 仍用 `resolveSimpleParameterValue`。  
**不选**：sanitizer 定义；`defineProperty(__sanitize)` 升 critical。

## entry-00103（GHSA-825Q-W924-XHGX，`57d6015f`）

**原问题**：entry 标在 `webhook-helpers.ts:615` 的 `}`，不是有效语句。  
**改动**：entry → `setResponseHeaders`（写头并读回 content-type）；critical 仍为 `html-sandbox.ts:20`（`toLowerCase` 前无 `trim`）。删掉 `}` 节点；streaming 行号改为 `606-615`。  
**不选**：把 critical 挪到 setResponseHeaders（那只是传脏值；根因是判定漏 trim）。  
**说明**：这是 CSP/XSS，critical 落在漏 trim 上合理。

## entry-00176（GHSA-MMGG-M5J7-F83H，`3af90952`）

**原问题**：critical 在 `BLOCKED_ATTRIBUTES = {` 静态集合。  
**改动**：critical → `visit_Attribute` 的 `in BLOCKED_ATTRIBUTES`；entry → 读 `pythonCode`。  
**不选**：静态集合作 critical；单独 name-mangle 作 critical。

## entry-00511（GHSA-6CQR-8CFR-67F8，`09e2c2b5`）

**原问题**：critical 在 native 回退「选出」`input[functionName]`，还没执行。  
**改动**：critical → `foundFunction.function.apply(...)`；entry 仍用 `data.extend = extend`。原回退分支放进 trace。  
**不选**：回退分支当 critical（只选函数）。

## entry-00512（同一 advisory）

**原问题**：critical 位置对（可写 `__sanitize`），desc / path.replace 行号可收紧。  
**改动**：critical 仍在 `reset.ts:46`；trace 里 path.replace 扩到完整语句 `493-504`；desc 写清「槽位可写导致过滤失效」。  
**不选**：把 critical 改成 PrototypeSanitizer 改写点或别的执行 sink——本条讲的是过滤被废掉。

---

## 和其它 PR

[#54](https://github.com/Tencent/VulnGym/pull/54) 六条结论方向一致。本 PR：源码核对可跑、拒绝项写清、不改 `verify`、不把 Tournament 构造当 critical（相对 [#77](https://github.com/Tencent/VulnGym/pull/77)）。

## 复现

```bash
python tools/semantic_rebuild/run_verify_batch.py
python tools/semantic_rebuild/build_deliverables.py
```
