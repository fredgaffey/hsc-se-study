# King's Calculator

def menu():
    global menu_choice 
    print("""Please insert a letter
    Menu:
    a for addition
    m for multiplication
    s for subtraction
    d for division
    q for quit""")
    menu_choice = input(">")

# check the menu is choice valid then call the relevent oporation
    match menu_choice:
        case "a" : return addition(get_and_clean_input(menu_choice)) # adds the user input
        case "s" : return subtraction(get_and_clean_input(menu_choice)) # subtracs the user input
        case "m" : return multiplication(get_and_clean_input(menu_choice)) # multipled the user input
        case "d" : return division(get_and_clean_input(menu_choice)) # divied the user input
        case "q" : quit()  
        case _ : print("Something whent wrong"); menu() # recursively calls menu 



def get_and_clean_input(menu_choice):
    num1 = input("Input the first number: ")
    num2 = input("Input the second number: ")

    # This converts a string to a number. If it can be converted to an integer, 
    # it will be converted to a float. If it cannot be converted to float.
    # Then a You have made a typo make shure you input a valid number will be printed then
    # function will be recursively called.
    try:
        try:    
            num1,num2 = int(num1),int(num2)
        except:
            num1,num2 = float(num1),float(num2)
    except:
        print("You have made a typo make sure you input a valid number")
        print("")
        return get_and_clean_input(menu_choice)

    try:
        if menu_choice == "d":
            _ = num1/num2
    except ZeroDivisionError:
        print("you have a Zero Divisor")
        return get_and_clean_input("d")
    return num1, num2
    
# Since the get_and_clean_input outputs a tuple than the first and second elemtes are added
def addition(num):
    return f"{num[0]} + {num[1]} = {num[0]+num[1]}"+ "\n" 
    # return num[0]+num[1]

# Since the get_and_clean_input outputs a tuple than the first and second elemtes are subtraced
def subtraction(num):
    return f"{num[0]} - {num[1]} = {num[0]-num[1]}"+ "\n" 
    # return num[0]-num[1]

# Since the get_and_clean_input outputs a tuple than the first and second elemtes are multipled
def multiplication(num):
    return f"{num[0]} x {num[1]} = {num[0]*num[1]}"+ "\n" 
    # return num[0]*num[1]

# Since the get_and_clean_input outputs a tuple than the first and second elemtes are divied
def division(num):
    return f"{num[0]} ÷ {num[1]} = {num[0]/num[1]}"+ "\n" 
    # return num[0]/num[1]

def quit():
    print("I hope you had fun doing maths ;)")
    exit()


# to make the global var calcs
print("press ctrl+c to quit")


while True:
    # call to init the globe var in loop in case use in multiple days 
    try:
        print(menu())
    except KeyboardInterrupt:
        print("I hope you had fun doing maths :)")
        break
