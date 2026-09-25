import importlib.util
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

_SCRIPT = Path(settings.REPO_ROOT) / "scripts" / "scan_lab_placeholders.py"
_spec = importlib.util.spec_from_file_location("scan_lab_placeholders", _SCRIPT)
scan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan)

# `content_lint.py`'s `find_duplicate_criteria` (and its `_normalize_criterion`
# helper) live outside `main()`, so importing the module this way defines them
# without running the full lint against the real content directory.
_LINT_SCRIPT = Path(settings.REPO_ROOT) / "scripts" / "content_lint.py"
_lint_spec = importlib.util.spec_from_file_location("content_lint", _LINT_SCRIPT)
content_lint = importlib.util.module_from_spec(_lint_spec)
_lint_spec.loader.exec_module(content_lint)


def guided(steps_bullets, deletes):
    return {
        "id": "gl-99",
        "kind": "guided",
        "steps": [{"id": "s01", "title": "t", "bullets": steps_bullets}],
        "teardown": {"orderedDeletesPowerShell": deletes},
    }


def unguided(deletes):
    return {"id": "ul-99", "kind": "unguided", "teardown": {"orderedDeletesPowerShell": deletes}}


class LabScanTests(SimpleTestCase):
    def test_clean_guided_lab_passes(self):
        lab = guided(
            ["Run `$VpcId = aws ec2 create-vpc --cidr-block 10.0.0.0/16`."],
            ["aws ec2 delete-vpc --vpc-id $VpcId"],
        )
        self.assertEqual(scan.scan_lab(lab), [])

    def test_null_reset_is_not_an_assignment(self):
        lab = guided([], ["$VpcId = $null", "if ($VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }"])
        errors = scan.scan_lab(lab)
        self.assertTrue(any("resets a variable to $null" in e for e in errors))
        self.assertTrue(any("$VpcId but nothing sets" in e for e in errors))

    def test_teardown_lookup_counts_as_assignment(self):
        lab = guided(
            [],
            [
                "$AccountId = aws sts get-caller-identity --query Account --output text",
                '$Arn = "arn:aws:iam::$($AccountId):policy/p"',
                "aws iam delete-policy --policy-arn $Arn",
            ],
        )
        self.assertEqual(scan.scan_lab(lab), [])

    def test_error_action_on_aws_fails_but_cmdlet_is_fine(self):
        lab = guided(
            ["Run `Remove-Item Env:AWS_SESSION_TOKEN -ErrorAction SilentlyContinue`."],
            ["aws eks delete-cluster --name c -ErrorAction SilentlyContinue"],
        )
        errors = scan.scan_lab(lab)
        self.assertEqual(len(errors), 1)
        self.assertIn("-ErrorAction on an aws command", errors[0])

    def test_unguided_needs_header_guards_and_own_names(self):
        bad = unguided(
            [
                "aws ec2 delete-vpc --vpc-id $VpcId",
                "aws lambda delete-function --function-name workbook-gl10",
            ]
        )
        errors = scan.scan_lab(bad)
        self.assertTrue(any("'# Uses:'" in e for e in errors))
        self.assertTrue(any("workbook-gl" in e for e in errors))

        unguarded = unguided(["# Uses: $VpcId", "aws ec2 delete-vpc --vpc-id $VpcId"])
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(unguarded)))

        good = unguided(
            [
                "# Uses: $VpcId (the IDs you set while building; unset ones are skipped)",
                "# Lost an ID? aws resourcegroupstaggingapi get-resources",
                "if ($VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }",
            ]
        )
        self.assertEqual(scan.scan_lab(good), [])

    def test_duplicate_lines_fail(self):
        line = "aws ec2 delete-vpc --vpc-id $VpcId"
        lab = guided(["Run `$VpcId = aws ec2 create-vpc`."], [line, line])
        self.assertTrue(any("duplicate" in e for e in scan.scan_lab(lab)))

    # -- PY-R3-002: guard-quality bypasses -----------------------------------

    def test_always_true_guard_fails(self):
        lab = unguided(
            [
                "# Uses: $VpcId",
                "if ($true -or $VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }",
            ]
        )
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(lab)))

    def test_inverted_guard_fails(self):
        lab = unguided(
            ["# Uses: $VpcId", "if (-not $VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }"]
        )
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(lab)))

    def test_delete_outside_guard_block_fails(self):
        lab = unguided(
            ["# Uses: $VpcId", "if ($VpcId) { } aws ec2 delete-vpc --vpc-id $VpcId"]
        )
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(lab)))

    def test_second_statement_after_guard_fails(self):
        lab = unguided(
            [
                "# Uses: $VpcId, $SubnetId",
                "if ($VpcId -and $SubnetId) { aws ec2 delete-x --id $VpcId }; "
                "aws ec2 delete-subnet --subnet-id $SubnetId",
            ]
        )
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(lab)))

    def test_guard_name_must_match_whole_variable(self):
        lab = unguided(
            ["# Uses: $VpcId", "if ($VpcIdOld) { aws ec2 delete-vpc --vpc-id $VpcId }"]
        )
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(lab)))

    def test_guard_eq_null_is_inverted_and_fails(self):
        lab = unguided(
            [
                "# Uses: $VpcId",
                "if ($VpcId -eq $null) { aws ec2 delete-vpc --vpc-id $VpcId }",
            ]
        )
        self.assertTrue(any("not guarded" in e for e in scan.scan_lab(lab)))

    def test_nested_blocks_inside_a_valid_guard_pass(self):
        lab = unguided(
            [
                "# Uses: $FileSystemId",
                "if ($FileSystemId) { $MtIds = aws efs describe-mount-targets "
                "--file-system-id $FileSystemId --output text; "
                "foreach ($MtId in $MtIds) { if ($MtId) { aws efs delete-mount-target "
                "--mount-target-id $MtId } } }",
            ]
        )
        self.assertEqual(scan.scan_lab(lab), [])

    def test_guard_with_value_comparison_passes(self):
        lab = unguided(
            [
                "# Uses: $VpcId",
                "if ($VpcId) { $IsDefault = aws ec2 describe-vpcs --vpc-ids $VpcId "
                "--query Vpcs[0].IsDefault --output text }",
                "if ($VpcId -and $IsDefault -eq 'False') { aws ec2 delete-vpc --vpc-id $VpcId }",
            ]
        )
        self.assertEqual(scan.scan_lab(lab), [])

    # -- PY-R3-003: null/empty-reset bypasses and empty teardowns -----------

    def test_empty_string_reset_is_not_an_assignment(self):
        lab = guided([], ["$VpcId = ''", "aws ec2 delete-vpc --vpc-id $VpcId"])
        self.assertTrue(any("$VpcId but nothing sets" in e for e in scan.scan_lab(lab)))

    def test_self_assignment_is_not_an_assignment(self):
        lab = guided([], ["$VpcId = $VpcId", "aws ec2 delete-vpc --vpc-id $VpcId"])
        self.assertTrue(any("$VpcId but nothing sets" in e for e in scan.scan_lab(lab)))

    def test_assignment_text_inside_a_string_does_not_count(self):
        lab = guided(
            [],
            [
                'Write-Host "$VpcId = gone"',
                "aws ec2 delete-vpc --vpc-id $VpcId",
            ],
        )
        self.assertTrue(any("$VpcId but nothing sets" in e for e in scan.scan_lab(lab)))

    def test_empty_teardown_fails(self):
        lab = guided(["Run `$VpcId = aws ec2 create-vpc`."], [])
        self.assertTrue(any("no delete commands" in e for e in scan.scan_lab(lab)))

    def test_comment_only_teardown_fails(self):
        lab = unguided(["# Uses: none", "# nothing else to do here"])
        self.assertTrue(any("no delete commands" in e for e in scan.scan_lab(lab)))

    # -- PY-R3-004: -ErrorAction rule per bullet/line, case and alias -------

    def test_lowercase_erroraction_on_aws_fails(self):
        lab = guided([], ["aws eks delete-cluster --name c -erroraction SilentlyContinue"])
        errors = scan.scan_lab(lab)
        self.assertTrue(any("-ErrorAction on an aws command" in e for e in errors))

    def test_ea_alias_on_aws_fails(self):
        lab = guided([], ["aws eks delete-cluster --name c -EA SilentlyContinue"])
        errors = scan.scan_lab(lab)
        self.assertTrue(any("-ErrorAction on an aws command" in e for e in errors))

    def test_aws_exe_with_erroraction_fails(self):
        lab = guided([], ["aws.exe eks delete-cluster --name c -ErrorAction SilentlyContinue"])
        errors = scan.scan_lab(lab)
        self.assertTrue(any("-ErrorAction on an aws command" in e for e in errors))

    def test_error_action_checked_per_bullet_not_whole_step(self):
        lab = guided(
            [
                "Configure the aws CLI profile first.",
                "Run `Remove-Item Env:X -ErrorAction SilentlyContinue`.",
            ],
            ["aws ec2 delete-vpc --vpc-id $VpcId"],
        )
        errors = scan.scan_lab(lab)
        self.assertFalse(any("-ErrorAction on an aws command" in e for e in errors))

    # -- PY-R3-005: narrower prose-assignment phrasing -----------------------

    def test_prose_copy_into_and_set_to_still_satisfy_the_rule(self):
        lab = guided(
            [
                "Copy the Account value into `$AccountId`.",
                "Set `$BoundaryArn` to the policy Arn shown.",
            ],
            [
                "aws budgets delete-budget --account-id $AccountId --budget-name b",
                "aws iam delete-policy --policy-arn $BoundaryArn",
            ],
        )
        self.assertEqual(scan.scan_lab(lab), [])

    def test_prose_that_only_mentions_the_variable_does_not_satisfy_the_rule(self):
        lab = guided(
            ["Look into `$AccountId` later.", "Set `$BoundaryArn` later."],
            [
                "aws budgets delete-budget --account-id $AccountId --budget-name b",
                "aws iam delete-policy --policy-arn $BoundaryArn",
            ],
        )
        errors = scan.scan_lab(lab)
        self.assertTrue(any("$AccountId but nothing sets" in e for e in errors))
        self.assertTrue(any("$BoundaryArn but nothing sets" in e for e in errors))

    # -- PY-R3-006: case-insensitive variable matching, `${Var}`, `If (` ----

    def test_variable_case_mismatch_is_not_flagged(self):
        lab = guided(
            ["Run `$VpcId = aws ec2 create-vpc --cidr-block 10.0.0.0/16`."],
            ["aws ec2 delete-vpc --vpc-id $vpcid"],
        )
        self.assertEqual(scan.scan_lab(lab), [])

    def test_braced_variable_is_recognized(self):
        lab = guided(
            ["Run `$VpcId = aws ec2 create-vpc --cidr-block 10.0.0.0/16`."],
            ["aws ec2 delete-vpc --vpc-id ${VpcId}"],
        )
        self.assertEqual(scan.scan_lab(lab), [])

    def test_pwd_automatic_variable_is_not_flagged(self):
        lab = guided([], ["Remove-Item $PWD/out.json"])
        self.assertFalse(any("but nothing sets" in e for e in scan.scan_lab(lab)))

    def test_uppercase_if_guard_is_recognized(self):
        lab = unguided(["# Uses: $VpcId", "If ($VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }"])
        self.assertEqual(scan.scan_lab(lab), [])


class ContentLintDuplicateCriterionTests(SimpleTestCase):
    """TEACHER-R3-001: two identical acceptanceCriteria entries should fail,
    normalising whitespace and case first."""

    def test_duplicate_criteria_detected(self):
        criteria = [
            "The VPC no longer exists.",
            "The subnet no longer exists.",
            "the vpc   no longer exists.",
        ]
        dups = content_lint.find_duplicate_criteria(criteria)
        self.assertEqual(dups, ["the vpc   no longer exists."])

    def test_distinct_criteria_pass(self):
        criteria = ["The VPC no longer exists.", "The subnet no longer exists."]
        self.assertEqual(content_lint.find_duplicate_criteria(criteria), [])
