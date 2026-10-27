BEGIN main

BEGIN get_input()
DISPLAY "number 1"
get number-1 = INPUT 
DISPLAY "number 2"
get number-2 = INPUT 

TRY:
    TRY:
        SET number-1 = int(number-1) 
        SET number-2= int(number-2) 
    EXCEPT Value_Erorr:
        SET number-1 = float(number-1) 
        SET number-2= float(number-2) 
EXCEPT:
    DISPLAY somthing went wrong
    RETURN get_input()

    
       
BEGIN add(num)

BEGIN subtract(num)
BEGIN multiply(num)
BEGIN division(num) 
BEGIN menu()
DISPLAY 
"Please insert a letter
    Menu:
    a for addition
    s for subtraction
    m for multiplication
    d for division
    t for draw triangle
"   
get menu_choice = INPUT 

IF menu_choice = a
