# entry-00176

## 采用

- entry_point：`Code.node.ts:206`，Python 分支读 `pythonCode`
- critical：`task_analyzer.py:66-69`，`node.attr in BLOCKED_ATTRIBUTES`
- verify：0

## 不采用

- `constants.py` 里 `BLOCKED_ATTRIBUTES = {`：静态列表，Issue 点名不要当 critical。补丁改集合，但「放行/拦截」发生在成员判断。
- 单独把 name-mangle（71–74 行）当 critical：对纯 `__objclass__` 本身就不触发，只能说明第二条线也帮不上忙。

## 补丁对照

漏洞 commit（2.9.2）集合里没有 `__objclass__`；`n8n@2.10.1` 同文件已加上。

## 校验

`run_verify_batch.py entry-00176` 已通过。细节见 `PATCH_NOTES.md`、`VERIFY.md`。
