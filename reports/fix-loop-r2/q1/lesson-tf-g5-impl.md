# Lesson tf-g5 (Terraform modules) -- implementation report

## Summary

Replaced the placeholder `bodyMarkdown` (objective-text stubs) with a full lesson for tf.004.5a-5d: one `###` section per objective in id order, each ending in `**Exam tip:**`, one `##` title, and the standard `### Warnings` section. `drillIds` now lists all 12 ids (`-mc`, `-mc2`, `-mr` per objective, objective order). `labIds`, `id`, `title`, `module`, `tier`, `practiceMode` and `objectiveIds` are unchanged. `citationIds` was replaced: the placeholder `cite-tf-004` is dropped, 12 new `cite-tf-g5-*` files are listed, and three g4 citations for the same pages are reused (`cite-tf-g4-variables`, `-outputs`, `-locals`; their URLs are the same pages quoted here).

All page text was fetched this turn with `curl -sL` and an HTML-to-text stripper (no WebFetch). Every quote in the table was machine-checked as a verbatim substring of the page named in its row, and every row is 20 words or fewer. Every double-quoted doc string in the lesson body was machine-checked as present in the table. The only quoted strings in the lesson that are not doc quotes are the scenario phrases inside the `**Exam tip:**` lines (for example "a value the parent gives to the child"); these are exam-style cue phrases, the same device tf-g4 uses, and assert nothing beyond the claims in the table.

Doc-reading notes that shaped the content:

- The module block page says the `source` value must be a literal string, yet also allows constant variables (`const = true`). That is internally inconsistent and a very new feature, so the lesson does not teach `const` or variables in `source`/`version`.
- The docs name the `.terraform` subdirectory (get page; "hidden subdirectory" on the use page) but no fetched page says `.terraform/modules` literally. The lesson therefore says `.terraform` subdirectory only.
- The lock-file claim was verified: the lock page says it tracks only provider dependencies. Modules are not covered.

## Three distinct facts per objective (question plan)

Each objective supports 3 questions (mc, mc2, mr) on different facts, and the lesson teaches each fact and the contrast that makes the wrong options wrong.

- **5a**
  - Fact 1: which address shape is which source type (`./` or `../` local; `<NAMESPACE>/<NAME>/<PROVIDER>` registry; `git::`, `github.com/`, `bitbucket.org/` version control; `s3::` archive).
  - Fact 2: a Git source without `?ref=` follows the default branch at HEAD, and `ref` accepts a branch, tag or SHA-1.
  - Fact 3: `//` marks a subdirectory inside a package (query parameters after it, whole package still downloaded), and changing `source` needs a fresh `terraform init`. A spare fact for an MR option: S3 objects must be archives.
- **5b**
  - Fact 1: how a child's variable receives its value (module-block argument) versus root variables (`-var`, `.tfvars`, `TF_VAR_`, HCP workspace).
  - Fact 2: a local is visible only in its own module but can be passed to a child as an argument.
  - Fact 3: values leave a child only through outputs, read as `module.<name>.<output>`. Spare facts: variable names are unique per module and some names are reserved.
- **5c**
  - Fact 1: root module = the `.tf` files in the working directory; a child is whatever a `module` block calls; flat tree/composition is recommended.
  - Fact 2: `terraform init` (or `get`) downloads modules into `.terraform`, never committed; re-running `init` does not change installed modules, `init -upgrade` or `get -update` does.
  - Fact 3: `count`/`for_each` on a module block, unique labels when a source is reused, and the output shape (map for `for_each`, list for `count`). A spare fact: default provider configurations are inherited by child modules; aliased ones and provider requirements are not.
- **5d**
  - Fact 1: `version` is registry-only; local paths do not support it; Git sources pin with `?ref=`.
  - Fact 2: `~>` semantics (`~> 1.0.4` allows 1.0.5 and 1.0.10 but not 1.1.0; `~> 1.1` allows 1.2 and 1.10 but not 2.0), plus `=` exact and the comparison operators.
  - Fact 3: the dependency lock file tracks only providers, so an exact `version` constraint is what freezes a module; `init -upgrade` / `get -update` move it.

## Claim table

| # | Section | Claim | Doc URL | Quote (<=20 words) |
|---|---|---|---|---|
| 1 | 5a | source argument says where Terraform gets module code | https://developer.hashicorp.com/terraform/language/block/module | The source argument specifies where Terraform retrieves the module source code. |
| 2 | 5a | Sources include local files, registry, VCS | https://developer.hashicorp.com/terraform/language/modules | Terraform can load modules from multiple sources, including the local file system, a Terraform registry, and VCS repositories. |
| 3 | 5a | Local path uses ./ or ../ prefix | https://developer.hashicorp.com/terraform/language/block/module | Use the ./ or ../ prefix followed by the path to local module source code |
| 4 | 5a | Registry address shape NAMESPACE/NAME/PROVIDER (hashicorp/consul/aws example is on the same page) | https://developer.hashicorp.com/terraform/language/block/module | Use the following syntax to install modules listed in the public Terraform Registry: |
| 5 | 5a | HCP private registry prefixes app.terraform.io | https://developer.hashicorp.com/terraform/language/block/module | For modules listed in an HCP Terraform private registry, prepend the path with app.terraform.io: |
| 6 | 5a | GitHub over HTTPS uses github.com/ORG/FOLDER | https://developer.hashicorp.com/terraform/language/block/module | Use the following syntax to clone module sources from GitHub over HTTPS: |
| 7 | 5a | GitHub over SSH uses git@github.com:ORG/FOLDER | https://developer.hashicorp.com/terraform/language/block/module | Use the following syntax to clone module sources from GitHub over SSH: |
| 8 | 5a | Generic Git uses the git:: prefix | https://developer.hashicorp.com/terraform/language/block/module | Use the git:: prefix followed by any valid Git URL, including the protocol |
| 9 | 5a | Bitbucket uses bitbucket.org prefix | https://developer.hashicorp.com/terraform/language/block/module | Use the with bitbucket.org prefix to reference to modules hosted in BitBucket: |
| 10 | 5a | Mercurial uses hg:: prefix | https://developer.hashicorp.com/terraform/language/block/module | Use the hg:: prefix followed by a valid Mercurial URL |
| 11 | 5a | s3:: sources must be archives (.zip, .tar.gz) | https://developer.hashicorp.com/terraform/language/block/module | The object stored in the S3 bucket must be an archive with one of the following extensions: |
| 12 | 5a | gcs:: prefix for Google Cloud Storage | https://developer.hashicorp.com/terraform/language/block/module | Use the gcs:: prefix followed by a GCS bucket object URL |
| 13 | 5a | ref accepts branch, SHA-1 or tag | https://developer.hashicorp.com/terraform/language/block/module | Specifies a branch name, full or short SHA-1 hash, or tag name to clone. |
| 14 | 5a | Without ref, Git default branch at HEAD is used | https://developer.hashicorp.com/terraform/language/block/module | Terraform defaults to the default branch referenced by HEAD in the repository. |
| 15 | 5a | // marks a subdirectory (registry example) | https://developer.hashicorp.com/terraform/language/block/module | source = "hashicorp/consul/aws//modules/consul-cluster" |
| 16 | 5a | // marks a subdirectory; query parameters after it (Git example) | https://developer.hashicorp.com/terraform/language/block/module | source = "git::https://example.com/network.git//modules/vpc?ref=v1.2.0" |
| 17 | 5a | Whole package downloaded, module read from subdirectory | https://developer.hashicorp.com/terraform/language/block/module | Terraform extracts the entire package to local disk, but reads the module from the subdirectory. |
| 18 | 5a | Changing source requires terraform init | https://developer.hashicorp.com/terraform/language/block/module | You must run terraform init after modifying the source argument so that Terraform can update the local code. |
| 19 | 5a | Same source can appear in several module blocks | https://developer.hashicorp.com/terraform/language/block/module | You can specify the same source address in two or more separate module blocks |
| 20 | 5b | A module is a self-contained group of resources | https://developer.hashicorp.com/terraform/language/modules/configuration | The resources defined in a module form a self-contained group of resources. |
| 21 | 5b | Root variables set by CLI, env vars, var files, HCP workspace | https://developer.hashicorp.com/terraform/language/block/variable | you can set variable values using CLI options, environment variables, variable definition files, or through an HCP Terraform workspace. |
| 22 | 5b | Child variables are set by the parent as module-block arguments | https://developer.hashicorp.com/terraform/language/block/variable | In child modules, the parent module passes values to child modules as arguments to the module block. |
| 23 | 5b | Child inputs come from the parent as arguments | https://developer.hashicorp.com/terraform/language/values/variables | Child modules receive their inputs from a parent module as arguments. |
| 24 | 5b | Root-module variables assigned by multiple methods (-var etc.) | https://developer.hashicorp.com/terraform/language/values/variables | You can assign values to root module variables through multiple methods |
| 25 | 5b | servers = 5 example: integer input given as a module argument | https://developer.hashicorp.com/terraform/language/modules/configuration | In the following example, the module expects an integer value for the servers input: |
| 26 | 5b | Variable names unique per module | https://developer.hashicorp.com/terraform/language/block/variable | must be unique among all variables in the same module. |
| 27 | 5b | Reserved variable names | https://developer.hashicorp.com/terraform/language/block/variable | any valid identifier except the following reserved names: source, version, providers, count, for_each, lifecycle, depends_on, or locals. |
| 28 | 5b | Locals accessible only in the defining module | https://developer.hashicorp.com/terraform/language/values/locals | You can access local values in the module where you define them, but not in other modules. |
| 29 | 5b | A local can be passed to a child as an argument | https://developer.hashicorp.com/terraform/language/values/locals | you can pass a local value to a child module as an argument. |
| 30 | 5b | Child outputs expose resource attributes to parent | https://developer.hashicorp.com/terraform/language/values/outputs | Child modules can expose resource attributes to parent modules. |
| 31 | 5b | Parent reads child outputs via module.NAME.OUTPUT | https://developer.hashicorp.com/terraform/language/values/outputs | Parent modules can access child module outputs using module.<CHILD_MODULE_NAME>.<OUTPUT_NAME> syntax. |
| 32 | 5c | Root module = .tf files in working directory | https://developer.hashicorp.com/terraform/language/modules/develop | The .tf files in your working directory when you run terraform plan or terraform apply together form the root module. |
| 33 | 5c | Child modules are those configured with module blocks | https://developer.hashicorp.com/terraform/language/modules | Modules you configure using module blocks are called child modules. |
| 34 | 5c | Nested child modules are possible | https://developer.hashicorp.com/terraform/language/modules | The root module can also call a child module that calls its own nested child module. |
| 35 | 5c | Recommendation: flat module tree | https://developer.hashicorp.com/terraform/language/modules/develop/composition | in most cases we strongly recommend keeping the module tree flat, with only one level of child modules |
| 36 | 5c | Example connecting modules with an expression at the root | https://developer.hashicorp.com/terraform/language/modules/develop/composition | vpc_id = module.network.vpc_id |
| 37 | 5c | Flat style is called module composition | https://developer.hashicorp.com/terraform/language/modules/develop/composition | We call this flat style of module usage module composition |
| 38 | 5c | Module author decides the inputs | https://developer.hashicorp.com/terraform/language/block/module | The module developer determines which inputs you can specify for the module. |
| 39 | 5c | count on a module block | https://developer.hashicorp.com/terraform/language/modules/configuration | count: Use this argument to state how many instances of a module to provision. |
| 40 | 5c | for_each on a module block | https://developer.hashicorp.com/terraform/language/modules/configuration | for_each: Use this argument to loop through a set of keys so that Terraform provisions similar module instances. |
| 41 | 5c | count and for_each are mutually exclusive on module block | https://developer.hashicorp.com/terraform/language/block/module | count number / mutually exclusive with for_each |
| 42 | 5c | depends_on accepted on a module block | https://developer.hashicorp.com/terraform/language/block/module | The depends_on meta-argument specifies an upstream resource that the module depends on. |
| 43 | 5c | providers accepted on a module block | https://developer.hashicorp.com/terraform/language/block/module | The providers argument instructs Terraform to use an alternate provider configuration. |
| 44 | 5c | Unique labels required when the same source is reused | https://developer.hashicorp.com/terraform/language/block/module | you must use unique labels for each block. |
| 45 | 5c | module.<label>.<output> syntax | https://developer.hashicorp.com/terraform/language/block/module | you can use the module.<label>.<output> syntax to reference them |
| 46 | 5c | Module without count/for_each is an object with one attribute per output | https://developer.hashicorp.com/terraform/language/expressions/references | the value will be an object with one attribute for each output value defined in the child module. |
| 47 | 5c | for_each module value is a map of objects | https://developer.hashicorp.com/terraform/language/expressions/references | If the corresponding module uses for_each then the value will be a map of objects |
| 48 | 5c | count module value is a list | https://developer.hashicorp.com/terraform/language/expressions/references | except that the value is a list with the requested number of elements |
| 49 | 5c | init installs modules into a hidden subdirectory | https://developer.hashicorp.com/terraform/language/modules/configuration | Terraform clones the module source configurations into a hidden subdirectory of the workspace's working directory. |
| 50 | 5c | terraform get downloads and updates modules | https://developer.hashicorp.com/terraform/cli/commands/get | Run the terraform get command to download and update modules declared in the root module. |
| 51 | 5c | Modules land in a .terraform subdirectory | https://developer.hashicorp.com/terraform/cli/commands/get | The modules are downloaded into a .terraform subdirectory of the current working directory. |
| 52 | 5c | Do not commit .terraform | https://developer.hashicorp.com/terraform/cli/commands/get | Don't commit this directory to your version control repository. |
| 53 | 5c | Child resources become part of the configuration | https://developer.hashicorp.com/terraform/language/modules | Terraform adds the child module's resources to your workspace and manages them as part of the configuration. |
| 54 | 5c | Re-running init installs newly added modules | https://developer.hashicorp.com/terraform/cli/commands/init | will install the sources for any modules that were added to configuration since the last init |
| 55 | 5c | Re-running init does not change installed modules | https://developer.hashicorp.com/terraform/cli/commands/init | but will not change any already-installed modules. |
| 56 | 5c | init -upgrade updates all modules | https://developer.hashicorp.com/terraform/cli/commands/init | updating all modules to the latest available source code. |
| 57 | 5c | get -update checks downloaded modules | https://developer.hashicorp.com/terraform/cli/commands/get | modules that are already downloaded will be checked for updates and the updates will be downloaded if present. |
| 58 | 5c | Child inherits default provider configurations | https://developer.hashicorp.com/terraform/language/modules/develop/providers | a child module automatically inherits default provider configurations from its parent |
| 59 | 5c | Aliased provider configurations are not inherited | https://developer.hashicorp.com/terraform/language/modules/develop/providers | Additional provider configurations (those with the alias argument set) are never inherited automatically by child modules |
| 60 | 5c | Only configurations inherited, not requirements | https://developer.hashicorp.com/terraform/language/modules/develop/providers | Only provider configurations are inherited by child modules, not provider source or version requirements. |
| 61 | 5d | version argument applies only to registry modules | https://developer.hashicorp.com/terraform/language/block/module | This argument only applies when installing modules from a registry: |
| 62 | 5d | version only when source is a registry module | https://developer.hashicorp.com/terraform/language/block/module | You can only use the version argument when the source argument points to a module listed in a registry |
| 63 | 5d | Local paths do not support version | https://developer.hashicorp.com/terraform/language/block/module | Modules sourced from local file paths do not support version |
| 64 | 5d | Reason: local modules share the caller version | https://developer.hashicorp.com/terraform/language/block/module | loaded from the same source repository and always share the same version as their caller. |
| 65 | 5d | Default when version omitted | https://developer.hashicorp.com/terraform/language/block/module | Defaults to latest version available from the source |
| 66 | 5d | Recommendation to constrain versions | https://developer.hashicorp.com/terraform/language/block/module | We recommend explicitly constraining the acceptable version numbers to avoid unexpected or unwanted changes. |
| 67 | 5d | Constraint syntax: comma-separated conditions | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | A version constraint is a string literal containing one or more conditions separated by commas. |
| 68 | 5d | Example constraint >= 1.2.0, < 2.0.0 | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | version = ">= 1.2.0, < 2.0.0" |
| 69 | 5d | = allows exactly one version and is not combinable | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | Allows only one exact version number. Cannot be combined with other conditions. |
| 70 | 5d | != excludes a version | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | Excludes an exact version number. |
| 71 | 5d | Comparison operators | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | The > and >= operators request newer versions. The < and <= operators request older versions. |
| 72 | 5d | ~> 1.0.4 behaviour | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | ~> 1.0.4: Allows Terraform to install 1.0.5 and 1.0.10 but not 1.1.0. |
| 73 | 5d | ~> 1.1 behaviour | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | ~> 1.1: Allows Terraform to install 1.2 and 1.10 but not 2.0. |
| 74 | 5d | ~> lets only the right-most component increment | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | Allows only the right-most version component to increment. |
| 75 | 5d | Newest installed version meeting constraints is used | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | For plugins and modules, Terraform uses the newest installed version that meets the applicable constraints. |
| 76 | 5d | If none installed, newest matching version is downloaded | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | it attempts to download the newest version that meets the applicable constraints. |
| 77 | 5d | Lock file tracks only providers | https://developer.hashicorp.com/terraform/language/files/dependency-lock | At present, the dependency lock file tracks only provider dependencies. |
| 78 | 5d | Lock file does not remember module versions | https://developer.hashicorp.com/terraform/language/files/dependency-lock | Terraform does not remember version selections for remote modules |
| 79 | 5d | Exact constraint freezes the module version | https://developer.hashicorp.com/terraform/language/files/dependency-lock | You can use an exact version constraint to ensure that Terraform will always select the same module version. |
| 80 | 5d | Changing registry version needs init | https://developer.hashicorp.com/terraform/language/block/module | You must run terraform init after modifying the version argument so that Terraform can update the local code. |
| 81 | 5d | Recommendation: specific versions for third-party modules | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | Require specific versions to ensure that updates only happen when convenient to you when your infrastructure depends on third-party modules. |
| 82 | 5d | init -upgrade moves a registry module to the latest allowed version | https://developer.hashicorp.com/terraform/language/modules/configuration | include the -upgrade flag to upgrade the module to the latest version allowed by the version constraint. |
| 83 | 5d | Git source pinned with ?ref= tag (v1.2.0 example) | https://developer.hashicorp.com/terraform/language/modules/configuration | Terraform selects the module version from a Git repository tagged as v1.2.0: |
| 84 | 5a | HTTPS URL with archive extension is used directly as the archive | https://developer.hashicorp.com/terraform/language/block/module | If an HTTPS URL has a common file extension associated with an archive file format, Terraform bypasses the terraform-get=1 redirection |
| 85 | 5a | A module is a directory of .tf files | https://developer.hashicorp.com/terraform/language/modules/develop | create a new directory for it and place one or more .tf files inside |
| 86 | 5a | The label is a local name for the module | https://developer.hashicorp.com/terraform/language/block/module | The LABEL is a local name for the module. |
| 87 | 5d | Terraform selects the newest module version meeting constraints (no module memory) | https://developer.hashicorp.com/terraform/language/files/dependency-lock | Terraform will always select the newest available module version that meets the specified version constraints. |

Claims that carry no quote because they restate or infer from the rows above, not new facts: a parent and a child can each declare a variable called `region` (inferred from the per-module uniqueness row); an unpinned Git source follows the repository's default branch (restates the HEAD row); `-var` and `TF_VAR_` set root variables, not a child's (the TF_VAR_ naming was taught and cited in tf-g4 4c; the child side is the two arguments rows); `~> 1.1` stays in major version 1 (restates the 1.2 and 1.10 but not 2.0 row).

## Self-consistency check (each section re-read in isolation against its rows)

- **5a:** every source shape has a row. The registry example `hashicorp/consul/aws` and the `app.terraform.io` prefix are on the module block page. "Nothing is selected for you" for a missing `ref` is backed by the HEAD row, and the sentence after it is a plain restatement. The lesson does not teach the `depth` parameter or the rule that `depth` needs a named branch or tag.
- **5b:** the section does not say that a parent cannot reference a child's resource address directly (the docs say a module is a self-contained group and that outputs are how attributes are exposed), so it says "no documented way". "Channels" was limited to variables in, outputs out, and local-as-argument, because default provider inheritance (5c) is also a boundary crossing and the docs never say the channels are exclusive. The Warnings bullet uses the same "documented channels" wording.
- **5c:** `terraform get` is described as "about modules alone", backed by the get page's one-line description; the lesson does not say `get` and `init` are equivalent, and `init -upgrade` and `get -update` are named separately. The `.terraform` claim cites the get page only. The root-module quote is exactly 20 words.
- **5d:** the `~> 1.1` example is "stays in major version 1", matching "1.2 and 1.10 but not 2.0". The lock-file claim is scoped to "provider dependencies" in one quote and "remote modules" in the other; both are quoted separately. Local-path modules lack `version` for a different reason (same repository as the caller), so the lesson never suggests the lock file is relevant to them.
- **Against tf-g4 4c:**
  - 4c: a `variable` is set from outside, and a child module call must supply it. 5b agrees ("the parent module passes values ... as arguments").
  - 4c: a `locals` block is invisible outside its module, "even to a parent module that calls it". 5b quotes the same doc line and adds only the documented exception (a local can be passed as an argument). The child receives a value, not the name. No contradiction.
  - 4c: a child's outputs are read with `module.<CHILD_MODULE_NAME>.<OUTPUT_NAME>`. 5b repeats the same doc sentence.
  - 4c: root outputs are what `terraform apply` prints. Not repeated or contradicted.
  - 4c: environment variables need the `TF_VAR_` prefix. 5b says only that `-var` and `TF_VAR_` set root variables, consistent with the doc's "root module variables" wording.
  - 4e/4f: `count`/`for_each` exclusivity and `depends_on` appear in 5c only as "the module block accepts them" plus one quote each; the `for_each` type restrictions and the literal-list rule for `depends_on` are not restated.

## Checks run

### content_lint.py

```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
```

### q1_batch_check.py tf-g5

```
task tf-g5: 12 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 4 for 4 objectives
FAIL: q-tf-004-5a-mc choice c: pastes objective text
FAIL: q-tf-004-5a-mc: stem pastes objective text
FAIL: q-tf-004-5a-mc: no citationIds
FAIL: q-tf-004-5a-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5a-mc: still a placeholder stem
FAIL: q-tf-004-5a-mc2 choice c: pastes objective text
FAIL: q-tf-004-5a-mc2: stem pastes objective text
FAIL: q-tf-004-5a-mc2: no citationIds
FAIL: q-tf-004-5a-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5a-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-5a-mr: stem pastes objective text
FAIL: q-tf-004-5a-mr: no citationIds
FAIL: q-tf-004-5a-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5b-mc choice b: pastes objective text
FAIL: q-tf-004-5b-mc: stem pastes objective text
FAIL: q-tf-004-5b-mc: no citationIds
FAIL: q-tf-004-5b-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5b-mc2 choice b: pastes objective text
FAIL: q-tf-004-5b-mc2: stem pastes objective text
FAIL: q-tf-004-5b-mc2: no citationIds
FAIL: q-tf-004-5b-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5b-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-5b-mr: stem pastes objective text
FAIL: q-tf-004-5b-mr: no citationIds
FAIL: q-tf-004-5b-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5c-mc choice a: pastes objective text
FAIL: q-tf-004-5c-mc: stem pastes objective text
FAIL: q-tf-004-5c-mc: no citationIds
FAIL: q-tf-004-5c-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5c-mc2 choice a: pastes objective text
FAIL: q-tf-004-5c-mc2: stem pastes objective text
FAIL: q-tf-004-5c-mc2: no citationIds
FAIL: q-tf-004-5c-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5c-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-5c-mr: stem pastes objective text
FAIL: q-tf-004-5c-mr: no citationIds
FAIL: q-tf-004-5c-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5d-mc: no citationIds
FAIL: q-tf-004-5d-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5d-mc2: no citationIds
FAIL: q-tf-004-5d-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-5d-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-5d-mr: no citationIds
FAIL: q-tf-004-5d-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: duplicate 6-word openings: ['select two actions that support this']
FAIL: longest-is-key 4/8 = 50%
PASS: shortest-is-key 2/8 = 25%
WARN: MC key positions {'a': 4, 'b': 2, 'c': 2}
PASS: MR key slots {'a': 1, 'b': 1, 'c': 3, 'd': 2, 'e': 1}
FAIL: MR key sets: most common 'c,d' in 2/4 (50%); all {'c,d': 2, 'b,c': 1, 'a,e': 1}
RESULT: FAIL
```

### claim_prose_check.py tf-g5

```
task tf-g5: 16 distinct numbers in lesson prose
PASS: every claim-table number appears in the lesson prose
```

## Round 1 fix pass

Applied every finding from `lesson-tf-g5-AWS.md` (AWS-Lg5-001 to 008) and `lesson-tf-g5-TEACHER.md` (TEACHER-Lg5-001 to 007). Overlaps applied once: AWS-Lg5-002 + TEACHER-Lg5-004 (a branch moves, so it is not a pin), AWS-Lg5-003 + TEACHER-Lg5-002 (reserved names). The page text for the new quotes was fetched this turn with curl (the same cached fetch from this task, re-checked by machine: every table row, including the new ones, is a verbatim substring of its page and 20 words or fewer; every double-quoted doc string in the lesson is in the table). The claim table above was regenerated and now has 87 rows.

New claim rows added (rows 84-87): HTTPS URL with an archive extension is used as the archive (module block page, AWS-Lg5-005); a module is a directory of `.tf` files (develop page, TEACHER-Lg5-005); the label is a local name (module block page, TEACHER-Lg5-005); Terraform selects the newest module version meeting the constraints (lock page, TEACHER-Lg5-003). Row 35 was widened to include "in most cases" (AWS-Lg5-006).

Changes per finding (old text, then new text):

- **AWS-Lg5-001**
  - Old: A `version` constraint belongs only on registry modules. Putting it on a local path or a `git::` source does not pin anything; pin Git sources with `?ref=` and registry modules with an exact `version`.
  - New: A `version` constraint belongs only on registry modules: the docs say the argument "only applies when installing modules from a registry" and that local-path modules "do not support version". Do not add it to a local path or a `git::` source. Pin a Git source with `?ref=` (a tag or commit) and a registry module with an exact `version`.

- **AWS-Lg5-002 + TEACHER-Lg5-004**
  - Old: Pin with a tag, branch or commit using `?ref=`, for example `?ref=v1.2.0` (5a).
  - New: Select a revision with `?ref=`, for example `?ref=v1.2.0` (5a): a tag or a commit SHA fixes the version, while a branch name is accepted too but a branch keeps moving as new commits arrive, so it is not a fixed version.

- **AWS-Lg5-003 + TEACHER-Lg5-002**
  - Old: A variable name cannot collide with the arguments a `module` block itself understands: it can be "any valid identifier except the following reserved names: source, version, providers, count, for_each, lifecycle, depends_on, or locals."
  - New: A variable cannot use certain reserved names: the label can be "any valid identifier except the following reserved names: source, version, providers, count, for_each, lifecycle, depends_on, or locals."

- **AWS-Lg5-004**
  - Old: The docs add the one way around it: "You can access local values in the module where you define them, but not in other modules." The same page adds that "you can pass a local value to a child module as an argument."
  - New: The docs state the rule: "You can access local values in the module where you define them, but not in other modules." They then give the one exception: "you can pass a local value to a child module as an argument."

- **AWS-Lg5-005**
  - Old: an HTTP or HTTPS URL, `s3::` for an S3 bucket object
  - New: an HTTPS URL (one ending in an archive extension such as `.zip` is used directly as the archive: "If an HTTPS URL has a common file extension associated with an archive file format, Terraform bypasses the terraform-get=1 redirection"), `s3::` for an S3 bucket object

- **AWS-Lg5-006**
  - Old: The docs recommend against deep nesting: "we strongly recommend keeping the module tree flat, with only one level of child modules"
  - New: In most cases the docs recommend against deep nesting: "we strongly recommend keeping the module tree flat, with only one level of child modules"

- **AWS-Lg5-008**
  - Old: which updates "all modules to the latest available source code", and `terraform get -update`
  - New: which updates "all modules to the latest available source code" (within any `version` constraint on a registry module, 5d), and `terraform get -update`

- **TEACHER-Lg5-001**
  - Old: Those are the methods 4c covered (`-var`, `.tfvars` files, `TF_VAR_` names).
  - New: `TF_VAR_` names were covered in 4c; `-var` and `.tfvars` files are the other methods in that list.

- **TEACHER-Lg5-003**
  - Old: can therefore move to a newer release the next time Terraform installs it, and no lock file prevents that.
  - New: can therefore move to a newer release the next time Terraform selects a version, and no lock file prevents that: "Terraform will always select the newest available module version that meets the specified version constraints." That happens on a first install, or after `init -upgrade` or `get -update`, not on a repeat `init` of an already-installed module (5c).

- **TEACHER-Lg5-005**
  - Old: how a `module` block is used, and how module versions are pinned.
  - New: how a `module` block is used, and how module versions are pinned. Vocabulary: a module is a folder of `.tf` files; the directory you run Terraform in is the root module, and any module it calls with a `module` block is a child module. The name after `module` in that block is its label.

- **TEACHER-Lg5-007**
  - Old: The docs add a rule for version control: "The modules are downloaded
  - New: The docs say where they land: "The modules are downloaded

- **TEACHER-Lg5-007**
  - Old: " And: "Don't commit this directory to your version control repository."
  - New: " And the rule: "Don't commit this directory to your version control repository."

- **AWS-Lg5-007:** no lesson change (the review says none is needed). The body already says "Don't commit this directory"; question writers must not claim Terraform refuses to commit it.
- **TEACHER-Lg5-006:** planning only, no lesson edit. Fact ownership when the questions are written:
  - 5b owns `module.<name>.<output>` and "a child must declare an output" for a parent to read a value.
  - 5c owns the output shape (map for `for_each`, list for `count`) and `init -upgrade` / `get -update`.
  - 5d owns the lock file, the exact-version pin, and registry-only `version`.
  - Spares: 5a S3 archives and HTTPS archive URLs; 5b variable-name uniqueness and reserved names; 5c provider inheritance.

Isolation re-read of each changed sentence against its row:

- Warnings `version` bullet: asserts only registry-only (rows 61, 62) and "do not add"; no claim about error versus ignored. Pin advice follows the `?ref=` and exact-version rows.
- 5d Git bullet: "a tag or a commit SHA fixes the version" is the inference that a tag/SHA does not move; the `ref` row says only that `ref` accepts those values. The branch half is plain explanation, unquoted, as AWS asked.
- Reserved names: quote is the whole reserved list; the claim no longer says they are module-block arguments.
- Locals: first quote is the rule, second is the exception; each quote is a separate sentence on the page.
- HTTPS archive: the claim says HTTPS only, matching the row; the HTTP vanity-URL behaviour is not taught.
- 5d move-to-newer sentence: the quote says it always selects the newest version meeting the constraints; the scoping to first install or `-upgrade`/`get -update` rests on the init rows (5c rows: re-running init does not change installed modules; `-upgrade`; `get -update`). It no longer conflicts with 5c.
- Vocabulary sentence: directory of `.tf` files and label rows; root and child were already defined in 5c rows.
- Against tf-g4 4c: unchanged. The `-var` statement no longer claims 4c covered `-var` or `.tfvars`.

The check outputs above were produced by the whole chain run after these edits.
