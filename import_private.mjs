// Imports trial papers that are for PERSONAL STUDY ONLY (e.g. from the SEN Discord / software.paper.is)
// into private_papers/<name>/ (exam.json + exam.md + assets), where the exam app lists them under
// "Trial papers (private)". private_papers/ must never be copied to the public hsc-se-study repo.
//   node import_private.mjs discord_inbox/paperis
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { buildPart, contentCollection, makeExamContext, parseTitle, examMd, setAssetBase } from './build.mjs';
setAssetBase('https://software.paper.is');   // their questions reference images as /img/<paper>/<n>.png
import { makeRenderer } from './render_drawings.mjs';

const SRC = process.argv[2];
const OUT = path.resolve('private_papers');
const NAMES = {
  cssa_trial: 'CSSA 2025 Trial', cssa_familiarisation: 'CSSA Familiarisation', doe_sample: 'NSW DoE Sample Exam',
  girraween: 'Girraween Trial', hsc_familiarisation: 'NESA HSC Familiarisation', hsc_sample_exam: 'NESA HSC Sample Exam',
  independent: 'Independent Trial', merewether: 'Merewether Trial', normanhurst: 'Normanhurst Trial',
  nsb: 'North Sydney Boys Trial', nsw_seng: 'NSW Software Engineering Paper', prelim: 'Preliminary (Year 11) Paper',
};
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// paper.is stores options as {id:"A"} + correctOptionsIndices; the exporter expects Gradeo's own shape.
function normalise(q, qi) {
  q.parts = (q.parts || []).map((p, pi) => {
    p.id ||= `${q.id || 'q' + qi}-${pi}-${crypto.randomUUID().slice(0, 8)}`;
    const prm = p.answer?.parameters;
    if (prm?.options) {
      prm.options = prm.options.map((o, i) => ({ displayIndex: i, ...o, id: o.id ?? String(i) }));
      if (!prm.correctOptions && prm.correctOptionsIndices) prm.correctOptions = prm.correctOptionsIndices.map(i => prm.options[i]?.id).filter(Boolean);
    }
    return p;
  });
  return q;
}

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'DO_NOT_PUBLISH.txt'), 'Personal study only. Never copy this folder into the public hsc-se-study repo (CSSA and school trials).\n');
const renderer = await makeRenderer();
for (const file of fs.readdirSync(SRC).filter(f => f.endsWith('.json')).sort()) {
  const key = file.replace(/\.json$/, '');
  const title = NAMES[key] || key;
  const raw = JSON.parse(fs.readFileSync(path.join(SRC, file), 'utf8').replace(/^﻿/, ''));
  const dir = path.join(OUT, slug(title));
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
  const X = makeExamContext(dir);
  const questions = [];
  let n = 0;
  for (const [qi, q0] of raw.entries()) {
    const q = normalise(q0, qi);
    const stim = await contentCollection(q.stimulusContentItemCollection, X);
    const parts = [];
    for (const p of q.parts) {
      try { parts.push(await buildPart(p, null, X, { dir, qid: `q${String(qi + 1).padStart(2, '0')}`, renderer, markers: {} })); }
      catch (e) { console.warn(`  ! ${title} Q${qi + 1}: ${e.message}`); }
    }
    if (!parts.length) continue;
    n++;
    const qt = q.title || parts[0]?.part || `Question ${n}`;
    questions.push({ number: n, question_id: q.id, title: qt, ...parseTitle(qt), copyright: q.copyrightText || null, stimulus: stim.md, stimulus_images: stim.images, parts });
  }
  const all = questions.flatMap(q => q.parts);
  const total = all.reduce((t, p) => t + (p.marks_available || 0), 0);
  const exam = {
    exam: title, private: true, source: 'software.paper.is via the SEN Discord (personal study only)',
    duration_minutes: total >= 70 ? 150 : Math.max(10, Math.round(total * 1.9)),
    total_available: total, parts_total: all.length, parts_answered: 0, parts_marked: 0, total_mark: null, questions,
  };
  fs.writeFileSync(path.join(dir, 'exam.json'), JSON.stringify(exam, null, 1));
  fs.writeFileSync(path.join(dir, 'exam.md'), examMd({ ...exam, syllabus: 'Software Engineering', status: 'private', review_url: '-' }));
  const keyed = all.filter(p => p.marking_criteria || p.marking_rubric || p.sample_answer || p.question?.correct_letters?.length).length;
  console.log(`✓ ${title}: ${questions.length} questions, ${all.length} parts, ${total} marks, ${keyed}/${all.length} parts with a key`);
}
await renderer.close();
