# Marking calibration against the teacher's real Gradeo marks

48 of the student's teacher-marked written/code answers (one more was dropped: Gradeo stored it under the
wrong question). Fresh Opus agents marked them blind: they never saw the teacher's marks or feedback.

## Without the skill (all 48)

| Condition | Exact | Within 1 | Total vs teacher | Bias / answer |
|---|---|---|---|---|
| With marking guideline | 26/48 | 48/48 | 117 vs 107.5 | +0.20 |
| No guideline | 23/48 | 47/48 | 105 vs 107.5 | −0.05 |

## With the skill (held-out answers 26–49 only)

The rules in SKILL.md were written from answers 1–25 and the teacher's feedback on them, then tested on
answers 26–49, which were not used to write them.

| Condition | Exact | Within 1 | 2+ off | Total (teacher 55) | Bias | Mean error |
|---|---|---|---|---|---|---|
| Guideline, no skill | 11/24 | 24/24 | 0 | 58 | +0.12 | 0.54 |
| **Guideline + skill** | 12/24 | 24/24 | 0 | **55** | **0.00** | 0.50 |
| No guideline, no skill | 9/24 | 23/24 | 1 | 49 | −0.25 | 0.67 |
| **No guideline + skill** | 9/24 | **24/24** | **0** | 52 | −0.12 | 0.62 |

Small improvement on a small sample: it removes the overall lean and the one 2+ mark miss, but is
within the noise for exact matches. Single answers stay ±1 mark; paper totals are reliable.

Where the skill still disagrees with the teacher: the teacher is kinder on some logic-paradigm and
short code answers, and stricter on "Difficulties" / "Backend Engineering" style explain questions
where the answer is correct but not linked to the scenario.
