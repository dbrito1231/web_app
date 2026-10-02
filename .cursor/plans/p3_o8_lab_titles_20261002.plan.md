# Plan P3: Finish O8 (GL-07 and GL-21 titles)

Author: Lead Developer. Status: **draft, awaiting user approval.** Phase 2 of `master_open_items_20261002.plan.md`.

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
2. Teacher ruling on `gl-21` `tf.004.8a`:
   - **Keep** if UL-21 or GL-21 really practises it.
   - Otherwise **remove** it from `gl-21.json` `objectiveIds`. The coverage registry and the Coverage tab are then re-checked, because labs feed `guided_refs`.
3. Check every other sidebar title against its lab file with a one-off script, read-only. Report other mismatches; do not fix them silently.
4. Student check (a browser screenshot or a text check of the rendered sidebar): Gone or not.

## Files

`frontend/src/data/curriculum.ts`; possibly `content/labs/gl-21.json` and `content/coverage/saa_registry.json`; the register.

## Risks

Removing an objective from a lab changes coverage counts. Only do it if the Teacher rules that way, and re-run `content_lint.py` and the lab scanner.

## Tests

`npm run build`; `content_lint.py`; `scripts/scan_lab_placeholders.py`; `manage.py test workbook`; the Student check.

## Learning content affected

Yes (lab titles a learner sees; possibly lab objectives). The Teacher validates before and after.
