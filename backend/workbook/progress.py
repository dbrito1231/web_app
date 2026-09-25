from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation
from typing import Any

from django.db import transaction

from workbook.models import Attempt, CostEntry, LabCheckpoint, SettingBlob

SCHEMA_VERSION = 1
IMPORT_MAX_BYTES = 2 * 1024 * 1024


def export_progress() -> dict[str, Any]:
    attempts = [
        {
            "questionId": a.question_id,
            "mode": a.mode,
            "presentedOrder": a.presented_order,
            "selectedIds": a.selected_ids,
            "correct": a.correct,
            "assisted": a.assisted,
            "isFirstExamAttempt": a.is_first_exam_attempt,
            "submittedAt": a.submitted_at.isoformat(),
        }
        for a in Attempt.objects.all().order_by("submitted_at")
    ]
    lab_checkpoints = [
        {
            "labId": c.lab_id,
            "checkpointId": c.checkpoint_id,
            "status": c.status,
            "updatedAt": c.updated_at.isoformat(),
        }
        for c in LabCheckpoint.objects.all().order_by("lab_id", "checkpoint_id")
    ]
    cost_entries = [
        {
            "description": e.description,
            "amountUsd": str(e.amount_usd),
            "labId": e.lab_id,
            "recordedAt": e.recorded_at.isoformat(),
        }
        for e in CostEntry.objects.all().order_by("recorded_at")
    ]
    settings = {
        blob.key: blob.value for blob in SettingBlob.objects.all().order_by("key")
    }
    return {
        "schemaVersion": SCHEMA_VERSION,
        "attempts": attempts,
        "labCheckpoints": lab_checkpoints,
        "costEntries": cost_entries,
        "settings": settings,
    }


def _clear_progress() -> None:
    Attempt.objects.all().delete()
    LabCheckpoint.objects.all().delete()
    CostEntry.objects.all().delete()
    SettingBlob.objects.all().delete()


@transaction.atomic
def import_progress(payload: dict[str, Any]) -> None:
    version = payload.get("schemaVersion")
    if version is None:
        raise ValueError("Missing schemaVersion")
    if not isinstance(version, int):
        raise ValueError("schemaVersion must be an integer")
    if version > SCHEMA_VERSION:
        raise ValueError(f"Unsupported schemaVersion {version}")
    if version != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schemaVersion {version}")

    _clear_progress()

    for row in payload.get("attempts") or []:
        Attempt.objects.create(
            question_id=row["questionId"],
            mode=row["mode"],
            presented_order=row.get("presentedOrder") or [],
            selected_ids=row.get("selectedIds") or [],
            correct=bool(row["correct"]),
            assisted=bool(row.get("assisted", False)),
            is_first_exam_attempt=bool(row.get("isFirstExamAttempt", False)),
        )
    for row in payload.get("labCheckpoints") or []:
        LabCheckpoint.objects.create(
            lab_id=row["labId"],
            checkpoint_id=row["checkpointId"],
            status=row.get("status", LabCheckpoint.STATUS_NOT_STARTED),
        )
    for row in payload.get("costEntries") or []:
        try:
            amount = Decimal(str(row["amountUsd"]))
        except (InvalidOperation, KeyError, TypeError) as exc:
            raise ValueError("Invalid cost entry amount") from exc
        CostEntry.objects.create(
            description=row["description"],
            amount_usd=amount,
            lab_id=row.get("labId") or "",
        )
    for key, value in (payload.get("settings") or {}).items():
        SettingBlob.objects.create(key=key, value=value)


def parse_import_body(raw: bytes) -> dict[str, Any]:
    if len(raw) > IMPORT_MAX_BYTES:
        raise ValueError("Import payload too large")
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON") from exc


def _best_by_question() -> dict[str, int]:
    best: dict[str, int] = {}
    for row in Attempt.objects.values("question_id", "correct"):
        score = 100 if row["correct"] else 0
        question_id = row["question_id"]
        best[question_id] = max(best.get(question_id, 0), score)
    return best


def get_progress_snapshot() -> dict[str, Any]:
    return {
        "attemptCounts": {
            "total": Attempt.objects.count(),
            "examFirstAttempts": Attempt.objects.filter(
                mode=Attempt.MODE_EXAM, is_first_exam_attempt=True, assisted=False
            ).count(),
        },
        "labCheckpoints": list(
            LabCheckpoint.objects.values("lab_id", "checkpoint_id", "status")
        ),
        "costEntryCount": CostEntry.objects.count(),
        "settingsKeys": list(
            SettingBlob.objects.values_list("key", flat=True).order_by("key")
        ),
        "bestByQuestion": _best_by_question(),
    }


@transaction.atomic
def reset_progress() -> None:
    _clear_progress()
