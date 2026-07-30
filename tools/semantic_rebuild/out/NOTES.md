# Fix notes for #6 (six priority n8n entries)

Rule: `CRITICAL_RULE.md`. Verify flag: `VERIFY_POLICY.md` (`verify` stays 0).

Updated in `data/entries.jsonl`. Diff for review: `out/semantic_diff.csv`.

`run_all.py` only checks that `{file,line,code}` matches the vuln commit. It does not validate semantics.

## Entries

### entry-00099

- Problem: critical on `PrototypeSanitizer` definition; entry was only `@Post`.
- Change: entry → `executeManually(req.body, …)`; critical → `evaluateExpression`.
- Rejected: sanitizer class/hooks as RCE critical (#6); Tournament ctor.
- Patch: `n8n@2.5.1` adds `visitWithStatement` (missing in vuln → described in trace).

### entry-00100

- Problem: critical on `sanitizer` function body.
- Change: same critical as 00099; entry kept at `resolveSimpleParameterValue`.
- Trace includes the MemberExpression-only gap.

### entry-00103

- Problem: entry on a closing `}`.
- Change: entry → `setResponseHeaders`; critical stays at `toLowerCase` without `trim`.
- Patch: `553b24458e` → `trim().toLowerCase()`.
- Trace uses the `sendStaticResponse` call site so it does not duplicate the entry body.

### entry-00176

- Problem: critical on static `BLOCKED_ATTRIBUTES = {`.
- Change: critical → membership test in `visit_Attribute`.
- Rejected: static set as critical; treating builtin `getattr` as this CVE’s critical (fix adds `__objclass__`).

### entry-00511

- Problem: original critical stopped at selecting `input[functionName]`; an intermediate version moved to `.apply`.
- Change: critical back at unchecked native return (`82-84`). `.apply` stays in trace.
- Patch: `1acdafe6ac` adds `UNSAFE_PROPERTY_NAMES` at the start of `findExtendedFunction` (no change to `.apply`).

### entry-00512

- Problem: critical line was already right; entry/desc/trace were weak.
- Change: entry → `vmEvaluator.evaluate`; critical kept on writable `__sanitize`.
- Patch: same fix commit locks `__sanitize` with `defineProperty`.

## Candidates / patches

Each `entry-*/` has `CANDIDATES.md` and `PATCH_NOTES.md` for the “why this locus / why not the others” part of #6.
