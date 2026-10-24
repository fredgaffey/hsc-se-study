// Downloads raw Gradeo data for every exam session into gradeo_out/raw/ using ONE Chrome connection
// (one "Allow" click). If bridge.mjs is already running it is used instead, so no click at all.
import fs from 'node:fs';
import { gradeoPage, api as pageApi } from './lib.mjs';

const OUT = 'gradeo_out/raw';
fs.mkdirSync(OUT, { recursive: true });

let api, browser;
const bridgeUp = await fetch('http://127.0.0.1:7777/api/user/authenticated').then(r => r.ok).catch(() => false);
if (bridgeUp) {
  console.log('Using running bridge');
  api = async p => { const r = await fetch('http://127.0.0.1:7777/api/' + p); if (!r.ok) throw new Error((await r.text()).split('\n')[0]); return r.json(); };
} else {
  console.log('Connecting to Chrome (click Allow once)...');
  const g = await gradeoPage();
  browser = g.b;
  api = p => pageApi(g.pg, p);
}

const list = [];
for (let off = 0; ; off += 50) {
  const d = await api(`exam-process/session-participant?limit=50&offset=${off}`);
  list.push(...d.list);
  if (!d.list.length || list.length >= d.pgn.total) break;
}
fs.writeFileSync(`${OUT}/_sessions.json`, JSON.stringify(list, null, 1));
console.log(`${list.length} sessions`);

for (const x of list) {
  const id = x.markingSessionId;
  if (!id) continue;
  const r = { id, title: x.summary.title, fetched: new Date().toISOString() };
  for (const [k, p] of [['questions', 'question'], ['answers', 'question-part-aggregated-by-student'], ['state', 'state-participant']]) {
    try { r[k] = await api(`marking-session/${p}/${id}`); } catch (e) { r[k + '_error'] = String(e.message).slice(0, 120); }
  }
  fs.writeFileSync(`${OUT}/${id}.json`, JSON.stringify(r));
  console.log(`${r.questions ? '✓' : '·'} ${x.summary.title}${r.questions ? '' : '  (locked until results released)'}`);
}
// Disconnect only; never close the user's Chrome.
if (browser) await browser._connection?.close?.();
process.exit(0);
