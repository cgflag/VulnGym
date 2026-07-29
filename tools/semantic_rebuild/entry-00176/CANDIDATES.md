# CANDIDATES — entry-00176

## 已核实（vuln commit `3af9095245` = n8n 2.9.2）

- `constants.py` 的 `BLOCKED_ATTRIBUTES` **不含** `__objclass__`。  
- 修复 tag `n8n@2.10.1` 在同一集合中 **新增** `"__objclass__"`（证据：`git show n8n@2.10.1:.../constants.py`）。  
- 强制拦截点：`task_analyzer.py` `visit_Attribute`：`if node.attr in BLOCKED_ATTRIBUTES:`（约 L66–69）。  
- `__objclass__` 形式的 name-mangle 启发式（L71–74）对纯双下划线名 **不触发**（`split("__",1)` 后 `parts[0]==""`）。

## entry_point 候选

| ID | 位置 | 理由 | 初评 |
|----|------|------|------|
| E1 | `Code.node.ts:206` `getNodeParameter(codeParameterName, 0)` | Python 分支读取用户脚本；原标注 | **保留倾向**（已在 `isPyLang` 块内；L189 是 JS runner 分支，勿混） |
| E2 | `Code.node.ts:207` `PythonTaskRunnerSandbox(...)` | 沙箱对象构造 | 偏中间；弱于 E1 |
| E3 | `task_runner.py` `analyzer.validate(...)` | 校验入口 | 更像 trace |

## critical_operation 候选

| ID | 位置 | 理由 | 初评 |
|----|------|------|------|
| C1 | `constants.py:126` `BLOCKED_ATTRIBUTES = {` | 缺 `__objclass__` 的策略数据 | **拒绝作 critical**（Issue 明文：非静态声明；补丁虽改此处，但「漏洞成立」是校验放过） |
| C2 | `task_analyzer.py:66-69` 成员判断 | 实际「是否拦截属性访问」施力点；缺项导致此处漏报 | **首选** |
| C3 | `task_analyzer.py:71-74` name-mangle | 第二条启发式也未挡住 `__objclass__` | 可作 trace「旁路未覆盖」；不宜单点 critical（非主路径设计意图） |
| C4 | `TaskAnalyzer.validate` | Miggo 所称 vulnerable function | 入口包装；可进 trace |
| C5 | 用户代码真正 `exec`/`eval` 处 | 危险发生 | 需再读 `task_executor`；易标太晚，暂不作首选 |

## REJECT 预写（红队）

- **拒 C1**：看起来像根因（补丁改列表），但是 SCHEMA/Issue 语义下 critical = 链路中缺陷「起作用」的点；静态字面量不是执行/判定。列表缺项应在 **desc/trace** 说清。  
- **拒把 JS 的 L189 当 entry**：非 Python 路径。
