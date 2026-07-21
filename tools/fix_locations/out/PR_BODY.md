# 关联 Issue：#4

## 问题是什么？

`data/entries.jsonl` 中部分节点的 `line`/`file` 与对应 commit 上的 `code` 对不齐。不确定时不能猜，否则会引入新的错误标注。

## 做了什么？

- 新增 `tools/fix_locations/`：按官方顺序  
  **原位置 → 邻域 ±5 → 原文件全文**（全仓库搜索有开关，本 PR **默认关闭**，可作为后续 PR）。
- 仅**唯一命中**时改 `file`/`line`；多命中 / 找不到 / 退化片段（如单独 `}`）写入 `needs_human.csv`。
- 交付：`entries.fixed.jsonl`、`fix_diff.csv`、`needs_human.csv`、README、单元测试与校验脚本。
- **不修改**仓库中的 `data/entries.jsonl`（官方要求提交修复后的 JSONL，未要求直接改主数据；是否合入由维护者决定）。另附高置信小子集，便于择优合入。

## 和已有 PR 的关系

| PR | 说明 |
|----|------|
| #35 / #39 | 偏保守（约十几处）。与我们的**真行偏移**部分高度一致。 |
| #41 / #43 | 修复数量同档（约百处）。差异主要在：是否把「多行 `code`、原先只标起始行」扩成 `N-M` 也算自动修复。 |
| #49 | 做人审写回；本 PR **不重复实现**。已提供 `needs_human.for_49.csv` + `COMPAT_WITH_49.md`，并对 #49 `init` 做过冒烟（见 `COMPAT_49_SMOKE.md`）。 |

**数字解读：** 自动修复 102 处 = 90 处「扩成行范围」+ 12 处「行号真的偏了」。  
与 #35/#39 修复集合相交约 12 处；与 #41 相交约 94 处。详见 `tools/fix_locations/out/OVERLAP_ANALYSIS.md`。

## 本 PR 额外提供的实用件

1. **修复集合对照报告**（`out/OVERLAP_ANALYSIS.md`）  
2. **独立校验脚本**（`scripts/verify_location_outputs.py`）：schema、与 diff 一致性、抽查幂等  
3. **高置信子集**：12 处多份 PR 共同覆盖的真偏移 → `out/entries.high_confidence.jsonl`（5 条 entry）  
4. 退化片段不自动当修好；Windows 长路径问题说明见 `out/FETCH_FAILED_NOTE.md`  
5. **desc 机械同步**：仅替换明确行号锚点 → `entries.fixed.desc_synced.jsonl`（本批 10 处，全在 `entry-00458`；不覆盖 `entries.fixed.jsonl`）  
6. **对接 #49**：`export_queue_for_49.py` 默认剔除 `fetch_failed`；与 #49 apply 内 desc 同步可并存（产物分文件）

## 结果摘要

- 408 entries；自动修复 102；人工队列见 `needs_human.csv`（导出 `needs_human.for_49.csv` 供人审）
- desc 机械同步：would_update **10** / no_anchor 92
- 测试通过；校验脚本通过；抽查记录见 `out/SPOTCHECK_AUTO.md`
- 全仓库搜索、LLM 猜位置：本 PR **不做**（留给后续）

## 复现

```bash
python -m unittest discover -s tools/fix_locations/tests -v
python tools/fix_locations/scripts/verify_location_outputs.py
python tools/fix_locations/scripts/desc_sync_apply.py
python tools/fix_locations/scripts/export_queue_for_49.py
```

热缓存下全量：

```bash
python -u tools/fix_locations/fix_code_locations.py --all --apply
```
