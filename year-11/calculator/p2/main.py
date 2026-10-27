# King's Calculator
import os 
import datetime
import shutil


# makes a valid file
def make_file():
    global file_name
    global folder_name    

    try:
        os.mkdir(folder_name:="calculations")
    except FileExistsError:
        shutil.rmtree(folder_name)
        os.mkdir(folder_name:="calculations")

    with  open(file_name := "calculations/calcs.txt",'w') as calcs:
        calcs.close()
        


def get_date():
    return [datetime.date.today().day,datetime.date.today().month,datetime.date.today().year]

def convert_to_roman_numerals(date):
    global final_date

    final_date = []

    # i know bad naming sorry
    for date in date:
        # this will convet integers to roman numrels but it will not do the optimisaton that like 4 = iv
        temp_date = date
        roman_date = ""

        for i in [[1000,"M"],[500,"M"],[100,"C"],[50,"L"],[10,"X"],[5,"V"],[1,"I"]]:
           while temp_date - i[0] >= 0:
                roman_date += i[1]
                temp_date -= i[0]
    
        
        # do the optimisaton like 4 = iv
        roman_date = roman_date.replace("DCCCC", "CM")
        roman_date = roman_date.replace("CCCC", "CD")
        roman_date = roman_date.replace("LXXXX", "XC")
        roman_date = roman_date.replace("XXXX", "XL")
        roman_date = roman_date.replace("VIIII", "IX")
        roman_date = roman_date.replace("IIII", "IV")

        

        final_date.append(roman_date)
    final_date = final_date[0] + "." + final_date [1] + "." + final_date[2]
    return final_date
    
def deci_to_morce(num_base_10):
    morce_dict = {
        0 : "-----",
        1 : ".----",
        2 : "..---",
        3 : "...--",
        4 : "....-",
        5 : ".....",
        6 : "-....",
        7 : "--...",
        8 : "---..",
        9 : "----.",}
    # split into a array that has each diget seperat
    num_base_10_array = []
    num_base_10 = str(num_base_10)
    for i in range(len(num_base_10)):
        num_base_10_array.append(int(num_base_10[i]))
    del num_base_10
    num_base_morce = ""

    for number in num_base_10_array:
        num_base_morce = f"{num_base_morce}" + " " f"{morce_dict[number]}"

    return num_base_morce        

def change_first_line():
    with open(file_name,"r") as calcs:
        old_file_contence = calcs.readlines()
        calcs.close()

    old_file_contence.insert(0, "Total calculations: " + deci_to_morce(str(len(old_file_contence)))+'\n')

    with open(file_name,"w+") as calcs:
        calcs.writelines(old_file_contence)
        calcs.close()


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
    change_first_line() 
    calcs.close()
    print("I hope you had fun doing maths ;)")
    exit()


# to make the global var calcs
make_file()
print("press ctrl+c to quit")


while True:
    # call to init the globe var in loop in case use in multiple days 
    convert_to_roman_numerals(get_date())
    try:
        print(text := menu())
        with open(f"{file_name}","a+") as calcs:
            if "None" in str(text):
                continue
            calcs.write(f"Timestamp {final_date}: {text}")
            calcs.close()
    except KeyboardInterrupt:
        change_first_line() 
        print("I hope you had fun doing maths :)")
        calcs.close()
        break


