"""Self-test for q1_batch_check.LETTER, the letter-reference detector.

Usage: python scripts/test_q1_letter.py      Prints PASS/FAIL; exits 1 on any FAIL.

The bad strings are the openings of the 10 tf-g4 rationales that shipped past
the old pattern at commit db11570. The good strings are English that a
letter pattern can mistake for a choice reference.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from q1_batch_check import LETTER  # noqa: E402

BAD = [
    "c misstates data blocks as managing a stateful placeholder object",
    "c is wrong because layering a redundant depends_on onto a pair",
    "d is wrong because depends_on takes a literal list",
    "e is wrong; there is no automatic mirroring between a local and an output",
    "b reverses the direction entirely.",
    "c overreaches: nothing about A's own depends_on argument",
    "b names a real version floor, but it's the one for check blocks",
    "c is wrong and directly contradicts a; prevent_destroy has a documented gap",
    "The rationale says choice c is fine.",
    "Option (b) is the default.",
    "It is wrong (d) here.",
    "Wrong. C is the trap.",
]
GOOD = [
    "AWS Config findings describe how the startup's own resources are configured, "
    "so they answer a different question.",
    "A data block is the opposite kind of read.",
    "a data block only performs read operations",
    "Referencing `aws_s3_bucket.b` is how the policy finds the bucket.",
    "Plan A and plan B are both valid.",
    "lets account B invoke the function",
    "SSE-C still works on existing buckets",
    "the single target in AZ-C is not seeing a disproportionate share",
    "Terraform re-reads a data source on every ordinary run.",
    "e.g. a hash of the value",
]

fails = 0
for s in BAD:
    if not LETTER.search(s):
        fails += 1
        print(f"FAIL: missed letter reference: {s!r}")
for s in GOOD:
    m = LETTER.search(s)
    if m:
        fails += 1
        print(f"FAIL: false positive {m.group(0)!r} in: {s!r}")
print(f"{'PASS' if not fails else 'FAIL'}: {len(BAD)} bad, {len(GOOD)} good, {fails} failures")
sys.exit(1 if fails else 0)
