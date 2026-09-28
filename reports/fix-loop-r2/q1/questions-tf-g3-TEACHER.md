# Teacher round 2 — lesson-tf-g3 + 21 questions (commit f3e3679)

## (a) My round-1 findings

- **TEACHER-Lg3-001 (version wording) — Gone.** 3d now cites the destroy page's precise "The `-destroy` option to `terraform apply` exists only in Terraform v0.15.2 and later" alongside the plan page's looser "v0.15 and earlier," with an explicit note on which to trust for an exact-version question. Re-fetched both pages: both quotes verbatim.
- **TEACHER-Lg3-004 (3f had only two discriminators) — Gone.** `destroy -target` added as a doc-verified third discriminator (claim row 47, quote verbatim on the destroy page). See the teachability assessment below — fixed correctly, and fixed *for the right reason* (the writer caught and reversed a wrong direction I had asserted).
- **TEACHER-Lg3-002 (unexpanded "CI") — Gone.** 3g now reads "CI (continuous integration)."
- **TEACHER-Lg3-003 (undefined "drifted") — Gone.** 3e now glosses "drifted (changed outside Terraform since the plan was made)."

## (b) Second-role check: AWS-Lg3-001, AWS-Lg3-002

- **AWS-Lg3-001 (fabricated fmt quote) — Gone.** Re-fetched the fmt page: "This command applies a subset of the Terraform language style conventions, along with other minor adjustments for readability" is verbatim there; the old fabricated quote is gone from row 42 and from prose. Also re-fetched to confirm the page has no sentence using "correct," "valid," or "validity" anywhere — none found, so the lesson's now-unquoted inference ("nothing on the fmt command's own doc page describes checking whether a configuration is correct or valid") is accurate, not just unquoted.
- **AWS-Lg3-002 (version boundary) — Gone.** Confirmed verbatim per (a) above. Good resolution: rather than just swapping one number for another, the lesson keeps both source sentences and explains which one is precise — that's more defensible than silently overwriting "0.15" with "0.15.2."

## (c) Question review — teach-before-test and fairness

All 21 read. Every key and every distractor-rejection reason traces to taught lesson content, with one exception (Qg3-001 below). Citations correctly paired to each question's own objective's citation id throughout. No stem pastes objective text; all MR stems carry "(Select TWO.)"; no strawman distractors (the closest candidate, 3a-mc2's "lock the entire repository," is a plausible bad team practice, not a nobody-would-pick anti-pattern).

**The 3f asymmetry — teachable as written.** The lesson states the destroy-vs-block-deletion dependency asymmetry three times in three forms (a direct claim, a contrast with block-deletion, and an explicit two-branch summary sentence), then the exam tip restates it a fourth time in parallel phrasing. That redundancy is what makes it learnable rather than a parsing trap. `3f-mc2` tests it as a scenario→command match (student must know *which* command has the wider blast radius); `3f-mr` tests it as a direct two-route comparison with a concrete dependency (instance→security group) named in the stem. Both require recalling the fact, not just parsing the question's grammar — I'd call these fair. Only cosmetic note: the lesson's own transition sentence ("this objective's discriminator is telling them apart") reads awkwardly; consider "This objective is about telling these three routes apart" — not blocking.

**Reworked `3d-mc2` and `3g-mc2` — genuine, objective-covered.** `3d-mc2` now tests the `-target`-extends-to-dependencies *consequence* (a plan over an instance that references a security group), correctly reversed to match the doc-confirmed direction; it no longer shares a flag-naming pool with `3d-mc`. `3g-mc2` now tests `fmt -check`'s consequence (file untouched, non-zero exit, name listed) instead of flag-naming, no longer overlapping `3g-mc`'s `-recursive` question. Both stay on their stated objectives.

**Self-explaining choices — fixed, and I found no others.** `3g-mc` c and `3g-mc2` a no longer state their own failure reason. I swept all 21 questions' choice text for the same pattern (a clause that hands over the elimination logic, like the old "...which only reaches the current directory") and found none remaining.

**New finding — TEACHER-Qg3-001 (Low).** `3d-mc2`'s rationale, rejecting choice c ("`-target` is only accepted by destroy, never by plan"), says: "`-target` is accepted by plan as well as by **apply and destroy**." Only the "by plan" half is needed to reject the distractor and is well taught; "and destroy" is true and taught (3f), but "apply" accepting `-target` is never taught anywhere in this lesson (3e's section never mentions `-target`) or cited. Fix: trim the clause to "`-target` is accepted by `plan`, not just `destroy`," dropping the untaught `apply` claim.

**New finding — TEACHER-Qg3-002 (Low, advisory).** `3d-mr` key (d) ("saved plan file can later be used to carry out exactly the actions shown, without recomputing them") and `3e-mc2` key (b) ("performs exactly the operations recorded in that saved plan, without regenerating it or prompting") rest on largely the same core fact. Each carries something the other doesn't (3d-mr pairs it with the "replace" action; 3e-mc2 adds the no-prompt/confirmation angle, which is 3e's own discriminator), so I'm not calling this a hard duplicate — but it's the closest the task comes to double-testing one idea. Not blocking; worth remembering if either question is revised.

## (d) Numbers and flag behavior in keys

Only two numeric literals appear anywhere in the lesson prose ("0.15" and "0.15.2"); neither is used in any of the 21 questions — no stem, choice, or rationale in this task mentions a Terraform version number, so there is nothing numeric to verify in a key. Every flag-behavior fact actually used in a key was checked against the cited doc page and is correct: `-refresh-only`, `-upgrade` (both clauses), `-target`'s dependency-extension direction (on `plan` and on `destroy` — both re-confirmed against source this round, matching the corrected direction), `-out`/"replace", `-auto-approve`, saved-plan-file behavior, `apply -destroy`, `destroy -target`, `-recursive`, `-check`'s exit-status/file-list behavior, and `validate`'s scope. No key or distractor-rejection asserts a flag behavior the docs contradict.

## Claim-table sweep (round-2 delta)

New/changed rows 42, 46, 47 all reach lesson prose verbatim (checked directly, not assumed): row 42's replacement quote, row 46's "v0.15.2" figure, and row 47's `destroy -target`/dependencies quote are all present in the current `bodyMarkdown`. No silent claim-table row this round.

Task tf-g3: close
Overall: approve
