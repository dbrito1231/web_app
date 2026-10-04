# Plan P5: Regional NAT gateway note (optional)

Author: Lead Developer. Status: **approved by the user 2026-10-04 (recommended option).** Phase 5 of `master_open_items_20261002.plan.md`.

## Problem (facts checked 2026-10-01 and 2026-10-02)

- AWS now offers a **regional NAT gateway**. The AWS docs (nat-gateways-regional.html, read with curl on 2026-10-01) say "A regional NAT gateway automatically expands across Availability Zones based on your workload presence", "Unlike standard NAT gateways (referred to as zonal NAT gateways)".
- Lesson 4.4 S01 and its exam tip teach "one NAT gateway per AZ" as the exam signal, and several 4.4 questions key on it.
- In the final sitting, both reviewers recommended skipping this item to keep the exam signal clear (`reports/final-sitting/TEACHER-plan.md`, `AWS-facts.md`).

## Options (KISS)

1. **Close as won't-do (recommended).** Record in the register that the SAA-C03 exam guide's networking bullets do not require it, and that both reviewers advised against it. Revisit if AWS updates the exam guide. No content change.
2. **One labelled sentence.** Add to 4.4 S01 a single cited sentence: "AWS also offers a regional NAT gateway that spans AZs automatically; this lesson and the exam signal use zonal NAT gateways, one per AZ." Add one new citation. No question changes. Small, but it may blur the taught signal.
3. **Full treatment.** Teach regional versus zonal NAT gateways and add or adjust questions. Most complete, but beyond the exam guide and expensive (a full lesson and question review cycle).

## Recommended approach (option 1)

Record the decision in the register and HANDOFF, with the exact revisit trigger: an SAA-C03 exam guide update, or exam questions that include regional NAT gateways. Also log the S01 sentence ("operates within a designated Availability Zone") as a known zonal simplification, with no content change. If you choose option 2 instead:
1. The technical reviewer re-verifies the quote.
2. The writer adds the one sentence and the citation.
3. The Teacher checks that no 4.4 question becomes ambiguous.
4. Run the full 4-4 check chain.

## Teacher pre-validation (2026-10-02)

**Approve** option 1. (The Teacher could not re-check the AWS quote in its run; the technical reviewer read it with curl on 2026-10-01.)

## Files

Option 1: the register and HANDOFF only. Option 2: `content/lessons/lesson-4-4.json` and a new `content/citations/cite-saa-4-4-*.json`.

## Risks

Option 2 or 3 could make a "one NAT gateway per AZ" key arguable. The Teacher must re-read every 4.4 NAT question.

## Tests

Option 2: `content_lint.py` and the 4-4 chain (`q1_batch_check`, `distractor_type_audit`, `stem_echo_check`, `claim_prose_check`).

## Learning content affected

Option 1: no. Option 2 or 3: yes, with the Teacher validating before and after.
