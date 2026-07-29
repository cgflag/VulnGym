# -*- coding: utf-8 -*-
"""Verify AFTER.json nodes; fix PowerShell UTF-16 artifacts if any."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
N8N = ROOT / ".cache" / "repos" / "n8n"
VERIFY = ROOT / "tools" / "semantic_rebuild" / "verify_nodes.py"

COMMITS = {
    "entry-00099": "8ab4492e8c0b743455e51fc111441d8d5010a6ad",
    "entry-00100": "8ab4492e8c0b743455e51fc111441d8d5010a6ad",
    "entry-00176": "3af9095245be3aaad6bc16622f379f79c6c6068f",
}

FILES_BY_ENTRY = {
    "entry-00099": [
        "packages/workflow/src/expression-sandboxing.ts",
        "packages/workflow/src/expression-evaluator-proxy.ts",
        "packages/workflow/src/expression.ts",
        "packages/cli/src/workflows/workflows.controller.ts",
    ],
    "entry-00100": [
        "packages/workflow/src/expression-sandboxing.ts",
        "packages/workflow/src/expression-evaluator-proxy.ts",
        "packages/workflow/src/expression.ts",
    ],
    "entry-00176": [
        "packages/nodes-base/nodes/Code/Code.node.ts",
        "packages/@n8n/task-runner-python/src/task_analyzer.py",
        "packages/@n8n/task-runner-python/src/constants.py",
    ],
}


def materialize(commit: str, files: list[str]) -> None:
    subprocess.check_call(["git", "checkout", "--detach", commit], cwd=N8N)
    for f in files:
        data = subprocess.check_output(["git", "show", f"HEAD:{f}"], cwd=N8N)
        path = N8N / f
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main() -> int:
    entries = sys.argv[1:] or ["entry-00099", "entry-00100", "entry-00176"]
    rc = 0
    for eid in entries:
        commit = COMMITS[eid]
        print(f"=== {eid} @ {commit[:12]} ===")
        materialize(commit, FILES_BY_ENTRY[eid])
        after = ROOT / "tools" / "semantic_rebuild" / eid / "AFTER.json"
        p = subprocess.run(
            [sys.executable, str(VERIFY), "--repo", str(N8N), "--nodes", str(after)],
            cwd=ROOT,
        )
        if p.returncode != 0:
            rc = p.returncode
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
