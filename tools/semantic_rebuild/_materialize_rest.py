# -*- coding: utf-8 -*-
import json
import subprocess
from pathlib import Path

ROOT = Path(r"D:\postgraduate\main-line\Job\Tencent\VulnGym")
N8N = ROOT / ".cache" / "repos" / "n8n"

FILES = {
    "entry-00103": [
        "packages/cli/src/webhooks/webhook-helpers.ts",
        "packages/core/src/html-sandbox.ts",
        "packages/cli/src/webhooks/webhook-request-handler.ts",
    ],
    "entry-00511": [
        "packages/workflow/src/expression.ts",
        "packages/@n8n/expression-runtime/src/extensions/extend.ts",
        "packages/@n8n/expression-runtime/src/runtime/reset.ts",
        "packages/workflow/src/expression-sandboxing.ts",
    ],
    "entry-00512": [
        "packages/workflow/src/expression.ts",
        "packages/@n8n/expression-runtime/src/runtime/reset.ts",
        "packages/workflow/src/expression-sandboxing.ts",
    ],
}


def main() -> None:
    entries = {}
    for line in (ROOT / "data/entries.jsonl").read_text(encoding="utf-8").splitlines():
        o = json.loads(line)
        if o["entry_id"] in FILES:
            entries[o["entry_id"]] = o["commit"]

    subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=N8N, check=False)
    for sha in sorted(set(entries.values())):
        print("fetch", sha[:12])
        subprocess.run(["git", "fetch", "--depth", "1", "origin", sha], cwd=N8N, check=False)

    done_sha = None
    for eid, files in FILES.items():
        sha = entries[eid]
        if sha != done_sha:
            print("checkout", sha[:12])
            subprocess.check_call(["git", "reset", "--hard", "HEAD"], cwd=N8N)
            subprocess.check_call(["git", "checkout", "--detach", sha], cwd=N8N)
            done_sha = sha
        for f in files:
            try:
                data = subprocess.check_output(["git", "show", f"HEAD:{f}"], cwd=N8N)
            except subprocess.CalledProcessError:
                print("MISSING", f)
                continue
            path = N8N / f
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            print("ok", eid, f, len(data))


if __name__ == "__main__":
    main()
