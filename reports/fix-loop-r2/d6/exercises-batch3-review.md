# D6 Part B batch 3: exercises review (issue ids AWS-DE3-###)

## Technical review (e668531)

Method: read the 24 files at e668531 (scenario, constraints, artifact, rubric, constraint_reason), the two writer reports, the plan's Part B method, batch 1's review, and lessons 4.1 to 4.4 plus 3.3 (SCT/DMS) and 2.2 (quotas). Regex over all lessons (case-insensitive) for peering, SCT, hibernation, multipart, ECMP, usage plan and backoff. AWS docs MCP checks:
- EBS Snapshot Archive and AWS Backup EBS cold storage: restore takes up to 72 hours; archived snapshots are full snapshots and archiving is recommended for monthly/quarterly/yearly points, not daily incrementals.
- AWS Backup cold storage: 90-day minimum.
- API Gateway: "throttles and quotas are applied on a best-effort basis ... targets rather than guaranteed request ceilings".
- Site-to-Site VPN: 1.25 Gbps standard per tunnel, Large Bandwidth Tunnel 5 Gbps on Transit Gateway/Cloud WAN only; Transit Gateway ECMP uses both tunnels of one connection for 2.5 Gbps.
- EC2 hibernation: Linux, RAM under 150 GiB, encrypted root (96 GiB is fine).
- S3 Lifecycle: 128 KB default transition floor; Glacier minimums 90 and 180 days.
- Regional NAT gateway and S3 Files both exist.
- VPC peering: no processing charge, same-AZ free, cross-AZ charged.

Arithmetic checked:
- 180 TB at 700 Mbps = 23.8 days (26.2 days if TiB); inside 60 days.
- 4,000 stations x 8,640 readings = 34.56 M objects/day; hourly batches = 96,000 (99.7 percent cut).
- 3 Gbps / 1.25 Gbps = 2.4, so 3 tunnels minimum; 2 VPN connections (4 tunnels) give 5 Gbps, 3.75 Gbps with one tunnel down.
- 1,500 rps / 15 per vCPU = 100 vCPUs against the 64 allowance.
- 10 x 100 + 100 x 4 = 1,400 rps.
- 2 of 60 TB stays on NAT (3.3 percent, so a 96.7 percent cut).
- 10 h x 5 days = 50 of 168 h, a 70.2 percent cut.
- 1.1 TB + 3 x 40 GB = 1.22 TB.
- 58 + 27 + 15 = 100 percent.

### Verdicts

| # | Exercise | Verdict |
| --- | --- | --- |
| 1 | de-saa-4.1-s01 | approve |
| 2 | de-saa-4.1-s02 | approve (one minor) |
| 3 | de-saa-4.1-s04 | changes required (major) |
| 4 | de-saa-4.1-s05 | approve with minor fixes (answers the Lead Dev r6 question) |
| 5 | de-saa-4.1-s06 | changes required (major) |
| 6 | de-saa-4.1-s08 | approve |
| 7 | de-saa-4.1-s09 | approve (one minor) |
| 8 | de-saa-4.1-s10 | approve (one minor) |
| 9 | de-storage-migration | approve (23.8 days confirmed) |
| 10 | de-outposts | approve |
| 11 | de-purchasing | changes required (major) |
| 12 | de-saa-4.2-s01 | approve |
| 13 | de-saa-4.2-s02 | changes required (major) |
| 14 | de-saa-4.2-s03 | approve |
| 15 | de-saa-4.2-s04 | changes required (major) |
| 16 | de-saa-4.2-s05 | changes required (major) |
| 17 | de-db-migration | approve (SCT + DMS taught in 3.3-K06; "optionally continuously replicate" covers the 30-minute cutover) |
| 18 | de-saa-4.3-s02 | approve (one minor) |
| 19 | de-saa-4.3-s04 | approve (one minor; Timestream LiveAnalytics closure is taught in 4.3-S04) |
| 20 | de-saa-4.4-s03 | approve (one minor) |
| 21 | de-saa-4.4-s05 | approve (one minor) |
| 22 | de-saa-4.4-s07 | approve (one minor) |
| 23 | de-tgw | approve (Lead Dev concern answered below; one optional minor) |
| 24 | de-throttling | approve (one minor) |

### Findings

**AWS-DE3-001 (major) de-saa-4.1-s06, scenario sentence 2 and constraint 7.** The scenario says restores of points older than 35 days "may wait up to a full working day". The cold tier the exercise is built for cannot meet that. AWS Backup's EBS cold tier is the EBS Snapshot Archive, and a restore from it takes up to 72 hours. Its archived points are also full snapshots, and AWS recommends archiving monthly, quarterly or yearly points rather than daily ones, so "daily points for 7 years" can cost more cold than warm. Replace the second sentence with: "The insurer requires every recovery point to be held for 7 years: one point a month, restored often in its first 35 days and after that only a few times a year, when a wait of up to four days is acceptable." Replace constraint 7 with: "Restores of points older than 35 days may take up to four days". In the last sentence replace "the first 35 days' points" with "points in their first 35 days". r6 and r7 stand. Teacher to confirm the new figures.

**AWS-DE3-002 (major) de-saa-4.1-s04, scenario arithmetic.** The volume is 1 TB and holds 800 GB, and the import is at most 150 GB, so it reaches 950 GB and never fills the volume. The stated problem ("has twice filled that volume") and r7 do not follow from the figures. Replace "one 1 TB block volume holding 800 GB today; a bulk catalogue import of up to 150 GB, arriving about weekly," with "one 1,000 GiB block volume holding 900 GiB today; a bulk catalogue import of up to 200 GiB, arriving about weekly,". In r7 replace "A 150 GB import" with "A 200 GiB import". (900 + 200 = 1,100 GiB against 1,000 GiB.)

**AWS-DE3-003 (minor) de-saa-4.1-s04, second design.** A managed relational database with storage auto scaling would also satisfy "nobody wakes up". Add to the scenario after "block volume": "The publishing database is self-managed software on that one server and stays there." It is a fact, not a solution.

**AWS-DE3-004 (minor) de-saa-4.1-s02, r6.** Constraint 5 funds only the next 90 days (1.22 TB), but r6 allows up to 1.5 TB. Replace r6 with: "The initial volume is between 1.22 TB (today's 1.1 TB plus 90 days at 40 GB a month) and 1.5 TB, with any rounding or margin stated".

**AWS-DE3-005 (minor) de-saa-4.1-s05, r6 (Lead Dev question).** It does not name a class, but it lists the three decision criteria in the lesson's own order (lowest storage price, retrieval time, minimum storage period). That points at one class by elimination, and the minimum-period clause signals the trap. The one-best-design logic holds: Glacier Instant Retrieval beats Standard-IA on storage price, and Intelligent-Tiering reaches the same price only from day 90, so days 30 to 90 cost more. Move "lowest" into constraint 5 and make r6 an outcome. Replace constraint 5 with: "Scans older than 30 days must be held at the lowest storage cost that still lets a clerk open one in under a second". Replace r6 with: "Scans older than 30 days are held at the lowest storage cost that still opens in under a second, the record shows no scan is charged an early-removal fee under the 7-year retention, and thumbnail storage and request cost does not rise".

**AWS-DE3-006 (minor) de-saa-4.1-s05, r7 and scenario day-60 ambiguity.** Noncurrent-version expiry counts days from when a copy was replaced, not from scan creation, so "gone by day 60" cannot be met exactly by a correct rule. Replace "the superseded copies are never read after 60 days" with "the superseded copies are never read more than 60 days after being replaced". Replace r7 with: "Superseded scan copies are gone 60 days after they are replaced, broken upload leftovers within 7 days and scans at the 7-year mark, each with the day number stated".

**AWS-DE3-007 (minor) de-saa-4.1-s09, object size and leap days.** Object size is not given, and the default 128 KB floor and the IA minimum billed size can change the answer. "10 years" is 3,652 days, not 3,650. After "trial documents" add "of about 3 MB each"; replace "for 10 years" with "for 10 years (count 3,650 days)". Stage design checked and correct: Standard to day 30, Standard-IA to day 90 (Glacier Instant would bill early removal, since 60 days is under 90), Glacier Flexible Retrieval Standard (3 to 5 h) to day 365, then Deep Archive Standard (within 12 h), expiry at day 3,650. One-Zone IA is excluded by the data-centre rule.

**AWS-DE3-008 (minor) de-saa-4.1-s10, r7.** "The smallest number of distinct storage services" can be contested by S3 Files (a file system view of a bucket, current but not taught). Replace r7 with: "No data set is placed on a service priced for a feature it does not need (for example, a managed file-system product with no Windows, HPC or NetApp requirement), and the record states the number of services used and why". Lesson addition requested (not for the exercise): one sentence in lesson 4.1 S10 on S3 Files.

**AWS-DE3-009 (major) de-purchasing, constraint 5 against r6.** "The deepest discount on usage that has run steadily" pulls toward a Standard Reserved Instance or EC2 Instance Savings Plan, which are deeper than a Compute Savings Plan (lesson K04). Those stop applying when half the floor moves to a serverless container service and instance families change, which fails r6. Replace constraint 5 with: "Finance wants the steady 40 vCPUs discounted for the next 3 years and will not re-buy the commitment when its mix of containers and instance families changes". In r6 replace "sized to the 40 vCPU steady floor" with "sized to the steady floor's hourly spend (40 vCPUs)". Note that a Savings Plan is a dollar-per-hour commitment, not a vCPU count.

**AWS-DE3-010 (major) de-saa-4.2-s02, second defensible design and inconsistent constraint 7.** The engine is used 07:30 to 18:00 on weekdays only. A scheduled stop at night and a scheduled start at about 07:05 (table rebuilt by 07:30) meets "not billed overnight" and the 3-minute wait with no hibernation. Constraint 7 ("not stored anywhere else") also contradicts "after any start it needs 25 minutes to rebuild". Replace the last-but-one sentence with: "Brokers open it at unpredictable times on weekdays between 07:30 and 18:00, sometimes with hours between uses, and never overnight or at weekends; each time they will wait at most 3 minutes from asking for it to a usable engine." Replace constraint 5 with: "Finance does not want the engine billed for server time while no broker is using it, including overnight and weekends". Replace constraint 7 with: "The engine's table can be rebuilt only by re-reading every source feed, which takes 25 minutes". Replace r6 with: "The engine is not billed for server time while idle and is usable within 3 minutes of any start, without the 25-minute rebuild". Note for Teacher: hibernation resume reads 96 GiB back from the root volume, so the 3 minutes depends on root-volume throughput (about 550 MiB/s or more); the record should state that as an assumption.

**AWS-DE3-011 (major) de-saa-4.2-s04, target lets a schedule alone pass.** A weekday 10-hour schedule alone cuts server-hours 70.2 percent, so the 60 percent target is met without touching the two-Availability-Zone layout. Single-AZ alone gives 50 percent and fails. Schedule alone and schedule plus single-AZ are both defensible. Replace "60 percent" with "75 percent" in the scenario, constraint 7 and r7, and add to the scenario: "Count run-rate as proportional to server-hours." Schedule alone (70.2 percent) then fails; schedule plus single-AZ (about 85 percent) passes, which is the lesson-4.2 S04 pairing ("strict schedules" and "leaner topology").

**AWS-DE3-012 (major) de-saa-4.2-s05, r7 asks for peaks the scenario does not give.** Only averages are stated, and the counts come out at 16 and 4 again, so "rather than copied from today's 16 and 4 servers" misleads. Transcription: 16 x 8 vCPUs = 128 vCPUs at 88 percent is about 113 needed, with memory 32 GiB x 18 percent = about 6 GiB per server, so a compute family (2 GiB per vCPU) keeps 16 servers of 8 vCPUs. Speaker-index: 4 x 64 GiB = 256 GiB at 90 percent is about 230 GiB needed, CPU 12 percent of 64 = about 8 vCPUs, so a memory family (8 GiB per vCPU) gives 4 servers of 8 vCPUs and 64 GiB, half the vCPUs paid for. Replace r7 with: "New instance sizes are derived from the stated averages (about 113 of the transcription fleet's 128 vCPUs in use, about 230 of the speaker-index fleet's 256 GiB in use), each fleet size and instance size is stated, and neither service is given less of its limiting resource than it uses today".

**AWS-DE3-013 (minor) de-saa-4.3-s02, vendor engine unstated.** "Only one of the two popular engines" does not say which, so r6's "the vendor add-on" cannot be checked. PostgreSQL is still decided by the nested-attribute and join-heavy requirements plus extensions (lesson S02), and RDS by the "fixed-size instance" requirement (lesson K07). Replace r6 with: "The chosen engine supports the filtering on nested attributes and the join-heavy month-end reports, the record says how the vendor's in-database add-on would be loaded, and explains why the developers' MySQL familiarity does not override them".

**AWS-DE3-014 (minor) de-saa-4.3-s04, r7 not checkable and Athena.** Scenario figures give no prices, so "the largest expected saving" cannot be checked. Replace r7 with: "The record states, for each workload, the figure from the scenario that drives its saving (for example, analysts read 4 of 60 columns, and gauge readings are never edited) and says what would be measured to confirm it". Athena on S3 is also a defensible columnar choice, but it is not in lesson 4.3. Accept it as the same type if justified; r6 grades the type, not the product.

**AWS-DE3-015 (minor) de-saa-4.4-s03, Regional NAT gateway.** A Regional NAT gateway (current, not taught) also satisfies "no cross-AZ hops" and "survives one AZ failing". Accept either in r7. No text change is needed. Note it in the plan; a lesson addition is optional.

**AWS-DE3-016 (minor) de-saa-4.4-s05, r6 overstates.** A CDN does not remove the internet-egress charge; it replaces the origin-egress charge with the cheaper edge rate, and origin-to-edge transfer is free. Replace "a fix that removes that driver's transfer charge" with "a fix that removes or reduces that driver's transfer charge". The rest of r6 stands.

**AWS-DE3-017 (minor) de-saa-4.4-s07, "minimum" is ambiguous and router facts are missing.** A VPN connection always has two tunnels, so the smallest purchasable allocation is 2 connections (4 tunnels, 5 Gbps), not 3 tunnels. "No more than one tunnel beyond the minimum" is a hint, and it clashes with constraint 7. Also, ECMP needs BGP and ECMP on the branch router, and one flow is capped at one tunnel's rate. Replace constraint 7 with: "Finance will not pay for more VPN connections than the stated figures require". Replace r6 with: "The allocation provides at least 3 Gbps at the documented per-tunnel ceiling, still provides at least 2 Gbps with any one tunnel down, and uses the fewest VPN connections that achieve both, noting that each connection carries two tunnels". Add to the scenario after "1.25 Gbps": "The router supports BGP and equal-cost multi-path routing, and the sync runs as many parallel transfers."

**AWS-DE3-018 (minor, optional) de-tgw (Lead Dev concern).**
- **Fact: true.** VPC peering has no data-processing charge, and traffic within an Availability Zone is free (cross-AZ is charged at the standard rate). Transit Gateway bills per attachment-hour and per GB processed. A VPC can be both attached to a Transit Gateway and peered with another VPC; the longest-prefix route (the peered VPC's CIDR) takes the peering path.
- **Taught: largely yes.** Regex over lessons for the objective SAA-4.4-K06: only lesson 4.4 K06 (peering also in 1-1 and 3-4). K06 teaches every component: "no charge to create a VPC peering connection", "all data transfer ... within an Availability Zone is free; charges apply ... cross Availability Zones", TGW "billed ... for each VPC attachment-hour and for the data it processes", and "choose peering for a small, static number of VPCs". It frames them as alternatives and does not say they can be combined. So the writer's "no lesson teaches this" is half right: the facts are taught, the combined pattern is one inference step.
- **Text names nothing.** r7 and constraint 6 never name peering, so there is no giveaway. The exercise title ("Transit Gateway and peering") already names both, but titles are fixed by the method.
- **Proposed fix: keep, make r7 checkable, add one lesson sentence.** Replace r7 with: "The 80 TB a month between the catalogue-data and analytics VPCs does not pass through the per-gigabyte processing charge the other VPCs' traffic incurs, and the record states what transfer charge, if any, still applies to that path". Request under "Lesson additions requested": add to lesson 4.4 K06 "A VPC can be attached to a Transit Gateway and also peered with one other VPC; the more specific peering route carries that pair's heavy traffic, so it avoids the Transit Gateway's per-GB charge." Do not drop the requirement; it is the exercise's deciding cost figure. r6 nit: "no existing VPC's configuration is edited" holds only if existing VPCs already route the whole private range to the hub; acceptable, no change.

**AWS-DE3-019 (minor) de-throttling, constraint 6 and r7.** API Gateway throttles are best-effort targets, not guaranteed ceilings, so "must never receive more than 1,500" overstates. Replace constraint 6 with: "The gateway's total ceiling for any combination of callers, including the company's own front end, must be set so that the backend is never offered more than 1,500 requests per second". Append to r6: ", and the record notes that gateway limits are best-effort targets and states the burst setting". The scenario also asks for caller guidance on rejected requests, but no rubric item grades it; add to r6 "and the caller guidance tells partner apps to back off between retries of rejected calls" (retry with backoff is taught in 2.2 K10 and 4.4 S06).

No finding (checked):
- de-saa-4.1-s01 (batching and multipart plus abort rule are determinate).
- de-saa-4.1-s08 (Intelligent-Tiering has no retrieval or minimum-duration charge; r6 and r7 are outcomes).
- de-storage-migration (DataSync plus Transfer Family; the copy fits 60 days even at 26 days if TiB).
- de-outposts (Local Zones excluded by the 150 km fact, Wavelength by no 5G need; rack-sized points to a rack).
- de-saa-4.2-s01 (ALB, NLB with two Elastic IPs, GWLB is the minimum of three).
- de-saa-4.2-s03 (Lambda, Fargate and EC2 commitment).
- de-db-migration.
- de-saa-4.3-s02 (beyond AWS-DE3-013).

constraint_reason holds for all 24. No dollar prices appear (grep clean). No closed or retired service is named; Timestream for LiveAnalytics is referenced only as "closed to new customers", which the lesson labels. The Snow Family appears in none of the 24.

Batch 3: not yet

Overall: concerns

---

## Technical confirmation (fix passes)

Checked at 989f0bf (4.3/4.4) and e994421 "D6 batch 3a fix pass" (4.1/4.2). I read the Teacher's review, both "Fix pass" sections, and the 24 files as they now stand, read-only. Each changed text was checked against the lessons and the AWS facts in the first review.

### AWS-DE3 status

| Id | Status | Note |
| --- | --- | --- |
| 001 (4.1-s06) | Gone | One point a month, four-day wait and constraint 7 agree. 72 h is within 96 h. The first-35-days wording is consistent. |
| 002 (4.1-s04) | Gone | 1,000 GiB volume holding 900 GiB plus a 200 GiB import is 1,100 GiB, so it overflows. r7 matches. |
| 003 (4.1-s04) | Gone | The "self-managed software on that one server" sentence closes the managed-database design without naming a solution. |
| 004 (4.1-s02) | Gone | The 1.22 to 1.5 TB window is checkable against constraint 5. |
| 005 (4.1-s05) | Gone | "Lowest" moved to constraint 5 and r6 is an outcome. No class is named. Glacier Instant Retrieval is still the only option that clears it, because Intelligent-Tiering reaches the same price only from day 90. The merge with TEACHER-DE3-002 is sound. |
| 006 (4.1-s05) | Gone | The day-60 count is now from replacement, in both the scenario and r7. |
| 007 (4.1-s09) | Gone | About 3 MB per document and 3,650 days. The stage design is unchanged and determinate. |
| 008 (4.1-s10) | Gone | r7 no longer asks for the smallest service count. Residual minor: constraint 4 ("as few services as possible") still invites the S3 Files count contest. The Teacher approved it and it is untaught, so no change is needed. |
| 009 (de-purchasing) | Gone | Constraint 5 states the outcome (no re-buy when the mix changes) and does not name a plan. It is true of Compute Savings Plans and false of the deeper family-locked options, so the answer is determinate. |
| 010 (4.2-s02) | Gone, except r6 (see AWS-DE3-020) | Unpredictable use removes the scheduled-start design, and the rebuild-from-feeds constraint removes stop and start. Hibernation is the only design that meets it. |
| 011 (4.2-s04) | Gone | Schedule alone gives 70.2 percent, which is under 75. Single-AZ alone gives 50 percent. Schedule plus single AZ gives about 85 percent. "Proportional to server-hours" means downsizing does not count, so only the lesson's pairing passes. |
| 012 (4.2-s05) | Gone (replaced by the Teacher's r7) | The Teacher's r7 is accurate and prints no answers. Residual minor, see AWS-DE3-021. |
| 013 (4.3-s02) | Gone | r6 is checkable and leaves the engine to the learner. |
| 014 (4.3-s04) | Gone | The merged r7 is outcome-based, checkable from the scenario, and gives nothing away. |
| 015 (4.4-s03) | Gone (no change, by decision) | Either NAT design is accepted and recorded. |
| 016 (4.4-s05) | Gone | "Removes or reduces" is accurate for a CDN. |
| 017 (4.4-s07) | Gone | The answer is 2 connections (4 tunnels): 5 Gbps, 3.75 Gbps with one tunnel down; 1 connection gives 2.5 Gbps, under 3. The router sentence states facts about the device and does not choose the allocation. r6's "each connection carries two tunnels" is a taught fact, not the count. |
| 018 (de-tgw) | Gone (superseded by the user's trim) | Constraint 2 and r7 are removed, the orphan 80 TB sentence is removed, and "All of the VPCs are in one Region." is added. The design is still determinate: one hub, with a mesh excluded by constraints 1 and 2. r6's "no existing VPC edited" still holds with a summary route. Only the per-GB cost angle of K06 is no longer graded. |
| 019 (de-throttling) | Gone | Constraint 2 is now factually accurate. The best-effort caveat is left out on purpose because it is untaught. "The gateway" is generic and does not name API Gateway. |

### Second-role check on TEACHER-DE3-001 to 009

- **001:** Accurate and determinate; it gives no answer. Residual in AWS-DE3-021.
- **002:** Replaced by the AWS r6 plus the new constraint 5, and the merge is sound. The Teacher's "costs less than today" alone still admits Standard-IA.
- **003:** Covered by AWS-002. Arithmetic confirmed.
- **004:** Applied. It is accurate and does not reveal which stores need no work.
- **005:** Applied merged. Correct.
- **006:** Applied merged. Backoff is taught in 2.2 K10 and 4.4 S06.
- **007:** Superseded by the user's trim. Outcome checked above.
- **008:** Applied. "Hostname in Dovecote's own domain" fits Transfer Family with a custom hostname. Constraint 7's "the address it sends to" is generic and consistent.
- **009:** Merged into r6. The merge is sound except for the leak ruled on below.

### New findings

**AWS-DE3-020 (minor, blocks close: one phrase) de-saa-4.2-s02 r6 (Lead Dev concern).** Yes, "including the root-volume throughput it assumes" points at the mechanism. Hibernation writes RAM to the root volume and reads it back on resume, so naming root-volume throughput tells the learner that state is saved to and restored from the root volume. The Teacher's confirm-the-3-minutes intent is sound; the volume reference is the leak. Replace r6 with: "The engine is not billed for server time while idle and is usable at any start without the 25-minute rebuild, and the record says how the 3-minute start limit will be confirmed and what that confirmation assumes".

**AWS-DE3-021 (minor, optional) de-saa-4.2-s05 r7.** The Teacher's r7 is a floor only. A learner who moves speaker-index to 4 servers of 16 vCPUs on a memory family (more expensive than today) would still pass r7. This contradicts the scenario's "run-rate reduced". Optional append to r7: ", and neither fleet keeps more vCPUs or memory than its utilisation plus the headroom the record states". It does not block close.

Batch 3: not yet

Overall: concerns

AWS-DE3-020: Gone. The r6 text in de-saa-4.2-s02 matches the replacement verbatim at 9698d31 and no longer names the root volume. AWS-DE3-021 remains optional and unapplied, which does not block.

Batch 3: close
