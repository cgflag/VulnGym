# 校验 — 00099 / 00100

```bash
python tools/semantic_rebuild/run_verify_batch.py entry-00099 entry-00100
```

commit：`8ab4492e8c0b743455e51fc111441d8d5010a6ad`  
结果：pass

说明：critical 和 #54 一样落在 evaluateExpression。多出来的是 trace 里把正则漏检和 MemberExpression-only 写清楚，以及不改 verify、不把 Tournament 构造当 critical。
