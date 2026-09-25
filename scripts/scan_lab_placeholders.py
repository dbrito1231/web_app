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
VAR_REF = re.compile(r"\$([A-Za-z][A-Za-z0-9_]*)")
ASSIGN = re.compile(r"\$([A-Za-z][A-Za-z0-9_]*)\s*=(?!=)\s*(\S*)")
FOREACH = re.compile(r"foreach\s*\(\s*\$([A-Za-z][A-Za-z0-9_]*)", re.I)
# Step text such as "Set `$CreatedAt` ..." or "Copy that Arn into `$BoundaryArn`".
PROSE_ASSIGN = re.compile(r"(?:\bSet|\binto)\s+`\$([A-Za-z][A-Za-z0-9_]*)`")
USES_HEADER = re.compile(r"^#\s*Uses:\s*(.*)$")
SEGMENT_SPLIT = re.compile(r"[;{}|]")

# PowerShell automatic variables and scope prefixes; never lab resources.
AUTOMATIC = {"_", "true", "false", "null", "env", "pwd", "LASTEXITCODE", "PSItem"}


def lab_has_vpc_create(text: str) -> bool:
    return "create-vpc" in text or "create_vpc" in text


def _assigned_in(text: str) -> set[str]:
    names = {name for name, rhs in ASSIGN.findall(text) if rhs != "$null"}
    names |= set(FOREACH.findall(text))
    return names


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

    deletes = (data.get("teardown") or {}).get("orderedDeletesPowerShell") or []
    unguided = lab_id.startswith("ul-")

    # Commands anywhere in the lab: `-ErrorAction` is a cmdlet parameter, and
    # PowerShell passes it to aws.exe as an unknown argument.
    for text in [step_text, *deletes]:
        for segment in SEGMENT_SPLIT.split(text):
            if re.search(r"(?:^|[\s`(])aws\s", segment) and "-ErrorAction" in segment:
                errors.append(f"{lab_id}: -ErrorAction on an aws command: {segment.strip()[:80]}")

    seen: set[str] = set()
    for line in deletes:
        if re.search(r"=\s*\$null\b", line):
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

    assigned = _assigned_in(step_text) | set(PROSE_ASSIGN.findall(step_text))
    for line in deletes:
        if line.lstrip().startswith("#"):
            continue
        made_here = _assigned_in(line)
        used = set(VAR_REF.findall(line)) - AUTOMATIC - made_here
        missing = sorted(v for v in used if v not in assigned and v not in declared)
        for var in missing:
            errors.append(f"{lab_id}: teardown uses ${var} but nothing sets or declares it")
        if unguided:
            learner_vars = used & declared - assigned
            guard = re.match(r"\s*if\s*\((.*?)\)\s*\{", line)
            if learner_vars and not (
                guard and all(f"${v}" in guard.group(1) for v in learner_vars)
            ):
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
