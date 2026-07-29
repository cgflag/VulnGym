# VERIFY — entry-00176

## Checkout

```text
repo: D:\postgraduate\main-line\Job\Tencent\VulnGym\.cache\repos\n8n
HEAD: 3af9095245be3aaad6bc16622f379f79c6c6068f
```

## 自动校验

```bash
python tools/semantic_rebuild/verify_nodes.py \
  --repo .cache/repos/n8n \
  --nodes tools/semantic_rebuild/entry-00176/AFTER.json
```

结果：**pass=true**（entry_point / critical_operation / 3×trace 全部 code 对齐；比较前做了行尾空白归一化）。

## 红队自攻记录

| ID | 质疑 | 处理 |
|----|------|------|
| R1 | 竞品也标 task_analyzer，无差异？ | 补丁证据 + 拒静态表的 Issue 依据 + name-mangle 无效证明；原数据其实把 visit_Attribute 放在 trace[5] 却把 critical 放错——我们是「纠正角色」不是瞎换文件 |
| R2 | 补丁只改 constants，critical 是否应跟补丁文件？ | Issue 明确 critical≠静态声明；补丁文件≠critical 文件是合理的 |
| R3 | verify 是否应改 1？ | **否**；保持 0 |
| R4 | 是否标太晚到 exec？ | 本漏洞是 AST 校验缺口；卡在 validate/visit_Attribute 更贴 GHSA「sandbox did not sufficiently restrict」 |

## 状态

- [x] ADVISORY / CANDIDATES / DECISION / PATCH_NOTES / BEFORE / AFTER / VERIFY  
- [ ] 合并进完整 entry patch JSONL（等第二条闭环后一起打）  
- [ ] 未开 PR、未认领  
