"""Content lint gates from the workbook plan."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

AKIA = re.compile(r"AKIA[0-9A-Z]{16}")
ACCOUNT = re.compile(r"\b\d{12}\b")


def load_all(folder: str):
    return [json.loads(p.read_text(encoding="utf-8")) for p in (CONTENT / folder).glob("*.json")]


def _normalize_criterion(text) -> str:
    normalized = re.sub(r"\s+", " ", str(text)).strip().lower()
    return normalized.rstrip(".")


def find_duplicate_criteria(criteria: list) -> list[str]:
    """Return the criteria (original text) that repeat, once each, comparing
    entries with whitespace collapsed and case folded."""
    seen: set[str] = set()
    duplicates: list[str] = []
    for c in criteria:
        norm = _normalize_criterion(c)
        if norm in seen:
            duplicates.append(str(c))
        seen.add(norm)
    return duplicates


def _is_list_of(value, item_type: type) -> bool:
    """True if `value` is missing/None (an absent field is fine — loader
    treats it as empty) or a list whose items are all `item_type`. Mirrors
    the shapes `content_loader.py` enforces at load time (PY-R4-010), so
    lint can catch a bad shape before the API turns it into a 500."""
    if value is None:
        return True
    if not isinstance(value, list):
        return False
    return all(isinstance(item, item_type) for item in value)


def check_question_shape(question: dict) -> list[str]:
    """Shape errors for one question, matching `load_question`'s checks:
    `choices` a list of objects with string `id`s, `objectiveIds` and
    `correctAnswerIds` lists of strings."""
    errors: list[str] = []
    qid = question.get("id", "?")
    choices = question.get("choices")
    if not _is_list_of(choices, dict):
        errors.append(f"{qid} 'choices' must be a list of objects")
    elif choices:
        for choice in choices:
            if not isinstance(choice.get("id"), str):
                errors.append(f"{qid} has a choice with a non-string 'id'")
                break
    if not _is_list_of(question.get("objectiveIds"), str):
        errors.append(f"{qid} 'objectiveIds' must be a list of strings")
    if not _is_list_of(question.get("correctAnswerIds"), str):
        errors.append(f"{qid} 'correctAnswerIds' must be a list of strings")
    return errors


def check_lab_shape(lab: dict) -> list[str]:
    """Shape errors for one lab, matching `load_lab`'s checks: `steps` a
    list of objects, `acceptanceCriteria` a list of strings."""
    errors: list[str] = []
    lab_id = lab.get("id", "?")
    if not _is_list_of(lab.get("steps"), dict):
        errors.append(f"{lab_id} 'steps' must be a list of objects")
    if not _is_list_of(lab.get("acceptanceCriteria"), str):
        errors.append(f"{lab_id} 'acceptanceCriteria' must be a list of strings")
    return errors


def main() -> int:
    errors: list[str] = []

    questions = [
        json.loads(p.read_text(encoding="utf-8")) for p in (CONTENT / "questions").glob("q-*.json")
    ]
    labs = load_all("labs")
    lessons = load_all("lessons")
    reg = json.loads((CONTENT / "coverage" / "saa_registry.json").read_text(encoding="utf-8"))

    # registry
    ids = [r["objective_id"] for r in reg["rows"]]
    if len(ids) != 189:
        errors.append(f"registry count {len(ids)} != 189")
    if len(set(ids)) != 189:
        errors.append("duplicate registry ids")

    # questions floors
    aws_q = [q for q in questions if str(q.get("module", "")).startswith("A")]
    tf_q = [q for q in questions if str(q.get("module", "")).startswith("T")]
    if len(aws_q) < 210:
        errors.append(f"AWS questions {len(aws_q)} < 210")
    if len(tf_q) < 111:
        errors.append(f"TF questions {len(tf_q)} < 111")

    by_mod = Counter(q.get("module") for q in questions)
    for m, n in by_mod.items():
        if m and n < 20 and m not in ("A0",):
            # A0 may be small
            if m.startswith(("A", "T")) and m != "A0" and n < 20:
                errors.append(f"module {m} has {n} < 20 questions")

    for q in questions:
        errors.extend(check_question_shape(q))
        if q.get("type") not in ("mc", "mr"):
            errors.append(f"{q['id']} bad type {q.get('type')}")
        if not q.get("rationale"):
            errors.append(f"{q['id']} missing rationale")
        if not q.get("objectiveIds"):
            errors.append(f"{q['id']} missing objectives")
        if q.get("type") == "mr" and not q.get("selectCount"):
            errors.append(f"{q['id']} MR missing selectCount")
        blob = json.dumps(q)
        if AKIA.search(blob):
            errors.append(f"{q['id']} AKIA pattern")

    # labs
    guided = [l for l in labs if l.get("kind") == "guided"]
    unguided = [l for l in labs if l.get("kind") == "unguided"]
    if len(guided) < 20:
        errors.append(f"guided labs {len(guided)} < 20")
    if len(unguided) < 20:
        errors.append(f"unguided labs {len(unguided)} < 20")
    for lab in labs:
        errors.extend(check_lab_shape(lab))
        crit = lab.get("acceptanceCriteria") or []
        for dup in find_duplicate_criteria(crit):
            errors.append(f"{lab['id']} duplicate acceptance criterion: {dup[:80]}")

    for lab in guided:
        steps = lab.get("steps") or []
        if len(steps) < 15:
            errors.append(f"{lab['id']} steps {len(steps)} < 15")
        td = lab.get("teardown") or {}
        if not td.get("orderedDeletesPowerShell"):
            errors.append(f"{lab['id']} teardown missing deletes")
        if not td.get("verification"):
            errors.append(f"{lab['id']} teardown missing verification")
        if not td.get("stillBillingNote"):
            errors.append(f"{lab['id']} teardown missing stillBillingNote")

    for lab in unguided:
        crit = lab.get("acceptanceCriteria") or []
        if len(crit) < 15:
            errors.append(f"{lab['id']} criteria {len(crit)} < 15")
        if not (lab.get("teardown") or {}).get("orderedDeletesPowerShell"):
            errors.append(f"{lab['id']} teardown missing")

    # skill coverage
    for r in reg["rows"]:
        if r["bullet_kind"] == "knowledge":
            if not r.get("lesson_refs") or not r.get("drill_refs"):
                errors.append(f"{r['objective_id']} knowledge missing lesson/drill")
        else:
            if not (r.get("guided_refs") or r.get("unguided_refs") or r.get("exercise_refs")):
                errors.append(f"{r['objective_id']} skill missing practice")

    question_ids = {q["id"] for q in questions}
    for lesson in lessons:
        for drill_id in lesson.get("drillIds") or []:
            if drill_id not in question_ids:
                errors.append(f"{lesson['id']} drillId missing file: {drill_id}")

    # banned copy
    banned = ["chance of passing", "probability of passing", "scaled score of"]
    for folder in ("questions", "lessons", "labs", "exercises"):
        for p in (CONTENT / folder).glob("*.json"):
            text = p.read_text(encoding="utf-8").lower()
            for b in banned:
                if b in text:
                    errors.append(f"{p.name} contains banned phrase: {b}")

    template_stems = [
        q["id"]
        for q in questions
        if (q.get("stem") or "").startswith("Which statement best reflects this exam objective")
    ]
    if template_stems:
        errors.append(f"template stems remaining: {len(template_stems)}")

    by_module: dict[str, Counter] = {}
    for q in questions:
        if q.get("type") != "mc":
            continue
        keys = q.get("correctAnswerIds") or []
        if len(keys) != 1:
            continue
        mod = q.get("module") or "?"
        by_module.setdefault(mod, Counter())[keys[0]] += 1
    for mod, counts in by_module.items():
        total = sum(counts.values())
        if total < 8:
            continue
        top = counts.most_common(1)[0][1]
        if top / total > 0.45:
            errors.append(f"{mod} MC key {counts.most_common(1)[0][0]} is {top}/{total}")

    print("questions", len(questions), "aws", len(aws_q), "tf", len(tf_q))
    print("labs", len(guided), "+", len(unguided))
    print("lessons", len(lessons))
    if errors:
        print("FAIL", len(errors))
        for e in errors[:40]:
            print(" -", e)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
