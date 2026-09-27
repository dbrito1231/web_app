# Task 4.4 drill — student run (blind)

## Committed answers (written before opening the answer key)

**Q1 (q-saa-4-4-k01-mc)** — a. The stem is a textbook re-tagging-vs-activation trap: tags applied, still not on reports after weeks, finance wants it fixed without re-tagging. Only activating the cost allocation tag key does that.

**Q2 (q-saa-4-4-k02-mc)** — b. "Automatic email," "nobody checking a dashboard," and a forecasted-spend threshold is exactly what Budgets is for; Cost Explorer requires someone to look.

**Q3 (q-saa-4-4-k03-mc)** — c. Third-party appliance fleet that AWS auto-scales, inline before any workload traffic, is the GWLB insertion pattern.

**Q4 (q-saa-4-4-k03-mr)** — a, b. Fixed small address set for partner allowlisting = NLB static IPs. URL-path routing to different backend teams on one domain = ALB path-based rules.

**Q5 (q-saa-4-4-k04-mc)** — d. Steady/low/predictable traffic, team willing to own patching, wants lowest total bill — that's the profile where a right-sized NAT instance's EC2 cost can beat a NAT gateway's fixed hourly charge.

**Q6 (q-saa-4-4-k05-mc)** — a. "Bandwidth guarantee" + "none of that traffic can cross the public internet" rules out both VPN options and plain internet; only dedicated Direct Connect satisfies both.

**Q7 (q-saa-4-4-k06-mc)** — b. Two VPCs now but a roadmap of many more VPCs/VPN sites and a wish to avoid re-architecting each addition is the standard "peering doesn't scale, move to a hub" cue.

**Q8 (q-saa-4-4-k06-mr)** — b, c. Three VPCs wanting direct low-cost connectivity = peering (no TGW per-attachment/per-GB overhead). Wanting inter-VPC traffic to stay in-AZ to dodge per-GB charges = keeping the chattiest peered resources co-located in one AZ.

**Q9 (q-saa-4-4-k07-mc)** — c. "Whichever endpoint responds fastest, same URL" is Route 53 latency-based routing; guessing slightly between this and "just fast DNS failover" but latency-based is the direct fit since the requirement is about speed, not failover.

**Q10 (q-saa-4-4-s01-mc)** — d. NAT gateway resilience is AZ-scoped; the only design where one AZ's failure doesn't take out the others' egress is one gateway per AZ with each subnet routed to its own AZ's gateway.

**Q11 (q-saa-4-4-s01-mr)** — c, d. Gateway endpoint for S3 strips that traffic (and its charge) off the NAT path entirely without touching AZ topology. Confirming (and if needed fixing) that each AZ's subnets route to their own AZ's gateway both preserves isolation and removes any accidental cross-AZ NAT data-processing charge.

**Q12 (q-saa-4-4-s02-mc)** — a. Encrypted backup path, needed in days not weeks, alongside an existing DX link — Site-to-Site VPN as DX backup is the named pattern in the lesson.

**Q13 (q-saa-4-4-s02-mr)** — d, e. Tomorrow's pilot with no existing hybrid connection = public internet + TLS (fastest option). Future dedicated non-internet requirement for the audit = start the DX order now since it's slow to provision.

**Q14 (q-saa-4-4-s03-mc)** — b. Constant S3 calls from private subnets dominating the NAT bill is the canonical gateway-endpoint-for-S3 scenario (no additional charge, removes the traffic from NAT entirely).

**Q15 (q-saa-4-4-s03-mr)** — a, c. DynamoDB calls from private subnets = gateway endpoint for DynamoDB. A nightly cross-Region copy nobody reads = confirm it's still needed before continuing to pay for it (the "don't default to multi-Region" principle).

**Q16 (q-saa-4-4-s04-mc)** — c. Same static assets served worldwide many times a day, wanting to stop paying full Regional transfer per repeat view, is squarely CloudFront-in-front-of-S3 (cached edge hits, no origin retrieval fee).

**Q17 (q-saa-4-4-s04-mr)** — b, d. Multiple CDNs re-pulling from one origin on cache miss is the Origin Shield use case (consolidates requests). Separately confirming what's actually cacheable and extending TTL directly cuts how often anything needs to be refetched.

**Q18 (q-saa-4-4-s05-mc)** — d. "Growing cross-boundary spend, nobody knows the driver" is a visibility problem first — flow logs + CloudWatch/Cost Explorer by usage type, not a blind fix.

**Q19 (q-saa-4-4-s05-mr)** — a, e. Flow logs show cross-AZ EC2-to-NAT calls — fix is same-AZ NAT gateway + repoint routing. The unexplained nightly cross-Region copy — confirm with the business and stop it if not needed, matching Q18's "identify then fix" pattern and Q15's "don't default to multi-Region" principle.

**Q20 (q-saa-4-4-s06-mc)** — a. Different limits per tier (free vs paid), tied to individual partners, without touching the backend, is what usage plans on API keys are built for; account/stage throttles are uniform across all callers so they can't do this.

**Q21 (q-saa-4-4-s06-mr)** — c, e. Absorbing an unpredictable nightly spike from one job = stage-level burst limit sized for it. Wanting a self-imposed ceiling below the AWS-enforced account-level Region limit = a usage plan quota on that job's key set below the account limit.

**Q22 (q-saa-4-4-s07-mc)** — b. 3 Gbps sustained and still growing exceeds a standard VPN tunnel's 1.25 Gbps ceiling; Large Bandwidth Tunnel isn't available on a standalone (non-TGW/Cloud WAN) VPN attachment per the lesson, so the fix is moving to a dedicated 10 Gbps Direct Connect connection.

**Q23 (q-saa-4-4-s07-mr)** — a, d. 800 Mbps site fits comfortably inside a hosted DX connection's 50 Mbps–25 Gbps range without a full dedicated port. 40 Gbps site needs the next dedicated tier up from the available 1/10/100/400 Gbps increments, which is 100 Gbps.

## Marking (against student-answers-4-4.md)

All 23 committed answers matched the answer key exactly.

**Score: 23/23**

## Fairness judgement

No wrong answers to judge. One guess was flagged in the committed reasoning (Q9, torn between latency-based routing and a failover framing) — it turned out correct and, on reflection, is not genuinely ambiguous: the stem asks about routing to whichever endpoint "currently responds fastest," which is latency-based routing's defining behavior, not failover's. No fairness complaint there.

## Guessable-stem count (word-matching without understanding the concept)

Applying the hard test — could a reader with no AWS knowledge land on the key purely by spotting shared distinctive wording between stem and one option — these look genuinely guessable that way:

- **Q1** — stem says "the tag key on cost reports without re-tagging"; option (a) is the only one containing "tag key" verbatim, and the other options either don't mention tags or explicitly involve re-tagging (which the stem rules out).
- **Q2** — stem says "automatic email"; option (b) is the only option containing "email notification."
- **Q7** — stem says "avoid re-architecting the hub each time one joins"; option (b) is the only option containing the word "hub."
- **Q8 (part a)** — stem's phrase "direct, low-cost connectivity" for the three-VPC part is close to verbatim from the lesson's own peering description, and option (b) is the peering option.
- **Q12** — stem says "backup path"; option (a) contains "backup path" verbatim.
- **Q13** — stem says "reach AWS for a small pilot by tomorrow" and "dedicated, non-internet path"; option (d) contains "reach AWS ... tomorrow's pilot traffic" almost verbatim, and option (e) contains "dedicated connection ... before the audit" matching "audit" verbatim.
- **Q15 (part a)** — stem says "calls DynamoDB"; option (a) is the only option that mentions DynamoDB at all, so it's identifiable by keyword alone regardless of understanding gateway endpoints. Part (c) also lifts "nightly," "cross-Region copy" verbatim from the stem.
- **Q19** — stem's description of EC2-in-one-AZ-calling-NAT-in-another is almost restated verbatim in option (a); option (e) lifts "nightly," "cross-Region copy" verbatim from the stem (same pattern as Q15).
- **Q21 (part c)** — stem says "unpredictable spike ... from one internal reporting job every night"; option (c) says "sized to absorb the nightly reporting job's traffic pattern" — near-verbatim restatement. Part (e) also reuses "account-level limit" and "Region" verbatim.

Count: **9 of 23** (Q1, Q2, Q7, Q8, Q12, Q13, Q15, Q19, Q21) show at least one option restating stem language closely enough to be picked by keyword-matching alone, without needing to know the underlying AWS service behavior. That is not obviously better than the 9-of-22 baseline the new stem-paraphrase rule was meant to fix — several stems still echo lesson/option vocabulary quite closely (DynamoDB, hub, backup path, tag key, nightly cross-Region copy, tomorrow's pilot).

## Eliminable-on-sight distractors

Ruled out without needing this lesson's material, either because the service is obviously the wrong tool for the stated job, or because the option is simply disabling a safety/cost control:

- Q3(d) — Route 53 weighted routing can't insert an inline appliance fleet.
- Q4(c) — GWLB doesn't give partner-facing static allowlist IPs; that's not its job.
- Q5(c) — GWLB appliance sizing has nothing to do with providing internet egress.
- Q6(c) — sending files over the public internet directly contradicts the stem's "none of that traffic can cross the public internet."
- Q8(d) — a shared internet-egress device doesn't carry inter-VPC traffic; wrong purpose entirely.
- Q9(a)/(d) — GWLB and NLB don't perform DNS resolution/routing between independent Regional endpoints.
- Q12(c) — routing unencrypted traffic during a maintenance window is directly turning off the required safety control (encryption).
- Q13(c) — Route 53 routing policies don't establish network reachability by themselves.
- Q16(a) — Global Accelerator doesn't cache HTTP content; wrong tool for a caching problem.
- Q17(e) — WAF rate-based rules target malicious/excessive traffic, not legitimate multi-CDN cache-miss fetches.
- Q20(d) — publishing documentation has no technical enforcement at all, so it can't be the answer to a "must be limited" requirement.
- Q21(a) — resizing the reporting job's EC2 instance has no effect on API Gateway throttling.
- Q21(d) — "leave everything at default" is a non-action masquerading as an option.
- Q23(e) — a shared 10 Gbps port for a site needing 40 Gbps fails on arithmetic alone, no AWS knowledge required.
