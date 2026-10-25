// Turns the raw Gradeo API dumps in gradeo_out/raw/ into one folder per exam:
//   exam.json   - normalised: questions, options, your answers, marks, feedback, criteria, rubric, sample answers
//   exam.md     - the same, laid out for pasting/uploading into Claude
//   assets/     - every image referenced by questions, stimuli, sample answers and your uploads
//   drawings/   - your Excalidraw answers rendered to PNG (+ the raw scene JSON)
// plus gradeo_out/all_exams.json and gradeo_out/INDEX.md.
// Run fetch.mjs first (needs Chrome); this step is offline apart from downloading images.
import fs from 'node:fs';
import path from 'node:path';
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';
import { makeRenderer, describeDrawing } from './render_drawings.mjs';

const OUT = 'gradeo_out';
const RAW = path.join(OUT, 'raw');
const EXAMS = path.join(OUT, 'exams');
const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

const safe = s => s.replace(/[^\w\- ()]+/g, '').replace(/\s+/g, '_').slice(0, 70) || 'exam';
const cleanMd = s => (s || '').replace(/ /g, ' ').replace(/\n{3,}/g, '\n\n').trim() || null;
const plain = html => cleanMd((html || '').replace(/<br\s*\/?>/gi, '\n').replace(/<\/p>/gi, '\n').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'"));

// Gradeo stores some UTF-8 filenames double-encoded ("10.50.36â\u0080¯am"); undo that when it round-trips cleanly.
const fixMojibake = s => { const t = Buffer.from(s, 'latin1').toString('utf8'); return /[\u0080-\u00ff]/.test(s) && !t.includes('\ufffd') ? t : s; };

// ---------- assets ----------
// Every exam keeps its own assets/ folder so each exam folder is self-contained.
const assetCache = new Map(); // url -> {buf, ext}
export let ASSET_BASE = null;   // set by importers whose content uses site-relative image paths
export const setAssetBase = b => { ASSET_BASE = b; };
async function download(url) {
  if (assetCache.has(url)) return assetCache.get(url);
  const r = await fetch(url.startsWith('/') && ASSET_BASE ? ASSET_BASE + url : url);
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  const ct = r.headers.get('content-type') || '';
  const ext = { 'image/png': '.png', 'image/jpeg': '.jpg', 'image/gif': '.gif', 'image/svg+xml': '.svg', 'image/webp': '.webp', 'application/pdf': '.pdf', 'video/mp4': '.mp4', 'video/webm': '.webm', 'video/quicktime': '.mov' }[ct.split(';')[0]] || '';
  const buf = Buffer.from(await r.arrayBuffer());
  // Gradeo sometimes labels videos as image/jpeg; trust the file's own signature instead.
  const sig = buf.subarray(4, 8).toString('latin1');
  const v = { buf, ext: sig === 'ftyp' ? (buf.subarray(8, 10).toString('latin1') === 'qt' ? '.mov' : '.mp4') : ext };
  assetCache.set(url, v);
  return v;
}

function makeExamContext(dir) {
  const pending = new Map(); // url -> relative path promise
  const asset = url => {
    if (!pending.has(url)) pending.set(url, (async () => {
      try {
        const { buf, ext } = await download(url);
        const rel = `assets/${url.split('/').pop()}${ext}`;
        fs.mkdirSync(path.join(dir, 'assets'), { recursive: true });
        fs.writeFileSync(path.join(dir, rel), buf);
        return rel;
      } catch (e) { console.warn('   ! image download failed', url, e.message); return url; }
    })());
    return pending.get(url);
  };
  const td = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced', bulletListMarker: '-' });
  td.use(gfm);
  // Gradeo tables usually have no <th> row, which the gfm plugin leaves as raw HTML - build them ourselves.
  td.addRule('anyTable', {
    filter: 'table',
    replacement: (_, node) => {
      const kids = (n, tags) => { const o = []; (function walk(x) { for (const c of [...x.childNodes]) { if (tags.includes(c.nodeName)) o.push(c); else if (c.nodeType === 1 && c.nodeName !== 'TABLE') walk(c); } })(n); return o; };
      const rows = kids(node, ['TR']).map(tr => kids(tr, ['TD', 'TH'])
        .map(c => td.turndown(c.innerHTML).replace(/\n+/g, ' ').replace(/\|/g, '\\|').trim()));
      if (!rows.length) return '';
      const w = Math.max(...rows.map(r => r.length));
      const line = r => '| ' + Array.from({ length: w }, (_, i) => r[i] ?? '').join(' | ') + ' |';
      return '\n\n' + [line(rows[0]), '|' + Array(w).fill('---').join('|') + '|', ...rows.slice(1).map(line)].join('\n') + '\n\n';
    },
  });
  // HTML -> markdown, with <img> pointed at the downloaded local copy.
  const md = async html => {
    if (!html) return { md: null, images: [] };
    // Videos: replace the <video> element with a link to the downloaded file.
    for (const m of [...html.matchAll(/<video[\s\S]*?<\/video>/gi)]) {
      const src = (m[0].match(/src="(https?:[^"]+)"/i) || [])[1];
      html = html.replace(m[0], src ? `<p><a href="${await asset(src)}">▶ VIDEO (open this file)</a></p>` : '<p>(video missing)</p>');
    }
    const urls = [...html.matchAll(/<img[^>]+src="([^"]+)"/gi)].map(m => m[1]).filter(u => /^https?:/.test(u) || (ASSET_BASE && u.startsWith("/")));
    const map = {};
    for (const u of urls) map[u] = await asset(u);
    let h = html;
    for (const [u, rel] of Object.entries(map)) h = h.split(u).join(rel);
    return { md: cleanMd(td.turndown(h)), images: Object.values(map) };
  };
  return { asset, md };
}

// A Gradeo content item collection (prompt / stimulus) -> markdown + images.
async function contentCollection(coll, X) {
  if (!coll?.items?.length) return { md: null, images: [] };
  const byId = Object.fromEntries(coll.items.map(i => [i.id, i]));
  const order = coll.itemIdOrder?.length ? coll.itemIdOrder.map(id => byId[id]).filter(Boolean) : coll.items;
  const mds = [], images = [];
  for (const it of order) {
    const r = await contentItem(it, X);
    if (r.md) mds.push(r.md);
    images.push(...r.images);
  }
  return { md: mds.join('\n\n') || null, images };
}

async function contentItem(it, X) {
  if (!it) return { md: null, images: [] };
  const images = [];
  let md = null;
  if (it.text) { const r = await X.md(it.text); md = r.md; images.push(...r.images); }
  if (it.type === 'MARKING_CRITERIA') md = (it.criteria || []).map(c => `- [${plain(c.point)} marks] ${plain(c.criterion)}`).join('\n');
  const files = it.files || [];
  const fileOrder = it.fileIdOrder?.length ? it.fileIdOrder.map(id => files.find(f => f.id === id)).filter(Boolean) : files;
  for (const f of fileOrder) {
    const u = f.url || f.file?.url;
    if (u) { const rel = await X.asset(u); images.push(rel); md = (md ? md + '\n\n' : '') + `![image](${rel})`; }
  }
  if (!md && !images.length && it.type !== 'RICH_TEXT') md = `[unsupported content type ${it.type}]`;
  return { md, images };
}

// "Big Data (Q9, SA, Topic Test)" -> parts
function parseTitle(t) {
  const m = (t || '').match(/^(.*?)\s*\((.*)\)\s*$/);
  if (!m) return { topic: t, label: null, kind: null, source: null };
  const p = m[2].split(',').map(s => s.trim());
  return { topic: m[1].trim(), label: p[0] || null, kind: p[1] || null, source: p.slice(2).join(', ') || null };
}

// ---------- one question part ----------
async function buildPart(part, agg, X, ctx) {
  const prm = part.answer?.parameters || {};
  const type = prm.type || null;
  const sheet = agg?.examAnswerSheetItem || null;
  const input = sheet?.answerInput || null;
  const prompt = await contentCollection(part.content?.contentItemCollection, X);

  const out = {
    part_id: part.id,
    part: part.title,
    marks_available: part.metadata?.mark ?? null,
    syllabus: part.metadata?.syllabus?.title || null,
    answer_type: type,
    prompt: prompt.md,
    prompt_images: prompt.images,
  };

  const spec = {}, resp = { answered: !!(input || sheet?.files?.length) };

  if (type === 'MULTI_CHOICE') {
    const chosen = new Set(input?.options || []);
    const correct = new Set(prm.correctOptions || []);
    spec.options = [];
    for (const [i, o] of [...(prm.options || [])].sort((a, b) => a.displayIndex - b.displayIndex).entries()) {
      const img = o.image?.url ? await X.asset(o.image.url) : null;
      spec.options.push({ letter: LETTERS[i], text: plain(o.text) ?? o.equation ?? null, image: img, correct: correct.has(o.id), chosen_by_you: chosen.has(o.id) });
    }
    spec.correct_letters = spec.options.filter(o => o.correct).map(o => o.letter);
    resp.chosen_letters = spec.options.filter(o => o.chosen_by_you).map(o => o.letter);
    if (input) resp.correct = resp.chosen_letters.join() === spec.correct_letters.join();
  } else if (type === 'OBJECTIVE_RESPONSE') {
    const cols = (prm.header || []).map(h => plain(h.text));
    const chosen = new Set(input?.cellIds || []), correct = new Set(prm.correctCellIds || []);
    spec.columns = cols.slice(1);
    spec.rows = (prm.rows || []).map(r => {
      const [label, ...cells] = r.cells;
      const pick = set => cells.map((c, i) => set.has(c.id) ? cols[i + 1] : null).filter(Boolean);
      return { statement: plain(label?.text), correct: pick(correct), yours: pick(chosen) };
    });
    spec.rows.forEach(r => { r.right = input ? r.correct.join() === r.yours.join() : null; });
    resp.rows = spec.rows.map(r => ({ statement: r.statement, yours: r.yours, right: r.right }));
  } else if (type === 'SHORT') {
    const s = prm.settings || {};
    if (s.wordLimit) spec.word_limit = s.wordCount;
    if ((prm.correctValues || []).some(v => v)) spec.accepted_answers = prm.correctValues.filter(Boolean);
    if (input?.value) { const r = await X.md(input.value); resp.text = r.md; resp.images = r.images; resp.word_count = (plain(input.value) || '').split(/\s+/).filter(Boolean).length; }
  } else if (type === 'CODING') {
    spec.language = prm.language;
    spec.starter_code = prm.defaultCode || null;
    if (input) resp.code = input.code ?? null;
  } else if (type === 'SQL') {
    spec.dataset_setup_sql = prm.datasetSetupQuery || null;
    spec.starter_query = prm.defaultAnswerQuery || null;
    if (input) resp.sql = input.value ?? null;
  } else if (type === 'RICH_TABLE') {
    const vals = Object.fromEntries((input?.values || []).map(v => [v.cellId, v.value]));
    spec.table = (prm.rows || []).map(row => row.map(c => {
      if (c.type === 'TEXT') return { type: 'text', text: plain(c.text) };
      if (c.type === 'DROPDOWN') {
        const opts = c.dropdown?.options || [];
        const v = vals[c.id];
        return { type: 'dropdown', options: opts.map(o => o.text), correct: opts.filter(o => c.dropdown.correctOptionIds?.includes(o.id)).map(o => o.text),
                 yours: v ? (opts.find(o => o.id === v)?.text ?? plain(v)) : null };
      }
      return { type: 'input', expected: c.inputText || null, yours: vals[c.id] != null ? plain(vals[c.id]) : null };
    }));
    resp.filled_cells = Object.keys(vals).length;
  } else if (type === 'DRAWING_V2') {
    const bg = [];
    for (const f of part.answer?.files || []) if (f.file?.url) bg.push(await X.asset(f.file.url));
    if (bg.length) spec.background_images = bg;
    const data = input?.data;
    if (data?.elements?.some(e => !e.isDeleted)) {
      const base = `drawings/${ctx.qid}_${safe(part.title || 'part')}`;
      fs.mkdirSync(path.join(ctx.dir, 'drawings'), { recursive: true });
      fs.writeFileSync(path.join(ctx.dir, base + '.excalidraw.json'), JSON.stringify({ type: 'excalidraw', version: 2, source: 'gradeo', elements: data.elements, appState: {}, files: data.files || {} }));
      try {
        const png = await ctx.renderer.render(data);
        if (png) { fs.writeFileSync(path.join(ctx.dir, base + '.png'), png); resp.drawing_png = base + '.png'; }
      } catch (e) { console.warn('   ! drawing render failed', e.message.split('\n')[0]); }
      resp.drawing_scene = base + '.excalidraw.json';
      resp.drawing_text = describeDrawing(data);
    } else if (input) resp.drawing_empty = true;
  } else if (type) {
    spec.raw_parameters = prm;
    if (input) resp.raw_input = input;
  }

  // Uploaded files (photos of working, screenshots...)
  if (sheet?.files?.length) {
    resp.uploaded_files = [];
    for (const f of sheet.files) resp.uploaded_files.push({ name: f.fileOriginalName ? fixMojibake(f.fileOriginalName) : null, path: await X.asset(f.url) });
  }
  if (!sheet || (!input && !sheet.files?.length)) resp.answered = false;

  out.question = spec;
  out.your_response = resp;

  // Marking
  const items = agg?.markingSessionMarkingItemList || [];
  out.result = {
    mark: agg?.mark ?? null,
    available: out.marks_available,
    not_submitted: items.some(m => m.answerNotSubmitted) || !resp.answered,
    automarked: items.length ? items.every(m => m.isAutomarked) : null,
    feedback: items
      .filter(m => (m.feedbackText || '').trim() || m.markerId)
      .map(m => ({
        marker: [m.markerFirstName, m.markerLastName].filter(Boolean).join(' ') || ctx.markers[m.markerId] || (m.isAutomarked ? 'auto' : null),
        mark: m.mark, feedback: (m.feedbackText || '').trim() || null, marked: m.markedDate,
      })),
  };
  out.result.feedback = out.result.feedback.filter(f => f.feedback || f.mark != null);

  // Marking guide
  const crit = part.markingCriteriaContentItem;
  out.marking_criteria = crit?.criteria?.length ? crit.criteria.map(c => ({ marks: plain(c.point), criterion: plain(c.criterion) })) : null;
  for (const [k, key] of [['marking_rubric', 'markingRubricContentItem'], ['marking_guidance', 'markingGuidanceContentItem'], ['sample_answer', 'sampleAnswerContentItem']]) {
    const it = part[key];
    if (!it) { out[k] = null; continue; }
    const r = it.type === 'MARKING_CRITERIA'
      ? { md: (it.criteria || []).map(c => `- [${plain(c.point)} marks] ${plain(c.criterion)}`).join('\n'), images: [] }
      : await contentItem(it, X);
    out[k] = r.md;
    if (r.images.length) out[k + '_images'] = r.images;
  }
  return out;
}

// ---------- markdown rendering ----------
const fence = (s, lang = '') => '```' + lang + '\n' + (s || '').replace(/\n+$/, '') + '\n```';
function partMd(p) {
  const L = [];
  L.push(`#### ${p.part || 'Part'} — ${p.result.mark ?? '–'}/${p.marks_available ?? '?'} marks  \`${p.answer_type}\``);
  if (p.prompt) L.push(p.prompt);
  const q = p.question, r = p.your_response;
  if (p.answer_type === 'MULTI_CHOICE') {
    L.push(q.options.map(o => `- **${o.letter}.** ${o.text ?? ''}${o.image ? ` ![](${o.image})` : ''}${o.correct ? '  ✅ *correct*' : ''}${o.chosen_by_you ? '  ⬅️ **your choice**' : ''}`).join('\n'));
    L.push(`**Your answer:** ${r.chosen_letters?.join(', ') || '(none)'} · **Correct:** ${q.correct_letters.join(', ')}${r.correct === true ? ' ✔' : r.correct === false ? ' ✘' : ''}`);
  } else if (p.answer_type === 'OBJECTIVE_RESPONSE') {
    L.push(`| Statement | Correct | Yours | |\n|---|---|---|---|\n` + q.rows.map(x => `| ${x.statement} | ${x.correct.join(', ')} | ${x.yours.join(', ') || '–'} | ${x.right ? '✔' : x.right === false ? '✘' : ''} |`).join('\n'));
  } else if (p.answer_type === 'RICH_TABLE') {
    const cell = c => c.type === 'text' ? (c.text || '') : c.type === 'dropdown'
      ? `**you:** ${c.yours ?? '–'} (correct: ${c.correct.join('/')})` : `**you:** ${c.yours ?? '–'}${c.expected ? ` (expected: ${c.expected})` : ''}`;
    const rows = q.table.map(row => '| ' + row.map(c => cell(c).replace(/\|/g, '\\|').replace(/\n/g, ' ')).join(' | ') + ' |');
    L.push([rows[0], '|' + q.table[0].map(() => '---').join('|') + '|', ...rows.slice(1)].join('\n'));
  } else {
    if (q.word_limit) L.push(`*Word limit: ${q.word_limit}*`);
    if (q.background_images) L.push('Drawing background provided:\n' + q.background_images.map(i => `![background](${i})`).join('\n'));
    if (q.language && q.starter_code) L.push(`Starter code (${q.language}):\n` + fence(q.starter_code));
    if (q.dataset_setup_sql) L.push('Dataset:\n' + fence(q.dataset_setup_sql, 'sql'));
    L.push('**Your answer:**');
    if (!r.answered) L.push('_(not answered)_');
    if (r.text) L.push(r.text.split('\n').map(l => '> ' + l).join('\n') + (r.word_count ? `\n\n*(${r.word_count} words)*` : ''));
    if (r.code != null) L.push(fence(r.code, (q.language || '').toLowerCase()));
    if (r.sql != null) L.push(fence(r.sql, 'sql'));
    if (r.drawing_png) L.push(`![your drawing](${r.drawing_png})`);
    if (r.drawing_text) {
      const d = r.drawing_text;
      L.push('Drawing contents (extracted): labels: ' + d.texts.map(t => JSON.stringify(t.text)).join(', ') +
        (d.connectors.length ? '\n\nConnectors: ' + d.connectors.map(c => `${c.type} ${JSON.stringify(c.from ?? '?')} → ${JSON.stringify(c.to ?? '?')}${c.label ? ` [${c.label}]` : ''}`).join('; ') : ''));
    }
    if (r.drawing_empty) L.push('_(empty drawing)_');
  }
  if (r.uploaded_files) L.push('Uploaded: ' + r.uploaded_files.map(f => `![${f.name || 'upload'}](${f.path})`).join(' '));
  for (const f of p.result.feedback) if (f.feedback) L.push(`**Feedback (${f.marker || 'marker'}${f.mark != null ? `, ${f.mark} marks` : ''}):** ${f.feedback}`);
  if (p.marking_criteria) L.push('**Marking criteria:**\n' + p.marking_criteria.map(c => `- [${c.marks}] ${c.criterion}`).join('\n'));
  if (p.marking_rubric) L.push('**Marking rubric:**\n\n' + p.marking_rubric);
  if (p.marking_guidance) L.push('**Marking guidance:**\n\n' + p.marking_guidance);
  if (p.sample_answer) L.push('**Sample answer:**\n\n' + p.sample_answer);
  return L.join('\n\n');
}

function examMd(e) {
  const head = [`# ${e.exam}`, '',
    `- Syllabus: ${e.syllabus} · Publisher: ${e.publisher || '–'}`,
    `- Status: ${e.status}${e.results_released ? ' · results released' : ''}${e.submitted ? ` · submitted ${e.submitted.slice(0, 10)}` : ''}`,
    `- **Score: ${e.total_mark ?? '–'} / ${e.total_available}**${e.total_mark != null ? ` (${Math.round(100 * e.total_mark / e.total_available)}%)` : ''} · answered ${e.parts_answered}/${e.parts_total} parts · marked ${e.parts_marked}/${e.parts_total}`,
    `- Review page: ${e.review_url}`];
  const L = [head.join('\n')];
  for (const q of e.questions) {
    L.push(`---\n\n## ${q.number}. ${q.title}`);
    if (q.copyright) L.push(`*Source: ${q.copyright}*`);
    if (q.stimulus) L.push('**Stimulus:**\n\n' + q.stimulus);
    for (const p of q.parts) L.push(partMd(p));
  }
  return L.join('\n\n') + '\n';
}

// ---------- main ----------
export { buildPart, contentCollection, makeExamContext, parseTitle, examMd };
if (import.meta.url === `file://${process.argv[1]}`) await main();

async function main() {
const sessions = JSON.parse(fs.readFileSync(path.join(RAW, '_sessions.json'), 'utf8'));
const only = process.argv[2] ? new RegExp(process.argv[2], 'i') : null;
if (!only) fs.rmSync(EXAMS, { recursive: true, force: true });
fs.mkdirSync(EXAMS, { recursive: true });
const renderer = await makeRenderer();
const all = [], index = [];

for (const s of sessions) {
  const title = s.summary.title;
  const msid = s.markingSessionId;
  const rawFile = msid && path.join(RAW, `${msid}.json`);
  const raw = rawFile && fs.existsSync(rawFile) ? JSON.parse(fs.readFileSync(rawFile, 'utf8')) : null;
  const hdr = s.userAnswerSheetHeader;
  const row = { title, status: s.status, submitted: hdr?.submitDate || null, results_released: !!(raw?.answers), msid };
  if (only && !only.test(title)) continue;
  if (!raw?.questions?.length) { index.push({ ...row, note: 'locked: Gradeo returns 403 until results are released' }); continue; }

  const date = (hdr?.submitDate || hdr?.startDate || '').slice(0, 10) || 'not-sat';
  const dir = path.join(EXAMS, `${date}_${safe(title)}_${msid.slice(0, 8)}`);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
  const X = makeExamContext(dir);
  const aggByPart = Object.fromEntries((raw.answers || []).map(a => [a.partId, a]));
  const markers = Object.fromEntries((raw.state?.markerUserList || []).map(m => [m.id, `${m.firstName} ${m.lastName}`]));

  const questions = [];
  for (const [qi, q] of raw.questions.entries()) {
    const qid = `q${String(qi + 1).padStart(2, '0')}`;
    const stim = await contentCollection(q.stimulusContentItemCollection, X);
    const parts = [];
    for (const p of [...q.parts].sort((a, b) => a.displayIndex - b.displayIndex))
      parts.push(await buildPart(p, aggByPart[p.id], X, { dir, qid, renderer, markers }));
    questions.push({ number: qi + 1, question_id: q.id, title: q.title, ...parseTitle(q.title), copyright: q.copyrightText || null,
      stimulus: stim.md, stimulus_images: stim.images, parts });
  }

  const allParts = questions.flatMap(q => q.parts);
  const sum = k => allParts.reduce((a, p) => a + (p[k] ?? 0), 0);
  const exam = {
    exam: title,
    syllabus: s.summary.syllabusTitle,
    publisher: s.summary.publisher?.name || null,
    topics: (s.summary.topicLabels || []).map(t => t.text),
    outcomes: (s.summary.outcomeLabels || []).map(t => t.text),
    status: s.status,
    results_released: !!raw.answers,
    submitted: hdr?.submitDate || null,
    started: hdr?.startDate || null,
    duration_minutes: s.summary.durationSeconds ? s.summary.durationSeconds / 60 : null,
    markers: Object.values(markers),
    review_url: `https://platform.gradeo.com.au/reviewExam/${msid}`,
    marking_session_id: msid, exam_id: s.summary.id, session_id: s.session.id,
    total_mark: allParts.some(p => p.result.mark != null) ? allParts.reduce((a, p) => a + (p.result.mark ?? 0), 0) : null,
    parts_answered: allParts.filter(p => p.your_response.answered).length,
    parts_marked: allParts.filter(p => p.result.mark != null).length,
    parts_total: allParts.length,
    total_available: sum('marks_available'),
    questions,
  };
  // per-topic breakdown, handy for spotting weak areas
  const byTopic = {};
  for (const q of questions) for (const p of q.parts) {
    const t = (byTopic[q.topic] ||= { mark: 0, available: 0 });
    t.mark += p.result.mark ?? 0; t.available += p.marks_available ?? 0;
  }
  exam.by_topic = byTopic;

  fs.writeFileSync(path.join(dir, 'exam.json'), JSON.stringify(exam, null, 2));
  fs.writeFileSync(path.join(dir, 'exam.md'), examMd(exam));
  all.push({ folder: path.relative(OUT, dir), ...exam });
  const answered = allParts.filter(p => p.your_response.answered).length;
  index.push({ ...row, folder: path.relative(OUT, dir), mark: exam.total_mark, available: exam.total_available, answered, marked: exam.parts_marked, parts: allParts.length });
  console.log(`✓ ${title}  ${exam.total_mark ?? '–'}/${exam.total_available}  (${answered}/${allParts.length} answered) -> ${dir}`);
}
await renderer.close();

if (!only) {
  fs.writeFileSync(path.join(OUT, 'all_exams.json'), JSON.stringify({ exported_at: new Date().toISOString(), exams: all }, null, 2));
  const L = ['# Gradeo export', '', `Exported ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC. Each folder has exam.md (read this), exam.json, assets/ and drawings/.`];
  const link = r => `[${path.basename(r.folder)}](${encodeURI(r.folder)}/exam.md)`;
  const sat = index.filter(r => r.folder && r.answered), unsat = index.filter(r => r.folder && !r.answered), locked = index.filter(r => !r.folder);
  L.push('', '## Exams you sat', '', '| Exam | Submitted | Score | Answered | Marked | Folder |', '|---|---|---|---|---|---|');
  for (const r of sat) L.push(`| ${r.title} | ${(r.submitted || r.status).slice(0, 10)} | ${r.mark != null ? `${r.mark}/${r.available} (${Math.round(100 * r.mark / r.available)}%)` : `–/${r.available}`} | ${r.answered}/${r.parts} | ${r.marked}/${r.parts} | ${link(r)} |`);
  L.push('', '## Papers not attempted (questions, criteria and sample answers only)', '', '| Exam | Marks | Parts | Folder |', '|---|---|---|---|');
  for (const r of unsat) L.push(`| ${r.title} | ${r.available} | ${r.parts} | ${link(r)} |`);
  L.push('', '## Locked (Gradeo returns 403 until your teacher releases results; re-run later)', '', '| Exam | Status | Submitted |', '|---|---|---|');
  for (const r of locked) L.push(`| ${r.title} | ${r.status} | ${(r.submitted || '').slice(0, 10)} |`);
  fs.writeFileSync(path.join(OUT, 'INDEX.md'), L.join('\n') + '\n');
}
console.log(`Done: ${all.length} exams built.`);
}
