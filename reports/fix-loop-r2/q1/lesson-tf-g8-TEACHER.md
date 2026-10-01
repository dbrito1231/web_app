# Teacher round 1 — lesson-tf-g8

Saved by the Lead Dev from the Teacher's reply (condensed; fixes and ownership verbatim).

**Method.** All 219 claim-table quotes were fetched with curl and matched. All 219 are verbatim; 12 needed a context read because of markup spacing. 24 rows were read in context. Every cross-reference to g1, g4, g5 and g6 holds.
- Row 79 (the Local-mode health inference) is honestly worded.
- Row 56 has a better source in `manage-policy-sets`.

## Findings
- **TEACHER-Lg8-001 (medium, 8b policy sets).** The quote includes "Stacks", but "Sentinel and OPA policy sets only support workspaces". Stacks are also undefined. Fix:
  - quote only "to specific projects, workspaces … or to workspaces with specific tags", or add "(Sentinel and OPA policy sets only support workspaces; Stacks are not covered here)", with a row for the policy-enforcement sentence;
  - add one gloss for the other "and Stacks" quotes: "Stacks are a newer HCP Terraform unit this lesson does not cover."
- **TEACHER-Lg8-002 (medium, 8b hard mandatory, Warnings, tip).** Hard mandatory is overridable when the policy set allows overrides. Fix:
  - 8b: "Hard mandatory stops the run; only a policy set configured to allow overrides changes that, so treat it as the level that cannot be overridden by default."
  - Warnings: "…overrides exist for soft mandatory and OPA mandatory policies, and for hard mandatory only when the policy set allows them…"
  - Questions must not claim hard mandatory is never overridable.
- **TEACHER-Lg8-003 (low, 8c sharing, 387 words).** Split it into `#### Run triggers` and `#### Remote state and workspace locking`. Add: "Locking a workspace stops new HCP Terraform runs, which wait in Pending; state locking (6b) is Terraform preventing two operations from writing state at once."
- **TEACHER-Lg8-004 (low, 8c Remote mode).** "the mode that enables Sentinel, cost estimation and notifications" overreaches. Fix: "The docs list Sentinel enforcement, cost estimation and notifications as features of this mode; Local mode 'disables remote execution'."
- **TEACHER-Lg8-005 (low, 8a vs 8c).** Fix 8a: "…remote operations enabled, which is 'the default' (a project can set a different default; see 8c)…"
- **TEACHER-Lg8-006 (low, 8a).**
  - Gloss "configuration version" as "(marked as a speculative run in the runs API)".
  - Drop the saved-plan exception clause unless a question needs it.
  - Add "(8b explains these)" after the stage list.
  - Move or cut the stray `terraform import` sentence.
- **TEACHER-Lg8-007 (low, intro).** "Group 1 (1b) introduced HCP Terraform in one sentence" should read "introduced HCP Terraform briefly".

**Teaching quality.**
- At 4,495 words the lesson is teachable: its `####` subsections run 111–387 words, and no subsection exceeds 350 after 003.
- Contrasts are present; only workspace lock vs state lock is thin (003).
- No contradictions.
- Tiers are quoted exactly with an adequate caveat, but **no question may use tier membership as a key**.

## Facts and ownership (one fact per question, no duplicates)
**8a**
- mc: remote operations run on disposable VMs, and a CLI apply executes there.
- mc2: the three workflows and what starts each.
- mr: a merge to the linked branch queues a run; remote apply only works with no linked repo (no pull-request fact).
- extra-00: speculative plans (plan-only, started by a PR, not run for forks).
- extra-04: plan-first, default approval, "Planned and finished", the per-workspace queue and pending.
- Spare: import not run remotely, saved plans need CLI v1.6.0, the stage list.

**8b**
- mc: the Plan role cannot apply; permissions are additive.
- mc2: Sentinel imports vs OPA Rego (an empty array passes), one framework per set. No enforcement levels.
- mr: soft, hard and OPA mandatory override rules (per 002).
- extra-01: run tasks (four stages, advisory vs mandatory, most restrictive wins).
- extra-05: health assessments only (drift detection, continuous validation, Remote/Agent required).
- Spare: audit trail (14 days), cost estimation (off by default), private registry. No editions as a key.

**8c**
- mc: an HCP workspace is required; a CLI workspace is optional.
- mc2: a project holds each workspace exactly once; the default project cannot be deleted; project permissions.
- mr: the three execution modes.
- extra-02: remote state sharing (off by default, three scopes, `tfe_outputs`). A run trigger may be a distractor.
- extra-06: variable sets (scopes, workspace beats set, `-var` beats both).
- Spare: run triggers, workspace lock, small workspaces.

**8d**
- mc: `terraform login` (plain-text token, app.terraform.io, interactive).
- mc2: `name` vs `tags`.
- mr: `TF_CLOUD_*` only when the argument is omitted, an empty `cloud` block, `TF_WORKSPACE` never creates.
- extra-03: `init` migrates state; `backend "remote"` becomes `cloud`; `prefix` becomes `tags`.
- extra-07: OAuth, webhooks, one branch, directory triggers, project-scoped connections (not "commits start runs", which 8a owns).
- Spare: implicit workspace creation by `init`, `.terraformignore`, Terraform 1.1+.

Lesson tf-g8: not yet (fix 001–002; 003–007 may ride along) · Overall: concerns

# Teacher round 2 — tf-g8 (c44481b)

I read the lesson (4,861 words) and all 20 questions end to end. I re-ran the five scripts (content_lint, q1_batch_check, stem_echo_check, distractor_type_audit, claim_prose_check) and all pass. "HCP Terraform" sits at exactly 3/20 (15%) in the distractor audit. I checked the Read-role and run-task override facts against the HashiCorp docs with curl.

## (a) My round 1 findings

| Id | Status | Evidence |
|---|---|---|
| 001 | Gone | The policy-set quote is cut to "globally, to specific projects, workspaces" or "to workspaces with specific tags". "Sentinel and OPA policy sets only support workspaces" is quoted. Stacks are glossed once in 8b ("another kind of resource a project can hold… this lesson does not cover them"). The later "and Stacks" quotes in 8c point back with "(Stacks are glossed in 8b)". |
| 002 | Gone | The 8b hard-mandatory bullet, the Enforcement-levels summary, the exam tip and Warnings bullet 5 all say hard mandatory is overridable only when the policy set allows it. 8b-mr key c matches. |
| 003 | Gone | `#### Run triggers` and `#### Remote state and workspace locking` exist. The sentence separating a workspace lock from state locking (6b) is present. |
| 004 | Gone | Remote now reads "The docs list Sentinel policy enforcement, cost estimation and notifications as features of remote execution". The Local line "disables remote execution" is quoted. |
| 005 | Gone | 8a says "the default" for a workspace left on its default settings, and "a project or organization can set a different default; see 8c". |
| 006 | Mostly gone | The "(8b explains…)" pointer is added, the stray `import` sentence is removed, and the saved-plan clause is replaced by the verified VCS limit. "Configuration version" is still not glossed (see TEACHER-Lg8-010). |
| 007 | Gone | The intro now says "introduced HCP Terraform briefly". |

## (b) Second-role check of AWS-Lg8-00x

| Id | Status | Evidence |
|---|---|---|
| 001 | Gone | The override option, the "even policies set to Hard mandatory" quote and the precedence quote are all in 8b, and Warnings is reworded. |
| 002 | Gone | 8c now teaches the layers: Project Default, then the organization's "Remote or Local", then "inherit the project default". 8d scopes "Remote" to a workspace that `terraform init` creates. 8a is qualified. |
| 003 | Gone | The pull-request condition and destination-branch quotes are in 8a. |
| 004 | Gone | The cost-estimation and policy-check stages are marked as conditional. |
| 005 | Gone | Same fix as my 001. |
| 006 | Gone | The saved-plan VCS limit and the v1.6.0 floor are both present. |
| 007 | Gone | The quoted "enables advanced features, such as…" wording replaces the exhaustive reading. |
| 008 | Gone | The Local-mode line is labelled "this follows from the requirement", and 8b-extra-05 words it the same way. |
| 009 | Gone | The migration sentences now follow the order on the page: "requires all workspaces to have a name", then rename, then unique names. |
| 010 | Not applied | Optional. |

## (c) The lesson as a whole

- **Coherence:** it is still coherent at 4,861 words. I found no new contradiction. The cross-references to 1b, 6b, 6c and 8a through 8d all hold.
- **Objective coverage:** no objective is under-taught.
- **Enforcement levels split:** the new `#### Enforcement levels` subsection is fine. It is about 150 words and gives the "trap" paragraph a clear home. It keeps each 8b subsection short, so I would keep it.
- **TEACHER-Lg8-008 (low, 8b policy sets):** the text says a policy set applies "to specific projects", then calls Sentinel and OPA sets "workspace-only". The two read as a clash.
  - Fix: change "are workspace-only:" to "do not cover Stacks:". The quote is unchanged.
- **TEACHER-Lg8-009 (low, 8b Teams and permissions):** the lesson never states what Read allows, so 8b-mc distractor c rests on inference. I verified the docs table: "Read: View information about workspace runs." and "Plan: Queue Terraform plans in the workspace."
  - Fix: add `Read means "View information about workspace runs."` beside the Apply and Plan quotes, with a claim row.
- **TEACHER-Lg8-010 (low, 8a speculative plans):** "configuration version" is undefined for a college student.
  - Fix: append "(the uploaded configuration a run uses)". No question depends on this.

## (d) Questions

I checked every choice against two tests: is it really wrong, and is the reason it is wrong taught in the lesson. Unless a row says otherwise, "really wrong?" and "reason taught?" are both yes for every distractor, and the key is right.

- **Ownership:** followed in all 20 questions.
- **Duplicates:** none. 8a-mc and 8c-mr overlap slightly, because 8c-mr distractor c is the negation of 8a-mc's key. They test different keyed facts, so I accept it.
- **Letter references:** none in any rationale.
- **Absolutes:** only on distractors, apart from the necessary qualifiers on 8b-mr c ("only when") and 8a-mr d ("cannot").
- **Equivalent pairs:** none.

| Question | Key | Verdict |
|---|---|---|
| 8a-mc | c | Distractor d (plan on laptop, apply remote) is a weak hybrid. TEACHER-Qg8-004. |
| 8a-mc2 | a | Clean. Distractors b and c are eliminated by stem details (no repository, no commands). |
| 8a-mr | b, d | Both keys are the two longest choices. TEACHER-Qg8-002. |
| 8a-extra-00 | b | Clean. |
| 8a-extra-04 | d | Clean. Choice c rests on "plan-only is the exception", which is adequate. |
| 8b-mc | d | Choice c (Read) is eliminated only by inference. TEACHER-Qg8-001 and Lg8-009. |
| 8b-mc2 | b | Clean. Choice d is a plausible, if thin, run-task misuse. |
| 8b-mr | a, c | Both keys are the longest two (115 and 104 characters against 84, 79 and 56). TEACHER-Qg8-002. The content is right and consistent with Lg8-002. |
| 8b-extra-01 | d | Clean. I confirmed the run-tasks docs mention no override for run tasks, so choice b is really wrong. |
| 8b-extra-05 | b | Clean, and the Local-mode wording is honest. |
| 8c-mc | a | Clean. |
| 8c-mc2 | c | Clean. The "permissions at workspace scope" fact is taught in 8b. |
| 8c-mr | a, e | Clean. |
| 8c-extra-02 | a | The key says sharing is switched on "in the `network` workspace itself", but the lesson never says where the setting lives. Choice c (lock needed to read state) is a borderline invented rule. TEACHER-Qg8-005. |
| 8c-extra-06 | c | Choice d ("Terraform stops…") is the longest choice and an outlier, while the key is the shortest. TEACHER-Qg8-006, minor. |
| 8d-mc | b | Clean. |
| 8d-mc2 | d | Clean. |
| 8d-mr | c, d | Clean. Distractor a is refuted by the quoted "will not create a new workspace from this variable". |
| 8d-extra-03 | c | Stem and key echo each other, and choice d is near-strawman. TEACHER-Qg8-003. |
| 8d-extra-07 | a | Key wording "directories… trigger runs" is close to the lesson's wording but is a structural reference. Choice c is acceptable because it is taught as a filter on CLI uploads only. |

Other checks:
- **Caricatures:** 8a-mc d, 8c-extra-02 c and 8d-extra-03 d are the borderline ones, covered by Qg8-004, 005 and 003.
- **Distractor-only "as…/because…" clauses:** none.
- **Stem/key echo:** only 8d-extra-03 and, weakly, 8b-mc.

New findings:
- **TEACHER-Qg8-001 (low, 8b-mc):** the stem says "queue plan runs" and the key says Plan "queues Terraform plans". That is a keyword match on the role name.
  - Fix: reword the stem to "submit changes for review and see what each would do, while a senior engineer decides what is applied". Add the Read quote from Lg8-009 so choice c is eliminated by a taught sentence.
- **TEACHER-Qg8-002 (low, 8a-mr and 8b-mr):** in both questions the two keys are the two longest choices, a length tell.
  - Fix for 8b-mr: shorten key a to "A failed OPA mandatory policy can be overridden by a user with Manage Policy Overrides". Shorten key c to "A failed Sentinel hard mandatory policy can be overridden only if its policy set allows overrides". Lengthen e to "OPA offers the same three enforcement levels as Sentinel: advisory, soft mandatory and hard mandatory".
  - Fix for 8a-mr: lengthen c to "A commit pushed to any branch of the repository, including feature branches, queues a run".
- **TEACHER-Qg8-003 (low, 8d-extra-03):** the stem asks about "the migration of that state" and the key says "migrate the existing state". Only the key shares that term with the stem.
  - Fix: stem "What step actually brings that existing state into HCP Terraform?" Key "Run `terraform init` and answer yes when prompted to copy the existing state".
- **TEACHER-Qg8-004 (low, 8a-mc):** distractor d says the plan runs on the laptop and only the apply runs remotely. Nobody believes this.
  - Fix: replace it with "On HCP Terraform's machines only for repository-linked workspaces, while CLI runs stay on the laptop". The lesson refutes this with "CLI operations are remotely executed by default".
- **TEACHER-Qg8-005 (low, 8c-extra-02):** drop the "in the `network` workspace itself" location claim from the key.
  - Fix: use "State sharing is off by default and has to be enabled for `network`".
- **TEACHER-Qg8-006 (low, 8c-extra-06):** shorten choice d to "Terraform reports an error for a key defined in several places".

**LD-Qg8-001 ruling:** the Read distractor is really wrong. It is taught only by inference from the role ladder, and the lesson never says Read is the lowest role. I would not accept it as it stands. Add the verified Read quote (TEACHER-Lg8-009) and the Plan quote already there. With both in place, c is eliminated by a quoted contrast.

**LD-Qg8-002 ruling on TERMS:** add only `run trigger` (3 questions, 15%, three different wrong reasons) and `variable set` (8c-mc2 b and extra-02 d, 10%). That is a safe addition, because the audit still passes at the cap.
- Do not add the rest. `speculative plan`, `tfe_outputs` and `TF_WORKSPACE` appear in no distractor or in only one question. `TF_CLOUD_` appears only in 8d-mr.
- Do not add `Sentinel` or `OPA`, since they are 8b's subject vocabulary.
- Leave "HCP Terraform" as is.

## (e) Numbers

No question uses a number beyond "three enforcement levels" (8b-mr e), "two levels" and "all three workspaces". These match the lesson: Sentinel has advisory, soft mandatory and hard mandatory, OPA has two, and the three `app-` workspaces are in the stem. No tier, version or day count is used as a key.

**not yet**

# Teacher round 2b — tf-g8 (ace0419)

I read the lesson and all 20 questions end to end. I re-ran the five scripts and all pass. The distractor audit shows "variable set", "run trigger" and "HCP Terraform" each at 3/20, which is the 15% cap. I checked the priority-variable-set wording against the managing-variables page with curl.

## 1. My round 2 findings

| Id | Status | Evidence |
|---|---|---|
| Lg8-008 | Gone | The 8b policy-set text now says "Sentinel and OPA sets do not cover Stacks", with the quote unchanged. The clash with "specific projects" is removed. |
| Lg8-009 | Gone | The Teams and permissions paragraph now says: Read means "View information about workspace runs." It sits next to the Plan and Apply quotes. |
| Lg8-010 | Gone | The gloss is in place, and I accept the deviation. "One saved version of a workspace's configuration, which a run uses" is plain and no longer undefined, and it makes no claim the page does not support. |
| Qg8-001 | Gone | The 8b-mc stem is now "submit changes for review and preview what each would do on their own". Choice c quotes the taught Read sentence, and the rationale contrasts it with the Plan quote. |
| Qg8-002 | Gone | In 8a-mr, distractor c (107 characters) is now the longest choice, and the keys are 78 and 84. In 8b-mr, the keys are 86 and 97, while distractor e (101) is the longest. `q1_batch_check` shows longest-is-key at 3/16 (19%). |
| Qg8-003 | Gone | The stem is now "What gets that state into the HCP Terraform workspace?". The key's "migrate" matches no stem word, and `stem_echo_check` is clean. |
| Qg8-004 | Gone | 8a-mc distractor d is now "HCP Terraform's machines only for repository-linked workspaces, while CLI runs stay on the laptop". It is a real misconception, and the "remotely executed by default" quote refutes it. |
| Qg8-005 | Gone | The extra-02 key is now "State sharing is off by default and has to be enabled for `network`", with no location claim. |
| Qg8-006 | Gone | The extra-06 distractor d is shortened to "Terraform reports an error for a key defined in several places". It is still the longest at 62 against 35 to 41, but it is a distractor and no longer an outlier. |

**Deviation 1 (Lg8-010 gloss):** accepted. Optionally say "saved copy of the configuration files" for a plainer read, but nothing depends on it.

**Deviation 2 (8c-mc2 "open workspaces"):** accepted. "Open" does not echo the key's "access", and the stem still states the constraint that eliminates d.

## 2. AWS findings, second-role check

- **AWS-Qg8-001:** Gone.
  - The stem says "not marked as priority".
  - The rationale says the set is not priority.
  - The lesson teaches the priority exception.
  - Key c is correct.
- **AWS-Qg8-002:** Gone. The stem adds the "neither team should open workspaces it does not already use" constraint. Distractor d is eliminated by the taught "By default, all workspaces belong to an organization's Default Project".
- **AWS-Qg8-003:** Gone. The stem is reworded, and option a is now `backend "local"` beside `cloud`. The lesson teaches that the two cannot coexist.
- **AWS-Qg8-004:** Gone. Distractor c is now "different projects, remote state only works within one project". The three taught share scopes (organization, same project, specific workspaces) refute it.
- **AWS-Qg8-005:** Gone. The key is "Plan, which can queue Terraform plans".
- **AWS-Qg8-006:** Gone. Distractor c now says "regular plan-and-apply run", so the speculative-plan reading no longer applies.
- **AWS-Lg8-011:** Gone. The text now says "One place the docs state Remote as the default…".
- **AWS-Lg8-012:** Gone. See section 3.
- **AWS-Lg8-013:** Gone. The text says "(plan-only runs are not affected: 'Locking does not affect plan-only runs')".
- **AWS-Lg8-014:** Gone. See section 3.

## 3. New lesson sentences

- **Priority variable sets:** accurate. The page says "The values in priority variable sets overwrite any variables with the same key set at more specific scopes", and the quote is limited to global sets. It makes "that is the exception" clear next to the -var sentence. It is consistent with the extra-06 rationale.
- **Read role:** accurate and clear, with no contradiction with Plan and Apply.
- **Configuration-version gloss:** clear, and nothing contradicts it.
- **Plan-only locking exception:** consistent with the queue paragraph ("plan-only runs … do not block the progress of other runs") and with extra-04.
- **OPA stage:** accurate to the page. See TEACHER-Lg8-011 below.

## 4. Re-read of changed items as a lesson-only reader

All chosen and eliminated answers have a taught reason.

- **8a-mc:** key c is shown by the quoted "disposable virtual machines" sentence. The distractors are eliminated by the Local mode, Agent mode and remote-by-default teaching.
- **8a-mr (b, d):** b is taught. d is taught by "Remote terraform apply is for workspaces without a linked VCS repository". a is refuted by the manual first run. c is refuted by the one-branch teaching. e is refuted because VCS code comes from the repository.
- **8b-mc vs Read c:** c is eliminated by the quoted Read versus Plan contrast. The key is the shortest choice at 37 characters. See TEACHER-Qg8-007.
- **8b-mr (a, c):** both keys are taught. Distractor e (three levels for OPA) is refuted by "two policy enforcement levels".
- **8c-mc2:** the d rationale is sound. Each project has its own team permissions, so moving the workspace into the Default Project either leaves both teams without access or exposes the other workspaces that start there, and the lesson teaches that default.
- **extra-02:** the new c ("different projects, remote state only works within one project") is refuted by the same-project share scope the lesson teaches.
- **extra-03:** key c is taught.
- **extra-06:** the stem pins "not priority", and the lesson gives the precedence order.
- **extra-07:** key a is taught. b, c and d each have a taught refutation.

**"Variable set" at the cap:** the three uses are three different wrong reasons.
- 8c-mc2 b: a variable set changes variable scope, not which project a workspace belongs to.
- extra-02 d: a variable set shares variables, not state.
- extra-06 a: a non-priority global set loses on precedence.

**"Run trigger" at the cap:** the three uses are also different.
- 8a-mc2 d: a run trigger starts a run from another workspace's apply, not from a pipeline upload.
- extra-02 b: a run trigger does not grant state access.
- extra-07 d: a run trigger is not driven by file changes.

## 5. New findings (all Low, none blocking)

- **TEACHER-Qg8-007 (Low, 8b-mc):** the key (37 characters) is much shorter than every distractor (61 to 75). It is not a length-tell for "longest is key", but a very short key can look unusual.
  - Fix: use "Plan, which can queue Terraform plans in the workspace", which matches the quoted phrase.
- **TEACHER-Qg8-008 (Low, 8b-mc, optional):** a Read user can still see a speculative plan that a pull request starts, so "preview what each would do" is not strictly impossible for Read. The key still holds, because "on their own" and the rationale's "queue plans" separate the roles.
  - Fix: if you want it tighter, say "start their own preview plans" instead of "preview what each would do on their own".
- **TEACHER-Lg8-011 (Low, 8a stages):** the sentence "An OPA policy check stage is conditional in the same way" names a stage that is not in the six-stage list just above it. It reads as a seventh stage.
  - Fix: add "(the policy check stage covers both Sentinel and OPA when enabled)".
  - Optionally, change "A variable set can be marked as priority" to "A global variable set can be marked as priority", to match the quote.

No new contradictions. No question depends on any of these items.

**Verdict: close** (the Low items may ride along or be dropped).
