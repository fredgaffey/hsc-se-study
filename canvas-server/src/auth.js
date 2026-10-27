/* Authentication helpers.
   Passwords are hashed with PBKDF2-SHA256 (WebCrypto, available in Workers).
   Plaintext is never stored or logged. Session cookies hold a random token;
   only its SHA-256 is persisted, so a database leak can't be replayed. */

const ITER = 100_000;                 // raise over time; stored per-user
const SESSION_DAYS = 30;

const b64 = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)));
const unb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
const enc = new TextEncoder();

export function randomB64(bytes = 32) {
  const b = new Uint8Array(bytes);
  crypto.getRandomValues(b);
  return b64(b).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

export async function hashPassword(password, saltB64, iter = ITER) {
  const salt = saltB64 ? unb64(saltB64) : crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", salt, iterations: iter, hash: "SHA-256" }, key, 256);
  return { hash: b64(bits), salt: b64(salt), iter };
}

/** Constant-time compare so timing can't leak how much of the hash matched. */
function sameSecret(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export async function verifyPassword(password, user) {
  const { hash } = await hashPassword(password, user.pw_salt, user.pw_iter);
  return sameSecret(hash, user.pw_hash);
}

export async function sha256b64(s) {
  return b64(await crypto.subtle.digest("SHA-256", enc.encode(s)));
}

export async function createSession(env, userId) {
  const token = randomB64(32);
  const now = new Date();
  const exp = new Date(now.getTime() + SESSION_DAYS * 864e5);
  await env.DB.prepare(
    "INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?,?,?,?)"
  ).bind(await sha256b64(token), userId, now.toISOString(), exp.toISOString()).run();
  return { token, expires: exp };
}

export function cookie(name, value, maxAgeSec) {
  // HttpOnly: unreadable from JS, so XSS cannot steal the session.
  // SameSite=Lax: not sent on cross-site POSTs, which blocks CSRF on our routes.
  const bits = [`${name}=${value}`, "Path=/", "HttpOnly", "Secure", "SameSite=Lax",
                `Max-Age=${maxAgeSec}`];
  return bits.join("; ");
}

export function readCookie(request, name) {
  const raw = request.headers.get("cookie") || "";
  for (const part of raw.split(/;\s*/)) {
    const i = part.indexOf("=");
    if (i > 0 && part.slice(0, i) === name) return part.slice(i + 1);
  }
  return null;
}

/** Resolve the current user from the session cookie, or null. */
export async function currentUser(request, env) {
  const token = readCookie(request, "sen_session");
  if (!token) return null;
  const row = await env.DB.prepare(
    `SELECT u.id, u.username, u.sync_key, s.expires_at
       FROM sessions s JOIN users u ON u.id = s.user_id
      WHERE s.token_hash = ?`
  ).bind(await sha256b64(token)).first();
  if (!row) return null;
  if (new Date(row.expires_at) < new Date()) {
    await env.DB.prepare("DELETE FROM sessions WHERE token_hash = ?")
      .bind(await sha256b64(token)).run();
    return null;
  }
  return row;
}

export async function destroySession(request, env) {
  const token = readCookie(request, "sen_session");
  if (!token) return;
  await env.DB.prepare("DELETE FROM sessions WHERE token_hash = ?")
    .bind(await sha256b64(token)).run();
}
