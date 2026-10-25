# Attempt: SQL 5 - read every word (2)

- Started: 2026-10-25T01:51:53.325Z · Submitted: 2026-10-25T02:10:50.580Z
- Auto-marked (MC + objective response): **0/0**. Written answers: to be marked by Claude.
- Time used: 19 min of 30 · Rest breaks: 0 (0 min)

---

## 1. Excursion payments

### Part A (3 marks, SQL)

The school wants a list of the Year 11 students who have not yet paid for the excursion, showing each student's name and the amount owing, with the student who owes the most listed first.

Write an SQL query to produce this list.

**Your answer:**

```
-- Y11
-- != paid 
-- F: Name | amount 
-- Order by high to low 

SELECT Students.Name, Payments.Amount
FROM Students, Payments
WHERE Students.StudentID = Payments.StudentID AND 
   Students.Year = 11 AND 
   Payments.Paid = 'No'
ORDER BY Payments.Amount DESC
   
```

*38 words*

---

## 2. Streaming report

### Part A (4 marks, SQL)

Construct a SQL query that displays, for each genre:

- the genre
- the number of views, with the heading Views
- the average minutes watched, with the heading AvgMinutes

Only include views of at least 30 minutes that were watched on a TV. List the results from the lowest to the highest average minutes watched.

**Your answer:**

```
-- F: genre | Number of views AS Views | AVE AS AvgMinutes
-- t > 30 min 
-- LOW to HIGH AVE

SELECT Genre, COUNT (Genre) AS Views,
  SUM (MinutesWatched)/COUNT (MinutesWatched) AS AvgMinutes
FROM Views
WHERE MinutesWatched >= 30
GROUP BY Genre
ORDER BY AvgMinutes DESC
```

*47 words*

---

## 3. Hawks goal table

### Part A (3 marks, SQL)

The coach of the Hawks wants the following report.

| Player | Goals |
|---|---|
| Kai Lomu | 4 |
| Leo Grant | 2 |
| Max Ortiz | 1 |

Write an SQL query that produces this result.

**Your answer:**

```
Select Players.Name AS Player, COUNT(GoalID) AS Goals
FROM Players, Goals
WHERE Players.PlayerID = Goals.PlayerID AND 
   Players.Team = 'Hawks'
GROUP BY Goals.PlayerID
ORDER BY Goals DESC
```

*25 words*

---

## 4. Who watched what (reading)

### Part A (2 marks, SHORT)

The following SQL query is run on the Views table.

```
SELECT UserName, Show
FROM Views
WHERE Genre = 'Drama' OR Genre = 'Documentary' AND Device = 'TV'
ORDER BY MinutesWatched ASC
```

Type the table of results produced by the query, with its column headings.

**Your answer:**

> UserName | Show
> ----------------------
> kira	Planet Earth
> sam	The Night Agent
> ava	         Planet Earth
> li	         The Night Agent
> 

*18 words*

---

## 5. Comedy watch times

### Part A (2 marks, SQL)

Write an SQL query to display the shortest and the longest time spent watching a comedy, with the headings Shortest and Longest.

**Your answer:**

```
SELECT MIN (MinutesWatched) as Shortest, MAX (MinutesWatched) AS Longest
FROM Views
WHERE Genre = 'Comedy'
```

*15 words*

---

## Timing

Time on each question (on screen; reading time and breaks excluded). Target ≈ 2 min per mark.

| Q | Marks | Time | Target | Visits | Started typing after | Words | Words/min |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 4:51 | 6:00 | 1 | 0:07 | 38 | 8 |
| 2 | 4 | 5:19 | 8:00 | 1 | 0:15 | 47 | 9 |
| 3 | 3 | 3:21 | 6:00 | 1 | 0:10 | 25 | 7 |
| 4 | 2 | 3:18 | 4:00 | 1 | 1:26 | 18 | 5 |
| 5 | 2 | 2:08 | 4:00 | 1 | 0:17 | 15 | 7 |

---

## Writing flow (from keystrokes)

### Writing flow: Q1

Typing 4:16 from first to last keystroke · 1:47 of that in pauses of 5 s or more · 42 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | -- Y11… | 0:03 | 2 | 47 | 0 | 0 |
| 2 | -- !… | 0:04 | 2 | 34 | 0 | 1 |
| 3 | = paid… | 0:18 | 2 | 7 | 1 | 2 |
| 4 | -- F: Name / amount… | 0:13 | 5 | 24 | 1 | 2 |
| 5 | -- Order by high to low… | 0:10 | 6 | 35 | 0 | 3 |
| 6 | SELECT Students.… | 0:08 | 2 | 15 | 0 | 4 |
| 7 | Name, Payments.… | 0:13 | 2 | 9 | 2 | 2 |
| 8 | Amount… | 0:08 | 1 | 8 | 0 | 6 |
| 9 | FROM Students, Payments… | 0:14 | 3 | 13 | 0 | 1 |
| 10 | WHERE Students.… | 0:20 | 2 | 6 | 1 | 2 |
| 11 | StudentID = Payments.… | 0:06 | 3 | 31 | 0 | 1 |
| 12 | StudentID AND… | 0:02 | 2 | 52 | 0 | 1 |
| 13 | Students.… | 0:16 | 1 | 4 | 1 | 1 |
| 14 | Year = 11 AND… | 0:04 | 4 | 57 | 0 | 3 |
| 15 | Payments.… | 0:14 | 1 | 4 | 1 | 6 |
| 16 | Paid = 'No'… | 0:25 | 3 | 7 | 1 | 3 |
| 17 | ORDER BY Payments.… | 0:12 | 3 | 14 | 1 | 4 |
| 18 | Amount DESC… | 0:12 | 2 | 10 | 1 | 0 |

**Longest pauses**: 16 s before “Students” · 15 s before “Students” · 10 s before “Payments” · 7.8 s before “Payments” · 5.8 s in the middle of “Name” · 5.1 s before “Payments”

**Most-corrected words** (backspaces): “Amount” 6 · “Payments” 3 · “by” 2 · “Name” 2 · “Students” 2 · “” 2 · “'No'” 2

**Slowest words per letter**: “Amount” 1.1 s/letter · “'No'” 1.0 s/letter · “Order” 0.8 s/letter · “SELECT” 0.7 s/letter · “Name” 0.6 s/letter · “FROM” 0.5 s/letter · “paid” 0.5 s/letter · “ORDER” 0.5 s/letter

### Writing flow: Q2

Typing 4:51 from first to last keystroke · 1:24 of that in pauses of 5 s or more · 60 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | -- F: genre / Number of views AS Views / AVE … | 0:30 | 13 | 26 | 1 | 4 |
| 2 | -- t > 30 min… | 0:13 | 5 | 22 | 1 | 0 |
| 3 | -- LOW to HIGH AVE… | 0:09 | 5 | 33 | 0 | 4 |
| 4 | SELECT Genre, COUNT (Genre) AS Views,… | 0:45 | 6 | 8 | 3 | 20 |
| 5 | SUM (MinutesWatched)/COUNT (MinutesWatched) A… | 0:26 | 5 | 12 | 1 | 11 |
| 6 | FROM Views… | 0:14 | 2 | 9 | 1 | 11 |
| 7 | WHERE MinutesWatched >= 30… | 0:30 | 4 | 8 | 2 | 5 |
| 8 | GROUP BY Genre… | 0:15 | 3 | 12 | 1 | 4 |
| 9 | ORDER BY AvgMinutes DESC… | 0:09 | 4 | 26 | 0 | 1 |

**Longest pauses**: 11 s before “Views” · 9.6 s before “AS” · 9.4 s before “Genre” · 7.5 s in the middle of “Genre” · 5.4 s before “MinutesWatched” · 5.1 s in the middle of “Number”

**Most-corrected words** (backspaces): “Genre” 7 · “genre” 2 · “MinutesWatched” 2

**Slowest words per letter**: “Genre” 0.9 s/letter · “SELECT” 0.8 s/letter · “Genre” 0.6 s/letter · “WHERE” 0.6 s/letter · “DESC” 0.5 s/letter · “Number” 0.4 s/letter · “GROUP” 0.4 s/letter · “ORDER” 0.4 s/letter

### Writing flow: Q3

Typing 3:04 from first to last keystroke · 0:24 of that in pauses of 5 s or more · 35 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | Select Players.… | 0:08 | 2 | 15 | 0 | 2 |
| 2 | Name AS Player, COUNT(GoalID) AS Goals… | 0:25 | 6 | 14 | 1 | 17 |
| 3 | FROM Players, Goals… | 0:11 | 3 | 17 | 0 | 0 |
| 4 | WHERE Players.… | 0:10 | 2 | 12 | 0 | 1 |
| 5 | PlayerID = Goals.… | 0:07 | 3 | 25 | 0 | 2 |
| 6 | PlayerID AND… | 0:12 | 2 | 10 | 1 | 0 |
| 7 | Players.… | 0:06 | 1 | 10 | 0 | 3 |
| 8 | Team = 'Hawks'… | 0:09 | 3 | 20 | 0 | 2 |
| 9 | GROUP BY Goals.… | 0:09 | 3 | 20 | 0 | 6 |
| 10 | PlayerID… | 0:10 | 1 | 6 | 1 | 1 |
| 11 | ORDER BY Goals DESC… | 0:09 | 4 | 28 | 0 | 1 |

**Longest pauses**: 7.8 s before “COUNTGoalID”

**Most-corrected words** (backspaces): “COUNTGoalID” 10 · “Players” 3 · “Goals” 2 · “'Hawks'” 2

**Slowest words per letter**: “WHERE” 0.9 s/letter · “GROUP” 0.9 s/letter · “Players” 0.8 s/letter · “Players” 0.8 s/letter · “ORDER” 0.7 s/letter · “Goals” 0.7 s/letter · “FROM” 0.6 s/letter · “'Hawks'” 0.6 s/letter

### Writing flow: Q4

Typing 1:49 from first to last keystroke · 0:40 of that in pauses of 5 s or more · 16 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | UserName / Show… | 0:04 | 3 | 44 | 0 | 2 |
| 2 | ----------------------… | 0:03 | 1 | 22 | 0 | 6 |
| 3 | kira	Planet Earth… | 0:30 | 3 | 6 | 1 | 0 |
| 4 | sam	The Night Agent… | 0:00 | 4 | 635 | 0 | 0 |
| 5 | ava	         Planet Earth… | 0:05 | 3 | 40 | 0 | 0 |
| 6 | li	         The Night Agent… | 0:15 | 4 | 15 | 1 | 8 |

**Longest pauses**: 30 s before “kira” · 9.9 s before “li”

**Most-corrected words** (backspaces): “Show” 2

**Slowest words per letter**: “Show” 0.3 s/letter · “----------------------” 0.1 s/letter

### Writing flow: Q5

Typing 1:34 from first to last keystroke · 0:43 of that in pauses of 5 s or more · 9 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT MIN (MinutesWatched) as Shortest, MAX … | 0:37 | 9 | 15 | 2 | 8 |
| 2 | FROM Views… | 0:32 | 2 | 4 | 1 | 0 |
| 3 | WHERE Genre = 'Comedy'… | 0:13 | 4 | 18 | 0 | 0 |

**Longest pauses**: 8.6 s before “MIN” · 6.8 s before “MAX”

**Slowest words per letter**: “'Comedy'” 0.5 s/letter · “WHERE” 0.4 s/letter · “FROM” 0.3 s/letter · “SELECT” 0.3 s/letter · “MinutesWatched” 0.1 s/letter · “Shortest” 0.0 s/letter
