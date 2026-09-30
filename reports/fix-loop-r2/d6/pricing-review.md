# D6 Part A: pricing review

## Technical review (1eaacbf)

Reviewer: technical reviewer (issue ids AWS-PA-###), 2026-09-29. Public pricing pages only. No API, no bulk Price List, no calculator, no credentials. Lab content read at commit 1eaacbf; nothing edited.

### Method notes

- Every one of the 16 labs was recomputed by script (billed hours = ceil(estimatedMinutes/60) only for resources whose basis says "billed in full hours": NAT, ALB, RDS, ElastiCache; per-second resources use the fractional hour; month = 720 h; round up to the cent). All 16 pairs of figures reproduce exactly. With a 730 h month the only change is ul-08 24 h (1.26 becomes 1.25); 720 h is the higher value and is the month length the EBS and ELB pricing pages use in their own examples ("30-day month", "24 hours x 30 days"), so 720 h stays.
- The field values, the "same-hour ≈ / forgotten 24 h ≈" numbers in the basis line and the number in stopChargesPanel agree in all 16 labs (checked by script). The generic "Review same-hour and 24-hour estimates" item is gone from all 16; exactly one "Cost basis" line per lab.
- Browser note: the `[data-pricing-markup]` tables on the ELB, VPC, WAF, CloudWatch, EFS and RDS pages did not render (the Browser pane reports `document.visibilityState = "hidden"`, and only the c0.b0 widgets run when hidden). The EBS page rendered once, in a single load, and I read it then. Only RDS and ElastiCache/EC2 pages have c0.b0 widget iframes. So NAT, WAF, CloudWatch alarm, RDS gp2/gp3 and EFS Standard could not be verified for us-east-1 by me either.

### Verdict per lab

| Lab | Basis lists what the steps create (and nothing else) | Figures | Verdict |
| --- | --- | --- | --- |
| gl-06 | 1 NAT + 1 EIP. Correct (public and private subnets have no auto-assign; no instance). | 0.10 / 1.20 reproduce | Approve; fix typo "rate rate" (LD-PA-003) |
| ul-06 | Same, from its own criteria. | 0.10 / 1.20 | Approve; same typo |
| gl-07 | t3.micro, 1 public IPv4 (default subnet), 8 GB gp3 root (AL2023 default), 8 GB gp3 data, 1 snapshot (upper bound 8 GB). Complete. | 0.04 / 0.43 (0.03547, 0.4256) | Approve; drop gp3/snapshot asterisk (AWS-PA-003) |
| ul-07 | t3.micro (type not stated), 1 IPv4, root gp3, EFS (unread). Reasonable. | 0.04 / 0.72 (computed 0.03258 / 0.39093; 0.72 kept by design) | Approve with wording change (AWS-PA-004, AWS-PA-005) |
| gl-08 | 1 ALB in 2 subnets = 2 public IPv4; t3.micro with no public IP (create-subnet does not auto-assign; run-instances has no public-IP flag); 8 GB gp3 root. Correct. | 0.08 / 1.06 (0.07693, 1.05093) | Approve; ALB now verified (AWS-PA-003) |
| ul-08 | gl-08 pattern plus web ACL plus one managed rule group. Complete. | 0.09 / 1.26 (0.08943, 1.25093) | Approve with AWS-PA-002 (same-hour 0.10) |
| gl-09 | ASG desired 1: t3.micro, IPv4 (default subnet), 8 GB root. ASG and template free. Correct. | 0.03 / 0.40 (0.02036, 0.39093) | Approve |
| ul-09 | Peak 2 instances, 2 IPv4, 2 roots, 2 target-tracking alarms. Correct (target tracking creates a high and a low alarm). | 0.05 / 0.79 (0.04107, 0.78853) | Approve |
| gl-14 | db.t3.micro Single-AZ, 20 GB, not public (no IPv4). Storage at the io1 rate is a valid upper bound. | 0.05 / 0.52 (0.04294, 0.51533) | Approve |
| ul-14 | 2 instances plus a 20 GB manual snapshot = 60 GB at the io1 bound. Conservative and complete. | 0.10 / 1.12 | Approve |
| gl-18 | 1 Fargate task 0.25 vCPU / 0.5 GB with public IPv4 (assignPublicIp ENABLED). Correct. | 0.03 / 0.42 | Approve; reword rate (LD-PA-002) |
| ul-18 | 2 tasks at two tiers, both counted as concurrent. Conservative. | 0.08 / 1.13 | Approve; reword rate |
| gl-19 | EKS control plane only. Correct (no node group in the steps). | 0.20 / 2.40 | Approve |
| ul-19 | Control plane plus one node assumed t3.micro. Criteria do not fix the node type or count; the CLI default is larger. | 0.24 / 2.83 for the stated assumption | Concerns (AWS-PA-001) |
| gl-21 | 1 cache.t3.micro Redis node. Correct. | 0.04 / 0.41 | Approve |
| ul-21 | AWS path only, gl-21 equivalent; HCP path is free. | 0.04 / 0.41 | Approve |

### Rates I verified

| Resource | Rate | URL | Verbatim text | Region evidence | Effect on labs |
| --- | --- | --- | --- | --- | --- |
| EBS gp3 storage | $0.08/GB-month | https://aws.amazon.com/ebs/pricing/ | "General Purpose SSD (gp3) - Storage $0.08/GB-month" | Region control read back "US East (N. Virginia)" | Confirms 0.08. Asterisk can go (gl-07, ul-07, gl-08, ul-08, gl-09, ul-09, ul-19). |
| EBS gp2 storage | $0.10/GB-month | same | "General Purpose SSD (gp2) Volumes $0.10 per GB-month of provisioned storage" | N. Virginia | Not used by these labs. Note only. |
| EBS Snapshot Standard | $0.05/GB-month | same (snapshot section) | "Standard $0.05/GB-month" | N. Virginia (same selector) | Confirms gl-07 snapshot. |
| EBS billing granularity | per second, 60 s minimum; 30-day month in examples | same | "billed in per-second increments, with a 60-second minimum" | n/a | Confirms fractional hours and 720 h. |
| ALB hourly | $0.0225/h; LCU $0.008 | https://aws.amazon.com/elasticloadbalancing/pricing/ | "using pricing in the US-East-1 Region as follows" (Example 1) then "Adding the hourly charge of $0.0225, the total Application Load Balancer costs are" | The example names US-East-1, so this is now verified for us-east-1 (the writer marked it region not named). | Confirms 0.0225. Asterisk can go on gl-08 and ul-08. |
| ELB partial hour | full hour | same | "Each partial Application Load Balancer hour used is billed as a full hour." | n/a | Confirms 2 h for a 90 min lab. |
| Public IPv4 | $0.005/h in use or idle; per second, 60 s minimum | https://aws.amazon.com/vpc/pricing/ | "Hourly charge for In-use Public IPv4 Address $0.005" | Flat, not per region | Confirms. |
| ALB public IPv4 count | 2 (one per AZ) | same, Public IPv4 pricing example 1 | "One Elastic load balancer with two in-use public IPv4 address" | n/a | Supports the 2-IPv4 count in gl-08 and ul-08. |
| WAF partial-hour treatment | Not documented (only "prorated hourly") | https://aws.amazon.com/waf/pricing/ | "Monthly fees are prorated hourly." | n/a | See AWS-PA-002. |
| Public-page text for CloudWatch alarm | $0.10 per alarm metric per month | https://aws.amazon.com/cloudwatch/pricing/ | "Four standard resolution alarms = $0.10 per alarm metric * 4 = $0.40 per month" | Nearby note says "based on US East Regions", not N. Virginia | Still not verified for us-east-1 (effect on ul-09: about $0.007 per day). |

Still not verified by me, so the labs' markers stay: NAT gateway $0.045/h (the page example is US East (Ohio); the price table did not render); WAF web ACL $5 and rule group $1 (worked example, region not named, "Pricing may vary across AWS Regions"); RDS gp2/gp3 (tokens only, the io1 $0.125 bound from the N. Virginia page example stays); EFS Standard (tokens only). None of these changes a figure by a cent except as noted in AWS-PA-002.

### Rulings on the Lead Dev pre-check

| Id | Ruling |
| --- | --- |
| LD-PA-001 (four same-hour figures "below their own basis") | Refuted. The recomputation applies full-hour rounding to every resource. The basis lines say "billed in full hours" only for the ALB (and NAT, RDS, ElastiCache in their labs); EC2, EBS, public IPv4 and Fargate bill per second, and the EBS and VPC pages say so. Correct figures under the stated basis: gl-08 0.07693 (0.08), gl-09 0.02036 (0.03), ul-09 0.04107 (0.05), ul-08 0.08943 (0.09). Only ul-08 changes, and for a different reason (AWS-PA-002). |
| LD-PA-002 (Fargate rate wording) | Confirmed, low. "0.25 vCPU at $0.000011244/vCPU-second ($0.0405/h)" reads as if $0.0405/h were the price of 0.25 vCPU. Reword as below. |
| LD-PA-003 (typo "rate rate") | Confirmed, low (gl-06, ul-06). |
| LD-PA-004 (gl-18 note) | Agreed, no change. |
| LD-PA-005 (unverified rates) | Partly resolved: ALB and EBS are now verified (see the table). NAT, WAF, RDS storage, EFS and the alarm stay unverified. |

### Findings

**AWS-PA-001 (medium) ul-19 node assumption is below the CLI default.** The acceptance criteria fix neither node type nor count ("one managed node group added briefly"). The `aws eks create-nodegroup` defaults (t3.medium, 20 GiB disk, and a scaling config whose desired size is 2, per the EKS CLI/API reference; not a pricing-page fact, so the Teacher should confirm it with the AWS Knowledge MCP) are larger than the t3.micro / 1 node the basis assumes. Figures with the same rules:

| Case | Same-hour | Forgotten 24 h |
| --- | --- | --- |
| stated (t3.micro x1, 20 GB) | 0.24 | 2.83 |
| t3.medium x1 ($0.0416/h) | 0.30 | 3.58 |
| t3.medium x2 (CLI default desired size) | 0.40 | 4.75 |

Fix, either: (a) pin the criterion ("t3.medium, desired size 1") and set the figures to 0.30 / 3.58 with a basis of "EKS $0.10/h + 1 t3.medium $0.0416/h + 1 public IPv4 $0.005/h + 20 GB gp3 $0.08/GB-month"; or (b) keep t3.micro and add the criterion "node type t3.micro, desired size 1". Option (b) leaves the figures as they are and is the smaller change. Do not leave it unpinned.

**AWS-PA-002 (low) ul-08 same-hour: WAF partial-hour treatment is undocumented.** The page says only "prorated hourly". Under the fractional reading ul-08 is 0.08943 (0.09); if a partial WAF hour bills as a full hour it is 0.09360, which rounds up to 0.10. The plan says never round down under doubt, so set ul-08 `sameHourEstimateUsd` to 0.10 and the basis to "same-hour ≈ $0.10". The 24 h figure is unaffected (1.26).

**AWS-PA-003 (low) Unverified markers now stale for ALB and EBS.** Remove the asterisk and the "worked-example rate whose region the page does not name" clause for ALB (gl-08, ul-08) and for EBS gp3 and snapshot (gl-07, ul-07, gl-08, ul-08, gl-09, ul-09, ul-19), keeping it for the NAT, WAF, RDS storage, CloudWatch alarm and EFS. Update `docs/labs-and-safety.md` "Example rates": ALB row to "Verified us-east-1 (page example names US-East-1)", EBS gp3 and snapshot rows to "Verified N. Virginia (EBS pricing page)"; add gp2 $0.10/GB-month. The docs say "partial hour bills as full hour" for ALB already.

**AWS-PA-004 (low/medium) "floor" wording is inaccurate and "LCU" appears where there is no load balancer.** The same-hour figure assumes every resource runs for the full estimatedMinutes, so it is padded, not a floor; and "LCU/usage charges" is meaningless for gl-06, 07, 09, 14, 18, 19, 21 and their twins. Replace in all 16 basis lines:

- Old: "This is a floor: it excludes data transfer and LCU/usage charges. Re-read the pricing page before you run the lab."
- New: "This excludes data transfer and per-GB or per-request usage charges (for example NAT per-GB processing or ALB LCU-hours), so a real bill can be higher. Re-read the pricing page before you run the lab."

And in all 16 stopChargesPanel lines: "(a floor; see the cost basis)" becomes "(excludes usage charges; see the cost basis)". The repeated 24 h figure itself is correct and consistent everywhere.

**AWS-PA-005 (low) ul-07: the basis presents a padded figure as computed.** The computed 24 h figure without EFS is 0.40 (0.39093); 0.72 is the old figure kept because EFS Standard is unread. Add "computed without EFS: $0.40; the $0.72 is the earlier figure kept while the EFS rate is unread; the lab stores one test file, so EFS storage is a small fraction of a cent per day at any published Standard rate". Do not claim the exact EFS rate.

**Wording fixes carried from the pre-check (no new id):**
- gl-06, ul-06: "N. Virginia rate rate not verified" becomes "N. Virginia rate not verified".
- gl-18, ul-18: "0.25 vCPU at $0.000011244/vCPU-second ($0.0405/h)" becomes "0.25 vCPU at $0.000011244 per vCPU-second ($0.0405 per vCPU-hour, so $0.0101/h for 0.25 vCPU) + 0.5 GB at $0.000001235 per GB-second ($0.00445 per GB-hour)". The figures 0.03 / 0.42 and 0.08 / 1.13 stay.

### Learner-facing text check

- The "rate not verified on <date>; re-check the pricing page before running" marker is clear and non-alarming; the bare "not reconciled" is gone. Keep it, with the narrower set in AWS-PA-003.
- The basis line is long but readable. The asterisk and its explanation are far apart (gl-07 and gl-08 in particular); acceptable, though the marker would read better right after the explanation of each starred rate.
- stopChargesPanel repeats the same 24 h number as the basis and the field in all 16 labs.

### Result

All 16 pairs of figures reproduce, the resource lists are complete against the steps (the gl-08 and ul-08 count of 2 public IPv4 on the ALB is confirmed by the VPC page's own example), and no figure is below its computed cost. Open before close: AWS-PA-001 (ul-19 node pin), AWS-PA-002 (ul-08 0.10), AWS-PA-003 and AWS-PA-004 (wording), AWS-PA-005, plus the two wording fixes above. After they are applied, no re-pricing is needed except ul-08 same-hour and, if option (a) is chosen, ul-19.

Part A: not yet

Overall: concerns

## Technical confirmation (fix pass)

Commit 0f3dc9c ("D6 Part A fix pass"), read-only. Inputs: the "Fix pass (review)" section of pricing-claims.md, pricing-review-TEACHER.md, the appended outcome in pricing-leaddev-precheck.md, and the 16 labs as they now stand.

### 1. AWS-PA status

| Id | Status | Evidence |
| --- | --- | --- |
| AWS-PA-001 (ul-19 node assumption) | Gone as to pricing; new wording finding AWS-PA-006 | ul-19 now prices 2 x t3.medium, 2 IPv4, 2 x 20 GB gp3 plus EKS: 0.40 / 4.75; the t3.micro alternative 0.24 / 2.83 is stated. |
| AWS-PA-002 (ul-08 same-hour) | Gone as to the figure (0.10); new finding AWS-PA-007 | Field, basis and the WAF-full-hour reading agree at 0.10. |
| AWS-PA-003 (stale markers) | Gone | No asterisks or "worked-example" wording in the 16 labs; ALB and EBS rows in docs/labs-and-safety.md read "Verified"; gp2 added; NAT, WAF, CloudWatch alarm and RDS storage keep "not verified". |
| AWS-PA-004 ("floor", "LCU") | Gone | No "floor" in any lab. "LCU" appears only in gl-08 and ul-08. Panels read "at least $X (see the cost basis)". |
| AWS-PA-005 (ul-07 padded figure) | Gone | Basis says "a cautious figure, not a calculated one (the parts we could price come to about $0.39)"; my computed 0.39093 agrees. |
| LD-PA-001 | Withdrawn (recorded in the precheck) | Agreed. |

### 2. Second-role check

| Id | Check |
| --- | --- |
| TEACHER-PA-001 (exclusions per lab) | Confirmed. Default "data transfer not included"; gl-06/ul-06 add NAT per-GB processing; gl-08/ul-08 add LCU and data transfer; ul-08 adds WAF requests $0.60 per million; ul-18 adds logs. |
| TEACHER-PA-002 (gl-14, ul-14) | Confirmed. The Teacher's text is used verbatim; no "at least" on the io1-overstated figures; "costly" is gone. Figures 0.05 / 0.52 and 0.10 / 1.12 reproduce. |
| TEACHER-PA-003 (ul-07) | Confirmed. Text verbatim; 0.72 labelled cautious. |
| TEACHER-PA-004 ("floor" jargon) | Confirmed. All panels use "at least $X (see the cost basis)". |
| TEACHER-PA-005 / LD-PA-003 ("rate rate") | Confirmed gone. |
| LD-PA-002 (Fargate rate wording) | Confirmed. "per vCPU-hour" and "per GB-hour" are used; 0.0405 x 0.25 + 0.00445 x 0.5 = 0.01235 (about $0.0124/h) and 0.0405 x 0.5 + 0.00445 x 1 = 0.02470 ($0.0247/h) both hold. |

### 3. Recomputation from the basis text as written

Rules: full hours only where the text says "billed in full hours" or "(full hours)"; everything else fractional; month 720 h; round up.

| Lab | Same-hour computed (field) | 24 h computed (field) |
| --- | --- | --- |
| gl-06, ul-06 | 0.09625 -> 0.10 (0.10) | 1.20000 (1.20) |
| gl-07 | 0.03547 -> 0.04 (0.04) | 0.42560 -> 0.43 (0.43) |
| ul-07 | 0.03258 -> 0.04 (0.04) | 0.72 by design; priced parts 0.39093 (about $0.39, as stated) |
| gl-08 | 0.07693 -> 0.08 (0.08) | 1.05093 -> 1.06 (1.06) |
| ul-08 | 0.08943 fractional-WAF; 0.09360 with WAF in full hours -> 0.10 (0.10) | 1.25093 -> 1.26 (1.26) |
| gl-09 | 0.02036 -> 0.03 (0.03) | 0.39093 -> 0.40 (0.40) |
| ul-09 | 0.04107 -> 0.05 (0.05) | 0.78853 -> 0.79 (0.79) |
| gl-14 | 0.04294 -> 0.05 (0.05) | 0.51533 -> 0.52 (0.52) |
| ul-14 | 0.09283 -> 0.10 (0.10) | 1.11400 -> 1.12 (1.12) |
| gl-18 | 0.02601 -> 0.03 (0.03) | 0.41622 -> 0.42 (0.42) |
| ul-18 | 0.07054 -> 0.08 (0.08) | 1.12867 -> 1.13 (1.13) |
| gl-19 | 0.20000 (0.20) | 2.40000 (2.40) |
| ul-19 | 0.39529 -> 0.40 (0.40) | 4.74347 -> 4.75 (4.75) |
| gl-21, ul-21 | 0.03400 -> 0.04 (0.04) | 0.40800 -> 0.41 (0.41) |

Every field, basis figure and panel figure matches. One exception in reading: ul-08 reaches 0.10 only if the WAF fees are counted in full hours, and the basis does not say so (AWS-PA-007).

### 4. ul-19 default node count

Correct the wording. The basis says "2 t3.medium nodes (the create-nodegroup default)". Per the writer, the documentation confirms t3.medium and a 20 GiB disk as defaults but states no default desired size, so "the create-nodegroup default" presents an assumed count as documented. (My earlier note in AWS-PA-001 that the default desired size is 2 came from memory of the CLI reference and is not established; do not rely on it.) Replace, exactly, the phrase

"plus 2 t3.medium nodes (the create-nodegroup default) $0.0416/h each"

with

"plus 2 t3.medium nodes $0.0416/h each (t3.medium is the create-nodegroup default; the default node count is not documented, so 2 is assumed)".

The rest of the line stays, including "Choosing 1 x t3.micro lowers this to about $0.24 / $2.83." The docs note at labs-and-safety.md line 68 already states the assumption correctly. The catalog row at line 96 still says "UL: Fargate profile or one managed node", which disagrees with the 2-node basis; change "one managed node" to "managed nodes (priced as 2)". Figures stay 0.40 / 4.75.

### New findings

- **AWS-PA-006 (low):** the ul-19 basis states the node count as documented (fix in section 4).
- **AWS-PA-007 (low):** ul-08's 0.10 depends on WAF fees being counted in full hours, but the basis says "(full hours)" only for the ALB. As written, the WAF fees bill fractionally and give 0.09. Replace "1 WAF web ACL $5.00/month, 1 managed rule group $1.00/month" with "1 WAF web ACL $5.00/month and 1 managed rule group $1.00/month (WAF partial hours counted as full hours here)". Figures stay 0.10 / 1.26.

Part A: not yet

Overall: concerns

## Technical confirmation (final wording, 44ea124)

AWS-PA-006 (ul-19 node count) Gone: the basis now says t3.medium is the default and "the default node count is not documented, so 2 is assumed"; figures 0.40 / 4.75 unchanged. AWS-PA-007 (ul-08 WAF full hours) Gone: "WAF partial hours counted as full hours here" added, so the basis as written gives 0.0936 -> 0.10 (24 h 1.26); the catalog row reads "managed nodes (priced as 2)".
Second-role check on ul-07: the basis and panel are the Teacher's text plus "Re-check current pricing before you run" and "check current pricing"; figures unchanged (0.04 / 0.72, priced parts 0.39093), so nothing to recompute. Confirmed.

Part A: close

Overall: approve
