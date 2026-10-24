// Creates a one-off question set ("drill") that appears under "From Claude" in the exam app.
//   node exam-app/drill.mjs spec.json        -> papers/drills/<name>/exam.json   (prints the name)
//
// spec.json:
// { "title": "Explain drill 1", "minutes": 12, "reading_minutes": 0,
//   "questions": [
//     { "title": "Usability vs security", "stimulus": "optional markdown",
//       "parts": [
//         { "type": "SHORT", "marks": 4, "prompt": "Explain …", "word_limit": 150,
//           "criteria": [{ "marks": "4", "criterion": "…" }], "sample": "…" },
//         { "type": "MULTI_CHOICE", "marks": 1, "prompt": "Which …?", "options": ["…", "…", "…", "…"], "correct": ["B"] },
//         { "type": "CODING", "marks": 3, "prompt": "…", "language": "PYTHON", "starter_code": "" },
//         { "type": "SQL", "marks": 3, "prompt": "…", "dataset_setup_sql": "CREATE TABLE …" },
//         { "type": "DRAWING_V2", "marks": 4, "prompt": "Draw …" } ] } ] }
// criteria / sample / correct never reach the page (the server strips them); they're kept for marking.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DRILLS = path.join(ROOT, 'papers', 'drills');
const LETTERS = 'ABCDEFGHIJ';
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40);

const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const now = new Date();
const name = `${now.toISOString().slice(0, 16).replace(/[-:T]/g, '')}-${slug(spec.title)}`;

let total = 0, nParts = 0;
const questions = spec.questions.map((q, qi) => ({
  number: qi + 1,
  title: q.title || `Question ${qi + 1}`,
  stimulus: q.stimulus || null,
  parts: q.parts.map((p, pi) => {
    total += p.marks; nParts++;
    const question = {};
    if (p.type === 'MULTI_CHOICE') {
      question.options = p.options.map((t, i) => ({ letter: LETTERS[i], text: t, image: null, correct: (p.correct || []).includes(LETTERS[i]) }));
      question.correct_letters = p.correct || [];
    }
    for (const k of ['word_limit', 'language', 'starter_code', 'dataset_setup_sql', 'starter_query']) if (p[k] != null) question[k] = p[k];
    if (p.type === 'CODING' && !question.language) question.language = 'PYTHON';
    return {
      part_id: crypto.randomUUID(),
      part: q.parts.length > 1 ? `Part ${String.fromCharCode(65 + pi)}` : 'Part A',
      marks_available: p.marks,
      answer_type: p.type,
      prompt: p.prompt,
      question,
      marking_criteria: p.criteria || null,
      marking_rubric: null,
      marking_guidance: p.guidance || null,
      sample_answer: p.sample || null,
      result: { mark: null, feedback: [] },
      your_response: { answered: false },
    };
  }),
}));

const exam = {
  exam: spec.title, drill: true, created: now.toISOString(),
  duration_minutes: spec.minutes ?? Math.max(2, Math.round(total * 2)),
  reading_minutes: spec.reading_minutes ?? 0,
  total_available: total, parts_total: nParts, parts_answered: 0, questions,
};
fs.mkdirSync(path.join(DRILLS, name), { recursive: true });
fs.writeFileSync(path.join(DRILLS, name, 'exam.json'), JSON.stringify(exam, null, 1));
console.log(name);
