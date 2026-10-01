# Questions tf-g7 (Maintain infrastructure) -- implementation report

## Summary

Nine questions written into `content/questions/q-tf-004-7{a,b,c}-{mc,mc2,mr}.json`. `id`, `type`, `module`, `difficulty`, `objectiveIds` and `selectCount` are unchanged. Every question has `citationIds` (cite-tf-g7-* files), `mcpStatus: "verified"` and `reviewedOn: "2026-09-26"`. MC has 4 choices, MR has 5 with "(Select TWO.)" in the stem. Keys and distractors are in parallel form: no "as ...", "because ...", "since ..." or "so ..." clause appears on any distractor alone. Rationales explain by content and use no letters. Facts follow the Teacher's ownership list: nothing here makes plain `state list`/`state show`, the import-block-versus-command contrast, or "-json/-raw print sensitive values" a key. Not used: the twenty-buckets scenario, a `terraform import` distractor, the labelled 7c advice, the tutorial's CORE/PROVIDER-with-PATH nuance, any `state pull` read-only claim, any claim that TRACE logs contain secrets, any version floor for `identity` or `for_each`.

One lesson addition was needed so a question rests on taught text: the push refusal sentences (7b-mr) and the `jq` sentence (7b-mc2). Both have claim rows and fetched quotes (see the lesson report).

## Key balance

- MC keys: 7a-mc c, 7a-mc2 a, 7b-mc d, 7b-mc2 b, 7c-mc d, 7c-mc2 b, so a1 b2 c1 d2.
- MR key slots: 7a-mr b,d; 7b-mr a,c; 7c-mr c,e, so a1 b1 c2 d1 e1.
- `q1_batch_check`: longest-is-key 1 of 6 (17%), shortest-is-key 1 of 6 (17%). In 7a-mc2 the key is the longest MC choice (105 characters against 69 to 84); in 7b-mc2 the key is the second longest.

## Questions, facts and distractor checks

Two checks per distractor: (R) it is a real option someone might use; (T) the reason it is wrong is taught in the lesson text.

### 7a-mc (generated configuration as a draft; difficulty applied)
Fact: output of the plan flag that writes the resource block is a best-guess draft to prune and review. New versus 6d (which owns only that the flag exists, is experimental, needs a new file).
- Finished and ready as it stands: R yes (a common assumption after generation). T "Terraform produces HCL to act as a template ... best guess"; "Please review the configuration and edit it as necessary"; the replace-after-import plan.
- Regenerated on each later plan: R yes (people expect generated files to track the provider). T generation covers resources "that do not already exist in your configuration", and once in state Terraform no longer needs to generate.
- Only values that differ from defaults: R yes (the tutorial recommends this pruning, so it is the form people expect). T the file "contains all possible arguments ... including those set to default values".

### 7a-mc2 (`for_each` on the import block; foundation)
Fact: one `import` block with `for_each`, `to` indexed by `each.key`, `id` from `each.value`. Scenario differs from 6d-mc2 (three databases from a `locals` map, one block; no bucket count, no `terraform import` distractor).
- `id` as a list of IDs: R yes (a natural attempt at batching). T "You must specify a string or an expression that evaluates to a string."
- `id` plus `identity`: R yes (`identity` is a real argument). T "You cannot use the id argument and identity argument in the same import block."
- `provider` argument naming the environments: R yes (a real meta-argument, easily confused with `for_each`). T `provider` selects "the specified provider configuration" (alias gloss, different regions), not which objects.

### 7a-mr (what import does and does not do; applied; keys b and d)
Keys: whole lifecycle including destruction; no detection of links between objects.
- Health check written from the provider: R yes (a plausible expectation). T "It cannot determine: the health of the infrastructure. the intent of the infrastructure."
- `id` may stay unknown until apply: R yes (values known "after apply" are common elsewhere). T "The ID must be known during the plan operation."
- One ID format for every type, documented in core: R yes. T the `id` value "depends on the type of resource", and the ID is found in the provider documentation.
- MR stem-need rule: the stem asks what Terraform "will and will not do once the import completes", and every option makes a claim about import behaviour or the import block's input.

### 7b-mc (find the address from an ID; applied)
Fact: `terraform state list -id=...`. New versus 6d (plain list and show).
- `terraform state show sg-...`: R yes (the obvious command for one resource). T "This command requires an address that points to a single resource in the state."
- `terraform state list aws_security_group`: R yes (filter by type). T patterns are in "resource addressing format", so this lists every group of that type; only `-id` filters by ID.
- `terraform state list module.network`: R yes. T it lists "resources in the given module and any submodules"; the stem says the owning module is unknown.

### 7b-mc2 (`-raw` for a script; foundation)
Fact: `terraform output -raw NAME` for a plain string; stem rules out JSON tooling and quotes.
- `terraform output lb_address`: R yes (default form). T the default human-readable format "can change over time", scripts should use `-json` or `-raw`; `-raw` prints "directly with no extra escaping".
- `terraform output -json lb_address`: R yes (the stable scripting format). T meant to be parsed by a tool such as jq, and the stem says the runner has none.
- `terraform show`: R yes (a real inspection command). T it prints the whole state or a plan file in human-readable form, not one root output.

### 7b-mr (state push checks; applied; keys a and c)
Keys: a higher destination serial blocks the push; `-force` disables both checks and the destination is overwritten.
- `state pull` with a path uploads: R yes (pull and push are easy to swap). T pull "downloads and outputs state ... outputs the raw format to stdout".
- Differing lineage accepted after a prompt: R yes (a prompt is how many tools handle risk). T "Terraform will not allow you to push the state."
- Docs recommend push as routine: R yes. T "We only recommend using this command when you must manually modify the remote state."
- MR stem-need rule: the stem asks about the upload step; each distractor is a claim about that step or the command that is often mistaken for it.

### 7c-mc (JSON format; applied)
Fact: `TF_LOG=JSON` gives parseable output at TRACE or higher.
- TRACE: R yes (the most verbose level). T by default logs are plain text lines, so it meets the detail need but not the structured need.
- DEBUG and INFO: R yes. T lower in "decreasing verbosity" and plain text.
- Shortest/longest: choices are within one character of each other by design (same frame).

### 7c-mc2 (core versus provider; foundation)
Fact: `TF_LOG_PROVIDER` at TRACE for plugins only.
- `TF_LOG_CORE` TRACE: R yes. T "Does not include providers."
- `TF_LOG_PROVIDER` ERROR: R yes (right variable, wrong level). T ERROR is "Least verbose".
- Both variables TRACE: R yes (a common way to collect everything). T it also turns on core logs, which the stem excludes; core and provider logs are separate streams.

### 7c-mr (log file for a bug report; applied; keys c and e)
Keys: `TF_LOG_PATH` alone enables nothing (a level variable is needed); the second run is appended to the same file.
- `WARN` is what maintainers ask for: R yes. T "we recommend setting TF_LOG=TRACE"; TRACE is the most verbose level.
- stdout by default: R yes. T "writes the specified log output to stderr."
- JSON logs are a stable interface: R yes (JSON sounds stable). T "The JSON encoding of log files is not considered a stable interface."
- Not tested: the tutorial's wording that pairs the path with core or provider variables. The key says "no level variable", which every page agrees on.

## Distractor types, counted by hand (the audit's TERMS lack most g7 constructs)

Cap is 1 question per type (15% of 9 rounds down to 1). Constructs named in distractors, by question:
- 7a-mc: statements about the generated file (finished, regenerated, minimal). 7a-mc2: `id` list, `id` with `identity`, `provider` argument. 7a-mr: health check, unknown `id`, uniform ID format.
- 7b-mc: `state show <ID>`, `state list <type>`, `state list <module>`. 7b-mc2: plain `output`, `output -json`, `show`. 7b-mr: `state pull`, lineage prompt, push as routine.
- 7c-mc: `TF_LOG` at TRACE, DEBUG, INFO. 7c-mc2: `TF_LOG_CORE`, `TF_LOG_PROVIDER` at ERROR, both at TRACE. 7c-mr: `WARN`, stdout, JSON stable.
- No construct appears as a distractor in more than one question: `state show` (7b-mc only), `state list` (7b-mc only), `output` (7b-mc2 only), `show` (7b-mc2 only), `state pull` (7b-mr only), TRACE as a distractor (7c-mc only; it is the key level elsewhere), ERROR (7c-mc2 only), WARN (7c-mr only), `import` block as a distractor term (7a-mr only; the audit counts it once), `TF_LOG_PATH` (key text only in 7c-mr, never a distractor), `TF_LOG_CORE` (7c-mc2 only). 7b-mc uses `state list` in two of its own distractors with different wrong reasons (type pattern, module pattern); that is within one question, so the cap is not affected.
- The audit's own output (below) shows `import block` 1, `state show` 1, `state list` 1, all at the cap of 1.

## Chain output (whole tf-g7, run after the last edit)

```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
---
task tf-g7: 9 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 3 for 3 objectives
PASS: duplicate 6-word openings: []
PASS: longest-is-key 1/6 = 17%
PASS: shortest-is-key 1/6 = 17%
PASS: MC key positions {'a': 1, 'b': 2, 'c': 1, 'd': 2}
PASS: MR key slots {'a': 1, 'b': 1, 'c': 2, 'd': 1, 'e': 1}
PASS: MR key sets: most common 'b,d' in 1/3 (33%); all {'b,d': 1, 'a,c': 1, 'c,e': 1}
RESULT: PASS
---
task tf-g7: 9 questions; 15% cap = 1 questions

import block                  1   11%  q-tf-004-7a-mr
state list                    1   11%  q-tf-004-7b-mc
state show                    1   11%  q-tf-004-7b-mc

RESULT: PASS
---
task tf-g7: 9 questions, 0 waiver(s) on file

no stem/key echo found

0 unwaived giveaway, 0 waived, 0 bulk echo, of 9 questions
RESULT: PASS
---
task tf-g7: 3 distinct numbers in lesson prose
PASS: every claim-table number appears in the lesson prose
---
PASS: 12 bad, 10 good, 0 failures
```

Overall: approve
