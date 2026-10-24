// Local Gradeo-style exam app.  Run:  node exam-app/server.mjs   then open http://localhost:7788
// - Sits any exported Gradeo paper (answers, criteria and sample answers are stripped before they reach the page)
// - "PDF paper" mode for papers you only have as a PDF (put them in papers/)
// - Autosaves to papers/attempts/<id>.json; on submit also writes <id>.md (answers + auto-marked MC) for Claude to mark
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const APP = path.join(ROOT, 'exam-app');
const EXAMS = path.join(ROOT, 'gradeo_out', 'exams');
const PAPERS = path.join(ROOT, 'papers');
const ATTEMPTS = path.join(PAPERS, 'attempts');
const PORT = +process.env.PORT || 7788;
fs.mkdirSync(ATTEMPTS, { recursive: true });

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp',
  '.pdf': 'application/pdf', '.mp4': 'video/mp4', '.mov': 'video/quicktime', '.webm': 'video/webm', '.md': 'text/markdown; charset=utf-8',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

const DRILLS = path.join(ROOT, 'papers', 'drills');
// "drill:<name>" = a one-off question set Claude wrote into papers/drills/<name>/exam.json
const examDir = folder => folder.startsWith('drill:') ? path.join(DRILLS, path.basename(folder.slice(6))) : path.join(EXAMS, path.basename(folder));
const readExam = folder => JSON.parse(fs.readFileSync(path.join(examDir(folder), 'exam.json'), 'utf8'));

// Remove everything that would give the answer away.
function sanitize(e) {
  return {
    exam: e.exam, folder: e.folder, duration_minutes: e.duration_minutes, total_available: e.total_available, reading_minutes: e.reading_minutes ?? null, drill: !!e.drill,
    questions: e.questions.map(q => ({
      number: q.number, title: q.title, stimulus: q.stimulus,
      parts: q.parts.map(p => {
        const s = p.question || {};
        const question = {};
        if (s.options) question.options = s.options.map(o => ({ letter: o.letter, text: o.text, image: o.image }));
        if (s.options) question.multi = (s.correct_letters || []).length > 1;
        if (s.columns) { question.columns = s.columns; question.rows = s.rows.map(r => ({ statement: r.statement })); }
        if (s.table) question.table = s.table.map(row => row.map(c => c.type === 'text' ? { type: 'text', text: c.text } : c.type === 'dropdown' ? { type: 'dropdown', options: c.options } : { type: 'input' }));
        for (const k of ['word_limit', 'language', 'starter_code', 'dataset_setup_sql', 'starter_query', 'background_images']) if (s[k] != null) question[k] = s[k];
        return { part_id: p.part_id, part: p.part, marks: p.marks_available, type: p.answer_type, prompt: p.prompt, question };
      }),
    })),
  };
}

function listExams() {
  const out = [];
  for (const folder of fs.readdirSync(EXAMS)) {
    try {
      const e = readExam(folder);
      if (/\bY11\b/.test(e.exam)) continue; // Year 11 papers excluded (not relevant to the HSC)
      out.push({ folder, exam: e.exam, marks: e.total_available, minutes: e.duration_minutes, parts: e.parts_total, sat: e.parts_answered > 0 });
    } catch {}
  }
  return out.sort((a, b) => b.marks - a.marks || a.exam.localeCompare(b.exam));
}

function listDrills() {
  if (!fs.existsSync(DRILLS)) return [];
  const submitted = new Set();
  for (const f of fs.readdirSync(ATTEMPTS).filter(f => f.endsWith('.json'))) {
    try { const a = JSON.parse(fs.readFileSync(path.join(ATTEMPTS, f), 'utf8')); if (a.submittedAt) submitted.add(a.folder); } catch {}
  }
  const out = [];
  for (const name of fs.readdirSync(DRILLS)) {
    try {
      const e = readExam('drill:' + name);
      const folder = 'drill:' + name;
      out.push({ folder, exam: e.exam, marks: e.total_available, minutes: e.duration_minutes, parts: e.parts_total, created: e.created || '', done: submitted.has(folder), drill: true });
    } catch {}
  }
  return out.sort((a, b) => (b.created || '').localeCompare(a.created || ''));
}

// ---- marking pack written on submit ----
const fence = s => '```\n' + (s || '').replace(/\n+$/, '') + '\n```';
function attemptMd(a) {
  const L = [`# Attempt: ${a.title}`, '', `- Started: ${a.startedAt || '–'} · Submitted: ${a.submittedAt || '(not submitted)'}`,
    `- Time used: ${Math.round((a.timeUsedMs || 0) / 60000)} min of ${a.durationMinutes ?? '–'} · Rest breaks: ${(a.pauses || []).length} (${Math.round((a.pauses || []).reduce((t, p) => t + ((p.end || Date.now()) - p.start), 0) / 60000)} min)`];
  if (a.mode === 'pdf') {
    L.push(`- Paper: papers/${a.pdf}`, '', '## Multiple choice', '');
    L.push(Object.entries(a.mc || {}).sort((x, y) => +x[0] - +y[0]).map(([n, l]) => `${n}. ${l}`).join('\n') || '(none)');
    L.push('', '## Written answers');
    for (const w of a.written || []) L.push('', `### ${w.label || '(unlabelled)'}${w.marks ? ` (${w.marks} marks)` : ''}`, '', w.text ? w.text : '_(blank)_', '', `*${wc(w.text)} words*`);
    return L.join('\n') + '\n';
  }
  const e = readExam(a.folder);
  let auto = 0, autoMax = 0;
  for (const q of e.questions) {
    L.push('', '---', '', `## ${q.number}. ${q.title}`);
    for (const p of q.parts) {
      const ans = a.answers?.[p.part_id];
      const s = p.question || {};
      L.push('', `### ${p.part || 'Part'} (${p.marks_available} marks, ${p.answer_type})`, '', p.prompt || '');
      if (p.answer_type === 'MULTI_CHOICE') {
        const got = [...(ans?.letters || [])].sort().join(',');
        const ok = got === [...s.correct_letters].sort().join(',');
        if (ok) auto += p.marks_available; autoMax += p.marks_available;
        L.push('', `**Your answer:** ${got || '(blank)'} · correct: ${s.correct_letters.join(',')} → **${ok ? p.marks_available : 0}/${p.marks_available}** (auto)`);
      } else if (p.answer_type === 'OBJECTIVE_RESPONSE') {
        let right = 0;
        L.push('', '| Statement | Yours | Correct |', '|---|---|---|');
        s.rows.forEach((r, i) => { const y = ans?.rows?.[i] || '–'; if (r.correct.includes(y)) right++; L.push(`| ${r.statement} | ${y} | ${r.correct.join(', ')} |`); });
        const m = right === s.rows.length ? p.marks_available : 0;
        auto += m; autoMax += p.marks_available;
        L.push('', `${right}/${s.rows.length} rows right → **${m}/${p.marks_available}** (auto, all-or-nothing; partial marks need checking)`);
      } else if (p.answer_type === 'RICH_TABLE') {
        L.push('', ...s.table.map((row, ri) => '| ' + row.map((c, ci) => c.type === 'text' ? (c.text || '') : `**${ans?.cells?.[`${ri},${ci}`] || '–'}**${c.correct ? ` (correct: ${c.correct.join('/')})` : ''}`).join(' | ') + ' |'));
      } else if (p.answer_type === 'DRAWING_V2') {
        const n = (ans?.elements || []).filter(x => !x.isDeleted).length;
        L.push('', n ? `Drawing: ${n} elements (rendered: ${a.id}_${p.part_id}.png)` : '_(blank drawing)_');
      } else {
        const t = ans?.text ?? '';
        L.push('', '**Your answer:**', '', p.answer_type === 'SHORT' ? (t ? t.split('\n').map(l => '> ' + l).join('\n') : '_(blank)_') : fence(t), '', `*${wc(t)} words*`);
      }
    }
  }
  L.splice(3, 0, `- Auto-marked (MC + objective response): **${auto}/${autoMax}**. Written answers: to be marked by Claude.`);
  const T = a.timing;
  if (T?.q) {
    const m = ms => ms == null ? '–' : `${Math.floor(ms / 60000)}:${String(Math.round(ms / 1000) % 60).padStart(2, '0')}`;
    L.push('', '---', '', '## Timing', '', 'Time on each question (on screen; reading time and breaks excluded). Target ≈ 2 min per mark.', '',
      '| Q | Marks | Time | Target | Visits | Started typing after | Words | Words/min |', '|---|---|---|---|---|---|---|---|');
    for (const q of e.questions) {
      const t = T.q[String(q.number)] || {};
      const marks = q.parts.reduce((n, p) => n + (p.marks_available || 0), 0);
      const words = q.parts.reduce((n, p) => n + wc(a.answers?.[p.part_id]?.text), 0);
      const firsts = q.parts.map(p => T.p?.[p.part_id]?.firstMs).filter(v => v != null);
      const start = firsts.length && t.firstSeenMs != null ? Math.min(...firsts) - t.firstSeenMs : null;
      const flag = t.ms > marks * 2 * 60000 * 1.5 ? ' ⚠ long' : '';
      L.push(`| ${q.number} | ${marks} | ${m(t.ms)}${flag} | ${m(marks * 120000)} | ${t.visits ?? 0} | ${m(start)} | ${words || '–'} | ${words && t.ms ? (words / (t.ms / 60000)).toFixed(0) : '–'} |`);
    }
    if (T.awayMs > 5000) L.push('', `Time with the exam window in the background: ${m(T.awayMs)}.`);
  }
  return L.join('\n') + '\n';
}
const wc = s => (s || '').split(/\s+/).filter(Boolean).length;

// ---- http ----
const send = (res, code, body, type = 'application/json') => { res.writeHead(code, { 'content-type': type, 'cache-control': 'no-store' }); res.end(typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body)); };
const safeJoin = (base, rel) => { const p = path.resolve(base, rel); if (!p.startsWith(base + path.sep)) throw new Error('bad path'); return p; };
const readBody = req => new Promise((r, j) => { let s = ''; req.on('data', d => { s += d; if (s.length > 50e6) j(new Error('too big')); }); req.on('end', () => r(s)); });

function serveFile(req, res, file) {
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) return send(res, 404, 'not found', 'text/plain');
  const type = MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
  const size = fs.statSync(file).size;
  const range = req.headers.range?.match(/bytes=(\d*)-(\d*)/);
  if (range) { // videos need range requests
    const start = range[1] ? +range[1] : 0, end = range[2] ? +range[2] : size - 1;
    res.writeHead(206, { 'content-type': type, 'content-range': `bytes ${start}-${end}/${size}`, 'accept-ranges': 'bytes', 'content-length': end - start + 1 });
    return fs.createReadStream(file, { start, end }).pipe(res);
  }
  res.writeHead(200, { 'content-type': type, 'content-length': size, 'accept-ranges': 'bytes' });
  fs.createReadStream(file).pipe(res);
}

http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    const p = decodeURIComponent(url.pathname);
    if (p === '/' || p === '/index.html') return serveFile(req, res, path.join(APP, 'index.html'));
    if (p === '/app.js' || p === '/style.css') return serveFile(req, res, path.join(APP, p.slice(1)));
    if (p.startsWith('/nesa/')) return serveFile(req, res, safeJoin(path.join(APP, 'nesa'), p.slice(6))); // NESA-look fonts/icons (local copies)
    if (p === '/vendor/marked.js') return serveFile(req, res, path.join(ROOT, 'node_modules/marked/lib/marked.umd.js'));
    if (p.startsWith('/exams/')) return serveFile(req, res, safeJoin(EXAMS, p.slice(7)));
    if (p.startsWith('/papers/')) return serveFile(req, res, safeJoin(PAPERS, p.slice(8)));
    if (p === '/api/exams') return send(res, 200, { exams: listExams(), drills: listDrills(), pdfs: fs.readdirSync(PAPERS).filter(f => f.toLowerCase().endsWith('.pdf')) });
    if (p.startsWith('/api/exam/')) { const folder = p.slice(10); const e = readExam(folder); return send(res, 200, sanitize({ ...e, folder })); }
    if (p === '/api/attempts') {
      return send(res, 200, fs.readdirSync(ATTEMPTS).filter(f => f.endsWith('.json')).map(f => {
        const a = JSON.parse(fs.readFileSync(path.join(ATTEMPTS, f), 'utf8'));
        return { id: a.id, title: a.title, mode: a.mode, startedAt: a.startedAt, submittedAt: a.submittedAt };
      }).sort((a, b) => (b.startedAt || '').localeCompare(a.startedAt || '')));
    }
    if (p.startsWith('/api/attempt/')) {
      const id = path.basename(p.slice(13)).replace(/[^\w.-]/g, '');
      const file = path.join(ATTEMPTS, id + '.json');
      if (req.method === 'GET') return fs.existsSync(file) ? send(res, 200, fs.readFileSync(file, 'utf8')) : send(res, 404, {});
      if (req.method === 'POST') {
        const a = JSON.parse(await readBody(req));
        a.id = id;
        a.savedAt = new Date().toISOString();
        // drawings: save PNG snapshots sent by the page
        for (const [pid, dataUrl] of Object.entries(a._drawingPngs || {}))
          if (dataUrl) fs.writeFileSync(path.join(ATTEMPTS, `${id}_${pid}.png`), Buffer.from(dataUrl.split(',')[1], 'base64'));
        delete a._drawingPngs;
        fs.writeFileSync(file + '.tmp', JSON.stringify(a, null, 1));
        fs.renameSync(file + '.tmp', file);
        if (a.submittedAt) fs.writeFileSync(path.join(ATTEMPTS, id + '.md'), attemptMd(a));
        return send(res, 200, { ok: true, savedAt: a.savedAt });
      }
    }
    send(res, 404, 'not found', 'text/plain');
  } catch (e) {
    console.error(e);
    send(res, 500, String(e.message || e), 'text/plain');
  }
}).listen(PORT, '127.0.0.1', () => console.log(`Exam app: http://localhost:${PORT}`));
