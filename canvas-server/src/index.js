/**
 * SEN Offline — Worker.
 *
 * Serves the static app from the ASSETS binding, and exposes a small sync API
 * so quiz progress follows you between devices.
 *
 * Design note: the 680-question bank stays a static asset (identical for every
 * user, precached, works offline). Only *attempts* live in D1.
 *
 *   GET  /api/sync?key=...      -> { scores: {...} }
 *   POST /api/sync  {key,scores} -> merge, returns the merged set
 *   GET  /api/health
 */

import { hashPassword, verifyPassword, createSession, currentUser,
         destroySession, cookie, randomB64 } from "./auth.js";

const KEY_RE = /^[A-Za-z0-9_-]{16,64}$/;
const UNAME_RE = /^[A-Za-z0-9_.-]{2,32}$/;
const SESSION_DAYS = 30;

/** Paths reachable without a session: the login page and the auth routes. */
function isPublic(pathname) {
  return pathname === "/login.html" || pathname === "/login" ||
         pathname.startsWith("/api/auth/");
}

/**
 * The sync key is a bearer secret, so it must not travel in the URL —
 * query strings leak into access logs, proxies and browser history.
 * Read it from the Authorization header; ?key= is still accepted so older
 * clients keep working, but such responses carry a warning header.
 */
function keyFrom(request, url) {
  const auth = request.headers.get("authorization") || "";
  const m = /^Bearer\s+(.+)$/i.exec(auth.trim());
  if (m) return { key: m[1].trim(), legacy: false };
  const q = url.searchParams.get("key");
  return q ? { key: q, legacy: true } : { key: "", legacy: false };
}
const MAX_BODY = 512 * 1024;      // 512 KB is far more than a full score set
const MAX_QUIZZES = 500;
const HISTORY_CAP = 20;

/**
 * Per-key rate limit. Isolate-local, so it is a speed bump rather than a
 * guarantee — a determined caller can land on a fresh isolate. A hard limit
 * would need Durable Objects.
 */
const HITS = new Map();
const LIMIT = 60, WINDOW_MS = 60000;
function overLimit(key) {
  const now = Date.now();
  const e = HITS.get(key);
  if (!e || now - e.start > WINDOW_MS) { HITS.set(key, { start: now, n: 1 }); return false; }
  e.n++;
  if (HITS.size > 5000) HITS.clear();
  return e.n > LIMIT;
}

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

const clampPct = (n) => Math.max(0, Math.min(100, Math.round(Number(n) || 0)));
const clampInt = (n) => Math.max(0, Math.min(1e6, Math.floor(Number(n) || 0)));

/** Rows -> the shape the client keeps in localStorage. */
function rowsToScores(rows) {
  const out = {};
  for (const r of rows) {
    let history = [];
    try { history = JSON.parse(r.history) || []; } catch { /* ignore */ }
    out[r.quiz_key] = {
      attempts: r.attempts, best: r.best, last: r.last,
      lastN: r.last_n, lastOf: r.last_of,
      when: r.updated_at, history,
    };
  }
  return out;
}

/**
 * Merge one incoming record with what's stored.
 * attempts/best take the max (either device may hold the higher figure);
 * the most recent run wins for last/lastN/lastOf; history is unioned by
 * timestamp so two devices don't clobber each other's runs.
 */
function mergeRecord(existing, incoming) {
  const e = existing || { attempts: 0, best: 0, last: 0, lastN: null, lastOf: null, when: null, history: [] };
  const newer = !e.when || (incoming.when && incoming.when > e.when);

  const seen = new Map();
  for (const h of [...(e.history || []), ...(incoming.history || [])]) {
    if (h && h.at) seen.set(h.at, { p: clampPct(h.p), at: String(h.at).slice(0, 40) });
  }
  const history = [...seen.values()].sort((a, b) => (a.at < b.at ? -1 : 1)).slice(-HISTORY_CAP);

  return {
    attempts: Math.max(clampInt(e.attempts), clampInt(incoming.attempts)),
    best: Math.max(clampPct(e.best), clampPct(incoming.best)),
    last: newer ? clampPct(incoming.last) : clampPct(e.last),
    lastN: newer ? clampInt(incoming.lastN) : e.lastN,
    lastOf: newer ? clampInt(incoming.lastOf) : e.lastOf,
    when: newer ? incoming.when : e.when,
    history,
  };
}

async function readAll(env, key) {
  const { results } = await env.DB
    .prepare("SELECT quiz_key, attempts, best, last, last_n, last_of, history, updated_at FROM progress WHERE sync_key = ?")
    .bind(key)
    .all();
  return results || [];
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    /* ---------------- auth routes ---------------- */
    if (url.pathname.startsWith("/api/auth/")) {
      const act = url.pathname.slice("/api/auth/".length);

      if (act === "me") {
        const u = await currentUser(request, env);
        return json(u ? { user: { username: u.username }, syncKey: u.sync_key } : { user: null });
      }

      if (act === "logout" && request.method === "POST") {
        await destroySession(request, env);
        const r = json({ ok: true });
        r.headers.append("set-cookie", cookie("sen_session", "", 0));
        return r;
      }

      if (request.method !== "POST") return json({ error: "method not allowed" }, 405);

      let body;
      try { body = await request.json(); } catch { return json({ error: "invalid json" }, 400); }
      const username = String((body && body.username) || "").trim();
      const password = String((body && body.password) || "");

      if (act === "register") {
        // A shared invite code gates who may create an account. Stored as a
        // Worker secret, so it can be rotated without touching the repo.
        const invite = String((body && body.invite) || "");
        const expected = env.INVITE_CODE || "";
        if (!expected) return json({ error: "registration is closed" }, 403);
        if (invite !== expected) return json({ error: "wrong access code" }, 403);
        if (!UNAME_RE.test(username)) return json({ error: "username: 2-32 letters, digits, . _ -" }, 400);
        if (password.length < 3) return json({ error: "password too short" }, 400);

        const exists = await env.DB.prepare("SELECT id FROM users WHERE uname_lc = ?")
          .bind(username.toLowerCase()).first();
        if (exists) return json({ error: "that username is taken" }, 409);

        const { hash, salt, iter } = await hashPassword(password);
        const syncKey = randomB64(18);
        const res = await env.DB.prepare(
          `INSERT INTO users (username, uname_lc, pw_hash, pw_salt, pw_iter, sync_key, created_at)
           VALUES (?,?,?,?,?,?,?)`
        ).bind(username, username.toLowerCase(), hash, salt, iter, syncKey, new Date().toISOString()).run();

        const { token } = await createSession(env, res.meta.last_row_id);
        const out = json({ ok: true, user: { username }, syncKey });
        out.headers.append("set-cookie", cookie("sen_session", token, SESSION_DAYS * 86400));
        return out;
      }

      if (act === "login") {
        const row = await env.DB.prepare(
          "SELECT id, username, pw_hash, pw_salt, pw_iter, sync_key FROM users WHERE uname_lc = ?"
        ).bind(username.toLowerCase()).first();

        // Same response and similar work whether or not the user exists, so the
        // endpoint doesn't reveal which usernames are registered.
        if (!row) {
          await hashPassword(password, null);
          return json({ error: "wrong username or password" }, 401);
        }
        if (!(await verifyPassword(password, row))) {
          return json({ error: "wrong username or password" }, 401);
        }
        const { token } = await createSession(env, row.id);
        const out = json({ ok: true, user: { username: row.username }, syncKey: row.sync_key });
        out.headers.append("set-cookie", cookie("sen_session", token, SESSION_DAYS * 86400));
        return out;
      }

      return json({ error: "not found" }, 404);
    }

    /* ---------------- gate everything else ---------------- */
    if (!isPublic(url.pathname)) {
      const user = await currentUser(request, env);
      if (!user) {
        const wantsHtml = (request.headers.get("accept") || "").includes("text/html");
        if (wantsHtml) return Response.redirect(new URL("/login.html", url).toString(), 302);
        return json({ error: "not signed in" }, 401);
      }
      request = new Request(request);          // pass through to the handlers below
    }

    if (!url.pathname.startsWith("/api/")) {
      // html_handling is "none" so nothing is rewritten or redirected for us:
      // map directory paths to their index.html by hand. Keeping redirects off
      // matters because a redirected response cannot be returned to a
      // navigation from the service worker.
      if (url.pathname.endsWith("/")) {
        const idx = new URL(url);
        idx.pathname += "index.html";
        const hit = await env.ASSETS.fetch(new Request(idx, request));
        if (hit.status !== 404) return hit;
      }
      return env.ASSETS.fetch(request);
    }

    if (url.pathname === "/api/health") {
      return json({ ok: true, time: new Date().toISOString() });
    }

    if (url.pathname !== "/api/sync") return json({ error: "not found" }, 404);

    const probe = keyFrom(request, url).key;
    if (probe && overLimit(probe)) return json({ error: "too many requests" }, 429);

    /* ---------- pull ---------- */
    if (request.method === "GET") {
      const me = await currentUser(request, env);
      const fromSession = me && me.sync_key;
      const { key: hdrKey, legacy } = keyFrom(request, url);
      const key = fromSession || hdrKey;
      if (!KEY_RE.test(key)) return json({ error: "bad sync key" }, 400);
      const res = json({ scores: rowsToScores(await readAll(env, key)) });
      if (legacy) res.headers.set("x-sen-warning", "send the key as an Authorization header, not a query string");
      return res;
    }

    /* ---------- push + merge ---------- */
    if (request.method === "POST") {
      const len = Number(request.headers.get("content-length") || 0);
      if (len > MAX_BODY) return json({ error: "payload too large" }, 413);

      let body;
      try { body = await request.json(); } catch { return json({ error: "invalid json" }, 400); }

      const me = await currentUser(request, env);
      const key = (me && me.sync_key) || keyFrom(request, url).key || (body && body.key) || "";
      if (!KEY_RE.test(key)) return json({ error: "bad sync key" }, 400);

      const incoming = (body && body.scores) || {};
      const quizKeys = Object.keys(incoming).slice(0, MAX_QUIZZES);

      const existing = rowsToScores(await readAll(env, key));
      const now = new Date().toISOString();
      const stmt = env.DB.prepare(
        `INSERT INTO progress
           (sync_key, quiz_key, attempts, best, last, last_n, last_of, history, updated_at)
         VALUES (?,?,?,?,?,?,?,?,?)
         ON CONFLICT(sync_key, quiz_key) DO UPDATE SET
           attempts=excluded.attempts, best=excluded.best, last=excluded.last,
           last_n=excluded.last_n, last_of=excluded.last_of,
           history=excluded.history, updated_at=excluded.updated_at`
      );

      const batch = [];
      for (const qk of quizKeys) {
        // Defence in depth: these strings are echoed back to clients, so refuse
        // anything containing markup even though the UI now renders with
        // textContent. Inert in SQL either way — this is about the DOM.
        if (typeof qk !== "string" || qk.length > 200) continue;
        if (/[<>]/.test(qk)) continue;
        const m = mergeRecord(existing[qk], incoming[qk] || {});
        existing[qk] = m;
        batch.push(stmt.bind(
          key, qk, m.attempts, m.best, m.last, m.lastN, m.lastOf,
          JSON.stringify(m.history), m.when || now
        ));
      }
      if (batch.length) await env.DB.batch(batch);

      return json({ ok: true, merged: batch.length, scores: existing });
    }

    return json({ error: "method not allowed" }, 405);
  },
};
