# DECISION — entry-00176

## 选拔者红队结论（本轮）

**采用：E1 + C2**；`verify` 保持 `0`。

### entry_point → E1

- `packages/nodes-base/nodes/Code/Code.node.ts:206`
- `code`: `\t\t\tconst code = this.getNodeParameter(codeParameterName, 0) as string;`
- **理由**：仅在 `isPyLang` 分支读取 `pythonCode`；是用户脚本进入 Python runner 管线的外部可控输入点。
- **拒绝 E2/E3**：构造与 validate 是后续内部步骤，放 trace。

### critical_operation → C2

- `packages/@n8n/task-runner-python/src/task_analyzer.py:66-69`（精确行以 VERIFY 脚本为准）
- **理由**：`visit_Attribute` 用 `BLOCKED_ATTRIBUTES` 决定是否报危险属性；漏洞窗口内 `__objclass__` 不在集合中 → **该判定放过** → AST 校验失败。这是「沙箱逃逸得以成立」的机制点。
- **拒绝 C1（原标注）**：Issue #6 点名静态列表；补丁虽向集合追加 `__objclass__`，但 critical 不应标在字面量定义行。
- **拒绝 C3 单独作 critical**：name-mangle 启发式对 `__objclass__` 本就不命中，属旁路未覆盖，不是主策略施力点。
- **对齐竞品**：与 PR #54 / #77 同向（task_analyzer 判断）；我们额外写清：补丁证据 + name-mangle 为何无效 + 拒 C1 的 Issue 依据。

### trace（草案，VERIFY 后定稿）

1. E1（可与 entry 重复或省略重复——倾向 trace 从 sandbox 构造起，避免与 entry 完全重复）  
2. `PythonTaskRunnerSandbox` / `validate` 调用  
3. C1 作为「策略缺 `__objclass__`」的 context 节点（desc 写明：非 critical）  
4. C2  

（最终节点以 AFTER.json 为准，删日志/无关返回值。）

### 仍待补

- [ ] `VERIFY.md`：code 字节级对齐 + 行号范围  
- [ ] `PATCH_NOTES.md`：记录 2.9.2 → 2.10.1 的 constants diff 摘录  
- [ ] AFTER.json  
- [ ] 是否需把 `getattr` 动态访问缺口写入 desc（若源码另有路径）— 读完 `task_analyzer` 其余 visit_* 再定
