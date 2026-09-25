"""All-or-nothing scoring for MC and MR items."""


def score_question(question: dict, selected_ids: list[str]) -> bool:
    correct_ids = set(question.get("correctAnswerIds") or [])
    selected = set(selected_ids or [])
    return selected == correct_ids
