import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import Client, TestCase

from workbook.content_loader import ContentParseError, _read_json, load_question
from workbook.models import Attempt
from workbook.progress import import_progress
from workbook.readiness import compute_readiness_metrics
from workbook.scoring import score_question


class ScoringTests(TestCase):
    def test_mc_all_or_nothing_correct(self):
        question = {"correctAnswerIds": ["b"]}
        self.assertTrue(score_question(question, ["b"]))
        self.assertFalse(score_question(question, ["a"]))

    def test_mr_all_or_nothing_partial_wrong(self):
        question = {"correctAnswerIds": ["a", "c"]}
        self.assertTrue(score_question(question, ["a", "c"]))
        self.assertFalse(score_question(question, ["a"]))
        self.assertFalse(score_question(question, ["a", "c", "d"]))


class ReadinessTests(TestCase):
    def test_insufficient_evidence_by_default(self):
        metrics = compute_readiness_metrics({})
        self.assertEqual(metrics["aws"]["status"], "insufficient_evidence")
        self.assertEqual(metrics["terraform"]["status"], "insufficient_evidence")


class ImportResetTests(TestCase):
    def test_import_rejects_future_schema(self):
        with self.assertRaises(ValueError):
            import_progress({"schemaVersion": 2, "attempts": []})

    def test_reset_requires_confirm_token(self):
        Attempt.objects.create(
            question_id="q-a0-mc-001",
            mode=Attempt.MODE_EXAM,
            selected_ids=["b"],
            correct=True,
            is_first_exam_attempt=True,
        )
        client = Client(enforce_csrf_checks=False)
        bad = client.post(
            "/api/reset",
            data=json.dumps({"confirm": "NOPE"}),
            content_type="application/json",
        )
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(Attempt.objects.count(), 1)

        ok = client.post(
            "/api/reset",
            data=json.dumps({"confirm": "RESET"}),
            content_type="application/json",
        )
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(Attempt.objects.count(), 0)


class AttemptApiTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_question_hides_answer_key(self):
        resp = self.client.get("/api/questions/q-a0-mc-001")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertNotIn("correctAnswerIds", data)
        self.assertNotIn("rationale", data)

    def test_post_with_vite_origin_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        health = client.get("/api/health")
        self.assertEqual(health.status_code, 200)
        token = client.cookies["csrftoken"].value
        origin = "http://127.0.0.1:5173"
        attempt = client.post(
            "/api/attempts",
            data=json.dumps(
                {
                    "questionId": "q-a0-mc-001",
                    "selectedIds": load_question("q-a0-mc-001")["correctAnswerIds"],
                    "mode": "practice",
                    "assisted": True,
                }
            ),
            content_type="application/json",
            HTTP_ORIGIN=origin,
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(attempt.status_code, 200, attempt.content[:200])
        self.assertIn("rationale", attempt.json())
        checkpoint = client.post(
            "/api/labs/gl-01/checkpoints",
            data=json.dumps({"checkpointId": "s01", "status": "self-reported"}),
            content_type="application/json",
            HTTP_ORIGIN=origin,
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertIn(checkpoint.status_code, (200, 204), checkpoint.content[:200])

    def test_catalog_omits_rationale(self):
        resp = self.client.get("/api/content/catalog")
        self.assertEqual(resp.status_code, 200)
        rows = resp.json()["questions"]
        self.assertGreater(len(rows), 100)
        self.assertNotIn("rationale", rows[0])
        self.assertIn("stem", rows[0])

    def test_attempt_rejects_unknown_choice(self):
        resp = self.client.post(
            "/api/attempts",
            data=json.dumps(
                {
                    "questionId": "q-a0-mc-001",
                    "selectedIds": ["not-a-choice"],
                    "mode": "practice",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_attempt_returns_rationale(self):
        resp = self.client.post(
            "/api/attempts",
            data=json.dumps(
                {
                    "questionId": "q-a0-mc-001",
                    "selectedIds": load_question("q-a0-mc-001")["correctAnswerIds"],
                    "mode": "exam",
                    "assisted": False,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertTrue(body["correct"])
        self.assertIn("rationale", body)

    def test_lab_hides_solution_until_reveal(self):
        hidden = self.client.get("/api/labs/gl-01")
        self.assertNotIn("solution", hidden.json())
        revealed = self.client.get("/api/labs/gl-01?reveal=1")
        self.assertIn("solution", revealed.json())


class ContentParseTests(TestCase):
    def test_loader_rejects_corrupt_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ContentParseError) as caught:
                _read_json(path)
        self.assertIn("broken.json", str(caught.exception))
        self.assertIn("not valid JSON", str(caught.exception))

    def test_question_get_returns_json_500_for_corrupt_file(self):
        with patch(
            "workbook.views.load_question",
            side_effect=ContentParseError(
                "Content file q-bad.json is not valid JSON: Expecting value (line 1)"
            ),
        ):
            response = Client().get("/api/questions/q-bad")
        self.assertEqual(response.status_code, 500)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        self.assertIn("not valid JSON", response.json()["error"])
