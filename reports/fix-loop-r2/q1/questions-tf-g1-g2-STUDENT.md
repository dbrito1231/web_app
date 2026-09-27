# Terraform Associate drills — tf-g1 and tf-g2

## Drill g1 (9 questions) — committed answers

| Q | Answer | Reason |
|---|---|---|
| Q1 | a | Versioned file stating end state, applied the same way every time = diffable/re-runnable IaC; b/c/d each lack something to read/diff or lack state tracking. |
| Q2 | b | An execution plan listing every add/change/delete with reviewer sign-off is the plan stage's exact purpose. |
| Q3 | b, c | Version-controlled + always-used config (IaC half) and a file stating end state without ordered steps (declarative half) are the two proofs. |
| Q4 | c | Dependency graph starts a resource as soon as its own prerequisites finish — automatic, not hand-ordered. |
| Q5 | d | Tracked state consulted before plan, compared against config, is what catches drift; cron/dashboard/backup don't compare state to config. |
| Q6 | a, d | PR-gated version control = second set of eyes; shared-location state record = anyone can check without asking the last editor. |
| Q7 | a | One plugin-model tool, one config language/workflow calling each vendor's API — b/d keep two toolchains. |
| Q8 | b | Engine calling a plugin for any API-having platform (cloud, on-prem, non-cloud SaaS) is what allows DNS + compute in one tool. |
| Q9 | c, e | Declaring an on-prem provider alongside a cloud provider in one config/apply cycle, and the provider model routing to the right plugin per resource block. |

No guesses flagged — answered from direct knowledge of Terraform's IaC/provider model on every item.

### g1 marking (opened answer key after full commit above)

Key: Q1 a · Q2 b · Q3 b,c · Q4 c · Q5 d · Q6 a,d · Q7 a · Q8 b · Q9 c,e

**Score: 9/9.** Every answer matched the key exactly.

---

## Drill g2 (12 questions) — committed answers

| Q | Answer | Reason |
|---|---|---|
| Q1 | c | `~> 2.4.0` allows only the right-most (patch) component to increment, blocking a minor jump to 2.5.0. |
| Q2 | d | Only a committed lock file records the exact version + checksum; a `~>` range, same-day installs, or manual copying don't guarantee it long-term. |
| Q3 | b, e | `!=3.2.0` excludes exactly that version; `~>3.2.0` allows 3.2.1/3.2.9 but not 3.3.0. (`>=` allows newer too; `=` is exact-only; `<=` includes 3.2.0 itself.) |
| Q4 | a | Region is a runtime setting that belongs in the `provider` block, not `required_providers`. |
| Q5 | b | The `aws` provider itself defines `aws_instance`; Terraform core has no built-in resource catalog. |
| Q6 | a, c | No `source` → default `registry.terraform.io/hashicorp/<LOCAL NAME>`; address format `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` with hostname optional. |
| Q7 | c | A second same-provider config for a second Region needs an `alias`, referenced via `provider = aws.<alias>`. |
| Q8 | a | With no alias, each resource type routes to its own type's provider default config automatically. |
| Q9 | d, e | Compound namespace-type local name resolves the naming collision; `required_providers` still needs two separate entries (one per provider) regardless of naming. |
| Q10 | a | State's mapping ties a resource block to the already-created real object, preventing a duplicate create. |
| Q11 | b | Default state lives in local `terraform.tfstate`, separate from `.tf` files, absent a remote backend. |
| Q12 | a, b | Mapping (avoid duplicate creation) and metadata/dependency tracking are state's two jobs described here; c/d/e are fabricated. |

No guesses flagged here either — every answer followed directly from the lesson's stated mechanisms (version-constraint operators, lock file, provider vs required_providers split, alias mechanism, state's three purposes).

### g2 marking (opened answer key after full commit above, only after g1 fully marked)

Key: Q1 c · Q2 d · Q3 b,e · Q4 a · Q5 b · Q6 a,c · Q7 c · Q8 a · Q9 d,e · Q10 a · Q11 b · Q12 a,b

**Score: 12/12.** Every answer matched the key exactly.

---

## Fairness judgement

No question was answered wrong, and no answer was flagged as a guess on either drill, so there is nothing in the "wrong or guessed" bucket to classify as fair/ambiguous/missing-requirement/duplicate-option/unfair. Both drills were answerable with full confidence directly from the lesson text and general Terraform knowledge — no stem required outside information, and I did not need to break a tie between two options on any item.

---

## Keyword-guessable vs structural counts (the actual point of this run)

Method: for every stem, I listed every choice sharing a distinctive word/phrase with the stem, then checked whether that same word also shows up in at least one *wrong* choice. If it appears only in the stem + the correct choice, it's a keyword-guessable defect. If it also appears in a wrong choice, or it's just the stem naming an object/tool/job it introduced into the scenario, it's structural (not a defect).

### g1 (9 questions)

**Keyword-guessable (defect): 0 of 9.** None found — no stem had a distinctive term that leaked into only the correct choice.

**Structural scenario references (not a defect): 4 of 9 — Q4, Q7, Q8, Q9.**
- Q4: "dependenc(y/ies)" appears in the stem's own scenario setup ("resources that have no dependencies on each other") before the correct choice ("dependency graph") reuses it — the stem introduced the concept itself, not a leaked hint.
- Q7: "configuration" appears in the stem, the correct choice, *and* wrong choice (c, "configuration management tool") — shared with a wrong choice, so not diagnostic.
- Q8: "cloud" appears in the stem, the correct choice, *and* wrong choice (a, "hardcoded list of cloud vendors") — same reason.
- Q9: "on-premises"/"cloud"/"configuration" all recur across the correct choice *and* multiple wrong choices (a, b) — the scenario's own vocabulary, not a giveaway.

### g2 (12 questions)

**Keyword-guessable (defect): 0 of 12.** None found.

**Structural scenario references (not a defect): 4 of 12 — Q4, Q5, Q6, Q9.**
- Q4: "region" appears in the stem, the correct choice (a), *and* two wrong choices (c, d both explicitly mention "region") — shared broadly, not a leaked hint.
- Q5: "aws_instance" appears in the stem, the correct choice (b), *and* wrong choice (c, "replace aws_instance with provider's own private syntax") — shared with a wrong choice.
- Q6: "local name" appears in the stem, the correct choice (a), *and* wrong choice (d, "local name ... cannot be reassigned") — shared with a wrong choice.
- Q9: "local name" / "local package name" appears in the stem, the correct choice (d), and a near-identical phrase in wrong choice (a, "local package name") — close enough in construction to count as shared, not exclusive to the key.

**Net result: 0/9 and 0/12 keyword-guessable defects.** The earlier flat count of "9" that couldn't tell defects from structural reuse is resolved here — in this run, every shared term I found either recurred in a wrong choice too or was the stem naming the very object the scenario was about, so nothing was actually guessable from vocabulary alone.

---

## Eliminable-on-sight distractors

Went looking for options dismissible purely because they're a tool doing a job it was never built for, or a practice no real team would use — *not* because I recalled the specific fact being tested.

**g1: none found.** Every distractor in g1 is a plausible-sounding but wrong practice that requires the actual lesson discriminator to rule out (e.g., Q4d's config-management tool converging settings on a schedule is a real tool doing a real job, just the wrong job for *provisioning* 40 new resources; Q9b's config-management tool for on-prem machines "that already physically exist" is likewise realistic-but-wrong, not a caricature). This suggests the rewrite removing g1's caricature distractors worked — I had to reason about each one, not dismiss it on sight.

**g2: two candidates.**
- Q2b — "every machine runs `terraform init` on the same calendar day so they all see the same latest release." No real team would rely on calendar-day coincidence for build reproducibility; this is dismissible on sight as an absurd mechanism, not a real (if wrong) practice.
- Q9a — "edit the second provider's local package name in its own source code so the two no longer collide." A consuming team generally can't (and wouldn't) edit a third-party provider's own source to fix a local naming collision in their configuration; eliminable on sight as outside what the actor in the scenario could even do, before considering Terraform-specific knowledge.

Everything else in both drills required actually knowing the material (version-constraint operators, alias semantics, provider vs required_providers, state's three purposes) rather than spotting an obviously-wrong tool.

---

## Summary

- g1: **9/9**. 0/9 keyword-guessable defects (Q4, Q7, Q8, Q9 are structural scenario reuse, not defects). 0 eliminable-on-sight distractors found — rewrite appears to have removed g1's caricatures.
- g2: **12/12**. 0/12 keyword-guessable defects (Q4, Q5, Q6, Q9 are structural scenario reuse, not defects). 2 eliminable-on-sight distractors found (Q2b calendar-day coincidence, Q9a editing a vendor's source code) — a residual caricature-style pair worth revisiting.
- No wrong answers and no guesses on either drill, so no fairness complaints (ambiguous/missing-requirement/duplicate-option) apply this round.
