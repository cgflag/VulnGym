# entry-00511

## 采用

- entry_point：`expression.ts:485` `data.extend = extend`（原标注可用）
- critical：`extend.ts:132-135` `foundFunction.function.apply(...)`
- verify：0

## 不采用

- 原 critical `82-84` native 回退：这里只是把 `input[functionName]` 选出来（functionName=`constructor` 时是 Function），还没有执行。
- 单独把正则漏检当 critical：extend 参数形式本来就不吃这正则。

## 和 00512

同一 GHSA。00511 走 extend→constructor→apply；00512 走可覆写的 `__sanitize` 槽位。
