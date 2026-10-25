# Attempt: Python 1 - greatest product (Normanhurst)

- Started: 2026-10-25T05:18:55.649Z · Submitted: 2026-10-25T06:55:42.235Z
- Auto-marked (MC + objective response): **0/0**. Written answers: to be marked by Claude.
- Time used: 97 min of 10 · Rest breaks: 0 (0 min) · Clock stopped for reports/marking: 1 (0 min)

---

## 1. SE: Code (4)

### Part A (4 marks, CODING)

In the 20 x 20 grid below, four numbers along a row have been marked in red.

08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
81 49 31 73 55 79 14 **29 93 71 40** 67 53 88 30 03 49 13 36 65
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48

The product of these numbers is 7,759,480.

Write a function in Python called 'GreatestProduct' which takes in a 2D array (20 x 20) and returns the greatest product of four adjacent numbers in the same direction (up, down, left, or right).

**Your answer:**

```
# The grid from the question, so you can test your function.
grid = [
    [8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
    [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0],
    [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
    [52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
    [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
    [24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
    [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
    [67, 26, 20, 68, 2, 62, 12, 20, 95, 63, 94, 39, 63, 8, 40, 91, 66, 49, 94, 21],
    [24, 55, 58, 5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
    [21, 36, 23, 9, 75, 0, 76, 44, 20, 45, 35, 14, 0, 61, 33, 97, 34, 31, 33, 95],
    [78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 3, 80, 4, 62, 16, 14, 9, 53, 56, 92],
    [16, 39, 5, 42, 96, 35, 31, 47, 55, 58, 88, 24, 0, 17, 54, 24, 36, 29, 85, 57],
    [86, 56, 0, 48, 35, 71, 89, 7, 5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
    [19, 80, 81, 68, 5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 4, 89, 55, 40],
    [4, 52, 8, 83, 97, 35, 99, 16, 7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
    [88, 36, 68, 87, 57, 62, 20, 72, 3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
    [4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18, 8, 46, 29, 32, 40, 62, 76, 36],
    [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 4, 36, 16],
    [20, 73, 35, 29, 78, 31, 90, 1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 5, 54],
    [1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48],
]

def calc_prod(arr):
    i = 1
    for a in arr:
        i *= a
    return int(i)
def max_prod_for_arr(g):
    max_v = 0
    for i in range(0,20):
        val = calc_prod(g[i:min(i+4,20)])
        if max_v < val:
            max_v = val
    return max_v
    
def GreatestProduct(grid):
    # this will do the row
    maxi = 0
    for g in grid:
       if maxi < max_prod_for_arr(g):
            maxi = max_prod_for_arr(g)

    for i in range(20):
        g = []
        for j in range(20):
            g.append(grid[j][i])

        if maxi < max_prod_for_arr(g):
            maxi = max_prod_for_arr(g)

    return maxi
              
        
print(GreatestProduct(grid))
```

*495 words*

✏️ Edited after feedback. Attempt 1 (Claude 2/4):

> # The grid from the question, so you can test your function.
> grid = [
>     [8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
>     [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0],
>     [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
>     [52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
>     [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
>     [24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
>     [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
>     [67, 26, 20, 68, 2, 62, 12, 20, 95, 63, 94, 39, 63, 8, 40, 91, 66, 49, 94, 21],
>     [24, 55, 58, 5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
>     [21, 36, 23, 9, 75, 0, 76, 44, 20, 45, 35, 14, 0, 61, 33, 97, 34, 31, 33, 95],
>     [78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 3, 80, 4, 62, 16, 14, 9, 53, 56, 92],
>     [16, 39, 5, 42, 96, 35, 31, 47, 55, 58, 88, 24, 0, 17, 54, 24, 36, 29, 85, 57],
>     [86, 56, 0, 48, 35, 71, 89, 7, 5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
>     [19, 80, 81, 68, 5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 4, 89, 55, 40],
>     [4, 52, 8, 83, 97, 35, 99, 16, 7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
>     [88, 36, 68, 87, 57, 62, 20, 72, 3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
>     [4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18, 8, 46, 29, 32, 40, 62, 76, 36],
>     [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 4, 36, 16],
>     [20, 73, 35, 29, 78, 31, 90, 1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 5, 54],
>     [1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48],
> ]
> 
> def calc_prod(arr):
>     i = 1
>     for a in arr:
>         i *= a
>     return a
>     
> def GreatestProduct(grid):
>     # this will do the row
>     max_v = 0
>     for g in grid:
>         max_r = 0
>         for i in range(0,20-3):
>              if max_v > (val := calc_prod(i[i:i+4])):
>                 max_v = val
> 
>     max_v = 0
>     for i in range(20):
>         g = []
>         for j in range(20):
>             g.append(grid[i][j])
>         max_c = prod
>         for i in range(0,20-3):
>             if max_v > (val := calc_prod(i[i,i+4])):
>                 max_v = val
>     return max_v
>               
>         
> print(GreatestProduct(grid))
> 

---

## Timing

Time on each question (on screen; reading time and breaks excluded). Target ≈ 2 min per mark.

| Q | Marks | Time | Target | Your plan | Visits | Started typing after | Words | Words/min |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 29:24 ⚠ long | 8:00 | 7:30 | 1 | 0:14 | 495 | 17 |

Time with the exam window in the background: 1:00.

---

## Writing flow (from keystrokes)

### Writing flow: Q1

Typing 26:21 from first to last keystroke · 6:40 of that in pauses of 5 s or more · 996 characters deleted.

| # | Sentence (start) | Time | Words | Words/min | Pauses ≥5 s | Backspaces |
|---|---|---|---|---|---|---|
| 1 | for i in range (grid})[10,1020)-43:… | 0:33 | 5 | 9 | 1 | 0 |
| 2 | #      manum =  {[]0[00{[0]*4grid… | 0:33 | 4 | 7 | 1 | 0 |
| 3 | gr… | 0:02 | 1 | 33 | 0 | 0 |
| 4 | for f i in range (0,20-3):… | 0:12 | 6 | 30 | 0 | 0 |
| 5 | fo… | 0:03 | 1 | 21 | 0 | 0 |
| 6 | num = [0]*4… | 0:01 | 3 | 290 | 0 | 0 |
| 7 | namdef calc _prod(arr):… | 0:26 | 3 | 7 | 1 | 0 |
| 8 | i = 0… | 0:03 | 3 | 58 | 0 | 0 |
| 9 | fofor i in arr:… | 0:04 | 4 | 56 | 0 | 0 |
| 10 | 1… | 0:02 | 1 | 35 | 0 | 0 |
| 11 | i + *= aa… | 0:06 | 4 | 37 | 0 | 0 |
| 12 | retrunurn turn     a… | 0:11 | 3 | 17 | 0 | 0 |
| 13 | if av xmax_v_v > ival (cval ::-= i[0i,i+4}])p… | 1:05 | 8 | 7 | 2 | 0 |
| 14 | ``                max_v = val… | 0:08 | 4 | 31 | 0 | 0 |
| 15 | ``… | 0:06 | 1 | 10 | 0 | 0 |
| 16 | # this will do the row… | 0:16 | 6 | 22 | 1 | 0 |
| 17 | for g in grid:… | 0:10 | 4 | 24 | 1 | 0 |
| 18 | max_v = prod… | 0:00 | 3 | – | 0 | 0 |
| 19 | for i in range(0,20-3):… | 0:00 | 4 | – | 0 | 0 |
| 20 | if max_v > (val := calc_prod(i[i,i+4])):… | 0:00 | 6 | – | 0 | 0 |
| 21 | max_v = val… | 0:00 | 3 | – | 0 | 0 |
| 22 | {[:}]{[i for i in i in range (ge(20)… | 0:47 | 8 | 10 | 3 | 0 |
| 23 | g = for i     j in raingange(20);:… | 0:16 | 7 | 26 | 0 | 0 |
| 24 | g = []g.… | 0:06 | 3 | 32 | 0 | 0 |
| 25 | appednnd(ii ,grid[i,][j[])vhrcr… | 0:32 | 2 | 4 | 1 | 0 |
| 26 | retruntrurn mavx(max_v,max_r)            prod… | 1:05 | 6 | 6 | 5 | 0 |
| 27 | m    max_v = 0    max_v = 0… | 0:04 | 7 | 95 | 0 | 0 |
| 28 | 0vaxv_v… | 0:07 | 1 | 9 | 0 | 0 |
| 29 | 4i+if max_v > (val := calc_prod(i[i,i+4])):… | 0:06 | 6 | 59 | 0 | 0 |
| 30 | #0}][  :min(i+4,20)<… | 0:29 | 2 | 4 | 2 | 0 |
| 31 | val = calc_prod(i[i:min(i+4,20)]) v iin t (i)… | 0:21 | 7 | 20 | 1 | 0 |
| 32 | degf max _facprod_for_rowarr(arr)g):… | 0:15 | 3 | 12 | 0 | 0 |
| 33 | max_r = 0… | 0:00 | 3 | 376 | 0 | 0 |
| 34 | for i in range(0,20):… | 0:00 | 4 | – | 0 | 0 |
| 35 | val = calc_prod(g[i:min(i+4,20)])… | 0:00 | 3 | – | 0 | 0 |
| 36 | if max_v < val:… | 0:00 | 4 | – | 0 | 0 |
| 37 | max_v = val… | 0:11 | 3 | 17 | 1 | 0 |
| 38 | max_prod_for_arr(g)mav if ma=vvif… | 0:17 | 3 | 11 | 1 | 0 |
| 39 | ma        maxi = 0if Mnamaxi >< = :… | 0:20 | 8 | 24 | 0 | 0 |
| 40 | maxi = max_prod_for_arr(g)… | 0:19 | 3 | 9 | 1 | 0 |
| 41 | if maxi < max_prod_for_arr(g):… | 0:02 | 4 | 136 | 0 | 0 |
| 42 | maxi = max_prod_for_arr(g)\… | 0:02 | 3 | 94 | 0 | 0 |
| 43 | for i in range(20):… | 0:05 | 4 | 44 | 0 | 0 |
| 44 | g = []… | 0:00 | 3 | – | 0 | 0 |
| 45 | for j in range(20):… | 0:00 | 4 | – | 0 | 0 |
| 46 | g.… | 0:00 | 1 | – | 0 | 0 |
| 47 | append(grid[i][j])… | 0:02 | 1 | 28 | 0 | 0 |
| 48 | i… | 0:26 | 1 | 2 | 2 | 0 |
| 49 | ``                            retrun max_v   … | 1:32 | 4 | 3 | 1 | 0 |
| 50 | iigg            print(len(g))… | 0:11 | 2 | 10 | 0 | 0 |
| 51 | print(g)ji… | 0:04 | 1 | 15 | 0 | 0 |

**Longest pauses**: 15 s in the middle of “00004grid” · 12 s before “ge20” · 11 s before “i0ii4prodcalc_roodprod” · 9.7 s in the middle of “grid101020-43” · 9.5 s in the middle of “namdef” · 8.9 s before “i”

**Slowest words per letter**: “mini420” 1.9 s/letter · “_prodarr” 1.5 s/letter · “grid101020-43” 1.3 s/letter · “gridijvhrcr” 1.3 s/letter · “020-3” 1.2 s/letter · “ge20” 1.2 s/letter · “00004grid” 1.1 s/letter · “i0ii4prodcalc_roodprod” 1.0 s/letter
