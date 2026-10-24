// Holds ONE CDP connection to Chrome (one "Allow" click) and exposes it on http://127.0.0.1:7777
//   GET  /api/<path>          -> Gradeo API JSON (uses the logged-in tab's token)
//   POST /eval  body=JS expr  -> evaluated in the Gradeo tab, JSON result
//   POST /run   body=JS       -> body of an async function(pg, ctx, api, fs) run in Node, JSON result
import http from 'node:http';
import fs from 'node:fs';
import { gradeoPage, api } from './lib.mjs';
const { b, ctx, pg } = await gradeoPage();
b.on('disconnected', () => { console.log('Chrome disconnected'); process.exit(1); });
const read = req => new Promise(r => { let s = ''; req.on('data', d => s += d); req.on('end', () => r(s)); });
http.createServer(async (req, res) => {
  try {
    let out;
    if (req.url.startsWith('/api/')) out = await api(pg, req.url.slice(5));
    else if (req.url === '/eval') out = await pg.evaluate(await read(req));
    else if (req.url === '/run') out = await new (Object.getPrototypeOf(async function () {}).constructor)('pg', 'ctx', 'api', 'fs', await read(req))(pg, ctx, p => api(pg, p), fs);
    else { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify(out ?? null));
  } catch (e) { res.writeHead(500); res.end(String(e.message || e)); }
}).listen(7777, '127.0.0.1', () => console.log('bridge ready on 7777, tab:', pg.url()));
