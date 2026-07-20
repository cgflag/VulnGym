# -*- coding: utf-8 -*-
"""Dry-run mechanical desc line-anchor sync (Diff Pack optional item 2). Does not write entries."""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "scripts"))
from _diffpack_lib import OUT, ROOT, load_fix_csv, load_fix_mod  # noqa: E402

# Explicit anchors only — no LLM.
CN_LINE = re.compile(r"第\s*(\d+)\s*行")
CN_RANGE = re.compile(r"第\s*(\d+)\s*[–—\-−‐]\s*(\d+)\s*行")
EN_LINE = re.compile(r"\bline\s+(\d+)\b", re.I)
EN_RANGE = re.compile(r"\blines?\s+(\d+)\s*-\s*(\d+)\b", re.I)


def old_line_start(v) -> int | None:
    s = str(v)
    if s.isdigit():
        return int(s)
    if "-" in s:
        return int(s.split("-", 1)[0])
    return None


def new_line_parts(v) -> tuple[int, int] | None:
    s = str(v)
    if s.isdigit():
        n = int(s)
        return n, n
    if "-" in s:
        a, b = s.split("-", 1)
        return int(a), int(b)
    return None


def try_sync(desc: str, old_line, new_line) -> tuple[str | None, str]:
    """Return (new_desc or None, status)."""
    if not desc:
        return None, "no_desc"
    old_s = old_line_start(old_line)
    new_p = new_line_parts(new_line)
    if old_s is None or new_p is None:
        return None, "unparseable_line"
    new_a, new_b = new_p
    # Only rewrite if desc mentions the exact old start line in a known anchor form.
    mentions = False
    for rx in (CN_LINE, EN_LINE):
        for m in rx.finditer(desc):
            if int(m.group(1)) == old_s:
                mentions = True
    for rx in (CN_RANGE, EN_RANGE):
        for m in rx.finditer(desc):
            if int(m.group(1)) == old_s:
                mentions = True
    if not mentions:
        return None, "no_anchor"

    def repl_cn_line(m):
        if int(m.group(1)) != old_s:
            return m.group(0)
        if new_a == new_b:
            return f"第 {new_a} 行"
        return f"第 {new_a}-{new_b} 行"

    def repl_en_line(m):
        if int(m.group(1)) != old_s:
            return m.group(0)
        if new_a == new_b:
            return f"line {new_a}"
        return f"lines {new_a}-{new_b}"

    out = CN_RANGE.sub(
        lambda m: (
            f"第 {new_a}-{new_b} 行"
            if int(m.group(1)) == old_s
            else m.group(0)
        ),
        desc,
    )
    out = CN_LINE.sub(repl_cn_line, out)
    out = EN_RANGE.sub(
        lambda m: (
            f"lines {new_a}-{new_b}"
            if int(m.group(1)) == old_s
            else m.group(0)
        ),
        out,
    )
    out = EN_LINE.sub(repl_en_line, out)
    if out == desc:
        return None, "anchor_but_unchanged"
    return out, "would_update"


def main() -> int:
    mod = load_fix_mod()
    fixes = load_fix_csv(OUT / "fix_diff.csv")
    originals = {}
    with (ROOT / "data" / "entries.jsonl").open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                originals[e["entry_id"]] = e

    rows = []
    counts: dict[str, int] = {}
    for (eid, fp), fr in fixes.items():
        e = originals[eid]
        node = None
        for path, n in mod.iter_nodes(e):
            if path == fp:
                node = n
                break
        if not node:
            continue
        desc = node.get("desc") or ""
        new_desc, status = try_sync(desc, fr.get("old_line"), fr.get("new_line"))
        counts[status] = counts.get(status, 0) + 1
        rows.append(
            {
                "entry_id": eid,
                "field_path": fp,
                "status": status,
                "old_line": fr.get("old_line"),
                "new_line": fr.get("new_line"),
                "old_desc_preview": (desc[:80] + "…") if len(desc) > 80 else desc,
                "new_desc_preview": (
                    ((new_desc[:80] + "…") if new_desc and len(new_desc) > 80 else new_desc)
                    or ""
                ),
            }
        )

    out = OUT / "desc_sync_dryrun.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "entry_id",
                "field_path",
                "status",
                "old_line",
                "new_line",
                "old_desc_preview",
                "new_desc_preview",
            ],
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary = {"counts": counts, "would_update": counts.get("would_update", 0)}
    (OUT / "desc_sync_dryrun_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
