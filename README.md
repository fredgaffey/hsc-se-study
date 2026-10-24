# HSC Software Engineering — study kit

Everything I used to prepare for the 2026 HSC Software Engineering exam, shared with my class.
It's all here: past papers, every Gradeo paper with marking criteria and sample answers, my own
answers and feedback, an offline exam app that works like NESA's, a SQL trainer, a pseudocode
checker, and a marking skill for Claude that's been tested against our teacher's real marks.

This will come down after the HSC.

## Quick start

Needs Node 20+ and Python 3.

```sh
npm install
node exam-app/server.mjs          # exam app      → http://localhost:7788
cd sql-app && ./start.sh          # SQL trainer   → http://127.0.0.1:5050
cd canvas && python3 -m http.server 8765   # course site + quiz generator → http://localhost:8765
```

## What's where

| Folder | What it is |
|---|---|
| `exam-app/` | Offline exam app styled like NESA's online HSC exam. Sit any Gradeo paper or a PDF paper with a timer, reading time, rest breaks (pauses the timer), flagging, spell-check off. Answers autosave to `papers/attempts/`. |
| `gradeo_out/exams/` | Every Gradeo paper: questions, images, videos, marking criteria, rubrics, sample answers. `exam.md` is the readable version, `exam.json` the data. Start at `gradeo_out/INDEX.md`. Includes my answers, marks and Sir's feedback. |
| `papers/` | NESA Sample HSC Exam (PDF/DOCX). `papers/marking/` has the official marking guidelines for it and for the 2025 HSC, plus the 2025 full-mark sample answers. |
| `practice/QUEUE.md` | 115 written questions from every paper, ordered for practice (extended responses and legal/ethical first). Answers are in `practice/key.json` — don't peek. |
| `worksheets/` | SQL, schema, data dictionary, DFD, decision tree, UI/UX and network diagram questions with answers, plus course notes. |
| `canvas/` | The Year 11 and 12 Canvas course: 195 lessons, 680 quiz questions with answers, quiz generator. Open `canvas/index.html` via the server above. |
| `sql-app/` | SQL trainer on the course specification's Games/Publishers/Developers database, 13 tasks, accepts NESA words (`GREATER THAN` etc.). |
| `skills/hsc-pseudocode/` | Claude skill + linter for NESA pseudocode syntax (`python3 skills/hsc-pseudocode/scripts/hsc_pseudocode_linter.py file.txt`). |
| `skills/hsc-marking/` | Claude skill for marking answers like our teacher. See `calibration.md` for how well it matches his marks. |
| `course-docs/` | NESA syllabus and course specifications (pseudocode, flowcharts, DFDs, structure charts, class diagrams and more). |
| `REVISION.md` | My revision plan, weak areas and progress log. |

## Using the Claude skills

Copy a skill folder into `~/.claude/skills/` (Claude Code), or upload the folder to a Claude.ai project.
Then ask e.g. *"mark my attempt papers/attempts/<file>.md using the hsc-marking skill"*.

How well the marking matches our teacher (blind test on 48 of his marked answers): every short answer
within 1 mark with a marking guideline, 47/48 without one. Paper totals land within a few marks.

## Exporting your own Gradeo papers

Each of us can pull our own Gradeo results (your answers, marks and feedback):

1. In Chrome, open `chrome://inspect/#remote-debugging` and turn on remote debugging.
2. Log in to platform.gradeo.com.au in that Chrome.
3. `node fetch.mjs` (click **Allow** in Chrome once), then `node build.mjs`.

Output goes to `gradeo_out/`. Papers you've submitted but whose results haven't been released return
"locked" until the teacher releases them.

## Tips that actually moved marks

- About **35 words per mark** and **2 minutes per mark**. Never leave a question blank.
- "Explain" = point → *this is because* → *for example* → *as a result*, linked to the scenario.
- Full sentences, not dot points, even for "identify".
- On "select all that apply", only add a second option if you're sure.
