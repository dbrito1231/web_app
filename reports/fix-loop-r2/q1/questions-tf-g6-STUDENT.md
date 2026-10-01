# Student run — tf-g6 (12 questions)

Sonnet agent; text packet (`make_student_packet.py tf-g6 12`, content at f924a10); all answers committed before the key was opened. Saved by the Lead Dev (condensed). The Student is Sonnet, stronger than the model that closed tasks 3.1–4.2, so the score is weaker evidence; the wording counts do not depend on the model.

- **Score: 12/12.** No misses and no guesses. The closest call was Q10, where "inspect before it is recorded" decides it.
- **Rationales:** none contradicts the lesson.
- **Distractors that can be eliminated without the material:** Q1 d, Q3 e, Q4 b, Q5 c, Q9 e, Q12 e and Q2 d (absolutes or implausible behaviour). These are acceptable distractors.
- **Form tells (defects):**
  - **Q9 = 6c-mr:** the three distractors carried "as …" / "because …" justification clauses, while the two keys were plain statements.
  - **Q8 = 6c-mc2 a:** the only option with a self-justifying clause.
  - **Q6 = 6b-mr d:** a distractor-only "because …" clause.
- **Stem wording:** 1 keyword-guessable (Q12 = 6d-mr, "keeps running" only in the stem and key c), 11 structural.
- **Length tell:** "avoid the extremes" keeps the key in 7 of 8 single-answer questions. It narrows to two options, so it is weak.

Student verdict: fair

## Lead Dev fixes (wording only; keys, ids and positions unchanged)
- **6c-mr:** a, b and e lose their "as …" / "because …" tails.
  - That removed the only distractor mention of "backend", so key c then echoed the stem. `stem_echo_check` caught it.
  - Key c now ends "to the new location" instead of "to the new backend".
- **6c-mc2 a:** now "Hardcode the credentials in the backend block for each environment". It is still wrong for the taught reason that hardcoded values land in `.terraform` and in plan files.
- **6b-mr d:** now "`terraform force-unlock` is safe for any engineer to run on a lock that another engineer's run still holds". The "because …" clause is gone.
- **6d-mr c:** now "... drops the database from state without destroying the real database". It no longer echoes "keeps running".

**Checks:** the whole chain re-run on tf-g6 passes (lint, batch check with longest-is-key 25%, audit, echo, claim-prose, letter test). The rationales still match by content. These changes go to the Teacher for a second-role confirmation before close.

## Teacher second-role check, and close
- **Teacher's check:** the form tells and the echo are gone. The changed distractors are still real and still wrong for taught reasons; 6c-mc2 a still fails "No secrets may reach the repository". The rationales match, and 6c-mr's "new location" is accurate. Verdict: **Task tf-g6: close.**
- **Remaining tails removed:** the Teacher noted three more "so …"/"because …" tails on distractors (6d-mr b, 6b-mr a and c). The Lead Dev removed them as well:
  - 6d-mr b: "Renaming the block alone keeps the instance in place under its new address". Still refuted by "a renamed block is read as destroy the old object and create a new one".
  - 6b-mr a and c: tails dropped.
- **Checks:** the whole chain re-run passes.
