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
FOREACH_HEADER = re.compile(r"\bforeach\s*\(", re.I)
FOREACH_BIND = re.compile(r"^\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?\s+in\s+(.*)$", re.I)

# Step prose that stands in for a real assignment, e.g. "Copy that Arn into
# `$BoundaryArn`" or "Set `$AccountId` to ...". Deliberately narrow: it must
# name the exact phrasing, not any sentence that merely mentions the variable
# ("Look into `$X` later" or "Set `$X` later" must NOT match).
PROSE_ASSIGN = re.compile(
    r"\bCopy\b(?:(?!`\$)[^`]){0,80}?\binto\s+`\$([A-Za-z_][A-Za-z0-9_]*)`"
    r"|\bSet\s+`\$([A-Za-z_][A-Za-z0-9_]*)`\s+to\b"
)

USES_HEADER = re.compile(r"^#\s*Uses:\s*(.*)$")

# `-ErrorAction`/`-EA` is a cmdlet parameter; PowerShell passes it to aws.exe
# (or aws.exe itself) as an unrecognized argument. The abbreviation set is
# `-EA` plus any case-insensitive prefix of `-ErrorAction` whose *flag text*
# (including the leading dash) is at least 3 characters, e.g. `-Er`,
# `-ErrorAct`, `-ErrorAction`.
AWS_CMD = re.compile(r"(?:^|[\s`(])aws(?:\.exe)?\s", re.I)
_ERROR_ACTION_PREFIXES = [
    re.escape("ErrorAction"[:n]) for n in range(2, len("ErrorAction") + 1)
]
ERROR_ACTION = re.compile(
    r"-(?:EA|" + "|".join(_ERROR_ACTION_PREFIXES) + r")\b", re.I
)

IF_OPEN = re.compile(r"^\s*if\s*\(", re.I)
ELSE_OPEN = re.compile(r"^else\s*\{", re.I)
# A guard term is a bare variable (a presence test), optionally compared with
# `-eq`/`-ne` to a quoted string, `$true` or `$false`. `-eq $null` is rejected
# explicitly: it guards the delete on the value being ABSENT, i.e. an
# inverted guard. Anything else (`-not`, `!`, `-or`, a bare `$true`) fails to
# match and invalidates the whole guard.
GUARD_TERM = re.compile(
    r"^\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?"
    r"(?:\s+-(?P<op>eq|ne)\s+(?P<val>'[^']*'|\"[^\"]*\"|\$null|\$true|\$false))?$",
    re.I,
)
GUARD_AND_SPLIT = re.compile(r"\s+-and\s+", re.I)

# Hard-to-parse constructs that a teardown line must never contain (PY-R4
# round-4 amendment 2, item F11-5): rather than teach the scanner to parse
# these correctly, ban them outright. None of the 42 real labs use any of
# them today.
HERE_STRING_OPEN = re.compile(r"@['\"]")
BACKTICK_CONT_TAIL = re.compile(r"`\s*$")
SET_CLEAR_REMOVE_VAR = re.compile(r"\b(?:Set|Clear|Remove)-Variable\b", re.I)
AMP_AWS_INVOKE = re.compile(r"&\s*[\"']?[^\"'\n]*?\baws(?:\.exe)?\b", re.I)
FULLPATH_AWS_EXE = re.compile(r"[\\/]aws\.exe\b", re.I)

# Backtick-delimited inline code spans in step-bullet prose, e.g. the
# `$VpcId = aws ec2 create-vpc ...` inside "Run `$VpcId = ...`.". Only text
# inside these spans is ever treated as command text for a bullet; prose
# apostrophes ("Don't", "VPC's") are never string delimiters.
BACKTICK_CODE = re.compile(r"`([^`]*)`")

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


def _mask_strings(text: str) -> str:
    """Blank the *contents* of every quoted string (keep the length, so
    reported offsets/snippets are unaffected) so a `;`/`|`/`aws`/`-EA` that
    only appears inside a string literal is never mistaken for real command
    text. Used for command text: teardown lines directly, and the inside of
    backtick code spans in step bullets (PY-R4-006/008, rule 6)."""
    return STRING_LITERAL.sub(lambda m: " " * len(m.group(0)), text)


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


def _strip_comment(text: str) -> str:
    """Drop a trailing `# ...` comment that sits outside any quoted string.
    A `#` inside a string (e.g. a shebang written into a heredoc-free
    `WriteAllText` call) is left alone. Applied before any assignment/use/
    guard/-ErrorAction/banned-construct analysis of a teardown line
    (PY-R4-004, rule 4): a fake assignment or a stray `-ErrorAction` typed
    into a trailing comment must never change what the scanner sees."""
    spans = _string_spans(text)
    for match in re.finditer("#", text):
        if not _inside_a_string(match.start(), spans):
            return text[: match.start()]
    return text


def _references_var(name: str, text: str) -> bool:
    return re.search(r"\$\{?" + re.escape(name) + r"\}?\b", text, re.I) is not None


def _is_reset_rhs(name: str, rhs: str) -> bool:
    rhs_clean = rhs.rstrip(";").strip()
    if rhs_clean.lower() == "$null":
        return True
    if rhs_clean in ("''", '""'):
        return True
    if rhs_clean.lower() == f"${name.lower()}":
        return True
    return False


def _is_noop_rhs(name: str, rhs: str) -> bool:
    """True if `rhs` does not introduce a real value for `name`: a reset
    (see `_is_reset_rhs`), empty, or an expression that merely re-derives
    `name` from itself (`"$X"` interpolation, `$X.Trim()`, `[string]$X`).
    PY-R4-003: only a real value source (an aws/terraform/cmdlet call, or
    any string/expression that does not mention `name`) counts as
    "setting" it."""
    rhs_clean = rhs.rstrip(";").strip()
    if not rhs_clean:
        return True
    if _is_reset_rhs(name, rhs):
        return True
    return _references_var(name, rhs_clean)


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
    """Parse a whole delete line as `if (COND) { BODY }`, optionally
    followed by a plain `else { ... }`, with only whitespace and an
    optional trailing `;` after that. Returns (cond, body) or None if the
    line is not exactly that shape. Uses bracket depth, not a greedy regex,
    so nested `if`/`foreach`/`do...while` blocks in BODY (or in the else
    branch) do not break the parse. The else branch's own content is never
    inspected — it only runs when the guard is false."""
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
    tail = rest[brace_end + 1 :].lstrip()
    if tail:
        else_match = ELSE_OPEN.match(tail)
        if else_match:
            else_open = else_match.end() - 1
            else_close = _match_balanced(tail, "{", "}", else_open)
            if else_close is None:
                return None
            tail = tail[else_close + 1 :].strip()
    if tail not in ("", ";"):
        return None
    return cond, body


def _banned_construct(line: str) -> str | None:
    """Name of the banned construct present in `line`, or None. These are
    hard to parse correctly (a here-string body, a continued statement, a
    variable-scope bypass, or an aws invocation disguised behind `&` or a
    full path), so instead of parsing them we simply forbid them in
    teardown lines (PY-R4-006/PY-R4-005-adjacent, rule 5). The here-string
    opener itself is checked on the raw line (it IS a string delimiter, so
    masking would hide it); everything else is checked on the masked line
    so a legitimate `${Var}` or `&`/`aws` mention *inside* a quoted string
    (e.g. `Write-Host "Skipping ${Bucket}: ..."`) is not banned."""
    if HERE_STRING_OPEN.search(line):
        return "here-string (@' or @\")"
    if BACKTICK_CONT_TAIL.search(line):
        return "backtick line continuation"
    # A quoted `& "...\aws.exe"` or `& 'aws'` IS the bypass this rule
    # targets, so these two run on the raw line, not the masked one.
    if AMP_AWS_INVOKE.search(line):
        return "& invoking aws"
    if FULLPATH_AWS_EXE.search(line):
        return "full-path aws.exe"
    masked = _mask_strings(line)
    if SET_CLEAR_REMOVE_VAR.search(masked):
        return "Set-Variable/Clear-Variable/Remove-Variable"
    if "${" in masked:
        return "${ construct"
    return None


def _assignments_in_spanned(text: str, spans: list[tuple[int, int]]) -> list[tuple[str, bool, bool]]:
    """Return [(name, is_reset, is_noop), ...] for each `$Name =` target in
    `text` that sits outside `spans` (quoted-string spans), so text that
    only resembles an assignment inside a string, e.g.
    `Write-Host "$X = gone"`, is ignored. The right-hand side is read from
    the original text, unmodified."""
    results = []
    for match in ASSIGN.finditer(text):
        if _inside_a_string(match.start(), spans):
            continue
        name, rhs = match.group(1), match.group(2)
        results.append((name, _is_reset_rhs(name, rhs), _is_noop_rhs(name, rhs)))
    return results


def _assignments_in(text: str) -> list[tuple[str, bool, bool]]:
    """`_assignments_in_spanned` using this text's own quote-based string
    spans. For teardown lines: this text already IS command text."""
    return _assignments_in_spanned(text, _string_spans(text))


def _foreach_assigned_in(text: str) -> set[str]:
    """Names bound by a `foreach ($Name in COLLECTION) { ... }` header in
    `text`, but only when COLLECTION is a real source: non-empty, not the
    literal `@()`, and not merely referencing `Name` itself. PY-R4-003:
    `foreach ($VpcId in @()) { }` must not "set" `$VpcId`."""
    names: set[str] = set()
    spans = _string_spans(text)
    for match in FOREACH_HEADER.finditer(text):
        if _inside_a_string(match.start(), spans):
            continue
        open_idx = match.end() - 1
        close_idx = _match_balanced(text, "(", ")", open_idx)
        if close_idx is None:
            continue
        header = text[open_idx + 1 : close_idx].strip()
        bind = FOREACH_BIND.match(header)
        if not bind:
            continue
        name, collection = bind.group(1), bind.group(2).strip()
        if not collection or collection == "@()":
            continue
        if _references_var(name, collection):
            continue
        names.add(name)
    return names


def _code_spans_in(bullet: str) -> list[str]:
    return BACKTICK_CODE.findall(bullet)


def _assigned_in(text: str) -> set[str]:
    """Teardown-line 'set' vars: real (non-noop, non-reset) assignments,
    plus foreach bindings over a genuine collection."""
    names = {name for name, _is_reset, is_noop in _assignments_in(text) if not is_noop}
    names |= _foreach_assigned_in(text)
    return names


def _assigned_in_bullet(bullet: str) -> set[str]:
    """Step-bullet 'set' vars. Only text inside backtick code spans is ever
    parsed as command text (rule 6): prose apostrophes outside backticks,
    e.g. "Don't skip: `$VpcId = ...`.", are never string delimiters, so they
    can no longer swallow the real assignment that follows them."""
    names: set[str] = set()
    for code in _code_spans_in(bullet):
        names |= {
            name
            for name, _is_reset, is_noop in _assignments_in_spanned(code, _string_spans(code))
            if not is_noop
        }
        names |= _foreach_assigned_in(code)
    return names


def _prose_assigned_in(bullet: str) -> set[str]:
    names: set[str] = set()
    for match in PROSE_ASSIGN.finditer(bullet):
        names.add(match.group(1) or match.group(2))
    return names


def _check_error_action(lab_id: str, text: str, errors: list[str]) -> None:
    masked = _mask_strings(text)
    if AWS_CMD.search(masked) and ERROR_ACTION.search(masked):
        errors.append(
            f"{lab_id}: -ErrorAction on an aws command: {text.strip()[:80]}"
        )


def _guard_covers(line: str, learner_vars: set[str]) -> bool:
    """True if every var in learner_vars has a presence term (a bare `$X`,
    or `$X -ne $null`) among the -and-joined terms of a single valid guard
    (`if ($A -and $B -ne 'x') { ... }`) that wraps the whole line. A value
    comparison alone (`$X -ne 'x'`, `$X -eq ''`) is never a presence test on
    its own — PY-R4-001 — though it may appear as an extra `-and` term once
    the same var already has a presence term."""
    parsed = _parse_guard(line)
    if parsed is None:
        return False
    cond, _body = parsed
    cond = cond.strip()
    if not cond:
        return False
    terms = GUARD_AND_SPLIT.split(cond)
    presence_vars: set[str] = set()
    for term in terms:
        term_match = GUARD_TERM.match(term.strip())
        if not term_match:
            return False
        name = term_match.group(1).lower()
        op = term_match.group("op")
        val = term_match.group("val") or ""
        if op is None:
            presence_vars.add(name)
            continue
        op = op.lower()
        if val.lower() == "$null":
            if op == "eq":
                # `-eq $null` guards on the value being ABSENT: inverted.
                return False
            presence_vars.add(name)  # `-ne $null` is a presence test.
        # Any other value comparison (`-eq`/`-ne` a string/$true/$false) is
        # an extra qualifier, not a presence test on its own.
    return _lower(learner_vars) <= presence_vars


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
        stripped_line = _strip_comment(line)
        _check_error_action(lab_id, stripped_line, errors)
        construct = _banned_construct(stripped_line)
        if construct:
            errors.append(f"{lab_id}: teardown uses a banned construct ({construct}): {line[:80]}")

    non_comment_deletes = [
        line for line in deletes if line.strip() and not line.lstrip().startswith("#")
    ]
    if not non_comment_deletes:
        errors.append(f"{lab_id}: teardown has no delete commands (empty or comments only)")

    seen: set[str] = set()
    for line in deletes:
        stripped_line = _strip_comment(line)
        if any(is_reset for _name, is_reset, _is_noop in _assignments_in(stripped_line)):
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
        assigned |= _assigned_in_bullet(bullet)
        assigned |= _prose_assigned_in(bullet)
    for line in deletes:
        if line.lstrip().startswith("#"):
            continue
        stripped_line = _strip_comment(line)
        made_here = _assigned_in(stripped_line)
        used = {
            v
            for v in VAR_REF.findall(stripped_line)
            if v.lower() not in AUTOMATIC and v.lower() not in _lower(made_here)
        }
        missing = sorted(
            v for v in used if v.lower() not in _lower(assigned) and v.lower() not in _lower(declared)
        )
        for var in missing:
            errors.append(f"{lab_id}: teardown uses ${var} but nothing sets or declares it")
        if unguided:
            learner_vars = {v for v in used if v.lower() in _lower(declared) - _lower(assigned)}
            if learner_vars and not _guard_covers(stripped_line, learner_vars):
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
