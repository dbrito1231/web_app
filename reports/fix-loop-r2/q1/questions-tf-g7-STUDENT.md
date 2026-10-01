# Student run — tf-g7 (9 questions)

Sonnet agent; text packet (`make_student_packet.py tf-g7 9`, content at abd3a08); all answers saved to a file before the key was opened. Saved by the Lead Dev (condensed). The Student is Sonnet, stronger than the model that closed tasks 3.1–4.2, so the score is weaker evidence; the wording counts do not depend on the model. A first Student run was stopped by an API safeguard before answering anything; it was restarted with reworded instructions and nothing carried over.

- **Score: 9/9.** Q7 (7c-mc) was narrowed down rather than certain, decided by the stem's "structured records" plus the lesson's JSON-at-TRACE sentence.
- **Rationales:** none contradicts the lesson. The Student flagged "may change at any time" as a paraphrase stretch. The Lead Dev traced it to the 7c-mr rationale (not 7c-mc) and checked the debugging page with curl: "It may change at any time, without warning." It is doc-backed and goes one step beyond the lesson's quote; no fix.
- **Distractors that can be eliminated without the material:** Q1 a/b, Q2 b/d, Q3 a/e, Q4 a, Q5 c/d, Q6 b/d/e, Q9 a/b/d. These are acceptable distractors.
- **Form tells:** no justification clauses on wrong choices only, no equivalent pairs. Absolutes on wrong MR choices only ("always" 7a-mr e, "whenever" 7b-mr e) were already accepted in round 2b as the legitimate falsifiers. 7c-mc's three plain-text levels make JSON the odd one out; the stem's "structured" is the real driver.
- **Stem wording:** 2 keyword-guessable by the Student's count (Q2 = 7a-mc2, `for_each` via "single import block to adopt all three" and the `locals` map; Q7 = 7c-mc, "structured" → JSON), 7 structural. The Lead Dev and the Teacher both read Q2 and Q7 as structural: each stem states the requirement under test, not a leaked token, and `stem_echo_check` reports 0.
- **Length tell:** "pick the longest" hits about 3 of 9, roughly chance.

Student verdict: fair

## Teacher second-role check, and close

- **Q2 and Q7: structural, agreed.** Q2's stem gives the situation (a map, one block for all three); the choices test the mechanism, and each wrong choice is a plausible invented argument. Q7's "structured records" was accepted in round 2; the student must still know JSON is a format, not a level.
- **Form tells:** none needs a fix.
- **Rationale wording:** no fix (the 7c-mc rationale matches the lesson; the stretch is in 7c-mr and is doc-backed, as above).

**Teacher: close.** With the technical close in round 2b (`7f26131`) and the Teacher close in round 2b (`abd3a08`), tf-g7 is closed.
