# Attempt: SQL 3 - read every word

- Started: 2026-10-25T01:28:00.925Z · Submitted: 2026-10-25T01:49:29.757Z
- Auto-marked (MC + objective response): **0/0**. Written answers: to be marked by Claude.
- Time used: 21 min of 26 · Rest breaks: 0 (0 min)

---

## 1. Library reminders

### Part A (3 marks, SQL)

The library wants to send reminders to members who live in Hornsby and still have a book that was borrowed in 2025 and has not been returned.

Write an SQL query to display the member names and book titles for these loans, in alphabetical order by member name.

**Your answer:**

```
SELECT Members.Name, Loans.BookTitle, Loans.LoanDate
FROM Loans, Members
WHERE Loans.MemberID = Members.MemberID AND
   LoanDate >= '2025-01-01' AND LoanDate < '2026-01-10' AND
   Loans.Returned = 'No'
ORDER BY Members.Name ASC
```

*27 words*

---

## 2. Gym visits (reading)

### Part A (2 marks, SHORT)

The following SQL query is run on the Sessions table.

```
SELECT MemberName, COUNT(SessionID) AS Visits
FROM Sessions
WHERE Minutes >= 50 AND Status = 'Attended'
GROUP BY MemberName
ORDER BY MemberName DESC
```

Type the table of results produced by the query, with its column headings.

**Your answer:**

> MemberName |  Visits
> Eve                       | 1
> Dev                       | 1
> Ben                       | 1
> Ana                       | 2 

*15 words*

---

## 3. Gym class report

### Part A (4 marks, SQL)

Construct a SQL query that displays, for each class:

- the class name
- the number of sessions attended, with the heading Attended
- the total minutes attended, with the heading TotalMinutes

Cancelled sessions must not be counted. List the results from the highest to the lowest total minutes.

**Your answer:**

```
SELECT Class,
   COUNT (Status) AS Attended,
   SUM (Minutes) AS TotalMinutes
FROM Sessions
WHERE Status = 'Attended'
GROUP BY Class
```

*19 words*

🔎 Checked live (answer locked): self-marked

---

## 4. Café drinks report

### Part A (3 marks, SQL)

The café manager wants the following report.

| Drink | NumberSold |
|---|---|
| Tea | 4 |
| Latte | 3 |
| Mocha | 1 |

Write an SQL query that produces this result.

**Your answer:**

```
SELECT Menu.ItemName AS Drink,
   sum(Orders.Qty) AS NumberSold
FROM Menu, Orders
WHERE Menu.ItemID = Orders.ItemID AND
   Menu.Category = 'Drink'
GROUP BY Menu.ItemName
ORDER BY Drink DESC
```

*25 words*

---

## Timing

Time on each question (on screen; reading time and breaks excluded). Target ≈ 2 min per mark.

| Q | Marks | Time | Target | Visits | Started typing after | Words | Words/min |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 9:49 ⚠ long | 6:00 | 1 | 0:30 | 27 | 3 |
| 2 | 2 | 3:45 | 4:00 | 4 | 0:13 | 15 | 4 |
| 3 | 4 | 4:05 | 8:00 | 4 | 0:16 | 19 | 5 |
| 4 | 3 | 3:50 | 6:00 | 1 | 0:13 | 25 | 7 |

---

## Writing flow (from keystrokes)

### Writing flow: Q1

Typing 9:17 from first to last keystroke · 1:52 of that in pauses of 5 s or more · 187 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT Members.… | 0:07 | 2 | 17 | 0 | 1 |
| 2 | Name, Loans.… | 0:06 | 2 | 20 | 0 | 5 |
| 3 | BookTitle, Loans.… | 0:28 | 2 | 4 | 1 | 1 |
| 4 | LoanDate… | 0:01 | 1 | 49 | 0 | 7 |
| 5 | FROM Loans, Members… | 0:14 | 3 | 13 | 1 | 0 |
| 6 | WHERE Loans.… | 0:22 | 2 | 6 | 2 | 11 |
| 7 | MemberID = Members.… | 0:03 | 3 | 72 | 0 | 1 |
| 8 | MemberID AND… | 0:06 | 2 | 19 | 0 | 38 |
| 9 | LoanDate >= '2025-01-01' AND LoanDate < '2026… | 1:12 | 8 | 7 | 3 | 102 |
| 10 | Loans.… | 0:17 | 1 | 4 | 1 | 1 |
| 11 | Returned = 'No'… | 0:07 | 3 | 24 | 0 | 15 |
| 12 | ORDER BY Members.… | 0:15 | 3 | 12 | 1 | 3 |
| 13 | Name ASC… | 0:02 | 2 | 58 | 0 | 2 |

**Longest pauses**: 21 s in the middle of “BookTitle” · 18 s in the middle of “'2025-01-01'” · 15 s before “Loans” · 14 s before “LoanDate” · 13 s in the middle of “Loans” · 10 s before “Members”

**Most-corrected words** (backspaces): “AND” 26 · “LoanDate” 21 · “'2025-01-01'” 15 · “'2026-01-10'” 15 · “'No'” 12 · “WHERE” 7 · “Name” 4 · “Loans” 3

**Slowest words per letter**: “'No'” 1.0 s/letter · “'2025-01-01'” 0.7 s/letter · “Loans” 0.6 s/letter · “ORDER” 0.6 s/letter · “'2026-01-10'” 0.6 s/letter · “WHERE” 0.3 s/letter · “Loans” 0.2 s/letter · “Members” 0.2 s/letter

### Writing flow: Q2

Typing 3:21 from first to last keystroke · 0:00 of that in pauses of 5 s or more · 80 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | MemberName /  Visits… | 0:09 | 3 | 19 | 0 | 69 |
| 2 | Eve                       / 1… | 0:06 | 3 | 28 | 0 | 1 |
| 3 | Dev                       / 1… | 0:13 | 3 | 13 | 0 | 3 |
| 4 | Ben                       / 1… | 0:05 | 3 | 33 | 0 | 4 |
| 5 | Ana                       / 2… | 0:16 | 3 | 11 | 0 | 3 |

### Writing flow: Q3

Typing 3:19 from first to last keystroke · 1:06 of that in pauses of 5 s or more · 175 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT Class,… | 0:12 | 2 | 10 | 1 | 1 |
| 2 | COUNT (Status) AS Attended,… | 0:21 | 4 | 11 | 1 | 10 |
| 3 | SUM (Minutes) AS TotalMinutes… | 0:24 | 4 | 10 | 1 | 3 |
| 4 | FROM Sessions… | 0:08 | 2 | 16 | 0 | 0 |
| 5 | WHERE Status = 'Attended'… | 0:30 | 4 | 8 | 2 | 8 |
| 6 | GROUP BY Class… | 0:29 | 3 | 6 | 1 | 5 |

**Longest pauses**: 20 s before “GROUP” · 13 s before “WHERE” · 10 s before “SUM” · 9.6 s before “Status” · 7.0 s in the middle of “SELECT” · 5.3 s before “COUNT”

**Most-corrected words** (backspaces): “Status” 8 · “GROUP” 5

**Slowest words per letter**: “Class” 1.2 s/letter · “FROM” 0.4 s/letter · “SELECT” 0.4 s/letter · “Class” 0.3 s/letter · “WHERE” 0.3 s/letter · “Status” 0.3 s/letter · “Minutes” 0.3 s/letter · “COUNT” 0.3 s/letter

### Writing flow: Q4

Typing 3:29 from first to last keystroke · 1:23 of that in pauses of 5 s or more · 37 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT Menu.… | 0:15 | 2 | 8 | 1 | 4 |
| 2 | ItemName AS Drink,… | 0:13 | 3 | 14 | 0 | 1 |
| 3 | sum(Orders.… | 0:12 | 1 | 5 | 1 | 7 |
| 4 | Qty) AS NumberSold… | 0:13 | 3 | 14 | 1 | 2 |
| 5 | FROM Menu, Orders… | 0:16 | 3 | 11 | 1 | 0 |
| 6 | WHERE Menu.… | 0:15 | 2 | 8 | 2 | 7 |
| 7 | ItemID = Orders.… | 0:07 | 3 | 27 | 1 | 2 |
| 8 | ItemID AND… | 0:20 | 2 | 6 | 1 | 0 |
| 9 | Menu.… | 0:05 | 1 | 11 | 0 | 1 |
| 10 | Category = 'Drink'… | 0:05 | 3 | 37 | 0 | 10 |
| 11 | GROUP BY Menu.… | 0:11 | 3 | 16 | 1 | 1 |
| 12 | ItemName… | 0:14 | 1 | 4 | 1 | 0 |
| 13 | ORDER BY Drink DESC… | 0:08 | 4 | 32 | 0 | 2 |

**Longest pauses**: 10 s before “SELECT” · 8.6 s in the middle of “Menu” · 8.6 s before “Menu” · 6.5 s before “Menu” · 6.0 s before “sumOrders” · 5.9 s in the middle of “Orders”

**Most-corrected words** (backspaces): “'Drink'” 7 · “WHERE” 6 · “sumOrders” 5 · “” 2

**Slowest words per letter**: “Drink” 0.8 s/letter · “ItemID” 0.6 s/letter · “DESC” 0.6 s/letter · “ORDER” 0.5 s/letter · “GROUP” 0.4 s/letter · “Menu” 0.4 s/letter · “Drink” 0.4 s/letter · “'Drink'” 0.3 s/letter
