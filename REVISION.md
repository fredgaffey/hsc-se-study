# HSC Software Engineering — revision notes

Shared notes between me and Claude. **Claude: read this file at the start of any revision
conversation, and update the Progress log and Open questions at the end of it.**

- **Exam:** Tuesday 27 October 2026 (HSC Software Engineering — assumed; confirm format/time below)
- **Data source:** `gradeo_out/` (export of all Gradeo exams, built 24 Oct 2026). Start at `gradeo_out/INDEX.md`.
- **Refresh data:** `node fetch.mjs && node build.mjs` in `~/gradeo` (one Chrome "Allow" click)

---

## 0. The real problem: written expression, not knowledge

- I have **dyslexia**; writing long answers is hard.
- My content knowledge is very good: my teacher went through a test with me verbally and said
  nearly every spoken answer was full marks. Practical assignments: near full marks.
- So most of the lost marks in extended responses come from **getting the answer onto paper**, not from missing knowledge.
- Main goals: (1) a fast, low-effort way to turn spoken answers into structured written ones;
  (2) build up the **legal / social / ethical** content they like to examine.

### Method
1. **Type everything; no voice dictation.** Type an answer, paste it to Claude, and Claude shows which parts
   earn marks and how to arrange them. Then retype it better from memory. Repeat until it's automatic.
2. **Sentence starters (memorise):**
   - Point: "One [benefit / risk / reason] is ___."
   - Explain: "This is because ___."
   - Effect: "As a result, ___."
   - Example: "For example, in this scenario ___."
   - Judgement (evaluate): "Overall, ___ because ___."
   - One paragraph per point. 8 marks ≈ 3–4 paragraphs.
3. **Plan in keywords first:** 3–4 keywords in the margin (about 30 seconds), then expand one at a time.
4. **Plain writing:** short sentences, one idea each. If unsure of a spelling, use a simpler word.
   Headings/labelled paragraphs in extended responses are generally fine (check with teacher).
5. **Spelling drill:** ~20 must-use terms (see section 5).

### Exam conditions (Tue 27 Oct)
- **Typed on a computer.** Rest breaks approved. No scribe.
- Type a 3–4 keyword plan at the top of the answer box, then expand each keyword into a paragraph.
  Typing lets me add or reorder later.
- **Practise with spell-check OFF**, as the exam probably has none.
- Take a rest break **just before the extended responses**, so I start them fresh.
- All practice is typed, under exam-like conditions.

### Word and time targets (from Trial Exam 1 sample answers)
- Whole trial exam: **~1,690 sample-answer words**, nearly all in the written questions (1,645 words, 47 marks).
- **About 35 words per mark:** 3 marks ≈ 100 words · 4 marks ≈ 140 words · 10 marks ≈ 350+ words
  (the 669-word sample is probably longer than needed).
- **Time: about 2 minutes per mark** (150 min / 78 marks). 3 marks ≈ 6 min · 4 marks ≈ 8 min · 10 marks ≈ 20 min.
- In that trial my 3-mark answers were about the right length (avg 67 words, 12/21 marks). I lost most on
  **near-blank answers**: Q26 4 words (0/4), Q11 7 words (0/3), Q29 39 words (0/10) = 17 marks lost for under 50 words.
- **Biggest gain = finishing every question.** Never leave a blank.
- [x] **Typing speed (Monkeytype, 5 min, punctuation, 24 Oct): 33 wpm, 84% accuracy, 55% consistency.**
  Fast enough: 1,650 words ≈ 50 min of pure typing. The stop-start pattern means pauses on spelling.
  In the exam: **don't stop to fix typos**; only fix badly wrong key terms.
  Don't spend time on typing drills. Only drill key-term spelling (Monkeytype custom mode, ~5 min/day).
- [x] **Answer speed (24 Oct): 96 words in 4:40 ≈ 21 wpm** (target 15). 1,650 words ≈ 80 min, so it fits.
  Speed is NOT the problem. Structure and finishing every question are.

### Legal / ethical content bank (to build)
For each: definition, the law or standard, 1–2 real examples, a ready-made "As a result..." effect.
- [ ] Intellectual property: copyright, licensing (open source / proprietary / Creative Commons), plagiarism of code
- [ ] Privacy: Privacy Act 1988 and Australian Privacy Principles, GDPR, data breaches (e.g. Optus, Medibank 2022)
- [ ] Accessibility and inclusivity: WCAG
- [ ] Bias in ML / AI and how human behaviour shapes it
- [ ] Security responsibilities and consequences of insecure software
- [ ] Stakeholder vs user ethics (e.g. the targeted-ads question)
- [ ] Workplace and social impacts of automation

---

## Exam app (local Gradeo clone)
Start: `node exam-app/server.mjs` in ~/gradeo, then open **http://localhost:7788**.
Spell-check off, timer with reading time, **Rest break** button pauses the timer, autosaves.
Submitted answers are saved to `papers/attempts/<id>.md`; tell Claude "mark my attempt".
PDF papers (e.g. 2025 HSC) go in `papers/`; "Free answer sheet" is for papers read on Gradeo.

## Practice routine (agreed 24 Oct)

**Questions:** `practice/QUEUE.md`: 98 written questions from every exported paper, including ones I left blank
or never tried, in priority order (17 more reserved for Monday's mock). No Year 11 papers.
Answers and criteria are in `practice/key.json` (Claude only). Progress is in `practice/progress.json`.
Rebuild after new data with `python3 -I practice/make_queue.py`.

**Order:** extended responses (at least one a day) → legal/social/ethical → previously blank/low →
new → previously OK. Topics are mixed so consecutive questions differ.

**Loop for each question:**
1. Type it, timed at 2 min per mark, spell-check off.
2. Mark it myself (1 min): which band of the criteria, and why?
3. Claude marks it: band + the 1–2 biggest fixes.
4. Rewrite once from memory; at most one more rewrite, then move on (even at 3/4).
5. Log the fix in the progress log.

About 20–25 min per short answer, about 40 min per extended response. Roughly 6–8 questions a day.

---

## 1. Where marks are lost (from 123 marked Gradeo parts, 24 Oct)

| Question type | Score |
|---|---|
| Objective response (tables) | 94% |
| Multiple choice | 73% |
| Coding | 72% |
| Short answer 2–3 marks | 69% |
| Short answer 4–5 marks | 58% |
| **Extended response 6+ marks** | **30%** |

- **18 marks left blank** across marked exams, incl. a whole 8-mark extended response (Intellectual Property, TopicTestRevisionTest3).
- Recurring feedback words: *explain* (18), *specific / example* (26), *clearer / structure* (15), *link to the scenario*, *spelling / grammar* (3 markers).

### Content gaps (from 62 multiple-choice/objective answers, 76% right)
- **Picking too many options** on "select all that apply" (4 of 15 misses): only add a 2nd option if sure.
- **Software Engineering Project unit, SDLC definitions:** pilot vs phased installation · Waterfall order
  (integration *before* testing) · load (expected users) vs stress (breaking point) · integration (modules
  together) vs system (whole app) · SAST usable at any stage once code exists · Agile method tailoring.
- Class diagram cardinality (customer to cart = one-to-many) · ML batch normalisation (keeps layer inputs on a similar scale).
- Left authentication vs authorisation blank (knew it; time).
- Diagnostic quiz: local Canvas site, `cd ~/canvas/app && ./serve.command`, then http://localhost:8765/pages/quiz.html
  (Units 1–3 only; doesn't cover the Software Engineering Project unit).

### Claude's marking accuracy (fair blind test, 24 Oct)
Fresh Opus agents that never saw the teacher's marks marked 48 of my teacher-marked written/code answers, twice:
| Condition | Exact | Within 1 mark | Total vs teacher | Bias |
|---|---|---|---|---|
| **With marking key** (criteria + sample) | 26/48 | **48/48** | 117 vs 107.5 | slightly generous (+0.2/answer) |
| **No key** (question + answer only) | 23/48 | 47/48 | 105 vs 107.5 | about neutral, slightly harsh on long answers |
- Every short answer within 1 mark either way. Extended responses (8–10 marks) were never exact: treat as **±1–2 marks**.
- Without a key (CSSA, Trial 3) the marking is nearly as good; with a key, knock ~0.2/answer off.
- (Earlier informal test by me: within 1 mark on 14/14, but less fair; I'd seen some marks.)

### Weakest topics (marks lost)
| Topic | Score | Key feedback |
|---|---|---|
| Impact of Secure Software (ER) | 7/20 | 0/10 then 7/10 — structure extended responses |
| SQL (ER) | 0/8 | Missing WHERE, GROUP BY, ORDER BY; use AVG() |
| Intellectual Property (ER) | 0/8 | Left blank |
| UI & UX (ER) | 7/14 | Analyse *this* interface, link each issue to its goal |
| Class Diagrams | 6/11 | Give attribute types |
| Big Data | 2/6 | Link metadata to searching / indexing / distributed storage |
| Testing and Evaluating | 4/8 | |
| Web Protocols | 3/7 | Say TLS not SSL; explain how HTTP transfers data; integrity |
| Development (Agile) | 1/5 | Flexible resource allocation, cross-functional teams |
| Algorithms – pseudocode | 1/4 | Use arrays as arrays; check parameters (Extract = start, N) |
| PWAs | 2/5 | Manifest (install, icons, display mode) ≠ service worker (offline caching) |
| Python coding | 6/9 | Check *all* rows before returning; don't return early |
| Client vs server validation | — | Client = usability; server = security; you need both |
| Minimise Vulnerabilities (XSS) | 2/4 | |
| ML/AI human behaviour | 2/4 | Topic sentence + cause → link → effect |

**Strengths:** multiple choice, objective response, basic coding, DFDs (3/4).

---

## 2. Answer technique (use every time)

- **Explain:** topic sentence → for each point **cause → link → effect** → tie it to the stimulus/scenario.
- **Evaluate / assess:** state criteria → strengths and weaknesses with specific evidence → clear judgement.
- **Compare / distinguish:** similarities and differences, side by side, on the same features.
- One mark ≈ one developed point. A 4-mark answer needs about 2 developed points, an 8-mark answer about 4.
- **Never leave a blank.** A partial answer earns marks.
- **Full sentences, not dot points**, even for "identify" questions. Dot points cost a mark on Q22 (2019 SDD) because
  they "don't link back to the question".
- Show reasoning even when unsure: wrong conclusions with visible reasoning still got part marks (logic paradigm Qs).
- Budget time by marks so the extended responses at the end aren't squeezed.
- Shorter sentences; spell the key terms correctly (security, information, validation, authentication).
- Diagrams: class diagram attributes need types; a level 1 DFD needs all external entities (including other systems), every process, data flows and a data store.

---

## Course material (from the Canvas repo, cloned 24 Oct)
Source: `~/canvas` (github.com/fredgaffey/canvas, my own site sen.pebnum.com). Read-only, don't work on it.
- `papers/NESA Sample HSC Exam.pdf`: official NESA sample paper, **unseen**. Key: `papers/marking/NESA Sample HSC Exam - Marking Guidelines.pdf`
- `papers/marking/2025 HSC - Marking Guidelines (official).pdf`: key for the 2025 HSC. The paper itself still needs downloading from NESA.
- `worksheets/`: SQL ×2, schema ×4, data dictionary, DFD ×2, decision tree, UI/UX, network diagram (question + answer PDFs),
  plus "2025 Notes" (course notes doc)
- `~/canvas/app/data/questions.json`: 499 Year 12 quiz questions with answer keys
  (Web 227, Secure Software Architecture 152, Automation 120); `~/canvas/app/pages/`: 105 Year 12 lessons incl. a 16-lesson Exam Revision module

## 3. Plan (revised 24 Oct: one full paper per day)

Fresh full papers: **2025 HSC (official)** · **SEN Holiday Practise 2026** (81 marks / 145 min, full key) ·
**CSSA SE 2025** (80 / 150, key locked) · **TrialExamRevisionTest3 timed** (81 / 150, key locked).
If sitting on Gradeo: **type written answers in a plain text file as I go** (answers lock after submitting until released).
Save files to `papers/`.

### Sat 24 Oct
- [ ] Afternoon: **Holiday Practise 2026**, timed (145 min)
- [ ] Evening: Claude marks it (blanks + long answers first); SQL lesson 1 if energy allows

### Sun 25 Oct
- [ ] Morning: SQL lesson 2 (60–90 min) + one 8-marker using the full loop (#4 Intellectual Property)
- [ ] Afternoon: **2025 HSC paper**, timed (download the paper and NESA marking guidelines to `papers/` first)
- [ ] Evening: mark it against the NESA marking guidelines

### Mon 26 Oct
- [ ] Morning: **one** paper: **NESA Sample HSC Exam** (official marking guidelines), in the exam app's PDF mode. Not two; too tiring the day before.
- [ ] Afternoon: fix list from the papers: one 8-marker rewrite, SQL review, 5 min spelling drill. **Stop by about 5pm.**

### Tue 27 Oct, exam morning
- [ ] Skim section 2 and the key terms. Nothing new.

### 8-marker shape
1. Plan (2 min): circle the verb; 3 points, one example each.
2. Opening (1–2 sentences): answer directly; for "evaluate", give the judgement now.
3. Three paragraphs: Point → This is because → For example → As a result → (evaluate:) "This is effective/limited because…"
4. Closing (1–2 sentences): overall judgement. About 280 words, 16 min.

### SQL (starting from zero)
- Use `worksheets/SQL 1/2` and the Schema worksheets (question first, then answer PDF)
- [ ] SELECT, WHERE, ORDER BY
- [ ] COUNT / SUM / AVG, GROUP BY, HAVING
- [ ] JOINs
- [ ] INSERT, UPDATE, DELETE
- [ ] SQL injection and parameterised queries (security angle)

## 4. Unused practice material (never attempted)

- SEN Holiday Practise 2026 — 81 marks *(Monday mock)*
- 12SEN_SecureSoftwareArchitectureRevisionTest — 50 marks
- 12SEN_TrialExamRevisionTest1 (non-timed) — 78 marks (same paper as the timed one you sat)
- ITE Software Engineering Y11 2024 — 57 marks
- 12SEN_Cycle1–5, 8, 9, 11, 12 — short sets

Locked until results are released: TrialExamRevisionTest2/4/5, TopicTestRevisionTest4/5 attempts and others (see INDEX.md).

---

## 5. Key terms sheet

**Spelling drill list** (Monkeytype custom mode): behaviour, influence, biases, labelling, model, predict,
applicant, generation, authentication, authorisation, encryption, validation, vulnerability, intellectual property,
accessibility, privacy, security, information, development, efficiency, metadata, protocol

*(fill in during revision: term — one-line definition)*

---

## 6. Progress log

*(newest first: date — what was done — score/result — what to fix next)*

- **24 Oct** — Fair blind test with 4 fresh agents: with key 48/48 within 1 mark; no key 47/48.
- **24 Oct** — Blind-marking test: Claude within 1 mark on 14/14 answers. MC analysis: content mostly solid; gaps in SDLC definitions.
- **24 Oct** — Cloned the canvas repo: found the NESA sample exam + official marking guidelines, the 2025 HSC marking guidelines, SQL/diagram worksheets and 499 quiz questions.
- **24 Oct** — New plan: one full paper per day (Holiday Practise Sat, 2025 HSC Sun, CSSA or Trial 3 Mon), SQL from scratch, an 8-marker each day.
- **24 Oct** — Agreed practice routine; built practice/QUEUE.md (no Year 11 papers; Holiday Practise reserved for the mock).
- **24 Oct** — Practice: "How human behaviour influences ML/AI" (4 marks). 96 words, 4:40, est. **3/4**.
  Good: correct idea (biased training data) plus Amazon hiring example. Missing: the *link* step (why past hires →
  sexist model) and a 2nd point (e.g. user behaviour after release, Microsoft Tay). Next: retype from memory using the starters.
- **24 Oct** — Monkeytype: 33 wpm / 84% acc. Typing speed is fine; time is lost on composing and spelling pauses.
- **24 Oct** — Switched to typed-only practice (no dictation). Counted Trial Exam 1 sample answers: ~1,690 words,
  ~35 words/mark; 17 marks lost to near-blank answers. Next: measure typing speed.
- **24 Oct** — Confirmed: exam is typed; I have rest breaks; no scribe. Practice now ends with typing from memory, spell-check off.
- **24 Oct** — Told Claude about dyslexia: knowledge is strong (verbal answers ≈ full marks); marks lost on
  written expression. Plan now focuses on the say-then-write method, sentence starters and the legal/ethical content bank.
- **24 Oct** — Exported all Gradeo data; analysed weaknesses; made this plan.

---

## 7. Open questions / to check

- Confirm exam start time, length and section structure.
- Is spell-check available in the online exam? (assume NO; ask teacher)

### Answered
- **Exam is on a computer** (typed). (24 Oct)
- **Provisions:** I have **rest breaks**. A scribe is **not allowed**. (24 Oct)
