---
name: hsc-pseudocode
description: "Write, review, fix, and convert pseudocode following the NSW HSC Software Engineering course specification conventions (November 2024). Use this skill whenever the user asks to write pseudocode, review pseudocode, check pseudocode, fix pseudocode, convert Python to pseudocode, convert code to pseudocode, or create algorithms for an HSC Software Engineering assessment. Also trigger when the user shares pseudocode that uses HSC-style keywords (BEGIN, END, ENDWHILE, CASEWHERE, ENDIF) or mentions HSC, SDD, Software Engineering course, or NESA conventions. Also trigger when the user shares Python, Flask, or Arduino/ESP32 code and wants pseudocode output for their HSC project. Also trigger when the user mentions AT3, AT3a, assessment task, project documentation, or algorithm design for their Software Engineering course. This skill ensures all pseudocode strictly follows the official HSC course spec rules — capitalised keywords, paired structural elements, correct subroutine patterns, and proper indentation."
---

# HSC Software Engineering — Pseudocode Skill

## Purpose

This skill ensures all pseudocode Claude writes or reviews conforms to the **NSW HSC Software Engineering Course Specifications (November 2024)**. The spec has specific conventions that differ from general programming pseudocode — getting these wrong costs marks.

**Before writing or reviewing any pseudocode, read `references/hsc-pseudocode-rules.md`** for the complete rule set and examples.

## When to Use

- User asks to **write** pseudocode for an HSC project or assessment
- User asks to **review, check, or fix** existing pseudocode
- User shares pseudocode using HSC-style keywords and wants feedback
- User is working on AT3 scaffold sections involving pseudocode/algorithms
- User asks to **convert Python, Flask, or Arduino/C++ code to pseudocode**
- User shares code and says "make this into pseudocode" or "write pseudocode for this"

## Workflow

### 1. Writing Pseudocode

1. Read `references/hsc-pseudocode-rules.md`
2. Design a **clean mainline** that calls named subroutines — this is a specific HSC spec requirement and markers look for it
3. Define each subroutine separately with its own BEGIN/END pair
4. Write the pseudocode following all rules from the reference, paying special attention to:
   - All keywords in CAPITALS
   - Every structural pair closed (BEGIN/END, IF/ENDIF, WHILE/ENDWHILE, FOR/NEXT, REPEAT/UNTIL, CASEWHERE/END CASE)
   - `SET` for assignment, `GET` for input, `DISPLAY` for output
   - END lines mirror BEGIN lines including name and parameters
   - No programming-language syntax (no dot notation, no f-strings, no named params)
5. Run the linter: `python3 scripts/hsc_pseudocode_linter.py <file>`
6. Self-check against the common mistakes checklist in the reference
7. Add comments that explain **why** (not just what) — the AT3 scaffold specifically asks for "detailed explanations and comments for each algorithm"

### 2. Reviewing Pseudocode

1. Read `references/hsc-pseudocode-rules.md`
2. Save the user's pseudocode to a temp file and **run the linter first**:
   ```bash
   python3 scripts/hsc_pseudocode_linter.py tempfile.txt
   ```
3. Then do a manual review for things the linter can't catch (see below)
4. Report issues grouped by severity:
   - **Bugs**: Logic errors that would produce wrong behaviour
   - **Convention violations**: Deviations from HSC spec rules (these lose marks)
   - **Readability**: Naming, comments, structure improvements
5. For each issue, explain what's wrong and show the fix
6. **Do NOT rewrite the entire algorithm unless asked** — point out specific lines and let the user fix them

### 3. Converting Code to Pseudocode

1. Read `references/hsc-pseudocode-rules.md` for the target format rules
2. Follow this conversion process:
   a. **Strip language-specific syntax**: Remove imports, decorators, type hints, f-strings, context managers, try/except, `self`, classes
   b. **Map constructs**: `if` → `IF/THEN/ENDIF`, `while` → `WHILE/ENDWHILE`, `def` → `BEGIN/END`, `return` → `RETURN`, `=` → `SET ... =`
   c. **Flatten OOP**: No dot notation — pass data as subroutine parameters or use array indexing
   d. **Raise abstraction**: Replace library calls, HTTP details, and framework syntax with natural language descriptions
   e. **Structure into mainline + subroutines**: Don't just translate line-by-line — reorganise into a clean mainline that calls separate subroutines
   f. **Add HSC-quality comments**: Explain *why* each step exists
3. Run the linter on the output
4. Self-check against the common mistakes checklist

## Key Rules Quick Reference

These are the most commonly broken rules. The full set is in `references/hsc-pseudocode-rules.md`.

| Rule | Right | Wrong |
|------|-------|-------|
| Keywords in CAPS | `SET x = 5` | `set x = 5` |
| Assignment keyword | `SET count = 0` | `LET count = 0` or bare `count = 0` |
| IF needs THEN | `IF x > 5 THEN` | `IF x > 5` |
| Structural pairs | `IF ... ENDIF` | `IF ...` (no ENDIF) |
| END mirrors BEGIN | `END Add (x, y)` | `END` or `END Add` |
| Positional params only | `calc(10, 5)` | `calc(rate=10, hours=5)` |
| No dot notation | `data[i]` or pass as param | `object.property` |
| No language syntax | `"Hello, " + name` | `f"Hello {name}"` |

## Automated Linter

The skill includes a Python linter at `scripts/hsc_pseudocode_linter.py`.

### What the linter catches
- Structural pair mismatches (missing ENDIF, ENDWHILE, END, NEXT, UNTIL, END CASE)
- LET usage (should be SET)
- Keyword capitalisation (lowercase keywords at start of line)
- Inline keyword capitalisation (lowercase `to`/`step` in FOR loops, lowercase `then` after IF)
- Named parameters (Python-style `func(name=value)`)
- Dot notation (`object.property`)
- Missing THEN after IF/ELSEIF
- Variable typos (near-miss names via Levenshtein distance)
- Indentation (unindented code inside control structures)
- Subroutine END matching (name and parameter mismatches)

### What needs human review (linter can't catch)
- Logic bugs (wrong conditions, wrong comparisons, off-by-one errors)
- Whether the mainline is "clean and uncluttered" enough (HSC spec requirement)
- Quality and usefulness of comments
- Whether the correct variable is being read/written
- Whether subroutines are appropriately decomposed
- Whether natural language descriptions are clear enough

### Usage

Save pseudocode to a file, then run:
```bash
python3 scripts/hsc_pseudocode_linter.py myfile.txt
```

Or pass text directly:
```bash
python3 scripts/hsc_pseudocode_linter.py --text "BEGIN Main\n    SET x = 5\nEND Main"
```

**Always run the linter before delivering pseudocode to the user.** If the linter reports issues, fix them before presenting the output.

## Test Suite

The `evals/` directory contains test cases for validating the linter:

- `spec_p15_binary_selection.txt` — IF/ELSE/ENDIF from spec p.15 (should pass clean)
- `spec_p16_nested_if_case.txt` — ELSEIF and CASEWHERE from spec p.16 (should pass clean)
- `spec_p17_loops.txt` — WHILE and REPEAT from spec p.17 (should pass clean)
- `spec_p18_for_next.txt` — FOR/NEXT from spec p.18 (should pass clean)
- `spec_p19_one_param.txt` — Subroutine from spec p.19 (flags `Get` → `GET`)
- `spec_p20_pass_by_ref.txt` — Pass-by-ref from spec p.20 (flags `Display` → `DISPLAY`, `to` → `TO`)
- `spec_p21_function_return.txt` — Function from spec p.21 (flags `Display` → `DISPLAY`, `to` → `TO`)
- `test_correct_lplate.txt` — Correct L-plate tracker example (should pass clean)
- `test_deliberate_errors.txt` — All error types planted (should catch 13+ issues)
- `run_tests.py` — Automated test runner (17 tests including edge cases)

Run the test suite:
```bash
python3 evals/run_tests.py
```

Note: The spec examples on pp.19–21 have known capitalisation inconsistencies (`Display` not `DISPLAY`, `to` not `TO`). The linter correctly flags these — the formal rule on p.14 says keywords must be capitalised.

## Common Pitfalls for Claude

These are mistakes Claude tends to make when writing HSC pseudocode — check for them:

1. **Forgetting THEN after IF** — every IF and ELSEIF needs THEN on the same line
2. **Using bare END without the subroutine name** — END must mirror BEGIN (e.g. `END ProcessTrip (trip_data)`)
3. **Leaving dot notation in** — especially when converting from Python. `trip.duration` must become `trip_duration` or be passed as a parameter
4. **Over-engineering** — HSC pseudocode should be readable by a human, not compilable. Use natural language for operations that don't have keywords
5. **Skipping the mainline pattern** — for anything beyond a trivial function, there must be a short mainline calling subroutines. This is explicitly marked in the HSC spec
6. **Using ELSE IF instead of ELSEIF** — the HSC spec uses `ELSEIF` as one word
7. **Missing parameters on END lines** — `BEGIN Add (x, y)` requires `END Add (x, y)`, not just `END Add`
