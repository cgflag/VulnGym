# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

root = Path(r"D:\postgraduate\main-line\Job\Tencent\VulnGym\.cache\repos\n8n")
files = [
    "packages/workflow/src/expression-sandboxing.ts",
    "packages/workflow/src/expression-evaluator-proxy.ts",
    "packages/workflow/src/expression.ts",
    "packages/cli/src/workflows/workflows.controller.ts",
]
for f in files:
    data = subprocess.check_output(["git", "show", f"HEAD:{f}"], cwd=root)
    path = root / f
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print("rewrote", f, len(data), "head", data[:3])
