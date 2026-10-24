---
name: hsc-marking
description: Mark NSW HSC Software Engineering written, code and SQL answers the way our teacher marks them, with or without an official marking guideline. Use when asked to mark a practice paper, a single answer, or an exam-app attempt (papers/attempts/*.md).
---

# HSC Software Engineering marking

Mark like an experienced NSW HSC marker who has been calibrated against our teacher's real marks
on Gradeo. The goal is to give the mark the teacher would give: not kinder, not harsher.

## Procedure (every answer)

1. **Read the question's directive verb** and what it is asking for, including any scenario or stimulus.
2. **Decide the band before the number.** If a marking guideline is given, find the band whose descriptor
   the answer meets *in full*. If no guideline is given, use the defaults below.
3. **Apply the teacher's adjustments** (next section), then give a whole mark (half marks only if the
   guideline uses them).
4. Write one sentence of reason and one sentence saying the single change that would earn the next mark.

## How our teacher differs from a generous marker

These were learned by comparing blind marks with the teacher's marks. Apply them.

- **An example is not an explanation.** If the answer gives examples or a story but never states the
  underlying concept or mechanism the question is about (e.g. sandboxing = isolation/containment;
  metadata = enables indexing/searching), cap it at the middle band. Examples support an explanation;
  they don't replace it.
- **Link to the question's context, or lose the top band.** "Explain … for web architectures that handle
  big data", "for this bookstore", "this dashboard": generic points that could apply to anything are
  not enough for full marks, even when correct.
- **A wrong central claim costs a mark.** If the answer contains a factual error about the thing being
  asked (e.g. "client-side validation is more secure than server-side"), take a mark off even if the rest
  is good. Small side errors (SSL vs TLS) cost nothing on their own, but count towards "unclear".
- **Partially developed = middle band.** Two points that are named but not developed ("brief or unclear,
  points need development") score about half. Full marks need each point developed with cause → effect.
- **Credit understanding over wording.** The student has dyslexia. Do not deduct for spelling, grammar
  or informal wording when the meaning is clear. Deduct only when meaning is genuinely unclear.
- **Code and pseudocode: credit the right structure.** If the algorithm's structure is right (correct loop,
  correct query form, correct class structure), give the middle band even with bugs or a missing piece.
  Each requirement missed costs a mark; small bugs (>= instead of >, wrong data type) cost one mark.
- **Logic-paradigm queries:** a query with the right shape but missing the variable gets partial credit, not 1.
- **Dot points lose a mark** on 3+ mark questions, even "identify" ones, because they don't link back to the question.
  Full sentences are expected.
- **Blank or headings-only extended responses get 0**, even with a promising first sentence.

## What NESA itself awards full marks for (2025 HSC official full-mark samples)

Use these as the reference point for "full marks", especially when there is no guideline.

- **Length is modest.** Full-mark 3-mark answers run about 40–95 words; 5-mark about 110–190; 6-mark
  about 280–300 (~25–30 words per mark). Don't hold back marks because an answer is short if every
  required part is there and developed.
- **Spelling and grammar are not penalised.** Full-mark samples contain many misspellings and run-on
  sentences. Never deduct for them.
- Full-mark answers address **every part the question names** (e.g. "ONE positive and ONE negative",
  "TWO ways", "with reference to the video"), each **tied to the scenario**, in plain paragraphs.
- Longer answers: the concept is explained (how it works), then applied to the scenario, then an impact
  or judgement. "Discuss" answers include at least one point from the other side.
- **Code and SQL: marked on producing the required result.** Minimal, unpolished code that meets every
  requirement gets full marks; small differences in approach (quote style, slightly broader filter) are fine.
- Class diagrams: inheritance shown, redundant attributes moved to a parent class, attributes typed.

## Default bands when there is no marking guideline

Roughly one developed, correct, relevant point per mark.

| Verb | Full marks needs |
|---|---|
| Identify / name | the right items, in sentences (still lose 1 for bare dot points on 3+ markers) |
| Outline | main features, briefly, each correct |
| Describe | characteristics and features, each stated clearly |
| Explain | cause → effect for each point: *why/how*, not just *what*, linked to the context |
| Compare / contrast / distinguish | both sides on the same features, with the difference made explicit |
| Discuss | points for and/or against, developed |
| Evaluate / assess / justify | criteria, evidence both ways, and a clear judgement |

Extended responses (6–10 marks), no guideline:

| Band | Descriptor |
|---|---|
| Top (9–10 / 7–8 of 8) | covers every part of the question, developed points with specific, well-integrated examples, judgement where asked, coherent structure |
| High (7–8 / 5–6) | most parts covered with relevant examples; a little less thorough or balanced |
| Middle (5–6 / 4) | some relevant points from at least two parts; examples general or underdeveloped |
| Low (3–4 / 2–3) | general statements, limited understanding, few or no examples |
| Minimal (1–2 / 1) | little relevant content |

## Output format

For a whole attempt: a table of question → mark / available → one-line reason, then the total, then the
three biggest fixes across the paper (patterns, not one-offs). For one answer: mark, reason, and the
next-mark fix.

## Calibration (24 Oct 2026)

Fresh Opus agents, blind, 48 teacher-marked answers: with a marking guideline every answer was within 1
mark of the teacher (+0.2/answer generous); without one, 47/48 within 1 (about neutral). Extended
responses are the least certain: treat as ±1–2 marks. These rules were derived from the first 25 of
those answers only; see `calibration.md` for the before/after on the other 24.
