# Inline plan: CR-0018 — lesson 2.2 downtime figures under-rounded

Status: **Teacher-validated (approve). Awaiting the user's approval.** No edit is made before approval.
Author: Lead Dev, 2026-09-30. CR: `docs/change-requests.md` CR-0018.

## Goal
Make the downtime figures that the lesson teaches, and one question uses, match the arithmetic:
- 99.9% of a 365-day year leaves 0.001 × 8,760 h = **8.76 h**, which rounds to about **8.8 hours**. The lesson says "roughly 8.7 hours".
- 99.99% leaves 0.0001 × 525,600 min = **52.56 min**, which rounds to about **53 minutes**. The lesson says "roughly 52 minutes".

## Where the figures appear (checked with a search of `content/`; nothing else matches)
1. **`content/lessons/lesson-2-2.json`, the availability sentence.** It says 99.9% allows "roughly 8.7 hours" of downtime a year and 99.99% "roughly 52 minutes".
2. **`content/questions/q-saa-2-2-s03-mc.json`:**
   - the stem: "about 52 minutes of downtime per year";
   - choices c and d: "An RTO of 52 minutes." and "An RPO of 52 minutes.";
   - the rationale: "about 52 minutes", "roughly 8.7 hours" and "the stated 52-minute limit".

## Change
- **Lesson:** "roughly 8.7 hours" becomes "about 8.8 hours", and "roughly 52 minutes" becomes "about 53 minutes". No other wording changes.
- **Question:** every "52" becomes "53" and "8.7" becomes "8.8". The key (b, 99.99%), choice order and ids are unchanged. Choices c and d stay parallel ("An RTO of 53 minutes." / "An RPO of 53 minutes."), so option lengths barely move.
- The question sits in closed task 2.2. This is a factual correction through a CR, not a reopen for rules introduced later.

## Risks
- **A key change:** none. 53 minutes still corresponds to 99.99%. `key_text_diff` is not a useful proof here, because the distractor text changes; instead, compare `correctAnswerIds` and choice ids field by field against HEAD.
- **Length or echo checks:** run `q1_batch_check 2-2` and `stem_echo_check 2-2` before and after. Expect no change beyond the digits.
- **Other lessons quoting these figures:** there are none (checked).

## Tests
`content_lint` PASS; `q1_batch_check 2-2` unchanged apart from digits; the field comparison shows the key and ids unchanged; the Teacher re-validates after the edit.

## Learning content affected?
Yes: one lesson sentence and one question, digits only.

## Teacher validation
Fresh Sonnet Teacher, 2026-09-30: **Plan: approve.**
- **Arithmetic:** confirmed. The lesson's figures were truncated, not rounded.
- **Completeness:** a case-insensitive search finds only the two files listed.
- **Wording:** "about" is harmless and matches the question stem.
- **Question:** changing choices c and d to 53 is neutral. Stem, choices and rationale must stay consistent.
- **Closed task:** a factual correction is a good reason to touch it.
- **Not taken:** the Teacher suggested updating the question's `reviewedOn` date. It stays `2026-09-26`, per the user's decision to sweep the date once at the end.
