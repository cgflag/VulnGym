## 关联 Issue：#6

### 做了什么

对官方优先 n8n 样本中的 **3 条**做语义重标（非整库脚本、不碰 `verify`）：

| entry | 原 critical 问题 | 新 critical |
|-------|------------------|-------------|
| entry-00099 | PrototypeSanitizer **定义** | `evaluateExpression`（Tournament 执行出口） |
| entry-00100 | sanitizer **函数定义** | 同上（同 advisory 姊妹条，不同 entry/trace） |
| entry-00176 | `BLOCKED_ATTRIBUTES` **静态集合** | `visit_Attribute` 成员判断施力点 |

交付：

- `tools/semantic_rebuild/out/entries.fixed.jsonl` — 3 条完整 entry
- `tools/semantic_rebuild/out/semantic_diff.csv`
- `tools/semantic_rebuild/out/NOTES.md` — 每条原问题/理由/拒绝候选
- 各 entry 目录：`BEFORE.json` / `AFTER.json` / `DECISION.md` / `VERIFY.md`
- `tools/semantic_rebuild/verify_nodes.py` + `run_verify_batch.py` — code 级对齐校验

**不修改** 仓库根 `data/entries.jsonl`（由维护者择优合入）。

### 与已有 #6 PR

- 方向对齐 [#54](https://github.com/Tencent/VulnGym/pull/54)「离开 sanitizer/静态表」。
- **不采用** [#77](https://github.com/Tencent/VulnGym/pull/77) 将 Tournament 构造当 critical，以及 `verify=1`。
- 差异：补丁锚点（`n8n@2.5.1` `visitWithStatement`；`n8n@2.10.1` `__objclass__`）、REJECTED 表、可复现 VERIFY。

### 复现

```bash
python tools/semantic_rebuild/run_verify_batch.py entry-00099 entry-00100 entry-00176
python tools/semantic_rebuild/build_deliverables.py
```

### 明确不做

- 不把本 PR 与 #4 定位脚本混装
- 本批不含 00103/00511/00512（可后续增量）
