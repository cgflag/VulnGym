# ADVISORY — entry-00176

- **GHSA**: [GHSA-mmgg-m5j7-f83h](https://github.com/advisories/GHSA-mmgg-m5j7-f83h)
- **CVE**: CVE-2026-27494
- **标题**：n8n has Arbitrary File Read via Python Code Node Sandbox Escape
- **VulnGym commit（漏洞快照）**：`3af9095245be3aaad6bc16622f379f79c6c6068f`
- **修复版本（advisory）**：1.123.22 / 2.9.3 / 2.10.1

## Impact（官方摘要）

已认证且能改 workflow 的用户，可通过 Python Code 节点逃逸沙箱：对某些内置对象属性限制不足 → 任意文件读 / RCE。需 `N8N_RUNNERS_ENABLED=true`。

## 机制理解（公开分析 + Issue 备注）

- 公开补丁分析（Miggo 等）指出：修复会把 `__objclass__` **加入**属性黑名单；易受攻击面在 Python task runner 的校验路径（`TaskAnalyzer.validate` 一带）。
- VulnGym 原标注把 `critical_operation` 放在 `constants.py` 的 `BLOCKED_ATTRIBUTES = {` **静态集合定义**。
- Issue #6 明确：**critical 不应是静态声明**；人工备注也质疑「落在静态列表」。

## 选拔者视角的初步裁决（待源码/补丁证实）

| 候选 | 角色 | 倾向 |
|------|------|------|
| `BLOCKED_ATTRIBUTES` 字面定义 | 策略数据；缺 `__objclass__` 是根因材料 | **拒绝作 critical**（符合 Issue 原文）；可进 trace 说明「策略缺项」 |
| `task_analyzer` 中对黑名单的成员判断 / `validate` | 实际施力/拦截点；补丁前后行为分界 | **强 critical 候选**（与 PR #54/#77 同向） |
| `getNodeParameter(... code ...)` | 外部脚本进入系统 | **entry_point 合理**（原标注可保留，需核对 code 对齐） |
| 真正执行用户代码的 runner 调用 | 危险发生点 | 可能是 critical 或 trace 末段；需防「标太晚」 |

## 下一步证据

1. clone n8n @ vuln commit，核对 BEFORE 的 code 对齐。  
2. diff 到 patched tag（如 `n8n@2.10.1`）看 `__objclass__` 加在哪、哪段逻辑改了。  
3. 写 CANDIDATES / DECISION，明确拒绝静态列表。

## 竞品已见分歧

- PR #54 / #77：critical → `task_analyzer.py` 黑名单判断 —— 与 Issue「离开静态表」一致，作为默认工作假说。  
- 我们额外要写清：缺的是「列表内容」还是「访问路径未覆盖」（PR #54 还提到 `getattr` / dunder 混淆）——用源码裁决，避免复述别人 desc。
