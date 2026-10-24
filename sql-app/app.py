"""SQL practice web app — HSC Software Engineering.

Every task runs against the one Games / Publishers / Developers database from
the HSC Software Engineering course specification (page 22-23). The student
writes a SELECT statement; the server runs it, runs the reference solution, and
compares results. Progress (completion + drafts) persists in progress.db.

Students may write comparison operators either as HSC words
(GREATER THAN, LESS THAN OR EQUAL TO, EQUALS, NOT EQUAL TO, CONTAINS,
DOES NOT CONTAIN) or as the symbol characters (>, <=, =, <>, LIKE). Both are
accepted — see translate_operators().
"""

import difflib
import os
import re
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).parent
DBS = ROOT / "databases"
PRACTICE_DB = DBS / "practice.db"
PROGRESS_DB = ROOT / "progress.db"

app = Flask(__name__, static_folder=None)


# ---------------------------------------------------------------------------
# The shared database — the syllabus example (Games / Publishers / Developers)
# ---------------------------------------------------------------------------

# Release dates are stored in ISO format (YYYY-MM-DD) so that date-range
# comparisons sort correctly. The syllabus prints them as DD/MM/YYYY, but text
# comparison of that format sorts by day-of-month, which breaks range filters.
SEED_SQL = """
    CREATE TABLE Publishers (
        Publisher_ID INTEGER PRIMARY KEY,
        Name         TEXT
    );
    INSERT INTO Publishers VALUES
        (1, 'Games Inc'),
        (2, 'Pixel Forge'),
        (3, 'Nova Interactive');

    CREATE TABLE Developers (
        Developer_ID INTEGER PRIMARY KEY,
        First_name   TEXT,
        Last_name    TEXT
    );
    INSERT INTO Developers VALUES
        (1, 'Sarah',  'Chen'),
        (2, 'Marcus', 'Reid'),
        (3, 'Aisha',  'Patel'),
        (4, 'Tom',    'Nguyen'),
        (5, 'Elena',  'Rossi');

    CREATE TABLE Games (
        ID           INTEGER PRIMARY KEY,
        Name         TEXT,
        Release_date TEXT,
        Cost         INTEGER,
        Publisher_ID INTEGER,
        Developer_ID INTEGER
    );
    INSERT INTO Games VALUES
        (1,  'Astro Miner',    '2022-06-15', 120000, 1, 1),
        (2,  'Battle Forge',   '2021-11-02', 250000, 1, 2),
        (3,  'Crystal Quest',  '2022-03-20', 180000, 2, 3),
        (4,  'Dungeon Dash',   '2023-01-10',  90000, 1, 1),
        (5,  'Echo Fields',    '2023-09-05', 300000, 3, 4),
        (6,  'Frost Realm',    '2023-03-28', 150000, 1, 2),
        (7,  'Galaxy Raiders', '2020-07-14', 200000, 2, 5),
        (8,  'Hidden Hollow',  '2022-03-03',  75000, 1, 3),
        (9,  'Iron Vanguard',  '2022-12-19', 220000, 3, 4),
        (10, 'Jade Empire',    '2022-03-01', 130000, 1, 5);
"""

# Tables shown to the student (schema + sample rows) on every task.
TABLES = ["Games", "Publishers", "Developers"]


# ---------------------------------------------------------------------------
# Tasks — all against the shared database, graded simple → complex
# ---------------------------------------------------------------------------

TASKS = [
    {
        "id": 1,
        "title": "List every game",
        "description": (
            "Display every column for every row in the Games table."
        ),
        "solution_sql": "SELECT * FROM Games",
        "ordered": False,
        "hint": "Use SELECT * to mean 'every column'. The FROM clause names the table.",
    },
    {
        "id": 2,
        "title": "Game names and release dates",
        "description": (
            "Display only the Name and Release_date of every game."
        ),
        "solution_sql": "SELECT Name, Release_date FROM Games",
        "ordered": False,
        "hint": "List the column names you want, separated by commas, between SELECT and FROM.",
    },
    {
        "id": 3,
        "title": "Expensive games",
        "description": (
            "Display the Name and Cost of every game whose Cost is GREATER "
            "THAN 150000.\n\nYou may write the operator as the word "
            "'GREATER THAN' or as the symbol '>' — both are accepted."
        ),
        "solution_sql": "SELECT Name, Cost FROM Games WHERE Cost > 150000",
        "ordered": False,
        "hint": "Use a WHERE clause. 'GREATER THAN' and '>' both work here.",
    },
    {
        "id": 4,
        "title": "Games released in 2023 or later",
        "description": (
            "Display the Name and Release_date of every game released on or "
            "after 1 January 2023 (Release_date GREATER THAN OR EQUAL TO "
            "'2023-01-01').\n\nThe operator may be written as the words "
            "'GREATER THAN OR EQUAL TO' or as the symbol '>='."
        ),
        "solution_sql": (
            "SELECT Name, Release_date FROM Games "
            "WHERE Release_date >= '2023-01-01'"
        ),
        "ordered": False,
        "hint": "Dates in this database are text in YYYY-MM-DD form, so they "
                "compare correctly. Use >= (or GREATER THAN OR EQUAL TO).",
    },
    {
        "id": 5,
        "title": "Developers with an 'a' in their first name",
        "description": (
            "Display the First_name and Last_name of every developer whose "
            "First_name CONTAINS the letter 'a' (case-insensitive).\n\nYou may "
            "write 'CONTAINS ''a''' or the SQL form LIKE '%a%'."
        ),
        "solution_sql": (
            "SELECT First_name, Last_name FROM Developers "
            "WHERE First_name LIKE '%a%'"
        ),
        "ordered": False,
        "hint": "'CONTAINS' becomes LIKE '%a%' — the % symbols match any "
                "characters before and after. Both forms are accepted.",
    },
    {
        "id": 6,
        "title": "Recent, affordable games",
        "description": (
            "Display the Name, Release_date and Cost of every game released on "
            "or after 1 January 2022 AND costing LESS THAN 150000."
        ),
        "solution_sql": (
            "SELECT Name, Release_date, Cost FROM Games "
            "WHERE Release_date >= '2022-01-01' AND Cost < 150000"
        ),
        "ordered": False,
        "hint": "Combine two conditions with AND. Operators can be words or "
                "symbols (>= / <, or GREATER THAN OR EQUAL TO / LESS THAN).",
    },
    {
        "id": 7,
        "title": "Games by cost, most expensive first",
        "description": (
            "Display the Name and Cost of every game, ORDERED BY Cost "
            "DESCENDING."
        ),
        "solution_sql": "SELECT Name, Cost FROM Games ORDER BY Cost DESC",
        "ordered": True,
        "hint": "Add ORDER BY Cost DESC at the end of the query for descending "
                "order.",
    },
    {
        "id": 8,
        "title": "Cost in thousands",
        "description": (
            "For every game display the Name and the Cost expressed in "
            "thousands of dollars (Cost / 1000.0) renamed AS cost_thousands."
        ),
        "solution_sql": (
            "SELECT Name, Cost / 1000.0 AS cost_thousands FROM Games"
        ),
        "ordered": False,
        "hint": "Divide Cost by 1000.0 and rename the result with AS "
                "cost_thousands.",
    },
    {
        "id": 9,
        "title": "Games summary",
        "description": (
            "Display the count of games renamed AS num_games, the SUM of Cost "
            "renamed AS total_cost, and the AVERAGE Cost renamed AS avg_cost. "
            "One row, three columns."
        ),
        "solution_sql": (
            "SELECT COUNT(ID) AS num_games, "
            "SUM(Cost) AS total_cost, "
            "AVG(Cost) AS avg_cost "
            "FROM Games"
        ),
        "ordered": False,
        "hint": "Put COUNT(ID), SUM(Cost), AVG(Cost) in the SELECT list and "
                "rename each with AS.",
    },
    {
        "id": 10,
        "title": "Games with their publisher",
        "description": (
            "Display each game's name renamed AS Game together with its "
            "publisher's name renamed AS Publisher. This needs both the Games "
            "and Publishers tables, joined on Publisher_ID."
        ),
        "solution_sql": (
            "SELECT Games.Name AS Game, Publishers.Name AS Publisher "
            "FROM Games, Publishers "
            "WHERE Games.Publisher_ID = Publishers.Publisher_ID"
        ),
        "ordered": False,
        "hint": "List both tables in FROM, then match the rows in WHERE: "
                "Games.Publisher_ID = Publishers.Publisher_ID. Because both "
                "tables have a Name column, qualify them (Games.Name) and "
                "rename with AS.",
    },
    {
        "id": 11,
        "title": "Total cost per publisher",
        "description": (
            "Display each publisher's Name and the SUM of the Cost of their "
            "games renamed AS total_cost, GROUPED BY publisher, ORDERED BY "
            "total_cost DESCENDING."
        ),
        "solution_sql": (
            "SELECT Publishers.Name, SUM(Games.Cost) AS total_cost "
            "FROM Games, Publishers "
            "WHERE Games.Publisher_ID = Publishers.Publisher_ID "
            "GROUP BY Publishers.Name "
            "ORDER BY total_cost DESC"
        ),
        "ordered": True,
        "hint": "Join Games and Publishers, SELECT the publisher name plus "
                "SUM(Games.Cost), then GROUP BY the publisher and ORDER BY the "
                "AS alias.",
    },
    {
        "id": 12,
        "title": "Games released in a date range (syllabus example)",
        "description": (
            "This is the first worked example from the course specification.\n\n"
            "Display the Name and Release_date of all games released from "
            "1 March 2022 to 31 March 2023. The results should be in ascending "
            "alphabetical order by game name."
        ),
        "solution_sql": (
            "SELECT Name, Release_date FROM Games "
            "WHERE Release_date >= '2022-03-01' AND Release_date <= '2023-03-31' "
            "ORDER BY Name ASC"
        ),
        "ordered": True,
        "hint": "Two conditions joined with AND give the range (>= the start "
                "AND <= the end), then ORDER BY Name ASC.",
    },
    {
        "id": 13,
        "title": "Developer totals for 'Games Inc' (syllabus example)",
        "description": (
            "This is the second worked example from the course specification "
            "— the hardest query in the course.\n\n"
            "Display each developer's First_name and Last_name, together with "
            "the total Cost of games they have developed for the publisher "
            "'Games Inc' renamed AS Totalcost, listed in descending order of "
            "developer last name."
        ),
        "solution_sql": (
            "SELECT Developers.First_name, Developers.Last_name, "
            "SUM(Games.Cost) AS Totalcost "
            "FROM Games, Publishers, Developers "
            "WHERE Publishers.Name = 'Games Inc' "
            "AND Publishers.Publisher_ID = Games.Publisher_ID "
            "AND Developers.Developer_ID = Games.Developer_ID "
            "GROUP BY Developers.Developer_ID "
            "ORDER BY Developers.Last_name DESC"
        ),
        "ordered": True,
        "hint": "List all three tables in FROM. In WHERE, filter to the "
                "publisher AND join Publishers to Games AND Developers to "
                "Games. Then GROUP BY the developer and ORDER BY Last_name "
                "DESC.",
    },
]


# ---------------------------------------------------------------------------
# DB setup
# ---------------------------------------------------------------------------

def build_practice_dbs() -> None:
    if DBS.exists():
        shutil.rmtree(DBS)
    DBS.mkdir(parents=True)
    with sqlite3.connect(PRACTICE_DB) as conn:
        conn.executescript(SEED_SQL)


def init_progress_db() -> None:
    with sqlite3.connect(PROGRESS_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                task_id      INTEGER PRIMARY KEY,
                completed_at TEXT,
                attempts     INTEGER DEFAULT 0,
                best_query   TEXT,
                draft_query  TEXT
            )
            """
        )


def open_practice_ro() -> sqlite3.Connection:
    uri = f"file:{PRACTICE_DB}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=2)
    conn.execute("PRAGMA query_only = 1")
    return conn


def all_columns() -> list[str]:
    """Every column name across the practice tables (for spell-check)."""
    cols: list[str] = []
    with open_practice_ro() as conn:
        for table in TABLES:
            for r in conn.execute(f"PRAGMA table_info({table})").fetchall():
                cols.append(r[1])
    return cols


# ---------------------------------------------------------------------------
# HSC word operators  →  SQL symbols
# ---------------------------------------------------------------------------

# Multi-word phrases must be tried longest-first so that "GREATER THAN OR EQUAL
# TO" is not partly consumed by "GREATER THAN".
_WORD_OPERATORS = [
    (r"\bGREATER\s+THAN\s+OR\s+EQUAL\s+TO\b", ">="),
    (r"\bLESS\s+THAN\s+OR\s+EQUAL\s+TO\b", "<="),
    (r"\bGREATER\s+THAN\b", ">"),
    (r"\bLESS\s+THAN\b", "<"),
    (r"\bNOT\s+EQUAL\s+TO\b", "<>"),
    (r"\bEQUAL\s+TO\b", "="),
    (r"\bEQUALS\b", "="),
]


def translate_operators(query: str) -> str:
    """Rewrite HSC word operators into the SQL symbols SQLite understands.

    Symbol operators (>, >=, <, <=, =, <>, LIKE) are left untouched, so students
    may use either form. CONTAINS / DOES NOT CONTAIN consume the following
    quoted string and become LIKE / NOT LIKE with % wildcards.
    """
    q = query

    # CONTAINS / DOES NOT CONTAIN need the following 'literal'; do them first,
    # longest phrase (DOES NOT CONTAIN) before its substring (CONTAINS).
    q = re.sub(
        r"\bDOES\s+NOT\s+CONTAIN\s+'((?:[^']|'')*)'",
        r"NOT LIKE '%\1%'", q, flags=re.IGNORECASE,
    )
    q = re.sub(
        r"\bCONTAINS\s+'((?:[^']|'')*)'",
        r"LIKE '%\1%'", q, flags=re.IGNORECASE,
    )

    # Mask string literals so operator words inside them are never rewritten.
    literals: list[str] = []

    def _mask(m: re.Match) -> str:
        literals.append(m.group(0))
        return f"\x00{len(literals) - 1}\x00"

    masked = re.sub(r"'(?:[^']|'')*'", _mask, q)

    for pattern, symbol in _WORD_OPERATORS:
        masked = re.sub(pattern, symbol, masked, flags=re.IGNORECASE)

    return re.sub(r"\x00(\d+)\x00", lambda m: literals[int(m.group(1))], masked)


# ---------------------------------------------------------------------------
# Spelling suggestions
# ---------------------------------------------------------------------------

SQL_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "AS",
    "AND", "OR", "NOT", "LIKE", "IN", "IS", "NULL",
    "ASC", "DESC", "DISTINCT", "LIMIT", "HAVING",
    "COUNT", "SUM", "AVG", "MIN", "MAX",
}

WORD_RE = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*\b")


def spelling_suggestions(query: str, columns: list[str]) -> list[str]:
    """Find words in the query that look like typos of known SQL identifiers."""
    known_upper = {kw: kw for kw in SQL_KEYWORDS}
    known_lower = {t.lower(): t for t in TABLES}
    for c in columns:
        known_lower[c.lower()] = c
    all_known = list(known_upper) + list(known_lower)

    seen = set()
    suggestions = []
    for word in WORD_RE.findall(query):
        if word.lower() in seen:
            continue
        seen.add(word.lower())

        if word.upper() in known_upper or word.lower() in known_lower:
            continue
        if word.isdigit():
            continue

        matches = difflib.get_close_matches(
            word.lower(), [k.lower() for k in all_known], n=1, cutoff=0.75
        )
        if not matches:
            matches = difflib.get_close_matches(
                word.upper(), list(known_upper), n=1, cutoff=0.75
            )
            if matches:
                suggestions.append(f"'{word}' → did you mean '{matches[0]}'?")
            continue
        m = matches[0]
        canonical = known_upper.get(m.upper()) or known_lower.get(m.lower()) or m
        if canonical.lower() == word.lower():
            continue
        suggestions.append(f"'{word}' → did you mean '{canonical}'?")
    return suggestions


# ---------------------------------------------------------------------------
# Query execution + comparison
# ---------------------------------------------------------------------------

def run_query(conn: sqlite3.Connection, query: str):
    cur = conn.execute(query)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = [list(r) for r in cur.fetchall()]
    return cols, rows


def compare(student_cols, student_rows, sol_cols, sol_rows, ordered):
    if [c.lower() for c in student_cols] != [c.lower() for c in sol_cols]:
        return False
    if ordered:
        return student_rows == sol_rows
    key = lambda r: tuple(repr(v) for v in r)
    return sorted(student_rows, key=key) == sorted(sol_rows, key=key)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/tasks")
def list_tasks():
    # Shared schema (all three tables) — the same for every task.
    schema = []
    with open_practice_ro() as conn:
        for table in TABLES:
            cols = [
                {"name": r[1], "type": r[2]}
                for r in conn.execute(f"PRAGMA table_info({table})").fetchall()
            ]
            sample_cur = conn.execute(f"SELECT * FROM {table} LIMIT 10")
            schema.append({
                "name": table,
                "columns": cols,
                "sample_columns": [d[0] for d in sample_cur.description],
                "sample_rows": [list(r) for r in sample_cur.fetchall()],
            })

    tasks = [
        {
            "id": t["id"],
            "title": t["title"],
            "description": t["description"],
            "hint": t.get("hint", ""),
        }
        for t in TASKS
    ]
    return jsonify({"schema": schema, "tasks": tasks})


@app.get("/progress")
def get_progress():
    with sqlite3.connect(PROGRESS_DB) as conn:
        cur = conn.execute(
            "SELECT task_id, completed_at, attempts, best_query, draft_query "
            "FROM progress"
        )
        rows = [
            {
                "task_id": r[0],
                "completed_at": r[1],
                "attempts": r[2],
                "best_query": r[3],
                "draft_query": r[4],
            }
            for r in cur.fetchall()
        ]
    return jsonify(rows)


@app.post("/run")
def run():
    data = request.get_json(force=True)
    task_id = int(data.get("task_id"))
    query = (data.get("query") or "").strip()
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Unknown task"}), 400
    if not query:
        return jsonify({"error": "Query is empty."}), 400

    executable = translate_operators(query)

    try:
        with open_practice_ro() as conn:
            student_cols, student_rows = run_query(conn, executable)
            sol_cols, sol_rows = run_query(conn, task["solution_sql"])
    except sqlite3.Error as e:
        record_attempt(task_id, query, success=False)
        suggestions = spelling_suggestions(query, all_columns())
        msg = f"SQL error: {e}"
        if suggestions:
            msg += "\n" + "\n".join(suggestions)
        return jsonify({"error": msg}), 200

    correct = compare(
        student_cols, student_rows, sol_cols, sol_rows, task["ordered"]
    )
    record_attempt(task_id, query, success=correct)

    payload = {
        "columns": student_cols,
        "rows": student_rows,
        "correct": correct,
        "rows_match": correct,
    }
    if not correct:
        payload["expected_columns"] = sol_cols
        payload["expected_rows"] = sol_rows
    return jsonify(payload)


def record_attempt(task_id: int, query: str, success: bool) -> None:
    with sqlite3.connect(PROGRESS_DB) as conn:
        conn.execute(
            "INSERT INTO progress (task_id, attempts, draft_query) "
            "VALUES (?, 1, ?) "
            "ON CONFLICT(task_id) DO UPDATE SET "
            "attempts = attempts + 1, draft_query = excluded.draft_query",
            (task_id, query),
        )
        if success:
            conn.execute(
                "UPDATE progress SET best_query = ?, "
                "completed_at = COALESCE(completed_at, ?) "
                "WHERE task_id = ?",
                (query, datetime.utcnow().isoformat(timespec="seconds"), task_id),
            )


@app.post("/save_draft")
def save_draft():
    data = request.get_json(force=True)
    task_id = int(data.get("task_id"))
    query = data.get("query") or ""
    with sqlite3.connect(PROGRESS_DB) as conn:
        conn.execute(
            "INSERT INTO progress (task_id, draft_query) VALUES (?, ?) "
            "ON CONFLICT(task_id) DO UPDATE SET draft_query = excluded.draft_query",
            (task_id, query),
        )
    return jsonify({"ok": True})


@app.post("/reset")
def reset():
    with sqlite3.connect(PROGRESS_DB) as conn:
        conn.execute("DELETE FROM progress")
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    build_practice_dbs()
    init_progress_db()
    port = int(os.environ.get("PORT", 5050))
    print(f"SQL practice running at http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
