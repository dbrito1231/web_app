import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings


class ContentNotFoundError(FileNotFoundError):
    pass


class ContentParseError(ValueError):
    """A content file exists but is not valid JSON."""


def content_root() -> Path:
    return Path(settings.CONTENT_ROOT)


def _read_json(path: Path, expect: type | None = None):
    if not path.is_file():
        raise ContentNotFoundError(str(path))
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ContentParseError(
            f"Content file {path.name} is not valid JSON: {exc.msg} (line {exc.lineno})"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ContentParseError(
            f"Content file {path.name} is not UTF-8 text"
        ) from exc
    if expect is not None and not isinstance(data, expect):
        kind = "object" if expect is dict else "list"
        raise ContentParseError(
            f"Content file {path.name} must contain a JSON {kind} at the top level"
        )
    return data


def list_content_ids(subdir: str) -> list[str]:
    directory = content_root() / subdir
    if not directory.is_dir():
        return []
    ids: list[str] = []
    for path in sorted(directory.glob("*.json")):
        ids.append(path.stem)
    return ids


def load_lesson(lesson_id: str) -> dict:
    return _read_json(content_root() / "lessons" / f"{lesson_id}.json", dict)


def _require_optional_list(value, path: Path, field: str, *, item_type: type | None = None) -> None:
    """Raise ContentParseError if `value` is present but not a list (of
    `item_type`, when given). `None`/missing is fine — callers already treat
    an absent field as an empty list. `bool` is never accepted where
    `item_type` is `str`, even though `bool` is technically an `int` subtype
    (not relevant here since `str` items never match `bool`, but kept
    explicit for clarity if a caller later passes `item_type=int`)."""
    if value is None:
        return
    if not isinstance(value, list) or (
        item_type is not None and not all(isinstance(item, item_type) for item in value)
    ):
        if item_type is dict:
            detail = "a list of objects"
        elif item_type is str:
            detail = "a list of strings"
        else:
            detail = "a list"
        raise ContentParseError(
            f"Content file {path.name} field '{field}' must be {detail}"
        )


def _require_choice_ids(choices, path: Path) -> None:
    """Each choice's `id` must be a string; a list/int/etc. is unhashable or
    otherwise breaks `create_attempt`'s `{choice.get("id") for choice in ...}`
    set-build and `score_question`'s set comparisons."""
    if not choices:
        return
    for choice in choices:
        if not isinstance(choice, dict) or not isinstance(choice.get("id"), str):
            raise ContentParseError(
                f"Content file {path.name} has a choice with a non-string 'id'"
            )


def load_question(question_id: str) -> dict:
    path = content_root() / "questions" / f"{question_id}.json"
    question = _read_json(path, dict)
    _require_optional_list(question.get("choices"), path, "choices", item_type=dict)
    _require_choice_ids(question.get("choices"), path)
    _require_optional_list(question.get("objectiveIds"), path, "objectiveIds", item_type=str)
    _require_optional_list(question.get("correctAnswerIds"), path, "correctAnswerIds", item_type=str)
    return question


def load_lab(lab_id: str) -> dict:
    path = content_root() / "labs" / f"{lab_id}.json"
    lab = _read_json(path, dict)
    _require_optional_list(lab.get("steps"), path, "steps", item_type=dict)
    _require_optional_list(lab.get("acceptanceCriteria"), path, "acceptanceCriteria", item_type=str)
    return lab


def load_coverage_registry() -> dict:
    return _read_json(content_root() / "coverage" / "saa_registry.json", dict)


def public_question(question: dict) -> dict:
    payload = dict(question)
    payload.pop("correctAnswerIds", None)
    payload.pop("rationale", None)
    return payload


def public_lab(lab: dict, *, reveal: bool) -> dict:
    payload = dict(lab)
    if not reveal:
        payload.pop("solution", None)
    return payload


def question_catalog() -> list[dict]:
    rows = []
    for question_id in list_content_ids("questions"):
        question = load_question(question_id)
        rows.append(
            {
                "id": question_id,
                "module": question.get("module"),
                "type": question.get("type"),
                "stem": question.get("stem"),
                "selectCount": question.get("selectCount"),
            }
        )
    return rows


def lesson_index() -> list[dict]:
    rows = []
    for lesson_id in list_content_ids("lessons"):
        lesson = load_lesson(lesson_id)
        rows.append(
            {
                "id": lesson_id,
                "title": lesson.get("title") or lesson_id,
                "drillIds": lesson.get("drillIds") or [],
                "objectiveIds": lesson.get("objectiveIds") or [],
            }
        )
    return rows


def lab_index() -> list[dict]:
    rows = []
    for lab_id in list_content_ids("labs"):
        lab = load_lab(lab_id)
        steps = lab.get("steps") or []
        if steps:
            step_ids = [
                step.get("id")
                for step in steps
                if isinstance(step, dict) and step.get("id")
            ]
        else:
            criteria = lab.get("acceptanceCriteria") or []
            step_ids = [f"c{index + 1:02d}" for index, _text in enumerate(criteria)]
        rows.append(
            {
                "id": lab_id,
                "title": lab.get("title") or lab_id,
                "objectiveIds": lab.get("objectiveIds") or [],
                "stepIds": step_ids,
            }
        )
    return rows


def exercise_index() -> list[dict]:
    rows = []
    directory = content_root() / "exercises"
    if not directory.is_dir():
        return rows
    for exercise_id in list_content_ids("exercises"):
        item = _read_json(directory / f"{exercise_id}.json", dict)
        rows.append(
            {
                "id": exercise_id,
                "title": item.get("title") or exercise_id,
                "objectiveIds": item.get("objectiveIds") or [],
                "scenario": item.get("scenario") or "",
            }
        )
    return rows


def content_summary() -> dict:
    root = content_root()
    return {
        "lessons": list_content_ids("lessons"),
        "lessonIndex": lesson_index(),
        "questions": list_content_ids("questions"),
        "labs": list_content_ids("labs"),
        "labIndex": lab_index(),
        "exerciseIndex": exercise_index(),
        "objectives": {
            "saa": _read_json(root / "objectives" / "saa_c03.json", list)
            if (root / "objectives" / "saa_c03.json").is_file()
            else [],
            "terraform": _read_json(root / "objectives" / "terraform_004.json", list)
            if (root / "objectives" / "terraform_004.json").is_file()
            else [],
        },
    }


@lru_cache(maxsize=1)
def saa_objective_domain_map() -> dict[str, str]:
    root = content_root()
    path = root / "objectives" / "saa_c03.json"
    if not path.is_file():
        return {}
    rows = _read_json(path, list)
    result: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or "id" not in row or "domain_id" not in row:
            raise ContentParseError(
                f"Content file {path.name} has an objective row missing 'id' or 'domain_id'"
            )
        if not isinstance(row["id"], str):
            raise ContentParseError(
                f"Content file {path.name} has an objective row with a non-string 'id'"
            )
        result[row["id"]] = row["domain_id"]
    return result


@lru_cache(maxsize=1)
def terraform_objective_group_map() -> dict[str, int]:
    root = content_root()
    path = root / "objectives" / "terraform_004.json"
    if not path.is_file():
        return {}
    rows = _read_json(path, list)
    result: dict[str, int] = {}
    for row in rows:
        if not isinstance(row, dict) or "id" not in row or "group" not in row:
            raise ContentParseError(
                f"Content file {path.name} has an objective row missing 'id' or 'group'"
            )
        if not isinstance(row["id"], str):
            raise ContentParseError(
                f"Content file {path.name} has an objective row with a non-string 'id'"
            )
        group = row["group"]
        # `bool` is an `int` subclass in Python, so `True`/`False` would
        # otherwise silently coerce to 1/0. `1.9` must not truncate to 1.
        if isinstance(group, bool) or not isinstance(group, int):
            raise ContentParseError(
                f"Content file {path.name} has a non-integer 'group' for {row['id']!r}"
            )
        result[row["id"]] = group
    return result


def question_track(question: dict) -> str:
    for objective_id in question.get("objectiveIds") or []:
        if objective_id.startswith("SAA-"):
            return "aws"
        if objective_id.startswith("tf."):
            return "terraform"
    return "aws"
