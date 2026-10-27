seats = [
    [1,1,1,1,0,0],
    [1,0,1,0,0,0],
    [1,1,1,1,1,0],
    [1,0,1,1,1,1]
]

def find_seats(seats, num_seats):
    break_out = False
    str_to_find = "0"*num_seats
    str_seats = []
    for row in seats:
        string = ' '.join(map(str,row))
        string.re
        string.replace(string,str_to_find,1)
        if string != ' '.join(map(str,row)):
            break_out = True
        str_seats.append(string)
    for i in str_seats:
        i = list(i)
        i = map(int,row)
    return break_out
    
print(find_seats(seats,1))

# def print_seats(seats):
#     for row in seats:
#         print(' '.join(map(str,row)))
# print_seats(seats)