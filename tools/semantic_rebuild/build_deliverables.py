# -*- coding: utf-8 -*-
"""Build issue #6 deliverables from AFTER.json node packs."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tools" / "semantic_rebuild" / "out"
ENTRIES = ROOT / "data" / "entries.jsonl"
IDS = [
    "entry-00099",
    "entry-00100",
    "entry-00103",
    "entry-00176",
    "entry-00511",
    "entry-00512",
]


def load_after(eid: str) -> dict:
    return json.loads((ROOT / "tools" / "semantic_rebuild" / eid / "AFTER.json").read_text(encoding="utf-8"))


def node_key(n: dict) -> tuple:
    return (n.get("file"), n.get("line"), n.get("code"))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    after_map = {eid: load_after(eid) for eid in IDS}
    originals = {}
    for line in ENTRIES.read_text(encoding="utf-8").splitlines():
        o = json.loads(line)
        if o["entry_id"] in after_map:
            originals[o["entry_id"]] = o

    fixed_rows = []
    diff_rows = []
    for eid in IDS:
        before = originals[eid]
        after = after_map[eid]
        fixed = dict(before)
        for field in ("entry_point", "critical_operation", "trace", "verify"):
            if field in after:
                fixed[field] = after[field]
        # never bump verify
        fixed["verify"] = 0
        fixed_rows.append(fixed)

        for field in ("entry_point", "critical_operation"):
            b, a = before[field], fixed[field]
            if node_key(b) != node_key(a) or b.get("desc") != a.get("desc"):
                diff_rows.append(
                    {
                        "entry_id": eid,
                        "field": field,
                        "before_file": b.get("file"),
                        "before_line": b.get("line"),
                        "before_code": (b.get("code") or "")[:160],
                        "after_file": a.get("file"),
                        "after_line": a.get("line"),
                        "after_code": (a.get("code") or "")[:160],
                        "reason": "semantic_rebuild",
                    }
                )
        # summarize trace change as one row
        diff_rows.append(
            {
                "entry_id": eid,
                "field": "trace",
                "before_file": f"len={len(before.get('trace') or [])}",
                "before_line": "",
                "before_code": "",
                "after_file": f"len={len(fixed.get('trace') or [])}",
                "after_line": "",
                "after_code": "",
                "reason": "rewritten_for_semantic_flow",
            }
        )

    fixed_path = OUT / "entries.fixed.jsonl"
    with fixed_path.open("w", encoding="utf-8", newline="\n") as f:
        for row in fixed_rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    csv_path = OUT / "semantic_diff.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "entry_id",
                "field",
                "before_file",
                "before_line",
                "before_code",
                "after_file",
                "after_line",
                "after_code",
                "reason",
            ],
        )
        w.writeheader()
        w.writerows(diff_rows)

    print("wrote", fixed_path)
    print("wrote", csv_path)
    print("entries", len(fixed_rows), "diff_rows", len(diff_rows))


if __name__ == "__main__":
    main()
