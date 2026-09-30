import json
import tempfile
from pathlib import Path

from django.test import Client, TestCase, override_settings

from workbook.content_loader import (
    ContentParseError,
    _read_json,
    load_lab,
    load_question,
    saa_objective_domain_map,
    terraform_objective_group_map,
)
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

    def test_summary_serves_exercise_constraints_and_rubric(self):
        rows = self.client.get("/api/content/summary").json()["exerciseIndex"]
        self.assertTrue(rows)
        for row in rows:
            self.assertIsInstance(row["constraints"], list)
            self.assertIsInstance(row["requiredArtifact"], str)
            for item in row["rubric"]:
                self.assertEqual(set(item), {"label", "points"})
        self.assertTrue(any(row["rubric"] and row["constraints"] for row in rows))


class ContentParseTests(TestCase):
    def test_loader_rejects_corrupt_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ContentParseError) as caught:
                _read_json(path)
        self.assertIn("broken.json", str(caught.exception))
        self.assertIn("not valid JSON", str(caught.exception))

    def test_corrupt_files_return_json_500_through_real_views(self):
        bad_files = {
            "syntax": "{".encode("utf-8"),
            "utf16": '{"id": "q"}'.encode("utf-16"),
            "wrong-type": b"[]",
        }
        for label, raw in bad_files.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for sub in ("questions", "lessons", "labs", "coverage"):
                    (root / sub).mkdir()
                (root / "questions" / "q-bad.json").write_bytes(raw)
                (root / "lessons" / "l-bad.json").write_bytes(raw)
                (root / "labs" / "lab-bad.json").write_bytes(raw)
                (root / "coverage" / "saa_registry.json").write_bytes(raw)
                routes = [
                    "/api/questions/q-bad",
                    "/api/lessons/l-bad",
                    "/api/labs/lab-bad",
                    "/api/content/catalog",
                    "/api/content/summary",
                    "/api/coverage",
                    "/api/metrics/readiness",
                ]
                with override_settings(CONTENT_ROOT=root), self.assertLogs(
                    "workbook.views", "ERROR"
                ):
                    for route in routes:
                        response = Client().get(route)
                        self.assertEqual(response.status_code, 500, route)
                        self.assertTrue(
                            response["Content-Type"].startswith("application/json"),
                            route,
                        )
                        self.assertIn("Content file", response.json()["error"], route)

                    client = Client(enforce_csrf_checks=True)
                    client.get("/api/health")
                    token = client.cookies["csrftoken"].value
                    attempt = client.post(
                        "/api/attempts",
                        data=json.dumps(
                            {
                                "questionId": "q-bad",
                                "selectedIds": ["a"],
                                "mode": "practice",
                            }
                        ),
                        content_type="application/json",
                        HTTP_ORIGIN="http://127.0.0.1:5173",
                        HTTP_X_CSRFTOKEN=token,
                    )
                    self.assertEqual(attempt.status_code, 500, "/api/attempts")
                    self.assertTrue(
                        attempt["Content-Type"].startswith("application/json"),
                        "/api/attempts",
                    )
                    self.assertIn("Content file", attempt.json()["error"], "/api/attempts")

    def test_question_with_bad_choices_shape_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "questions").mkdir()
            (root / "questions" / "q-bad-choices.json").write_text(
                json.dumps({"id": "q-bad-choices", "choices": "ab"}), encoding="utf-8"
            )
            with override_settings(CONTENT_ROOT=root):
                with self.assertRaises(ContentParseError):
                    load_question("q-bad-choices")

    def test_objective_row_missing_fields_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "objectives").mkdir()
            (root / "objectives" / "saa_c03.json").write_text(
                json.dumps([{"domain_id": "d1"}]), encoding="utf-8"
            )
            (root / "objectives" / "terraform_004.json").write_text(
                json.dumps([{"id": "tf.1"}]), encoding="utf-8"
            )
            saa_objective_domain_map.cache_clear()
            terraform_objective_group_map.cache_clear()
            try:
                with override_settings(CONTENT_ROOT=root):
                    with self.assertRaises(ContentParseError):
                        saa_objective_domain_map()
                    with self.assertRaises(ContentParseError):
                        terraform_objective_group_map()
            finally:
                saa_objective_domain_map.cache_clear()
                terraform_objective_group_map.cache_clear()

    # -- PY-R4-010: element types inside lists ------------------------------

    def test_question_with_bad_choice_id_shape_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "questions").mkdir()
            (root / "questions" / "q-bad-choice-id.json").write_text(
                json.dumps({"id": "q-bad-choice-id", "choices": [{"id": ["a"]}]}),
                encoding="utf-8",
            )
            with override_settings(CONTENT_ROOT=root):
                with self.assertRaises(ContentParseError):
                    load_question("q-bad-choice-id")

    def test_question_with_good_choice_ids_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "questions").mkdir()
            (root / "questions" / "q-good-choices.json").write_text(
                json.dumps(
                    {
                        "id": "q-good-choices",
                        "choices": [{"id": "a"}, {"id": "b"}],
                        "objectiveIds": ["SAA-1"],
                        "correctAnswerIds": ["a"],
                    }
                ),
                encoding="utf-8",
            )
            with override_settings(CONTENT_ROOT=root):
                question = load_question("q-good-choices")
        self.assertEqual(question["id"], "q-good-choices")

    def test_question_with_non_string_objective_id_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "questions").mkdir()
            (root / "questions" / "q-bad-objectives.json").write_text(
                json.dumps({"id": "q-bad-objectives", "objectiveIds": [1]}), encoding="utf-8"
            )
            with override_settings(CONTENT_ROOT=root):
                with self.assertRaises(ContentParseError):
                    load_question("q-bad-objectives")

    def test_question_with_non_string_correct_answer_id_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "questions").mkdir()
            (root / "questions" / "q-bad-correct.json").write_text(
                json.dumps({"id": "q-bad-correct", "correctAnswerIds": [["a"]]}),
                encoding="utf-8",
            )
            with override_settings(CONTENT_ROOT=root):
                with self.assertRaises(ContentParseError):
                    load_question("q-bad-correct")

    def test_lab_with_non_list_steps_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs").mkdir()
            (root / "labs" / "lab-bad-steps.json").write_text(
                json.dumps({"id": "lab-bad-steps", "steps": 7}), encoding="utf-8"
            )
            with override_settings(CONTENT_ROOT=root):
                with self.assertRaises(ContentParseError):
                    load_lab("lab-bad-steps")

    def test_lab_with_non_list_acceptance_criteria_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs").mkdir()
            (root / "labs" / "lab-bad-criteria.json").write_text(
                json.dumps({"id": "lab-bad-criteria", "acceptanceCriteria": 5}), encoding="utf-8"
            )
            with override_settings(CONTENT_ROOT=root):
                with self.assertRaises(ContentParseError):
                    load_lab("lab-bad-criteria")

    def test_lab_with_good_shape_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs").mkdir()
            (root / "labs" / "lab-good.json").write_text(
                json.dumps(
                    {
                        "id": "lab-good",
                        "steps": [{"id": "s01", "bullets": []}],
                        "acceptanceCriteria": ["a", "b"],
                    }
                ),
                encoding="utf-8",
            )
            with override_settings(CONTENT_ROOT=root):
                lab = load_lab("lab-good")
        self.assertEqual(lab["id"], "lab-good")

    def test_summary_route_500s_on_a_lab_with_bad_steps_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for sub in ("questions", "lessons", "labs", "coverage"):
                (root / sub).mkdir()
            (root / "labs" / "lab-bad.json").write_text(
                json.dumps({"id": "lab-bad", "steps": "not-a-list"}), encoding="utf-8"
            )
            (root / "coverage" / "saa_registry.json").write_text(json.dumps({"rows": []}), encoding="utf-8")
            with override_settings(CONTENT_ROOT=root), self.assertLogs("workbook.views", "ERROR"):
                response = Client().get("/api/content/summary")
        self.assertEqual(response.status_code, 500)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        self.assertIn("Content file", response.json()["error"])

    def test_saa_objective_row_with_non_string_id_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "objectives").mkdir()
            (root / "objectives" / "saa_c03.json").write_text(
                json.dumps([{"id": ["x"], "domain_id": "d1"}]), encoding="utf-8"
            )
            saa_objective_domain_map.cache_clear()
            try:
                with override_settings(CONTENT_ROOT=root):
                    with self.assertRaises(ContentParseError):
                        saa_objective_domain_map()
            finally:
                saa_objective_domain_map.cache_clear()

    def test_terraform_objective_row_with_bool_group_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "objectives").mkdir()
            (root / "objectives" / "terraform_004.json").write_text(
                json.dumps([{"id": "tf.1", "group": True}]), encoding="utf-8"
            )
            terraform_objective_group_map.cache_clear()
            try:
                with override_settings(CONTENT_ROOT=root):
                    with self.assertRaises(ContentParseError):
                        terraform_objective_group_map()
            finally:
                terraform_objective_group_map.cache_clear()

    def test_terraform_objective_row_with_float_group_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "objectives").mkdir()
            (root / "objectives" / "terraform_004.json").write_text(
                json.dumps([{"id": "tf.1", "group": 1.9}]), encoding="utf-8"
            )
            terraform_objective_group_map.cache_clear()
            try:
                with override_settings(CONTENT_ROOT=root):
                    with self.assertRaises(ContentParseError):
                        terraform_objective_group_map()
            finally:
                terraform_objective_group_map.cache_clear()

    def test_terraform_objective_row_with_good_int_group_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "objectives").mkdir()
            (root / "objectives" / "terraform_004.json").write_text(
                json.dumps([{"id": "tf.1", "group": 3}]), encoding="utf-8"
            )
            terraform_objective_group_map.cache_clear()
            try:
                with override_settings(CONTENT_ROOT=root):
                    self.assertEqual(terraform_objective_group_map(), {"tf.1": 3})
            finally:
                terraform_objective_group_map.cache_clear()
