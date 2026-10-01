# lesson-tf-g8 -- AWS (Terraform docs) review, round 1

## Method

- Parsed all 219 claim-table rows and fetched every distinct URL myself with `curl -sL`, stripped HTML to text with Python (scratchpad `awsg8_chk.py`, `awsg8_g.py`; page texts kept as `awsg8_*.txt`). No WebFetch.
- Machine-checked every row's quote against the page named in its URL column (whitespace, quote marks and backticks normalised). First pass reported 15 misses; I read each page and all 15 are formatting artefacts only (a space before a comma, bullet labels split by markup, a heading rendered as `Remote (custom)`). Result: 219 of 219 present on their pages.
- Read in context (not only the quote) the rows on: plan tiers (teams, projects, health, audit trails, policy-set free limit), version floors (`cloud` v1.1, saved plans v1.6.0, run tasks 1.1.9), numbers (14 days, 20 source workspaces, five users, one policy set of five policies), enforcement levels (Sentinel and OPA), defaults (remote operations, execution mode, cost estimation, remote state sharing, run-trigger auto-apply) and absolutes (fork PRs, `cloud` name versus tags, env-var precedence). About 60 rows read in context, well over the 25 required.
- Read the whole `bodyMarkdown`, g6 6b/6c (plus g1 1b, g4, g5, g7 cross-references) and the 8 extras' objectiveIds. Checked prose with no claim row against the pages.
- No AWS calls, no terraform commands, no HCP Terraform sign-in, no git, no content edits.

## Rows verified (219 of 219 verbatim; exact-claim judgment on the priority rows)

| Rows | Page | Verbatim | Exact claim? |
|---|---|---|---|
| 1-3 | cloud-docs overview | yes | yes. Name change; Terraform Enterprise as "self-hosted distribution". |
| 7-11 | remote-operations, run/states | yes | yes, with AWS-Lg8-004 (stage list). "Planned and finished" is on the page for a no-change plan. |
| 12-18 | remote-operations, run/ui, run/api, run/cli | yes | yes. "You must manually trigger an initial run", `.tar.gz`, and "Remote terraform apply is for workspaces without a linked VCS repository" are exact. |
| 19-26 | remote-operations, run/ui | yes | yes, with AWS-Lg8-003 (PR speculative plans are conditional). Fork rule exact (the page adds a Terraform Enterprise exception, not needed). |
| 27-32 | remote-operations, run/cli | yes | yes, with AWS-Lg8-006. v1.6.0 is on both pages. Import quote exact. |
| 33-34 | workspaces, cli | yes | yes: "remote operations enabled (the default)". See AWS-Lg8-002 for the execution-mode default. |
| 36-41 | teams, permissions | yes | yes. Team management "Essentials, Standard, and Premium" is a Note on the teams page, quoted exactly. "more than five users" is on the overview. "does not override the Write role" exact. |
| 42-47 | permissions/workspace | yes | yes. Plan, Apply, Admin wording exact (run-access table and admin list). |
| 48-63 | policy-enforcement, manage-policy-sets, sentinel, opa, run/cli | yes | quotes exact; incomplete on hard mandatory: AWS-Lg8-001. "four imports" exact. OPA "If the array is empty ..." exact. Free edition "one policy set of up to five policies" exact. Stacks: AWS-Lg8-005. |
| 64-73 | run-tasks, cost-estimation | yes | yes. Four stages, advisory/mandatory, "most restrictive enforcement level", "Terraform version of 1.1.9 and later" (a Requirements bullet). Cost estimation "disables ... by default" and "extra run phase, between the plan and apply" exact. |
| 74-80 | workspaces/health | yes | yes. "Standard and Premium editions" is a Note; "Remote execution mode or Agent execution mode" is a requirements bullet. The page also requires Terraform 0.15.4+ (drift) or 1.3.0+ (drift plus continuous validation) and a successful latest run; the lesson omits these (fine). Local-mode statement: AWS-Lg8-008. |
| 81-84 | api-docs/audit-trails | yes | yes. "retains 14 days", "Standard and Premium editions" (a Note), "cannot be accessed with a user token or team token. You must access it with an organization token or an audit trail token" all exact. |
| 85-92 | private-registry, sentinel | yes | yes. |
| 93-110 | workspaces, projects | yes | yes. "exactly one project", rename but not delete, "Manage all Projects" exact. The projects tier is a Note at the top of the projects page, quoted exactly. |
| 111-125 | workspace settings, remote-operations | yes | quotes exact. Remote sentence is not verbatim: AWS-Lg8-007. Default: AWS-Lg8-002. "Agents are a paid feature" exact on remote-operations ("HCP Terraform agents are a paid feature"); no edition named there and none in the lesson (correct). |
| 126-145 | managing-variables, run-triggers | yes | yes. Variable-set scopes; precedence (workspace-specific beats variable sets; `-var`/`-var-file` beat both); "up to 20 source workspaces"; "requires admin access"; "do not auto-apply unless you enable the Auto-apply run triggers setting"; sensitive "write-only ... all users (including you)"; "stores variable descriptions in plain text". |
| 146-163 | workspaces/state, workspaces | yes | yes. Remote state sharing off by default; three share options; `tfe_outputs` more secure and ignores access controls; lock keeps runs Pending. |
| 164-182 | run/cli, cli/cloud, terraform-cloud | yes | yes. `cloud` v1.1 is a Note on run/cli and is the only floor stated; none is stated for `project`, tags-as-map or `TF_CLOUD_*`. |
| 183-198 | terraform-cloud, cli/cloud/settings | yes | yes. Env vars apply only when the argument is omitted ("the configuration takes precedence"); empty `cloud` block; `TF_WORKSPACE` does not create a workspace; migration prompts; `backend "remote"` swap; no `prefix`. Wording point: AWS-Lg8-009. |
| 199-218 | vcs, run/ui, login | yes | yes. |

## Prose with no claim row (checked)

- "Remote ... is the mode that enables Sentinel, cost estimation and notifications": on the workspace settings page, but the lesson's sentence drops "and version control integration" and the "such as" frame. AWS-Lg8-007.
- "Agents are a paid feature": row 124 exists; exact.
- Local-mode health inference (8b): a direct consequence of the requirement bullet. Fine (AWS-Lg8-008).
- Run stages list: exact quote; context in AWS-Lg8-004.
- Sentinel imports `tfplan`, `tfconfig`, `tfstate`, `tfrun`: all four on the Sentinel page.
- OPA levels and override rule: exact. Hard-mandatory override rule: incomplete (AWS-Lg8-001).
- "The same workspace can use several sets in different frameworks": on manage-policy-sets ("you can apply multiple policy sets using different frameworks to the same workspace or Stack"). Accurate.
- "It holds the configuration (from a linked repository or uploaded), the variable values and the state": workspaces page table. Accurate.
- "HCP Terraform keeps the state" in Local mode: "Your workspace still stores your state". Accurate.
- "Do not mix up what starts a run with where it executes": the lesson's own framing; consistent with the pages.
- No prices appear anywhere. Tier names (Free, Essentials, Standard, Premium) match the docs.

## Findings

**AWS-Lg8-001 (Medium, 8b "Policy as code and enforcement levels", and Warnings bullet 5).** The lesson says hard mandatory "cannot be overridden by default" and the Warnings say "overrides exist for soft mandatory and OPA mandatory policies". The docs have a set-level switch that overrides even hard mandatory and takes precedence over the policy's own level: "Enabling this option lets users with the appropriate permissions, such as admins or team owners, override any failed policy checks in that set, even policies set to Hard mandatory. This override setting takes precedence over the individual policy's enforcement level." (option "This policy set can be overridden in the event of mandatory failures", manage-policy-sets). The lesson quotes only "Unless the set containing the policy is configured to allow overrides" and never explains it. A question keyed "hard mandatory can never be overridden" would be wrong.
- Fix: after the hard-mandatory bullet add: the set can enable "This policy set can be overridden in the event of mandatory failures", which lets users with the right permissions override "any failed policy checks in that set, even policies set to Hard mandatory"; this setting "takes precedence over the individual policy's enforcement level." Add a claim row (manage-policy-sets; quote "even policies set to Hard mandatory"). Reword Warnings bullet 5: advisory never stops a run; soft mandatory and OPA mandatory failures can be overridden; hard mandatory failures can be overridden only when the policy set allows overrides.
- Question guidance: key "hard mandatory is not overridable unless the policy set allows overrides"; never "hard mandatory can never be overridden".

**AWS-Lg8-002 (Medium, 8c "Execution mode" versus 8a and 8d).** 8a says remote operations are "the default", and 8d says a workspace's execution mode "defaults to remote", while 8c says the workspace default is "Project Default". The projects page adds an organization level that can be Local: "By default, a project uses the organization's execution mode, which is either Remote or Local, but you can override the organization execution mode in your project. Any workspaces created in the project after changing the project execution mode inherit the project default." "Defaults to Remote" is accurate only for a workspace created implicitly by `terraform init` (run/cli: "The execution mode defaults to "Remote,""). The lesson never mentions the organization level, so a "default execution mode" question has no single right answer from the lesson text.
- Fix: in 8c, after the Project Default bullet add: a project uses the organization's execution mode by default, "which is either Remote or Local", and workspaces created in a project "inherit the project default." In 8d change "Its execution mode defaults to remote" to "For a workspace that `terraform init` creates, the docs say the execution mode defaults to "Remote,"". In 8a qualify "(the default)" as the default for a workspace left on default settings. Add a claim row for the projects quote.
- Question guidance: do not make "Remote" the key to a generic "default execution mode" stem; use the `terraform init`-created wording or ask about inheritance (Project Default).

**AWS-Lg8-003 (Low, 8a "Speculative plans").** "pull requests start speculative plans" is unconditional. The VCS page adds: "Pull requests can only trigger runs in workspaces where automatic speculative plans are allowed." and a pull request "will only trigger speculative plans in workspaces that are connected to that pull request's destination branch."
- Fix: append "when the workspace allows automatic speculative plans and the pull request targets the linked branch" (quote "Pull requests can only trigger runs in workspaces where automatic speculative plans are allowed", 14 words; run/ui). Questions must not say every pull request always starts a plan.

**AWS-Lg8-004 (Low, 8a "Remote runs").** The stage list "pending, plan, cost estimation, policy check, apply, and completion" reads as if every run passes every stage. Run-states says the policy stage "only occurs if Sentinel policies are enabled", cost estimation only if enabled, and a no-change plan reaches "Planned and Finished" when "neither cost estimation nor Sentinel policy checks will be done".
- Fix: after the list add "Cost estimation and policy check stages occur only when those features are enabled." (row: run/states "This stage only occurs if Sentinel policies are enabled"). Keep questions on the stage order, not on "every run has a policy check".

**AWS-Lg8-005 (Low, 8b "Policy as code").** The policy-set quote lists "specific projects, workspaces, and Stacks", but the overview says "Sentinel and OPA policy sets only support workspaces" (Terraform policy, the beta framework, supports Stacks). The lesson teaches Sentinel and OPA, so "Stacks" misleads.
- Fix: add after the quote: Stacks apply only to the beta Terraform policy framework, because "Sentinel and OPA policy sets only support workspaces." (policy-enforcement overview). Questions must not use Stacks for Sentinel or OPA.

**AWS-Lg8-006 (Low, 8a saved plans).** "`terraform plan -out` ... works against HCP Terraform too" omits the same limit as remote apply: "Like remote terraform apply, remote saved plans are for workspaces without a linked VCS repository. Saved plans require at least Terraform CLI v1.6.0." (run/cli).
- Fix: add the first sentence (quote "remote saved plans are for workspaces without a linked VCS repository", 11 words). The v1.6.0 floor is safe to ask; do not imply saved plans work in VCS-linked workspaces.

**AWS-Lg8-007 (Low, 8c Remote bullet).** "This is the mode that enables Sentinel, cost estimation and notifications" is the lesson's wording with no claim row. The settings page says "enables advanced features, such as Sentinel policy enforcement, cost estimation, notifications, and version control integration." The lesson's version drops the last item and reads as exhaustive.
- Fix: replace with that quote (14 words) and add a row (workspaces/settings).

**AWS-Lg8-008 (Low, 8b health assessments).** Local-mode sentence is a correct consequence of the requirement; keep. Optionally add "(this follows from the requirement; the docs do not name Local mode)". Question guidance: key "Remote or Agent execution mode is required"; do not write "the docs say Local mode is unsupported".

**AWS-Lg8-009 (Low, 8d "Initializing and migrating state").** The sentences on unique names and "requires all workspaces to have a name" are joined with "So" in the opposite order from the page. The page: "HCP Terraform requires all workspaces to have a name. As a result, Terraform may also prompt you to rename your workspaces during the migration." It then says CLI workspaces (production, staging) are renamed because HCP Terraform workspaces "must have unique names within the HCP Terraform organization."
- Fix: reword: HCP Terraform requires all workspaces to have a name, so Terraform may prompt you to rename them during migration; CLI workspaces such as production and staging are renamed because HCP Terraform workspace names "must have unique names within the HCP Terraform organization." No new row needed.

**AWS-Lg8-010 (Low, density).** 4,495 words and about 200 quoted spans; 8b (1,196 words, 62 quotes) and 8c (1,218 words, 60 quotes) are heaviest. Coverage is not the risk (each objective has well over five facts); density is. Optional: trim sub-detail used for at most a spare question (audit-trail credential, OAuth/webhook detail, `.terraformignore`). Keep the four discriminator lines and exam tips as the study anchor.

## Coverage and readiness

- 8a: remote operations on disposable VMs; plan-then-approve default; run queue; three workflows; remote apply limited to non-VCS workspaces; speculative plans (three triggers, fork rule); saved plans v1.6.0; `import` not run remotely. 8 distinct facts.
- 8b: teams (additive, owners team, Free versus paid); Plan versus Write; Sentinel versus OPA (imports, empty array, one framework per set); levels; run tasks (4 stages, levels, 1.1.9); cost estimation; health assessments (tier, mode, drift versus validation); audit trails (14 days, tier, token); private registry. 9+ facts.
- 8c: HCP versus CLI workspaces; small-workspace advice; projects; execution modes; variables and variable sets; run triggers (20, admin, auto-apply); remote state sharing and `tfe_outputs`; workspace lock. 10+ facts.
- 8d: `terraform login`; `cloud` block (organization, `name` xor `tags`, `project`, `hostname`, v1.1); `TF_CLOUD_*` and `TF_WORKSPACE`; init workspace creation and migration; VCS. 9+ facts.
- Extras: q-tf-004-8-extra-00 and -04 are 8a; -01 and -05 are 8b; -02 and -06 are 8c; -03 and -07 are 8d. That gives 5 questions per objective, 20 in all, matching the writer's `drillIds`.
- Exam tips: present for all four and discriminating. Format matches the established pattern; no tables, links, numbered lists or single-asterisk italics found.
- Cross-lesson: g6 6b/6c (queued locking; `cloud` versus `backend`; one `cloud` block; no named values) are built on, not contradicted. g1 1b (private registry), g4 (sensitive is display-only; `terraform_remote_state` reads root outputs), g5 (`app.terraform.io/<NS>/<NAME>/<PROVIDER>`) and g6 6d (`-refresh-only`, `import`) agree with g8's cross-references.
- No prices. Tier claims are stated as the docs state them; none broader than its quote.
- No retired or renamed services introduced (Terraform Cloud is labelled once as the former name).

## Verdict

Two Medium findings (AWS-Lg8-001, AWS-Lg8-002), each with a doc-verified fix and quote above, plus eight Low items. All 219 quotes are verbatim; no stale or unquoted tier claim was found.

Lesson tf-g8: not yet

Overall: concerns
