// Starts all three study apps and prints their links.   npm start   (Ctrl-C stops them all)
//   Exam app     http://localhost:7788
//   SQL trainer  http://localhost:5050
//   Course site  http://localhost:8765   (Canvas lessons + quiz generator)
// Works on macOS, Windows and Linux. Needs Node 20+ and Python 3 (Python is only for the SQL trainer).
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const WIN = process.platform === 'win32';
const EXAM_PORT = +process.env.EXAM_PORT || 7788;
const SQL_PORT = +process.env.SQL_PORT || 5050;
const SITE_PORT = +process.env.SITE_PORT || 8765;
const children = [];

function run(name, cmd, args, opts = {}) {
  const p = spawn(cmd, args, { cwd: ROOT, stdio: ['ignore', 'pipe', 'pipe'], ...opts });
  const tag = s => s.toString().split('\n').filter(Boolean).forEach(l => console.log(`[${name}] ${l}`));
  p.stdout.on('data', tag);
  p.stderr.on('data', tag);
  p.on('exit', code => code && console.log(`[${name}] stopped (exit ${code})`));
  children.push(p);
  return p;
}

// 1. Node dependencies
if (!fs.existsSync(path.join(ROOT, 'node_modules', 'marked'))) {
  console.log('Installing Node packages (first run only)…');
  spawnSync(WIN ? 'npm.cmd' : 'npm', ['install', '--no-audit', '--no-fund'], { cwd: ROOT, stdio: 'inherit', shell: WIN });
}

// 2. Exam app
const hasExam = fs.existsSync(path.join(ROOT, 'exam-app', 'server.mjs'));
if (hasExam) run('exam', process.execPath, ['exam-app/server.mjs'], { env: { ...process.env, PORT: String(EXAM_PORT) } });
else console.log('[exam] exam app not included yet, skipping (git pull later to get it)');

// 3. SQL trainer (Python + Flask in its own virtual environment)
const sqlDir = path.join(ROOT, 'sql-app');
const venvPy = path.join(sqlDir, '.venv', WIN ? 'Scripts/python.exe' : 'bin/python');
const sysPy = ['python3', 'python', 'py'].find(c => spawnSync(c, ['--version'], { shell: WIN }).status === 0);
if (!sysPy) {
  console.log('[sql] Python 3 not found, so the SQL trainer is skipped. Install Python from python.org to use it.');
} else {
  if (!fs.existsSync(venvPy)) {
    console.log('Setting up the SQL trainer (first run only)…');
    spawnSync(sysPy, ['-m', 'venv', '.venv'], { cwd: sqlDir, stdio: 'inherit', shell: WIN });
    spawnSync(venvPy, ['-m', 'pip', 'install', '--quiet', 'flask'], { cwd: sqlDir, stdio: 'inherit' });
  }
  run('sql', venvPy, ['app.py'], { cwd: sqlDir, env: { ...process.env, PORT: String(SQL_PORT) } });
}

// 4. Course site (static files)
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.pdf': 'application/pdf', '.webmanifest': 'application/manifest+json',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' };
const SITE = path.join(ROOT, 'canvas');
http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const file = path.resolve(SITE, '.' + p);
  if (!file.startsWith(SITE) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end('not found'); }
  res.writeHead(200, { 'content-type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
}).listen(SITE_PORT, '127.0.0.1');

setTimeout(() => console.log(`
  ┌─────────────────────────────────────────────────────────┐
  │  Exam app     ${hasExam ? `http://localhost:${EXAM_PORT}        ` : '(not included yet)           '}             │
  │  SQL trainer  http://localhost:${SQL_PORT}${sysPy ? '                     ' : ' (needs Python)      '}│
  │  Course site  http://localhost:${SITE_PORT}                     │
  │                                                         │
  │  Press Ctrl-C to stop everything.                       │
  └─────────────────────────────────────────────────────────┘`), 1500);

const stop = () => { children.forEach(c => c.kill()); process.exit(0); };
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
