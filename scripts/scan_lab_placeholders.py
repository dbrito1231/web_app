"""Read-only scan for CR-0005 lab placeholder patterns. Exit 1 on failure."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "content" / "labs"

errors: list[str] = []

BAD_TAG = re.compile(r"\{\{Key=")
LITERAL_DOTS = re.compile(r"`aws [^`]* \.\.\.")
ENI_VPC = re.compile(r"ENIs, then VPC", re.I)
VAR_REF = re.compile(r"\$([A-Za-z][A-Za-z0-9_]*)")


def steps_blob(steps: list) -> str:
    return json.dumps(steps)


def lab_has_vpc_create(text: str) -> bool:
    return "create-vpc" in text or "create_vpc" in text


def scan_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    lab_id = data.get("id", path.stem)
    blob = path.read_text(encoding="utf-8")

    if BAD_TAG.search(blob):
        errors.append(f"{lab_id}: contains {{{{Key= tag syntax")

    if LITERAL_DOTS.search(blob):
        errors.append(f"{lab_id}: contains literal `...` command placeholder")

    steps = data.get("steps") or []
    step_text = steps_blob(steps)
    if ENI_VPC.search(step_text):
        num = int(lab_id.split("-")[1]) if "-" in lab_id else 0
        guided = data.get("kind") == "guided"
        if guided and num >= 10 and not lab_has_vpc_create(blob):
            errors.append(f"{lab_id}: ENIs/VPC boilerplate in steps without create-vpc in file")
        elif guided and num < 10 and lab_id not in ("gl-05", "gl-06", "gl-07", "gl-08"):
            if ENI_VPC.search(step_text):
                errors.append(f"{lab_id}: generic ENIs/VPC text in non-VPC lab steps")

    td = data.get("teardown") or {}
    deletes = td.get("orderedDeletesPowerShell") or []
    delete_text = "\n".join(deletes)
    assigned = set(re.findall(r"\$([A-Za-z][A-Za-z0-9_]*)\s*=", blob))
    assigned |= set(re.findall(r"foreach\s*\(\$([A-Za-z][A-Za-z0-9_]*)", blob, re.I))
    seen_vars: set[str] = set()
    for var in VAR_REF.findall(delete_text):
        if var in seen_vars:
            continue
        seen_vars.add(var)
        if len(var) < 2 or var in assigned:
            continue
        if var in (
            "AccountId",
            "CreatedAt",
            "ExpiresAt",
            "Bucket",
            "Suffix",
            "ErrorAction",
            "Confirm",
            "true",
            "false",
            "null",
        ):
            continue
        if steps:
            errors.append(f"{lab_id}: teardown uses ${var} but the file never assigns it")

    if lab_id.startswith("ul-") and "# Replace" in delete_text:
        errors.append(f"{lab_id}: teardown still has placeholder comments")


def main() -> None:
    for path in sorted(LABS.glob("*.json")):
        if path.stem == "gl-01":
            continue
        scan_file(path)

    if errors:
        print("FAIL", len(errors))
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("PASS", len(list(LABS.glob("*.json"))) - 1, "labs scanned")


if __name__ == "__main__":
    main()
