# tf-g4 round-2 fix spec (Lead Dev, after both round-2 reports)

Sources: `questions-tf-g4-leaddev-precheck.md` (LD-*), `questions-tf-g4-TEACHER.md` (TEACHER-Qg4-*), the `## Round 2` section of `lesson-tf-g4-AWS.md` (AWS-Qg4-*). Every finding below is confirmed by at least two roles. Where the reviewers proposed different fixes, the choice and the reason are stated. The deciding test throughout: **the reason a distractor is wrong must be taught in this lesson**, and no replacement may rest on version-sensitive or untaught behaviour.

## Lesson edits (bodyMarkdown)

- **L1 (LD-Lg4-012, both agree):** in 4a, drop the first "but" of the doubled-but sentence.
- **L2 (AWS-Qg4-008, supports Q7):** in 4a's timing paragraph, add a doc-verified sentence that Terraform refreshes/re-reads data sources on each run. The AWS reviewer quotes `data-sources`: "By default, Terraform refreshes prior to creating a plan." Re-fetch it and verify it word for word, and confirm it refers to data sources (or state generally, including data sources) before using it. Add a claim row. The citation `cite-tf-g4-data-sources` exists already.
- **L3 (TEACHER-Qg4-006 / AWS-Qg4-006, both agree):** in 4c, add one sentence stating that Terraform reads a variable's value from an environment variable only when the name has the `TF_VAR_` prefix (e.g. `TF_VAR_subnet_id`). Quote `https://developer.hashicorp.com/terraform/cli/config/environment-variables`. Add a new citation file `cite-tf-g4-env-vars.json` (copy the schema of an existing cite-tf-g4 file) and add it to `citationIds` and to a claim row.
- **L4 (Q5 support):** in 4f, add doc-verified sentences for the two other `lifecycle` arguments. `ignore_changes` tells Terraform to ignore changes to the listed attributes when planning updates, and the bare keyword `all` ignores every attribute. `replace_triggered_by` replaces the resource when any referenced resource or attribute changes. Quote the page that documents them (`language/block/resource` or `language/meta-arguments/lifecycle`, whichever the existing 4f rows cite; verify). Add claim rows.
- **L5 (LD-Lg4-009, both agree):** in 4g, change "Three condition mechanisms" so the count agrees with the later "fourth … of the four". "Four condition mechanisms" is fine, provided the next sentences still read correctly.
- **L6 (LD-Lg4-010, both agree; AWS wording):** in 4h, replace "There are three ways to get one: …" with wording that makes the `ephemeral` argument and the `ephemeral` block the two *sources*, and the write-only argument the *channel* that delivers an ephemeral value into a managed resource. Keep the rest of the paragraph consistent with that.
- **L7 (LD-Lg4-011):** in 4h, change "in the writer's own words" to "in the documentation's own words".

## Question edits

- **Q1 (LD-Qg4-001 / TEACHER-Qg4-001 / AWS-Qg4-001): remove every letter reference** from the rationales of `4a-mr 4b-mr 4c-mr 4d-mr 4e-mr 4f-mc 4f-mr 4g-mr 4h-mc2 4h-mr`, and name every option by its content. The Teacher's report gives replacement texts for nine of them; use them as a base, **but write each final rationale against the final choice text**, because Q2–Q9 change some of those choices. Every rationale must explain the key(s) and every distractor.
- **Q2 (`4d-mc`, LD-Qg4-002 / TEACHER-Qg4-002 / AWS-Qg4-002): replace choice "Sort the set alphabetically first; it becomes indexable".** Decision: **use the Teacher's version**, a string-key reference such as ``Reference the set element by a string key, such as `var.names["second"]` ``. It is wrong for a reason 4d teaches verbatim: sets have no secondary identifiers, and named labels belong to map/object. The AWS proposal (`values()` on a set) was rejected because `values()` is untaught, so a lesson-only reader would be guessing. Rewrite the rationale sentence to match.
- **Q3 (`4e-mc2`, LD-Qg4-004, all three agree):** change the key text "`can`, boolean-only" to a bare "`can`", so all four choices are bare function names. Do **not** lengthen the `try` distractor with an explanation (the AWS suggestion); an annotation on one choice is its own tell. If the batch check then complains about length, report it; do not pad.
- **Q4 (`4b-mc2`, LD-Qg4-007, all three agree): replace choices a and b.**
  - One becomes: "Terraform infers no ordering between the two resources, because a `name` value is plain data with no dependency implication". The Teacher and AWS proposed the same thing. It is wrong because 4b teaches that an attribute reference creates the implicit dependency.
  - The other becomes a **directionality** misconception: "Terraform infers that the instance is created before the instance profile, because the resource holding the reference is processed first". It is wrong because 4b/4f teach that the referenced resource is created first. The AWS "parallel unless depends_on" was rejected because it nearly duplicates the existing `depends_on` distractor. The Teacher's "shared provider meta-argument" was rejected because no practitioner holds it.
  - Keep both about as long as the others.
- **Q5 (`4f-mc2`, LD-Qg4-003, all three agree):** the four choices become genuine `lifecycle` arguments: `prevent_destroy = true` (keep), `ignore_changes = all` (correct syntax), ``replace_triggered_by = [aws_lb_target_group.<label>]`` (pick any valid address that matches the scenario), and `create_before_destroy = true` (key). Delete the `count = 2 (…)` choice. The AWS `create_before_destroy = false` was rejected, because a true/false pair of the same argument points at the key. All three distractors must be wrong for reasons taught after L4. Rationale explains each by content.
- **Q6 (`4h-mr` choice c, LD-Qg4-005 / TEACHER-Qg4-003 / AWS-Qg4-005): the current rationale is false against the current docs.** Decision: **use the AWS replacement**, a distractor claiming `nonsensitive()` converts the value to a different type the way `tostring()`/`tonumber()` would. It is wrong for a reason 4h teaches: it only lifts the redaction marking. The Teacher's flip ("raises an error") was rejected, because that was the documented behaviour in v1.2–v1.5, is untaught, and would make the question depend on the version. **Do not add any error-on-unmarked-value claim to the lesson.**
- **Q7 (`4h-mr` choice d, LD-Qg4-005 low):** "Vault-issued credentials are stored directly as Terraform language keywords…" is a caricature. Replace it with a real misconception about Vault that 4h's existing text refutes. For example, that using the Vault provider by itself keeps the issued credentials out of state with no further configuration; 4h says Vault is a source consumed through ephemeral/write-only mechanisms, not one of those mechanisms. Before using it, verify against the Vault provider or 4h's cited pages that the claim is actually false. If you cannot verify it, pick a different real misconception and say why. **Do not** use the negation of key e (static credentials last forever), because a negation pair points at the key.
- **Q8 (`4a-mr`, TEACHER-Qg4-009 duplicate facts + AWS-Qg4-008):** at present its two keys duplicate `4a-mc`'s key (read-only) and `4a-mc2`'s key (deferral). Retarget both keys onto facts no other 4a question keys:
  - (i) a `terraform_data` resource is a `resource` block that stores values/triggers operations without creating real infrastructure (lesson row 82);
  - (ii) Terraform re-reads data sources on each run, which L2 makes taught.
  - Distractors must be real misconceptions wrong for taught reasons; the existing "placeholder object in state" and "appears as add/change/destroy" are fine to keep.
  - **Rewrite the stem** to fit the new pair under the paraphrase rule. It no longer needs the "unresolved until apply" framing; remove it if it points at nothing.
  - Keep selectCount 2.
- **Q9 (`4d-mr` choice d, LD-Qg4-008 low; the reviewers split, Teacher replace / AWS keep):** decision: **replace**. A choice about what "Terraform's own documentation" calls things tests documentation wording, not behaviour. Use a real, taught misconception about list/set/map behaviour that does not duplicate `4d-mc`'s key (indexing a set). Do not rely on list↔tuple conversion unless 4d actually teaches it (verify with a regex first).
- **Q10 (`4c-mc2`):** no choice change. After L3 the `TF_VAR_` distractor is taught. Update the rationale only if it needs to point at the new sentence.

## Unchanged by decision

- `4a-mr` stem-echo advisory: classified **structural** by AWS; no waiver needed, and Q8 rewrites the stem anyway.
- Key-length rank observation: the reviewers **disagree** (Teacher: partly a real, cross-task tell; AWS: arithmetic consequence of the two caps). Neither blocks tf-g4. Goes to the user.

## Constraints for the fix pass

All RULES.md question rules still apply:
- no two stems share their first 6 words;
- MC keys stay spread a/b/c/d and MR key slots stay spread a–e (do not move keys unless a check fails);
- no giveaway words;
- the 15% distractor-type cap (add any new named construct, e.g. `replace_triggered_by`, `ignore_changes`, `TF_VAR`, to `TERMS` in `scripts/distractor_type_audit.py` only if Lead Dev asks — report it instead);
- claim table rows for every new fact, quotes of ≤20 words copied from a page fetched this turn;
- `reviewedOn`/`accessed` stay `2026-09-26`.
