-- Accounts. Passwords are never stored: only a PBKDF2-SHA256 hash and its salt.
CREATE TABLE IF NOT EXISTS users (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  username   TEXT    NOT NULL,
  uname_lc   TEXT    NOT NULL UNIQUE,        -- case-insensitive uniqueness
  pw_hash    TEXT    NOT NULL,               -- base64 PBKDF2 output
  pw_salt    TEXT    NOT NULL,               -- base64, 16 random bytes
  pw_iter    INTEGER NOT NULL,               -- iterations, so it can be raised later
  sync_key   TEXT    NOT NULL UNIQUE,        -- this account's progress bucket
  created_at TEXT    NOT NULL
);

-- Sessions. The cookie holds a random token; only its SHA-256 is stored, so a
-- leaked database cannot be replayed as a login.
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT    PRIMARY KEY,
  user_id    INTEGER NOT NULL,
  created_at TEXT    NOT NULL,
  expires_at TEXT    NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_exp  ON sessions(expires_at);
