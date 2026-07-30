# entry-00103

## 采用

- entry_point：`webhook-request-handler.ts:146-154` `setResponseHeaders`（写入并读回 content-type）
- critical：`html-sandbox.ts:20` 只 `toLowerCase`、没有 `trim`
- verify：0

## 不采用

- 原 entry `webhook-helpers.ts:615` 的 `}`：不是语句，体现不了外部输入怎么进来。
- 把 critical 改到 setResponseHeaders：那里只是把脏 content-type 传下去；根因是判定函数缺 trim。

## 说明

这条是 CSP/XSS，不是 RCE。critical 落在「漏 trim」的判定上，和 Issue 说的「别把 RCE sink 标在 sanitizer 定义」不冲突。
