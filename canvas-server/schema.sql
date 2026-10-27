-- Per-topic quiz progress. One row per (sync key, quiz).
-- The 680-question bank stays a static asset; only attempts live here.
CREATE TABLE IF NOT EXISTS progress (
  sync_key   TEXT    NOT NULL,               -- groups devices belonging to one person
  quiz_key   TEXT    NOT NULL,               -- "12951|1.1 Secure Code Benefits"
  attempts   INTEGER NOT NULL DEFAULT 0,
  best       INTEGER NOT NULL DEFAULT 0,
  last       INTEGER NOT NULL DEFAULT 0,
  last_n     INTEGER,                        -- correct count, most recent run
  last_of    INTEGER,                        -- question count, most recent run
  history    TEXT    NOT NULL DEFAULT '[]',  -- JSON [{p,at}], newest last, capped at 20
  updated_at TEXT    NOT NULL,
  PRIMARY KEY (sync_key, quiz_key)
);
CREATE INDEX IF NOT EXISTS idx_progress_sync ON progress(sync_key, updated_at DESC);
