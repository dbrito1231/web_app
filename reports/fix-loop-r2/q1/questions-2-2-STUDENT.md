# Task 2.2 fairness check — College IT Student review

Reviewer: College IT Student persona (basic IT background, not an AWS expert), studying from this workbook.
Method: read lesson 2.2 in full at `/start?lesson=lesson-2-2`, then answered each drill below at `/exam?q=<id>` by reading only — no question JSON files were opened. For each question my answer and one-line reason were decided and written down before clicking "Check answers" (clicked once per question).

## Per-question results

| ID | My answer (recorded before submitting) | My one-line reason | Result | Fair? | Why |
| --- | --- | --- | --- | --- | --- |
| q-saa-2-2-k01-mc | "Configure a Route 53 latency-based routing policy" | Lesson ties "lowest latency, no manual %" directly to latency-based routing, distinct from weighted (manual %) and geolocation (by place, not speed). | Correct (100%) | Y | Answerable straight from lesson K01. All 4 choices are same length/structure ("Configure a Route 53 X routing policy") — no wording giveaway. Weighted/geolocation/failover are plausible, not silly. Explanation matched the choices shown and taught the distinction between the four policies clearly. |
| q-saa-2-2-k04-mc | "Pilot light, keeping data stores running while compute is created from configuration only when needed" | RPO ~10 min / RTO ~30 min matches pilot light's band (RPO minutes, RTO tens of minutes) and it's cheaper than warm standby, which also fits. | Correct (100%) | Y | Numbers map cleanly onto K04's four-strategy table. Distractors (backup/restore too slow, active/active too costly, warm standby also fits but costs more) are all reasonable — the "cheapest that still meets both numbers" framing is exactly what the lesson's exam tip trains for. No giveaway wording. |
| q-saa-2-2-k06-mc | "A Multi-AZ DB cluster deployment" | "Automatic failover + two additional readable standbys, one Region" is the lesson's exact description of a Multi-AZ DB cluster vs. a Multi-AZ DB instance (non-readable standby) or a read replica (not automatic failover). | Correct (100%) | Y | Tests a genuinely confusable pair (DB instance vs. DB cluster) the lesson calls out by name. Distractors are not silly — a read replica and an Aurora Global Database are realistic wrong picks for someone who skims. Explanation cleanly re-taught the distinction. |
| q-saa-2-2-k09-mr | "Holds client-side connections open during failover..." + "Pools the many short-lived connections..." | These are literally the two K09 benefits called out in the lesson for RDS Proxy. | Correct (100%) | Y | The 3 wrong choices (cross-Region replication, replacing Multi-AZ, adding read standbys) are things RDS Proxy explicitly does NOT do per the lesson, so they're fair distractors, not silly ones. No length/wording giveaway — all options are one sentence each. |
| q-saa-2-2-k12-mr | "Configure a CloudWatch alarm...to trigger Auto Scaling" + "Enable AWS X-Ray tracing..." | Two separate asks in the stem (alarm-driven scaling, and tracing one slow request) map 1:1 to CloudWatch alarms and X-Ray per K12. | Correct (100%) | Y | Good design — the 3 distractors (dashboard widget, Logs Insights, Route 53 health check) are all real AWS features that sound plausible but each fails one part of the ask. This is the strongest question of the ten for testing real understanding rather than memorization. |
| q-saa-2-2-s02-mc | "Amazon DynamoDB global tables" | Stem needs both-Regions-writable within seconds + automatic conflict resolution — that is global tables' definition; Aurora Global secondary is read-only until promoted. | Correct (100%) | Y | Fair and unambiguous once you know Aurora Global Database's secondary is read-only (taught in K06/S02). RDS Multi-AZ and S3 CRR are clearly off-topic (wrong scope), not silly, just wrong scope — reasonable distractors for someone who half-remembers the service names. |
| q-saa-2-2-s03-mr | "Recovery point objective (RPO)" + "Recovery time objective (RTO)" | Stem literally defines "max acceptable downtime" (RTO) and "max acceptable data loss" (RPO) as the two numbers. | Correct (100%) | Y | Distractors (availability %, durability %, service quota) are real metrics from the same lesson but are conceptually different (aggregate/yearly vs. per-incident), so this tests real discrimination, not a trick. No wording giveaway. |
| q-saa-2-2-s05-mr | "A mandatory grace period of at least 72 hours..." + "Lock the vault in compliance mode" | Lesson S05 states compliance mode + a minimum 72-hour cooling-off period together make retention truly immutable, including against root; governance mode is removable by permitted users. | Correct (100%) | Y | Nice, since 24h vs 72h is a specific number check straight from the lesson, and governance-vs-compliance mode is the key distinction the lesson explicitly warns about. Not a giveaway — both "72 hours" and "24 hours" read equally plausible without having read the lesson. |
| q-saa-2-2-s07-mc | "An Application Load Balancer or Network Load Balancer... health checks removing unhealthy targets" | Stem explicitly says "without depending on DNS changes reaching clients," which rules out Route 53 failover and points to a load balancer, matching lesson S07. | Correct (100%) | Y | The "without depending on DNS" phrase is a fair, lesson-taught discriminator (Route 53 failover works via DNS answer changes, which do depend on TTL/propagation) rather than a giveaway — you need to know that fact, not just spot longer wording. AWS DRS and RDS Proxy are legitimate S07 tools for other jobs, so they're reasonable distractors, not silly ones. |
| q-saa-2-2-s08-mr | "Amazon DynamoDB global tables..." + "AWS Backup, with a policy-based backup plan..." | Two homegrown tools in the stem (cron snapshot job, hand-rolled cross-Region DynamoDB replication) map 1:1 onto AWS Backup and DynamoDB global tables per S08's "purpose-built service instead of homegrown tooling" framing. | Correct (100%) | Y | Good design: Vault Lock, Aurora Global Database, and AWS DRS are all real services from the same lesson but each is wrong for a specific, checkable reason (Vault Lock only locks retention, doesn't schedule backups; Aurora Global doesn't apply to a DynamoDB table; DRS replicates servers not table rows). No silly distractors. |

## Fairness percentage

10 / 10 fair = **100%** (target ≥90% — met).

## Score

10 / 10 correct on first attempt (all marked "Correct", 100% each; "Resilient architectures" progress went from 0/67 to 10/67 over the session).

## Anything confusing

- Nothing in the lesson content was confusing. The lesson text itself is dense (12 knowledge items + 8 skill items) but each drill only needed the one paragraph/exam-tip tied to its objective, and the explanations after each answer consistently pointed back to the right paragraph.
- Minor UI/workflow note (not a content issue): the exam page renders all 429 drills as one long virtualized list, and the `?q=` URL parameter scrolls to and expands the target question rather than showing it alone. This made reading each question take a couple of extra tool calls but did not affect the fairness of the content itself, so I'm not filing this as a content change request — it's an app-behavior observation for Lead Dev/Teacher awareness only if useful.
- No wrong-answer wording giveaways were found (no option was conspicuously longer, no option explained itself, no choice was obviously a joke/filler).

## Verdict

**Task 2.2: close**

**Overall: approve**
