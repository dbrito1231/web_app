# Plan: reopen tasks 4-3, 4-1, 1-3 for the shortest-is-key tell, and fix the letter-reference check

Status: **approved by the user 2026-09-29; implemented and closed 2026-09-29.** No implementation starts before the user approves.
Author: Lead Dev, 2026-09-29. Follows the user's decision of 2026-09-28 (HANDOFF "Decisions taken by the user", item 1).

## Goal

1. **Part A.** Remove the "pick the shortest option" tell from three closed SAA tasks, without introducing any other tell and without changing what any question tests.
2. **Part B.** Make `q1_batch_check.py`'s letter-reference check catch the form that shipped in tf-g4 ("c is wrong because…"), and stop it flagging ordinary English ("answer a different question").

## Part A — scope

Measured today with `q1_batch_check.py`. A tie for shortest counts as shortest.

| Task | MC | Shortest is key | Cap 35% allows | Clearly short (gap ≥ ~10 chars or ≥ 15%) | Near-ties (1–5 chars) |
|---|---:|---:|---:|---|---|
| 4-3 | 14 | 8 (57%) | 4 | k03 (47 vs 63), k05 (47/65), k09 (48/65), s02 (29/51) | k04 (tie), k07 (83/88), s03 (65/67), s04 (72/77) |
| 4-1 | 21 | 10 (48%) | 7 | k05 (10/23), s07 (26/40), s06 (55/63), k03 (11/15) | k01 (36/38), k04 (9/10), k06 (tie), k11 (9/10), s03 (57/58), s10 (9/10) |
| 1-3 | 11 | 5 (45%) | 3 | k04 (12/31), s01 (37/64), s05 (10/34) | k03 (tie), s07 (55/62) |

**Change the 11 clearly-short questions only.** That leaves 4-3 at 4/14 (29%), 4-1 at 6/21 (29%) and 1-3 at 2/11 (18%), all under the cap. The near-ties are not a tell a reader can use: several are sets of bare service names 9 against 10 characters long. Padding them would create the opposite tell.

The HANDOFF figure of "~50 MC questions" was the total MC count in the three tasks, not the number that needs changing.

**Not in scope:** MR questions (the tell is measured on MC only); `3-1` and `3-5` (the user decided to leave them closed and record their figures); the stem-paraphrase and stem-echo rules (closed tasks are not reopened for them); lessons (no change expected — see Risks).

### Method for each of the 11

- **Preferred:** make the key as specific as its distractors. Add the real configuration detail that distinguishes it, stated at the same level of detail the distractors already carry. Never add a justification, a restatement of the stem, or a banned word (`since`, `because`-style self-justification, `even though`, `must`, and the rest of RULES "No giveaway wording").
- **Alternative:** where the key is already as specific as it can honestly be, tighten one verbose distractor instead. Stop once the key sits at a middle rank.
- **Target:** the key lands at length rank 2 or 3 of 4, and must not become the longest. The longest-is-key cap (35%) still applies to the whole task.
- **Fixed:** the tested fact and the correct answer do not change. `id`, `type`, `objectiveIds`, `selectCount`, `correctAnswerIds` and the key's letter position stay as they are, so MC position balance is untouched.
- **Rationale:** if a key's wording changes, the rationale is updated to match, by content, with no letter references.
- **Teach-before-test:** any detail added to a key must already be taught in that task's lesson. If it is not, the writer reports it under "Lesson additions requested" instead of adding it.
- **Parallel form (added at the Teacher's request).** All four options stay in the same form. If every option is a bare service name (e.g. 4-1 k03, k05, s07 and 1-3 s05), do not add a descriptor to the key alone, because the only option with a descriptor becomes the new tell. Either give every option a parallel descriptor, or tighten the long distractors.
- **Each distractor keeps its failing requirement (added at the Teacher's request).** Tightening a distractor must not remove the one stated requirement it fails on. Take particular care with 4-1 s07's DataSync option.
- **Quote the lesson for every added detail (added at the Teacher's request).** For each added detail, the impl report quotes the lesson sentence that teaches it. Known tight cases:
  - For 4-3 s02, tighten distractors rather than add "advanced JSON" to the key, which would echo the stem.
  - For 4-1 s06, confirm whether the lesson teaches the archive-tier price and minimum before using them.
  - For 1-3 k04, do not add "PKCS #11" to the key; the stem already carries it.
- **Record ranks.** The impl report records the length rank of all four options before and after each edit, not just the key's. The final tallies count ties as shortest.

### Pipeline (per RULES and AGENTS.md; content-affecting, so the Teacher validates before and after)

1. **Teacher validates this plan** (read-only). Its verdict is recorded in this file before it goes to the user.
2. **User approves.**
3. **Writer** (1 Sonnet agent, all 11 questions). It edits only those 11 question files, then runs the whole chain on all three tasks and appends a report to `reports/fix-loop-r2/q1/reopen-shortest-key-impl.md`. For each question the report gives old and new text for every changed choice, and the length rank before and after.
4. **Lead Dev pre-check.** Run the whole chain on all three tasks. Run `key_text_diff.py <task> <HEAD before edits>` to prove no key changed which option is correct (expect 0 mismatches). Read every changed choice in isolation, with the two questions for each: is it still real, and is the reason it is right or wrong taught in the lesson? Confirm no new stem echo on the changed questions: `stem_echo_check` is advisory for 1-3, 4-1 and 4-3, so it is compared against a baseline taken before the edits.
5. **Review** (2 Sonnet agents in parallel): the technical reviewer and the Teacher review the 11 questions for correctness, new tells, strawmen and teach-before-test. They report as `AWS-RSK-###` and `TEACHER-RSK-###` in `reports/fix-loop-r2/q1/reopen-shortest-key-review.md` (the Teacher's text is saved by the Lead Dev). Every item closes only when its reporter and a second role mark it Gone.
6. **Student** (1 Sonnet agent). A text packet containing only the three lessons' relevant sections, the 11 changed questions, and four near-tie controls (4-3 k07, s03, s04; 1-3 k03), which check that the near-ties left alone are not exploitable. All questions are answered before the key is opened, with the same two stem-wording numbers plus the length-tell count.
7. **Close.** Add a row to `progress.md`, a row to the issue register, and a note in HANDOFF; record the unchanged `3-1`/`3-5` figures; confirm the DB fingerprint; commit after each step.

## Part B — letter-reference check in `scripts/q1_batch_check.py`

**Current defect** (`scripts/q1_batch_check.py:19`): the regex matches only "choice c", "option b" or "(c)".
- **Misses:** the bare form "c is wrong because…". All 10 tf-g4 rationales with shifted letters passed the check at `db11570`.
- **False positive:** it matches "answer a" in "so they answer a different question", which makes `1-3` FAIL today on `q-saa-1-3-s01-mc`.

**Change:** replace `LETTER` with a pattern that matches
- "choice/option X" and "(X)", as now; "answer" is dropped from this form;
- a lone `b`–`e`, not inside a word or backticks, followed by a predicate verb (is, misstates, reverses, overreaches, names, claims, confuses, …);
- a lone `a` only before a verb the article never precedes (is, was, misstates, reverses, …);
- a sentence-initial capital `A`–`E` followed by the same verbs.

**Measured with a prototype** (scratchpad `plan_letter_proto.py`, read-only):

| Corpus | Result |
|---|---|
| The 24 tf-g4 files at `db11570` | 10 caught, exactly the 10 found by hand |
| The current corpus, 429 files | 0 hits, and the `1-3` false positive is gone |

**Test:** add a unit-style self-check to the script, or a small `scripts/test_q1_letter.py` if the file has no test hook. It covers known-bad strings (the 10 tf-g4 openings) and known-good ones ("answer a different question", "a data block is", "`aws_s3_bucket.b` is"), and asserts both directions.

## Files touched

- **Part A:** the 11 question files under `content/questions/`, which are learning content. Also `reports/fix-loop-r2/q1/{reopen-shortest-key-impl.md, reopen-shortest-key-review.md, progress.md}`, `reports/fix-loop/issue-register.md`, `HANDOFF.md` and `docs/status.md`.
- **Part B:** `scripts/q1_batch_check.py`, plus possibly `scripts/test_q1_letter.py` (app code; no content impact).

## Risks

- **A repair introduces a new defect.** This has happened on four tasks, which is why RULES has its "After applying a fix" section. Mitigation: whole-chain runs, reading every changed fragment in isolation, and the key_text_diff proof.
- **The fix inverts the tell to longest-is-key.** Mitigation: the rank 2–3 target, and the cap still enforced across the whole task.
- **Lengthening a key with a detail the lesson does not teach.** That is a teach-before-test failure. Mitigation: the writer must quote the lesson sentence for any added detail, or request a lesson addition. A lesson addition would be a lesson change and needs a note back to the user before it is applied.
- **Stale AWS facts in a key being lengthened.** These tasks were closed on 2026-09-26/27. Any new fact goes through the AWS Knowledge MCP and gets a claim row.
- **Part B false positives on future tasks.** Mitigation: the self-test, and the regex requires a verb after the letter.

## Tests (definition of done)

- `content_lint.py` PASS.
- `q1_batch_check.py` for 4-3, 4-1 and 1-3: shortest-is-key ≤ 35%, longest-is-key ≤ 35%, and no other FAIL. `1-3`'s current letter FAIL clears with Part B.
- `key_text_diff.py` shows 0 correct-option changes against the pre-edit HEAD for all three tasks.
- Both reviewers approve.
- The Student is fair, with 0 keyword-guessable stems among the 11.
- Part B: the self-test passes in both directions; all 22 tasks are re-run and every other result is unchanged.
- `python manage.py test workbook`, `content_lint.py` and `npm run build` are deferred to the final sitting, per HANDOFF. No app code other than the script changes.

## Learning content affected?

**Yes**, for 11 question files, by wording only; no fact and no key changes. The lesson is not expected to change.

## Estimated cost

About 0.6–0.8M subagent tokens: a Teacher plan check, 1 writer, 2 reviewers and 1 Student. tf-g4 cost about 1.2M across three review rounds.

## Teacher validation (before user approval)

Fresh Sonnet Teacher, 2026-09-29. Verdict: **Plan: approve**, with two required changes, both now applied above: parallel option form with each distractor keeping its failing requirement, and a quoted lesson sentence per added detail.

- **Scope confirmed.** All 11 are real gaps and none is a false alarm. The near-ties are correctly left out. 4-3 k07 (83 vs 88) should stay out, but the longest-is-key cap must be re-run after any 4-3 edit, because the projected 29% leaves little margin.
- **Lesson additions.** None expected. The tight cases are 4-3 s02, 4-1 s06 and 1-3 k04, handled as in the method.
- **Part B.** No learner impact.
- **One Teacher claim was wrong.** It asked to "re-verify the four stem-echo waivers already recorded for these tasks". `stem-echo-waivers.json` has no entries, and its README says tasks 1.1–4.4 have none. There is nothing to re-verify; `stem_echo_check` stays advisory for these tasks against a pre-edit baseline.

## Close-out (2026-09-29)

- **Correction to the Tests section.** `key_text_diff.py` compares the *text* of the correct option, so it flags every key that was reworded on purpose (4-3: 4, 4-1: 3, 1-3: 3). The right proof was a field-by-field comparison against `289014c`. `id`, `type`, `objectiveIds`, `selectCount`, `stem`, `correctAnswerIds` and choice-id order were all identical in the 11 files.
- **Final figures.** Shortest-is-key is 29/29/18%; longest-is-key is 21/29/27%. Stem echo: one flag removed (4-3 k05), none added. The 4-1 distractor-audit FAIL is byte-identical to `289014c`.
- **Reviews.** Technical and Teacher both close/approve after one fix pass (4-3 s02, 4-3 k09, 1-3 s01). Optional items AWS-RSK-002/003 and TEACHER-RSK-003 were left unapplied, with the agreement of both reviewers.
- **Student.** 15/15, fair. See `reopen-shortest-key-STUDENT.md` for the two minor observations recorded in the register.
- **DB.** Fingerprint `930f0e72…`, unchanged.
