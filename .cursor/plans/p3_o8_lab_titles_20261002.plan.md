# Plan P3: Finish O8 (GL-07 and GL-21 titles)

Author: Lead Developer. Status: **approved by the user 2026-10-04 (recommended option).** Phase 2 of `master_open_items_20261002.plan.md`.

## Problem (facts checked 2026-10-02)

Round 2 "fixed" O8 by renaming the lab files. GL-07 is now "GL-07 — EC2 and EBS" (with the line "UL-07 adds the EFS file system"). GL-21 is now "GL-21 — ElastiCache tradeoffs". The fix was never second-role closed, and it is **incomplete**: the Labs sidebar still uses the old names, from `frontend/src/data/curriculum.ts`:
- `gl-07`: "EC2, EBS, EFS". GL-07 has no EFS steps.
- `gl-21`: "ElastiCache & HCP path". GL-21 contains no HCP text.

Also, `gl-21.json` lists objective `tf.004.8a` (HCP Terraform) although the lab teaches no HCP content. `ul-21` ("ElastiCache then HCP as allowed") may be the lab that covers it.

## Options (KISS)

1. **Fix the two nav titles and check (recommended).**
   - Change `curriculum.ts` to "EC2 and EBS" and "ElastiCache tradeoffs", matching the lab files.
   - The Teacher rules on whether `tf.004.8a` belongs on `gl-21`.
   - A Student (second role) confirms the Labs screen.
2. **Derive nav titles from the lab files.** Change the code so the sidebar reads each lab's `title`, so the two can never drift again. This is more robust, but it is a code change across all 42 labs.
3. **Second-role check only.** Have a Student confirm the lab files as they are and change no code. This leaves the sidebar wrong.

## Recommended approach (option 1)

1. Edit the two strings in `curriculum.ts`.
2. `tf.004.8a` ("Use HCP Terraform to create infrastructure"). The Teacher has already ruled, from the lab steps:
   - **Remove it from `gl-21.json`**: GL-21 teaches no HCP and says "Terraform is not required".
   - **Keep it on `ul-21` as partial**: UL-21 covers HCP sign-up, a remote-backend block and notes, but stops before connecting AWS credentials and never creates infrastructure through HCP. Record "partial (setup and concepts, no run)".
   - `tf.004.8a` is not in `saa_registry.json`; it is in `content/objectives/terraform_004.json`. Check how the Coverage tab counts Terraform lab coverage, so 8a still shows one lab (UL-21).
3. Check every other sidebar title against its lab file with a one-off script, read-only. Normalise benign differences, such as shortened names ("IAM role & STS") and hyphenation ("single AZ" vs "single-AZ"), so the report is not noise. Report only real mismatches (the Teacher suggests looking at gl-20 and gl-03); do not fix them silently.
4. Student check (a browser screenshot or a text check of the rendered sidebar): Gone or not.

## Files

`frontend/src/data/curriculum.ts`; possibly `content/labs/gl-21.json` and `content/coverage/saa_registry.json`; the register.

## Risks

Removing an objective from a lab changes coverage counts. Only do it if the Teacher rules that way, and re-run `content_lint.py` and the lab scanner.

## Tests

`npm run build`; `content_lint.py`; `scripts/scan_lab_placeholders.py`; `manage.py test workbook`; the Student check.

## Teacher pre-validation (2026-10-02)

**Approve**, with the `tf.004.8a` ruling folded in above (CR-0023).

## Learning content affected

Yes (lab titles a learner sees; possibly lab objectives). The Teacher validates before and after.
