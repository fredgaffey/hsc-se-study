// Captures a NESA HSC online-exam paper from the public familiarisation site using a private headless Chromium.
// Clicking a paper's button returns the full paper (state.itemGroups + test.questionPresentationGroups) in one
// Concerto response; nothing personal is entered and the exam is never started.
import { chromium } from '/Users/fred/gradeo/node_modules/playwright-core/index.mjs';
import fs from 'node:fs';
const [, , button, outFile] = process.argv;
const b = await chromium.launch({ executablePath: process.env.HOME + '/Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell' });
const pg = await b.newPage();
let got = null;
pg.on('response', async r => {
  if (!/\/test\/session\/.*\/submit/.test(r.url())) return;
  try { const j = JSON.parse(await r.text()); if (j.data?.templateParams?.state?.itemGroups) got = j.data.templateParams; } catch {}
});
await pg.goto('https://fam.hsconline.nesa.nsw.edu.au/', { waitUntil: 'networkidle' });
await pg.getByRole('button', { name: button, exact: true }).click();
for (let i = 0; i < 60 && !got; i++) await pg.waitForTimeout(500);
if (!got) { console.error('no paper data'); process.exit(1); }
// images: fetch inside the same browser session (protected files need the session cookie)
const files = [...(got.preloadProtected || []), ...(got.preloadUnprotected || [])].map(f => f.file).filter(f => /protected\//.test(f));
for (const m of JSON.stringify(got).matchAll(/files\/protected\/([A-Za-z0-9_.-]+)/g)) {
  const f = '/bundles/concertopanel/files/protected/' + m[1];
  if (!files.includes(f) && !/^(info|exit|zoom)/.test(m[1]) && !/\.mp4$/.test(m[1])) files.push(f);
}
const imgs = {};
for (const f of files) {
  const r = await pg.request.get('https://fam.hsconline.nesa.nsw.edu.au' + f);
  if (r.ok()) imgs[f] = (await r.body()).toString('base64'); else console.error('img', r.status(), f);
  await pg.waitForTimeout(300);
}
fs.writeFileSync(outFile, JSON.stringify({ captured: new Date().toISOString(), button, params: got, images: imgs }));
console.log('ok', got.test?.title, Object.keys(imgs).length, 'images');
await b.close();
