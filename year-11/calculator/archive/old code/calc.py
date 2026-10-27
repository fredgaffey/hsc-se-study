print("""Kings Calculator:
You can input a calulton using aditon subtractn and deiton using like in a casio 
Note: you can use any pyton notation
for example 
1 + 4 = 5
1 - 4 = -3 
1 * 4 = 4 
1 / 4 = 0.25

""")
digits = [1,2,3,4,5,6,7,8,9,0]
symbols_allowed  = """!%^*/+-=()""" 

# Modify the string from algebraic notaton to pyton notation
def process_string():
    eq = input(">")
# )( with is not vaild to )*( which is not vaild
    for i in range(len(eq)):
        # print(eq[i:i+2])
        if eq[i:i+1] == ")(":
            eq = eq[:i+1] + "*" + eq[1+i:]
    print(eq)
# n(1+3) which is not vaild to n*(1+3) 
    for i in range(len(eq)):
        for j in digits: 
            if eq[i:i+2] == f"{j}(":
                eq = eq[:i+1] + "*" + eq[1+i:]
    print(eq)
    try:
        for i in eq:
            if i not in symbols_allowed or i not in digits:
                print("The equaton is invalad")
                process_string()
            else:
                eval(eq)
                return eq
    except:
        process_string()


while True:
    print(eval(process_string()))
