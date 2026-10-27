# Equilateral, Isosceles, Scalene,   Right-angled
lengths = [1,1,1]

def right_angle(tri):
    tri.sort()
    tri = tri[::-1]
    a = tri[2]
    b = tri[1]
    c = tri[0]
    
    if a**2 + b**2 == c**2:
        return "Right-angled"
    else:
        return "Not right angle"
def tYpe(tri):
    tri.sort()
    tri = tri[::-1]
    a = tri[2]
    b = tri[1]
    c = tri[0]
    
    if a == b == c:
        return "Equilateral"
    elif a == b or b==c:
        print("Isosceles")
    else:
        print("Scalene")

print(tYpe(lengths))
print(right_angle(lengths))