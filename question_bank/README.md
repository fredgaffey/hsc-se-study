# HSC Software Engineering question bank

A deduplicated, syllabus-tagged bank of **1,421 question parts** for the NSW HSC Software Engineering exam
(Tuesday 27 October 2026). It's built from Gradeo, NESA's online exam site and the MikeTeachesTech resources.

> **RESERVED: do not use the 32 parts with `"reserved": true` before Sunday.** They are the real
> **2025 HSC Software Engineering** paper. Their `source` starts with `RESERVED – 2025 HSC (unseen until Sunday)`. Filter them
> out of any drill or quiz (`[q for q in bank if not q["reserved"]]`). `coverage.md` leaves them out of its counts.

## Files

| Path | What it is |
|---|---|
| `bank.json` | The bank: one object per unique question part |
| `coverage.md` | Coverage of all 66 Year 12 syllabus points, sorted with the weakest at the top |
| `assets/` | Every image, diagram and video the questions refer to (`assets/...` paths in the bank are relative to this folder) |
| `raw/` | Untouched source data: Gradeo API responses for the new quizzes, the quiz-pool listing, the captured NESA papers and the 2025 marking-guideline text |
| `tools/` | The scripts that rebuild everything (see "Rebuilding") plus the manual review files |

## Sources and counts

| Source | Parts | Quality 3 / 2 / 1 | Written / objective | Notes |
|---|---:|---|---|---|
| Gradeo: existing export (`gradeo_out/exams/*/exam.json`, 28 papers) | 274 | 102 / 135 / 37 | 152 / 122 | Teacher topic tests, cycles and trial-revision tests (mostly "TKS 2025"), plus older SDD HSC items |
| Gradeo: 11 quizzes generated for this bank | 869 | 193 / 408 / 268 | 549 / 320 | The whole quiz-generator pool for the SE syllabus (536 questions): CSSA 2014–2024 and Independent Trials (ITE) 2014–2025 trial papers |
| NESA: HSC Software Engineering Familiarisation Questions | 18 | 18 / 0 / 0 | 10 / 8 | From fam.hsconline.nesa.nsw.edu.au. NESA publishes no key, so the answers are Claude's (`key_source: "claude"` plus `key_confidence`) |
| NESA: **2025 HSC paper (RESERVED)** | 32 | 31 / 1 / 0 | 16 / 16 | Keys, criteria and sample answers come from the official marking guidelines; the official full-mark student responses are in `sample_answer_images` |
| MikeTeachesTech | 228 | 42 / 184 / 2 | 149 / 79 | 160 question-bank items (Year 12 sections 1–4), Practice Trial Exam 1 (36 parts), and Practice Exam 2 (32 parts; a transcription of NESA's SE Sample Examination, marked with NESA's official guidelines) |

Dedup removed 106 duplicate parts. Duplicates are matched on normalised stimulus, prompt and option text, and the best-documented copy is kept.
`also_in` lists the other papers the same part appeared in.

**Old-course content.** Most of the Gradeo pool comes from trial papers for the *old* Software Design and Development (SDD) course.
Topics that aren't in the SE syllabus are tagged `syllabus: ["OUT"]` with quality 1. That covers 180 parts on the logic paradigm/Prolog,
assembler/registers, IEEE 754, two's complement, binary/hex, ASCII/Unicode, CASE tools, sequential/relative files, RAD, end-user
development and similar topics. SDD questions on topics that SE still covers (algorithms, testing, modelling tools, implementation
methods, social/ethical issues, and so on) are tagged normally. Year 11-only content (OOP theory, mechatronics, data representation basics) is
tagged `["Y11"]` with quality 1 (93 parts).

## Fields (`bank.json`)

| Field | Meaning |
|---|---|
| `id` | Stable id. `g-<Gradeo part id>`, `nesa-fam-q…`, `nesa-hsc2025-q…`, `mtt-…` |
| `origin` | `Gradeo`, `NESA` or `MikeTeachesTech` |
| `reserved` | `true` only for the 2025 HSC paper (don't show it before Sunday) |
| `source` | The paper or quiz it came from. For Gradeo it's the session title plus `[orig: <original paper and question>]` |
| `source_paper`, `publisher`, `also_in` | The original paper (e.g. `CSSA 2021`, `ITE 2023`, `TKS 2025`), the publisher, and other places the part appeared |
| `question_title`, `part` | The question's title and the part label |
| `stimulus`, `prompt` | Markdown. Images are `![](assets/…)` |
| `answer_type` | `MULTI_CHOICE`, `MULTI_SELECT` (tick all that apply), `OBJECTIVE_RESPONSE` (matching grid), `DROPDOWN`, `RICH_TABLE`, `SORTING`/`SORTING_TABLE` (ordering), `SHORT` (short or extended answer; `extended: true` for extended), `CODING` (+`language`), `SQL` (+`dataset_setup_sql`), `DRAWING`/`DRAWING_V2`, `IMAGE` |
| `marks` | Marks available |
| `options` | MC and multi-select options: `{letter, text, image, correct}`. Some Gradeo multi-select items are stored as `MULTI_CHOICE` with several `correct` options, and their `issues` say so |
| `objective` | Matching grid: `{columns, rows: [{statement, correct: [column…]}]}` |
| `dropdowns` | `[{label, options, correct}]` |
| `table` | Gradeo "complex table": rows of cells (`text`, `dropdown` with `correct`, `input` with `expected`) |
| `sorting` | `{items, correct_order}` (NESA/MTT). For Gradeo, the raw parameters |
| `criteria` | Marking criteria `[{marks, criterion}]` |
| `rubric`, `guidance` | Gradeo marking rubric and guidance (markdown). For the MTT question banks, `rubric` lists the marking points |
| `sample_answer`, `sample_answer_images` | Sample or official answer (markdown) and any answer images |
| `key_source`, `key_confidence` | Where the answer key came from (NESA and MTT entries) |
| `images` | Every local asset the part uses |
| `syllabus` | 1–2 ids from `study/syllabus_points.json` (e.g. `PROJ-15`), or `Y11` / `OUT` |
| `quality` | 3 = HSC-like (clear NESA directive verb, marks fit the task, scenario-based where appropriate, correct and unambiguous key); 2 = usable; 1 = poor, ambiguous, broken, out of syllabus or Year 11 |
| `issues` | Problems found in review: wrong or debatable keys, criteria copied from another question, marks that don't match the criteria, missing stimulus, images not checked, and so on |
| `reviewed`, `review_note` | `reviewed: true` means a person-style manual review set the syllabus/quality/issues (every Gradeo part was reviewed) |

## How it was built

1. **Gradeo, read-only.** Requests went through the logged-in Chrome bridge (127.0.0.1:7777), throttled to about 1.7 requests per second.
   - `GET question-bank/question-many-quiz/count` and `…/summary` are the endpoints behind Gradeo's "Generate quiz" screen.
     The summary call returns at most 50 random questions, so the pool was enumerated in slices (by syllabus item, subtopic and answer type) until all
     **536** question ids for syllabus `d1a54432…` (Software Engineering, Year 12) were known (`raw/quiz_pool_summary.json`).
     The Year 11 syllabus `79cc4e36…` has 0 quiz questions.
   - `GET exam-bank/?syllabusId=…` lists 30 SE exams (`raw/exam_bank_se.json`). Students can only read exam content through their own
     sessions, so these weren't used directly. The CSSA and ITE trial papers are reachable through the quiz pool anyway.
   - `GET exam-process/session-participant` re-checked his 49 sessions. 21 of them (the CSSA SE 2025 trial, several TrialExamRevisionTest/
     TopicTestRevisionTest sessions, 2026_12SE_Practice_Test_1 and others) return **403** on `marking-session/question/<id>`. Each was retried with a fresh
     token, and the app's own request was captured from his tab (same headers: bearer token, x-request-id, correlation ids). The app gets
     the same 403, so it's Gradeo's access control (results not released or teacher-restricted). These sessions were recorded and left alone.
2. **Gradeo quiz generation (approved by the student).** `POST /api/exam-edit/quiz` is the call the "Generate quiz" button makes (`{title, syllabusId,
   questionIds, showTimer:false, createExamSession:true}`). It was used 11 times with 50 question ids each (the UI's maximum), covering the 535 pool questions
   that weren't already exported. Each quiz's questions, answers, criteria and sample answers were then read with
   `GET marking-session/question/<markingSessionId>`. **No quiz was started and no answer was saved. The quizzes are still in his list as LIVE,
   not started.** See `raw/quizzes_created.json`:

   | Quiz title | markingSessionId | examId | Questions |
   |---|---|---|---:|
   | Generated quiz 2026-10-24 14:52:50 | f7d06ddc-0a34-4b27-9291-207b1e3d8fe1 | 520bcfee-f6be-4e40-b7dd-7a748a15ff56 | 50 |
   | Generated quiz 2026-10-24 14:53:00 | f45800dd-bdd3-4688-aa47-d7a5325c267a | 09d6ccd5-38d3-4398-b7c0-2ff30038e1ad | 50 |
   | Generated quiz 2026-10-24 14:53:00 | a81ef0cd-cdfb-4824-9256-52d8933a13d0 | 7767d0fd-9687-49c0-a9ac-ce4c33143774 | 50 |
   | Generated quiz 2026-10-24 14:53:01 | a5ebb61e-e14b-4e34-a2b1-c80e08e9dd95 | 2525f121-ee3b-4700-ac8e-4aee818e5c06 | 50 |
   | Generated quiz 2026-10-24 14:53:02 | e522d23e-a9a4-482e-aa68-321a7944f65a | a7d71982-f0fd-4f60-af73-80c180db929b | 50 |
   | Generated quiz 2026-10-24 14:53:02 | 8faaba78-8cdc-486b-b777-d1f1a73cbb77 | 62ea2c8f-275b-4c02-ab59-b123710d038e | 50 |
   | Generated quiz 2026-10-24 14:53:03 | 3f774c08-c677-442f-bcc5-05a980e753cd | 6ac78ca4-8021-45ec-9bdd-637462421316 | 50 |
   | Generated quiz 2026-10-24 14:53:04 | 2c04c912-e1de-4626-adab-992d8f232ad0 | 68727868-e6d5-4f2f-826c-41c1afdd5b9f | 50 |
   | Generated quiz 2026-10-24 14:53:04 | 8d854375-c88d-4628-8f83-3cd4ddeec67a | 0c5b53bd-50da-4ade-9fc6-02f21a9133b0 | 50 |
   | Generated quiz 2026-10-24 14:53:05 | 74fb2a6f-269c-4b91-8205-cbb0b17c7746 | 2cce25bc-f4f8-4a70-94e1-05656e18b120 | 50 |
   | Generated quiz 2026-10-24 14:53:05 | 788c11ca-47d5-4cb3-957f-a371bab63a76 | 87080f67-5e4e-4d5c-8680-ecc05ae5727a | 35 |

3. **NESA.** A private headless Chromium (playwright-core with chrome-headless-shell, not his Chrome) opened
   fam.hsconline.nesa.nsw.edu.au. Choosing a paper returns the whole paper in one Concerto response, so no exam was started and nothing personal
   was entered (`tools/nesa_capture.mjs`, `tools/nesa_md.mjs`). The entries were then cleaned by hand in `tools/make_nesa_entries.py`.
4. **MikeTeachesTech** (`/Users/fred/hsc-se-resources`, github.com/miketeachestech/hsc-software-engineering-resources, **CC BY-NC 4.0, © Michael Grassi 2025**:
   personal study use only). Parsed by `tools/make_mtt_entries.py`. Practice Exam 2 is transcribed in `tools/mtt_exam2.py`.
   Practice Exams/3 (NESA's familiarisation questions) and the Year 11 revision folder were skipped.
5. **Merge, syllabus tagging and review** (`tools/build_bank.mjs`). Gradeo's own syllabus-item tags were mapped onto the 66 points
   (`tools/gradeo_item_map.json`), but they proved unreliable: many old SDD questions are filed under "SSA-1/SSA-2". **Every Gradeo part was
   then reviewed by hand** (`tools/review/c00–c18.txt`, compiled to `tools/overrides.json`, keyed by the dedup hash). MC keys were checked by working
   the questions where the stimulus was text. Image-only options are flagged "not checked". MTT tags are in `tools/review_mtt.txt` and NESA tags are in
   `tools/make_nesa_entries.py`.

## Rebuilding

```
python3 question_bank/tools/make_nesa_entries.py
python3 question_bank/tools/make_mtt_entries.py
node    question_bank/tools/build_bank.mjs        # needs network only for Gradeo images not yet in assets/
```
`tools/enumerate.py` and `tools/make_quizzes.py` are the (already-run) Gradeo steps and need the bridge. Don't re-run `make_quizzes.py`: it would create
more quizzes in his account.

## Known gaps

- 3 Gradeo stimulus images hosted on Google Docs (lh7-rt.googleusercontent.com) return 403 and are flagged "image could not be downloaded"
  (5 parts).
- Question 27 of the 2025 HSC uses a video that NESA hasn't released (copyright), so it's quality 2.
- The familiarisation paper's keys and sample answers are Claude's, not NESA's.
- `raw/nesa_2025hsc_RESERVED*`, `raw/hsc25_marking_RESERVED.txt`, `tools/nesa_entries.json` and `tools/_review_view.json` also contain the
  reserved 2025 paper. Don't open them before Sunday either.

## Merge 24 Oct

Merged the 12 parsed `private_papers/*/exam.json` papers (origin `paper.is`, from the SEN Discord; personal study only, never copy into the public repo)
and the new PDF in `papers/` into the bank. The original is kept as `bank.before-merge.json`.

**Counts.** 1,421 entries before, **1,637** after (+219 new, −3 duplicates merged inside the old bank). 359 new parts were read in total
(322 from the 12 parsed papers plus 37 from the TH Software Tuition PDF). 126 of them were duplicates of entries already in the bank and 27 duplicated
each other (DoE sample vs Normanhurst, TH vs DoE and Normanhurst). The 32 reserved 2025 HSC entries are byte-identical to before and no new part matched them.

**New entries by source** (a part shared by two new papers is counted under the paper whose copy was kept; `also_in` lists the other):

| Source | Parts read | New entries | Matched an existing entry |
|---|---:|---:|---:|
| CSSA 2025 Trial | 33 | 0 | 33 (Gradeo, same part ids) |
| CSSA Familiarisation | 10 | 10 | 0 |
| NSW DoE Sample Exam | 29 | 26 | 0 (13 shared with Normanhurst, 2 with TH) |
| Girraween Trial (no keys) | 34 | 27 | 7 (Gradeo) |
| Independent Trial | 32 | 7 | 25 (Gradeo) |
| Merewether Trial | 32 | 25 | 7 (Gradeo) |
| NESA HSC Familiarisation | 18 | 0 | 18 (`nesa-fam-*`) |
| NESA HSC Sample Exam | 32 | 0 | 32 (`mtt-exam2-*`, i.e. MikeTeachesTech Practice Exam 2) |
| Normanhurst Trial | 29 | 16 | 4 (Gradeo) |
| North Sydney Boys Trial | 18 | 18 | 0 |
| NSW Software Engineering Paper (student-written, unofficial) | 30 | 30 | 0 |
| Preliminary (Year 11) Paper | 25 | 25 (13 tagged `Y11`; the rest are algorithm, DFD and SDLC items the Year 12 syllabus also covers) | 0 |
| TH Software Tuition 2026 Trial (PDF, no answers) | 37 | 35 | 0 (2 shared with DoE and Normanhurst) |

New entries by quality: 89 at 3, 104 at 2, 26 at 1; 19 are tagged `Y11` (13 Preliminary, 4 Girraween, 1 North Sydney, 1 NSW paper). All 219 were tagged by hand (`reviewed: true`, tags in `tools/merge_oct24_tags.json`).

**PDFs checked against the parsed papers (first questions compared; same wording, options and numbering):**

| PDF | Result |
|---|---|
| `2025 Independent SE Trial (AceHSC).pdf` (scanned) | **Duplicate** of `private_papers/independent-trial` (Q1 Privacy by Design, Q2 CSRF, Q3 email protocol, Q4 client-side, Q5 automation, Q6 regression, Q18 race condition). Not re-parsed. |
| `2025 NSW DoE Sample Trial SE.pdf` | **Duplicate** of `private_papers/nsw-doe-sample-exam` (22 of 29 prompts found verbatim in the PDF text; the rest differ only by line breaks). The keys in `marking/2025 NSW DoE Sample Trial SE - Answers.docx` agree with the parsed keys. Not re-parsed. Normanhurst re-uses 11-13 of its questions. |
| `2026 TH Software Tuition SE Trial.pdf` | **New paper** (no overlap beyond 3 shared questions). Transcribed by hand in `tools/make_th_entries.py`: 19 MC, 12 short answer, 6 extended (79 marks). The paper has no marking guidelines, so only MC answers (and two trace questions) carry Claude's key (`key_source: claude`). |
| `MikeTeachesTech Practice Exam 1.pdf` | Skipped, already in the bank. |

**Duplicate handling.** Two parts are the same when prompt, stimulus and option or grid text are each at least 90% similar (difflib on normalised text) and any images are the same files.
The kept copy is the most complete key (correct options, criteria, sample answer), then NESA > paper.is/school trial > Gradeo > MikeTeachesTech.
Missing fields are filled from the other copies, all copies are listed in `also_in`, `merge_note` says what was copied, and the kept entry keeps the existing bank id.
NESA's own papers (Familiarisation, Sample Exam) became `origin: NESA` with a `paper.is (exam.json answers)` key. The NESA Sample Exam entries remain `mtt-exam2-*` ids.
Near-identical questions that differ only in one key term (for example the ITE 2017 "Define ... Inheritance / Attributes / Classes" family, or 2's complement vs sign modulus) were deliberately kept apart.
Inside the old bank, 3 near-duplicates were merged (the chat-app sandboxing item, the parallel-installation item and the Agile "regular working versions" item).

**Answer-key and source problems recorded in `issues`:**
- `KEY CONFLICT` between copies: DoE Q3 (unsupervised model: DoE says neural network, Normanhurst says KNN; none of the options is a standard unsupervised model, so quality 1).
- Debatable keys: Normanhurst CSS multi-select (D and F), Normanhurst Q3 (Phased vs Pilot), Normanhurst Q4 (POP3 vs IMAP), Merewether Q9 (FOR...NEXT for an array of unknown length), DoE Q5 ("produces code faster than Waterfall" marked correct).
- Wrong key: Preliminary paper Big O item keys bubble sort as O(n).
- Existing entry `g-0fc8049d-...` (CSSA 2025 Q22b): the sample answer computes minutes with `//60` instead of `% 60`.
- Girraween has no keys at all: clear Year 12 MC items got Claude's key (`key_source: claude`), the rest are flagged. Matching grids and dropdown tables with no key (Girraween Q18 and Q27, Preliminary documentation item) are flagged.
- 9 prompts or sample answers referenced images that were never exported (`img/...` paths in the Merewether, North Sydney Boys, NSW Software Engineering and Familiarisation papers): the broken link was replaced by "[image not available in the source export]".
- Items whose options or stimulus are images only are marked "not checked".
- `nesa-fam-q2`: the paper.is copy is a multiple-choice variant with a differently ordered results table, so the old dropdown copy was replaced and its sample answer dropped.
- Girraway SQL "quoted number" items and TH Q10/Q12 are flagged as debatable or unkeyed.

**Coverage.** `coverage.md` was regenerated (73 Year 12 points now; the 66 mentioned above predates the syllabus file's current contents) with the same script logic as `build_bank.mjs`. Still thin: PROJ-14 (2 parts), WEB-15, SSA-1, AUTO-2, WEB-8, AUTO-10, WEB-17, WEB-20 and WEB-12 (no HSC-like quality-3 written question for PROJ-14, WEB-15, SSA-1, AUTO-2 and WEB-12).

**Scripts** (run in this order; `merge_oct24_finish.py --prune` is the last step and removes unused copied images, after which the build step can no longer be re-run):
`tools/merge_oct24_convert.py` (parse and copy images, writes `tools/_merge_candidates.json`), `tools/make_th_entries.py`, `tools/merge_oct24_build.py` (cluster and merge,
uses `merge_oct24_match.py`), `tools/merge_oct24_finish.py` (tags, key checks, atomic write of `bank.json`), `tools/merge_oct24_coverage.py`.
The `origin` field now also takes `paper.is` and `TH Software Tuition`.
