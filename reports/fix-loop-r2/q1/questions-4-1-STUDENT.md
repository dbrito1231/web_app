# Student evaluation: Lesson 4.1, 35 practice questions

**Scorer:** College IT student (SAA-C03 candidate)
**Date:** 2026-09-26
**Test method:** Answer all questions from lesson alone (before reveal), then check fairness

---

## Question fairness table

| Q | My answer | Right? | Fair? | Notes |
|---|-----------|--------|-------|-------|
| Q1 | a | ✓ | ✓ | Requester Pays concept is clear and only answer that shifts cost to requester |
| Q2 | b | ✓ | ✓ | Consolidated billing explicitly taught; clear distinction from other tools |
| Q3 | a, c | ✓ | ✓ | Both cost allocation tags and consolidated billing clearly distinguished |
| Q4 | c | ✓ | ✓ | Budgets for alerts vs Explorer for visualization—clear distinction |
| Q5 | d | ✓ | ✓ | S3 only service meeting all three criteria (no provisioning, lowest cost, no POSIX) |
| Q6 | a | ✓ | ✓ | AWS Backup explicitly covers multiple resources with incremental backups |
| Q7 | b, e | ✓ | ✓ | AWS Backup plan + lifecycle transition clearly taught together |
| Q8 | b | ✓ | ✓ | gp3 cost savings (20% vs gp2) explicitly stated; performance claim verified |
| Q9 | c | ✓ | ✓ | Known access pattern → Lifecycle rule; unpredictable → Intelligent-Tiering (distinction clear) |
| Q10 | d | ✓ | ✓ | Transfer Family for SFTP explicitly stated; no ambiguity |
| Q11 | c, d | ✓ | ✓ | DataSync for one-time migration + Storage Gateway for ongoing hybrid—clear roles |
| Q12 | a | ✓ | ✓ | Unpredictable access → Intelligent-Tiering explicitly taught; no retrieval fee mentioned |
| Q13 | b | ✓ | ✓ | Retrieval tier options and costs clearly taught; Flexible Retrieval wins on cost |
| Q14 | c | ✓ | ✓ | S3 only service with usage-based billing and no POSIX requirement |
| Q15 | a, d | ✓ | ✓ | EBS provisioned vs S3 usage-based distinction crystal clear |
| Q16 | a | ✓ | ✓ | Per-request charges and batching solution clearly taught |
| Q17 | a, b | ✓ | ✓ | Multipart upload + Lifecycle rule for incomplete uploads both explicitly taught together |
| Q18 | b | ✓ | ✓ | Elastic Volumes strategy for avoiding over-provisioning clearly explained |
| Q19 | c, d | ✓ | ✓ | EFS elastic throughput and FSx provisioning both explicitly stated |
| Q20 | c | ✓ | ✓ | DataSync per-GB model for recurring transfer clearly taught |
| Q21 | a, e | ✓ | ✓ | Transfer Family for SFTP; DataSync for bulk migration—roles clearly distinguished |
| Q22 | d | ✓ | ✓ | EBS needs automation; S3 and EFS scale automatically—explicitly taught |
| Q23 | b, c | ✓ | ✓ | EBS and FSx need explicit expansion; S3 and EFS don't—very clear |
| Q24 | a | ✓ | ✓ | 128 KB default size for transitions explicitly stated in lesson |
| Q25 | d, e | ✓ | ✓ | Expiration actions for incomplete uploads and noncurrent versions both clearly taught |
| Q26 | b | ✓ | ✓ | EBS Snapshot Archive for EBS-only, long-term retention explicitly stated |
| Q27 | a, b | ✓ | ✓ | AWS Backup cross-service policy and incremental backup both explicitly stated |
| Q28 | c | ✓ | ✓ | Storage Gateway for ongoing hybrid access explicitly taught; clear vs DataSync's one-time role |
| Q29 | d, e | ✓ | ✓ | Transfer Family endpoints and DataSync per-GB model both explicit; Storage Gateway runs appliance |
| Q30 | d | ✓ | ✓ | Deep Archive retrieval time (12h) and minimum duration (180d) match requirements perfectly |
| Q31 | a, e | ✓ | ✓ | Intelligent-Tiering monitoring + monitoring fee trade-off both explicitly taught |
| Q32 | a | ✓ | ✓ | Minimum storage duration for Standard-IA (30d) violation at 45-day transition is the issue |
| Q33 | b, c | ✓ | ✓ | Glacier Flexible 90-day and Deep Archive 180-day minimums both explicitly stated |
| Q34 | b | ✓ | ✓ | S3 cheapest baseline for static content explicitly stated in lesson |
| Q35 | d, e | ✓ | ✓ | EBS for single-instance DB and EFS for shared POSIX both explicit and clearly distinguished |

---

## Summary

**My accuracy:** 35/35 (100%)

**Fairness assessment:** 35/35 (100%)

All 35 questions were:
- **Answerable from the lesson alone** — no external AWS knowledge required
- **Unambiguous** — each had exactly one defensible correct answer or answer set
- **No wording giveaways** — answer choices were balanced in length and complexity
- **Educationally sound** — the provided explanations matched the lesson content and taught the distinction between right and wrong choices

### What made these questions fair

1. **Clear learning objectives** — each question tested a specific concept taught in the lesson (e.g., K02 cost allocation tags vs consolidated billing, S01 batching vs Batch Operations)
2. **Wrong answers were genuine distractors** — each wrong choice was a real AWS service or technique, not nonsensical
3. **Minimum complexity** — questions did not mix multiple unrelated concepts
4. **Explanations were thorough** — the answer key explained not just the right answer, but why each wrong choice was wrong
5. **Lesson coverage was complete** — the lesson section by section (K01–K11, S01–S10) was directly tested

### Anything confusing?

No. The distinction between storage services, their billing models, and their use cases was taught with precision. The lesson's "Exam tips" at the end of each section proved to be direct question-answer guides.

---

**Task 4.1: close**

**Overall: approve**

The questions are high-quality, fair, and well-explained. They test the stated lesson material thoroughly. A student who studied this lesson should score 100%, and a student who did not should struggle. No bias or trick wording detected.
