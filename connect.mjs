import { chromium } from 'playwright-core';
import fs from 'node:fs';
const [port, p] = fs.readFileSync(process.env.HOME + '/Library/Application Support/Google/Chrome/DevToolsActivePort', 'utf8').trim().split('\n');
export async function connect() {
  return chromium.connectOverCDP(`ws://localhost:${port}${p}`, { timeout: 60000 });
}
