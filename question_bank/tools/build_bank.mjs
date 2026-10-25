// Builds question_bank/bank.json + coverage.md from:
//   (a) gradeo_out/exams/*/exam.json (already exported papers; assets copied)
//   (b) question_bank/raw/quizq_*.json (Gradeo quizzes generated for this bank; assets downloaded)
//   (c) question_bank/tools/nesa_entries.json (hand-built from the NESA online papers + official marking guidelines)
// then applies question_bank/tools/overrides.json (manual syllabus / quality / issues review).
// Run from anywhere: node question_bank/tools/build_bank.mjs
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import TurndownService from '/Users/fred/gradeo/node_modules/turndown/lib/turndown.cjs.js';
import { gfm } from '/Users/fred/gradeo/node_modules/turndown-plugin-gfm/lib/turndown-plugin-gfm.cjs.js';

const ROOT = '/Users/fred/gradeo';
const QB = path.join(ROOT, 'question_bank');
const ASSETS = path.join(QB, 'assets');
const RAW = path.join(QB, 'raw');
const TOOLS = path.join(QB, 'tools');
fs.mkdirSync(ASSETS, { recursive: true });
const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const POINTS = JSON.parse(fs.readFileSync(path.join(ROOT, 'study/syllabus_points.json'), 'utf8'));
const POINT_IDS = new Set(POINTS.map(p => p.id));

const cleanMd = s => (s || '').replace(/ /g, ' ').replace(/\n{3,}/g, '\n\n').trim() || null;
const plain = html => cleanMd((html || '').replace(/<br\s*\/?>/gi, '\n').replace(/<\/p>/gi, '\n').replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'"));

// ---------- assets ----------
const dlCache = new Map();
async function download(url) {
  if (dlCache.has(url)) return dlCache.get(url);
  const p = (async () => {
    const base = url.split('/').pop().split('?')[0];
    const existing = fs.readdirSync(ASSETS).find(f => f.startsWith(base + '.') || f === base);
    if (existing) return 'assets/' + existing;
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error(r.status);
      const ct = (r.headers.get('content-type') || '').split(';')[0];
      let ext = { 'image/png': '.png', 'image/jpeg': '.jpg', 'image/gif': '.gif', 'image/svg+xml': '.svg', 'image/webp': '.webp', 'application/pdf': '.pdf', 'video/mp4': '.mp4' }[ct] || '';
      const buf = Buffer.from(await r.arrayBuffer());
      if (buf.subarray(4, 8).toString('latin1') === 'ftyp') ext = '.mp4';
      fs.writeFileSync(path.join(ASSETS, base + ext), buf);
      return 'assets/' + base + ext;
    } catch (e) { console.warn('  ! asset failed', url, e.message); return url; }
  })();
  dlCache.set(url, p);
  return p;
}
const td = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced', bulletListMarker: '-' });
td.use(gfm);
td.addRule('anyTable', {
  filter: 'table',
  replacement: (_, node) => {
    const kids = (n, tags) => { const o = []; (function walk(x) { for (const c of [...x.childNodes]) { if (tags.includes(c.nodeName)) o.push(c); else if (c.nodeType === 1 && c.nodeName !== 'TABLE') walk(c); } })(n); return o; };
    const rows = kids(node, ['TR']).map(tr => kids(tr, ['TD', 'TH']).map(c => td.turndown(c.innerHTML).replace(/\n+/g, ' ').replace(/\|/g, '\\|').trim()));
    if (!rows.length) return '';
    const w = Math.max(...rows.map(r => r.length));
    const line = r => '| ' + Array.from({ length: w }, (_, i) => r[i] ?? '').join(' | ') + ' |';
    return '\n\n' + [line(rows[0]), '|' + Array(w).fill('---').join('|') + '|', ...rows.slice(1).map(line)].join('\n') + '\n\n';
  },
});
async function md(html) {
  if (!html) return { md: null, images: [] };
  for (const m of [...html.matchAll(/<video[\s\S]*?<\/video>/gi)]) {
    const src = (m[0].match(/src="(https?:[^"]+)"/i) || [])[1];
    html = html.replace(m[0], src ? `<p><a href="${await download(src)}">VIDEO</a></p>` : '<p>(video missing)</p>');
  }
  const urls = [...html.matchAll(/<img[^>]+src="([^"]+)"/gi)].map(m => m[1]).filter(u => /^https?:/.test(u));
  const images = [];
  for (const u of urls) { const rel = await download(u); html = html.split(u).join(rel); images.push(rel); }
  return { md: cleanMd(td.turndown(html)), images };
}
async function contentItem(it) {
  if (!it) return { md: null, images: [] };
  const images = []; let m = null;
  if (it.text) { const r = await md(it.text); m = r.md; images.push(...r.images); }
  if (it.type === 'MARKING_CRITERIA') m = (it.criteria || []).map(c => `- [${plain(c.point)} marks] ${plain(c.criterion)}`).join('\n');
  const files = it.files || [];
  const order = it.fileIdOrder?.length ? it.fileIdOrder.map(id => files.find(f => f.id === id)).filter(Boolean) : files;
  for (const f of order) { const u = f.url || f.file?.url; if (u) { const rel = await download(u); images.push(rel); m = (m ? m + '\n\n' : '') + `![image](${rel})`; } }
  return { md: m, images };
}
async function collection(coll) {
  if (!coll?.items?.length) return { md: null, images: [] };
  const byId = Object.fromEntries(coll.items.map(i => [i.id, i]));
  const order = coll.itemIdOrder?.length ? coll.itemIdOrder.map(id => byId[id]).filter(Boolean) : coll.items;
  const mds = [], images = [];
  for (const it of order) { const r = await contentItem(it); if (r.md) mds.push(r.md); images.push(...r.images); }
  return { md: mds.join('\n\n') || null, images };
}
function parseTitle(t) {
  const m = (t || '').match(/^(.*?)\s*\((.*)\)\s*$/);
  if (!m) return { topic: t, label: null, paper: null };
  const p = m[2].split(',').map(s => s.trim());
  return { topic: m[1].trim(), label: p[0] || null, paper: p.slice(1).join(', ') || null };
}

// ---------- Gradeo item -> syllabus point map ----------
const gsyl = JSON.parse(fs.readFileSync(path.join(RAW, 'syllabus_gradeo.json'), 'utf8'));
const words = s => new Set(s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(w => w.length > 3));
const itemToPoint = {};
for (const t of gsyl.topics) for (const st of t.subtopics) for (const it of st.items) {
  const w = words(it.text); let best = null, bs = -1;
  for (const p of POINTS) {
    const pw = words(p.text + ' ' + p.subs.join(' '));
    const s = [...w].filter(x => pw.has(x)).length / Math.sqrt(w.size * pw.size || 1);
    if (s > bs) { bs = s; best = p.id; }
  }
  itemToPoint[it.id] = { point: best, score: +bs.toFixed(2), text: it.text.slice(0, 90) };
}
fs.writeFileSync(path.join(TOOLS, 'gradeo_item_map.json'), JSON.stringify(itemToPoint, null, 1));
const manualItemMap = fs.existsSync(path.join(TOOLS, 'gradeo_item_map_fix.json')) ? JSON.parse(fs.readFileSync(path.join(TOOLS, 'gradeo_item_map_fix.json'), 'utf8')) : {};
const mapItems = ids => [...new Set((ids || []).map(i => manualItemMap[i] || itemToPoint[i]?.point).filter(Boolean))];

// ---------- part -> bank entry ----------
function partSpec(prm, part) {
  const type = prm.type || null;
  const out = {};
  if (type === 'MULTI_CHOICE') {
    const correct = new Set(prm.correctOptions || []);
    out.options = [...(prm.options || [])].sort((a, b) => a.displayIndex - b.displayIndex).map((o, i) => ({ letter: LETTERS[i], text: plain(o.text) ?? o.equation ?? null, image: o.image?.url || null, correct: correct.has(o.id) }));
  } else if (type === 'OBJECTIVE_RESPONSE') {
    const cols = (prm.header || []).map(h => plain(h.text));
    const correct = new Set(prm.correctCellIds || []);
    out.objective = { columns: cols.slice(1), rows: (prm.rows || []).map(r => { const [label, ...cells] = r.cells; return { statement: plain(label?.text), correct: cells.map((c, i) => correct.has(c.id) ? cols[i + 1] : null).filter(Boolean) }; }) };
  } else if (type === 'RICH_TABLE') {
    out.table = (prm.rows || []).map(row => row.map(c => c.type === 'TEXT' ? { type: 'text', text: plain(c.text) }
      : c.type === 'DROPDOWN' ? { type: 'dropdown', options: (c.dropdown?.options || []).map(o => o.text), correct: (c.dropdown?.options || []).filter(o => c.dropdown.correctOptionIds?.includes(o.id)).map(o => o.text) }
      : { type: 'input', expected: c.inputText || null }));
  } else if (type === 'SHORT') {
    if (prm.settings?.wordLimit) out.word_limit = prm.settings.wordCount;
    if ((prm.correctValues || []).some(v => v)) out.accepted_answers = prm.correctValues.filter(Boolean);
    if (prm.settings?.extendedView || prm.extendedView) out.extended = true;
  } else if (type === 'CODING') { out.language = prm.language; out.starter_code = prm.defaultCode || null; }
  else if (type === 'SQL') { out.dataset_setup_sql = prm.datasetSetupQuery || null; out.starter_query = prm.defaultAnswerQuery || null; }
  else if (type === 'SORTING_TABLE') out.sorting = prm;
  return out;
}

const entries = [];
// (a) existing export
const rawPartMeta = {};
for (const f of fs.readdirSync(path.join(ROOT, 'gradeo_out/raw')).filter(f => /^[0-9a-f-]{36}\.json$/.test(f))) {
  const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'gradeo_out/raw', f), 'utf8'));
  for (const q of d.questions || []) for (const p of q.parts) rawPartMeta[p.id] = { meta: p.metadata, publisher: q.publisher?.name || null, syllabusId: p.metadata?.syllabus?.id };
}
const copyAsset = (dir, rel) => {
  if (!rel || /^https?:/.test(rel)) return rel;
  const src = path.join(dir, rel), base = path.basename(rel);
  if (fs.existsSync(src) && !fs.existsSync(path.join(ASSETS, base))) fs.copyFileSync(src, path.join(ASSETS, base));
  return 'assets/' + base;
};
const fixPaths = (dir, s) => s ? s.replace(/\]\((assets\/[^)\s]+)\)/g, (_, r) => `](${copyAsset(dir, r)})`).replace(/href="(assets\/[^"]+)"/g, (_, r) => `href="${copyAsset(dir, r)}"`) : s;
for (const ex of fs.readdirSync(path.join(ROOT, 'gradeo_out/exams'))) {
  const dir = path.join(ROOT, 'gradeo_out/exams', ex);
  const e = JSON.parse(fs.readFileSync(path.join(dir, 'exam.json'), 'utf8'));
  for (const q of e.questions) for (const p of q.parts) {
    const rm = rawPartMeta[p.part_id] || {};
    const spec = {};
    if (p.answer_type === 'MULTI_CHOICE') spec.options = p.question.options.map(o => ({ letter: o.letter, text: o.text, image: copyAsset(dir, o.image), correct: o.correct }));
    if (p.answer_type === 'OBJECTIVE_RESPONSE') spec.objective = { columns: p.question.columns, rows: p.question.rows.map(r => ({ statement: r.statement, correct: r.correct })) };
    if (p.answer_type === 'RICH_TABLE') spec.table = p.question.table.map(row => row.map(c => { const { yours, ...rest } = c; return rest; }));
    for (const k of ['word_limit', 'accepted_answers', 'language', 'starter_code', 'dataset_setup_sql', 'starter_query']) if (p.question[k] != null) spec[k] = p.question[k];
    if (p.question.background_images) spec.background_images = p.question.background_images.map(r => copyAsset(dir, r));
    if (p.answer_type === null && p.question.raw_parameters) spec.raw_parameters = p.question.raw_parameters;
    const pt = parseTitle(q.title);
    entries.push({
      id: 'g-' + p.part_id, origin: 'Gradeo', reserved: false,
      source: `${e.exam}${pt.paper ? ` [orig: ${[pt.paper, pt.label].filter(Boolean).join(' ')}]` : ''}`,
      source_paper: pt.paper || null, publisher: rm.publisher || e.publisher || null,
      question_title: q.title, part: p.part, stimulus: fixPaths(dir, q.stimulus), prompt: fixPaths(dir, p.prompt),
      answer_type: p.answer_type, marks: p.marks_available, ...spec,
      criteria: p.marking_criteria, rubric: fixPaths(dir, p.marking_rubric), guidance: fixPaths(dir, p.marking_guidance), sample_answer: fixPaths(dir, p.sample_answer),
      images: [...new Set([...(q.stimulus_images || []), ...(p.prompt_images || []), ...(p.sample_answer_images || []), ...(p.marking_rubric_images || [])].map(r => copyAsset(dir, r)))],
      _gradeoItems: rm.meta?.subtopicItemIds || [], _yr11: rm.syllabusId === '79cc4e36-7dc8-43d3-abdc-d4320853a7c8',
    });
  }
}
console.log('existing parts', entries.length);
// (b) new quizzes
const quizLog = JSON.parse(fs.readFileSync(path.join(RAW, 'quizzes_created.json'), 'utf8'));
for (const ql of quizLog) {
  const d = JSON.parse(fs.readFileSync(path.join(RAW, `quizq_${ql.markingSessionId}.json`), 'utf8'));
  for (const q of d.questions) {
    const stim = await collection(q.stimulusContentItemCollection);
    const pt = parseTitle(q.title);
    for (const part of [...q.parts].sort((a, b) => a.displayIndex - b.displayIndex)) {
      const prm = part.answer?.parameters || {};
      const prompt = await collection(part.content?.contentItemCollection);
      const spec = partSpec(prm, part);
      if (spec.options) for (const o of spec.options) if (o.image) o.image = await download(o.image);
      const crit = part.markingCriteriaContentItem;
      const extra = {};
      for (const [k, key] of [['rubric', 'markingRubricContentItem'], ['guidance', 'markingGuidanceContentItem'], ['sample_answer', 'sampleAnswerContentItem']]) {
        const it = part[key]; if (!it) { extra[k] = null; continue; }
        const r = it.type === 'MARKING_CRITERIA' ? { md: (it.criteria || []).map(c => `- [${plain(c.point)} marks] ${plain(c.criterion)}`).join('\n'), images: [] } : await contentItem(it);
        extra[k] = r.md; extra['_img_' + k] = r.images;
      }
      const bg = [];
      for (const f of part.answer?.files || []) if (f.file?.url) bg.push(await download(f.file.url));
      if (bg.length) spec.background_images = bg;
      entries.push({
        id: 'g-' + part.id, origin: 'Gradeo', reserved: false,
        source: `${ql.title} (generated for bank)${pt.paper ? ` [orig: ${[pt.paper, pt.label].filter(Boolean).join(' ')}]` : ''}`,
        source_paper: pt.paper || null, publisher: q.publisher?.name || null,
        question_title: q.title, part: part.title, stimulus: stim.md, prompt: prompt.md,
        answer_type: prm.type || null, marks: part.metadata?.mark ?? null, ...spec,
        criteria: crit?.criteria?.length ? crit.criteria.map(c => ({ marks: plain(c.point), criterion: plain(c.criterion) })) : null,
        rubric: extra.rubric, guidance: extra.guidance, sample_answer: extra.sample_answer,
        images: [...new Set([...stim.images, ...prompt.images, ...(extra._img_sample_answer || []), ...(extra._img_rubric || []), ...(extra._img_guidance || []), ...bg])],
        _gradeoItems: part.metadata?.subtopicItemIds || [], _yr11: false,
      });
    }
  }
}
console.log('with new quizzes', entries.length);
// (c) NESA
const nesaFile = path.join(TOOLS, 'nesa_entries.json');
if (fs.existsSync(nesaFile)) for (const n of JSON.parse(fs.readFileSync(nesaFile, 'utf8'))) entries.push({ origin: 'NESA', reserved: false, _gradeoItems: [], ...n });
console.log('with NESA', entries.length);
const mttFile = path.join(TOOLS, 'mtt_entries.json');
if (fs.existsSync(mttFile)) for (const n of JSON.parse(fs.readFileSync(mttFile, 'utf8'))) entries.push({ _gradeoItems: [], ...n });
console.log('with MikeTeachesTech', entries.length);

// ---------- dedupe ----------
const norm = s => (s || '').toLowerCase().replace(/!\[[^\]]*\]\([^)]*\)/g, ' ').replace(/\\([_*[\]()#|`-])/g, '$1').replace(/<[^>]+>/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim();
const keyOf = e => crypto.createHash('sha1').update(norm(e.stimulus) + '||' + norm(e.prompt) + '||' + (e.options || []).map(o => norm(o.text)).join('|')).digest('hex');
const score = e => (e.origin === 'NESA' ? 100 : e.origin === 'MikeTeachesTech' ? 50 : 0) + (e.criteria ? 4 : 0) + (e.sample_answer ? 4 : 0) + (e.options?.some(o => o.correct) ? 4 : 0) + (e.guidance ? 1 : 0) + (e.rubric ? 1 : 0) + (e.images.every(i => !/^https?:/.test(i)) ? 1 : 0);
const groups = new Map();
for (const e of entries) { const k = keyOf(e); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(e); }
let bank = [];
for (const [k, g] of groups) {
  g.sort((a, b) => score(b) - score(a));
  const best = { ...g[0] };
  best.also_in = [...new Set(g.slice(1).map(x => x.source))];
  // keep the union of Gradeo item tags
  best._gradeoItems = [...new Set(g.flatMap(x => x._gradeoItems))];
  best._yr11 = g.every(x => x._yr11);
  // conflicting keys between duplicates
  const keys = new Set(g.filter(x => x.options).map(x => x.options.filter(o => o.correct).map(o => norm(o.text)).sort().join('+')));
  best._keyConflict = keys.size > 1;
  best._dupKey = k;
  bank.push(best);
}
console.log('unique', bank.length);

// ---------- automatic syllabus + quality ----------
const KW = JSON.parse(fs.readFileSync(path.join(TOOLS, 'keywords.json'), 'utf8'));
const VERBS = /\b(account|analyse|apply|assess|calculate|clarify|classify|compare|construct|contrast|deduce|define|demonstrate|describe|discuss|distinguish|evaluate|examine|explain|extract|identify|interpret|investigate|justify|outline|predict|propose|recommend|summarise|synthesise|design|develop|write|draw|complete|modify|determine|state|name|list|select|match|calculate|create|trace|desk check|rewrite|convert|use)\b/i;
function autoSyllabus(e) {
  const fromG = mapItems(e._gradeoItems);
  const text = (e.stimulus || '') + ' ' + (e.prompt || '') + ' ' + (e.options || []).map(o => o.text).join(' ');
  const t = text.toLowerCase();
  const hits = [];
  for (const [pid, kws] of Object.entries(KW)) { let s = 0; for (const k of kws) if (t.includes(k)) s += k.length > 12 ? 2 : 1; if (s) hits.push([pid, s]); }
  hits.sort((a, b) => b[1] - a[1]);
  return { fromG, kw: hits.slice(0, 3).map(h => h[0]) };
}
function autoQuality(e) {
  const issues = [];
  const prompt = (e.prompt || '');
  if (e.answer_type === 'MULTI_CHOICE') {
    const nc = (e.options || []).filter(o => o.correct).length;
    if (nc === 0) issues.push('no option marked correct');
    if (nc > 1) issues.push(`${nc} options marked correct`);
    if ((e.options || []).length < 4) issues.push(`only ${(e.options || []).length} options`);
    const texts = (e.options || []).map(o => norm(o.text));
    if (new Set(texts).size < texts.length) issues.push('duplicate option text');
  } else if (['OBJECTIVE_RESPONSE', 'RICH_TABLE', 'SORTING_TABLE'].includes(e.answer_type)) {
    // auto-marked
  } else if (!e.criteria && !e.sample_answer && !e.accepted_answers && e.origin !== 'NESA') issues.push('no marking criteria or sample answer');
  if (!e.prompt && !e.stimulus) issues.push('empty question text');
  if (e._keyConflict) issues.push('duplicates of this question have different answer keys');
  if (e.images.some(i => /^https?:/.test(i))) issues.push('image could not be downloaded');
  let q = 2;
  const premium = ['CSSA', 'Independent Trials', 'NESA'].includes(e.publisher) || e.origin === 'NESA';
  if (e.answer_type === 'MULTI_CHOICE') q = premium && !issues.length ? 3 : 2;
  else q = premium && (VERBS.test(prompt) || VERBS.test(e.stimulus || '')) && (e.criteria || e.sample_answer) && !issues.length ? 3 : 2;
  if (issues.some(i => /no option|options marked|no marking|empty/.test(i))) q = 1;
  return { q, issues };
}
const overrides = fs.existsSync(path.join(TOOLS, 'overrides.json')) ? JSON.parse(fs.readFileSync(path.join(TOOLS, 'overrides.json'), 'utf8')) : {};
for (const e of bank) {
  const s = autoSyllabus(e);
  e._auto = s;
  let syl = s.fromG.length ? s.fromG.slice(0, 2) : s.kw.slice(0, 1);
  const { q, issues } = autoQuality(e);
  if (e.origin === 'NESA' || e.origin === 'MikeTeachesTech') { syl = e.syllabus; }
  else { e.quality = q; e.issues = issues; }
  e.syllabus = syl;
  if (e._yr11) { e.syllabus = ['Y11']; e.quality = 1; e.issues = [...e.issues, 'Year 11 content']; }
  const o = overrides[e.id] || overrides[e._dupKey];
  if (o) {
    if (o.syllabus) e.syllabus = o.syllabus;
    if (o.quality != null) e.quality = o.quality;
    if (o.issues) e.issues = o.issues === 'clear' ? [] : [...new Set([...e.issues.filter(i => !/^Year 11/.test(i) || e.syllabus[0] === 'Y11'), ...o.issues])];
    if (o.issues_replace) e.issues = o.issues_replace;
    if (o.note) e.review_note = o.note;
    e.reviewed = true;
  }
  for (const id of e.syllabus) if (id !== 'Y11' && id !== 'OUT' && !POINT_IDS.has(id)) console.warn('bad syllabus id', id, e.id);
}

// ---------- write ----------
const ORDER = ['id', 'origin', 'reserved', 'source', 'source_paper', 'publisher', 'also_in', 'question_title', 'part', 'stimulus', 'prompt', 'answer_type', 'marks', 'options', 'objective', 'table', 'sorting', 'word_limit', 'accepted_answers', 'extended', 'language', 'starter_code', 'dataset_setup_sql', 'starter_query', 'background_images', 'raw_parameters', 'criteria', 'rubric', 'guidance', 'sample_answer', 'sample_answer_images', 'key_source', 'key_confidence', 'images', 'syllabus', 'quality', 'issues', 'review_note', 'reviewed'];
const sec = id => id === 'Y11' ? 9998 : id === 'OUT' ? 9999 : ['SSA', 'WEB', 'AUTO', 'PROJ'].indexOf(id.split('-')[0]) * 100 + +id.split('-')[1];
bank.sort((a, b) => (a.reserved - b.reserved) || (sec(a.syllabus[0] || 'Y11') - sec(b.syllabus[0] || 'Y11')) || a.id.localeCompare(b.id));
const clean = bank.map(e => { const o = {}; for (const k of ORDER) if (e[k] !== undefined && !(Array.isArray(e[k]) && !e[k].length && !['issues', 'syllabus', 'images'].includes(k))) o[k] = e[k]; if (!o.issues) o.issues = []; return o; });
fs.writeFileSync(path.join(QB, 'bank.json'), JSON.stringify(clean, null, 1));
fs.writeFileSync(path.join(TOOLS, '_review_view.json'), JSON.stringify(bank.map(e => ({ id: e.id, dup: e._dupKey, src: e.source, pub: e.publisher, type: e.answer_type, marks: e.marks, stim: (e.stimulus || '').slice(0, 1500), prompt: (e.prompt || '').slice(0, 1200), opts: e.options?.map(o => `${o.correct ? '*' : ' '}${o.letter}. ${o.text ?? '[img]'}`), obj: e.objective, table: e.table, crit: e.criteria?.map(c => `[${c.marks}] ${c.criterion}`.slice(0, 300)), sample: (e.sample_answer || '').slice(0, 600), auto: e._auto, syl: e.syllabus, q: e.quality, issues: e.issues, reviewed: !!e.reviewed, reserved: e.reserved })), null, 0));

// coverage
const cov = Object.fromEntries(POINTS.map(p => [p.id, { w: 0, mc: 0, q3: 0, q3w: 0, n: 0 }]));
const isMC = e => ['MULTI_CHOICE', 'OBJECTIVE_RESPONSE', 'RICH_TABLE', 'SORTING_TABLE', 'MULTI_SELECT', 'DROPDOWN', 'SORTING'].includes(e.answer_type);
for (const e of clean) for (const id of e.syllabus) if (cov[id]) {
  const c = cov[id];
  if (e.reserved) { c.res = (c.res || 0) + 1; continue; }
  c.n++; isMC(e) ? c.mc++ : c.w++; if (e.quality === 3) { c.q3++; if (!isMC(e)) c.q3w++; }
}
const yr11 = clean.filter(e => e.syllabus.includes('Y11')).length;
const outN = clean.filter(e => e.syllabus.includes('OUT')).length;
const rows = POINTS.map(p => ({ ...p, ...cov[p.id] })).sort((a, b) => a.q3 - b.q3 || a.n - b.n || sec(a.id) - sec(b.id));
const L = ['# Syllabus coverage of the question bank', '',
  `${clean.length} unique question parts (${clean.filter(e => e.reserved).length} reserved, ${yr11} Year 11-only, ${outN} old-SDD/out-of-syllabus). Each part is tagged with 1–2 syllabus points, so a part can count twice. ` +
  '"Objective" = multiple choice and other auto-marked formats (matching grids, dropdown tables, ordering); "Written" = short answer, extended response, code, SQL and drawing.', '',
  'Sorted by number of quality-3 (HSC-like) parts, fewest first, so gaps are at the top.', '',
  'Counts exclude the 32 RESERVED 2025 HSC parts (shown separately in the last column) and Year 11 / out-of-syllabus parts.', '', '| Point | Content | Written | Objective | Total | Quality 3 (all) | Quality 3 written | Reserved 2025 HSC |', '|---|---|---:|---:|---:|---:|---:|---:|'];
for (const r of rows) L.push(`| ${r.id} | ${r.text.replace(/\|/g, '/').slice(0, 95)}${r.text.length > 95 ? '…' : ''} | ${r.w} | ${r.mc} | ${r.n} | ${r.q3} | ${r.q3w} | ${r.res || 0} |`);
fs.writeFileSync(path.join(QB, '_coverage_rows.json'), JSON.stringify(rows.map(r => ({ id: r.id, text: r.text, w: r.w, mc: r.mc, n: r.n, q3: r.q3, q3w: r.q3w })), null, 1));
const weak = rows.filter(r => r.q3 <= 1 || r.n <= 4);
const noW = rows.filter(r => r.q3w === 0);
L.push('', '## Weakest-covered points', '', 'Points with at most one HSC-like (quality 3) part, or four or fewer parts in total:', '');
for (const r of weak) L.push(`- **${r.id}** ${r.text} — ${r.n} parts (${r.w} written, ${r.mc} objective), ${r.q3} quality 3`);
L.push('', 'Points with no quality-3 written (short-answer/extended/code) question: ' + noW.map(r => r.id).join(', ') + '.');
fs.writeFileSync(path.join(QB, 'coverage.md'), L.join('\n') + '\n');
const tally = (f) => clean.reduce((m, e) => (m[f(e)] = (m[f(e)] || 0) + 1, m), {});
console.log('origin', tally(e => e.origin), 'quality', tally(e => e.quality), 'type', tally(e => e.answer_type));
