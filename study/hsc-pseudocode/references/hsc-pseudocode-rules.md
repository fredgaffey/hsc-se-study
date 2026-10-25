# HSC Software Engineering — Pseudocode Rules Reference

> Source: NSW HSC Software Engineering Course Specifications, updated November 2024 (Pages 14–21)
> This reference was cross-checked against the official NESA document. Page numbers are cited throughout.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Keywords](#keywords)
3. [Structural Pairing Rules](#structural-pairing-rules)
4. [Sequence](#sequence)
5. [Selection](#selection)
6. [Repetition](#repetition)
7. [Subroutines and Functions](#subroutines-and-functions)
8. [Variables and Assignment](#variables-and-assignment)
9. [Input and Output](#input-and-output)
10. [Mainline Structure](#mainline-structure)
11. [Comments](#comments)
12. [Common Mistakes Checklist](#common-mistakes-checklist)
13. [Complete Examples](#complete-examples)

---

## Core Principles

From the course spec (p.14), pseudocode is described as follows:

- "Pseudocode is a method of describing the logic in an algorithm"
- "It makes use of capitalised keywords and indentation to show control structures used"
- "keywords are written in capitals"
- "structural elements come in pairs, eg for every BEGIN there is an END, for every IF there is an ENDIF"
- "indenting is used to identify control structures in the algorithm"
- "when refining the solution to a problem, a subroutine can be referred to in an algorithm by its name, with a separate subroutine developed with that same name to show the detailed logic"

Also from p.14 (in the Algorithms introduction above the Pseudocode section):

- "It is important to start complex algorithms with a clear, uncluttered mainline"
- "The mainline should reference required subroutines, the details of which are shown in separate algorithms"
- "Each subroutine should be concise and correctly make use of further subroutines for detailed logic"

### Natural Language in Pseudocode

Pseudocode is a mix of capitalised keywords for control structures and **plain English for everything else**. When there is no pseudocode keyword for an operation (e.g. hardware interactions, file I/O, complex data manipulation), describe it in natural language as a process step. The spec's own examples do this (p.19):

```
Set pointer to first position
Get a character
Store data in arrayname at the position given by the pointer
Increment the pointer
```

These are plain English descriptions — there is no special keyword for "set pointer" or "store data at position." Note that "Set pointer" here is natural language (lowercase "pointer"), distinct from the `SET variable = value` keyword assignment pattern.

**The rule**: if an operation HAS a keyword (`SET`, `IF`, `WHILE`, etc.), use the keyword. If it doesn't, describe it in clear natural language. This keeps the control flow visible (capitalised keywords stand out) while allowing the algorithm to describe domain-specific operations that pseudocode can't formally express.

Good examples of natural language process steps:
```
Connect to OBD device
Open log_file for writing
Write trip_data to log_file
Send data to server
Wait for GPS signal lock
```

---

## Keywords

The spec (p.14) states keywords are written in capitals. The spec does NOT provide a formal keyword list — keywords are identified from the control structure definitions on pp.15–21. The following keywords appear in the spec examples:

### Structure
- `BEGIN` / `END` — marks the start and end of an algorithm or subroutine (pp.19–21)

### Selection
- `IF` / `THEN` / `ELSE` / `ELSEIF` / `ENDIF` — binary and nested selection (pp.15–16)
- `CASEWHERE` / `OTHERWISE` / `END CASE` — multi-way selection (p.16)

### Repetition
- `WHILE` / `ENDWHILE` — pre-test loop (p.17)
- `REPEAT` / `UNTIL` — post-test loop (p.17)
- `FOR` / `TO` / `STEP` / `NEXT` — counted loop (p.18)

### Assignment and Data
- `SET` — assign a value to a variable (p.21 example: `SET total = x + y`)
- `RETURN` — pass a single value back from a function (p.21)

### Logical Operators
- `AND` — used in conditions (p.19 example: `WHILE more data AND space in array`)

### Keywords inferred from convention (not explicitly defined in spec but consistent with pseudocode practice)
- `GET` — receive input (from user, sensor, file, etc.)
- `DISPLAY` — output to screen/user
- `OR`, `NOT` — logical operators

Note: The spec examples on p.20 show `Display sum` (not all-caps) and `FOR i = 1 to 5` (lowercase "to"). These appear to be typographic inconsistencies in the spec — the formal rule on p.14 says "keywords are written in capitals", so always capitalise: `DISPLAY`, `TO`.

---

## Structural Pairing Rules

The spec (p.14) states: "structural elements come in pairs, eg for every BEGIN there is an END, for every IF there is an ENDIF."

Every opening structural keyword MUST have its matching closing keyword. There are no exceptions.

| Opens | Closes | Spec page |
|-------|--------|-----------|
| `BEGIN` | `END` | pp.19–21 |
| `IF ... THEN` | `ENDIF` | p.15 |
| `WHILE` | `ENDWHILE` | p.17 |
| `REPEAT` | `UNTIL` | p.17 |
| `FOR` | `NEXT` | p.18 |
| `CASEWHERE` | `END CASE` | p.16 |

**CRITICAL**: `ELSE` and `ELSEIF` are INSIDE an IF/ENDIF pair — they do NOT replace `ENDIF`. An IF block with an ELSE still needs ENDIF (p.15):

```
IF condition THEN
    process 2
ELSE
    process 1
ENDIF
```

---

## Sequence

Steps executed one after another, in the order written. No special keywords needed. From the spec (p.15):

```
process 1
process 2
…
…
process n
```

---

## Selection

### Binary Selection (IF/THEN/ELSE/ENDIF)

From the spec (p.15):

Without ELSE:
```
IF condition THEN
    process 1
ENDIF
```

With ELSE:
```
IF condition THEN
    process 2
ELSE
    process 1
ENDIF
```

### Nested IF (ELSEIF)

From the spec (p.16):

```
IF condition A THEN
    process 1
ELSEIF condition B THEN
    process 2
ELSEIF condition C THEN
    process 3
ELSE
    process 4
ENDIF
```

Note: Only ONE `ENDIF` at the end of the entire nested chain.

### Multi-way Selection (CASEWHERE)

From the spec (p.16):

```
CASEWHERE expression evaluates to
    choice a: process a
    choice b: process b
    …
    OTHERWISE: default process
END CASE
```

---

## Repetition

### Pre-test Loop (WHILE/ENDWHILE)

From the spec (p.17): "The pre-test loop tests the condition at the start of the loop to determine whether the body of the loop is executed. The body of the loop is executed repeatedly while the termination condition is true."

```
WHILE condition is true
    process
ENDWHILE
```

### Post-test Loop (REPEAT/UNTIL)

From the spec (p.17): "A post-test loop executes the body of the loop before testing the termination condition. The body of the loop is repeatedly executed until the termination condition is true."

```
REPEAT
    process
UNTIL condition is true
```

### Counted Loop (FOR/NEXT)

From the spec (p.18):

```
FOR variable = start TO finish STEP increment
    statements
NEXT variable
```

Note from spec (p.18): "Increment can take either a positive or negative value."

If STEP is 1, it can be omitted (inferred from spec examples on pp.20–21 which show `FOR i = 1 TO 5` without STEP).

---

## Subroutines and Functions

From the spec (p.19): "The terms subroutine, module, subprogram and procedure can be used interchangeably to represent a collection of statements that achieve a specific purpose."

"A function is a particular type of subroutine that returns a single value." (p.19)

### Subroutine with parameters (no return value)

Definition — pass-by-reference pattern from spec (p.20):
```
BEGIN Add (x, y, total)
    total = x + y
END Add (x, y, total)
```

Calling (p.20):
```
Add (i, i + 1, sum)
```

### Subroutine with no parameters

From spec (p.20) — no parentheses on either line:
```
BEGIN AddNumbers
    FOR i = 1 TO 5
        Add(i, i + 1, sum)
        DISPLAY sum
    NEXT i
END AddNumbers
```

### Function (returns a single value)

Definition — uses RETURN, from spec (p.21):
```
BEGIN Add (x, y)
    SET total = x + y
    RETURN total
END Add (x, y)
```

Calling (p.21):
```
DISPLAY Add(i, i + 1)
```

Or storing the result:
```
SET answer = FunctionName(value1, value2)
```

### Subroutine with one parameter

From spec (p.19) — the `read` subroutine fills an array:
```
BEGIN read (arrayname)
    Set pointer to first position
    Get a character
    WHILE more data AND space in array
        Store data in arrayname at the position given by the pointer
        Increment the pointer
        Get next character
    ENDWHILE
END read (arrayname)
```

And the mainline that calls it (p.19):
```
BEGIN
    read (name)
    read (address)
END
```

Note: This mainline uses bare `BEGIN`/`END` without a name — the spec allows both named and unnamed mainlines.

### END Line Parameter Rules

The course spec examples consistently include parameters in the END line, mirroring the BEGIN line:
- `BEGIN Add (x, y, total)` → `END Add (x, y, total)` (spec p.20)
- `BEGIN Add (x, y)` → `END Add (x, y)` (spec p.21)
- `BEGIN read (arrayname)` → `END read (arrayname)` (spec p.19)

Subroutines with **no parameters** have no parentheses on either line:
- `BEGIN AddNumbers` → `END AddNumbers` (spec p.20)
- `BEGIN Addnumbers` → `END Addnumbers` (spec p.21)

### Parameter Rules

- Parameters are **positional only** — defined in the subroutine header
- Call with values in the same order: `Add(i, i + 1, sum)` not `Add(x=i, y=i+1, total=sum)`
- Named/keyword parameters are a Python convention, NOT valid HSC pseudocode
- A subroutine can modify parameters passed to it (pass by reference, as in the p.20 Add example) or return via RETURN (p.21)

---

## Variables and Assignment

### Setting Variables

Use `SET` (spec p.21 example: `SET total = x + y`):
```
SET counter = 0
SET name = "Fred"
SET is_logging = True
```

**Do NOT use**:
- `LET` — not in the HSC spec
- Bare assignment without SET at the top level (e.g. `counter = 0` outside a subroutine parameter context)

**Note on bare assignment**: The spec example on p.20 shows `total = x + y` (without SET) inside a pass-by-reference subroutine, while p.21 shows `SET total = x + y` inside a function. Both patterns appear in the spec. For clarity and consistency, **prefer using SET everywhere** — it makes the assignment visible and avoids ambiguity.

### No Programming-Language Syntax

Pseudocode must not use syntax from specific programming languages. Common violations:

- **No dot notation**: `object.property` is OOP syntax. Use arrays with indices (`data[i]`) or pass values as subroutine parameters instead.
- **No named parameters**: `func(rate=10)` is Python syntax. Use positional parameters: `func(10)`.
- **No f-strings or string interpolation**: `f"Hello {name}"` is Python. Use `"Hello, " + name`.
- **No list comprehensions, lambda, or other language-specific constructs**.

---

## Input and Output

### GET and DISPLAY

The spec examples on pp.19–20 show input/output operations described in natural language ("Get a character", "Display sum"). Capitalise these as keywords when using them in the formal `GET variable` or `DISPLAY expression` pattern:

```
GET username
GET sensor_reading
DISPLAY "Hello, " + name
DISPLAY total
```

### File Operations

The spec does not prescribe specific file I/O keywords. Use clear English descriptions:

```
OPEN filename FOR writing
WRITE data TO filename
READ data FROM filename
CLOSE filename
```

These are acceptable as descriptive process steps in pseudocode.

---

## Mainline Structure

The spec (p.14) states:

"It is important to start complex algorithms with a clear, uncluttered mainline. The mainline should reference required subroutines, the details of which are shown in separate algorithms."

"Each subroutine should be concise and correctly make use of further subroutines for detailed logic."

This means for any non-trivial algorithm:

1. Write a **short mainline** that shows the high-level flow
2. Use **subroutine calls** for any detailed logic
3. Define each subroutine **separately** with its own BEGIN/END

The mainline can be **named** (e.g. `BEGIN AddNumbers` on p.20) or **unnamed** (e.g. bare `BEGIN`/`END` on p.19). Named mainlines are preferable for clarity.

### Good Example — Clean Mainline

```
BEGIN TripLogger
    # Initialise hardware and start logging
    initialise_hardware()
    start_logging()
    upload_trip()
END TripLogger
```

Then define `initialise_hardware`, `start_logging`, and `upload_trip` as separate subroutines.

### Bad Example — Everything in One Block

```
BEGIN
    connect to OBD
    get SD card
    open file
    WHILE logging
        get GPS
        write GPS
        get accel
        write accel
        check if done
    ENDWHILE
    close file
    upload file
END
```

This is too detailed for a mainline — the loop logic should be in a subroutine.

---

## Comments

The spec does not prescribe a comment syntax. Use `#` prefix, which is consistent with Python — the HSC programming language (spec p.32).

```
# Calculate the hash of the entered password
SET password_hash = hash(entered_password)
```

### HSC Assessment Expectations

The AT3 scaffold asks for "detailed explanations and comments for each algorithm." This means:

- Explain **why** each step exists, not just what it does
- Explain the **purpose** of subroutines when you call them
- Note any **assumptions** or **constraints**
- Describe **data flow** — where does input come from, where does output go

Bad comment (just restates the code):
```
# Set counter to 0
SET counter = 0
```

Good comment (explains why):
```
# Track elapsed time since last GPS reading to enforce the logging interval
SET last_gps_time = 0
```

---

## Common Mistakes Checklist

Use this to review pseudocode before submitting. Check each item:

### Structural
- [ ] Every `BEGIN` has a matching `END`
- [ ] Every `IF` has a matching `ENDIF` (even with ELSE/ELSEIF)
- [ ] Every `WHILE` has a matching `ENDWHILE`
- [ ] Every `FOR` has a matching `NEXT`
- [ ] Every `REPEAT` has a matching `UNTIL`
- [ ] Every `CASEWHERE` has a matching `END CASE`
- [ ] All code inside control structures is indented one level

### Keywords
- [ ] All keywords are in CAPITALS (including TO in FOR loops, THEN after IF)
- [ ] Using `SET` for assignment (not `LET`, not bare assignment)
- [ ] Using `DISPLAY` for output (not `Display` or `print`)
- [ ] Using `RETURN` for function return values

### Subroutines
- [ ] Mainline is clean and uncluttered — detail is in subroutines
- [ ] Each subroutine has `BEGIN name` / `END name`
- [ ] END line includes parameters matching the BEGIN line (e.g. `BEGIN Add (x, y)` → `END Add (x, y)`)
- [ ] Subroutines with no params have no parentheses: `BEGIN Name` / `END Name`
- [ ] Functions use `RETURN` before `END`
- [ ] Subroutine calls use positional parameters only (no named/keyword params)
- [ ] Subroutine names are consistent between definition and call
- [ ] Subroutines are defined separately — not nested inside other subroutines

### Logic
- [ ] Loop conditions are correct (will the loop actually terminate?)
- [ ] Variables are initialised before use
- [ ] Variable names are consistent (no typos between SET and later references)
- [ ] Conditions in IF/WHILE statements are logically correct
- [ ] Correct variable is being read/written (e.g. not GET current_gps when you mean current_accel)
- [ ] No programming-language syntax leaking in — no dot notation (`object.property`), no f-strings, no pointers, no list comprehensions

### Comments and Readability
- [ ] Variable names are descriptive (not just `x`, `SD`, `car`)
- [ ] Comments explain WHY, not just WHAT
- [ ] Spelling is correct in comments (markers read them)
- [ ] No code-specific syntax leaking in (no Python f-strings, no C++ pointers, etc.)

---

## Complete Examples

### Example 1: Simple Function

```
# Calculate the area of a rectangle
BEGIN CalculateArea (length, width)
    SET area = length * width
    RETURN area
END CalculateArea (length, width)
```

### Example 2: Spec Example — Pass-by-Reference (p.20)

```
BEGIN AddNumbers
    FOR i = 1 TO 5
        Add(i, i + 1, sum)
        DISPLAY sum
    NEXT i
END AddNumbers

BEGIN Add (x, y, total)
    SET total = x + y
END Add (x, y, total)
```

### Example 3: Spec Example — Function with RETURN (p.21)

```
BEGIN Addnumbers
    FOR i = 1 TO 5
        DISPLAY Add(i, i + 1)
    NEXT i
END Addnumbers

BEGIN Add (x, y)
    SET total = x + y
    RETURN total
END Add (x, y)
```

### Example 4: Spec Example — Subroutine with One Parameter (p.19)

```
BEGIN
    read (name)
    read (address)
END

BEGIN read (arrayname)
    Set pointer to first position
    Get a character
    WHILE more data AND space in array
        Store data in arrayname at the position given by the pointer
        Increment the pointer
        Get next character
    ENDWHILE
END read (arrayname)
```

### Example 5: Mainline with Subroutines (custom example)

```
# Main program to process student grades
BEGIN ProcessGrades
    # Load all student records from file
    load_students(student_list)

    # Calculate average for each student
    FOR i = 1 TO number_of_students
        SET average = calculate_average(student_marks[i], number_of_marks)
        DISPLAY student_names[i] + ": " + average
    NEXT i

    # Save results to output file
    save_results(student_list)
END ProcessGrades

# Load student data from the grades file into an array
BEGIN load_students (student_list)
    OPEN "grades.csv" FOR reading
    SET index = 1
    WHILE NOT end of file
        READ record FROM "grades.csv"
        SET student_list[index] = record
        SET index = index + 1
    ENDWHILE
    CLOSE "grades.csv"
END load_students (student_list)

# Calculate the average mark for a single student
BEGIN calculate_average (marks, number_of_marks)
    SET total = 0
    FOR j = 1 TO number_of_marks
        SET total = total + marks[j]
    NEXT j
    SET average = total / number_of_marks
    RETURN average
END calculate_average (marks, number_of_marks)
```

### Example 6: Selection and Repetition Combined (custom example)

```
# Validate user input - keep asking until valid
BEGIN get_valid_age
    SET valid = False
    REPEAT
        GET age
        IF age >= 0 AND age <= 150 THEN
            SET valid = True
        ELSE
            DISPLAY "Invalid age. Please enter a number between 0 and 150."
        ENDIF
    UNTIL valid = True
    RETURN age
END get_valid_age
```
