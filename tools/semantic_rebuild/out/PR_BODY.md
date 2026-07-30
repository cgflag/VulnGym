## Issue

Fixes #6

## What this does

Re-checks `entry_point` / `critical_operation` / `trace` for the six priority n8n entries named in #6, against each entry’s vuln commit (and fix patches where useful). Updates those six rows in `data/entries.jsonl`. Leaves `verify` at `0`.

## Mapping to #6

| Issue ask | Where |
|-----------|--------|
| Corrected `{file, line, code, desc}` | `data/entries.jsonl` + `tools/semantic_rebuild/out/entries.fixed.jsonl` |
| Per-entry: old problem, new locus, why / why not | `entry-*/DECISION.md`, `CANDIDATES.md` |
| Reviewable diff | `out/semantic_diff.csv` |
| Nodes match source at commit | `python tools/semantic_rebuild/run_all.py` (line/code check only) |
| entry = how input enters; critical ≠ wrapper/static/`}` | see table below |
| SCHEMA | field shapes unchanged; `verify` still 0 |

## Per entry

| entry | Was wrong | Now |
|-------|-----------|-----|
| 00099 | critical on `PrototypeSanitizer` def; entry only `@Post` | entry `executeManually(req.body, …)`; critical `evaluateExpression` (sanitizer gap kept in trace — see `CRITICAL_RULE.md`) |
| 00100 | critical on `sanitizer` body | same sink as 00099 |
| 00103 | entry on `}` | entry `setResponseHeaders`; critical still missing `trim` (`553b24458e`) |
| 00176 | critical on `BLOCKED_ATTRIBUTES = {` | critical `node.attr in BLOCKED_ATTRIBUTES` |
| 00511 | “pick Function” vs `.apply` confusion | critical unchecked native return `82-84`; fix commit `1acdafe6ac` blocks names earlier, does not change `.apply` |
| 00512 | weak entry/desc | entry `vmEvaluator.evaluate`; critical writable `__sanitize` (same line as fix) |

Rule used for critical: `tools/semantic_rebuild/CRITICAL_RULE.md` (prefer patch locus; only 00099/00100 fall back to exec sink because #6 rejects RCE critical on sanitizer hooks).

## How to check

```bash
python tools/semantic_rebuild/run_all.py
```

This checks formatting and that quoted `code` matches the checkout. It does **not** prove the semantic choice is right.

## Notes

- Full write-up: `tools/semantic_rebuild/out/NOTES.md`
- `verify`: kept `0` on purpose (`VERIFY_POLICY.md`); bump after review if you agree
