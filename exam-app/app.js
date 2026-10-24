// Exam practice app (front end), styled and laid out like NESA's HSC online exam
// (fam.hsconline.nesa.nsw.edu.au). Plain JS, no build step.
const $app = document.getElementById('app');
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const wc = s => (s || '').split(/\s+/).filter(Boolean).length;
const api = async (url, body) => {
  const r = await fetch(url, body ? { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) } : {});
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
};
const slug = s => s.replace(/[^\w]+/g, '_').replace(/^_|_$/g, '').slice(0, 50);
const stamp = () => new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '').replace(/^(\d{8})/, '$1-');
const store = { get: (k, d) => { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } }, set: (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} } };
const NO_SPELL = 'spellcheck="false" autocorrect="off" autocapitalize="off" autocomplete="off"';

let exam = null;      // sanitised exam (structured mode)
let attempt = null;   // saved state
let groups = [];      // one entry per question: { q, idx }
let tick = null;
const ui = { highlighter: null, hl: {}, hidden: {}, navRange: null, wasReading: false };

// ---------- markdown ----------
function mdHtml(text, inline = false) {
  if (!text) return '';
  const base = exam ? `/exams/${encodeURIComponent(exam.folder)}/` : '';
  let html = inline && !/\n/.test(text) ? marked.parseInline(text) : marked.parse(text);
  html = html.replace(/(src|href)="(assets\/[^"]+)"/g, (_, a, p) => `${a}="${base}${p}"`);
  html = html.replace(/<a href="([^"]+\.(?:mp4|mov|webm))"[^>]*>[^<]*<\/a>/gi, (_, u) => `<span class="media-window"><video controls preload="metadata" src="${u}"></video></span>`);
  html = html.replace(/<img\b[^>]*>/gi, m => `<span class="zoom-window">${m}<i class="fas fa-search-plus zoom-icon"></i></span>`);
  return html;
}
const md = (text, inline) => text ? `<div class="md">${mdHtml(text, inline)}</div>` : '';
const imgBox = src => `<span class="zoom-window"><img src="${src}" alt=""><i class="fas fa-search-plus zoom-icon"></i></span>`;

// ---------- persistence ----------
let saveTimer = null, saving = false, pendingPngs = {};
function save(now = false) {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(doSave, now ? 0 : 700);
}
async function doSave() {
  if (!attempt) return;
  if (saving) return save();
  saving = true;
  try {
    const body = { ...attempt, _drawingPngs: pendingPngs };
    pendingPngs = {};
    await api(`/api/attempt/${attempt.id}`, body);
    try { localStorage.setItem('attempt:' + attempt.id, JSON.stringify(attempt)); } catch {}
    setSaveState('');
  } catch (e) {
    setSaveState('⚠ Not saved – check the server');
    console.warn(e);
  } finally { saving = false; }
}
function setSaveState(t) { const el = document.getElementById('save-state'); if (el) el.textContent = t; }
window.addEventListener('beforeunload', () => { if (attempt && !attempt.submittedAt) doSave(); });

// ---------- timing ----------
const pausedMs = () => (attempt.pauses || []).reduce((t, p) => t + ((p.end || Date.now()) - p.start), 0);
const usedMs = () => Date.now() - Date.parse(attempt.startedAt) - pausedMs();
const isPaused = () => (attempt.pauses || []).some(p => !p.end);
const inReading = () => !!attempt && !attempt.submittedAt && usedMs() < attempt.readingMs;
const hms = ms => { const s = Math.max(0, Math.floor(Math.abs(ms) / 1000)); return [Math.floor(s / 3600), Math.floor(s / 60) % 60, s % 60].map(n => String(n).padStart(2, '0')).join(':'); };
const fmt = hms;
const words = ms => { const s = Math.max(0, Math.round(ms / 1000)); const parts = []; const h = Math.floor(s / 3600), m = Math.floor(s / 60) % 60, x = s % 60;
  if (h) parts.push(`${h} hour${h > 1 ? 's' : ''}`); if (m) parts.push(`${m} minute${m > 1 ? 's' : ''}`); if (x && !h) parts.push(`${x} second${x > 1 ? 's' : ''}`); return parts.join(' ') || '0 minutes'; };
// Rest breaks (NESA style): an allowance of N minutes per 30 minutes of exam time (reading + working).
// Each break uses at least 5 minutes of the allowance: you can come back early, but a short break is still
// charged as 5 minutes. A break ends by itself when the allowance runs out. The exam timer stops only for the
// actual time spent on the break.
const REST_MIN_MS = 5 * 60000;
const restAllowanceMs = (per, readingMs, durationMinutes) => per > 0 ? Math.floor((readingMs / 60000 + durationMinutes) / 30) * per * 60000 : null;
const restInfo = (per, readingMs, durationMinutes) => {
  const a = restAllowanceMs(per, readingMs, durationMinutes);
  return a == null ? 'Rest breaks – unlimited (practice setting)' : `Rest breaks – ${words(a)} in total (${per} minutes per 30 minutes of exam time), up to ${Math.floor(a / REST_MIN_MS)} break${Math.floor(a / REST_MIN_MS) === 1 ? '' : 's'}; each break uses at least 5 minutes, even if you return early`;
};
const hasAllowance = () => attempt.rest && attempt.rest.allowanceMs != null;
const restChargedMs = () => (attempt.pauses || []).reduce((t, p) => t + (p.end ? Math.max(p.end - p.start, REST_MIN_MS) : Date.now() - p.start), 0);
const restLeftMs = () => hasAllowance() ? attempt.rest.allowanceMs - restChargedMs() : Infinity;
const canRest = () => !hasAllowance() || restLeftMs() >= REST_MIN_MS;
const writingLeft = () => attempt.readingMs + attempt.durationMinutes * 60000 - usedMs();

// Per-question timing: time on screen (not during reading or breaks), visits, and typing per part.
function trackTime() {
  const now = Date.now(), last = ui.lastTick || now;
  ui.lastTick = now;
  if (!attempt || attempt.submittedAt || attempt.mode !== 'structured' || !groups.length || isPaused() || inReading()) return;
  const T = attempt.timing ||= { q: {}, p: {}, awayMs: 0 };
  const dt = Math.min(now - last, 2000);
  if (document.hidden) { T.awayMs += dt; return; }
  const key = String(groups[attempt.current]?.q.number);
  const q = T.q[key] ||= { ms: 0, visits: 0, firstSeenMs: workMs() };
  if (T.lastKey !== key) { q.visits++; T.lastKey = key; }
  q.ms += dt;
  if (now - (ui.lastTimingSave || 0) > 15000) { ui.lastTimingSave = now; save(); }
}
const workMs = () => Math.max(0, usedMs() - (attempt.readingMs || 0));
// Keystroke log: one entry per change, [working ms, position, chars deleted, text inserted].
// Worked out by diffing old and new text, so paste/autocorrect/undo are captured too.
function logKeys(partId, before, after) {
  if (before === after) return;
  let i = 0;
  while (i < before.length && i < after.length && before[i] === after[i]) i++;
  let j = 0;
  while (j < before.length - i && j < after.length - i && before[before.length - 1 - j] === after[after.length - 1 - j]) j++;
  const log = (attempt.keylog ||= {})[partId] ||= [];
  log.push([workMs(), i, before.length - i - j, after.slice(i, after.length - j)]);
}
function noteTyping(partId) {
  const T = attempt.timing ||= { q: {}, p: {}, awayMs: 0 };
  const p = T.p[partId] ||= { firstMs: workMs(), edits: 0 };
  p.lastMs = workMs(); p.edits++;
}

function updateTimer() {
  trackTime();
  if (!attempt || attempt.submittedAt) return;
  const el = document.getElementById('timer');
  if (!el) return;
  const used = usedMs();
  const reading = used < attempt.readingMs;
  const left = writingLeft();
  el.innerHTML = `<i class="far fa-clock"></i> ${reading ? 'Reading time left: ' + hms(attempt.readingMs - used) : left < 0 ? 'Overtime: ' + hms(-left) : 'Time left: ' + hms(left)}`;
  const rl = document.getElementById('rest-left'), bb = document.getElementById('break-box');
  if (rl) { rl.textContent = hasAllowance() ? hms(restLeftMs()) : ''; rl.title = hasAllowance() ? 'Rest time left' : ''; }
  if (bb && !isPaused()) bb.classList.toggle('hidden', !canRest());
  if (ui.wasReading !== reading) {
    const ended = ui.wasReading && !reading;
    ui.wasReading = reading;
    document.body.dataset.reading = reading ? '1' : '0';
    rerender();
    if (ended && !isPaused()) readingFinishedModal();
  }
  if (left <= 0 && !attempt.timeUpAt) {
    attempt.timeUpAt = new Date().toISOString();
    attempt.answersAtTimeUp = JSON.parse(JSON.stringify(attempt.answers || attempt.written || {}));
    attempt.mcAtTimeUp = attempt.mc ? { ...attempt.mc } : undefined;
    save(true);
    renderBanner();
    if (!isPaused()) timeUpModal();
  }
  attempt.timeUsedMs = Math.max(0, used - attempt.readingMs);
}
function rerender() { if (!attempt) return; if (attempt.mode === 'pdf') { if (document.getElementById('answers')) renderPdfAnswers(); } else renderQuestion(); }

// ---------- accessibility options (FONT SIZE / COLOUR), remembered per browser ----------
const FONT_SIZES = ['1em', '1.25em', '1.5em', '1.75em'];
const access = store.get('nesa:access', { font: 0, fg: '#000000', bg: '#ffffff' });
function applyAccess() {
  document.body.style.fontSize = FONT_SIZES[access.font] || '1em';
  const mod = access.fg.toLowerCase() !== '#000000' || access.bg.toLowerCase() !== '#ffffff';
  document.body.classList.toggle('colours-modified', mod);
  document.documentElement.style.setProperty('--user-fg', access.fg);
  document.documentElement.style.setProperty('--user-bg', access.bg);
  store.set('nesa:access', access);
}
applyAccess();

// ---------- toolbar ----------
function toolbarHtml({ flag, highlight, font = true, colour = true, info = true }) {
  const flagged = flag && groups.length && isFlagged(groups[attempt.current]);
  return `<div class="nav-toolbar"><div class="nav-toolbar-cell">
    ${flag ? `<div class="nav-toolbar-button nav-toolbar-button-flag"><div class="nav-toolbar-button-top${flagged ? ' expanded' : ''}" id="tb-flag" tabindex="0" title="Flag"><i class="fas fa-flag${flagged ? ' active' : ''}"></i><span>${flagged ? 'REMOVE FLAG' : 'FLAG'}</span></div></div>` : ''}
    ${highlight ? `<div class="nav-toolbar-button nav-toolbar-button-highlight dd"><div class="nav-toolbar-button-top has-chevron${ui.highlighter ? ' expanded' : ''}" tabindex="0" title="Highlight"><i class="fas fa-highlighter${ui.highlighter ? ' active' : ''}"></i><span>HIGHLIGHT</span><i class="fas fa-angle-down chevron"></i></div>
      <div class="nav-toolbar-button-dropdown"><p>Choose colour:</p><div class="hl-swatches">${['yellow', 'blue', 'red'].map(c => `<div class="highlight-color-button highlight-color-button-${c}${ui.highlighter === c ? ' selected' : ''}" data-hlc="${c}" tabindex="0" title="${c}"></div>`).join('')}</div>
      <div class="highlight-color-button-eraser${ui.highlighter === 'none' ? ' selected' : ''}" data-hlc="none" tabindex="0">No colour</div></div></div>` : ''}
    ${font ? `<div class="nav-toolbar-button nav-toolbar-button-font dd"><div class="nav-toolbar-button-top has-chevron${access.font ? ' expanded' : ''}" tabindex="0" title="Font size"><i class="fas fa-font${access.font ? ' active' : ''}"></i><span>FONT SIZE</span><i class="fas fa-angle-down chevron"></i></div>
      <div class="nav-toolbar-button-dropdown"><table class="font-table"><tbody>${['Regular', 'Large', 'Extra Large', 'XX Large'].map((n, i) => `<tr data-font="${i}" tabindex="0"><td>${access.font === i ? '<i class="fas fa-check"></i>' : ''}</td><td>${n}</td></tr>`).join('')}</tbody></table></div></div>` : ''}
    ${colour ? `<div class="nav-toolbar-button nav-toolbar-button-color dd"><div class="nav-toolbar-button-top has-chevron${document.body.classList.contains('colours-modified') ? ' expanded' : ''}" tabindex="0" title="Colour"><i class="fas fa-adjust"></i><span>COLOUR</span><i class="fas fa-angle-down chevron"></i></div>
      <div class="nav-toolbar-button-dropdown"><table class="colour-table"><tbody><tr><td>Font colour:</td><td style="text-align:right"><input type="color" id="fg-selector" value="${access.fg}"></td></tr><tr><td>Background colour:</td><td style="text-align:right"><input type="color" id="bg-selector" value="${access.bg}"></td></tr></tbody></table>
      <a class="reset-colours" id="reset-access" tabindex="0"><i class="fas fa-redo"></i> reset to default settings</a></div></div>` : ''}
    ${info ? `<div class="nav-toolbar-button nav-toolbar-button-info"><div class="nav-toolbar-button-top nav-toolbar-button-top-info" id="tb-info" tabindex="0" title="Info"><i class="fas fa-key"></i><span>INFO</span></div></div>` : ''}
  </div></div>`;
}
function bindToolbar(root, rerenderToolbar) {
  $$('.dd', root).forEach(dd => {
    let t = null;
    const open = v => { clearTimeout(t); if (v) { $$('.dd.open', root).forEach(o => o !== dd && o.classList.remove('open')); dd.classList.add('open'); } else t = setTimeout(() => dd.classList.remove('open'), 150); };
    dd.addEventListener('mouseenter', () => open(true));
    dd.addEventListener('mouseleave', () => open(false));
    const top = $('.nav-toolbar-button-top', dd);
    top.addEventListener('click', () => dd.classList.toggle('open'));
    top.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); dd.classList.toggle('open'); } });
  });
  const flag = $('#tb-flag', root);
  if (flag) { flag.onclick = toggleFlag; flag.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleFlag(); } }; }
  $$('[data-hlc]', root).forEach(b => b.onclick = () => {
    ui.highlighter = ui.highlighter === b.dataset.hlc ? null : b.dataset.hlc;
    document.body.classList.remove('hl-yellow', 'hl-blue', 'hl-red', 'hl-none');
    if (ui.highlighter) document.body.classList.add('hl-' + ui.highlighter);
    rerenderToolbar();
  });
  $$('[data-font]', root).forEach(r => r.onclick = () => { access.font = +r.dataset.font; applyAccess(); rerenderToolbar(); if (groups.length && $('#nav')) renderNav(true); });
  const fg = $('#fg-selector', root), bg = $('#bg-selector', root);
  if (fg) fg.oninput = () => { access.fg = fg.value; applyAccess(); };
  if (bg) bg.oninput = () => { access.bg = bg.value; applyAccess(); };
  const reset = $('#reset-access', root);
  if (reset) reset.onclick = () => { Object.assign(access, { font: 0, fg: '#000000', bg: '#ffffff' }); applyAccess(); rerenderToolbar(); if (groups.length && $('#nav')) renderNav(true); };
  const info = $('#tb-info', root);
  if (info) { info.onclick = infoModal; info.onkeydown = e => { if (e.key === 'Enter') infoModal(); }; }
}
function renderToolbar(opts) {
  const host = document.getElementById('toolbar');
  if (!host) return;
  host.innerHTML = toolbarHtml(opts);
  bindToolbar(host, () => renderToolbar(opts));
}

// close toolbar dropdowns when the pointer or a click goes elsewhere
const closeDropdowns = e => { $$('.dd.open').forEach(d => { if (!e || !d.contains(e.target)) d.classList.remove('open'); }); };
document.addEventListener('mousedown', closeDropdowns);
document.addEventListener('mouseover', e => { if (!e.target.closest('.dd')) closeDropdowns(e); });

// ---------- modals ----------
function openModal(html, { large = false, closable = false } = {}) {
  closeModal(); closeDropdowns();
  const c = document.createElement('div');
  c.className = 'modal-container';
  c.id = 'modal';
  c.innerHTML = `<div class="modal${large ? ' modal-large' : ''}" role="dialog" aria-modal="true">${closable ? '<button class="close-x" id="modal-close">Close this screen X</button>' : ''}<div class="modal-body">${html}</div></div>`;
  document.body.appendChild(c);
  if (closable) {
    $('#modal-close', c).onclick = closeModal;
    c.addEventListener('click', e => { if (e.target === c) closeModal(); });
    c.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
  }
  return c;
}
function closeModal() { document.getElementById('modal')?.remove(); }
// In-page yes/no question. Browser confirm() is unreliable: it is silently dismissed whenever
// automation (e.g. a DevTools/Playwright connection) is attached to Chrome.
function askConfirm(message, yes = 'Yes', no = 'Cancel') {
  return new Promise(resolve => {
    const m = openModal(`<p>${esc(message)}</p><div class="modal-actions" style="display:flex;gap:12px;justify-content:center;margin-top:16px">
      <button class="nsw-button nsw-button--dark" id="ask-yes">${esc(yes)}</button>
      <button class="nsw-button nsw-button--white" id="ask-no">${esc(no)}</button></div>`);
    $('#ask-yes', m).onclick = () => { closeModal(); resolve(true); };
    $('#ask-no', m).onclick = () => { closeModal(); resolve(false); };
    $('#ask-yes', m).focus();
  });
}

function infoModal() {
  const timed = attempt && !attempt.submittedAt;
  const sample = (cls, inner) => `<span class="nav-elem${cls}">${inner}</span>`;
  const m = openModal(`<div class="info-content">
    <div class="info-block"><h2>Exam information</h2>
      <h4>Reading time</h4><p>${timed && attempt.readingMs ? `You have ${words(attempt.readingMs)} reading time. During reading time you will not be able to answer questions. You can move freely between the questions, and you can flag questions. Highlighting of text is also permitted.` : 'There is no reading time for this practice attempt. In the real exam you will be given 10 minutes reading time.'}</p>
      <h4>Working time</h4><p>${timed ? `You have ${words(attempt.durationMinutes * 60000)} to attempt the questions. A countdown timer is displayed at the top right.` : 'The countdown timer is displayed at the top right.'}</p>
      <h4>Rest breaks</h4><p>${timed && hasAllowance() ? `You have ${words(attempt.rest.allowanceMs)} of rest breaks (${attempt.rest.perHalfHour} minutes per 30 minutes); ${words(Math.max(0, restLeftMs()))} left. ` : ''}Use <b>Take a break</b> in the header to pause the timer; the time next to it is your rest time left. Each break uses at least 5 minutes of rest time, even if you click <b>CONTINUE</b> early, and a break ends by itself when your rest time runs out. The exam timer stops only while you are on a break.</p>
      <h4>Word count</h4><p>The number of words shown under each response box (for example <span class="word-count" style="display:inline">0 / 105 words</span>) gives an indication of the length of response.</p>
    </div>
    <div class="info-block"><h2>Navigation and toolbar</h2>
      <p><b>The navigation bar</b> contains the question numbers, and access to this information page.</p>
      <ul class="legend">
        <li>${sample('', '6<i class="fas fa-flag nav-elem-flagged"></i>')} A question you have flagged to come back to later</li>
        <li>${sample('', '2<i class="far fa-check-circle nav-elem-answered halo"></i><i class="fas fa-check-circle nav-elem-answered"></i>')} A question for which you have attempted all parts</li>
        <li>${sample(' nav-elem-current', '5<span class="nav-elem-current-underline"></span>')} The question you are on now</li>
        <li>${sample('', '<i class="fas fa-angle-left"></i>')}${sample('', '<i class="fas fa-angle-right"></i>')} ‘Next’ and ‘previous’ buttons for when there are more questions than the navigation bar has space to display</li>
      </ul>
      <h4>Toolbar</h4><p><b>FLAG</b> a question to come back to later · <b>HIGHLIGHT</b> text or remove a highlight (choose a colour, then select text; choose the same colour again to turn highlighting off) · <b>FONT SIZE</b> to increase text size · <b>COLOUR</b> to change the colours of the foreground text and the background.</p>
    </div>
    <div class="info-block"><h2>Zoom functions</h2>
      <h4>Browser/screen zoom</h4><p><i>command +</i> or <i>command –</i> (Mac), <i>control +</i> or <i>control –</i> (Windows).</p>
      <h4>Zoom-window</h4><p>Images appearing with a blue border can be expanded to a full-screen view by clicking on them.</p>
    </div>
    <div class="info-block"><h2>Textbox tools</h2><p>Spell-check is turned off, as in the HSC exam. The response textbox toolbar has bullet and numbered lists, cut, copy, paste, undo, redo and special characters (Ω).</p>
      <h4>Python code editor</h4><p>Input Python code in the left panel. When you click ‘Run’, the output will appear in the right panel. Click ‘Full screen’ to view the code editor full screen.</p>
      <h4>Generic code editor</h4><p>A panel for entering pseudocode or other code formats, without a ‘Run’ function.</p>
      <h4>Drawing tool</h4><p>Draw diagrams with the drawing tool. ‘Reset’ clears your drawing.</p>
    </div>
    <div class="info-block"><h2>Exit exam</h2><p>You can choose to exit the exam by using the ‘Exit exam’ button at the bottom of the last question.</p>
      ${timed ? `<h4>Practice app</h4><p>Your answers are saved automatically to <code>papers/attempts/</code>.</p><button class="nsw-button nsw-button--dark-outline" id="to-menu">Save and return to menu</button>` : ''}
    </div></div>`, { large: true, closable: true });
  const tm = $('#to-menu', m);
  if (tm) tm.onclick = () => { closeModal(); doSave(); home(); };
}

function readingFinishedModal() {
  const m = openModal(`<h3>Reading time has now finished.</h3><p>You have <strong>${words(writingLeft())}</strong> to answer the questions.</p>
    <button class="nsw-button nsw-button--dark" id="start-writing">START <i class="fa fa-angle-right"></i></button>`);
  $('#start-writing', m).onclick = closeModal;
}

function timeUpModal() {
  const m = openModal(`<h2>Working time has finished.</h2><p>In the HSC exam your responses are submitted now. Your answers at this moment have been saved.</p>
    <p>You can finish now, or keep writing for practice — anything you add from now on is marked as overtime.</p>
    <div class="modal-button-container"><button class="nsw-button nsw-button--dark" id="tu-finish">Yes, finish exam now <i class="fa fa-angle-right"></i></button>
    <button class="nsw-button nsw-button--dark" id="tu-cont">Keep writing (overtime) <i class="fa fa-angle-right"></i></button></div>`);
  $('#tu-finish', m).onclick = () => finishExam();
  $('#tu-cont', m).onclick = closeModal;
}

// Drills (questions from Claude): one click to finish, straight back to the menu.
async function finishDrill() {
  const unatt = groups.filter(g => !groupAnswered(g)).length;
  if (unatt && !(await askConfirm(`${unatt} question${unatt === 1 ? ' is' : 's are'} unanswered. Finish anyway?`, 'Finish drill', 'Keep going'))) return;
  finishExam();
}
document.addEventListener('click', e => { if (e.target.closest('#finish-drill')) finishDrill(); });

function finishModal() {
  if (exam?.drill && attempt?.mode === 'structured') return finishDrill();
  const unatt = attempt.mode === 'pdf' ? (attempt.written || []).filter(w => !(w.text || '').trim()).length : groups.filter(g => !groupAnswered(g)).length;
  const flagged = attempt.mode === 'pdf' ? 0 : groups.filter(isFlagged).length;
  const left = writingLeft();
  const m = openModal(`<h2>Are you sure you want to finish your exam now?</h2>
    <p>You have <strong>${unatt}</strong> ${attempt.mode === 'pdf' ? `blank answer box${unatt === 1 ? '' : 'es'}` : `unattempted question${unatt === 1 ? '' : 's'}`} and flagged <strong>${flagged}</strong> question${flagged === 1 ? '' : 's'}.</p>
    ${left > 0 ? `<p>You have <strong>${words(left)} remaining</strong> to complete or review your answers.</p>` : ''}
    <p><strong>Once you finish your exam, you will no longer be able to review or edit responses.</strong></p>
    <p class="check-row"><input id="agree" type="checkbox"><label for="agree">Yes, I am sure I want to finish this exam and submit my responses now.</label></p>
    <div class="modal-button-container"><button class="nsw-button nsw-button--dark" id="finish" disabled>Yes, finish exam now <i class="fa fa-angle-right"></i></button>
      <button class="nsw-button nsw-button--dark" id="return">Return to exam <i class="fa fa-angle-right"></i></button></div>`);
  const agree = $('#agree', m), fin = $('#finish', m);
  agree.onchange = () => { fin.disabled = !agree.checked; };
  fin.onclick = () => finishExam();
  $('#return', m).onclick = closeModal;
}

// ---------- lightbox for zoom-window images ----------
document.addEventListener('click', e => {
  const z = e.target.closest('.zoom-window');
  if (!z || ui.highlighter || window.getSelection()?.toString()) return;
  const img = $('img', z);
  if (!img) return;
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = `<button class="close-x">Close this screen X</button><img src="${img.src}" alt="">`;
  lb.onclick = () => lb.remove();
  document.body.appendChild(lb);
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') $('.lightbox')?.remove(); });

// ---------- highlighter ----------
document.addEventListener('mouseup', () => {
  if (!ui.highlighter) return;
  const sel = window.getSelection();
  if (!sel || sel.isCollapsed || !sel.rangeCount) return;
  const range = sel.getRangeAt(0);
  const host = (range.commonAncestorContainer.nodeType === 1 ? range.commonAncestorContainer : range.commonAncestorContainer.parentElement).closest('.hl');
  if (!host) return;
  const texts = [];
  const walker = document.createTreeWalker(host, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) if (range.intersectsNode(walker.currentNode) && walker.currentNode.nodeValue.trim()) texts.push(walker.currentNode);
  for (let node of texts) {
    if (ui.highlighter === 'none') { const sp = node.parentElement.closest('.highlighted'); if (sp && host.contains(sp)) sp.replaceWith(...sp.childNodes); continue; }
    let start = node === range.startContainer ? range.startOffset : 0;
    let end = node === range.endContainer ? range.endOffset : node.nodeValue.length;
    if (end <= start) continue;
    if (end < node.nodeValue.length) node.splitText(end);
    if (start > 0) node = node.splitText(start);
    const old = node.parentElement.closest('.highlighted');
    if (old && host.contains(old) && old.childNodes.length === 1) { old.className = 'highlighted ' + ui.highlighter; continue; }
    const span = document.createElement('span');
    span.className = 'highlighted ' + ui.highlighter;
    node.replaceWith(span); span.appendChild(node);
  }
  host.normalize();
  sel.removeAllRanges();
  if (attempt && host.dataset.hl) ui.hl[`${attempt.id}|${attempt.current}|${host.dataset.hl}`] = host.innerHTML;
});
function restoreHighlights(root) {
  $$('[data-hl]', root).forEach(h => { const v = ui.hl[`${attempt.id}|${attempt.current}|${h.dataset.hl}`]; if (v != null) h.innerHTML = v; });
}

// ---------- shared exam chrome ----------
function chromeHtml(title, { nav = true, flag = true, highlight = true } = {}) {
  return `<div class="test-container">
    <header class="header-test"><div class="margin-wrapper"><div class="header-container">
      <div class="header-test-title">${esc(title)}</div>
      <span id="save-state" class="save-state"></span>
      <div class="header-test-break" id="break-box"><button class="nsw-button nsw-button--dark" id="pause" name="break">Take a break <i aria-hidden="true" class="fa fa-angle-right"></i></button><span id="rest-left"></span></div>
      ${exam?.drill ? '<button class="nsw-button nsw-button--dark" id="finish-drill" style="margin-right:12px">Finish drill <i class="fas fa-check"></i></button>' : ''}
      <div class="header-test-subtitle" id="timer"></div>
    </div></div></header>
    <div class="nav-bar"><div class="margin-wrapper"><div class="nav-bar-inner">
      <div class="nav-wrapper">${nav ? '<nav id="nav"></nav>' : ''}</div>
      <div id="toolbar"></div>
    </div></div></div>
    <div id="banner"></div>
    <div class="content test-content" id="content"></div>
    <footer class="test-footer"></footer>
  </div>`;
}
function renderBanner() {
  const b = document.getElementById('banner');
  if (!b) return;
  b.innerHTML = attempt.timeUpAt ? `<div class="exam-banner timeup">Working time has finished. Your answers at time-up were saved separately; anything you add now is marked as overtime.</div>` : '';
}
function startClock() {
  ui.wasReading = inReading();
  document.body.dataset.reading = ui.wasReading ? '1' : '0';
  clearInterval(tick); tick = setInterval(updateTimer, 500); updateTimer();
  document.getElementById('pause').onclick = pause;
  if (isPaused()) showBreakScreen();
}

// ---------- home (menu) ----------
async function home() {
  exam = null; attempt = null; groups = []; clearInterval(tick); closeModal();
  const [{ exams, pdfs, drills = [] }, attempts] = await Promise.all([api('/api/exams'), api('/api/attempts')]);
  const priv = exams.filter(e => e.private), fresh = exams.filter(e => !e.sat && !e.private), sat = exams.filter(e => e.sat && !e.private);
  const prefs = { reading: 10, targets: true, restPer: 5, live: false, ...store.get('nesa:prefs', {}) };
  const examRow = e => `<div class="exam-row"><button class="nsw-button nsw-button--dark" data-start="${esc(e.folder)}">${esc(e.exam)}</button>
      <span class="meta">${e.marks} marks · ${e.minutes ? e.minutes + ' min' : 'untimed'} · ${e.parts} parts${e.sat ? '<span class="tag">sat before</span>' : ''}</span></div>`;
  const unsub = attempts.filter(a => !a.submittedAt), subm = attempts.filter(a => a.submittedAt);
  $app.innerHTML = `<div class="landing">
    <div class="masthead">Local practice copy of the HSC online exam interface</div>
    <div class="landing-header"><div><div class="brand">HSC Online Examinations – Practice</div><div class="sub">Software Engineering · your exported Gradeo papers, sat in the NESA exam layout</div></div></div>
    <div class="nav-bar"><div class="nav-bar-inner" id="toolbar"></div></div>
    <div class="landing-grid">
      <div class="feature">
        ${unsub.length ? `<h2>Resume</h2>${unsub.map(a => `<div class="exam-row"><button class="nsw-button nsw-button--dark" data-resume="${esc(a.id)}">${esc(a.title)}</button><span class="meta">started ${new Date(a.startedAt).toLocaleString()}</span></div>`).join('')}` : ''}
        ${drills.filter(d => !d.done).length ? `<h2${unsub.length ? ' class="small"' : ''}>From Claude</h2>${drills.filter(d => !d.done).map(examRow).join('')}` : ''}
        ${drills.some(d => d.done) ? `<details><summary>Finished questions from Claude (${drills.filter(d => d.done).length})</summary>${drills.filter(d => d.done).map(examRow).join('')}</details>` : ''}
        ${priv.length ? `<h2 class="small">Trial papers (private)</h2>${priv.map(examRow).join('')}` : ''}
        <h2${unsub.length || drills.length || priv.length ? ' class="small"' : ''}>Exported Gradeo papers – not sat yet</h2>
        ${fresh.map(examRow).join('') || '<p>None</p>'}
        <details><summary>Papers you've sat before (${sat.length})</summary>${sat.map(examRow).join('')}</details>
        <h2 class="small">PDF papers</h2>
        ${pdfs.length ? pdfs.map(f => `<div class="pdf-row"><button class="nsw-button nsw-button--dark" data-pdf="${esc(f)}">${esc(f.replace(/\.pdf$/i, ''))}</button><label>Writing time <input class="field" type="number" data-dur="${esc(f)}" value="150"> min</label><label>MC qs <input class="field" type="number" data-mc="${esc(f)}" value="20"></label></div>`).join('') : '<p>No PDFs yet (put them in ~/gradeo/papers/).</p>'}
        <h2 class="small">Free answer sheet</h2>
        <p>For papers read elsewhere (e.g. on Gradeo): answer boxes and a timer.</p>
        <div class="pdf-row"><label>Name <input class="field" type="text" id="free-name" placeholder="CSSA 2025" ${NO_SPELL}></label><label>Time <input class="field" type="number" id="free-dur" value="150"> min</label><button class="nsw-button nsw-button--dark" id="free-start">Start <i class="fa fa-angle-right"></i></button></div>
        ${subm.length ? `<details><summary>Submitted attempts (${subm.length})</summary>${subm.map(a => `<p><b>${esc(a.title)}</b> – submitted ${new Date(a.submittedAt).toLocaleString()} · <a href="/papers/attempts/${esc(a.id)}.md" target="_blank">answers file</a></p>`).join('')}</details>` : ''}
      </div>
      <div class="feature">
        <h2>Settings for the next start</h2>
        <div class="settings-row"><label>Reading time <input class="field" type="number" id="reading" value="${prefs.reading}" min="0" max="15"> min</label></div>
        <div class="settings-row"><label>Rest breaks <input class="field" type="number" id="rest-per" value="${prefs.restPer}" min="0" max="30"> min per 30 min of exam time</label></div>
        <p class="muted" style="margin-top:-.5em">Each break uses at least 5 minutes of rest time, even if you come back early. Counted on reading + working time, e.g. the HSC Software Engineering exam (10 min reading + 2 h 20 min working = 2 h 30 min) gives 25 minutes, so up to 5 breaks. Set 0 for unlimited breaks.</p>
        <div class="settings-row"><label><input type="checkbox" id="live" ${prefs.live ? 'checked' : ''}> Check answers as I go on papers too (shows the answer and explanation after each question; drills always do this)</label></div>
        <div class="settings-row"><label><input type="checkbox" id="targets" ${prefs.targets ? 'checked' : ''}> Show word guides under answer boxes (~35 words per mark, shown as “0 / 105 words”)</label></div>
        <p>The exam screens follow NESA's HSC online exam: question numbers across the top, FLAG / HIGHLIGHT / FONT SIZE / COLOUR / INFO toolbar, “Time left” at the top right, <b>Take a break</b> to pause the timer, and <b>Exit exam</b> on the last question to finish.</p>
        <p>Spell-check is off in every answer box, as in the real exam. Answers autosave to <code>papers/attempts/</code>; when you finish, an answers file is written for marking.</p>
        <p>The real HSC Software Engineering exam gives 10 minutes reading time.</p>
      </div>
    </div>
    <footer class="site-footer"><div>HSC Online Examinations – practice</div><div class="footer-secondary">Runs locally on this computer</div></footer>
  </div>`;
  renderToolbar({ font: true, colour: true, info: false });
  const settings = () => {
    const s = { readingMs: Math.max(0, +document.getElementById('reading').value || 0) * 60000, showTargets: document.getElementById('targets').checked, restPer: Math.max(0, +document.getElementById('rest-per').value || 0), liveMark: document.getElementById('live').checked };
    store.set('nesa:prefs', { reading: s.readingMs / 60000, targets: s.showTargets, restPer: s.restPer, live: s.liveMark });
    return s;
  };
  $$('[data-start]').forEach(b => b.onclick = () => startStructured(b.dataset.start, settings()));
  $$('[data-resume]').forEach(b => b.onclick = () => resume(b.dataset.resume));
  $$('[data-pdf]').forEach(b => b.onclick = () => {
    const f = b.dataset.pdf;
    startPdf({ pdf: f, title: f.replace(/\.pdf$/i, ''), durationMinutes: +$(`[data-dur="${CSS.escape(f)}"]`).value || 150, mcCount: +$(`[data-mc="${CSS.escape(f)}"]`).value || 20, ...settings() });
  });
  document.getElementById('free-start').onclick = () => {
    const name = document.getElementById('free-name').value.trim() || 'Free answer sheet';
    startPdf({ pdf: null, title: name, durationMinutes: +document.getElementById('free-dur').value || 150, mcCount: 20, ...settings() });
  };
}

async function resume(id) {
  attempt = await api(`/api/attempt/${id}`);
  if (attempt.mode === 'pdf') return runPdf();
  exam = await api(`/api/exam/${encodeURIComponent(attempt.folder)}`);
  runStructured();
}

// ---------- begin screen (General Instructions → BEGIN READING TIME / START) ----------
function beginScreen({ title, instructions, structure, readingMs, onStart }) {
  $app.innerHTML = `<div class="test-container">
    <header class="header-test"><div class="margin-wrapper"><div class="header-container"><div class="header-test-title">${esc(title)}</div></div></div></header>
    <div class="nav-bar"><div class="margin-wrapper"><div class="nav-bar-inner"><div class="nav-wrapper"></div><div id="toolbar"></div></div></div></div>
    <div class="content test-content begin-content"><div class="begin-grid">
      <div><h1>General Instructions</h1><ul>${instructions.map(i => `<li>${i}</li>`).join('')}</ul></div>
      <div class="feature begin-box"><div class="feature aqua">${structure}</div>
        <div class="go"><button class="nsw-button nsw-button--dark" id="begin">${readingMs ? 'BEGIN READING TIME' : 'START'} <i aria-hidden="true" class="fa fa-angle-right"></i></button>
        <p style="margin-top:1.5em"><a href="#" id="back-menu">Back to menu</a></p></div></div>
    </div></div>
    <footer class="test-footer"></footer></div>`;
  renderToolbar({ font: true, colour: true, info: false });
  $('#back-menu').onclick = e => { e.preventDefault(); home(); };
  $('#begin').onclick = () => {
    if (!readingMs) return onStart();
    const m = openModal(`<p class="check-row"><input id="agree" type="checkbox"><label for="agree">The Supervisor has announced you can begin ${words(readingMs)} Reading Time.</label></p>
      <button class="nsw-button nsw-button--dark" id="begin-reading" disabled>BEGIN READING TIME <i class="fa fa-angle-right"></i></button>`, { closable: true });
    $('#agree', m).onchange = e => { $('#begin-reading', m).disabled = !e.target.checked; };
    $('#begin-reading', m).onclick = () => { closeModal(); onStart(); };
  };
}
const durWords = min => words(min * 60000);

// ---------- structured (exported Gradeo) exam ----------
async function startStructured(folder, settings) {
  exam = await api(`/api/exam/${encodeURIComponent(folder)}`);
  if (exam.reading_minutes != null) settings = { ...settings, readingMs: exam.reading_minutes * 60000 };
  const durationMinutes = exam.duration_minutes || Math.round(exam.total_available * 1.9);
  const counts = {};
  const typeName = { MULTI_CHOICE: 'multiple-choice', OBJECTIVE_RESPONSE: 'objective-response', SHORT: 'short-answer', CODING: 'coding', SQL: 'SQL', RICH_TABLE: 'table', DRAWING_V2: 'drawing' };
  exam.questions.forEach(q => q.parts.forEach(p => { const n = typeName[p.type] || 'short-answer'; counts[n] = (counts[n] || 0) + 1; }));
  const n = exam.questions.length;
  beginScreen({
    title: exam.exam, readingMs: settings.readingMs,
    instructions: [settings.readingMs ? `Reading time – ${durWords(settings.readingMs / 60000)}` : 'No reading time', `Working time – ${durWords(durationMinutes)}${exam.duration_minutes ? '' : ' (estimated: this paper is untimed)'}`,
      restInfo(settings.restPer, settings.readingMs, durationMinutes), 'Answer all questions in the spaces provided on screen', 'Spell-check is turned off', 'Your responses are saved automatically'],
    structure: `<h3>${exam.total_available} marks</h3><p><b>Attempt Questions 1–${n}</b></p><p>Allow about ${durWords(durationMinutes)} for this paper.</p>
      <p>${Object.entries(counts).map(([k, v]) => `${v} ${k} item${v > 1 ? 's' : ''}`).join(' · ')}</p>`,
    onStart: () => {
      attempt = { id: `${stamp()}_${slug(exam.exam)}`, mode: 'structured', folder, title: exam.exam, startedAt: new Date().toISOString(),
        durationMinutes, readingMs: settings.readingMs, showTargets: settings.showTargets,
        rest: { perHalfHour: settings.restPer, allowanceMs: restAllowanceMs(settings.restPer, settings.readingMs, durationMinutes) },
        pauses: [], answers: {}, flags: {}, current: 0, navByQuestion: true, liveMark: !!exam.drill || !!settings.liveMark };
      save(true);
      runStructured();
    },
  });
}

function runStructured() {
  if (attempt.liveMark == null) attempt.liveMark = !!exam.drill;
  groups = exam.questions.map((q, idx) => ({ q, idx }));
  if (!attempt.navByQuestion) { // older attempts stored the part index
    const flat = []; exam.questions.forEach((q, qi) => q.parts.forEach(() => flat.push(qi)));
    attempt.current = flat[attempt.current] ?? 0; attempt.navByQuestion = true;
  }
  attempt.flags = attempt.flags || {};
  attempt.current = Math.max(0, Math.min(groups.length - 1, attempt.current || 0));
  ui.navRange = null;
  $app.innerHTML = chromeHtml(exam.exam);
  renderToolbar({ flag: true, highlight: true });
  renderNav(); renderQuestion(); renderBanner();
  startClock();
  window.onresize = () => { if (groups.length && $('#nav')) renderNav(true); };
}

function answered(p) {
  const a = attempt.answers[p.part_id];
  if (!a) return false;
  if (a.letters) return a.letters.length > 0;
  if (a.rows) return a.rows.some(Boolean);
  if (a.cells) return Object.values(a.cells).some(v => (v || '').trim());
  if (a.elements) return a.elements.some(e => !e.isDeleted);
  if (a.text != null) return !!a.text.trim() && a.text.trim() !== (p.question.starter_code || p.question.starter_query || '').trim();
  return false;
}
const groupAnswered = g => g.q.parts.every(answered);
const flagKey = g => 'Q' + g.q.number;
const isFlagged = g => !!(attempt.flags[flagKey(g)] || g.q.parts.some(p => attempt.flags[p.part_id]));
function toggleFlag() {
  const g = groups[attempt.current];
  const on = !isFlagged(g);
  delete attempt.flags[flagKey(g)]; g.q.parts.forEach(p => delete attempt.flags[p.part_id]);
  if (on) attempt.flags[flagKey(g)] = true;
  save(); renderNav(); renderToolbar({ flag: true, highlight: true });
}

// navigation bar with NESA's paging (‹ › when the numbers don't fit)
function navMax() {
  const nav = $('#nav');
  const w = nav.parentElement.getBoundingClientRect().width - 20;
  const fs = parseFloat(getComputedStyle(nav).fontSize);
  return Math.max(3, Math.floor(w / (fs * 2 + 2 + 7)));
}
function resetRange(index, max) {
  const total = groups.length;
  if (max >= total) return { start: 0, end: total, max, total, previous: false, next: false };
  const before = Math.round((max - 1) / 2), after = max - before - 1;
  const r = { start: index - before, end: index + after + 1, max, total };
  if (r.start < 0) { r.start = 0; r.end = max; }
  if (r.end > total) { r.start = total - max; r.end = total; }
  r.previous = r.start !== 0; if (r.previous) r.start += 1;
  r.next = r.end !== total; if (r.next) r.end -= 1;
  return r;
}
function moveRange(inc) {
  const o = ui.navRange, r = { ...o, start: o.start + inc, end: o.end + inc };
  if (o.previous) { if (r.start === 1) { r.start = 0; r.previous = false; } } else if (r.start > 0) { r.start += 1; r.previous = true; }
  if (o.next) { if (r.end === r.total - 1) { r.end = r.total; r.next = false; } } else if (r.end < r.total) { r.end -= 1; r.next = true; }
  ui.navRange = r; renderNav();
}
function renderNav(recalc = false) {
  const nav = $('#nav');
  if (!nav) return;
  const max = navMax();
  if (!ui.navRange || recalc || ui.navRange.max !== max) ui.navRange = resetRange(attempt.current, max);
  const r = ui.navRange;
  nav.innerHTML = (r.previous ? `<div class="nav-elem" data-move="-1" tabindex="0"><i class="fas fa-angle-left"></i></div>` : '') +
    groups.slice(r.start, r.end).map(g => {
      const cur = g.idx === attempt.current, fl = isFlagged(g), done = groupAnswered(g);
      return `<div class="nav-elem${cur ? ' nav-elem-current' : ''}" data-go="${g.idx}" tabindex="0" title="Question ${esc(g.q.number)}">${cur ? '<div class="nav-elem-current-underline"></div>' : ''}${done && !fl ? '<i class="far fa-check-circle nav-elem-answered halo"></i><i class="fas fa-check-circle nav-elem-answered"></i>' : ''}${fl ? '<i class="fas fa-flag nav-elem-flagged"></i>' : ''}${esc(g.q.number)}</div>`;
    }).join('') +
    (r.next ? `<div class="nav-elem" data-move="1" tabindex="0"><i class="fas fa-angle-right"></i></div>` : '');
  $$('[data-go]', nav).forEach(b => { b.onclick = () => go(+b.dataset.go); b.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') go(+b.dataset.go); }; });
  $$('[data-move]', nav).forEach(b => b.onclick = () => moveRange(+b.dataset.move));
}
function go(i) {
  attempt.current = Math.max(0, Math.min(groups.length - 1, i));
  save();
  ui.navRange = resetRange(attempt.current, ui.navRange?.max || navMax());
  renderNav(); renderQuestion(); renderToolbar({ flag: true, highlight: true });
}

// ---- Excalidraw (NESA's drawing tool is Excalidraw too) ----
let excalidrawLoaded = null;
const addScript = src => new Promise((r, j) => { const s = document.createElement('script'); s.src = src; s.onload = r; s.onerror = j; document.head.appendChild(s); });
function loadExcalidraw() {
  if (excalidrawLoaded) return excalidrawLoaded;
  window.EXCALIDRAW_ASSET_PATH = 'https://unpkg.com/@excalidraw/excalidraw@0.17.6/dist/';
  excalidrawLoaded = addScript('https://unpkg.com/react@18.3.1/umd/react.production.min.js')
    .then(() => addScript('https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js'))
    .then(() => addScript('https://unpkg.com/@excalidraw/excalidraw@0.17.6/dist/excalidraw.production.min.js'));
  excalidrawLoaded.catch(() => { excalidrawLoaded = null; });
  return excalidrawLoaded;
}

const partLabel = p => { const m = /^part\s*([a-z0-9]+)/i.exec(p.part || ''); return m ? `(${m[1].toLowerCase()})` : (p.part || ''); };
const marksText = m => m == null ? '' : `(${m} mark${m === 1 ? '' : 's'})`;
function withMarks(prompt, marks) {
  const t = (prompt || '').replace(/\s+$/, '');
  if (marks == null) return t;
  const last = t.split('\n').pop() || '';
  return /^\s*(\||```|!\[|<|\s{4})/.test(last) || !last.trim() ? `${t}\n\n${marksText(marks)}` : `${t} ${marksText(marks)}`;
}
// Python questions get NESA's Python editor (with Run); pseudocode and other code get the generic code editor
const isPython = p => p.type === 'CODING' && (!p.question.language || /py/i.test(p.question.language)) && !/pseudo-?code/i.test(p.prompt || '');

function itemControlHtml(p, i, reading) {
  reading = reading || !!attempt.checked?.[p.part_id];   // a checked answer is locked like reading time
  const s = p.question, a = attempt.answers[p.part_id] || {}, dis = reading ? 'disabled' : '';
  const base = `/exams/${encodeURIComponent(exam.folder)}/`;
  switch (p.type) {
    case 'MULTI_CHOICE':
      return `${s.multi ? '<p class="select-all">Select all that apply.</p>' : ''}<table class="ninja response_table"><tbody>${s.options.map((o, k) => {
        const id = `opt-${i}-${k}`;
        return `<tr><td class="rcell"><input type="${s.multi ? 'checkbox' : 'radio'}" id="${id}" name="mc-${i}" data-opt="${esc(o.letter)}" ${(a.letters || []).includes(o.letter) ? 'checked' : ''} ${dis}></td>
          <td class="acell"><label for="${id}" class="hl" data-hl="opt-${i}-${k}">${mdHtml(o.text || '', true)}${o.image ? imgBox(base + o.image) : ''}</label></td></tr>`;
      }).join('')}</tbody></table>`;
    case 'OBJECTIVE_RESPONSE':
      return `<table class="hoa-table-multiselect"><thead><tr><th></th>${s.columns.map(c => `<th class="centre">${esc(c)}</th>`).join('')}</tr></thead><tbody>${s.rows.map((r, ri) => `<tr><td class="hl" data-hl="or-${i}-${ri}">${esc(r.statement)}</td>${s.columns.map(c => `<td class="centre"><input type="radio" name="or-${i}-${ri}" data-or="${ri}" value="${esc(c)}" aria-label="${esc(c)}" ${a.rows?.[ri] === c ? 'checked' : ''} ${dis}></td>`).join('')}</tr>`).join('')}</tbody></table>`;
    case 'RICH_TABLE': {
      const headRow = s.table[0]?.every(c => c.type === 'text');
      return `<table class="rich"><tbody>${s.table.map((row, ri) => `<tr>${row.map((c, ci) => {
        const k = `${ri},${ci}`, v = a.cells?.[k] || '';
        if (c.type === 'text') return ri === 0 && headRow ? `<th>${esc(c.text || '')}</th>` : `<td class="${ci === 0 ? 'rowhead' : ''}">${esc(c.text || '')}</td>`;
        if (c.type === 'dropdown') return `<td><select class="hoa-select" data-cell="${k}" ${dis}><option value=""></option>${c.options.map(o => `<option ${o === v ? 'selected' : ''}>${esc(o)}</option>`).join('')}</select></td>`;
        return `<td><textarea class="hoa-input" rows="1" data-cell="${k}" ${NO_SPELL} ${reading ? 'readonly' : ''}></textarea></td>`;
      }).join('')}</tr>`).join('')}</tbody></table>`;
    }
    case 'DRAWING_V2':
      return `${(s.background_images || []).length ? `<div class="bg-images">${s.background_images.map(x => imgBox(base + x)).join('')}</div>` : ''}
        <div class="drawing-host" id="draw-${i}"><p class="drawing-msg">${reading ? 'The drawing tool opens when reading time ends.' : 'Loading drawing tool…'}</p></div>`;
    case 'CODING':
      if (isPython(p)) return `<div class="python-item"><div class="code-editor dark"><div class="gutter"></div><textarea class="code" id="ta-${i}" wrap="off" ${NO_SPELL} placeholder="# Input code" ${reading ? 'readonly' : ''}></textarea></div><pre class="python-console" id="out-${i}"># Output</pre></div>`;
      return `<div class="code-editor"><div class="gutter"></div><textarea class="code" id="ta-${i}" wrap="off" ${NO_SPELL} ${reading ? 'readonly' : ''}></textarea></div>`;
    case 'SQL':
      return `${s.dataset_setup_sql ? `<details class="dataset"><summary>Dataset (setup SQL)</summary><pre><code>${esc(s.dataset_setup_sql)}</code></pre></details>` : ''}
        <div class="sql-panel"><div class="sql-tab">Query</div><div class="code-editor"><div class="gutter"></div><textarea class="code" id="ta-${i}" wrap="off" ${NO_SPELL} ${reading ? 'readonly' : ''}></textarea></div>
        <div class="sql-results" id="out-${i}">No results to display</div></div>`;
    default:
      return `${ckeHtml(`ta-${i}`, reading)}<div class="word-count" id="wcount-${i}"></div>`;
  }
}
function ckeHtml(id, reading) {
  const b = (cmd, icon, title) => `<button type="button" class="cke-btn" data-cmd="${cmd}" title="${title}" tabindex="-1" ${reading ? 'disabled' : ''}>${icon}</button>`;
  return `<div class="cke"><div class="cke-top">
    <span class="cke-group">${b('bullet', '<i class="fas fa-list-ul"></i>', 'Insert/Remove Bulleted List')}${b('number', '<i class="fas fa-list-ol"></i>', 'Insert/Remove Numbered List')}</span>
    <span class="cke-group">${b('cut', '<i class="fas fa-cut"></i>', 'Cut')}${b('copy', '<i class="far fa-copy"></i>', 'Copy')}${b('paste', '<i class="fas fa-paste"></i>', 'Paste')}</span>
    <span class="cke-group">${b('undo', '<i class="fas fa-undo"></i>', 'Undo')}${b('redo', '<i class="fas fa-redo"></i>', 'Redo')}</span>
    <span class="cke-group">${b('special', '<span class="omega">Ω</span>', 'Insert Special Character')}</span>
  </div><textarea class="answer" id="${id}" ${NO_SPELL} ${reading ? 'readonly' : ''}></textarea><div class="cke-bottom"></div></div>`;
}
function itemButtons(p, i, multi) {
  const b = (act, label) => `<button class="nsw-button nsw-button--dark" data-act="${act}" data-i="${i}">${label}</button>`;
  let h = '';
  if (p.type === 'DRAWING_V2') h += b('full', 'Full screen') + b('reset-draw', 'Reset');
  else if (p.type === 'CODING') h += b('full', 'Full screen') + (isPython(p) ? b('run-py', 'Run') : '');
  else if (p.type === 'SQL') h += b('full', 'Full screen') + b('run-sql', 'Run') + b('reset-db', 'Reset DB');
  if (multi) h += `<button class="nsw-button nsw-button--dark-outline" data-act="hide" data-i="${i}">${ui.hidden[p.part_id] ? 'show <i class="fas fa-angle-down"></i>' : 'hide <i class="fas fa-angle-up"></i>'}</button>`;
  return h ? `<div class="item-buttons">${h}</div>` : '';
}

let drawRoots = [];
function renderQuestion() {
  const content = document.getElementById('content');
  if (!content || !groups.length || attempt.mode === 'pdf') return;
  drawRoots.forEach(r => { try { r.unmount(); } catch {} }); drawRoots = [];
  const { q, idx } = groups[attempt.current];
  const reading = inReading();
  const total = q.parts.reduce((t, p) => t + (p.marks || 0), 0);
  const multi = q.parts.length > 1;
  const title = `<div class="item-title"><h3>Question ${esc(q.number)} ${marksText(total)}</h3></div>`;
  const items = q.parts.map((p, i) => `<div class="feature left-stripe item${ui.hidden[p.part_id] ? ' item-hidden' : ''}" data-i="${i}">
      <div class="item-header">${itemButtons(p, i, multi)}
        <div class="item-question hl" data-hl="prompt-${i}">${multi ? `<div class="q-sub"><span class="q-label">${esc(partLabel(p))}</span><div class="q-text">${md(withMarks(p.prompt, p.marks))}</div></div>` : md(p.prompt)}</div></div>
      <div class="item-control type-${p.type === 'SHORT' || !p.type ? 'short' : p.type.toLowerCase()}">${itemControlHtml(p, i, reading)}</div>${attempt.liveMark && !reading ? liveHtml(p, i) : ''}${notesHtml(p)}</div>`).join('');
  const last = idx === groups.length - 1;
  const actions = `<div class="action-bar-wrapper"><div class="action-bar">
      <button class="nsw-button nsw-button--dark-outline" id="prev" ${idx === 0 ? 'disabled' : ''}><i class="fa fa-angle-left left-side"></i>Previous question</button>
      ${!last ? '<button class="nsw-button nsw-button--dark" id="next">Next question <i class="fa fa-angle-right"></i></button>' : reading ? '' : '<button class="nsw-button nsw-button--dark" id="exit-exam">Exit exam <i class="fas fa-sign-out-alt"></i></button>'}
    </div></div>`;
  const wide = q.parts.some(p => ['CODING', 'SQL', 'DRAWING_V2', 'RICH_TABLE'].includes(p.type));
  content.innerHTML = q.stimulus
    ? `<div class="item-group-wrapper item-group-two-col${wide ? ' bigger-right' : ''}"><div class="col col-left">${title}<div class="itemgroup-intro hl" data-hl="stim">${md(q.stimulus)}</div></div><div class="col col-right">${items}${actions}</div></div>`
    : `<div class="item-group-wrapper item-group-one-col">${title}${items}${actions}</div>`;
  restoreHighlights(content);
  $$('.col, .item-group-one-col', content).forEach(c => c.scrollTop = 0);

  $('#prev').onclick = () => go(idx - 1);
  if ($('#next')) $('#next').onclick = () => go(idx + 1);
  if ($('#exit-exam')) $('#exit-exam').onclick = finishModal;
  q.parts.forEach((p, i) => bindItem(p, i, $(`.item[data-i="${i}"]`, content), reading));
}

// ---- live marking: Check answer → key, explanation, strategy → Accept ----
const liveCache = {};
function liveHtml(p, i) {
  const ck = attempt.checked?.[p.part_id];
  if (!ck) return `<div class="live-check"><button type="button" class="nsw-button nsw-button--dark live-btn" data-live="check">Check answer <i class="fas fa-check"></i></button></div>`;
  return `<div class="live-check live-done ${ck.correct === true ? 'is-right' : ck.correct === false ? 'is-wrong' : ''}" id="live-${i}"><p class="live-loading">Loading…</p></div>`;
}
async function fetchKey(p) {
  return liveCache[p.part_id] ||= await api(`/api/check?folder=${encodeURIComponent(exam.folder)}&part=${encodeURIComponent(p.part_id)}`);
}
function bindLive(p, i, el) {
  const btn = $('[data-live="check"]', el);
  if (btn) btn.onclick = async () => {
    const a = attempt.answers[p.part_id] || {};
    const empty = p.type === 'MULTI_CHOICE' ? !(a.letters || []).length : p.type === 'OBJECTIVE_RESPONSE' ? !(a.rows || []).some(Boolean) : !(a.text || '').trim();
    if (empty && !(await askConfirm('You haven’t answered yet. Check anyway? Your answer will be locked.', 'Check anyway', 'Keep answering'))) return;
    const key = await fetchKey(p);
    let correct = null;
    if (p.type === 'MULTI_CHOICE' && key.correct_letters) correct = [...(a.letters || [])].sort().join() === [...key.correct_letters].sort().join();
    if (p.type === 'OBJECTIVE_RESPONSE' && key.rows) correct = key.rows.every((r, ri) => r.correct.includes(a.rows?.[ri]));
    (attempt.checked ||= {})[p.part_id] = { atMs: workMs(), correct };
    save(); renderNav(); renderQuestion();
  };
  const box = $(`#live-${i}`, el);
  if (box) fetchKey(p).then(key => fillLive(p, i, el, box, key)).catch(() => { box.innerHTML = '<p>Could not load the answer. Is the server running?</p>'; });
}
function fillLive(p, i, el, box, key) {
  const ck = attempt.checked[p.part_id], a = attempt.answers[p.part_id] || {}, ex = key.explanation || {};
  const yours = a.letters || [];
  if (p.type === 'MULTI_CHOICE' && key.correct_letters) $$('[data-opt]', el).forEach(inp => {
    const L = inp.dataset.opt, tr = inp.closest('tr');
    tr.classList.toggle('opt-correct', key.correct_letters.includes(L));
    tr.classList.toggle('opt-wrong', yours.includes(L) && !key.correct_letters.includes(L));
  });
  if (p.type === 'OBJECTIVE_RESPONSE' && key.rows) $$('[data-or]', el).forEach(inp => {
    const ok = key.rows[+inp.dataset.or].correct.includes(inp.value);
    inp.closest('td').classList.toggle('opt-correct', ok);
    inp.closest('td').classList.toggle('opt-wrong', inp.checked && !ok);
  });
  const H = [];
  if (ck.correct === true) H.push(`<p class="live-verdict">✅ Correct</p>`);
  else if (ck.correct === false) H.push(`<p class="live-verdict">❌ Not quite. The answer is <b>${esc((key.correct_letters || []).join(', ') || 'shown in green')}</b>.</p>`);
  else H.push('<p class="live-verdict">Compare your answer with the marking criteria and sample answer below.</p>');
  if (ex.key_check && ex.key_check !== 'ok') H.push(`<p class="live-warn">⚠ The answer key may be ${esc(ex.key_check)}: ${esc(ex.key_note || '')}</p>`);
  if (ex.correct) H.push(`<p><b>Why:</b> ${esc(ex.correct)}</p>`);
  if (ck.correct === false && ex.options) {
    const show = [...new Set([...yours, ...(key.correct_letters || [])])].sort();
    H.push('<ul class="live-opts">' + show.map(L => ex.options[L] ? `<li><b>${esc(L)}</b> ${yours.includes(L) ? '(your choice)' : '(correct)'}: ${esc(ex.options[L])}</li>` : '').join('') + '</ul>');
  }
  if (ck.correct === false && ex.strategy) H.push(`<p class="live-strategy"><b>Strategy:</b> ${esc(ex.strategy)}</p>`);
  if (ck.correct === false && !ex.correct && p.type === 'MULTI_CHOICE') H.push('<p class="muted">No written explanation for this one yet; add a note below if you want one.</p>');
  if (key.criteria?.length) H.push('<p><b>Marking criteria</b></p><ul>' + key.criteria.map(c => `<li>[${esc(c.marks ?? '')}] ${esc(c.criterion)}</li>`).join('') + '</ul>');
  if (key.rubric) H.push(`<div><b>Marking rubric</b>${md(key.rubric)}</div>`);
  if (key.guidance) H.push(`<div><b>Marking guidance</b>${md(key.guidance)}</div>`);
  if (key.sample_answer && p.type !== 'MULTI_CHOICE') H.push(`<div class="live-sample"><b>Sample answer</b>${md(key.sample_answer)}</div>`);
  const last = attempt.current === groups.length - 1 && i === groups[attempt.current].q.parts.length - 1;
  H.push(`<button type="button" class="nsw-button nsw-button--dark" data-live="accept">${last ? 'Accept and finish' : 'Accept'} <i class="fa fa-angle-right"></i></button>`);
  box.innerHTML = H.join('');
  $('[data-live="accept"]', box).onclick = () => {
    const q = groups[attempt.current].q;
    if (i < q.parts.length - 1) return $(`.item[data-i="${i + 1}"]`)?.scrollIntoView({ behavior: 'smooth' });
    if (attempt.current < groups.length - 1) return go(attempt.current + 1);
    return exam.drill ? finishDrill() : finishModal();
  };
}

// "Notes for Claude": quick self-assessment tags + free text per question. Not part of the answer.
const NOTE_TAGS = ['Guessed', 'Not sure', 'Confused between options', "Didn't understand the question", "Haven't learnt this", 'Key looks wrong'];
function notesHtml(p) {
  const n = attempt.notes?.[p.part_id] || {};
  return `<details class="claude-notes"${n.text || n.tags?.length ? ' open' : ''}><summary>Notes for Claude <span>(not part of the exam)</span></summary>
    <div class="note-tags">${NOTE_TAGS.map(t => `<button type="button" class="note-tag${n.tags?.includes(t) ? ' on' : ''}" data-tag="${esc(t)}">${esc(t)}</button>`).join('')}</div>
    <input type="text" class="note-text" placeholder="e.g. mixed up B and C, forgot what DAST means…" value="${esc(n.text || '')}" ${NO_SPELL}></details>`;
}
function bindNotes(p, el) {
  const box = $('.claude-notes', el);
  if (!box) return;
  const get = () => (attempt.notes ||= {})[p.part_id] ||= { tags: [], text: '' };
  $$('.note-tag', box).forEach(b => b.onclick = () => {
    const n = get(), t = b.dataset.tag;
    n.tags = n.tags.includes(t) ? n.tags.filter(x => x !== t) : [...n.tags, t];
    b.classList.toggle('on', n.tags.includes(t));
    save();
  });
  $('.note-text', box).oninput = e => { get().text = e.target.value; save(); };
}

function bindItem(p, i, el, reading) {
  bindNotes(p, el);
  bindLive(p, i, el);
  const s = p.question;
  const a = attempt.answers[p.part_id] || {};
  const set = v => {
    if (attempt.checked?.[p.part_id]) return;   // locked after live checking
    if ('text' in v) logKeys(p.part_id, attempt.answers[p.part_id]?.text ?? (s.starter_code || s.starter_query || ''), v.text ?? '');
    attempt.answers[p.part_id] = { ...(attempt.answers[p.part_id] || {}), ...v, overtime: !!attempt.timeUpAt || undefined }; noteTyping(p.part_id); save(); renderNav();
  };

  $$('[data-act]', el).forEach(b => b.onclick = () => itemAction(b.dataset.act, p, i, el));
  $$('[data-opt]', el).forEach(inp => inp.onchange = () => {
    if (inReading()) return;
    set({ letters: $$('[data-opt]', el).filter(x => x.checked).map(x => x.dataset.opt).sort() });
  });
  $$('[data-or]', el).forEach(inp => inp.onchange = () => {
    const rows = [...(attempt.answers[p.part_id]?.rows || [])];
    rows[+inp.dataset.or] = inp.value; set({ rows });
  });
  $$('[data-cell]', el).forEach(c => {
    if (c.tagName === 'TEXTAREA') { c.value = a.cells?.[c.dataset.cell] || ''; autoGrow(c); }
    c.oninput = c.onchange = () => { if (c.tagName === 'TEXTAREA') autoGrow(c); set({ cells: { ...(attempt.answers[p.part_id]?.cells || {}), [c.dataset.cell]: c.value } }); };
  });
  const ta = $(`#ta-${i}`, el);
  if (ta) {
    ta.value = a.text ?? (s.starter_code || s.starter_query || '');
    const wcEl = $(`#wcount-${i}`, el);
    const upd = () => {
      if (!wcEl) return;
      const n = wc(ta.value);
      const target = s.word_limit || (attempt.showTargets && p.marks ? p.marks * 35 : null);
      wcEl.textContent = target ? `${n} / ${target} words` : `${n} word${n === 1 ? '' : 's'}`;
      wcEl.classList.toggle('over', !!(s.word_limit && n > s.word_limit));
    };
    upd();
    if (ta.classList.contains('answer')) { autoGrow(ta); bindCke(ta, el); }
    else bindCode(ta);
    ta.addEventListener('input', () => { set({ text: ta.value }); upd(); if (ta.classList.contains('answer')) autoGrow(ta); });
  }
  if (p.type === 'DRAWING_V2' && !reading) mountDrawing(p, i, a);
}
function autoGrow(t) { t.style.height = 'auto'; t.style.height = Math.max(t.scrollHeight + 2, 0) + 'px'; }

// code editors: line-number gutter + Tab inserts spaces
function bindCode(ta) {
  const gutter = ta.parentElement.querySelector('.gutter');
  const draw = () => { const n = ta.value.split('\n').length; gutter.textContent = Array.from({ length: n }, (_, k) => k + 1).join('\n'); gutter.scrollTop = ta.scrollTop; };
  draw();
  ta.addEventListener('input', draw);
  ta.addEventListener('scroll', () => { gutter.scrollTop = ta.scrollTop; });
  ta.addEventListener('keydown', e => {
    if (e.key === 'Tab' && !ta.readOnly) {
      e.preventDefault();
      if (!document.execCommand('insertText', false, '    ')) { ta.setRangeText('    ', ta.selectionStart, ta.selectionEnd, 'end'); ta.dispatchEvent(new Event('input')); }
    }
  });
}

// CKEditor-like toolbar (plain-text versions of the tools)
const SPECIAL = '≤ ≥ ≠ ≈ ± × ÷ → ← ↔ ⇒ ↑ ↓ ° π √ ∞ Σ ∆ µ Ω α β θ λ • – — … ‘ ’ “ ” © ® ™ € £ ¥ ½ ¼ ¾ ² ³ ∴ ∈ ∉ ∪ ∩ ⊂ ∧ ∨ ¬ ⊕'.split(' ');
function insertText(ta, str) {
  ta.focus();
  if (!document.execCommand('insertText', false, str)) { ta.setRangeText(str, ta.selectionStart, ta.selectionEnd, 'end'); ta.dispatchEvent(new Event('input')); }
}
function bindCke(ta, el) {
  $$('.cke-btn', ta.closest('.cke')).forEach(b => b.onmousedown = e => e.preventDefault());
  $$('.cke-btn', ta.closest('.cke')).forEach(b => b.onclick = async e => {
    if (ta.readOnly) return;
    const cmd = b.dataset.cmd;
    ta.focus();
    if (cmd === 'bullet' || cmd === 'number') {
      const v = ta.value, st = v.lastIndexOf('\n', ta.selectionStart - 1) + 1;
      let en = v.indexOf('\n', ta.selectionEnd); if (en < 0) en = v.length;
      const lines = v.slice(st, en).split('\n');
      const re = cmd === 'bullet' ? /^• / : /^\d+\. /;
      const off = lines.every(l => re.test(l));
      const out = lines.map((l, k) => off ? l.replace(re, '') : (cmd === 'bullet' ? '• ' : `${k + 1}. `) + l.replace(/^(• |\d+\. )/, '')).join('\n');
      ta.setSelectionRange(st, en); insertText(ta, out);
    } else if (cmd === 'cut' || cmd === 'copy') document.execCommand(cmd);
    else if (cmd === 'paste') { try { insertText(ta, await navigator.clipboard.readText()); } catch { openModal('<p>Use command-V (Mac) or control-V (Windows) to paste.</p>', { closable: true }); } }
    else if (cmd === 'undo' || cmd === 'redo') document.execCommand(cmd);
    else if (cmd === 'special') {
      $('.special-chars')?.remove();
      const pop = document.createElement('div');
      pop.className = 'special-chars';
      pop.innerHTML = SPECIAL.map(c => `<button type="button" title="${c}">${c}</button>`).join('');
      const r = b.getBoundingClientRect();
      pop.style.left = (r.left + window.scrollX) + 'px'; pop.style.top = (r.bottom + window.scrollY + 4) + 'px';
      pop.style.position = 'fixed'; pop.style.left = r.left + 'px'; pop.style.top = (r.bottom + 4) + 'px';
      document.body.appendChild(pop);
      $$('button', pop).forEach(x => { x.onmousedown = ev => ev.preventDefault(); x.onclick = () => { insertText(ta, x.textContent); pop.remove(); }; });
      setTimeout(() => document.addEventListener('mousedown', function off(ev) { if (!pop.contains(ev.target)) { pop.remove(); document.removeEventListener('mousedown', off); } }), 0);
    }
  });
}

// per-item buttons: hide/show, Full screen, Run (Python / SQL), Reset DB, Reset drawing
const sqlDbs = {};
let pyodideP = null, sqlP = null;
async function itemAction(act, p, i, el) {
  if (act === 'hide') { ui.hidden[p.part_id] = !ui.hidden[p.part_id]; el.classList.toggle('item-hidden', ui.hidden[p.part_id]); $('[data-act="hide"]', el).innerHTML = ui.hidden[p.part_id] ? 'show <i class="fas fa-angle-down"></i>' : 'hide <i class="fas fa-angle-up"></i>'; return; }
  if (act === 'full') {
    const on = el.classList.toggle('item-fullscreen');
    $('[data-act="full"]', el).textContent = on ? 'Exit full screen' : 'Full screen';
    setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
    return;
  }
  if (act === 'run-py') return runPython($(`#ta-${i}`, el).value, $(`#out-${i}`, el));
  if (act === 'run-sql') return runSql(p, $(`#ta-${i}`, el).value, $(`#out-${i}`, el));
  if (act === 'reset-db') { delete sqlDbs[p.part_id]; $(`#out-${i}`, el).textContent = 'Database reset. No results to display'; return; }
  if (act === 'reset-draw') {
    if (inReading() || !(await askConfirm('Clear your drawing for this question?', 'Clear drawing'))) return;
    const api = drawApis[p.part_id];
    if (api) api.updateScene({ elements: [] });
  }
}
async function runPython(code, out) {
  out.textContent = 'Loading Python…';
  try {
    if (!pyodideP) pyodideP = addScript('https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js').then(() => loadPyodide());
    const py = await pyodideP;
    out.textContent = '';
    const dec = new TextDecoder();
    const write = buf => { out.textContent += dec.decode(buf, { stream: true }); out.scrollTop = out.scrollHeight; return buf.length; };
    py.setStdout({ write }); py.setStderr({ write });
    py.setStdin({ stdin: () => { const lastLine = out.textContent.split('\n').pop(); const v = prompt(lastLine || 'Input:'); if (v == null) return null; out.textContent += v + '\n'; return v + '\n'; }, autoEOF: true });
    const g = py.globals.get('dict')();
    await py.runPythonAsync(code, { globals: g });
    g.destroy();
  } catch (e) {
    if (!window.loadPyodide) { pyodideP = null; out.textContent = 'Could not load Python (needs internet).'; return; }
    const sp = document.createElement('span');
    sp.className = 'err';
    // show the traceback from the student's code only
    sp.textContent = (out.textContent && !out.textContent.endsWith('\n') ? '\n' : '') + String(e.message || e).replace(/^[\s\S]*?(?=File "<exec>")/, 'Traceback (most recent call last):\n  ');
    out.appendChild(sp);
  }
}
async function runSql(p, query, out) {
  out.textContent = 'Loading…';
  try {
    if (!sqlP) sqlP = addScript('https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.js').then(() => initSqlJs({ locateFile: f => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/${f}` }));
    const SQL = await sqlP;
    if (!sqlDbs[p.part_id]) { const db = new SQL.Database(); if (p.question.dataset_setup_sql) db.exec(p.question.dataset_setup_sql); sqlDbs[p.part_id] = db; }
    const res = sqlDbs[p.part_id].exec(query);
    if (!res.length) { out.textContent = 'No results to display'; return; }
    const r = res[res.length - 1];
    out.innerHTML = `<table><thead><tr>${r.columns.map(c => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${r.values.map(v => `<tr>${v.map(x => `<td>${esc(x)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  } catch (e) {
    if (!window.initSqlJs) { sqlP = null; out.textContent = 'Could not load the SQL engine (needs internet).'; return; }
    out.innerHTML = `<span class="err">${esc(e.message || e)}</span>`;
  }
}

const drawApis = {};
// NESA's own Software Engineering shape library (process, data store, external entity, data flow,
// structure-chart data/control pointers, sub-program, decision, repetition, class boxes, flowchart shapes),
// extracted from the HSC familiarisation app's drawing tool.
let nesaLibrary = null;
const loadNesaLibrary = () => nesaLibrary ||= fetch('/nesa/se-library.excalidrawlib').then(r => r.json()).then(j => j.libraryItems || []).catch(() => []);
async function mountDrawing(p, i, a) {
  try { await loadExcalidraw(); } catch { const h = document.getElementById(`draw-${i}`); if (h) h.innerHTML = '<p class="drawing-msg">Could not load the drawing tool (needs internet).</p>'; return; }
  const host = document.getElementById(`draw-${i}`);
  if (!host || attempt?.mode !== 'structured' || groups[attempt.current]?.q.parts[i] !== p) return;
  host.innerHTML = '';
  let t = null, pngT = null;
  const onChange = (elements, appState, files) => {
    clearTimeout(t);
    t = setTimeout(() => {
      const live = elements.filter(e => !e.isDeleted);
      const prev = attempt.answers[p.part_id]?.elements || [];
      if (!live.length && !prev.length) return;
      attempt.answers[p.part_id] = { elements: JSON.parse(JSON.stringify(live)), files: files || {}, overtime: !!attempt.timeUpAt || undefined };
      save(); renderNav();
    }, 600);
    clearTimeout(pngT);
    pngT = setTimeout(async () => {
      const live = elements.filter(e => !e.isDeleted);
      if (!live.length) return;
      const blob = await ExcalidrawLib.exportToBlob({ elements: live, files, mimeType: 'image/png', appState: { exportBackground: true, viewBackgroundColor: '#fff' } });
      pendingPngs[p.part_id] = await new Promise(r => { const fr = new FileReader(); fr.onload = () => r(fr.result); fr.readAsDataURL(blob); });
      save();
    }, 2500);
  };
  const libraryItems = await loadNesaLibrary();
  const root = ReactDOM.createRoot(host);
  drawRoots.push(root);
  root.render(React.createElement(ExcalidrawLib.Excalidraw, {
    initialData: { elements: a.elements || [], files: a.files || {}, libraryItems, appState: { viewBackgroundColor: '#ffffff', openSidebar: { name: 'default', tab: 'library' } } },
    excalidrawAPI: api => { drawApis[p.part_id] = api; },
    onChange,
  }));
}

// ---------- rest breaks ("Take a break") ----------
function pause() {
  if (isPaused() || !canRest()) return;
  attempt.pauses = [...(attempt.pauses || []), { start: Date.now() }];
  save(true);
  showBreakScreen();
}
function showBreakScreen() {
  closeModal();
  const header = $('.header-test');
  const o = document.createElement('div');
  o.className = 'break-screen';
  o.id = 'break-screen';
  o.style.top = (header ? header.getBoundingClientRect().height : 54) + 'px';
  o.innerHTML = `<div class="feature"><h2>You are currently resting. Please click "CONTINUE" to resume test.</h2>
      <p class="break-time" id="rest-time"></p><p class="muted" id="rest-note"></p></div>
    <p style="text-align:center;margin-top:1.5em"><button class="nsw-button nsw-button--dark" id="resume" name="continue">CONTINUE <i aria-hidden="true" class="fa fa-angle-right"></i></button></p>`;
  document.body.appendChild(o);
  $('#break-box')?.classList.add('hidden');
  const cur = attempt.pauses.find(p => !p.end);
  const btn = $('#resume', o);
  btn.disabled = false;
  const before = hasAllowance() ? attempt.rest.allowanceMs - (restChargedMs() - (Date.now() - cur.start)) : Infinity; // allowance left when this break began
  const finish = () => {
    if (cur.end) return;
    cur.end = Math.min(Date.now(), cur.start + before);
    clearInterval(iv); o.remove(); save(true); updateTimer();
  };
  const show = () => {
    const took = Date.now() - cur.start;
    $('#rest-time', o).textContent = hasAllowance() ? `Rest time left: ${hms(Math.max(0, before - took))}` : `Break: ${hms(took)}`;
    $('#rest-note', o).textContent = 'The timer is paused and the questions are hidden.' +
      (hasAllowance() && took < REST_MIN_MS ? ` A break uses at least 5 minutes of rest time: if you continue now, ${hms(REST_MIN_MS)} is taken from your rest time.` : '');
    if (hasAllowance() && took >= before) finish(); // rest time used up: back to the exam
  };
  const iv = setInterval(show, 500);
  show();
  btn.onclick = finish;
}

// ---------- finish / submit ----------
async function finishExam() {
  closeModal();
  const m = openModal(`<p>The exam is now finished.</p><p id="submit-status">Submitting responses. Please wait.</p>
    <button class="nsw-button nsw-button--dark" id="close-exam" style="margin:auto;display:block" disabled>CLOSE</button>`);
  trackTime();
  attempt.submittedAt = new Date().toISOString();
  attempt.timeUsedMs = Math.max(0, usedMs() - attempt.readingMs);
  clearInterval(tick);
  await doSave();
  const ok = !$('#save-state')?.textContent;
  if (ok && exam?.drill) { closeModal(); home(); return; }
  $('#submit-status', m).innerHTML = ok ? 'Your responses have been submitted.' : '<strong>Your responses could not be saved. Check the server is running, then click CLOSE to retry.</strong>';
  const btn = $('#close-exam', m);
  btn.disabled = false;
  btn.onclick = async () => { if (!ok) { await doSave(); } closeModal(); submittedPage(); };
}
function submittedPage() {
  const a = attempt;
  groups = [];
  $app.innerHTML = `<div class="test-container">
    <header class="header-test"><div class="margin-wrapper"><div class="header-container"><div class="header-test-title">${esc(a.title)}</div></div></div></header>
    <div class="nav-bar"><div class="margin-wrapper"><div class="nav-bar-inner"><div class="nav-wrapper"></div><div id="toolbar"></div></div></div></div>
    <div class="content test-content begin-content"><div class="feature left-stripe" style="max-width:860px">
      <h2>Your responses have been submitted.</h2>
      <p>Your answers are saved to <code>~/gradeo/papers/attempts/${esc(a.id)}.md</code>.</p>
      <p>Tell Claude: <b>"mark my attempt"</b>.</p>
      <p>Time used: ${hms(a.timeUsedMs)} · Rest breaks: ${(a.pauses || []).length} (${hms((a.pauses || []).reduce((t, p) => t + ((p.end || Date.now()) - p.start), 0))})</p>
      <div class="action-bar"><a class="nsw-button nsw-button--dark-outline" href="/papers/attempts/${encodeURIComponent(a.id)}.md" target="_blank">View answers file</a><button class="nsw-button nsw-button--dark" id="back">Back to menu <i class="fa fa-angle-right"></i></button></div>
    </div></div><footer class="test-footer"></footer></div>`;
  renderToolbar({ font: true, colour: true, info: false });
  document.getElementById('back').onclick = home;
}

// ---------- PDF / free answer sheet ----------
function startPdf(cfg) {
  beginScreen({
    title: cfg.title, readingMs: cfg.readingMs,
    instructions: [cfg.readingMs ? `Reading time – ${durWords(cfg.readingMs / 60000)}` : 'No reading time', `Working time – ${durWords(cfg.durationMinutes)}`,
      restInfo(cfg.restPer, cfg.readingMs, cfg.durationMinutes), cfg.pdf ? 'The paper is shown on the left; answer on the right' : 'Read the paper elsewhere; type your answers here', 'Spell-check is turned off', 'Your responses are saved automatically'],
    structure: cfg.pdf ? `<h3>${esc(cfg.title)}</h3><p>Multiple-choice answer grid for ${cfg.mcCount} questions, then answer boxes for the written questions.</p>` : `<h3>Free answer sheet</h3><p>Add one answer box per question.</p>`,
    onStart: () => {
      attempt = { id: `${stamp()}_${slug(cfg.title)}`, mode: 'pdf', pdf: cfg.pdf, title: cfg.title, startedAt: new Date().toISOString(),
        durationMinutes: cfg.durationMinutes, readingMs: cfg.readingMs, showTargets: cfg.showTargets, mcCount: cfg.mcCount,
        rest: { perHalfHour: cfg.restPer, allowanceMs: restAllowanceMs(cfg.restPer, cfg.readingMs, cfg.durationMinutes) },
        pauses: [], mc: {}, written: [{ label: '', marks: null, text: '' }] };
      save(true);
      runPdf();
    },
  });
}

function runPdf() {
  groups = [];
  $app.innerHTML = chromeHtml(attempt.title, { nav: false });
  renderToolbar({ font: true, colour: true, info: true });
  $('#content').innerHTML = attempt.pdf
    ? `<div class="pdf-two-col"><iframe src="/papers/${encodeURIComponent(attempt.pdf)}#view=FitH" title="Exam paper"></iframe><div class="pdf-answers" id="answers"></div></div>`
    : `<div class="pdf-answers"><div class="pdf-one-col" id="answers"></div></div>`;
  renderPdfAnswers(); renderBanner();
  startClock();
}

function renderPdfAnswers() {
  const box = document.getElementById('answers');
  const n = attempt.mcCount || 0;
  const reading = inReading();
  box.innerHTML = `
    ${attempt.pdf && n ? `<div class="item-title"><h3>Section I – Multiple choice</h3></div><div class="feature left-stripe item"><div class="mc-grid">${Array.from({ length: n }, (_, i) => i + 1).map(i => `<div class="mc-row"><b>${i}</b>${'ABCD'.split('').map(L => `<label><input type="radio" name="mc${i}" data-mc="${i}" value="${L}" ${attempt.mc[i] === L ? 'checked' : ''} ${reading ? 'disabled' : ''}>${L}</label>`).join('')}</div>`).join('')}</div></div>` : ''}
    <div class="item-title" style="margin-top:20px"><h3>${attempt.pdf ? 'Written answers' : 'Answers'}</h3></div>
    <div id="wlist"></div>
    <div class="action-bar-wrapper"><div class="action-bar"><button class="nsw-button nsw-button--dark-outline" id="addw">+ Add answer box</button>
      ${reading ? '' : '<button class="nsw-button nsw-button--dark" id="exit-exam">Exit exam <i class="fas fa-sign-out-alt"></i></button>'}</div></div>`;
  $$('[data-mc]', box).forEach(r => {
    r.onclick = () => {
      if (inReading()) return;
      const i = r.dataset.mc;
      if (attempt.mc[i] === r.value) { r.checked = false; delete attempt.mc[i]; } else attempt.mc[i] = r.value;
      save();
    };
  });
  const list = document.getElementById('wlist');
  const draw = () => {
    list.innerHTML = '';
    attempt.written.forEach((w, i) => {
      const d = document.createElement('div');
      d.className = 'feature left-stripe item';
      d.innerHTML = `<div class="wblock-head"><input type="text" placeholder="Question (e.g. 21 a)" value="${esc(w.label)}" ${NO_SPELL}><label>Marks <input type="number" min="0" value="${w.marks ?? ''}"></label><button class="nsw-button nsw-button--dark-outline nsw-button--small" title="Remove">Remove</button></div>
        ${ckeHtml(`w-${i}`, reading)}<div class="word-count"></div>`;
      const [label, marks] = $$('input', d);
      const ta = $('textarea', d), wcEl = $('.word-count', d);
      ta.value = w.text || '';
      const upd = () => { const t = attempt.showTargets && w.marks ? w.marks * 35 : null; const k = wc(ta.value); wcEl.textContent = t ? `${k} / ${t} words` : `${k} word${k === 1 ? '' : 's'}`; };
      upd();
      label.oninput = () => { w.label = label.value; save(); };
      marks.oninput = () => { w.marks = +marks.value || null; upd(); save(); };
      ta.addEventListener('input', () => { w.text = ta.value; if (attempt.timeUpAt) w.overtime = true; upd(); autoGrow(ta); save(); });
      $('.wblock-head button', d).onclick = async () => { if ((w.text || '').trim() && !(await askConfirm('Delete this answer?', 'Delete'))) return; attempt.written.splice(i, 1); save(); draw(); };
      list.appendChild(d);
      autoGrow(ta); bindCke(ta, d);
    });
  };
  draw();
  document.getElementById('addw').onclick = () => { attempt.written.push({ label: '', marks: null, text: '' }); save(); draw(); list.lastElementChild?.querySelector('input').focus(); };
  if ($('#exit-exam', box)) $('#exit-exam', box).onclick = finishModal;
}

home();
