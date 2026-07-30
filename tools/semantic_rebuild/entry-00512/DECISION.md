# entry-00512

## 采用

- entry_point：`expression.ts:524` `renderExpression`（原标注可用）
- critical：`reset.ts:46` `globalThis.__data.__sanitize = __sanitize`（普通赋值，可覆写）
- verify：0

## 不采用

- 把 critical 改成 PrototypeSanitizer 的 path.replace：那是编译期插入过滤调用；本路径失守点是运行时槽位可写。
- 改成 evaluate/apply 之类执行点：这条 entry 刻画的是「过滤被废掉」，不是另一条 RCE sink。

## 说明

位置与原数据相同，主要改 desc，并修正 trace 里 path.replace 的行号范围到完整语句（493-504）。
