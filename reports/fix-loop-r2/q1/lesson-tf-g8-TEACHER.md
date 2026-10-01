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
