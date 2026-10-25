// NESA Concerto paper JSON -> per-question markdown (raw/nesa_<x>.md + .parsed.json) for building bank entries.
import fs from 'node:fs';
import TurndownService from '/Users/fred/gradeo/node_modules/turndown/lib/turndown.cjs.js';
import { gfm } from '/Users/fred/gradeo/node_modules/turndown-plugin-gfm/lib/turndown-plugin-gfm.cjs.js';
const [, , inFile, outBase, prefix] = process.argv;
const d = JSON.parse(fs.readFileSync(inFile, 'utf8'));
const td = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced', bulletListMarker: '-' });
td.use(gfm);
td.remove(['style', 'script', 'button']);
td.addRule('inputs', { filter: n => n.nodeName === 'INPUT' || n.nodeName === 'TEXTAREA' || n.nodeName === 'SELECT',
  replacement: (_, n) => n.nodeName === 'SELECT' ? ` [dropdown: ${[...n.childNodes].filter(o => o.nodeName === 'OPTION').map(o => o.textContent.trim()).filter(Boolean).join(' / ')}] ` : n.getAttribute('type') === 'radio' ? ' ( ) ' : n.getAttribute('type') === 'checkbox' ? ' [ ] ' : ' [answer box] ' });
td.addRule('sortItem', { filter: n => n.nodeName === 'DIV' && n.getAttribute('data-id'), replacement: c => `\n- [sortable] ${c.trim()}\n` });
// list-style-type:'7 (a)' carries the question number
td.addRule('qnum', { filter: n => n.nodeName === 'UL' && /list-style-type/.test(n.getAttribute('style') || ''),
  replacement: (c, n) => { const m = (n.getAttribute('style') || '').match(/list-style-type:\s*'([^']*)'/); return `\n\n**${m ? m[1].replace(/ /g, ' ') : ''}** ${c.replace(/^\s*-\s*/, '').trim()}\n\n`; } });
td.addRule('codeBlock', { filter: n => n.nodeName === 'CODE' && /<br/i.test(n.innerHTML || ''),
  replacement: (_, n) => '\n```\n' + n.innerHTML.replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/\r/g, '').replace(/\n\s*\n/g, '\n').trim() + '\n```\n' });
const imgs = new Set();
const md = h => {
  if (!h) return '';
  h = h.replace(/\{\{media_url\}\}/g, '/bundles/concertopanel/files/protected/');
  h = h.replace(/src="\/bundles\/concertopanel\/files\/protected\/([^"]+)"/g, (_, f) => { imgs.add(f); return `src="assets/${prefix}${f}"`; });
  return td.turndown(h).replace(/ /g, ' ').replace(/\n{3,}/g, '\n\n').trim();
};
const p = d.params, qpg = JSON.parse(p.test.questionPresentationGroups), groups = p.state.itemGroups;
const out = [], L = [];
groups.forEach((g, i) => {
  const items = typeof g.items === 'string' ? JSON.parse(g.items) : g.items;
  const title = md((g.title || '').replace(/<button[\s\S]*?<\/button>/g, ''));
  const q = { n: i + 1, title, stimulus: md(g.stimulus), instructions: md(g.instructions), items: items.map(it => ({ id: it.id, md: md(it.question) })) };
  out.push(q);
  L.push(`\n\n======== GROUP ${i + 1}: ${title}\n` + (q.stimulus ? `--- STIMULUS\n${q.stimulus}\n` : '') + (q.instructions ? `--- INSTR\n${q.instructions}\n` : '') + q.items.map(x => `--- ITEM ${x.id}\n${x.md}`).join('\n'));
});
fs.writeFileSync(outBase + '.parsed.json', JSON.stringify({ title: p.test.title, groups: out, images: [...imgs] }, null, 1));
fs.writeFileSync(outBase + '.md', L.join('\n'));
console.log(out.length, 'groups', [...imgs]);
