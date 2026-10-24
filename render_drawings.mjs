// Renders Excalidraw scenes (Gradeo DRAWING_V2 answers) to PNG in a private headless Chromium.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

function headlessShell() {
  const root = path.join(os.homedir(), 'Library/Caches/ms-playwright');
  const dirs = fs.readdirSync(root).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse();
  for (const d of dirs) for (const sub of fs.readdirSync(path.join(root, d))) {
    const exe = path.join(root, d, sub, 'chrome-headless-shell');
    if (fs.existsSync(exe)) return exe;
  }
  throw new Error('No Playwright headless Chromium found - run: npx playwright install chromium-headless-shell');
}

const HTML = `<!doctype html><html><head>
<script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script>window.EXCALIDRAW_ASSET_PATH = "https://unpkg.com/@excalidraw/excalidraw@0.17.6/dist/";</script>
<script src="https://unpkg.com/@excalidraw/excalidraw@0.17.6/dist/excalidraw.production.min.js"></script>
</head><body></body></html>`;

export async function makeRenderer() {
  const browser = await chromium.launch({ executablePath: headlessShell() });
  const page = await browser.newPage();
  await page.setContent(HTML, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.ExcalidrawLib?.exportToBlob, null, { timeout: 30000 });
  return {
    // data = { elements, files } as stored by Gradeo. Returns PNG Buffer or null if nothing drawn.
    async render(data) {
      const files = {};
      for (const [k, f] of Object.entries(data.files || {})) {
        let url = f.dataURL;
        if (url && !url.startsWith('data:')) {
          const r = await fetch(url);
          url = `data:${r.headers.get('content-type') || f.mimeType};base64,` + Buffer.from(await r.arrayBuffer()).toString('base64');
        }
        files[k] = { ...f, dataURL: url };
      }
      data = { ...data, files };
      const b64 = await page.evaluate(async data => {
        const elements = (data.elements || []).filter(e => !e.isDeleted);
        if (!elements.length) return null;
        const files = data.files;
        await document.fonts.ready;
        const blob = await ExcalidrawLib.exportToBlob({
          elements, files, mimeType: 'image/png', exportPadding: 20,
          appState: { exportBackground: true, viewBackgroundColor: '#ffffff', exportScale: 2 },
        });
        const buf = new Uint8Array(await blob.arrayBuffer());
        let s = ''; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode(...buf.subarray(i, i + 0x8000));
        return btoa(s);
      }, data);
      return b64 ? Buffer.from(b64, 'base64') : null;
    },
    close: () => browser.close(),
  };
}

// Text summary of a drawing: every text label, and arrows/lines with the labels they connect.
export function describeDrawing(data) {
  const els = (data.elements || []).filter(e => !e.isDeleted);
  const byId = Object.fromEntries(els.map(e => [e.id, e]));
  const label = e => {
    if (!e) return null;
    if (e.type === 'text') return e.text;
    const t = (e.boundElements || []).map(b => byId[b.id]).find(x => x?.type === 'text');
    return t ? t.text : `[${e.type}]`;
  };
  const texts = els.filter(e => e.type === 'text').map(e => ({ text: e.text, inside: e.containerId ? byId[e.containerId]?.type : null }));
  const shapes = els.filter(e => ['rectangle', 'ellipse', 'diamond'].includes(e.type)).map(e => ({ shape: e.type, label: label(e) }));
  // Arrows drawn freehand are often not "bound" to a shape, so fall back to the nearest shape/label to each end.
  const targets = els.filter(e => !['arrow', 'line', 'freedraw'].includes(e.type) && !(e.type === 'text' && e.containerId && ['arrow', 'line'].includes(byId[e.containerId]?.type)));
  const dist = (e, x, y) => Math.hypot(Math.max(e.x - x, 0, x - (e.x + e.width)), Math.max(e.y - y, 0, y - (e.y + e.height)));
  const near = (x, y) => {
    let best = null, bd = 80;
    for (const t of targets) { const d = dist(t, x, y); if (d < bd) { bd = d; best = t; } }
    if (best?.type === 'text' && best.containerId) best = byId[best.containerId];
    return best ? label(best) + ' (nearest)' : null;
  };
  const connectors = els.filter(e => ['arrow', 'line'].includes(e.type)).map(e => {
    const p = e.points || [[0, 0]], a = p[0], z = p[p.length - 1];
    return {
      type: e.type,
      from: e.startBinding ? label(byId[e.startBinding.elementId]) : near(e.x + a[0], e.y + a[1]),
      to: e.endBinding ? label(byId[e.endBinding.elementId]) : near(e.x + z[0], e.y + z[1]),
      label: label(e) === `[${e.type}]` ? null : label(e),
    };
  });
  const counts = {}; for (const e of els) counts[e.type] = (counts[e.type] || 0) + 1;
  return { element_counts: counts, texts, shapes, connectors };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [, , inFile, outFile] = process.argv;
  const r = await makeRenderer();
  const data = JSON.parse(fs.readFileSync(inFile, 'utf8'));
  fs.writeFileSync(outFile, await r.render(data));
  console.log(JSON.stringify(describeDrawing(data), null, 1));
  await r.close();
}
