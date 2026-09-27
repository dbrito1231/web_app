# lesson-tf-g1 / lesson-tf-g2 — Round 1 technical review (AWS role, HashiCorp docs as primary source)

## Rows verified (11 total, WebFetch on developer.hashicorp.com)

**tf-g1** (claim table rows, source: `/terraform/intro`, `/terraform/intro/vs/cloudformation`):
- Row 1 — "infrastructure as code tool that lets you build, change, and version..." — exact match on `/terraform/intro`.
- Row 3 — "Terraform configuration files are declarative, meaning that they describe the end state..." — exact match on `/terraform/intro`.
- Row 9 — "orchestrate an AWS and OpenStack cluster simultaneously..." — exact match on `/terraform/intro/vs/cloudformation`; confirms the claim (Terraform runs both clouds from one config), not a mere mention.
- Row 10 — "single unified syntax, instead of requiring operators to use independent and non-interoperable tools..." — exact match, same page; confirms the claim.
- Row 11 — "represent and manage the entire infrastructure with its supporting services, instead of only the subset..." — exact match, same page; confirms the claim.

**tf-g2**:
- Row 4 — `~> 1.0.4` example — exact match on `/terraform/language/expressions/version-constraints`.
- Row 8 — dependency lock file claim — **quote does not appear on the cited page.** See Finding AWS-Lg2-001.
- Row 13 — source-address format `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` — exact match on `/terraform/language/providers/requirements`.
- Row 15 — "Resources that begin with `aws_` use the default `aws` provider configuration..." — exact match on `/terraform/language/providers/configuration`.
- Row 16 — "provider block without an alias argument is the default configuration..." — exact match, same page.
- Row 19 — "record[s] the identity of that remote object against a particular resource instance" — present, `/terraform/language/state`; confirms the mapping claim, though verbatim quote has a tense mismatch (see Finding AWS-Lg2-002).
- Row 21/22 — "improve performance for large infrastructures," and default local file `terraform.tfstate` — both confirmed current (no deprecation notice as of the live page).

That is 11 rows spot-checked (5 in g1, 6 in g2), above the 8-row minimum, each checked for "asserts the claim" not just "mentions the topic."

## Findings

**AWS-Lg2-001 — Major — lesson-tf-g2.json, section tf.004.2a, claim-table row 8 / citation `cite-tf-g2-providers-lock`**
The quote "To ensure Terraform always installs the same provider versions for a given configuration, you can use Terraform CLI to create a dependency lock file and commit it to version control" is cited to `https://developer.hashicorp.com/terraform/cli/commands/providers/lock`. That page is the `terraform providers lock` subcommand reference; its own opening text is "The `terraform providers lock` adds new provider selection information to the dependency lock file without initializing the referenced providers..." — a different claim. The quoted sentence is actually the introduction of `https://developer.hashicorp.com/terraform/language/files/dependency-lock` (confirmed via search). Fix: change the URL in claim-table row 8 and in citation file `cite-tf-g2-providers-lock.json` to `https://developer.hashicorp.com/terraform/language/files/dependency-lock`, and rename the citation id if the naming convention expects the id to match the page (e.g. `cite-tf-g2-dependency-lock`). The lesson prose claim itself is accurate; only the citation is wrong.

**AWS-Lg2-002 — Low — lesson-tf-g2.json, section tf.004.2d, claim-table row 19**
Quote is given as "record the identity of that remote object against a particular resource instance." The actual doc sentence is "...it **records** the identity of that remote object against a particular resource instance..." (present tense, embedded mid-sentence: "When Terraform creates a remote object in response to a change of configuration, it records..."). Not a substantive error, but the claim-table rule asks for a verbatim quote; fix by changing "record" to "records" in the claim table (the lesson's own prose paraphrases correctly and is not affected).

No other misquotes, no version-stated-as-current-but-stale claims, and no deprecated/renamed terms found in either lesson. `required_providers`, provider installation, the dependency lock file, and the constraint operators (`=`, `!=`, `>`, `>=`, `<`, `<=`, `~>`) are all stated in line with the current docs, with no operator or syntax that has been renamed or removed.

## g1 sourcing judgment (11 rows on 2 pages)

Two pages can carry all 11 rows **as currently written**, because every row already has its own verbatim, on-topic quote and group 1 is explicitly the overview/conceptual tier of the objective list (what IaC is, why it helps, that Terraform is multi-cloud) rather than the mechanism tier that groups 2–4 cover in depth. I checked five of the eleven rows directly and all five both resolve and assert (not merely mention) the attached claim.

That said, two rows are the weakest links and are the ones I'd single out if this lesson is revisited later for a deeper technical pass:
- **Row 5** (resource graph / parallel creation of non-dependent resources) — `/terraform/intro` states this as a bullet-point benefit; HashiCorp's own dependency-graph mechanics live on a separate internals page. For a group-1 "why Terraform" claim this is fine, but it is the most mechanism-like claim resting on the marketing-toned intro page.
- **Row 7** (HCP Terraform collaboration) — same pattern: a specific product claim resting on an intro paragraph rather than an HCP Terraform product page. Fine for this lesson's tier, but the row a technical reviewer would want re-sourced first if group 8 (which does cover HCP Terraform) needs a shared citation later.
Rows 1–4, 6, 8–11 are squarely within what their two source pages are written to assert, so I would not require new citations for them.

## Objective and format coverage

All seven group-1/group-2 objectives (`tf.004.1a/1b/1c`, `tf.004.2a/2b/2c/2d`) have their own `###` section, in id order, each ending with `**Exam tip:**`. Both lessons keep the single `##` title and end with the standard `### Warnings` section — both are the established pattern per RULES.md, not defects.

`required_providers` vs `provider` block (2b) and single-provider vs same-provider-twice-via-alias (2c) are each given an explicit, applicable rule ("if the stem is about which version Terraform is allowed to download, that is `required_providers`; if it's about a runtime setting for an already-downloaded plugin, that is the `provider` block" / "two different platforms = two ordinary declarations; the same platform twice = `alias`"), not just a true sentence a student would have to infer from. This resolves the confusion the task asked me to check.

Teach-before-test readiness: both lessons state the key fact and the contrasting wrong-answer fact for every discriminator, sufficient to support MC/MR questions once written.

Lesson tf-g1: approve for question writing
Lesson tf-g2: not yet — hold for AWS-Lg2-001 (citation URL wrong; lesson text itself is fine, no rewrite needed) and AWS-Lg2-002 (verbatim-quote nit) to be fixed in the citation file / claim table.

Overall: concerns

## Round 2

### (a) Own findings: Gone / not gone

- **AWS-Lg2-001 — Gone.** I had named the wrong replacement URL (`/terraform/language/files/dependency-lock`); the coordinator and Teacher were right that the sentence lives on `/terraform/language/providers/requirements`, "Version Constraints" section. Re-fetched that page directly and confirmed the exact sentence is present verbatim, under that heading. `cite-tf-g2-providers-lock.json` has been deleted, claim-table row 8 and both lesson-tf-g2 and the question files now cite `cite-tf-g2-provider-requirements`, whose `url` is `https://developer.hashicorp.com/terraform/language/providers/requirements`. Confirmed correct.
- **AWS-Lg2-002 — Gone.** The updated claim table (row 19 in `lesson-tf-g2-impl.md`) now reads "records the identity of that remote object against a particular resource instance," matching the doc's tense exactly. The lesson `bodyMarkdown` itself still smooths this to "record" for grammatical fit inside its own sentence ("Terraform uses state to \"record the identity...\""), but RULES.md has reviewers verify quote accuracy against the claim table, not the prose, so this closes.

### (b) Second-role check on TEACHER-Lg2-001/-002/-003

- **TEACHER-Lg2-001 — Gone (concur).** Teacher named the correct page from the start; verified above.
- **TEACHER-Lg2-002 — Gone (concur).** `lesson-tf-g2.json`, section 2d, now reads "(A workspace here is the working directory's current state environment; named workspaces that let one configuration manage several separate states are covered in a later objective.)" immediately after first use of "workspace." Matches the requested fix.
- **TEACHER-Lg2-003 — Gone (concur).** Section 2c now reads "(a module is a reusable, packaged Terraform configuration, covered in full in group 5)" at first use of "module." Matches the requested fix.

### (c)/(d) Question review — all 21, plus every number/literal in every key

**g2 (12 questions) — no defects found.** Checked every syntax literal named in the coordinator's list against current HashiCorp docs, character by character:
- `2a-mc`: `~> 2.4.0` allows patch releases (e.g. `2.4.1`) but blocks `2.5.0` — matches the right-most-component rule exactly; `>= 2.4.0` / `= 2.4.0` / `!= 2.5.0` distractor behavior is each correctly characterized.
- `2a-mr`: `!= 3.2.0` (excludes only that version) and `~> 3.2.0` (allows `3.2.1`/`3.2.9`, blocks `3.3.0`) are the correct keys; the three wrong statements about `>=`, `=`, `<=` are each accurately wrong.
- `2b-mr`: omitted-`source` default `registry.terraform.io/hashicorp/<LOCAL NAME>` and address structure `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` both confirmed verbatim on `/terraform/language/providers/requirements`.
- `2c-mr` key d: re-fetched `/terraform/language/providers/requirements` directly for the naming-collision guidance — HashiCorp's own example is "combining each provider's namespace with its type name to produce compound local names with a dash," with `hashicorp-http` / `mycorp-http` as its own worked example. This is current documented guidance, not folklore; key d is accurate.
- `2c-mc` / `2c-mc2`: `alias`, `provider = aws.<alias>`, and default-configuration-by-resource-type-ownership are all stated correctly and match `/terraform/language/providers/configuration`.
- `2d-mc2`: local state file `terraform.tfstate` in the working directory absent a remote backend — confirmed current default, no deprecation notice on the live docs page.
- No claim in any g2 question is true only of a past Terraform version without saying so; nothing else deprecated or renamed surfaced.

**g1 (9 questions) — one new finding.**

**AWS-Qg1-001 — Major — `content/questions/q-tf-004-1b-mc.json`, choice b (and its clause in the rationale).** Choice b claims "A cloud vendor's own native template tool that provisions every resource strictly in the order it is listed in the template, one at a time," and the rationale calls this "declarative but still serial." This is factually wrong for the real tool this evokes: AWS's own CloudFormation documentation states CloudFormation "creates, updates, and deletes resources in parallel to the extent possible, and automatically determines which resources in a template can be parallelized and which have dependencies that require other operations to finish first" — the same graph-based parallel/serial split Terraform uses, not strict listed-order, one-at-a-time execution. (Verified via AWS's `DependsOn` documentation and the CloudFormation parallel-stack-creation announcement.) As written, the distractor is not "a real option that meets every requirement but one" (RULES.md) — it invents an inaccurate limitation for a real tool rather than using the tool's actual, defensible limitation. It does not change the correct answer (c, the resource graph, is still uniquely correct), but a candidate who knows CloudFormation's real behavior could reasonably contest choice b's premise.
  - **Doc-verified fix:** Rewrite choice b to something a candidate cannot factually dispute. Two doc-supported options: (1) drop the vendor-tool premise and instead describe a practice with no dependency analysis at all, e.g. "A checklist of manual console steps followed in the same fixed sequence every time, with no way to know which steps have no dependency on each other" (distinct from choice a's scripted/ordered-CLI case); or (2) keep a native-tool distractor but make its flaw the true, doc-supported one from objective 1c instead of a parallelism claim — but that would duplicate 1c's discriminator inside a 1b question, so option (1) is the cleaner fix. Either way, remove "strictly... one at a time" and "declarative but still serial" from the choice/rationale text since both are false of CloudFormation's actual, documented default behavior.

No other new issues surfaced in the remaining 8 g1 questions (1a-mc, 1a-mc2, 1a-mr, 1b-mc2, 1b-mr, 1c-mc, 1c-mc2, 1c-mr) — each distractor's stated limitation (script running in fixed order, golden image being opaque/undiffable, config-management tool acting only on already-provisioned servers, one-laptop/no-review-gate practices, CloudFormation's engine understanding only one vendor's resources) is accurate and doc-supported.

### Trimmed quotes

Re-checked every claim-table quote in both updated impl reports by word count: all rows in `lesson-tf-g1-impl.md` (20 rows) and `lesson-tf-g2-impl.md` (22 rows) are now ≤20 words, with the longest at exactly 20 (g1 row 9). Spot-read each trimmed quote against its full sentence on the live doc page for the rows checked in this round (g2 rows 2, 14, 19) and in round 1 (g1 rows 1, 3, 9–11; g2 rows 4, 8, 13, 15, 16, 22) — every trim still asserts its attached claim rather than merely gesturing at the topic; none was cut short of its verb or its key qualifier.

### Version sensitivity

No claim in either lesson or in any of the 21 questions is stated as current but is actually version-specific or stale; the `~>`/`>=`/`=`/`!=` operator semantics, `required_providers` nesting, provider source-address structure, and the local `terraform.tfstate` default are all current on the live docs with no deprecation notice. No newly-deprecated or newly-renamed term surfaced beyond what round 1 already covered.

### Round 2 follow-up (commit 733b1a4)

- **AWS-Qg1-001 — Gone.** `q-tf-004-1b-mc` choice b now reads "Split the 40 resources across several scripts that run at the same time, with an engineer deciding which resources go in which script." — a real, true practice with no claim about any tool's internals, so the CloudFormation-serial misstatement is removed entirely.
- **Rationale accuracy — confirmed for all four choices.** a: fixed-order script is serial by construction (unchanged, accurate). b: "does produce parallelism, but a person has to decide the split, which is the hand-ordering the team wants to avoid" — correctly states the new choice is a real parallel practice that still fails the stem's specific "without anyone hand-ordering" requirement. c (key): resource graph, unchanged, accurate. d: config-management tool only converges already-existing servers, unchanged, accurate.
- **Nothing else broke.** Stem, choices a/c/d, `correctAnswerIds`, `citationIds`, `reviewedOn`, and `mcpStatus` are all unchanged from the version I already cleared; only choice b's text and its clause in the rationale changed.
- **TEACHER-Qg2-001 — confirmed, concur Gone.** Claim-table row 8 now reads "To ensure Terraform always installs the same provider versions... create a dependency lock file and commit it to version control" (20 words). The elision keeps "To ensure... [outcome], ... create a dependency lock file" intact, so it still asserts the causal claim — a committed lock file is what makes the identical install happen — not a bare "Terraform always does this" assertion. This matches the live doc sentence's structure with only the linking clause ("for a given configuration, you can use Terraform CLI to") removed. Agrees with the Teacher's finding; over-trim risk is resolved.

Noted for g3–g8: will check tool-behavior claims inside distractors, not just keys, given this defect's origin (a real-tool swap that introduced an unverified behavioral claim).

Task tf-g1: close
Task tf-g2: close

Overall: approve

### Round 2 follow-up 2 (commit d26850c) — two replaced g2 distractors

1. **`terraform init -upgrade` claim — accurate.** Re-fetched `/terraform/cli/commands/init`: "Upgrade all previously-selected plugins to the newest version that complies with the configuration's version constraints. This will cause Terraform to ignore any selections recorded in the dependency lock file..." `q-tf-004-2a-mc2` choice b's claim (ignores the lock file, installs newest matching constraint) is exactly this, not a narrower or different behavior.
2. **Unique-local-name claim — accurate, and the failure is the local name, not `source`.** Re-fetched `/terraform/language/providers/requirements`: "Local names are module-specific... Local names must be unique per-module." `q-tf-004-2c-mr` choice a's claim (distinct `source` addresses under the same local name still collide) is correctly attributed to the local-name rule, not to anything about `source`.
3. **Rationales accurate for all choices, both questions.** `2a-mc2`: a (tight `~>` is still a range), b (now correctly explains `-upgrade` ignores the lock file), c (manual copy, unverified), d (key, lock file) — all correct. `2c-mr`: a (now correctly explains the local name is still shared regardless of `source`), b (deleting `required_providers` doesn't fix a naming collision), c (`alias` distinguishes configs of one provider, not two providers), d/e (keys) — all correct.
4. **No duplicate choices.** `2a-mc2`'s four mechanisms (tight `~>`, `-upgrade`, manual copy, lock file) are all distinct; `2c-mr`'s five (same-local-name-different-source, deleting `required_providers`, shared `alias`, compound name, one-entry-per-provider) are all distinct.
5. **Teach-before-test: one gap found.** `q-tf-004-2c-mr` choice a is adequately taught — lesson tf-g2's 2c naming-collision paragraph teaches the fix as renaming the local name itself (the compound-name mechanism), which is enough for a student to see why changing only `source` under a shared local name fails. **`q-tf-004-2a-mc2` choice b is not taught.** I grepped `lesson-tf-g2.json` for "upgrade" — zero occurrences. The lesson's 2a section teaches that `terraform init` "will not silently drift to an incompatible version, because the constraint (and the lock file below) both hold it back," but never states that `-upgrade` is the flag that explicitly overrides the lock file. This is a real, doc-verified claim the question needs but the lesson does not teach — the same failure mode as the CloudFormation distractor (real, but untaught), just with a true rather than false claim this time.

**AWS-Qg2-001 — Moderate — lesson-tf-g2.json, section tf.004.2a; `q-tf-004-2a-mc2` choice b.** Add one doc-verified sentence to the 2a section covering `-upgrade`, e.g.: "Running `terraform init -upgrade` explicitly ignores any selections recorded in the dependency lock file and installs the newest version that still matches the configured constraint, which is why `-upgrade` does not give a reproducible, byte-for-byte identical build across machines." (Paraphrase of `/terraform/cli/commands/init`'s own "Upgrade all previously-selected plugins to the newest version that complies with the configuration's version constraints. This will cause Terraform to ignore any selections recorded in the dependency lock file..." — cite `cite-tf-g2-provider-requirements` or add a new `init`-page citation.) Once added, this closes.

Task tf-g2: not yet — hold for AWS-Qg2-001 (lesson needs one sentence on `-upgrade` vs. the lock file; both distractor claims themselves are accurate and nothing else broke).

### Round 2 follow-up 3 (commit 7707035) — AWS-Qg2-001 fix

1. **Gone.** Lesson 2a now reads, right after the lock-file paragraph: "One command-line option deliberately overrides that guarantee: running `terraform init -upgrade` makes Terraform \"ignore any selections recorded in the dependency lock file\" and install the newest version that still complies with the configuration's version constraints, so two machines running it on different days can still end up with different builds." This teaches the exact fact `q-tf-004-2a-mc2` choice b rests on.
2. **Accurate and verbatim.** Re-fetched `/terraform/cli/commands/init`: "Upgrade all previously-selected plugins to the newest version that complies with the configuration's version constraints. This will cause Terraform to ignore any selections recorded in the dependency lock file, and to take the newest available version matching the configured version constraints." The embedded quote "ignore any selections recorded in the dependency lock file" is verbatim, and the surrounding paraphrase ("install the newest version that still complies with the configuration's version constraints") matches the doc's own paraphrase of the same sentence.
3. **Row 8b's strength matches.** The claim-table quote is the same clause used in the lesson body, asserting only that `-upgrade` ignores the lock file's recorded selections — not a stronger claim (e.g., that it ignores version constraints too, which it does not) and not a weaker one (e.g., merely that it "may check for updates").
4. **Nothing contradicted or duplicated.** The new sentence is additive: the preceding sentence about plain `terraform init` not silently drifting still holds (that claim is about `init` without `-upgrade`), and `-upgrade` is presented as the deliberate exception, not a contradiction. The citation `cite-tf-g2-init-upgrade` is new and not a duplicate of any existing citation; `citationIds` on the lesson includes it exactly once.

Task tf-g2: close

Overall: approve
