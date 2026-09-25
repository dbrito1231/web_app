from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.utils import timezone

from workbook.content_loader import (
    saa_objective_domain_map,
    terraform_objective_group_map,
)
from workbook.models import Attempt

AWS_DOMAIN_WEIGHTS = {"d1": 30, "d2": 26, "d3": 24, "d4": 20}
AWS_DOMAINS = ("d1", "d2", "d3", "d4")
TF_GROUPS = tuple(range(1, 9))

AWS_MIN_ITEMS = 40
AWS_MIN_PER_DOMAIN = 5
TF_MIN_ITEMS = 30
TF_MIN_PER_GROUP = 2

SAA_OBJECTIVE_COUNT = 189
TF_OBJECTIVE_COUNT = 37


def _attempt_track(attempt: Attempt, question_objectives: dict[str, list[str]]) -> str:
    for objective_id in question_objectives.get(attempt.question_id, []):
        if objective_id.startswith("SAA-"):
            return "aws"
        if objective_id.startswith("tf."):
            return "terraform"
    if attempt.question_id.startswith("q-t"):
        return "terraform"
    return "aws"


def _build_question_objectives(content_questions: dict[str, dict]) -> dict[str, list[str]]:
    return {
        qid: q.get("objectiveIds") or [] for qid, q in content_questions.items()
    }


def _domain_for_attempt(
    attempt: Attempt, question_objectives: dict[str, list[str]]
) -> str | None:
    domain_map = saa_objective_domain_map()
    for objective_id in question_objectives.get(attempt.question_id, []):
        if objective_id in domain_map:
            return domain_map[objective_id]
    return None


def _group_for_attempt(
    attempt: Attempt, question_objectives: dict[str, list[str]]
) -> int | None:
    group_map = terraform_objective_group_map()
    for objective_id in question_objectives.get(attempt.question_id, []):
        if objective_id in group_map:
            return group_map[objective_id]
    return None


def _weighted_accuracy(
    buckets: dict[str, list[Attempt]], weights: dict[str, int]
) -> float:
    used = {k: v for k, v in buckets.items() if v}
    if not used:
        return 0.0
    total_weight = sum(weights[k] for k in used)
    if total_weight == 0:
        return 0.0
    score = 0.0
    for key, attempts in used.items():
        correct = sum(1 for a in attempts if a.correct)
        acc = correct / len(attempts)
        score += acc * (weights[key] / total_weight)
    return score


def _objective_coverage(
    attempts: list[Attempt], question_objectives: dict[str, list[str]], track: str
) -> float:
    covered: set[str] = set()
    for attempt in attempts:
        for objective_id in question_objectives.get(attempt.question_id, []):
            if track == "aws" and objective_id.startswith("SAA-"):
                covered.add(objective_id)
            if track == "terraform" and objective_id.startswith("tf."):
                covered.add(objective_id)
    total = SAA_OBJECTIVE_COUNT if track == "aws" else TF_OBJECTIVE_COUNT
    return len(covered) / total if total else 0.0


def _recent_accuracy(attempts: list[Attempt], *, days: int = 14) -> tuple[float, int]:
    cutoff = timezone.now() - timedelta(days=days)
    recent = [a for a in attempts if a.submitted_at >= cutoff]
    if not recent:
        return 0.0, 0
    correct = sum(1 for a in recent if a.correct)
    return correct / len(recent), len(recent)


def _compute_readiness(
    attempts: list[Attempt],
    question_objectives: dict[str, list[str]],
    *,
    track: str,
    bucket_fn,
    weights: dict,
    min_items: int,
    min_per_bucket: int,
    bucket_keys: tuple,
) -> dict[str, Any]:
    track_attempts = [
        a
        for a in attempts
        if _attempt_track(a, question_objectives) == track
    ]
    buckets: dict[Any, list[Attempt]] = {k: [] for k in bucket_keys}
    for attempt in track_attempts:
        bucket = bucket_fn(attempt, question_objectives)
        if bucket is not None and bucket in buckets:
            buckets[bucket].append(attempt)

    total_first = len(track_attempts)
    missing: dict[str, int] = {}
    insufficient = total_first < min_items
    for key in bucket_keys:
        count = len(buckets[key])
        if count < min_per_bucket:
            insufficient = True
            missing[str(key)] = min_per_bucket - count

    if insufficient:
        return {
            "status": "insufficient_evidence",
            "firstAttemptCount": total_first,
            "missingPerBucket": missing,
            "message": "Insufficient evidence until practice thresholds are met.",
        }

    weighted_first = _weighted_accuracy(buckets, weights)
    objective_cov = _objective_coverage(track_attempts, question_objectives, track)
    recent_acc, recent_n = _recent_accuracy(track_attempts)

    if recent_n >= 10:
        readiness = round(
            100
            * (0.70 * weighted_first + 0.20 * objective_cov + 0.10 * recent_acc)
        )
        components = {
            "weightedFirstAttemptAccuracy": round(weighted_first * 100),
            "objectiveCoverage": round(objective_cov * 100),
            "recentAccuracy": round(recent_acc * 100),
            "recentItemCount": recent_n,
        }
    else:
        readiness = round(
            100 * (0.80 * weighted_first + 0.20 * objective_cov)
        )
        components = {
            "weightedFirstAttemptAccuracy": round(weighted_first * 100),
            "objectiveCoverage": round(objective_cov * 100),
            "recentAccuracy": None,
            "recentItemCount": recent_n,
            "note": "Recent-accuracy weight folded into first-attempt (fewer than 10 items in 14 days).",
        }

    return {
        "status": "ok",
        "readiness": readiness,
        "firstAttemptCount": total_first,
        "components": components,
        "caption": (
            "Weighted summary of this workbook's practice, not a prediction, "
            "does not include exam-day form difficulty."
        ),
    }


def compute_readiness_metrics(
    question_objectives: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    if question_objectives is None:
        question_objectives = {}

    attempts = list(
        Attempt.objects.filter(
            mode=Attempt.MODE_EXAM,
            assisted=False,
            is_first_exam_attempt=True,
        )
    )

    aws = _compute_readiness(
        attempts,
        question_objectives,
        track="aws",
        bucket_fn=_domain_for_attempt,
        weights=AWS_DOMAIN_WEIGHTS,
        min_items=AWS_MIN_ITEMS,
        min_per_bucket=AWS_MIN_PER_DOMAIN,
        bucket_keys=AWS_DOMAINS,
    )
    terraform = _compute_readiness(
        attempts,
        question_objectives,
        track="terraform",
        bucket_fn=_group_for_attempt,
        weights={g: 1 for g in TF_GROUPS},
        min_items=TF_MIN_ITEMS,
        min_per_bucket=TF_MIN_PER_GROUP,
        bucket_keys=TF_GROUPS,
    )
    terraform.setdefault(
        "groupWeightNote",
        "Terraform groups use equal weights; HashiCorp publishes none.",
    )

    return {"aws": aws, "terraform": terraform}
