## 关联 Issue：#6

### 范围

官方优先的 6 条 n8n 样本都改了：`00099 / 00100 / 00103 / 00176 / 00511 / 00512`。  
`verify` 仍为 0。未直接改 `data/entries.jsonl`。

### 改动摘要

| entry | 主要修正 |
|-------|----------|
| 00099 | critical：PrototypeSanitizer 定义 → `evaluateExpression` |
| 00100 | critical：sanitizer 定义 → `evaluateExpression` |
| 00103 | entry：`}` → `setResponseHeaders`；critical 保留漏 `trim` |
| 00176 | critical：静态黑名单 → `visit_Attribute` 成员判断 |
| 00511 | critical：native 回退选出函数 → `.apply` 执行 |
| 00512 | critical 位置保留（可写 `__sanitize`）；收紧 desc / trace 行号 |

说明与拒绝项：`tools/semantic_rebuild/out/NOTES.md`。  
校验：`python tools/semantic_rebuild/run_verify_batch.py`（6 条 pass）。

### 交付

- `out/entries.fixed.jsonl`、`out/semantic_diff.csv`、`out/NOTES.md`
- 各 entry：`BEFORE.json` / `AFTER.json` / `DECISION.md`
- `verify_nodes.py`、`run_verify_batch.py`

### 和已有 PR

方向与 [#54](https://github.com/Tencent/VulnGym/pull/54) 接近；本 PR 带可复现核对，且不改 `verify`、不用 Tournament 构造当 critical。
