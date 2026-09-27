# Task 4.4 questions — implementation report

## Summary

Wrote all 23 questions for task 4.4 (14 MC + 9 MR, one MC per objective plus one MR each for K03, K06, S01-S07). Kept `id`, `type`, `module`, `objectiveIds`, `selectCount` unchanged from the placeholder files. Set `citationIds` to the relevant `cite-saa-4-4-*` files (post lesson-fix set), `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"`. Updated the lesson's `drillIds` to the full ordered 23-id list (was the stale 14-item `-mc`-only placeholder list).

## Paraphrase rule (new from task 4.4)

Every stem is a scenario (company + constraint + requirement) in operational language — bandwidth numbers, business constraints ("finance wants an automatic email", "partners must allowlist a fixed set of addresses"), not lesson terms like "cost allocation tags" or "gateway endpoint" pasted from the objective text. Keys name the AWS action/service directly without echoing the stem's distinctive phrasing back (e.g. K05-mc's stem never says "Direct Connect"; the key does). Distractors were checked the same way — none quote the stem's constraint language back as their justification.

## Distractor type table (from `distractor_type_audit.py 4-4`, cap = 3 of 23)

| Type | Count | % | Questions |
|---|---|---|---|
| Application Load Balancer | 3 | 13% | k03-mc, k03-mr, s04-mc |
| Network Load Balancer | 3 | 13% | k03-mc, k03-mr, k07-mc |
| Gateway Load Balancer | 3 | 13% | k03-mr, k04-mc, k07-mc |
| NAT Gateway | 3 | 13% | k04-mc, s01-mc, s01-mr |
| Global Accelerator | 3 | 13% | s03-mc, s03-mr, s04-mc |
| Savings Plan | 2 | 9% | k01-mc, s05-mc |
| Transit Gateway | 2 | 9% | k05-mc, k06-mr |
| Direct Connect | 2 | 9% | s02-mc, s02-mr |
| CloudFront | 2 | 9% | s05-mc, s05-mr |
| Reserved Instance | 1 | 4% | k01-mc |
| DynamoDB | 1 | 4% | s03-mr |

No type exceeds the 3-question (15%) cap. `distractor_type_audit.py 4-4` → PASS.

Two rounds of rewording were needed to get here without changing any correct answer: Direct Connect and NAT Gateway each briefly hit 4/23. Fixed by rewording distractors where the term was incidental rather than the point of the question:
- `k02-mc` choice d: dropped "Direct Connect and Transit Gateway" → "the affected network resources" (still fails for the same reason: tags don't create an alert).
- `k06-mc` choice d: dropped "the Direct Connect gateway" → "the existing hybrid gateway" (still fails: no VPC-to-VPC hub).
- `s03-mr` choice b: replaced "route the nightly replication through a NAT gateway placed in the destination Region" with "enable AWS Global Accelerator to speed up the nightly replication job" (a different, still-real, still-wrong-for-a-stated-reason option — Global Accelerator does not reduce inter-Region data-transfer charges for a batch job). Rationale text updated to match.

## Balance

- MC key letters: a:4, b:4, c:3, d:3 (of 14).
- MR key slots across a–e: a:4, b:3, c:4, d:4, e:3 (of 18 slots across 9 questions).
- MR key sets: all 9 combinations are distinct (`a,b`; `b,c`; `c,d`; `d,e`; `a,c`; `b,d`; `a,e`; `c,e`; `a,d`) — no combination repeats, well under the 40% cap.
- Longest-choice-is-key: 4/14 = 29% (cap 35%). Five questions (`k01-mc`, `k02-mc`, `k04-mc`, `s01-mc`, `s06-mc`) originally had the key as the longest choice; fixed by lengthening one real distractor in each rather than shortening the key, so the key still reads as a normal-length action.
- No two stems share their first six words (checked by `q1_batch_check.py`).

## Teach-before-test

Every key and every distractor's failure reason traces to a fact or discriminator in the rewritten `lesson-4-4.json`:
- NAT gateway vs NAT instance cost/ops tradeoff (K04, S01) → k04-mc, s01-mc, s01-mr.
- NAT gateway per-AZ redundancy and routing (S01) → s01-mc, s01-mr, s05-mr.
- Direct Connect vs VPN vs internet, and DX/VPN bandwidth tiers (K05, S02, S07) → k05-mc, s02-mc, s02-mr, s07-mc, s07-mr.
- VPC peering vs Transit Gateway cost/scale (K06) → k06-mc, k06-mr.
- Gateway vs interface VPC endpoints, and the explicit selection rule added in the lesson-fix round (S03) → s03-mc, s03-mr.
- CloudFront vs Global Accelerator, including the HTTP-only discriminator added in the lesson-fix round, and Origin Shield now named in prose (S04) → s04-mc, s04-mr.
- ALB vs NLB vs GWLB by layer, with NLB/GWLB now spelled out on first use (K03) → k03-mc, k03-mr.
- Route 53 vs load balancing vs DNS (K07) → k07-mc.
- Cost allocation tag activation and Budgets/Cost Explorer/CUR use cases (K01, K02) → k01-mc, k02-mc.
- API Gateway token-bucket throttling vs usage plans (S06) → s06-mc, s06-mr.
- Reviewing a workload with VPC Flow Logs / CloudWatch / Cost Explorer (S05) → s05-mc, s05-mr.

No question required a fact outside the lesson; no "Lesson additions requested" needed this round.

## Other RULES checks

- No strawmen (no "by hand", "one instance", "hardcode an IP", "wait until next time"); every distractor is a real, currently-supported AWS option or configuration choice that fails exactly one stated requirement in its stem.
- No giveaway words (`since`, `even though`, `because`, `by default`, `as the only`, `which does not`, `despite`, `requiring`, `must`, `without changing`) appear in any choice text; all reasoning lives in `rationale`.
- No duplicate facts tested twice (each question maps to a distinct objective/discriminator pair; even where the same service pair recurs, e.g. ALB/NLB/GWLB across K03 and K07, the tested fact differs — layer identification vs. DNS-vs-load-balancer scope).
- Rationale explains the key and every distractor by content, with no letter references.

## Verification

- `content_lint.py` → PASS
- `q1_batch_check.py 4-4` → PASS (all lines, including drillIds match, longest-is-key 29%, MC/MR key spread, MR key-set diversity, no duplicate stem openings)
- `distractor_type_audit.py 4-4` → PASS (cap 3/23, no type over cap)
