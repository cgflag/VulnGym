## 关联 Issue：#6

### 范围（先说清楚）

只改了官方优先样本里的 **3 条**：`entry-00099`、`entry-00100`、`entry-00176`。  
`00103` / `00511` / `00512` **没有**做完，不声称 Issue 已全部解决。Issue 允许先交可靠子集。

### 改了什么

| entry | 原来的 critical | 现在的 critical |
|-------|-----------------|-----------------|
| 00099 | `PrototypeSanitizer` 函数定义 | `evaluateExpression`（真正执行出口） |
| 00100 | `sanitizer` 函数定义 | 同上（同 advisory，入口/trace 不同） |
| 00176 | `BLOCKED_ATTRIBUTES = {` 静态集合 | `visit_Attribute` 里 `in BLOCKED_ATTRIBUTES` 的判断 |

每条的原问题、选用理由、未采用点见 `tools/semantic_rebuild/out/NOTES.md`。  
`{file,line,code}` 已在对应 commit 上对过源码（`run_verify_batch.py`）。  
`verify` 仍为 0。未直接改 `data/entries.jsonl`。

### 交付文件

- `tools/semantic_rebuild/out/entries.fixed.jsonl`
- `tools/semantic_rebuild/out/semantic_diff.csv`
- `tools/semantic_rebuild/out/NOTES.md`
- 各 entry 下 `BEFORE.json` / `AFTER.json` / `DECISION.md`
- `verify_nodes.py`、`run_verify_batch.py`

### 和已有 PR

结论方向和 [#54](https://github.com/Tencent/VulnGym/pull/54) 接近。本 PR 侧重：可跑的源码核对、写清拒绝项、不改 `verify`、不把 Tournament 构造标成 critical（[#77](https://github.com/Tencent/VulnGym/pull/77)）。

### 复现

```bash
python tools/semantic_rebuild/run_verify_batch.py entry-00099 entry-00100 entry-00176
python tools/semantic_rebuild/build_deliverables.py
```
