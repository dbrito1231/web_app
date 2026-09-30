# Student run — reopen check (15 questions)

This was a Sonnet agent working from a text packet. The packet had the three lessons, the 11 changed questions, and 4 unchanged near-tie controls (4-3 k07, s03, s04; 1-3 k03), shuffled together. The content was at commit 22f9ca8. All answers were committed before the key was opened.

This summary was saved by the Lead Dev. The Student's full reply is condensed, and its question numbers are mapped to ids below.

Q-number → id: Q1 4-3-k05, Q2 4-3-k03, Q3 1-3-k04, Q4 1-3-s05, Q5 1-3-k03 (control), Q6 4-3-s04 (control), Q7 4-3-k07 (control), Q8 4-3-s02, Q9 4-1-k03, Q10 4-1-s06, Q11 1-3-s01, Q12 4-3-k09, Q13 4-3-s03 (control), Q14 4-1-k05, Q15 4-1-s07.

## Score
**15/15.** The Student was least certain of Q7, Q10 and Q13, and the lessons resolved all three.

## Fairness
No question is unfair and no rationale contradicts a lesson. Two notes:

- **Untaught names that aren't needed to answer:** MariaDB (Q8 d) and Athena-as-warehouse (Q6 b).
- **Rationales slightly beyond the lesson:** Q7 (DMS and stored procedures) and Q5 (the bucket-policy bypass). Both are sound inferences.

About half of the questions have at least one plainly weak distractor. This pattern predates the reopen; the Student calls them "easy, not unfair".

## Stem wording
- **1 keyword-guessable (defect):** Q6 = **4-3 s04, a control, unchanged**. The stem says "column subsets"; only the key says "columnar storage". It is pre-existing in a closed task, written before the paraphrase rule, so it is recorded and not fixed.
- **13 structural scenario references.** The closest to a defect are Q3 (HSM), Q4 and Q14 (backup), and Q7 (schema/query).

## Length and form tells
- **Shortest key:** 3 of 15 (Q6, Q7, Q13, all controls; Q7 and Q13 are near-ties). Chance is about 3.75, so this is **not a tell any more**.
- **Longest key:** 0 of 15. "Never pick the longest" was right 15 of 15 times, against about 75% by chance.
- **"Avoid the extremes":** found the key in 12 of 15 (80%), against 50% by chance.
- **Form tells:**
  - **Q14 = 4-1 k05 (changed):** the key "AWS Backup with a backup plan" is the only option with a "with…" qualifier. This is mild.
  - **Q1 = 4-3 k05 (changed):** the key is the only option that defines its mode. This is minor.
  - **Q2, Q7, Q8, Q13:** a distractor carries a built-in flaw clause.

Student verdict: fair, with minor concerns: the Q6 keyword match and the flaw-clause pattern in distractors.
