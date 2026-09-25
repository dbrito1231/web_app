import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from workbook.content_loader import (
    ContentNotFoundError,
    ContentParseError,
    content_summary,
    list_content_ids,
    load_coverage_registry,
    load_lab,
    load_lesson,
    load_question,
    public_lab,
    public_question,
    question_catalog,
)
from workbook.models import Attempt, LabCheckpoint
from workbook.progress import (
    export_progress,
    get_progress_snapshot,
    import_progress,
    parse_import_body,
    reset_progress,
)
from workbook.readiness import compute_readiness_metrics
from workbook.scoring import score_question

logger = logging.getLogger(__name__)


def _json_error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"error": message}, status=status)


def _parse_json_body(request) -> dict | None:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _content_error(exc: ContentParseError) -> JsonResponse:
    logger.error("Corrupt content file: %s", exc)
    return _json_error(str(exc), 500)


def _question_objectives_map() -> dict[str, list[str]]:
    objectives: dict[str, list[str]] = {}
    for qid in list_content_ids("questions"):
        try:
            question = load_question(qid)
        except ContentNotFoundError:
            continue
        objectives[qid] = question.get("objectiveIds") or []
    return objectives


@ensure_csrf_cookie
@require_GET
def health(_request):
    return JsonResponse({"status": "ok"})


@require_GET
def question_catalog_view(_request):
    try:
        return JsonResponse({"questions": question_catalog()})
    except ContentParseError as exc:
        return _content_error(exc)


@require_GET
def content_summary_view(_request):
    try:
        return JsonResponse(content_summary())
    except FileNotFoundError as exc:
        return _json_error(str(exc), 500)
    except ContentParseError as exc:
        return _content_error(exc)


@require_GET
def lesson_detail(_request, lesson_id: str):
    try:
        return JsonResponse(load_lesson(lesson_id))
    except ContentNotFoundError:
        return _json_error("Lesson not found", 404)
    except ContentParseError as exc:
        return _content_error(exc)


@require_GET
def question_detail(_request, question_id: str):
    try:
        question = load_question(question_id)
    except ContentNotFoundError:
        return _json_error("Question not found", 404)
    except ContentParseError as exc:
        return _content_error(exc)
    return JsonResponse(public_question(question))


@csrf_protect
@require_POST
def create_attempt(request):
    body = _parse_json_body(request)
    if body is None:
        return _json_error("Invalid JSON body")

    question_id = body.get("questionId")
    selected_ids = body.get("selectedIds")
    mode = body.get("mode")
    assisted = bool(body.get("assisted", False))

    if not question_id or not isinstance(selected_ids, list):
        return _json_error("questionId and selectedIds are required")
    if mode not in (Attempt.MODE_PRACTICE, Attempt.MODE_EXAM):
        return _json_error("mode must be practice or exam")
    if any(not isinstance(item, str) for item in selected_ids):
        return _json_error("selectedIds must be strings", 400)
    if len(selected_ids) != len(set(selected_ids)):
        return _json_error("selectedIds must be unique", 400)

    try:
        question = load_question(question_id)
    except ContentNotFoundError:
        return _json_error("Question not found", 404)
    except ContentParseError as exc:
        return _content_error(exc)

    choice_ids = {choice.get("id") for choice in question.get("choices") or []}
    if any(item not in choice_ids for item in selected_ids):
        return _json_error("selectedIds must be choice ids for this question", 400)

    correct = score_question(question, selected_ids)
    is_first_exam = False
    if mode == Attempt.MODE_EXAM and not assisted:
        is_first_exam = not Attempt.objects.filter(
            question_id=question_id,
            mode=Attempt.MODE_EXAM,
            assisted=False,
        ).exists()

    Attempt.objects.create(
        question_id=question_id,
        mode=mode,
        presented_order=body.get("presentedOrder") or [],
        selected_ids=selected_ids,
        correct=correct,
        assisted=assisted,
        is_first_exam_attempt=is_first_exam,
    )

    return JsonResponse(
        {
            "correct": correct,
            "rationale": question.get("rationale", ""),
            "objectiveIds": question.get("objectiveIds") or [],
        }
    )


@require_GET
def lab_detail(request, lab_id: str):
    reveal = request.GET.get("reveal") == "1"
    try:
        lab = load_lab(lab_id)
    except ContentNotFoundError:
        return _json_error("Lab not found", 404)
    except ContentParseError as exc:
        return _content_error(exc)
    return JsonResponse(public_lab(lab, reveal=reveal))


@csrf_protect
@require_POST
def lab_checkpoint(request, lab_id: str):
    body = _parse_json_body(request)
    if body is None:
        return _json_error("Invalid JSON body")

    checkpoint_id = body.get("checkpointId")
    status = body.get("status")
    allowed = {
        LabCheckpoint.STATUS_NOT_STARTED,
        LabCheckpoint.STATUS_SELF_REPORTED,
        LabCheckpoint.STATUS_UNRESOLVED,
    }
    if not checkpoint_id or status not in allowed:
        return _json_error("checkpointId and valid status are required")

    obj, _created = LabCheckpoint.objects.update_or_create(
        lab_id=lab_id,
        checkpoint_id=checkpoint_id,
        defaults={"status": status},
    )
    return JsonResponse(
        {
            "labId": obj.lab_id,
            "checkpointId": obj.checkpoint_id,
            "status": obj.status,
            "updatedAt": obj.updated_at.isoformat(),
        }
    )


@require_GET
def progress_view(_request):
    return JsonResponse(get_progress_snapshot())


@csrf_protect
@require_POST
def export_view(_request):
    return JsonResponse(export_progress())


@csrf_protect
@require_POST
def import_view(request):
    try:
        payload = parse_import_body(request.body)
        import_progress(payload)
    except ValueError as exc:
        return _json_error(str(exc))
    return JsonResponse({"ok": True})


@csrf_protect
@require_POST
def reset_view(request):
    body = _parse_json_body(request)
    if body is None:
        return _json_error("Invalid JSON body")
    if body.get("confirm") != "RESET":
        return _json_error('confirm must be "RESET"')
    reset_progress()
    return JsonResponse({"ok": True})


@require_GET
def readiness_metrics(_request):
    try:
        data = compute_readiness_metrics(_question_objectives_map())
    except ContentParseError as exc:
        return _content_error(exc)
    return JsonResponse(data)


@require_GET
def coverage_registry(_request):
    try:
        payload = load_coverage_registry()
    except ContentNotFoundError:
        return _json_error("Coverage registry not found", 404)
    except ContentParseError as exc:
        return _content_error(exc)
    return JsonResponse(payload)
