# Teacher review (1eaacbf) — D6 Part A lab cost basis

Saved by Lead Dev from the Teacher's reply. The replacement texts and the template are verbatim.

The Teacher recomputed every figure. All 24 h figures reconcile, except ul-07's (by design). LD-PA-001's four low same-hour figures are confirmed.

## Conditions
- **Met on all 16:** the 24 h figure in the panel, a floor/exclusions note, and "re-read pricing".
- **Readability, not met:** every basis line is 50–130 words of rates, footnotes and asterisks.
- **Unverified-rate wording:** "rate not verified …; re-check the pricing page before running" is actionable. The surrounding jargon ("worked-example rate whose region the page does not name") is not.

## Verdicts
- **Fix (template, trim):** gl-06, ul-06, gl-07, gl-18, ul-18, gl-19, gl-21, ul-21.
- **Fix (figure):** gl-08 ($0.09), gl-09 ($0.04), ul-08 ($0.11, the most cluttered line), ul-09 ($0.07).
- **Fix (keep note):** ul-19. Keep its t3.medium note and add the resulting 24 h figure (≈ $3.52 before storage).
- **Concerns:** gl-14, ul-14 (TEACHER-PA-002) and ul-07 (TEACHER-PA-003).

## Findings
- **TEACHER-PA-001 (medium): the "LCU/usage" exclusion is on all 16 labs, but only gl-08 and ul-08 have a load balancer.**
  - Default: "Not included: data transfer."
  - gl-08 and ul-08: "Not included: LCU (traffic) charges and data transfer." ul-08 adds "and WAF request charges ($0.60 per million)."
  - gl-14 and ul-14: add "backup storage beyond the free allowance" only if the docs support it.
- **TEACHER-PA-002 (medium): gl-14 and ul-14 label as "a floor" a figure that uses io1 storage ($0.125/GB-month) as a stand-in, which overstates it.** The gl-14 panel also says "costly" beside $0.52.
  - gl-14 basis: "Cost basis (us-east-1, priced 2026-09-29): 1 RDS db.t3.micro Single-AZ $0.018/h, 20 GB storage (no public IPv4). This run ≈ $0.05; forgotten 24 h ≈ $0.52. Storage is priced at the higher io1 rate because the gp2/gp3 rate was not read, so real cost is likely slightly lower. Not included: data transfer. Re-check pricing before you run."
  - gl-14 panel: "RDS bills every hour until deleted. Forgotten 24 h ≈ $0.52 (see the cost basis; check current pricing)."
  - ul-14: the same pattern, with $0.10 and $1.12, 2 instances and 60 GB.
- **TEACHER-PA-003 (medium): ul-07 says "conservative" and "floor" about a $0.72 that is not derived from anything.** The verified parts come to about $0.39, and the same-hour figure omits EFS without saying so.
  - Basis: "Cost basis (us-east-1, priced 2026-09-29): t3.micro $0.0104/h (smallest assumed), 1 public IPv4 $0.005/h, 8 GB gp3 root, plus EFS storage. The EFS rate was not read on 2026-09-29, so check the EFS pricing page before you run. This run ≈ $0.04 (EFS not included); forgotten 24 h ≈ $0.72, a cautious figure, not a calculated one (the parts we could price come to about $0.39). Not included: data transfer."
  - Panel: "Forgotten 24 h ≈ $0.72 (cautious, not calculated; see the cost basis)."
- **TEACHER-PA-004 (low): "floor" is jargon.** Panels should read "Forgotten 24 h: at least $X (see the cost basis)."
- **TEACHER-PA-005 (low):** the "rate rate" typo, the same as LD-PA-003.

## Template for all 16 basis lines
"Cost basis (us-east-1, priced 2026-09-29): {resource list with counts and hourly rates}. This run ≈ $X; forgotten 24 h ≈ $Y (at least; {one exclusion}). {ONE caveat sentence if any rate is unverified: 'The {service} rate is not verified for us-east-1; check its pricing page before you run.'} Re-check current pricing before you run."
- Move the asterisk footnotes, the "worked-example" wording and the AMI-default detail to the docs table.
- Target length: about 45–70 words.
- Example (gl-19): "Cost basis (us-east-1, priced 2026-09-29): EKS control plane $0.10/cluster-hour (no nodes). This run ≈ $0.20; forgotten 24 h ≈ $2.40 (at least; data transfer not included). Re-check current pricing before you run."

## Views on the Lead Dev pre-check
- **LD-PA-001:** agree. Apply all four; for ul-09, $0.07 is safer.
- **LD-PA-002:** agree. Also state the task cost ("0.25 vCPU + 0.5 GB ≈ $0.0124/h").
- **LD-PA-003 and LD-PA-004:** agree.
- **LD-PA-005:** agree that the unverified rates need a reviewer check. The Teacher could not read the pricing pages.

Part A: not yet · Overall: concerns
