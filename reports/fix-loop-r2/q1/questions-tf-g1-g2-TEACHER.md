# Teacher round 2 — lesson-tf-g1 / lesson-tf-g2 (commit b21be9a)

## (a) Own lesson findings

- **TEACHER-Lg2-001** — Gone. `row 8`'s claim now reuses `cite-tf-g2-provider-requirements` (`https://developer.hashicorp.com/terraform/language/providers/requirements`). WebFetch confirms the sentence is on that page, in the Version Constraints section, not on `/terraform/cli/commands/providers/lock` (deleted) and not on `/terraform/language/files/dependency-lock` (AWS's proposed alternative, also fetched — the sentence is not there either). The Lead Dev's fix is the correct one.
- **TEACHER-Lg2-002** — Gone. `tf.004.2d` prose now reads "(A workspace here is the working directory's current state environment; named workspaces ... are covered in a later objective.)" before further uses. Definition is in the prose.
- **TEACHER-Lg2-003** — Gone. `tf.004.2c` prose now reads "(a module is a reusable, packaged Terraform configuration, covered in full in group 5)" at first use. Definition is in the prose.

## (b) Second-role check on AWS's lesson findings

- **AWS-Lg2-001** — Gone. Same citation as above; AWS's suggested URL (`/terraform/language/files/dependency-lock`) was not where the sentence lives, but the Lead Dev's actual fix (`/terraform/language/providers/requirements`) is verified correct, so the underlying defect (wrong URL) is resolved regardless of whose replacement was used.
- **AWS-Lg2-002** — Gone. `lesson-tf-g2-impl.md` row 19 quote now reads "records the identity of that remote object against a particular resource instance" (present tense, matches the doc verbatim). Lesson prose itself still paraphrases as "record," which AWS's finding explicitly said was fine.

## (c)/(d) Question review — all 21

Read all 21 question files. Per-question discriminator and teach-before-test mapped against the lesson (table in `questions-tf-g1-impl.md` / `questions-tf-g2-impl.md`) and checked directly. Findings:

- **TEACHER-Qg1-001 (moderate, teach-before-test)** — `q-tf-004-1b-mc`, distractor b: "A cloud vendor's own native template tool that provisions every resource strictly in the order it is listed in the template, one at a time." The lesson's 1b discriminator only contrasts Terraform's resource graph against a generic "plain automation script... no resource graph deciding what is safe to run in parallel" — it never claims a native single-cloud template tool is strictly serial, and this specific claim is not accurate to how such tools generally work (they also resolve dependencies and can parallelize independent resources). The key (c) is still correct regardless, but the *reason* b is wrong rests on an untaught, likely-inaccurate premise about a named category of real tool. Fix: reword b to something the lesson does teach and that is accurate — e.g. a config-management tool with no dependency graph, or a hand-written script (already used for choice a; needs a distinct replacement), rather than asserting a specific serialization behavior for native template tools.
- **TEACHER-Qg2-001 (minor, citation fidelity)** — `lesson-tf-g2-impl.md` row 8's trimmed quote, "Terraform always installs the same provider versions for a given configuration," was cut from the middle of a conditional sentence ("**To ensure** Terraform always installs the same provider versions... **you can use** ... a dependency lock file..."). Standalone, the fragment reads as an unconditional claim and drops the lock-file mechanism the claim table itself says it backs. It still technically contains the right words, but the excerpt no longer asserts "a lock file provides this guarantee" on its own — it asserts something broader/weaker than the row's claim. Fix: extend the quote to include "...you can use Terraform CLI to create a dependency lock file" (still well under 20 words) so the excerpt actually asserts the row's claim.
- All other spot-checked trims (g1 rows 1–20, g2 rows 1–22) still assert their claim after trimming; no other weakening found. `claim_prose_check.py` shows 0 long-quote warnings for both tasks (confirms the ≤20-word cap is met everywhere).
- Every number used in a key verified against the docs: `~> 2.4.0`/`~> 3.2.0` patch-only increment behavior (`q-tf-004-2a-mc`, `-2a-mr`), and the contrasted `>=`, `=`, `!=`, `<=` behaviors in the same two questions, all match HashiCorp's version-constraints page exactly.
- No duplicate facts across g1's 9 or g2's 12 (own read matches both impl-report maps); g1's enrichment (core workflow, resource-graph concurrency, drift, HCP Terraform, service-agnostic breadth) gives each of its 9 questions a genuinely distinct discriminator — the thinness risk from round 1 is resolved.
- Fairness: every key and every distractor's wrong-answer reason is taught in the task's lesson, except the one exception above (Qg1-001).

## Answers to the five judgment calls

1. **g1 nine questions, no duplicate fact:** Confirmed by direct read — 1a: file+process / plan-stage preview / IaC+declarative as two properties; 1b: resource-graph parallelism / state-backed drift / VCS+shared-visibility; 1c: provider-plugin multi-cloud / service-agnostic breadth / hybrid on-prem+cloud. Nine distinct facts, none repeated. The enrichment worked.
2. **Distractor line:** drawn in the right place — every current distractor is a real practice or real tool category (click-ops, golden images, single-vendor native tools, config-management-after-provisioning, manual runbooks, one-laptop-plus-chat). `1b-mr` choice c specifically is a realistic small-team anti-pattern, not a caricature, and is eliminable only by applying the stated requirement (shared visibility), not on sight — I would not change it. The one distractor I'd still call eliminable-for-the-wrong-reason is `1b-mc` choice b, flagged above as Qg1-001: not because no one would use a native template tool, but because the specific "strictly serial" behavior attributed to it isn't taught and is doubtful.
3. **1a/1b balance:** already shifted mostly to real-tool-vs-real-tool contrasts rather than IaC-vs-manual strawmanning — `1a-mc2` (plan preview vs. rollback/PR-comment/line-review), `1b-mc` (resource graph vs. script/native-tool/config-mgmt), `1b-mc2` (state-backed drift vs. cron/alerting/backup) are all real-vs-real. Only `1a-mc`/`1a-mr` lean on the IaC-vs-manual contrast, which is appropriate since 1a's objective is literally "explain what IaC is." I would not add more contrast questions at the cost of the nine-question budget.
4. **Trimmed quotes:** one fragment (g2 row 8) was cut in a way that drops the conditional/mechanism it was backing — see Qg2-001. All other spot-checked trims still assert their claim.
5. **Bare "provider" in 9/12 g2 distractors:** agree with your read — "provider" is the literal subject of all four g2 objectives, so its presence in distractors is unavoidable subject-matter vocabulary, not recycled phrasing, the same call as "RDS" in a databases lesson. The curated list correctly targets the specific mechanisms (`required_providers`, `provider block`) rather than the bare noun.

Lesson tf-g1: findings closed (TEACHER); no open Teacher lesson findings remain.
Lesson tf-g2: findings closed (TEACHER and AWS, second-role confirmed).

Task tf-g1: not yet (Qg1-001 — one distractor's wrong-answer reasoning is untaught/inaccurate)
Task tf-g2: not yet (Qg2-001 — one citation quote trimmed into a weaker/different claim)
Overall: concerns
