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
