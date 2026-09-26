# Teacher review: lesson 4.1 (round 1)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**1. Claim table (8 rows spot-checked):** Rows 1, 5, 8, 10, 12, 13, 16, 20 all match the lesson prose verbatim in substance. No discrepancies in these 8. Row 11 does not match (see TEACHER-L41-003 below) — claim table cites a fact never written into the lesson body.

**2. Coverage:** All 21 `SAA-4.1-*` objectives (K01–K11, S01–S10) have their own `###` section in id order, each ending in `**Exam tip:**`. Confirmed by section/tip counts (22 sections incl. Warnings, 21 tips). Coverage: complete.

**3. Teaching quality:**
- Storage class by access pattern/retrieval need: taught well (K09, K10, S08).
- Intelligent-Tiering vs Lifecycle rule: contrast present but soft — K09 says "tiered manually" instead of naming the mechanism. See TEACHER-L41-001.
- Glacier Instant vs Flexible vs Deep Archive: class names, minimum durations and cost ordering are taught correctly, but the lesson never teaches the actual retrieval-speed tiers that distinguish Flexible Retrieval and Deep Archive. See TEACHER-L41-002 (this is the classic way this contrast is tested).
- Cost Explorer vs Budgets vs CUR/Data Exports vs Storage Lens: clearly contrasted (K03, K10).
- gp2 vs gp3 cost: correct and consistent with lesson 3.1's performance treatment.
- Snapshot archive, EFS lifecycle, data transfer directions: taught, except EFS lifecycle day thresholds — see TEACHER-L41-003.
- Exam tips: all 21 read as correct, no giveaway wording, no contradictions found.
- No contradiction of lessons 2.2, 3.1, 3.5 — checked all three directly (gp2/gp3, Snow Family/Data Transfer Terminal, DataSync/Storage Gateway naming all line up).
- Filler: none found worth cutting; prose is dense and objective-focused throughout.

**4. Length:** 3,336 words confirmed exactly (script-verified) for 21 objectives (~159 words/objective). Acceptable — no filler identified to cut; the ~4% overage the writer flagged is justified by objective count, not padding.

**5. Format (`q1_batch_check.py 4-1`, lesson lines only):**
```
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
WARN: lesson names retired/closed service 'Snowball': ...never the retired Snowball Edge.
```
The WARN is expected/correct — Snowball is explicitly labeled retired, per RULES.md.

**6. Teach-before-test gaps:**
- Glacier Flexible Retrieval (Expedited/Standard/Bulk) and Deep Archive (Standard/Bulk) retrieval-time tiers are not taught anywhere — a question testing retrieval-time differences among the Glacier classes cannot be sourced to this lesson yet.
- EFS Lifecycle Management's specific transition-day thresholds (30 days to IA, 90 days to Archive) are not in the lesson body despite being in the claim table — a question testing those specific numbers has no teaching to point to.
- S3 Intelligent-Tiering's own internal archive access tiers are not taught (not required by the prompt's contrast list, flagging only so no question assumes it).

**Issues:**
- **TEACHER-L41-001** (low, K09): "tiered manually" is vague for the required Intelligent-Tiering-vs-Lifecycle contrast. Fix: change to "...can be tiered with a scheduled S3 Lifecycle rule to save the monitoring fee that Intelligent-Tiering charges."
- **TEACHER-L41-002** (moderate, K10): Add one sentence stating Glacier Flexible Retrieval's three retrieval tiers (Expedited ~1–5 min, Standard ~3–5 hrs, Bulk ~5–12 hrs) and Deep Archive's two (Standard ~12 hrs, Bulk ~48 hrs), doc-verified against `glacier-storage-classes.html`.
- **TEACHER-L41-003** (moderate, K07/K10): Claim table row 11's EFS Lifecycle Management day thresholds (30-day IA, 90-day Archive) never made it into the lesson text. Either add the two numbers to K07 or K10, or instruct the question writer not to test EFS-specific day thresholds for this task.

Lesson 4.1: not yet.

Overall: concerns.
