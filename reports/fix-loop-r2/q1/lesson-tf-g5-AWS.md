# lesson-tf-g5 -- AWS (Terraform docs) review, round 1

## Method

- Fetched every cited HashiCorp page myself this turn with `curl -sL`, stripped to text with a small Python HTML-to-text script (scratchpad `awsg5.py`). No WebFetch.
- Ran a machine check of all 83 claim-table quotes against the page named in each row, then read the surrounding paragraph for each prose claim to judge whether the quote asserts exactly the claim.
- 72 of 83 quotes are verbatim after whitespace normalisation. The other 11 (rows 5, 6, 8, 27, 29, 39, 40, 41, 72, 73, 83) differ only by punctuation or markup (inline code ticks, `::`, `<...>`, the `|` in a config-model line), and the words are all present. None is a fabricated or reworded quote.
- Read the whole `bodyMarkdown` sentence by sentence and checked everything with no claim row against the pages (list under "Prose with no claim row").
- No AWS calls, no terraform commands, no git, no content edits. Pages read: `language/block/module`, `language/modules`, `language/modules/configuration`, `language/modules/sources` (extra), `language/block/variable`, `language/values/{variables,locals,outputs}`, `language/modules/develop{,/composition,/providers}`, `language/expressions/{references,version-constraints}`, `cli/commands/{get,init}`, `language/files/dependency-lock`.

## Rows verified (83 of 83 for verbatim; semantics judged on the rows below)

All 83 verbatim as described above. Exact-claim judgment (quote asserts the claim, no more and no less):

| Rows | Page | Verbatim | Exact claim? |
|---|---|---|---|
| 1, 3, 8, 9, 10, 11, 12 | block/module | yes | yes (source shapes; S3 must be an archive, extension list follows) |
| 13, 14 | block/module | yes | yes. `ref` and the HEAD default sit in the same Git parameter list. |
| 15-17 | block/module | yes | yes. `//` plus query-after-subdirectory plus "entire package" confirmed. |
| 18, 19, 44 | block/module | yes | yes (same paragraph: init after changing source; same source in two blocks needs unique labels) |
| 41 | block/module | yes (config-model line) | yes. `count number \| mutually exclusive with for_each` is the page's own model. |
| 61-63 | block/module | yes | yes. "Modules sourced from local file paths do not support version" and the reason clause are verbatim. |
| 65 | block/module | yes | yes. This is the Summary "Default:" field of the version argument. |
| 26, 27 | block/variable | yes | yes. Reserved list is exact. See AWS-Lg5-003 for how the prose frames it. |
| 28, 29 | values/locals | yes | yes ("but not in other modules. However, you can pass a local value to a child module as an argument") |
| 31 | values/outputs | yes | yes |
| 32, 33, 34 | develop, modules | yes | yes |
| 35, 36, 37 | develop/composition | yes | yes. Row 35 says "in most cases we strongly recommend"; the lesson drops "in most cases" (see AWS-Lg5-006). |
| 49 | modules/configuration | yes | yes, but it backs `init` only through the preceding step "Initialize the workspace to install the module". Acceptable. |
| 54, 55, 56 | cli/init | yes | yes ("Use -upgrade to override this behavior, updating all modules to the latest available source code") |
| 58, 59, 60 | develop/providers | yes | yes. Row 59 page continues "and so must always be passed explicitly using the providers map", matching the lesson. |
| 67-71 | version-constraints | yes | yes |
| 72-74 | version-constraints | yes | yes. The `=` row reads "`=`, no operator", so "`=` or no operator" is right. |
| 77, 78, 79 | dependency-lock | yes | yes. One sentence also says "Terraform will always select the newest available module version that meets the specified version constraints", which supports the lesson's "can move to a newer release". |
| 82 | modules/configuration | yes | yes, and it carries the "allowed by the version constraint" qualifier. |

## Findings

**AWS-Lg5-001 (Medium, the Lead Dev concern: Warnings bullet 2 and, by echo, the 5d exam tip).** The Warnings say that putting `version` on a local path or `git::` source "does not pin anything". No fetched page says that, and no page says the opposite either.
- What the docs say: `version` "only applies when installing modules from a registry"; "You can only use the version argument when the source argument points to a module listed in a registry"; "Modules sourced from local file paths do not support version because they're loaded from the same source repository and always share the same version as their caller" (module block page). The sources page adds "If you are using modules hosted in GitHub, BitBucket, or another Git repository, Terraform clones and uses the default branch referenced by HEAD. You can add the ref query parameter".
- I could not find a doc sentence that states what happens (error versus ignored) when `version` is put on a non-registry source. "Does not pin anything" implies Terraform silently ignores it. My recollection of Terraform's init code is that it returns an error ("Cannot apply a version constraint to module ... because it has a relative local path"), but I cannot confirm that from the docs and may not run terraform, so the lesson must not assert either behaviour.
- Fix: replace the bullet with doc-backed wording that makes no claim about the outcome. Exact text: "A `version` constraint belongs only on registry modules: the docs say the argument "only applies when installing modules from a registry" and that local-path modules "do not support version". Do not add it to a local path or a `git::` source. Pin a Git source with `?ref=` (a tag or commit) and a registry module with an exact `version`."
- Keep the 5d exam tip as is: it says only "the trap, because `version` is registry-only", which is accurate.
- Optional: if the Lead Dev wants the "it is an error" claim, it needs a doc source first; none of these pages gives one.

**AWS-Lg5-002 (Medium, 5d, git bullet).** "Pin with a tag, branch or commit using `?ref=`" calls a branch a pin. A branch moves, and the `ref` row only says it "Specifies a branch name, full or short SHA-1 hash, or tag name to clone." Pinning a version is done by a tag or a commit SHA. The 5d question writer could use "a branch pins" as a distractor or a key, so the lesson must be unambiguous.
- Fix: "Pin with a tag or a commit SHA using `?ref=`, for example `?ref=v1.2.0` (5a). A branch name is accepted by `ref` too, but a branch keeps moving as new commits arrive, so it is not a fixed version."
- The last clause is inference from what a branch is, not a doc quote. State it as plain explanation, not in quotation marks.

**AWS-Lg5-003 (Low, 5b, "Variable names are scoped per module").** "A variable name cannot collide with the arguments a `module` block itself understands: it can be 'any valid identifier except the following reserved names ...'". The reserved list includes `locals` and `lifecycle`, which are not `module` block arguments (the module block page lists source, version, count, depends_on, for_each, providers, ignore_nested_deprecations). The framing is slightly off, so a reader could conclude the list is the module-block argument list.
- Fix: "A variable name cannot be one of the reserved names: the label can be "any valid identifier except the following reserved names: source, version, providers, count, for_each, lifecycle, depends_on, or locals.""

**AWS-Lg5-004 (Low, 5b, locals paragraph).** "The docs add the one way around it:" is followed by the restriction quote ("You can access local values in the module where you define them, but not in other modules."). The way around is the next sentence ("you can pass a local value to a child module as an argument"). The attribution reads wrongly.
- Fix: "4c said a `locals` block is invisible outside its module. The docs state the rule: "You can access local values in the module where you define them, but not in other modules." They then give the one exception: "you can pass a local value to a child module as an argument.""

**AWS-Lg5-005 (Low, 5a, "Archives and object storage" bullet).** "an HTTP or HTTPS URL" is listed as an archive source. The module block page ("HTTP URLs") says an HTTP or HTTPS URL is used for vanity URLs, where "Terraform [sends] a GET request to the URL" and the service redirects; only an HTTPS URL "with a common file extension associated with an archive file format" is used directly as an archive. There is no claim row for this bullet.
- Fix: "an HTTP or HTTPS URL (a URL ending in an archive extension such as `.zip` is downloaded as an archive), `s3::` ... or `gcs::` ...". Add a claim row: https://developer.hashicorp.com/terraform/language/block/module, "If an HTTPS URL has a common file extension associated with an archive file format, Terraform bypasses the terraform-get=1 redirection" (18 words, verbatim).

**AWS-Lg5-006 (Low, 5c).** The lesson quotes the flat-tree advice as "we strongly recommend keeping the module tree flat, with only one level of child modules", but the page says "in most cases we strongly recommend". The quoted fragment is verbatim and a legitimate trim, but the lead-in "The docs recommend against deep nesting" is fine while a question that makes flatness an absolute would not be.
- Fix (optional): "In most cases the docs strongly recommend keeping the module tree flat, with only one level of child modules".

**AWS-Lg5-007 (Low, 5c exam tip and prose).** "into a `.terraform` subdirectory ... that is never committed". The source is the get page's "Don't commit this directory to your version control repository", which is an instruction, not a guarantee. "Never" is fine as advice but could turn an MR option "`.terraform` should be committed so teammates get the same modules" into a clean wrong answer only if the lesson says "should not be committed" (it does in the body). No change needed; flagged only so question writers do not make the claim "Terraform refuses to commit it".

**AWS-Lg5-008 (Low, 5c, unquoted inference).** "`terraform init -upgrade` ... updates 'all modules to the latest available source code'" in 5c, while 5d row 82 says "to the latest version allowed by the version constraint". Both are true. A reader of 5c alone could think `-upgrade` ignores `version`. 5d does fix this, but the 5c sentence stands alone in the lesson.
- Fix: append to the 5c sentence: ", within any `version` constraint on a registry module (5d)". Backed by row 82.

### Prose with no claim row (checked; result)

- "The shape of that string, not a separate setting, tells Terraform what kind of location it is": consistent with the block page (the `source` value carries the shape); fine, inference.
- "Sourcing happens at install time, not at plan time": consistent with `init`/`get` rows 49-50 and with the `init` page ("retrieves the source code for referenced modules"). Fine.
- Registry "three parts" and `hashicorp/consul/aws`: the block page's registry syntax is `<NAMESPACE>/<NAME>/<PROVIDER>` and the consul example is there. Fine. The page also mentions a generic hostname form (`localterraform.com/...`); the lesson only teaches `app.terraform.io`, which is acceptable.
- "Bitbucket uses `bitbucket.org/`" and "Mercurial uses `hg::`": rows 9, 10. Fine. Note for question writers: the `ref` parameter is stated for Git sources; Mercurial's source uses `#revision` in the docs, so do not ask "which sources accept `?ref=`" with Mercurial as a key.
- `servers = 5` inside `module "servers" { ... }`: the page example is exactly `module "servers" { source = "./app-cluster" servers = 5 }`. Fine.
- "which arrives in the child as an ordinary variable": inference. Correct, and the surrounding doc statement is that a local is passed as an argument, so the child declares a variable for it. Fine.
- "A parent and a child can each declare a variable called `region` without conflict": inference from "unique among all variables in the same module". Correct.
- "If the child never declares an output ..., the parent has no documented way to read it": hedged "documented", fine.
- "`count` and `for_each` work on a `module` block just as on a resource": the pages describe them as meta-arguments with the same meaning. No version floor is given in the docs fetched; modules `count`/`for_each` are old (0.13+), not an issue.
- "the label is also how you reach outputs": yes (row 45).
- "A `terraform get` ... about modules alone": the get page's one-line description. Fine.
- "Editing `source`, or the `version` of a registry module, always needs a fresh `init`": rows 18, 80, and the sources page "If you change the source argument or change the version argument for a module in a registry, you must rerun terraform init". Fine.
- 5d "`version = "6.0.1"` pins that single release": the example number is arbitrary; exact `=` semantics per row 69. Fine.
- "`~> 1.0.4` stays in the 1.0 line while `~> 1.1` stays in major version 1": follows from rows 72-74. Fine.
- `.terraform.lock.hcl` filename: the lock page title is "Dependency Lock File (.terraform.lock.hcl)". Fine.
- Warnings bullets 1, 3, 4: bullet 3 matches rows 77-79; bullet 4 uses "documented channels", matching the hedge in 5b; bullet 1 is the standard safety text.
- Heading separator: the `tf.004.5x ? Title` heading carries a U+FFFD character, but tf-g4 4c has the same character, so this is the established pattern and is not flagged as a g5 defect.

## Specific concern: `version` on local path or `git::`

See AWS-Lg5-001. The lesson's rule ("`version` is registry-only; Git pins with `?ref=`") is exactly what the docs say. Only the Warnings' consequence ("does not pin anything") goes beyond the docs. The docs give no error text, so use the wording above.

## Coverage, exam tips, teach-before-test

- Objectives 5a-5d each have one `###` section in id order, one `**Exam tip:**` line each, and one `###` Warnings section. The format is correct.
- Three distinct facts per objective: yes, and the lesson teaches each fact and the contrast that makes wrong options wrong.
  - 5a: address shapes; `ref` default and accepted values; `//` and re-init; S3 archive rule (spare). With AWS-Lg5-005, the HTTP/archive rule is a fourth.
  - 5b: how child versus root variables get values; locals scope plus the pass-as-argument exception; outputs and `module.` syntax; reserved/unique names (spare).
  - 5c: root versus child and flat composition; init/get/-upgrade/-update workflow and `.terraform`; count/for_each/labels and output shapes; provider inheritance (spare).
  - 5d: registry-only `version`; `~>` arithmetic; lock file does not cover modules; init-needed-after-version-change.
- Teach-before-test hazards for question writers (not defects in the lesson):
  - Do not make "Terraform errors on `version` with a local path" a key or a rationale sentence. The docs support only "do not support" and "only applies to registry modules".
  - The root module is the working directory's `.tf` files; a question stem should not treat a `terraform.tfvars` file as part of "the module" definition.
  - `depth` is not taught (the lesson's self-check says so). Do not use it.
  - `const = true` variables in `source`/`version` are not taught, deliberately. The docs are inconsistent here; stay away.
- Contradictions with tf-g4 4c: none. 4c says a local is invisible "even to a parent module that calls it" and "a parent module can never address it"; 5b says the local cannot be seen by the child but its value can be passed as an argument. These are consistent (a value is passed, the name is not). The `module.<CHILD_MODULE_NAME>.<OUTPUT_NAME>` quote matches. `TF_VAR_` is consistent with 4c.
- Citations: the 12 new `cite-tf-g5-*` files each carry one-sentence `note`s naming the claim; `accessed` and URLs match the claim table.

New retired/renamed/closed-service finds: none (no AWS service is named in this lesson).

Lesson tf-g5: approve for question writing
Overall: concerns

## Round 2

Method: re-fetched `language/block/module` and `language/modules/configuration` with `curl -sL` plus the HTML strip (no WebFetch). Read the current lesson (29230f0) and all 12 question files (f97c818, key = `correctAnswerIds`), the writer's fix pass, the Teacher's round-1 report and the Lead Dev pre-check. All 12 questions have `mcpStatus: verified`, `reviewedOn: 2026-09-26`, and non-empty citation ids. Every cited id maps to a page that backs the question's facts. No version-sensitive claim is made: the only numbers are `~>` arithmetic and sample versions.

### (a) My round-1 findings

- **AWS-Lg5-001 Gone.** The Warnings bullet now quotes "only applies when installing modules from a registry" and "do not support version", says "Do not add it", and makes no claim about error versus ignored.
- **AWS-Lg5-002 Gone.** The Git bullet reads "a tag or a commit SHA fixes the version, while a branch ... keeps moving".
- **AWS-Lg5-003 Gone.** The text now reads "A variable cannot use certain reserved names", followed by the quote.
- **AWS-Lg5-004 Gone.** The rule quote and the exception quote are separate sentences, each attributed correctly.
- **AWS-Lg5-005 Gone.** The bullet now says HTTPS URL with an archive extension and quotes the "terraform-get=1 redirection" sentence. I re-fetched it: verbatim, and the page continues "uses the contents of the referenced archive as the module source code".
- **AWS-Lg5-006 Gone.** "In most cases" was added.
- **AWS-Lg5-007 Gone.** No change was required, and the lesson says "Don't commit this directory".
- **AWS-Lg5-008 Gone.** "(within any `version` constraint on a registry module, 5d)" was added.

### (b) Second-role check of TEACHER-Lg5-001..007

- **001 Gone.** The text says "`TF_VAR_` names were covered in 4c; `-var` and `.tfvars` files are the other methods in that list", and "methods 4c covered" is gone (0 hits).
- **002 Gone.** Same fix as AWS-Lg5-003.
- **003 Gone.** The page sentence is "Terraform will always select the newest available module version that meets the specified version constraints". The lesson now scopes it to a first install, `init -upgrade` or `get -update`, which agrees with 5c's "will not change any already-installed modules".
- **004 Gone.** Same fix as AWS-Lg5-002.
- **005 Gone.** The vocabulary sentence (folder of `.tf` files, root, child, label) is in the intro.
- **006 Gone.** Ownership was followed; see (c) for the duplicate-fact check.
- **007 Gone.** The lesson reads "where they land ... And the rule".

### (c) Question review

For each question I report the key, each distractor as real? and taught?, and any defect. Syntax is valid everywhere: the `s3::https://s3-eu-west-1.amazonaws.com/...` form is the page's own form, and `//` and `?ref=` are as documented. No distractor is a working answer.

**5a-mc.** The key b is correct.
- a (single slash, `?ref=main`): real and taught (`//` marks the folder). It fails because the folder is not marked.
- c (`./network.git//modules/vpc`): real and taught (local path means files already on disk).
- d (`acme/network/aws//modules/vpc`): real and taught (registry shape).
- **AWS-Qg5-001 (Low).** The rationale says "the module is not published to a registry", but the stem never says so; it says only "internal Git server". Fix: add to the stem "The module is not published to any registry."

**5a-mc2.** The key d is correct.
- a (`//v2.3.0`): real and taught. I rule it acceptable: the lesson teaches that `//` marks a folder, and `github.com/acme/queue-module//v2.3.0` would name a folder `v2.3.0` that does not exist.
- b (`?ref=main`): real and taught. The stem says the unfinished change went to the primary branch, and a branch moves.
- c (explicit `git::` form): real and taught (default branch at HEAD).
- **AWS-Qg5-002 (Low-Medium, rationale wording).** "a slash-delimited tag name would be read as a folder path" is confusing, since `v2.3.0` is not slash-delimited. Fix: "A double slash marks a folder inside the package, not a revision, so `//v2.3.0` would be read as a folder named v2.3.0 inside the repository, which does not exist, instead of selecting the tag."
- **AWS-Qg5-003 (Low, giveaway).** c's tail "with nothing else changed" signals a wrong answer, close to the banned "without changing" family. Fix: "Rewrite the address in the explicit `git::https://github.com/acme/queue-module.git` form".

**5a-mr.** The keys b and e are correct.
- a (loose folder works like a packaged file): real and taught (the object must be an archive). It answers the packaging need.
- c (three-part shape with the bucket as namespace): real, a little contrived. Taught (registry shape, versus `s3::`). It answers the packaging need.
- d (".terraform directory deleted and recreated"): ruling below. It answers the edit need.
- Both needs are answered by at least one distractor each, so the MR-need rule is met.
- Echo: "edit" is in the stem and in key e but not in a distractor. It is structural, since it names the event, and the script passes.

**5b-mc.** The key a is correct.
- b (`-var`), c (`TF_VAR_replicas`) and d (tfvars in the child folder) are real and taught as root-module methods.
- d is the thinnest: it is true in Terraform (definition files are read from the working directory only), and the lesson lists `.tfvars` only among root-module methods. Acceptable.

**5b-mc2.** The key c is correct.
- a (direct `local.` use), b (a second `locals` block) and d (output read as `module.app.prefix`) are real and taught. d tests direction; the "in" direction is owned here and 5b-mr owns "out", so there is no duplication.

**5b-mr.** The keys a and d are correct.
- b (`module.network.aws_subnet.main.id`): real. It is an error in practice, and the lesson hedges with "no documented way". The rationale keeps that hedge, so that is fine.
- c (a `locals` block) and e (a `variable` default): real and taught.
- Note: b carries "because the child's resources are shared with its caller", a justification clause. It is the false claim itself, not a hint, so I do not require a change.
- Note: both keys mention "output" and no distractor does. The stem does not mention output, so this is not echo.

**5c-mc.** The key d is correct (row 47).
- a (one object per output) and b (a list) are the other two real shapes, and both are taught.
- **AWS-Qg5-004 (Low).** c ("a map keyed by output name, whose values are lists") is a caricature, as the writer flagged. The key is also the shortest choice. Fix: replace c with "A set of objects, one per module instance, with no keys to look instances up by". This is real (sets were taught in 4d), and it is wrong because the lesson says the value is a map. It also makes the choice lengths less revealing.

**5c-mc2.** The key a is correct. The ruling on LD-Qg5-005 and the replacement are in (e).

**5c-mr.** The keys c and e are correct.
- **AWS-Qg5-005 (Medium, giveaway).** The stem says "routine initialization keeps leaving the old copy in place". That sentence refutes choice a ("terraform init again with no extra flags") and tests reading rather than knowledge. Fix: delete the clause. Stem: "(Select TWO.) Tallgrass Insurance installed its modules last quarter. A registry module has since published a newer release that its `version` constraint allows. Which two actions would move the installed modules forward?"
- **AWS-Qg5-006 (Medium, teach-before-test).** d (`terraform apply` on an unchanged configuration) is real, but the lesson never says apply does not install or update modules. It teaches only "Sourcing happens at install time, not at plan time"; the "not apply" half is untaught. Lesson addition requested, in 5c after the workflow sentence: "Only `init` and `get` install or update module code: the docs list the steps as "Initialize the workspace to install the module." and then "Apply the configuration to provision the module's resources."" Both quotes are verbatim on https://developer.hashicorp.com/terraform/language/modules/configuration (checked this turn). Add them as claim rows, then update the rationale to "plan and apply use the modules already installed".

**5d-mc.** The key c is correct.
- a, b and d are real and taught, and each is wrong for a different reason.
- The "can carry" wording avoids any claim about error behaviour.

**5d-mc2.** Numbers verified: `~> 1.0.4` allows 1.0.5 and 1.0.10 but not 1.1.0 (row 72). So 1.1.10 is out, 1.0.5 and 1.0.10 qualify, and 1.0.10 is numerically newer than 1.0.5. The key b (1.0.10) is correct.
- 1.0.3 is wrong whatever the lower bound is, because it is not the newest.
- **AWS-Qg5-007 (Low).** The rationale says "1.0.3 is below the stated lower bound". The lesson and the page do not state a lower bound. Fix: "1.0.3 is older than the 1.0.4 the constraint starts from, and in any case it is not the newest qualifying release."

**5d-mr.** The keys a and c are correct.
- d (a range keeps the first release): real, and false for the stem's fresh clones, which is taught.
- e (`!=` holds a single release): real mix-up, and taught.
- **AWS-Qg5-008 (Medium, negation pair).** b ("Committing the lock file freezes the module release, because it lists every external dependency") is almost the plain negation of key a. A reader sees one true and one false version of the same sentence, and "because ..." justifies the false claim. This is the same pair pattern as 5c-mc2. Fix: replace b with "Running `terraform init -upgrade` in each CI job keeps the module on the release chosen the first time". Real, because people mix up `-upgrade`. It is wrong for a reason taught in 5c and 5d: `-upgrade` moves modules to the newest release the constraint allows. It tests a different fact from a, so it is not a negation.
- The MR need rule is met: all distractors address the single stated need.

### (d) Numbers and versions in keys and distractors

All verified against the pages: 1.0.5, 1.0.10, 1.1.0, 1.0.3, 1.1.10, `~> 1.0.4`, `~> 6.0`, exact `6.0.1`, `v2.3.0`, `2.x`. The arithmetic is correct. There is no Terraform version floor in any question.

### (e) Rulings

**LD-Qg5-005 (5c-mc2): it is a pair tell, and worse, an odd-one-out tell.** a and d share their first words ("In a `.terraform` subdirectory of the working directory") and differ only in "kept out of" versus "committed so teammates skip the download". Three of four choices (b, c, d) say "committed", so the key is the only choice that does not. A student who knows the lesson says "Don't commit" picks it without reading the location. Replacement for d, which stays real and taught: "In a `modules` folder beside the root `.tf` files, kept out of version control". It is wrong for the same location reason as b, namely that modules land in `.terraform` (taught, row 51). Then two choices commit and two do not, and the question is decided by the location, which is the fact the lesson teaches. Update the rationale: "Nothing creates a `modules` folder next to the root files by default, whether or not it is committed." Drop its last sentence about `.terraform` itself.

**5a-mc2 "Append `//v2.3.0` to the repository address": accept.** It is real, because people reuse `//` as a revision marker. It is taught, because the lesson says `//` marks a subdirectory and `ref` selects a revision. It is not a working answer: it names a folder that does not exist. Only the rationale wording needs the fix in AWS-Qg5-002.

**5a-mr "picked up only after the `.terraform` directory has been deleted and recreated": accept, with one note.** It is clearly false for a taught reason: the lesson says changing `source` requires a fresh `terraform init` "so that Terraform can update the local code", so `init` alone is enough and "only after" is wrong. The rationale states that nothing requires deleting the directory. The lesson does not say so in as many words. If a reviewer wants it airtight, add to 5a: "Re-running `terraform init` is enough; the `.terraform` directory does not need to be deleted." This is not a doc quote, so state it as plain explanation. I do not require it.

### Duplicate facts across questions

None. 5b-mc2 (local value passed as an argument) and 5b-mr (output declaration and `module.<label>.<name>`) are different facts. 5a-mr's "`init` after a `source` edit" is different from 5c-mr's "`-upgrade` / `get -update`". The `./` distractor in 5a-mc and 5d-mc is a recorded exception (each tests a different owned fact), and I accept it.

### Distractor types

After AWS-Qg5-008 and the 5c-mc2 change, `-upgrade` appears as a distractor once (5d-mr) and as a key once (5c-mr). That is within the 15% cap, and the lock file is a distractor in 5c-mc2 only.

### Summary of open items

- AWS-Qg5-001: Low.
- AWS-Qg5-002: Low-Medium.
- AWS-Qg5-003: Low.
- AWS-Qg5-004: Low.
- AWS-Qg5-005: Medium.
- AWS-Qg5-006: Medium, needs a lesson addition (teach-before-test).
- AWS-Qg5-007: Low.
- AWS-Qg5-008: Medium.
- LD-Qg5-005: the pair tell is confirmed; the replacement is above.

Task tf-g5: not yet
Overall: concerns
