# AWS review — Task 3.4 questions, Round 2

## Gone lines

- **AWS-L34-001: Gone.** `content/lessons/lesson-3-4.json` K01 now reads "Lesson 2.1 K07 already contrasts CloudFront with Global Accelerator..." — correct attribution confirmed.
- **TEACHER-L34-002: Gone (second-role check).** The checker fix in `scripts/q1_batch_check.py` (commit `020b233`) now strips backtick-delimited code spans (`` `[^`]*` ``) before scanning for single-asterisk spans, so `` `/images/*` `` and `` `/api/*` `` are correctly excluded — code-span asterisks render literally, not as italics markup, so this is the right fix rather than a lesson wording change. Re-ran `q1_batch_check.py 3-4`: `PASS: lesson single-asterisk spans: 0`. Agree this is resolved.

## Batch check

`backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 3-4` → `RESULT: PASS`, all 9 checks PASS, no FAILs.

## Per-question review

| Question | Key correct? | Distractors real/non-strawman? | Rationale accurate? | Stem unambiguous? | Citations support? |
|---|---|---|---|---|---|
| k01-mc | Yes (a, Origin Shield) | Yes | Yes | Yes | Yes |
| k02-mc | Yes (b, /16, RFC1918) — number verified | Yes | Yes | Yes | Yes |
| k03-mc | Yes (c, NLB) | Yes | Yes | Yes | Yes |
| k03-mr | Yes (a, b — 2 of 2) | Yes | Yes | Yes | Yes |
| k04-mc | Yes (d, VPN-over-DX-via-TGW) | Yes | Yes | Yes | Yes |
| s01-mc | Yes (a, private subnet/no IGW route) | Yes | Yes | Yes | **No — see AWS-Q34-002** |
| s01-mr | Yes (c, d — 2 of 2) | Yes | Yes | Yes | Weak (see AWS-Q34-003) |
| s02-mc | Yes (b, secondary CIDR) | Yes | Yes | Yes | Yes |
| s02-mr | Yes (b, e — 2 of 2) | Yes | Yes | Yes | Yes |
| s03-mc | Yes (c, Wavelength) | Yes | Yes | Yes | Yes |
| s03-mr | Yes (c, e — 2 of 2) | Yes, but see AWS-Q34-001 | Yes | Yes | **No — see AWS-Q34-002** |
| s04-mc | Yes (d, NLB) | Yes | Yes | Yes | Yes |
| s04-mr | Yes (b, d — 2 of 2) | Yes | Yes | Yes | Yes |

## Issues

- **AWS-Q34-001** (moderate, duplicate fact) — `q-saa-3-4-s01-mc` and `q-saa-3-4-s03-mr` (choices a/c) both test the identical fact: "a route table with no route to an internet gateway, not a security group, is what keeps a subnet unreachable from the internet." The stems, correct choice, and the wrong "public subnet + security-group deny rule" distractor are near-verbatim restatements of each other. Fix: rewrite `s03-mr`'s unreachability half to test a fact not already covered by `s01-mc` — e.g. drop the private/public-subnet pairing entirely and pair the Local-Zone-vs-Wavelength choice with a second, S03-specific requirement such as placing a NAT gateway or load balancer in the correct public/private tier for a stated multi-tier layout, so the question doesn't re-test S01's route-table fact.
- **AWS-Q34-002** (moderate, citation mismatch) — `q-saa-3-4-s01-mc` and `q-saa-3-4-s03-mr` cite `cite-saa-3-4-vpc-cidr-blocks` (https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html), which documents CIDR block sizing, not route tables. The tested fact — a route table's internet-gateway route, not a security group, determines a subnet's public/private reachability — is documented at https://docs.aws.amazon.com/vpc/latest/userguide/route-table-options.html ("Routing to an internet gateway"), verified via `search_documentation` this round. This citation gap also exists in the lesson body itself (the route-table sentence in K02 has no dedicated citation in the lesson's `citationIds` list). Fix: add `cite-saa-3-4-route-table-igw` (that URL, note: "confirms a route to an internet gateway in a subnet's route table is what makes it public"), add it to the lesson's `citationIds`, and swap it in for `cite-saa-3-4-vpc-cidr-blocks` on both `s01-mc` and `s03-mr`.
- **AWS-Q34-003** (minor, weak citation) — `q-saa-3-4-s01-mr` cites `cite-saa-3-4-vpn-tunnel-bandwidth` to support the "Site-to-Site VPN as an automatic backup path for Direct Connect" fact, but that citation's verified note is only about tunnel bandwidth numbers (1.25 Gbps / 5 Gbps), not the backup/failover pattern. This claim also has no dedicated row in the writer's claim table. Fix: verify and cite a page such as https://docs.aws.amazon.com/whitepapers/latest/hybrid-connectivity/vpn-as-a-backup-for-dx.html (or the equivalent current AWS guidance on VPN as a Direct Connect backup) and add it as a new citation for this fact.

## Number verification

Every number that appears in a key or is decisive to a key was checked this round:
- `q-saa-3-4-k02-mc`: `/16` = 65,536 addresses — verified against `vpc-cidr-blocks.html` (already confirmed Round 1).
- No other question key turns on a specific numeric value (bandwidth, port speed, partition counts, etc. appear only in distractor rationale text as qualitative "capped/dedicated" comparisons, not as the discriminating number in a choice).

## Retired/closed services

None used in any of the 13 questions.

Task 3.4: not yet (blocked on AWS-Q34-001 and AWS-Q34-002; AWS-Q34-003 is minor and can close alongside)

Overall: concerns
