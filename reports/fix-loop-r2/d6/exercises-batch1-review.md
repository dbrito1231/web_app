# D6 Part B batch 1: exercises review (issue ids AWS-DE1-###)

## Technical review (b422d65)

Method: read all 20 files at b422d65, the writer report, and the lessons 2.1 (S02, S03, K11). AWS facts checked with the AWS docs MCP where doubtful: SCPs bind member-account root users (orgs_manage_policies_scps); MACsec exists only on dedicated 10/100/400 Gbps connections (Direct Connect MACsec page). Arithmetic: 10 TB in 6 h = 3.7 Gbps (decimal) or 4.07 Gbps (TiB), so "roughly 4 Gbps" holds; 99.9 percent = 525.6 min = 8.76 h a year.

### Verdicts

| # | Exercise | Verdict |
| --- | --- | --- |
| 1 | de-federation | approve (one minor) |
| 2 | de-multi-account | approve (one minor) |
| 3 | de-direct-connect | changes required (major) |
| 4 | de-saa-1.2-s03 | changes required (major) |
| 5 | de-cloudhsm | approve |
| 6 | de-saa-1.3-s01 | approve (one minor) |
| 7 | de-saa-1.3-s03 | approve (one minor) |
| 8 | de-saa-1.3-s05 | approve |
| 9 | de-saa-1.3-s07 | approve (r6 rewrite) |
| 10 | de-saa-2.1-s02 | changes required (major) |
| 11 | de-saa-2.1-s03 | changes required (major) |
| 12 | de-saa-2.1-s04 | changes required (major) |
| 13 | de-saa-2.1-s06 | approve (one minor) |
| 14 | de-saa-2.1-s07 | approve (one minor) |
| 15 | de-multi-region-dr | changes required (major) |
| 16 | de-saa-2.2-s01 | approve |
| 17 | de-saa-2.2-s02 | approve (r6 rewrite) |
| 18 | de-saa-2.2-s04 | changes required (major) |
| 19 | de-saa-2.2-s07 | approve (one minor) |
| 20 | de-saa-2.2-s08 | approve |

### Findings

**AWS-DE1-001 (major) de-direct-connect, scenario last two sentences.** The requirement is not determinate. (a) "the link must still work if that circuit fails" gives no rate. A VPN backup (1.25 Gbps per tunnel) cannot meet the transfer tool's 3 Gbps abort threshold or the 4 Gbps figure, so "VPN backup works" and "VPN backup fails" are both defensible. (b) The five-day pilot has the same problem: only a VPN can be ready in five days, and it cannot sustain 3 Gbps either. (c) The encryption constraint does not fix a mechanism. Application TLS, MACsec (dedicated 10 Gbps connections only, not hosted) and VPN over Direct Connect (per-tunnel cap) each satisfy it, and they differ on the 4 Gbps figure. Replace the last two sentences of the scenario with:
"The lab has budget for one physical circuit only. If that circuit fails, the nightly transfer must still complete within 24 hours, and analysis for that day may be skipped; the 3 Gbps abort rule applies only to normal nightly runs. The pilot may move a 1 TB subset at whatever rate it reaches."
Replace constraint 7 (the "Finance funds one physical circuit only" item) with: "Finance funds one physical circuit only, so resilience cannot come from a second circuit; the transfer takes up to 24 hours while that circuit is down". Replace r6 with: "Steady-state nightly path sustains more than 4 Gbps, and the design shows why the 1.5 Gbps internet dips do not occur on it". Replace r7 with: "Pilot within five days, encryption in transit on every path, and a working path while the circuit is down (transfer within 24 hours) are each met and each states the rate that path can sustain". Result: a 10 Gbps dedicated or 5 Gbps hosted port both remain valid, and the backup answer is now determinate (a single VPN at about 1 Gbps meets 10 TB in 24 h; 0.93 Gbps needed).

**AWS-DE1-002 (major) de-saa-1.2-s03, scenario sentence 2.** "a flood of traffic exhausted the site" does not say which layer, and 60,000 requests per second is also the legitimate on-sale peak. A WAF rate-based rule and a WAF SQL-injection rule are then both defensible, which collides with constraint 6 and r6 ("distinct control", "no control covers two"). Replace with: "A penetration test found SQL fragments accepted in query strings, and last month a volumetric network-layer flood (SYN and UDP reflection packets, not HTTP requests) exhausted the site during an on-sale." Constraints and r6/r7 stand.

**AWS-DE1-003 (major) de-saa-2.1-s02, cost cap not checkable, schedule vs predictive not separated.** No price is given, so "2,500 USD cap" cannot be checked, and a schedule that starts scaling one hour before the earliest peak plus a target-tracking policy is a second defensible design (the lesson says "known recurring peak" is scheduled or predictive). Replace constraint 6 ("Monthly compute spend is capped at 2,500 USD") with: "Peak-sized capacity may be paid for at most 90 minutes per weekday in total, including warm-up time". Add to the scenario after the first sentence: "The peak lasts about 60 minutes." Replace r6 with: "Capacity is ready for each peak start (10-minute warm-up) without a hand-maintained calendar and without holding peak-sized capacity for more than 90 minutes per weekday". With a 60-minute peak, an hour-wide safety padding plus warm-up exceeds 90 minutes, so a padded schedule fails; a forecast-driven approach holds capacity only around the forecast start. (Writer: confirm the lesson supports "forecast per hour"; if not, add to the "Lesson additions requested" list.)

**AWS-DE1-004 (major) de-saa-2.1-s03, two defensible designs and r7 giveaway.** SNS topic with one SQS queue per consumer and an EventBridge bus with three SQS targets both meet every figure. Constraint 7, "No content-based routing is needed", names EventBridge's feature and steers away from it, and r7 ("own durable buffer") tells the learner to use a queue per consumer. Replace constraint 7 with: "Each team takes every order whole; nothing is filtered by content." Replace r7 with: "Any of the 3 consumers can be down for a day and afterwards still receives every order it missed, with no action by checkout or by the other two consumers." Add a rubric-neutral instruction to the artifact only: none. Accept either fan-out mechanism if the record justifies it against the stated figures; Lead Dev to record in the plan that both are valid and that the intended lesson-2.1 discriminator (SNS "one publisher, many subscribers" vs EventBridge "event patterns") is carried by the "every consumer takes every order" fact already in the scenario. If the user wants exactly one answer, make the constraint "three teams, each of which already polls a queue endpoint" hmm not recommended; prefer accept-either.

**AWS-DE1-005 (major) de-saa-2.1-s04, r6 asserts a false premise.** "including where containers are not the fit" presumes the nightly script is not a container fit; a scheduled Fargate task is equally valid and costs nothing idle. Replace r6 with: "Each of the nine applications and the nightly script is given a compute choice with a reason drawn from the scenario's figures (runtime pinning, unchanged vendor builds, 23 idle hours a day)". r7 mostly restates constraints 1 and 2; keep it but shorten to "No Kubernetes and no host operating system patching remain in the design".

**AWS-DE1-006 (major) de-multi-region-dr, scenario sentence 3 and constraint 1 contradict pilot light.** "only stored data" reads as backup and restore, yet RPO 5 minutes needs a continuously replicating (running) database. Backup and restore vs pilot light is then not determinate. Replace sentence 3 with: "The finance director will not fund any continuously running application servers in the recovery Region; a continuously running replicated database there is acceptable." Replace constraint 1 with: "Finance funds no continuously running application servers in the recovery Region (a replicated database is allowed)". r6/r7 stand.

**AWS-DE1-007 (major) de-saa-2.2-s04, constraint 2 and r7.** (a) "the application must run unchanged on duplicated components" cannot hold for the label job server (a second copy would render labels twice). (b) The doubling cap cannot be checked without prices, and adding a load balancer takes any "two of everything" design above 2x. (c) "roughly 8.7 hours" should be 8.76 h, about 8.8 hours (525 minutes). Replace constraint 2 with: "No application rewrite is planned; the design may duplicate or replace infrastructure around the application but not change its code". Replace r7 with: "The design keeps at most two copies of any current component (one per Availability Zone) and names every added component (such as a load balancer) with why the run-rate is still expected to stay within double". In the scenario replace "roughly 8.7 hours a year" with "roughly 8.8 hours (525 minutes) a year". Lesson 2.2 S03 has the same 8.7; note for Lead Dev.

**AWS-DE1-008 (minor) de-multi-account, scenario / r6.** SCPs do not apply to the management account. If the 45 accounts include it, "including root users" cannot be met by SCPs. Replace the scenario's "runs 45 AWS accounts" with "runs 45 member accounts (plus a separate management account)" and r6 with "Region restriction and audit record cover all 45 member accounts, their root users, and accounts added later without per-account work".

**AWS-DE1-009 (minor) de-federation.** Constraints 5-8 name SAML/AD FS, IAM Identity Center, AD Connector and AWS Managed Microsoft AD. This is acceptable for a compare exercise: they define the comparison and the scenario carries the decisive facts (no passwords in AWS, no domain controllers in AWS, 12 accounts, two engineers). No change beyond this: keep r6/r7. One accuracy note for Teacher: an external IdP (AD FS) plugged into Identity Center is a fourth defensible multi-account design; r7 only requires the three named options compared, so leave it and let the record mention it.

**AWS-DE1-010 (minor) de-saa-1.3-s01, r6 wording.** Scenario has three auditor asks plus one insurer ask. Replace r6 with: "Each of the four asks (provider evidence, continuous proof, seven-year retention, consistent labels) is mapped to a distinct control".

**AWS-DE1-011 (minor) de-saa-1.3-s03, scenario / r6.** "a content delivery network" does not say it is CloudFront, and r6 assumes a Region rule for the CDN certificate. Replace "delivered by a content delivery network" with "delivered by Amazon CloudFront". Replace r6 with: "Each endpoint's certificate is one that its own service can use, and the design states the Region each certificate must be requested in".

**AWS-DE1-012 (minor) de-saa-1.3-s07, r6 gives a mild hint.** Replace r6 with: "Each of the 6 signing keys has a stated annual replacement path that meets the no-application-change rule, and the record says why the symmetric keys' approach does not apply to them". Also add to the scenario: "The 4 imported certificates must stay issued by the partner's authority only if the partner requires it; otherwise the team is free to replace them" to avoid a hidden requirement is optional; no change required.

**AWS-DE1-013 (minor) de-saa-2.1-s06, scenario sentence 2.** Operating system not stated, so FSx for Windows File Server vs EFS is open. Replace "must read and write the same template directory at the same time as an ordinary mounted folder" with "(all Linux) must read and write the same template directory at the same time as an ordinary mounted folder".

**AWS-DE1-014 (minor) de-saa-2.1-s07, broker.** Broker protocol is not given, so SQS and Amazon MQ are both defensible. Replace "a self-hosted message broker between the intake and indexing programs" with "a self-hosted message broker used only for plain send-and-receive messages between the intake and indexing programs, both of which the team can re-point".

**AWS-DE1-015 (minor) de-saa-2.2-s02, r6 restates constraint 1 as the answer.** Replace r6 with: "A change saved at either site during normal operation succeeds without waiting for a failover and becomes readable at the other site". Also add to constraint 2 nothing. Data tier sentence "key-value, no joins" already decides DynamoDB global tables over Aurora.

**AWS-DE1-016 (minor) de-saa-2.2-s07, engine unstated.** RDS Proxy supports specific engines only. Replace "an RDS database" with "an RDS for MySQL database". Also r7 ends "by changing only the hostname", which restates constraint 2; acceptable.

Checked and no finding: de-cloudhsm (CloudHSM vs KMS decided by the PKCS #11 library and single-tenant FIPS 140 Level 3; r6 wording is outcome-based), de-saa-1.3-s05 (RTC, Batch Replication, AWS Backup all determinate; "every" upload vs 99.99 percent SLA is a nit), de-saa-2.2-s01, de-saa-2.2-s08 (mild overlap with 2.2-s02 as the writer notes). constraint_reason holds for all 20; no retired/closed service appears (Snow Family is in batch 2).

Batch 1: not yet

Overall: concerns

---

## Teacher review (b422d65)

Saved by Lead Dev from the Teacher's reply (condensed; replacement texts verbatim).

**Method:** a case-insensitive, backtick-stripped regex over the lessons for each exercise's objectives.
- **MACsec is not taught** (only in 3.4/4.4 reviewer text) and must never be required.
- **Every solution service is taught**, and every scenario is in operational language.

**Verdicts**
- **Changes required:** de-direct-connect, de-saa-1.2-s03, de-saa-2.1-s02, de-saa-2.1-s03, de-saa-2.1-s04, de-multi-region-dr, de-saa-2.2-s04.
- **Approve:** de-federation, de-cloudhsm, de-saa-2.2-s01, de-saa-2.2-s08. De-saa-2.2-s08 overlaps 2.2-s02 in using global tables, but the intent differs.
- **Approve with minor fixes:** de-multi-account (AWS-008), de-saa-1.3-s01 (AWS-010), de-saa-1.3-s03 (AWS-011), de-saa-1.3-s05 (T-004), de-saa-1.3-s07 (AWS-012 r6, T-003), de-saa-2.1-s06 (AWS-013, T-007), de-saa-2.1-s07 (AWS-014), de-saa-2.2-s02 (AWS-015), de-saa-2.2-s07 (AWS-016).

**Findings**
- **TEACHER-DE1-001 (major) de-saa-2.1-s02.** A peak that "shifts by up to an hour from week to week" leaves predictive scaling nothing to learn. Lesson 2.1 teaches it for a "recurring pattern" from "historical load".
  - Replace sentence 2 with: "The peak start differs by up to an hour between school terms but stays the same within a term, and the term dates are not tracked by anyone at Pinecrest."
  - Word r6 as "ahead of a forecasted recurring pattern", not "per hour".
- **TEACHER-DE1-002 (minor) de-direct-connect, amending AWS-DE1-001.** Change "within 24 hours" to "within 36 hours (a one-night backlog is acceptable)" in the scenario, constraint 7 and r7. That is about 0.62 Gbps, against a standard tunnel's 1.25 Gbps.
  - Do not add MACsec anywhere.
  - Accept application-layer TLS, VPN over DX, or several tunnels.
- **TEACHER-DE1-003 (minor) de-saa-1.3-s07.** Replace "it also runs 30 public TLS certificates, 4 of which were imported from a banking partner's authority" with "it also runs 30 public TLS certificates on its load balancers, 26 issued through AWS Certificate Manager with DNS validation and 4 imported from a banking partner's authority".
  - Ignore the optional tail of AWS-DE1-012.
- **TEACHER-DE1-004 (minor) de-saa-1.3-s05.** In the scenario use "at least 99.99 percent of new uploads available in a second Region within 15 minutes". Set r6 to "The 15-minute ceiling for 99.99 percent of new uploads is met and the existing 14 TB is also covered".
- **TEACHER-DE1-005 (minor) de-saa-2.2-s04.** In the scenario use "which is more than half of the roughly 525 minutes (about 8.8 hours) a year that a 99.9 percent target allows". Also apply AWS-DE1-007's constraint 2 and r7.
- **TEACHER-DE1-007 (minor) de-saa-2.1-s06.** Set r7 to "Repeat reads of the same 500 price-list rows do not each reach the database, and the record states how stale the data may be".

**Second-role check on AWS-DE1-001 … 016:** agree with every finding.
- **001:** apply with the TEACHER-DE1-002 amendment.
- **004:** accept either fan-out mechanism. Drop the "hmm" paragraph, and do not force SNS.
- **012:** apply the r6 rewrite only.
- **The rest:** accurate replacements that keep the exercises fair.

**Lesson 2.2** "8.7 hours" (and "52 minutes" for 99.99%): agree it should be logged as a separate low-severity CR, needing its own plan.

Batch 1: not yet · Overall: concerns

---

## Technical confirmation (fix pass)

Checked at 353fe54 (`git diff b422d65 HEAD -- content`: 16 files, 31 lines changed, exercises only) against the writer's "## Fix pass" table and the live JSON of de-saa-2.1-s02, de-direct-connect and de-saa-1.3-s07.

### 1. AWS-DE1-001 to 016

| Id | Status |
| --- | --- |
| 001 | Gone. Backup rate is now determinate: 10 TB in 36 h is about 0.62 Gbps, within one 1.25 Gbps tunnel. The 3 Gbps abort rule is scoped to normal nights, the pilot moves a 1 TB subset, and encryption is required "on every path" without naming a mechanism (MACsec not mentioned). |
| 002 | Gone (see item 3 on the untaught words). |
| 003 | Gone, but r6 wording needs the change in item 4. |
| 004 | Gone. Either fan-out design is accepted; r7 is outcome-based. |
| 005 | Gone. |
| 006 | Gone. A replicated database is allowed, so pilot light is determinate and warm standby is excluded by the no-app-servers rule. |
| 007 | Gone. 525 minutes is 8.76 h and 300 min is more than half. |
| 008 | Gone. |
| 009 | Not applicable (no change, by decision). |
| 010, 011, 012, 013, 014, 015 | Gone. |
| 016 | Gone (see item 3). |

### 2. Second-role check on the Teacher's findings

- TEACHER-DE1-001: agree. Peak start fixed within a term, changing between terms, plus the constraint against hand-editing timetables when calendars change, excludes a fixed schedule and leaves a learned pattern. Text is accurate.
- TEACHER-DE1-002: agree (36 h, no MACsec).
- TEACHER-DE1-003: agree. Naming ACM/DNS validation for the 26 describes existing state and does not reveal how to handle the 4 imported certificates or the 6 signing keys.
- TEACHER-DE1-004: agree. RTC is a 99.99 percent commitment, so the wording is now accurate.
- TEACHER-DE1-005: agree.
- TEACHER-DE1-007: agree. It is checkable against the scenario's "up to one hour out of date".

### 3. Changed-text checks

All 33 changes are accurate and determinate, and none names its solution service. Two context-word notes, both non-blocking:
- "MySQL" (016): an engine name used only as scenario context. RDS Proxy supports MySQL, so the design is valid. Keep.
- "SYN and UDP reflection" (002): context that fixes the layer (network, not HTTP) without naming Shield or WAF. Acceptable; a simpler equivalent that avoids both untaught terms, if preferred: "a volumetric network-layer flood of packets (not HTTP requests)".
- Minor residual: the 2.1-s04 r6 and 1.3-s03 r6 still hint at a trap ("reason drawn from the figures", "the Region each certificate must be requested in") but describe outcomes only. Keep.

### 4. de-saa-2.1-s02 r6: "forecasted recurring pattern"

Answer: **yes**, an outcome wording keeps the exercise determinate. "Forecasted recurring pattern" all but names predictive scaling and should go. The deciding facts stay in the scenario: the peak start is fixed within a term but shifts between terms, engineers may not hand-edit timetables (this rules out a fixed schedule), the 60-minute peak plus 10-minute warm-up fits the 90-minute budget only if capacity is added shortly before each peak (this rules out padded schedules and always-on), and 30 percent surges need target tracking (r7). Replace r6 with exactly:

"Capacity is ready before each peak starts (allowing the 10-minute warm-up), with no hand-maintained calendar, and peak-sized capacity is held for no more than 90 minutes per weekday."

Batch 1: not yet (one text change outstanding: 2.1-s02 r6; then close)

Overall: concerns

---

## Teacher confirmation (310a291)

Saved by the Lead Dev from the Teacher's reply (condensed).

1. **The Teacher's findings:** TEACHER-DE1-001, 002, 003, 004, 005 and 007 are Gone.
2. **Second-role check:** AWS-DE1-001–008 and 010–016 are Gone. 009 has no change, by decision.
   - 002: "SYN and UDP reflection" is accepted as context wording.
   - 016: "MySQL" is kept as engine context.
   - 004: either fan-out design is accepted.
3. **Teach-before-test and fairness:** every changed text is accurate, and no solution service is named in any scenario, constraint or rubric item. Each exercise is determinate, and the rubrics grade outcomes.
4. **de-saa-2.1-s02 r6:** the outcome wording is accepted and the Teacher's "forecasted" wording is withdrawn. The exercise stays determinate:
   - a fixed schedule either needs hand-edited timetables or breaks the 90-minute cap;
   - target tracking alone reacts after the 10-minute warm-up;
   - what remains is capacity added ahead of a learned start, plus target tracking for the surges (both taught in 2.1 S02).

Batch 1: close · Overall: approve
