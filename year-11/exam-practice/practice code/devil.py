import math
num = 43987

def lenght(num):
    lenght = 0
    while True:
        if num // 1 * 10**lenght <= 0:
            return lenght
        print(1 * 10**lenght/num)
        print(1 * 10**lenght)
        lenght += 1

print(lenght(num))