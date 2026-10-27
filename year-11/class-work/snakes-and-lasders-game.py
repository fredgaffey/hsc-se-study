import random
win = False
b = range(1,101)
for i in b:
    if random.randrange(10) ==0:
        i = random.randrange(-10,10)
p1 = 0
p2 = 0
while win == False:
    input(f"p1 at {p1} p2 at {p2}")
    input("p1 turn")
    rool = random.randrange(1,7)
    print(f"p1 roolled {rool}")
    try:
        p1 = b[p1+ rool] + rool
    except IndexError:
        print("p1 win")
        win = True 
    if p1 >= 100:
        win = True
        print("p1 wins")
    input("p2 turn")
    rool = random.randrange(1,7)
    print(f"p2 roolled {rool}")
    try:
        p2 = b[p1+ rool] + rool
    except IndexError:
        print("p2 win")
        win = True 
    if p2 >= 100:
        win = True
        print("p2 wins")
