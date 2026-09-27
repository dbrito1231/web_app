# Student fairness review — task 4.2 (A4 Cost-optimized compute)

Run from the text packet on `composer-2.5-fast` (Haiku 4.5 unavailable; see plan §10).
All 24 answers were committed in writing before the answer file was opened.
Saved by Lead Dev from the Student's reply.

## Step 2 — committed answers (before key)

| ID | My answer | One-line reason |
|----|-----------|-----------------|
| Q1 | a | Lesson: activate tags for chargeback; turn off RI/SP sharing for per-account isolation. |
| Q2 | c | Lesson exam tip: visualize/forecast by dimensions -> Cost Explorer. |
| Q3 | b, d | Budgets for threshold alarms; CUR to S3 for Athena raw rows. |
| Q4 | b | Production AZ failure -> at least two AZs behind a load balancer. |
| Q5 | d | Baseline -> commitments; interruptible rendering -> Spot. |
| Q6 | a | 5G + carrier edge latency -> Wavelength Zones. |
| Q7 | a, e | Matchmaking at Local Zone; system-of-record tier stays in Region. |
| Q8 | c | On-premises + native AWS APIs -> Outposts. |
| Q9 | b | Direct physical host -> `metal` size in instance name. |
| Q10 | d | Short event bursts, idle overnight -> Lambda. |
| Q11 | c, d | Fargate drops host patching; independent microservice scaling cuts idle capacity. |
| Q12 | a | Hibernate preserves RAM for 14-min warm index; Auto Scaling for elastic daytime load. |
| Q13 | c | HTTP path routing + TLS -> ALB (Layer 7). |
| Q14 | b, e | Inline scalable appliances -> GWLB + appliance target groups. |
| Q15 | b | Stateless, hourly swings -> horizontal target-tracking Auto Scaling. |
| Q16 | a, c | Flash crowds -> horizontal scale-out; cache cold start -> hibernate pre-warmed instances. |
| Q17 | d | S3 event short work -> Lambda; all-day containers -> Fargate. |
| Q18 | a, d | Short handlers -> Lambda; >15 min containers without host mgmt -> Fargate. |
| Q19 | a | Tier-1 checkout multi-AZ; tier-3 QA leaner scheduled capacity. |
| Q20 | a, b | High-impact checkout multi-AZ; dev sandbox smaller/scheduled single-AZ OK. |
| Q21 | c | High CPU, moderate memory -> compute-optimized (C) family. |
| Q22 | c, e | CPU-bound -> C; memory-bound -> R. |
| Q23 | b | Already on `large`; next safe step up for exceeded peaks -> `xlarge`. |
| Q24 | b, d | Step down one size where headroom; keep Auto Scaling for peak scale-out. |

## Step 3 — score

All 24 answers matched the published key.

**Score: 24/24 (100%)**

## Step 4 — wrong answers

None. No category (i)-(iv) categorizations apply.

## Step 5 — additional observations

### Guessable from wording (without deep knowledge)

Several stems mirror lesson vocabulary so closely that elimination is easy even with shallow recall:

- **Q6:** "5G phones" and "carrier networks" map almost verbatim to Wavelength; Region/Local Zone/Outposts distractors are clearly off-pattern.
- **Q8:** "on premises" + "same AWS APIs" is the Outposts exam tip almost word-for-word; Local Zone and Wavelength are AWS-managed edge, not the factory floor.
- **Q13:** "HTTP," "URL path," and "TLS termination" scream ALB; NLB/GWLB/Classic are wrong layer or generation.
- **Q4, Q19, Q20:** Single-AZ and "mirror production in QA" options are extreme anti-patterns the lesson warns against, so the multi-AZ / tiered-resilience choice stands out.
- **Q9:** "direct physical host access" aligns with the lesson's `metal` explanation; other choices are ordinary virtual sizes/families.

That is acceptable for formative drills but reduces discrimination among students who only skimmed headings.

### Overlapping coverage (same fact tested twice)

| Fact | Questions |
|------|-----------|
| Production resilience -> multi-AZ (+/- load balancer) | Q4, Q19, Q20 (part a) |
| Horizontal Auto Scaling for elastic/stateless traffic | Q15, Q16 (part a) |
| Lambda for short, bursty, event-driven work | Q10, Q17, Q18 (part a) |
| Fargate for containers without host management / longer run | Q11, Q17, Q18 (part d) |
| C vs R family by bottleneck | Q21, Q22 (part c/e) |
| Edge placement: Wavelength vs Local Zone vs Outposts | Q6, Q7, Q8 |

Overlap is thematic (expected for one lesson) but Q4/Q19/Q20 and Q10/Q17/Q18 feel redundant for a single 24-question sitting.

### Confusing or easy-to-misread stems

- **Q23:** "Smallest size that safely handles 95th percentile CPU peaks **above current large capacity**" requires assuming the fleet is already on `c7g.large` and needs the next step (`xlarge`). A quick read might wonder whether "large" is naming the size tier or describing capacity generically; the keyed reading (current size = `large` -> bump to `xlarge`) matches K06's doubling ladder once that assumption is clear.
- **Q2 vs Q3:** Both involve cost tooling; Q2 (forecast/visualize) vs Q3 (alarms + CUR export) is fair if the student absorbed K02's Cost Explorer vs Budgets vs CUR contrasts. Q3's inclusion of tag activation (e) as a distractor is fair - the lesson separates tags (attribution) from alarms and CUR.
- **Q14:** Selecting **both** GWLB as insertion point **and** registering appliances in GWLB target groups tests one design pattern twice in one MR item; both are taught under S01, but a student might expect one "architecture" answer and one "operational" answer from unrelated domains.

### Fairness notes (even on items answered correctly)

- **Q1:** Requires combining tag activation (K01) with **disabling** discount sharing - not the default "sharing on" example - which is a good, fair contrast if the stem's "isolated per account" is read carefully.
- **Q11:** "Move each service to Lambda zip functions" is a plausible trap for students who over-generalize "serverless"; the lesson's container/Fargate vs Lambda runtime split supports the key.
- **Q24:** Distractor (e) ("downsize and **lower** Auto Scaling maximum") is a strong teaching moment aligned with S06's "combine right-size with Auto Scaling" message.

Student fairness: pass

---

## Lead Dev note

Pass recorded: 24/24 against a 90% target, with no category (ii), (iii) or (iv)
defects, so nothing blocks closure.

Step 5 raises no defect but one observation is worth carrying forward rather than
discarding. The Student scored 100% and reported that several stems reuse the
lesson's own vocabulary closely enough to be answerable by keyword matching
(Q6, Q8, Q13, Q9) and that three clusters test the same fact more than once
(multi-AZ in Q4/Q19/Q20, Lambda-for-short-work in Q10/Q17/Q18). The earlier tasks
in this rewrite also scored at or near full marks (3.5 at 24/24, 4.1 at 35/35),
so this is a pattern across the method, not a one-off.

Not actioned for 4.2: the questions are accurate, fair and teach-before-test
clean, and RULES does not require a target difficulty. Logged here so that if the
user wants harder drills, the fix is a RULES change applied across tasks
(for example, requiring stems to paraphrase rather than reuse lesson keywords),
not a rework of this one task.
