# Attempt: SQL 2 - reading, joins and GROUP BY

- Started: 2026-10-25T00:58:45.992Z · Submitted: 2026-10-25T01:16:59.803Z
- Auto-marked (MC + objective response): **0/0**. Written answers: to be marked by Claude.
- Time used: 18 min of 28 · Rest breaks: 1 (0 min)

---

## 1. TH Trial Section II Question 1

### Part A (3 marks, SHORT)

Trace through the SQL query below and explain exactly what it returns, describing the effect of each clause in order.

```sql
SELECT category_id, COUNT(*)
FROM posts
WHERE published = 1
GROUP BY category_id;
```

**Your answer:**

> First you are useing the table "posts" this table has coumbs like published and category_id.
> you remove all the posts that are not pubised.
> Next you grouping it by category_id this will allow you to count the number in each catogory

*41 words*

🔎 Checked live (answer locked): self-marked

---

## 2. HSC SE 2025, Q22, SQL and Race Conditions

### Part A (2 marks, SQL)

Write an SQL query to generate the number of students at each level.

**Your answer:**

```
SELECT Level, COUNT(*)
FROM *
GROUP BY Level
```

*8 words*

🔎 Checked live (answer locked): self-marked

---

## 3. Practice Trial Exam 1 Q17

### Part A (3 marks, SQL)

**The following database tables store data for a mobile game app:**

#### Players
| PlayerID | Name     | Age | Country |
|----------|----------|-----|---------|
| P001     | Jack     | 15  | AU      |
| P002     | Riley    | 16  | NZ      |
| P003     | Sienna   | 17  | AU      |
| P004     | Oliver   | 14  | AU      |

#### Scores
| ScoreID | PlayerID | Points |
|---------|----------|--------|
| S001    | P001     | 1500   |
| S002    | P003     | 1800   |
| S003    | P004     | 900    |
| S004    | P002     | 1200   |

**Write an SQL query to show the names of Australian players who scored more than 1000 points.**

**Your answer:**

```
SELECT Players.Name, Scores.Points
FROM Scores, Players
WHERE Players.PlayerID = Scores.PlayerID AND 
   Players.Country = "AU" AND
   Scores.Points > 1000
```

*18 words*

🔎 Checked live (answer locked): self-marked

---

## 4. Question 22 sql

### Part A (5 marks, SQL)

Write a single SQL query to identify the top-performing product categories from all sales in 2024.

Your query must:

-   Only include transactions where the **Quantity** of items sold was greater than 1.
-   For each category, calculate and display:
    -   The category name.
    -   Total number of transactions.
    -   Total number of items sold.
    -   Average items sold per transaction.
    -   Total revenue (Unit_Price × Quantity, summed).
    -   The highest price of a single unit sold.
-   Sort the final results by **Total\_Revenue** in descending order.

**Your answer:**

```
SELECT Category,
   COUNT (Transaction_ID ) AS Number_of_Transactions,
   SUM (Quantity) as Total_Items_Sold,
   SUM (Quantity*1.0)/COUNT (Quantity*1.0) AS Average_Items_Per_Transaction,
   SUM(Unit_Price* Quantity) AS Total_Revenue,
   MAX (Unit_Price) AS Highest_Unit_Price

FROM Sales_Transactions
WHERE Quantity > 1
GROUP BY Category
ORDER BY Total_Revenue DESC
```

*37 words*

---

## Timing

Time on each question (on screen; reading time and breaks excluded). Target ≈ 2 min per mark.

| Q | Marks | Time | Target | Visits | Started typing after | Words | Words/min |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 2:50 | 6:00 | 2 | 0:25 | 41 | 14 |
| 2 | 2 | 2:01 | 4:00 | 4 | 0:30 | 8 | 4 |
| 3 | 3 | 3:49 | 6:00 | 4 | 0:47 | 18 | 5 |
| 4 | 5 | 9:14 | 10:00 | 2 | 0:32 | 37 | 4 |

---

## Writing flow (from keystrokes)

### Writing flow: Q1

Typing 2:07 from first to last keystroke · 0:00 of that in pauses of 5 s or more · 60 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | First you are useing the table "posts" this t… | 0:38 | 15 | 24 | 0 | 15 |
| 2 | you remove all the posts that are not pubised… | 0:14 | 9 | 38 | 0 | 10 |
| 3 | Next you grouping it by category_id this will… | 0:24 | 17 | 43 | 0 | 32 |

**Most-corrected words** (backspaces): “catogory” 7 · “useing” 5 · “posts” 2 · “table” 2 · “posts” 2 · “pubised” 2 · “category_id” 2

**Slowest words per letter**: “count” 0.8 s/letter · “posts” 0.8 s/letter · “pubised” 0.7 s/letter · “like” 0.7 s/letter · “table” 0.7 s/letter · “posts” 0.6 s/letter · “useing” 0.6 s/letter · “coumbs” 0.6 s/letter

### Writing flow: Q2

Typing 0:50 from first to last keystroke · 0:08 of that in pauses of 5 s or more · 12 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT Level, COUNT(*)… | 0:14 | 3 | 13 | 0 | 9 |
| 2 | FROM *… | 0:11 | 2 | 11 | 1 | 2 |
| 3 | GROUP BY Level… | 0:09 | 3 | 20 | 0 | 1 |

**Longest pauses**: 8.2 s before “”

**Most-corrected words** (backspaces): “Level” 9

**Slowest words per letter**: “Level” 1.1 s/letter · “COUNT” 1.0 s/letter · “Level” 0.9 s/letter · “GROUP” 0.5 s/letter · “FROM” 0.3 s/letter · “SELECT” 0.3 s/letter

### Writing flow: Q3

Typing 2:29 from first to last keystroke · 1:11 of that in pauses of 5 s or more · 11 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT Players.… | 0:03 | 2 | 47 | 0 | 3 |
| 2 | Name, Scores.… | 0:09 | 2 | 13 | 1 | 1 |
| 3 | Points… | 0:01 | 1 | 48 | 0 | 1 |
| 4 | FROM Scores, Players… | 0:09 | 3 | 19 | 0 | 0 |
| 5 | WHERE Players.… | 0:17 | 2 | 7 | 2 | 1 |
| 6 | PlayerID = Scores.… | 0:06 | 3 | 29 | 0 | 0 |
| 7 | PlayerID AND… | 0:13 | 2 | 9 | 1 | 0 |
| 8 | Players.… | 0:07 | 1 | 9 | 1 | 2 |
| 9 | Country = "AU" AND… | 0:10 | 4 | 24 | 0 | 1 |
| 10 | Scores.… | 0:07 | 1 | 8 | 1 | 2 |
| 11 | Points > 1000… | 0:35 | 3 | 5 | 1 | 0 |

**Longest pauses**: 8.1 s before “Players” · 6.6 s before “Scores” · 6.1 s before “Scores” · 5.4 s before “Players” · 5.3 s before “AND”

**Most-corrected words** (backspaces): “Players” 3 · “Players” 2 · “Scores” 2

**Slowest words per letter**: “1000” 0.6 s/letter · “Name” 0.5 s/letter · “SELECT” 0.2 s/letter · “WHERE” 0.2 s/letter · “Scores” 0.2 s/letter · “FROM” 0.2 s/letter · “Players” 0.1 s/letter · “Scores” 0.1 s/letter

### Writing flow: Q4

Typing 8:13 from first to last keystroke · 3:58 of that in pauses of 5 s or more · 188 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | SELECT Category,… | 0:20 | 2 | 6 | 1 | 146 |
| 2 | COUNT (Transaction_ID ) AS Number_of_Transact… | 0:21 | 5 | 14 | 1 | 3 |
| 3 | SUM (Quantity) as Total_Items_Sold,… | 0:36 | 4 | 7 | 4 | 0 |
| 4 | SUM (Quantity*1.… | 0:43 | 2 | 3 | 2 | 12 |
| 5 | 0)/COUNT (Quantity*1.… | 0:28 | 2 | 4 | 2 | 14 |
| 6 | 0) AS Average_Items_Per_Transaction,… | 0:26 | 3 | 7 | 2 | 6 |
| 7 | SUM(Unit_Price* Quantity) AS Total_Revenue,… | 0:46 | 4 | 5 | 4 | 3 |
| 8 | MAX (Unit_Price) AS Highest_Unit_Price… | 0:14 | 4 | 17 | 0 | 1 |
| 9 | FROM Sales_Transactions… | 0:33 | 2 | 4 | 1 | 2 |
| 10 | WHERE Quantity > 1… | 0:17 | 4 | 14 | 1 | 0 |
| 11 | GROUP BY Category… | 0:17 | 3 | 11 | 1 | 0 |
| 12 | ORDER BY Total_Revenue DESC… | 0:11 | 4 | 22 | 1 | 1 |

**Longest pauses**: 27 s in the middle of “Quantity1” · 21 s before “SUMUnit_Price” · 13 s before “Average_Items_Per_Transaction” · 13 s before “Category” · 9.2 s before “COUNT” · 7.8 s in the middle of “Total_Items_Sold”

**Most-corrected words** (backspaces): “0COUNT” 14 · “Quantity1” 12 · “Sales_Transactions” 2

**Slowest words per letter**: “0COUNT” 1.1 s/letter · “Category” 0.6 s/letter · “ORDER” 0.4 s/letter · “Quantity1” 0.4 s/letter · “WHERE” 0.3 s/letter · “GROUP” 0.3 s/letter · “COUNT” 0.3 s/letter · “DESC” 0.2 s/letter
