import { connect } from './connect.mjs';
export async function gradeoPage() {
  const b = await connect();
  const ctx = b.contexts()[0];
  let pg = ctx.pages().find(p => p.url().startsWith('https://platform.gradeo.com.au/'));
  if (!pg) { pg = await ctx.newPage(); await pg.goto('https://platform.gradeo.com.au/', { waitUntil: 'networkidle' }); }
  return { b, ctx, pg };
}
export const api = (pg, path) => pg.evaluate(async p => {
  const k = Object.keys(localStorage).find(k => k.startsWith('@@auth0spajs@@') && k.includes('api.portal.gradeo.com.au'));
  const tok = k && JSON.parse(localStorage[k]).body?.access_token;
  if (!tok) throw new Error('No Gradeo login token in this tab - log in to platform.gradeo.com.au first');
  const r = await fetch('/api/' + p, { credentials: 'include', headers: { accept: 'application/json', authorization: 'Bearer ' + tok } });
  if (!r.ok) throw new Error(`${r.status} ${p}`);
  return r.json();
}, path);
export async function listSessions(pg) {
  const out = [];
  for (let off = 0; ; off += 50) {
    const d = await api(pg, `exam-process/session-participant?limit=50&offset=${off}`);
    out.push(...d.list);
    if (!d.list.length || out.length >= d.pgn.total) break;
  }
  return out;
}
