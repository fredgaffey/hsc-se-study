# Canvas course site: server

The back end for the course site in [`../canvas`](../canvas): a **Cloudflare Worker** with a **D1** (SQLite) database. It adds accounts (sign-up needs an invite code), a login gate, and progress sync between devices (each user's sync key is sent in the Authorization header, never in the URL).

You don't need it to use the course: `npm start` in the repo root serves `canvas/` locally with no login. Use this if you want to host your own copy online.

| File | Does |
|---|---|
| `src/index.js` | Worker: serves the site, sign-up/login routes, progress sync API |
| `src/auth.js` | PBKDF2 password hashing, random session tokens (only their SHA-256 is stored), cookie handling |
| `schema.sql`, `migrations/` | D1 tables (users, sessions, progress) |
| `wrangler.jsonc` | Worker config. Points at `../canvas` as the static site |

## Deploy your own

```bash
npm install -g wrangler
wrangler login
wrangler d1 create sen-offline            # copy the new database_id into wrangler.jsonc
wrangler d1 execute sen-offline --remote --file=schema.sql
wrangler d1 execute sen-offline --remote --file=migrations/0002_auth.sql
wrangler secret put INVITE_CODE           # the access code people need to sign up
wrangler deploy
```

Worth reading as a worked example for **Secure Software Architecture** and **Programming for the Web**: hashed and salted passwords, session tokens stored as hashes, HTTP-only cookies, and server-side checks on every request.
