# Concept: an exam-practice loop with Claude as the tutor

This repo started as "export my Gradeo answers" and became a general pattern for preparing for a written exam with an AI tutor that **only works from real past questions, marks like the real markers, and sees how you work, not just what you wrote**.

The subject (NSW HSC Software Engineering) is incidental. The pattern is:

```
 sources ─► question bank ─► drills / papers ─► exam app (you answer)
                 ▲                                   │  answers, timing, keystrokes,
                 │                                   │  notes, "ask Claude", chat
                 │                                   ▼
          reservations  ◄── Claude (in Claude Code) ◄── request queue
          + weak areas       marks, explains, builds    (file + HTTP)
                             the next drill
                                   │
                                   └──► live result back to the page (SSE)
```

---

## 1. The paper bank (the ground truth)

**Idea:** practise only on real exam questions, with the official marking criteria attached, so every mark means something.

- **Pull everything into one normalised format.** Each question has: prompt, stimulus (markdown + local images), answer type (MC, matching, short, code, SQL, drawing), marks, and **the key**: marking criteria, sample answer and correct options. Sources here: a school LMS (Gradeo, via its API using the student's own login), official exam-board papers, teacher sites, community-shared trial papers.
- **Deduplicate, then tag** each question with a syllabus point, so coverage and weak areas can be counted.
- **Reserve whole papers** for full timed practice. A reserved paper's questions can never appear in a drill, so the "unseen exam" stays unseen.
- **Record key problems** (wrong or debatable keys, transcription errors) on the question itself, not in someone's head.
- **Generated questions are the exception.** They're used only for gaps, or to drill one specific skill (e.g. "read every requirement" SQL traps), are labelled as generated, and must be harder than the real exam.

Lesson learned: **the import is where quality is won or lost.** Transcribed papers had answers sorted into a giveaway diagonal, code tables flattened into one line, and line breaks dropped from grids. Every one of those was found by the student while practising, and then fixed in the importer, not just in that one question.

## 2. The exam app (the practice surface)

**Idea:** practise in a copy of the real exam interface, so nothing is new on the day.

- A local web app that looks and behaves like the real online exam: navigation, flagging, highlighter, reading time, rest breaks, the official drawing tool with its shape library, code and SQL editors that can run.
- **Two modes:**
  - **Full paper:** realistic timing (reading + writing), no feedback until the end.
  - **Drill:** usually **one question at a time**. You plan your time from the marks before the question appears; the clock counts down **your plan**; it stops while you read feedback.
- **It records how you work, not just the answer:** time on each question, time before you started typing, visits, a keystroke log (pauses, words you correct most, slowest words), breaks and pauses. For a student with dyslexia this separated "doesn't know it" from "knows it, loses time writing it", which changed the whole revision plan.
- Answers can be **checked against the key**, **edited after feedback** (the earlier attempt and its feedback are kept), and the student can **report a problem** or attach **notes for the tutor** ("guessed", "key looks wrong") to any question.

## 3. The Claude link (the tutor)

**Idea:** the tutor is Claude running in Claude Code on the same machine, with the bank, the app's data and the marking skill all in reach. The app and Claude talk through a tiny queue.

**How it works now (no MCP yet):**

1. **Ask Claude to mark:** the page posts the answer to the local server. The server writes a request file (answer + drawing PNG + the key) and appends one line to `mark_requests.jsonl`. The timer pauses.
2. **Claude wakes up:** a background watcher in the Claude Code session sees the new line, and Claude reads the request.
3. **Claude marks** with a marking skill calibrated against real teacher marks (blind-marked within ±1 on 48 answers), then posts `{mark, feedback}` back (`study/post_mark.py`).
4. **The server pushes the result** to the open page with Server-Sent Events. The mark appears in place and the clock resumes.
5. **Dialog:** under any feedback there is a chat box. Messages go through the same queue, so the student can argue a mark ("code that doesn't run can still get full marks") and Claude answers with evidence: the criteria, a counterexample, or the student's own past teacher marks.

Claude also works **between** questions: it keeps the revision notes and progress log, finds the weak pattern across attempts (here: loop boundaries and missed requirements), and builds the next drill from the bank to target exactly that, using spaced repetition the next day.

**The obvious next step is an MCP server,** so the link is a proper tool interface instead of watched files:

| MCP tool | Does |
|---|---|
| `next_request()` | Blocks until the student asks for a mark or sends a message, then returns it (replaces the file watcher) |
| `get_attempt(id)` | Answers, timing, keystroke stats, notes |
| `post_mark(id, mark, feedback)` / `reply(id, text)` | Sends the result or message to the page |
| `search_bank(query, syllabus, type, marks)` | Finds real, unreserved questions |
| `create_drill(question_ids, options)` | Puts a drill in the app (validated: no broken options, no reserved papers) |
| `reserve_paper(name)` / `progress()` | Keeps exam papers unseen; returns the weak-area summary |

With that, the same loop works from any MCP client, and Claude needs no shell access to the student's machine.

## 4. What made it work

- **Real questions + real keys + calibrated marking.** The feedback is trusted because it matches how the real markers mark.
- **One question at a time, marked immediately, then a targeted redo.** Scores on one skill went 69% → 75% → 79% across three drills in one afternoon.
- **The student can push back.** The chat, the "key looks wrong" note and the problem report turned bugs and bad keys into fixes within minutes.
- **Measure process, not just answers.** Time planned vs used, typing pauses and edit counts showed where marks were really lost.
- **Protect the unseen papers.** Reservations stop "practice" from quietly spoiling the mock exams.

## 5. To reuse this for another subject

1. Write an importer for your sources into the bank format (keep the key with each question).
2. Tag questions to your syllabus; reserve 2–3 full papers.
3. Point the exam app at the bank (it only needs `exam.json` + `assets/`).
4. Calibrate a marking skill: give Claude 20–50 teacher-marked answers, mark blind, compare, and adjust.
5. Run the loop: drill → mark → chat → targeted redo → full paper → repeat.
