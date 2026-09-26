# AWS review — UL-11 Cognito domain teardown (round 6)

Scope: verify commit `f5ca78f` against STUDENT-R5-001 in `content/labs/ul-11.json`.

## STUDENT-R5-001 — verdict: **Gone**

Original issue: the UL-11 teardown called `delete-user-pool` directly, with only a comment
telling the student to remember to delete a domain first. If a domain (default prefix or
custom) was attached, `delete-user-pool` would fail and leave the pool (and its cost/exposure)
in place.

The fixed line (`orderedDeletesPowerShell[12]`) now:
1. Resolves the pool id via `list-user-pools`.
2. For each id, calls `describe-user-pool --query "UserPool.Domain"` and, if non-empty/non-`None`,
   calls `delete-user-pool-domain --domain $Domain --user-pool-id $Id`.
3. Repeats the same describe/delete pair for `UserPool.CustomDomain`.
4. Only then calls `delete-user-pool --user-pool-id $Id`.

### CLI reference check (docs.aws.amazon.com/cli/latest/reference/cognito-idp/…)

- `delete-user-pool-domain`: required params are `--domain` and `--user-pool-id`, both supplied
  correctly, in the correct order for this API. No incorrect flags.
- `describe-user-pool`: output has `Domain` and `CustomDomain` as top-level fields directly under
  `UserPool` — so `--query "UserPool.Domain"` / `"UserPool.CustomDomain"` are the correct JMESPath
  expressions used by the script. Confirmed.
- `delete-user-pool`: required param is `--user-pool-id`, supplied correctly. AWS's own known
  behavior (not contradicted by the fetched doc) is that a pool with an attached domain must have
  the domain removed first — the fix's ordering (domain(s) deleted, then pool) matches this.
- A custom domain is deleted with the **same** `delete-user-pool-domain` command (per AWS API,
  `CustomDomain` and prefix `Domain` share one delete operation) — the script does this correctly
  by passing whichever domain value it found as `--domain`.
- A missing domain: both `Domain` and `CustomDomain` are guarded by
  `if ($X -and $X -ne 'None')`, so an empty/`'None'` result from `describe-user-pool` skips the
  delete call safely — no false-positive deletes, no crash from an empty `--domain`.
- Order is correct: domain deletes happen strictly before `delete-user-pool` inside the same
  `if ($Id)` block.

### PowerShell 5.1 syntax and logic check

- Parsed the full line with `[System.Management.Automation.Language.Parser]::ParseInput` —
  **PARSE OK**, no errors. Valid PowerShell 5.1 (no PS7-only syntax used).
- Stubbed `aws` as a PowerShell function and ran the line under 4 scenarios:
  - prefix domain only → domain deleted, then pool deleted, no custom-domain delete attempted (guarded).
  - custom domain only → custom-domain deleted, then pool deleted.
  - no domain at all (`'None'`/`'None'`) → both domain deletes skipped, pool still deleted.
  - no pool found (`$PoolId = 'None'`) → no calls made at all.
  All four matched expected behavior.
- Guards: every `delete-user-pool-domain` and `delete-user-pool` call sits inside an `if (...)`
  (`if ($Domain ...)`, `if ($CustomDomain ...)`, and the enclosing `if ($Id)`/`if ($PoolId ...)`).
  No delete runs unguarded.
- No `-ErrorAction` appears on any `aws` line anywhere in the file (`grep -n "ErrorAction"` — no
  matches), consistent with the house style of letting failures surface rather than being
  silently suppressed.

### `stopChargesPanel` consistency

`stopChargesPanel` reads: "...any Cognito user pool (delete its domain first, default prefix or
custom), and the IAM role for ul-11." This matches the teardown script's actual order and its
handling of both domain types. Consistent.

## New issues found

None (AWS-R6L-### not needed — no new issue raised).

## Overall: approve
