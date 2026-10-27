import random 
import math

# city = (random.random() * 100,random.random()* 100)
city = (0,0)
array_citys = [(10,10)]

for _ in range(100):
    array_citys.append((random.random() * 100,random.random()* 100))

def dist(p1,p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)
        
def closest(cit,list):
    cords = (0,0)
    shortest_dist = dist(cit,list[0]) *-1 
    for i in list:
        print(dist(cit,i))
        if (dist(cit,i) *-1) > shortest_dist:
            shortest_dist = dist(cit,i) *-1
            cords = i
    print(cords)
    return cords
        
closest(city,array_citys)
