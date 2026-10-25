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
const MARKS = path.join(PAPERS, 'claude_marks');   // one file per "Ask Claude to mark" request (+ its result)
const PORT = +process.env.PORT || 7788;
fs.mkdirSync(ATTEMPTS, { recursive: true });
fs.mkdirSync(MARKS, { recursive: true });

const markClients = new Set();   // open SSE streams: { attempt, res }
const marksFor = attemptId => fs.readdirSync(MARKS).filter(f => f.endsWith('.json'))
  .map(f => JSON.parse(fs.readFileSync(path.join(MARKS, f), 'utf8'))).filter(m => m.attempt === attemptId);
const pauseSummary = pz => {   // rest breaks vs clock stops for "Report a problem" and "Ask Claude to mark"
  const mins = l => Math.round(l.reduce((t, p) => t + ((p.end || Date.now()) - p.start), 0) / 60000);
  const rest = pz.filter(p => !p.kind), other = pz.filter(p => p.kind);
  return `Rest breaks: ${rest.length} (${mins(rest)} min)` + (other.length ? ` · Clock stopped (pause/report/marking): ${other.length} (${mins(other)} min)` : '');
};
const markSummary = m => ({ id: m.id, part_id: m.part_id, marks: m.marks, result: m.result, chat: !!m.chat, thread: m.thread || [] });
const pushMark = m => { const msg = `data: ${JSON.stringify(markSummary(m))}\n\n`; for (const c of markClients) if (c.attempt === m.attempt) c.res.write(msg); };

const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp',
  '.pdf': 'application/pdf', '.mp4': 'video/mp4', '.mov': 'video/quicktime', '.webm': 'video/webm', '.md': 'text/markdown; charset=utf-8',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

const DRILLS = path.join(ROOT, 'papers', 'drills');
// "drill:<name>" = a one-off question set Claude wrote into papers/drills/<name>/exam.json
const PRIVATE = path.join(ROOT, 'private_papers');   // personal-study papers; never published
const examDir = folder => folder.startsWith('drill:') ? path.join(DRILLS, path.basename(folder.slice(6)))
  : folder.startsWith('private:') ? path.join(PRIVATE, path.basename(folder.slice(8))) : path.join(EXAMS, path.basename(folder));
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
  if (fs.existsSync(PRIVATE)) for (const name of fs.readdirSync(PRIVATE)) {
    try {
      const e = readExam('private:' + name);
      out.push({ folder: 'private:' + name, exam: e.exam, marks: e.total_available, minutes: e.duration_minutes, parts: e.parts_total, sat: false, private: true });
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

// ---- writing-flow analysis from the keystroke log ----
// Replays [ms, pos, deleted, inserted] entries so every character in the final text knows when it was typed,
// the gap before it, and how many backspaces happened right after it.
const PAUSE = 5000;
function writingFlow(log) {
  const chars = [];
  let prev = null, dels = 0;
  for (const [t, pos, d, ins] of log) {
    const gap = prev == null ? 0 : Math.max(0, t - prev);
    prev = t;
    if (d) { const gone = chars.splice(pos, d); dels += d; const c = chars[pos - 1] || chars[pos]; if (c) c.del += d + gone.reduce((n, g) => n + g.del, 0); }
    if (ins) chars.splice(pos, 0, ...[...ins].map((ch, k) => ({ ch, gap: k ? 0 : gap, del: 0, pasted: ins.length > 3 })));
  }
  const words = [], sentences = [];
  let w = null, sen = { text: '', ms: 0, del: 0, pauses: 0, words: 0 };
  const endSentence = () => { if (sen.text.trim()) sentences.push(sen); sen = { text: '', ms: 0, del: 0, pauses: 0, words: 0 }; };
  chars.forEach((c, i) => {
    sen.text += c.ch; sen.ms += c.gap; sen.del += c.del; if (c.gap >= PAUSE) sen.pauses++;
    if (/\s/.test(c.ch)) { if (w) { words.push(w); sen.words++; w = null; } }
    else {
      if (!w) w = { text: '', typeMs: 0, pause: 0, mid: false, del: 0 };
      if (c.gap >= PAUSE && c.gap > w.pause) { w.pause = c.gap; w.mid = w.text.length > 0; }
      w.text += c.ch; w.del += c.del; if (c.gap < PAUSE && !c.pasted) w.typeMs += c.gap;
    }
    if (/[.!?]/.test(c.ch) && /\s|$/.test(chars[i + 1]?.ch ?? '') || c.ch === '\n') { if (w) { words.push(w); sen.words++; w = null; } endSentence(); }
  });
  if (w) { words.push(w); sen.words++; }
  endSentence();
  const totalMs = log.length ? log[log.length - 1][0] - log[0][0] : 0;
  const pauseMs = chars.reduce((n, c) => n + (c.gap >= PAUSE ? c.gap : 0), 0);
  return { words, sentences, dels, totalMs, pauseMs, events: log.length };
}
function flowMd(log, label) {
  const f = writingFlow(log);
  if (f.events < 10) return [];
  const m = ms => `${Math.floor(ms / 60000)}:${String(Math.round(ms / 1000) % 60).padStart(2, '0')}`;
  const sec = ms => `${(ms / 1000).toFixed(ms < 10000 ? 1 : 0)} s`;
  const clean = t => t.replace(/[^\w'’-]/g, '');
  const L = ['', `### Writing flow: ${label}`, '',
    `Typing ${m(f.totalMs)} from first to last keystroke · ${m(f.pauseMs)} of that in pauses of 5 s or more · ${f.dels} characters deleted.`, '',
    '| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |', '|---|---|---|---|---|---|---|'];
  f.sentences.forEach((x, i) => L.push(`| ${i + 1} | ${x.text.trim().slice(0, 45).replace(/\|/g, '/')}… | ${m(x.ms)} | ${x.words} | ${x.ms ? Math.round(x.words / (x.ms / 60000)) : '–'} | ${x.pauses} | ${x.del} |`));
  const pauses = f.words.filter(w => w.pause).sort((a, b) => b.pause - a.pause).slice(0, 6);
  if (pauses.length) L.push('', '**Longest pauses**: ' + pauses.map(w => `${sec(w.pause)} ${w.mid ? 'in the middle of' : 'before'} “${clean(w.text)}”`).join(' · '));
  const fixes = f.words.filter(w => w.del >= 2).sort((a, b) => b.del - a.del).slice(0, 8);
  if (fixes.length) L.push('', '**Most-corrected words** (backspaces): ' + fixes.map(w => `“${clean(w.text)}” ${w.del}`).join(' · '));
  const slow = f.words.filter(w => clean(w.text).length >= 4 && w.typeMs).map(w => ({ ...w, per: w.typeMs / clean(w.text).length }))
    .sort((a, b) => b.per - a.per).slice(0, 8);
  if (slow.length) L.push('', '**Slowest words per letter**: ' + slow.map(w => `“${clean(w.text)}” ${(w.per / 1000).toFixed(1)} s/letter`).join(' · '));
  return L;
}

// ---- marking pack written on submit ----
const fence = s => '```\n' + (s || '').replace(/\n+$/, '') + '\n```';
function attemptMd(a) {
  const L = [`# Attempt: ${a.title}`, '', `- Started: ${a.startedAt || '–'} · Submitted: ${a.submittedAt || '(not submitted)'}`,
    `- Time used: ${Math.round((a.timeUsedMs || 0) / 60000)} min of ${a.durationMinutes ?? '–'} · ` + pauseSummary(a.pauses || [])];
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
      const ck = a.checked?.[p.part_id];
      if (ck) L.push('', `🔎 Checked live (answer locked): ${ck.correct === true ? 'correct' : ck.correct === false ? 'incorrect' : 'self-marked'}`);
      for (const [k, h] of (a.history?.[p.part_id] || []).entries())
        L.push('', `✏️ Edited after feedback. Attempt ${k + 1}${h.mark ? ` (Claude ${h.mark.mark}/${p.marks_available})` : h.correct === true ? ' (correct)' : h.correct === false ? ' (incorrect)' : ''}:`, '',
          h.answer?.letters ? `> ${h.answer.letters.join(', ')}` : (h.answer?.text || '_(blank)_').split('\n').map(x => '> ' + x).join('\n'));
      const n = a.notes?.[p.part_id];
      if (n && (n.tags?.length || n.text?.trim())) L.push('', `📝 **Your notes:** ${[...(n.tags || []), n.text?.trim() ? `“${n.text.trim()}”` : ''].filter(Boolean).join(' · ')}`);
    }
  }
  L.splice(3, 0, `- Auto-marked (MC + objective response): **${auto}/${autoMax}**. Written answers: to be marked by Claude.`);
  const noteCounts = {};
  for (const n of Object.values(a.notes || {})) for (const t of n.tags || []) noteCounts[t] = (noteCounts[t] || 0) + 1;
  const noted = Object.values(a.notes || {}).filter(n => n.tags?.length || n.text?.trim()).length;
  if (noted) L.splice(4, 0, `- 📝 Notes on ${noted} question${noted === 1 ? '' : 's'}: ${Object.entries(noteCounts).map(([t, c]) => `${t} ×${c}`).join(', ') || 'text only'}`);
  const T = a.timing;
  if (T?.q) {
    const m = ms => ms == null ? '–' : `${Math.floor(ms / 60000)}:${String(Math.round(ms / 1000) % 60).padStart(2, '0')}`;
    L.push('', '---', '', '## Timing', '', 'Time on each question (on screen; reading time and breaks excluded). Target ≈ 2 min per mark.', '',
      '| Q | Marks | Time | Target | Your plan | Visits | Started typing after | Words | Words/min |', '|---|---|---|---|---|---|---|---|---|');
    for (const q of e.questions) {
      const t = T.q[String(q.number)] || {};
      const marks = q.parts.reduce((n, p) => n + (p.marks_available || 0), 0);
      const words = q.parts.reduce((n, p) => n + wc(a.answers?.[p.part_id]?.text), 0);
      const firsts = q.parts.map(p => T.p?.[p.part_id]?.firstMs).filter(v => v != null);
      const start = firsts.length && t.firstSeenMs != null ? Math.min(...firsts) - t.firstSeenMs : null;
      const flag = t.ms > marks * 2 * 60000 * 1.5 ? ' ⚠ long' : '';
      L.push(`| ${q.number} | ${marks} | ${m(t.ms)}${flag} | ${m(marks * 120000)} | ${a.qBudget?.[q.number] ? m(a.qBudget[q.number].ms) : '–'} | ${t.visits ?? 0} | ${m(start)} | ${words || '–'} | ${words && t.ms ? (words / (t.ms / 60000)).toFixed(0) : '–'} |`);
    }
    if (T.awayMs > 5000) L.push('', `Time with the exam window in the background: ${m(T.awayMs)}.`);
  }
  if (a.keylog) {
    const flows = [];
    for (const q of e.questions) for (const p of q.parts) {
      const log = a.keylog[p.part_id];
      if (log?.length) flows.push(...flowMd(log, `Q${q.number}${q.parts.length > 1 ? ' ' + (p.part || '') : ''}`));
    }
    if (flows.length) L.push('', '---', '', '## Writing flow (from keystrokes)', ...flows);
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
  const noCache = /\.(html|js|css|excalidrawlib)$/i.test(file) ? { 'cache-control': 'no-cache' } : {};   // always pick up app updates
  res.writeHead(200, { 'content-type': type, 'content-length': size, 'accept-ranges': 'bytes', ...noCache });
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
    if (p.startsWith('/exams/')) { const [folder, ...rest] = p.slice(7).split('/'); return serveFile(req, res, safeJoin(examDir(folder), rest.join('/'))); }
    if (p.startsWith('/papers/')) return serveFile(req, res, safeJoin(PAPERS, p.slice(8)));
    if (p === '/api/report' && req.method === 'POST') {   // "Report a problem" notes for Claude
      const r = JSON.parse(await readBody(req));
      fs.appendFileSync(path.join(PAPERS, 'reports.jsonl'), JSON.stringify(r) + '\n');
      return send(res, 200, { ok: true });
    }
    // "Ask Claude to mark": the page posts one answer; Claude (watching mark_requests.jsonl) posts the mark back;
    // results are pushed to open pages with Server-Sent Events.
    if (p === '/api/claude-mark' && req.method === 'POST') {
      const r = JSON.parse(await readBody(req));
      const e = readExam(r.folder || '');
      const part = e.questions.flatMap(q => q.parts).find(x => x.part_id === r.part_id);
      if (!part) return send(res, 404, { error: 'no such question' });
      const id = `${new Date().toISOString().replace(/[-:.TZ]/g, '').slice(0, 14)}-${crypto.randomUUID().slice(0, 6)}`;
      const png = path.join(ATTEMPTS, `${r.attempt}_${r.part_id}.png`);
      const reqObj = {
        id, at: new Date().toISOString(), attempt: r.attempt, folder: r.folder, exam: e.exam, question: r.question,
        part_id: r.part_id, marks: part.marks_available, type: part.answer_type, prompt: part.prompt,
        answer: r.answer, drawing_png: fs.existsSync(png) ? png : null, time_ms: r.time_ms,
        key: { criteria: part.marking_criteria, rubric: part.marking_rubric, guidance: part.marking_guidance, sample_answer: part.sample_answer, correct_letters: part.question?.correct_letters },
        result: null, chat: !!r.chat, thread: [],
      };
      fs.writeFileSync(path.join(MARKS, id + '.json'), JSON.stringify(reqObj, null, 1));
      if (!r.chat) fs.appendFileSync(path.join(PAPERS, 'mark_requests.jsonl'), JSON.stringify({ id, attempt: r.attempt, exam: e.exam, question: r.question }) + '\n');
      return send(res, 200, { id });
    }
    if (p.startsWith('/api/claude-mark/') && p.endsWith('/result') && req.method === 'POST') {   // Claude posts { mark, feedback }
      const id = path.basename(p.slice(17, -7));
      const file = path.join(MARKS, id + '.json');
      if (!fs.existsSync(file)) return send(res, 404, {});
      const m = JSON.parse(fs.readFileSync(file, 'utf8'));
      m.result = { ...JSON.parse(await readBody(req)), at: new Date().toISOString() };
      fs.writeFileSync(file, JSON.stringify(m, null, 1));
      const msg = `data: ${JSON.stringify(markSummary(m))}\n\n`;
      for (const c of markClients) if (c.attempt === m.attempt) c.res.write(msg);
      return send(res, 200, { ok: true, pushed: [...markClients].filter(c => c.attempt === m.attempt).length });
    }
    if (p.startsWith('/api/claude-mark/') && p.endsWith('/message') && req.method === 'POST') {   // dialog: { from: 'student'|'claude', text }
      const id = path.basename(p.slice(17, -8));
      const file = path.join(MARKS, id + '.json');
      if (!fs.existsSync(file)) return send(res, 404, {});
      const m = JSON.parse(fs.readFileSync(file, 'utf8'));
      const msg = JSON.parse(await readBody(req));
      (m.thread ||= []).push({ from: msg.from === 'claude' ? 'claude' : 'student', text: String(msg.text || ''), at: new Date().toISOString() });
      fs.writeFileSync(file, JSON.stringify(m, null, 1));
      if (msg.from !== 'claude') fs.appendFileSync(path.join(PAPERS, 'mark_requests.jsonl'), JSON.stringify({ id, attempt: m.attempt, exam: m.exam, question: m.question, reply: true }) + '\n');
      pushMark(m);
      return send(res, 200, { ok: true });
    }
    if (p === '/api/claude-mark/events') {   // SSE stream for one attempt: sends existing results, then new ones as they arrive
      const attemptId = url.searchParams.get('attempt') || '';
      res.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'keep-alive' });
      for (const m of marksFor(attemptId)) res.write(`data: ${JSON.stringify(markSummary(m))}\n\n`);
      const c = { attempt: attemptId, res };
      markClients.add(c);
      const ping = setInterval(() => res.write(': ping\n\n'), 25000);
      req.on('close', () => { clearInterval(ping); markClients.delete(c); });
      return;
    }
    if (p === '/api/check') {   // live marking: the key for ONE question, fetched only after the student locks their answer
      const e = readExam(url.searchParams.get('folder') || '');
      const part = e.questions.flatMap(q => q.parts).find(x => x.part_id === url.searchParams.get('part'));
      if (!part) return send(res, 404, { error: 'no such question' });
      const s = part.question || {};
      return send(res, 200, {
        type: part.answer_type,
        correct_letters: s.correct_letters || null,
        rows: s.rows ? s.rows.map(r => ({ correct: r.correct })) : null,
        explanation: part.explanation || null,
        criteria: part.marking_criteria || null, rubric: part.marking_rubric || null,
        guidance: part.marking_guidance || null, sample_answer: part.sample_answer || null,
      });
    }
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
