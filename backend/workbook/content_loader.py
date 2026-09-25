import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings


class ContentNotFoundError(FileNotFoundError):
    pass


def content_root() -> Path:
    return Path(settings.CONTENT_ROOT)


def _read_json(path: Path) -> dict:
    if not path.is_file():
        raise ContentNotFoundError(str(path))
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def list_content_ids(subdir: str) -> list[str]:
    directory = content_root() / subdir
    if not directory.is_dir():
        return []
    ids: list[str] = []
    for path in sorted(directory.glob("*.json")):
        ids.append(path.stem)
    return ids


def load_lesson(lesson_id: str) -> dict:
    return _read_json(content_root() / "lessons" / f"{lesson_id}.json")


def load_question(question_id: str) -> dict:
    return _read_json(content_root() / "questions" / f"{question_id}.json")


def load_lab(lab_id: str) -> dict:
    return _read_json(content_root() / "labs" / f"{lab_id}.json")


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
        rows.append({"id": lesson_id, "title": lesson.get("title") or lesson_id})
    return rows


def content_summary() -> dict:
    root = content_root()
    return {
        "lessons": list_content_ids("lessons"),
        "lessonIndex": lesson_index(),
        "questions": list_content_ids("questions"),
        "labs": list_content_ids("labs"),
        "objectives": {
            "saa": _read_json(root / "objectives" / "saa_c03.json")
            if (root / "objectives" / "saa_c03.json").is_file()
            else [],
            "terraform": _read_json(root / "objectives" / "terraform_004.json")
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
    rows = _read_json(path)
    return {row["id"]: row["domain_id"] for row in rows}


@lru_cache(maxsize=1)
def terraform_objective_group_map() -> dict[str, int]:
    root = content_root()
    path = root / "objectives" / "terraform_004.json"
    if not path.is_file():
        return {}
    rows = _read_json(path)
    return {row["id"]: int(row["group"]) for row in rows}


def question_track(question: dict) -> str:
    for objective_id in question.get("objectiveIds") or []:
        if objective_id.startswith("SAA-"):
            return "aws"
        if objective_id.startswith("tf."):
            return "terraform"
    return "aws"
