# Student run — tf-g4 (24 questions)

Sonnet agent; text packet only (`make_student_packet.py tf-g4 24`, content at 157e12a). All answers committed before the key was opened. Saved verbatim by the Lead Dev.

Caveat: this Student is Sonnet, which is stronger than the model that closed tasks 3.1–4.2, so a high score is weaker evidence than it was there. The stem-wording counts do not depend on the model.

## Answers (committed before the key)

1. a — data reads without creating/changing.
2. b — data block deferred to apply when its args depend on a resource this plan changes.
3. a, c — terraform_data is a resource-lifecycle value store with no infra; data sources re-read every ordinary run.
4. c — `data.<TYPE>.<LABEL>.<ATTRIBUTE>` syntax required.
5. d — argument reads profile's attribute → profile created first.
6. b, d — depends_on only for behavior-only deps; existing attribute reference already implies order.
7. a — output is what a parent reads after the child runs.
8. b — no default/no supplied value → Terraform prompts before plan.
9. a, e — locals are module-scoped, referenced with `local.<NAME>`.
10. c — sets are unordered; must `tolist()` before indexing.
11. d — null = omitted, falls back to default/error.
12. c, e — map keys always strings; auto string conversion exists but not for `==`.
13. a — genuinely distinct per-instance args → `for_each`.
14. b — `can` gives boolean pass/fail for a validation condition.
15. b, c — `for` supports optional `if`; `merge` lets the later map win on key collision.
16. c — depends_on in A naming B: A depends on B, nothing implied about A's dependents.
17. d — avoiding a zero-healthy-target gap = `create_before_destroy`.
18. a, d — prevent_destroy has a config-removal gap; lifecycle only takes literals.
19. a — postcondition with `self.public_dns`, checked after creation, needs 1.2+.
20. b — check blocks only warn, need 1.5+.
21. c, d — variable validations run before plan; validation only sees its own variable.
22. c — sensitive redacts CLI/UI only, still plaintext in state.
23. d — write-only arguments need 1.11+; 1.9 doesn't qualify.
24. b, e — nonsensitive() exposes value in output; Vault issues short-lived credentials.

## Score

**24/24 correct.** No misses.

## Fairness

No misses to adjudicate. No question felt like a pure guess — each stem's discriminator was directly traceable to a sentence in the lesson (e.g., Q2's apply-phase deferral, Q10's `tolist()` requirement, Q19's precondition-vs-postcondition timing, Q23's 1.11 floor for write-only args). No rationale in the key contradicted the lesson text. No distractor was eliminable purely by absurdity/self-contradiction without domain knowledge — the wrong choices (e.g., Q18's "prevent_destroy blocks under every circumstance," Q23's "sensitive unlocks write-only support") are plausible-sounding misconceptions that require the lesson's specific facts to rule out, not surface tells.

## Stem wording

Every case where a term appeared in both the stem and the key also appeared in at least one distractor, or simply named an object/resource the stem itself introduced (e.g., "AMI" in Q1, "instance profile" in Q5, "state file" in Q22, "write-only" in Q23, "target group" in Q17).

**0 stems keyword-guessable (defect).**
**10 stems with a structural scenario reference (not a defect):** Q1, Q2, Q3, Q4, Q5, Q10, Q17, Q19, Q22, Q23.

## Length tell

16 single-answer questions. The key was the longest option in Q5, the shortest in Q10, and tied-shortest in Q14. In the other 13 the key was neither the longest nor the shortest.

**"Never pick the longest or shortest" would have found the key in 13 of 16 single-answer questions.** It narrows each of those to two options; it does not identify the key by itself.

Student verdict: fair
