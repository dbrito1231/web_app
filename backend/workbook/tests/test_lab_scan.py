import importlib.util
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

_SCRIPT = Path(settings.REPO_ROOT) / "scripts" / "scan_lab_placeholders.py"
_spec = importlib.util.spec_from_file_location("scan_lab_placeholders", _SCRIPT)
scan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan)


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
