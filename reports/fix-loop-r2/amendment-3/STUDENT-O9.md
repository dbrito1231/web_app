# Student review — O9 (sidecar files + s12–s15 rewrite)

Reviewer: College IT Student (read-only). Basic IT background, not an AWS expert. Reviewed by
opening each lab card in the running app (`http://127.0.0.1:5173`, Labs tab) and reading it top to
bottom the way I would while actually doing the lab. No commands run, no files edited, no Reset/
Import/Check-answers clicked.

Scope: GL-01, GL-02, GL-03, GL-09, GL-10, GL-11, GL-12, GL-18, GL-19, and GL-05 (delete-order text
only). Change logs read: `impl-O9-A.md`, `impl-O9-B.md`, `AWS-O9.md`.

## Per-lab table

| Lab | File step clear? | Copyable? | s12–s15 make sense? | Notes |
| --- | --- | --- | --- | --- |
| GL-01 | y | y | y | Step 6 tells me exactly what the boundary policy contains in plain English ("Allow Action * on Resource *", then the four denies) right before the one-line command that writes it. The line is long but it's one continuous line with no breaks, so a copy-paste should just work. |
| GL-02 | y | y | y | Step 8 (`lifecycle.json`) is simple. Step 10 (`gl02-policy.json`) is the first "hashtable piped to ConvertTo-Json" style command I hit — `$Gl02Policy = @{ Version = ...; Statement = @(@{ ... }) }; ... ConvertTo-Json -Depth 10 -Compress`. It's still one line so it should paste fine, but it's the most intimidating-looking line so far for someone who isn't comfortable with PowerShell hashtables. Not a defect, just harder to *read* than to *use*. |
| GL-03 | y | y | y | Step 7 first captures `$CallerArn` (a real gap the impl report says it fixed), then writes `gl03-trust.json`, then creates the role — in that order, which makes sense. Step 8 does the same pattern for the read policy. Cost checkpoint text ("IAM roles and policies carry no charge...") is accurate and matches what's on the card. |
| GL-05 | n/a (no sidecar) | n/a | y | "Order the deletes" (step 13) now reads: VPC endpoint → restore NACL association to default + delete custom NACL → disassociate/delete both route tables → delete both subnets → detach/delete IGW → delete SG → delete VPC. That is the exact order the Stop Charges commands run in. Before this fix (per the impl note) it listed NACL twice and in the wrong spot — I can't see the old version, but the current text and the actual commands agree, which is what matters to me as the person following along. |
| GL-09 | y | y | mostly | `gl09-lt.json` (step 7) is clear and short. **But** the cost checkpoint (step 12) says "...the ASG resource still exists until you delete it in **step s10**." I don't know what "s10" is — the numbered steps I see on screen go 1–15, and step 10 is literally titled "Delete ASG", so it does map, but showing me the internal id "s10" instead of "step 10" is confusing on first read. I had to go count steps to work out what it meant. |
| GL-10 | **no** | n/a | y | This is the one that actually stopped me. Step 9 ("Create Lambda function") says: "Zip gl10_lambda.py as function.zip with a handler that logs the event." — and that's it. There's no PowerShell line that writes `gl10_lambda.py`, unlike every other lab in this set where the file-writing command is spelled out right there. Worse, the very next line runs `aws lambda create-function ... --handler lambda_function.lambda_handler ...` — so the function file AWS expects is called `lambda_function.py`, not `gl10_lambda.py`. If I actually created a file named `gl10_lambda.py` (which is what the step tells me to do) and zipped that, `create-function` would fail because the zip wouldn't contain `lambda_function.py`. This is exactly the kind of "hand-write it yourself and guess" step O9 was supposed to remove, and it also has a naming mismatch on top. |
| GL-11 | y | y | y | Step 6 is dense — it writes the trust policy, creates the role, attaches the policy, reads the role Arn, writes `lambda_function.py` **and** zips it, then calls `create-function`, all in one step block. Each PowerShell line has a plain-English sentence after it ("This writes the handler with LF endings and no BOM, then zips it..."), so I could follow it, but it's a lot to absorb in a single step compared to GL-01–GL-03. The `lambda_function.py`/`function.zip` naming here is consistent with the `--handler lambda_function.lambda_handler` flag used later — this is what GL-10 should look like. |
| GL-12 | y, but see below | y | y | Step 6 writes the trust policy and, in the same step, writes `gl12-log-policy.json` and attaches it with `put-role-policy`. Step 7 writes the ASL and creates the state machine. Both file-writing lines come before the commands that use them, and each has an explanatory sentence. **However**: I never see `--logging-configuration` on the `create-state-machine` call in step 7, and nothing later in the lab checks CloudWatch Logs. So I attach a whole CloudWatch Logs permission policy to the role in step 6 and then never use it or verify it anywhere. As a student this did confuse me — I assumed I'd see a log-checking step later (the way GL-10/GL-11 end with `aws logs tail`), and when it never showed up I was left wondering if I'd missed a step. This matches AWS's finding AWS-O9-001. |
| GL-18 | y | y | mostly | Steps 6–8 write `gl18-trust.json`, `gl18-task.json`, and `network.json` in that order, each right before the command that consumes it, each with a one-line explanation. Step 8 also resolves `$VpcId`/`$SubnetId` before writing `network.json`, so nothing is blank. Same "internal id" issue as GL-09: step 13 says "...but **s10** deregisters this one for tidiness" instead of "step 10." Minor, but same pattern. |
| GL-19 | y | y | y | Step 6 writes `gl19-eks-trust.json` before `create-role`. Cost checkpoint correctly says the EKS control plane "cannot be stopped, only deleted," which matches there being no scale-to-zero option for this lab. No sidecar or teardown confusion here. |

## AWS-O9-001 (GL-12 unused logging policy) — did it confuse me as a student?

Yes. I would not have known this was a "loose end" on my own — from the lab's point of view, step 6
looks like a normal, necessary setup step (it even explains what the policy does), so I'd do it and
move on. The confusion shows up later: nothing in the lab ever exercises CloudWatch Logs for Step
Functions, so if I went looking for the payoff of that step (a log entry, a console screen, anything
to check), I wouldn't find one. A student in "just follow the lab" mode would probably not notice
anything is wrong; a student trying to understand *why* each step exists (which is the point of a
study lab) would notice the disconnect. I'd rather the lab either show me the log group and turn
logging on, or skip that policy entirely — AWS's suggested fix (b) (drop the policy write and
`put-role-policy` bullet, since the state machine only needs `sts:AssumeRole`) matches what I as a
student would expect from a "minimal" lab description.

## New issues found

**STUDENT-O9-001 (Medium) — GL-10 step 9 has no file-writing command and a filename mismatch.**
`content/labs/gl-10.json`, step `s09` ("Create Lambda function"), bullet 1 reads "Zip gl10_lambda.py
as function.zip with a handler that logs the event" with no PowerShell line that creates that file
(unlike GL-11's equivalent step, which was fixed under this same amendment). Bullet 2 then runs
`aws lambda create-function ... --handler lambda_function.lambda_handler --zip-file
fileb://function.zip`, which requires the zip to contain a file named `lambda_function.py`, not
`gl10_lambda.py`. Following the step literally (write `gl10_lambda.py`, zip it) produces a zip
`create-function` will reject or that will error at invoke time. Suggested fix: give GL-10 s09 the
same treatment GL-11 s06 got — a `WriteAllText`/`Compress-Archive` bullet that writes
`lambda_function.py` and zips it to `function.zip`, matching the `--handler` flag, before the
`create-function` call.

**STUDENT-O9-002 (Low) — internal step-ids ("s09", "s10", "s11") leak into student-facing text.**
Found in `content/labs/gl-06.json` (s12, "...releasing the EIP in step s11..."), `gl-09.json` (s12,
"...you delete it in step s10."), `gl-14.json` (s12, "...only deletion in s09 stops the meter."),
and `gl-18.json` (s13, "...but s10 deregisters this one for tidiness."). All four are inside the
rewritten cost-checkpoint / order-the-deletes text from this same batch (TEACHER-210). The numbered
steps shown on screen are plain integers ("Step 10", not "s10"), so a student has to translate the
internal id back into an on-screen step number to know what's being referenced. Suggested fix:
reword each to name the step by its visible number or title ("...until you delete it in the Delete
ASG step" / "step 10") instead of the internal id.

## Overall: concerns

The sidecar-file rewrite (TEACHER-209) is a real improvement everywhere I could check it: GL-01,
GL-02, GL-03, GL-09, GL-11, GL-12, GL-18, and GL-19 all now show me the exact file contents and a
copy-pasteable PowerShell line before the command that needs the file, with plain-English
explanations where the command is dense. GL-05's teardown-order prose now matches its commands.
That said, I can't approve outright because of STUDENT-O9-001: GL-10, which is in the same "guided
labs" family and one step away from GL-11's fixed version, still has an unwritable/mismatched file
step that would stop a student cold. AWS-O9-001 (GL-12's unused logging policy) is a real point of
confusion for anyone following the lab to understand *why* they're doing each step, not just to
finish it — I'd want that resolved too, though I recognize AWS graded it Low and technically
correct. STUDENT-O9-002 is cosmetic but shows up in four labs, so it's worth a single sweep rather
than four one-off fixes.
