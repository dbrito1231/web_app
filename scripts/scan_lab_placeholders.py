"""Read-only scan for lab placeholder and teardown patterns. Exit 1 on failure."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "content" / "labs"

BAD_TAG = re.compile(r"\{\{Key=")
LITERAL_DOTS = re.compile(r"`aws [^`]* \.\.\.")
ENI_VPC = re.compile(r"ENIs, then VPC", re.I)

# Variable reference: `$Name` or `${Name}`. PowerShell names are case-insensitive,
# so callers must compare captured names with `.lower()`.
VAR_REF = re.compile(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?")
ASSIGN = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)\s*(\S*)")
FOREACH = re.compile(r"\bforeach\s*\(\s*\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?", re.I)

# Step prose that stands in for a real assignment, e.g. "Copy that Arn into
# `$BoundaryArn`" or "Set `$AccountId` to ...". Deliberately narrow: it must
# name the exact phrasing, not any sentence that merely mentions the variable
# ("Look into `$X` later" or "Set `$X` later" must NOT match).
PROSE_ASSIGN = re.compile(
    r"\bCopy\b(?:(?!`\$)[^`]){0,80}?\binto\s+`\$([A-Za-z_][A-Za-z0-9_]*)`"
    r"|\bSet\s+`\$([A-Za-z_][A-Za-z0-9_]*)`\s+to\b"
)

USES_HEADER = re.compile(r"^#\s*Uses:\s*(.*)$")
SEGMENT_SPLIT = re.compile(r"[;{}|]")

# `-ErrorAction`/`-EA` is a cmdlet parameter; PowerShell passes it to aws.exe
# (or aws.exe itself) as an unrecognized argument.
AWS_CMD = re.compile(r"(?:^|[\s`(])aws(?:\.exe)?\s", re.I)
ERROR_ACTION = re.compile(r"-(?:ErrorAction|EA)\b", re.I)

IF_OPEN = re.compile(r"^\s*if\s*\(", re.I)
# A guard term is a bare variable, optionally compared with `-eq`/`-ne` to a
# quoted string, `$true` or `$false`. `-eq $null` is rejected explicitly: it
# guards the delete on the value being ABSENT, i.e. an inverted guard.
# Anything else (`-not`, `!`, `-or`, a bare `$true`) fails to match and
# invalidates the whole guard.
GUARD_TERM = re.compile(
    r"^\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?"
    r"(?:\s+-(?P<op>eq|ne)\s+(?P<val>'[^']*'|\"[^\"]*\"|\$null|\$true|\$false))?$",
    re.I,
)
GUARD_AND_SPLIT = re.compile(r"\s+-and\s+", re.I)


def _match_balanced(text: str, open_ch: str, close_ch: str, start: int) -> int | None:
    """Return the index of the bracket matching the opener at `start`
    (text[start] must be `open_ch`), tracking nesting depth. None if the
    brackets in `text` from `start` onward never balance."""
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i
    return None


def _parse_guard(line: str) -> tuple[str, str] | None:
    """Parse a whole delete line as `if (COND) { BODY }`, with only
    whitespace and an optional trailing `;` after the closing brace. Returns
    (cond, body) or None if the line is not exactly that shape. Uses bracket
    depth, not a greedy regex, so nested `if`/`foreach`/`do...while` blocks in
    BODY do not break the parse."""
    stripped = line.strip()
    open_match = IF_OPEN.match(stripped)
    if not open_match:
        return None
    paren_start = open_match.end() - 1
    paren_end = _match_balanced(stripped, "(", ")", paren_start)
    if paren_end is None:
        return None
    cond = stripped[paren_start + 1 : paren_end]
    rest = stripped[paren_end + 1 :].lstrip()
    if not rest.startswith("{"):
        return None
    brace_end = _match_balanced(rest, "{", "}", 0)
    if brace_end is None:
        return None
    body = rest[1:brace_end]
    tail = rest[brace_end + 1 :].strip()
    if tail not in ("", ";"):
        return None
    return cond, body

STRING_LITERAL = re.compile(r"'[^']*'|\"[^\"]*\"")

# PowerShell automatic variables and scope prefixes; never lab resources.
# Compared case-insensitively, so this is already all-lowercase.
AUTOMATIC = {"_", "true", "false", "null", "env", "pwd", "lastexitcode", "psitem"}


def _lower(names) -> set[str]:
    return {n.lower() for n in names}


def _string_spans(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in STRING_LITERAL.finditer(text)]


def _inside_a_string(index: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in spans)


def lab_has_vpc_create(text: str) -> bool:
    return "create-vpc" in text or "create_vpc" in text


def _iter_bullets(steps: list) -> list[str]:
    """Flatten guided-lab step bullets into plain strings. Each bullet is a
    real Python string (unlike `json.dumps(steps)`, which re-quotes it), so
    string-literal stripping and regex matching both work on it directly."""
    bullets: list[str] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        for bullet in step.get("bullets") or []:
            bullets.append(str(bullet))
    return bullets


def _is_reset_rhs(name: str, rhs: str) -> bool:
    rhs_clean = rhs.rstrip(";").strip()
    if rhs_clean.lower() == "$null":
        return True
    if rhs_clean in ("''", '""'):
        return True
    if rhs_clean.lower() == f"${name.lower()}":
        return True
    return False


def _assignments_in(text: str) -> list[tuple[str, bool]]:
    """Return [(name, is_reset), ...] for each assignment whose `$Name =`
    target sits outside any quoted string (so text that only resembles an
    assignment inside a string, e.g. `Write-Host "$X = gone"`, is ignored).
    The right-hand side is read from the original text, unmodified, so a
    real reset such as `$X = ''` or `$X = $null` is still recognized."""
    spans = _string_spans(text)
    results = []
    for match in ASSIGN.finditer(text):
        if _inside_a_string(match.start(), spans):
            continue
        name, rhs = match.group(1), match.group(2)
        results.append((name, _is_reset_rhs(name, rhs)))
    return results


def _assigned_in(text: str) -> set[str]:
    spans = _string_spans(text)
    names = {name for name, is_reset in _assignments_in(text) if not is_reset}
    for match in FOREACH.finditer(text):
        if not _inside_a_string(match.start(), spans):
            names.add(match.group(1))
    return names


def _prose_assigned_in(text: str) -> set[str]:
    names: set[str] = set()
    for match in PROSE_ASSIGN.finditer(text):
        names.add(match.group(1) or match.group(2))
    return names


def _check_error_action(lab_id: str, text: str, errors: list[str]) -> None:
    for segment in SEGMENT_SPLIT.split(text):
        if AWS_CMD.search(segment) and ERROR_ACTION.search(segment):
            errors.append(
                f"{lab_id}: -ErrorAction on an aws command: {segment.strip()[:80]}"
            )


def _guard_covers(line: str, learner_vars: set[str]) -> bool:
    """True if every var in learner_vars is inside a single valid guard
    (`if ($A -and $B) { ... }`) that wraps the whole line."""
    parsed = _parse_guard(line)
    if parsed is None:
        return False
    cond, _body = parsed
    cond = cond.strip()
    if not cond:
        return False
    terms = GUARD_AND_SPLIT.split(cond)
    guard_vars: set[str] = set()
    for term in terms:
        term_match = GUARD_TERM.match(term.strip())
        if not term_match:
            return False
        if term_match.group("op") and term_match.group("op").lower() == "eq" and (
            term_match.group("val") or ""
        ).lower() == "$null":
            return False
        guard_vars.add(term_match.group(1).lower())
    return _lower(learner_vars) <= guard_vars


def scan_lab(data: dict) -> list[str]:
    """Return the problems found in one lab document."""
    errors: list[str] = []
    lab_id = data.get("id", "?")
    blob = json.dumps(data)

    if BAD_TAG.search(blob):
        errors.append(f"{lab_id}: contains {{{{Key= tag syntax")
    if LITERAL_DOTS.search(blob):
        errors.append(f"{lab_id}: contains literal `...` command placeholder")

    steps = data.get("steps") or []
    step_text = json.dumps(steps)
    if ENI_VPC.search(step_text):
        num = int(lab_id.split("-")[1]) if "-" in lab_id else 0
        guided = data.get("kind") == "guided"
        if guided and num >= 10 and not lab_has_vpc_create(blob):
            errors.append(f"{lab_id}: ENIs/VPC boilerplate in steps without create-vpc in file")
        elif guided and num < 10 and lab_id not in ("gl-05", "gl-06", "gl-07", "gl-08"):
            errors.append(f"{lab_id}: generic ENIs/VPC text in non-VPC lab steps")

    bullets = _iter_bullets(steps)

    # -ErrorAction rule: check each bullet, and each teardown line, on its
    # own. Never join separate bullets/lines into one string before matching.
    for bullet in bullets:
        _check_error_action(lab_id, bullet, errors)

    deletes = (data.get("teardown") or {}).get("orderedDeletesPowerShell") or []
    unguided = lab_id.startswith("ul-")

    for line in deletes:
        _check_error_action(lab_id, line, errors)

    non_comment_deletes = [
        line for line in deletes if line.strip() and not line.lstrip().startswith("#")
    ]
    if not non_comment_deletes:
        errors.append(f"{lab_id}: teardown has no delete commands (empty or comments only)")

    seen: set[str] = set()
    for line in deletes:
        if any(is_reset for _name, is_reset in _assignments_in(line)):
            errors.append(f"{lab_id}: teardown resets a variable to $null: {line[:80]}")
        if line in seen:
            errors.append(f"{lab_id}: duplicate teardown line: {line[:80]}")
        seen.add(line)

    declared: set[str] = set()
    if unguided:
        header = USES_HEADER.match(deletes[0]) if deletes else None
        if not header:
            errors.append(f"{lab_id}: unguided teardown must start with a '# Uses:' line")
        else:
            declared = set(VAR_REF.findall(header.group(1)))
        if "# Replace" in "\n".join(deletes):
            errors.append(f"{lab_id}: teardown still has placeholder comments")
        if any("workbook-gl" in line for line in deletes):
            errors.append(f"{lab_id}: unguided teardown names a guided-lab resource (workbook-gl..)")

    assigned: set[str] = set()
    for bullet in bullets:
        assigned |= _assigned_in(bullet)
        assigned |= _prose_assigned_in(bullet)
    for line in deletes:
        if line.lstrip().startswith("#"):
            continue
        made_here = _assigned_in(line)
        used = {
            v
            for v in VAR_REF.findall(line)
            if v.lower() not in AUTOMATIC and v.lower() not in _lower(made_here)
        }
        missing = sorted(
            v for v in used if v.lower() not in _lower(assigned) and v.lower() not in _lower(declared)
        )
        for var in missing:
            errors.append(f"{lab_id}: teardown uses ${var} but nothing sets or declares it")
        if unguided:
            learner_vars = used & declared - assigned
            if learner_vars and not _guard_covers(line, learner_vars):
                errors.append(f"{lab_id}: delete is not guarded by if (...): {line[:80]}")
        # Lookups made in the teardown count for the lines after them.
        assigned |= made_here

    return errors


def main() -> None:
    paths = sorted(LABS.glob("*.json"))
    errors: list[str] = []
    for path in paths:
        errors.extend(scan_lab(json.loads(path.read_text(encoding="utf-8"))))

    if errors:
        print("FAIL", len(errors))
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("PASS", len(paths), "labs scanned")


if __name__ == "__main__":
    main()
