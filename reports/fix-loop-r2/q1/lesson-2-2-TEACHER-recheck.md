# Teacher re-check: lesson 2.2 (commit `56d6a3e`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

## 1. TEACHER-L22-001 (Route 53 geoproximity / IP-based routing)
**Gone.** K01 now lists all 8 current Route 53 policies (simple, weighted, latency-based, geolocation, geoproximity, IP-based, multivalue answer, failover). Independently re-fetched `routing-policy.html` live: geoproximity = "route traffic based on the location of your resources and, optionally, shift traffic from resources in one location to resources in another location" — matches the lesson's wording exactly. IP-based = "route traffic based on the location of your users, and have the IP addresses that the traffic originates from" — matches. Both are placed correctly in K01's routing-policy list, read clearly, and don't clutter the section.

## 2. AWS-L22-001 to 003 (second-role check)
- **Citation notes:** Spot-checked 5 of the 26 (`ddb-global-tables`, `backup-vault-lock`, `route53-routing`, `s3-durability`, `rds-multiaz-cluster`). All name the specific claim backed, tie to the fix ID/section, and are no longer generic boilerplate. **Gone.**
- **DynamoDB MREC/MRSC sentence (S02):** "defaults to multi-Region eventual consistency (MREC), with an MRSC same-account option for multi-Region strong consistency, and conflicting writes resolved last-writer-wins" — independently re-verified live against `GlobalTables.html`: matches word-for-word on all three facts (MREC default, MRSC same-account-only, last-writer-wins). Clear for a student and correctly parenthetical inside the existing S02 sentence rather than a separate tangent. **Gone.**
- **Backup Vault Lock sentence (S05):** independently re-fetched `vault-lock.html` live. The lesson's claim (governance mode removable by sufficient IAM permissions; compliance mode immutable — unchangeable/undeletable by any user including root — after a mandatory cooling-off period of at least 72 hours) matches the doc exactly, including the "3 days (72 hours)" minimum grace time and the "any user... including root" scope. Clear and correct. **Gone.**

## 3. Placement and length
All three additions sit inside the section that already owned the topic (K01, S02, S05) rather than as bolted-on appendices, and each reads as one integrated clause/sentence, not a new paragraph — no clutter introduced.

Word count: my own count (stripping markdown markers) is 3,067 words; the impl notes report 3,173 (counting method differs, e.g. header markers). Either way this is within the acceptable band already used for lesson 2.1 (3,101 words / 23 objectives) — for 20 objectives here that's roughly 150–160 words/objective, in line with lesson 2.1's precedent. Acceptable; nothing needs cutting.

## 4. Format
- Markdown subset only: confirmed by inspection, no tables/links/numbered lists introduced.
- Single-asterisk spans: 0 (programmatically verified).
- `citationIds`: 26 entries, all resolve to existing files in `content/citations/` (verified programmatically, including the two new files `cite-saa-2-2-backup-vault-lock` and `cite-saa-2-2-s3-durability`).
- `drillIds`: all 32 present, all resolve to existing `q-saa-2-2-*` files, listed in exact objective order (K01→K12, S01→S08).
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, labs 21+21, lessons 23).

## Verdicts
- TEACHER-L22-001: **Gone**
- AWS-L22-001 (citation notes): **Gone**
- AWS-L22-002 (DynamoDB MREC/MRSC): **Gone**
- AWS-L22-003 (Backup Vault Lock): **Gone**

No new issues found (no TEACHER-L22-R-### items).

**Lesson 2.2: approve for question writing**

**Overall: approve**
