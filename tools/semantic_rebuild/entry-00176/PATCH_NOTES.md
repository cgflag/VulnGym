# PATCH_NOTES — entry-00176

## Vuln snapshot

- Commit: `3af9095245be3aaad6bc16622f379f79c6c6068f`（Release 2.9.2）
- `BLOCKED_ATTRIBUTES`：**无** `__objclass__`

## Patched reference

- Tag: `n8n@2.10.1`（advisory 修复线之一）
- 同文件集合中 **新增** `"__objclass__",`（位于 `__self_class__` 与 introspection 段之间）

## 含义（给选拔者）

补丁改的是策略集合；**运行时是否逃逸**取决于 `visit_Attribute` 的 `node.attr in BLOCKED_ATTRIBUTES` 是否报违例。  
因此：

- 把 critical 放在集合字面量 = 描述「缺了什么数据」  
- 把 critical 放在成员判断 = 描述「校验如何失败」← Issue #6 要求的语义

## 命令备忘

```text
git -C .cache/repos/n8n show 3af9095245:packages/@n8n/task-runner-python/src/constants.py
git -C .cache/repos/n8n show n8n@2.10.1:packages/@n8n/task-runner-python/src/constants.py
```
