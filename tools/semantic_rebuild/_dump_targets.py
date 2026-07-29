# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(r"D:\postgraduate\main-line\Job\Tencent\VulnGym\data\entries.jsonl")
want = {
    "entry-00099",
    "entry-00100",
    "entry-00103",
    "entry-00176",
    "entry-00511",
    "entry-00512",
}
out = Path(r"D:\postgraduate\main-line\Job\Tencent\VulnGym\tools\semantic_rebuild\_raw_targets.json")
out.parent.mkdir(parents=True, exist_ok=True)
rows = []
for line in p.open(encoding="utf-8"):
    e = json.loads(line)
    if e["entry_id"] in want:
        rows.append(e)
        print("===", e["entry_id"])
        print(" title:", e.get("vuln_title", "")[:100])
        print(" report:", e["report_id"], "verify:", e.get("verify"))
        print(" repo:", e.get("repo_url"), "commit:", e.get("commit"))
        for k in ("entry_point", "critical_operation"):
            n = e[k]
            print(f" {k}: {n.get('file')}:{n.get('line')}")
            print("   code:", repr(n.get("code"))[:200])
            print("   desc:", repr(n.get("desc"))[:220])
        print(" trace_len:", len(e.get("trace") or []))
        if e.get("trace"):
            for i, t in enumerate(e["trace"][:5]):
                print(f"   trace[{i}]: {t.get('file')}:{t.get('line')} {repr(t.get('code'))[:80]}")
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", out, "n=", len(rows))
