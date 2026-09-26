# Teacher review — Task 3.4, Round 2

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**(a) TEACHER-L34-002:** Gone. The checker fix (stripping backtick code spans before scanning for single asterisks) is the correct approach — `` `/images/*` `` and `` `/api/*` `` are literal glob wildcards inside code spans, not italics markup, so no wording change to the lesson was needed. `q1_batch_check.py 3-4` confirms `PASS: lesson single-asterisk spans: 0`.

**(b) Second-role check:**
- **AWS-L34-001:** Gone, confirmed — K01 now reads "Lesson 2.1 K07 already contrasts CloudFront with Global Accelerator," matching lesson-2-1.json's actual K07 content.
- **AWS-Q34-001 (duplicate fact):** Gone. `s03-mr` now tests NAT-gateway placement (public subnet + IGW route) paired with Local Zone vs. Wavelength vs. Direct Connect, no longer overlapping `s01-mc`'s private-subnet/security-group fact.
- **AWS-Q34-002 (citation mismatch):** Gone. `s01-mc` and `s03-mr` both now cite `cite-saa-3-4-route-tables` (`route-table-options.html`), which documents the IGW-route-makes-it-public fact directly, and the lesson's `citationIds` list now includes it.
- **AWS-Q34-003 (weak citation):** Gone. `s01-mr` now cites `cite-saa-3-4-vpn-dx-backup` (an AWS reference-architecture page titled "AWS Direct Connect as Primary and AWS Site-to-Site VPN as Backup"), which directly supports the backup-path claim.
- **Is NAT-gateway placement (new `s03-mr`) taught?** Yes — lesson 3.4 S03 states directly: "a database tier belongs in a private subnet with no route to an internet gateway, while a NAT gateway or a public-facing load balancer belongs in a public subnet." K02 additionally teaches that a route-table entry to an internet gateway is what makes a subnet public. Both the key (public subnet + IGW route) and the wrong-placement distractor (private subnet, no IGW route) are covered.

**(c) Per-question review:**

| Question | Objective fit | Teach-before-test | Difficulty/strawman | Rationale/fairness |
|---|---|---|---|---|
| k01-mc | Yes | Yes (Origin Shield, cache behaviors, Global Accelerator all taught) | Fair, no strawman | Clear |
| k02-mc | Yes | Yes (/16–/28, RFC1918) | Fair | Clear |
| k03-mc | Yes | Yes (NLB/ALB/GWLB from 2.1) | Fair | Clear |
| k03-mr | Yes | Yes | Fair | Clear |
| k04-mc | Yes | Yes (VPN-over-DX-via-TGW taught in K04) | Fair | Clear |
| s01-mc | Yes | Yes | Fair | Clear |
| s01-mr | Yes | Yes (VPN backup + CloudFront/GA taught) | Fair | Clear |
| s02-mc | Yes | Yes | Fair | Clear |
| s02-mr | Yes | Yes | Fair | Clear |
| s03-mc | Yes | Yes (Local Zone vs Wavelength) | Fair | Clear |
| s03-mr | Yes | Yes (see above) | Fair, no longer duplicate | Clear |
| s04-mc | Yes | Yes | Fair | Clear |
| s04-mr | Yes | Partial — see TEACHER-Q34-001 | Fair | Citation gap |

**TEACHER-Q34-001** (minor, citation mismatch) — `q-saa-3-4-s04-mr`: the rationale for key choice **d** ("move the affected target to an instance family that supports enhanced networking") rests entirely on the enhanced-networking fact from lesson 3.4 S04 / lesson 3.2 (citation `cite-saa-3-2-enhanced-networking`), but that citation is missing from this question's `citationIds` — only `cite-saa-2-1-alb-cross-zone` is listed, which supports choice **b** (cross-zone) but is an **ALB**-specific doc page (`elasticloadbalancing/latest/application/...`) being used to back an **NLB** target-group claim in this stem. Fix: add `cite-saa-3-2-enhanced-networking` to `citationIds` for choice d's claim, and either swap in an NLB-specific cross-zone-load-balancing doc citation for choice b or verify/annotate that the same target-group attribute doc applies to NLB target groups before reusing it here.

No strawmen, no giveaway wording (`since`, `must`, `despite`, etc. — grepped across all 13 questions' choices, none found), no duplicate 6-word stem openings, no retired/closed services used.

**(d) Batch check:**
```
task 3-4: 13 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 8 for 8 objectives
PASS: duplicate 6-word openings: []
PASS: longest-is-key 0/8 = 0%
PASS: MC key positions {'a': 2, 'b': 2, 'c': 2, 'd': 2}
PASS: MR key slots {'a': 2, 'b': 3, 'c': 1, 'd': 2, 'e': 2}
RESULT: PASS
```

Task 3.4: not yet (blocked only on TEACHER-Q34-001, a minor citation fix)

Overall: concerns
