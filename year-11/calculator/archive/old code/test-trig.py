import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from math import *

def get_angles():
    while True:
        # get inputs for angle's
        angle_A = 60 # float(input("Angle 1: "))
        angle_B = 60 # float(input("Angle 2: "))
        angle_C = 60 # float(input("Angle 3: "))

                # check if valid triangle
        if angle_A + angle_B + angle_C != 180 and angle_A * angle_B * angle_C != 0:
            print("This is not a valid triangle")
            continue
    
        angle_A = radians(angle_A)
        angle_B = radians(angle_B)
        angle_C = radians(angle_C)

        return [angle_A,angle_B,angle_C]

def triangle(angle_ABC):

    angle_A = angle_ABC[0]
    angle_B = angle_ABC[1]
    angle_C = angle_ABC[2]

    known_side_length = 1
    unknown_side_length_to_use_in_trig = (sin(angle_C)*known_side_length)/sin(angle_A)
    testing_side_length = sin(angle_B)*known_side_length/sin(angle_A)

    print("side a",known_side_length)
    print("side b",unknown_side_length_to_use_in_trig)
    print("side c",testing_side_length)

    """
    the c point is = (0,0) as I have defind it to be at the orign
    the b pint is = (1,0) as it has a bace lenth of 1 and a is the bottem of the triangle
    the unknoen point is acheve by maing a right angle triangle whith the angle c knowen and the b length then we slove the x and y conponits
    """
    x_unknown = sin(angle_B)*unknown_side_length_to_use_in_trig
    y_unknown = cos(angle_B)*unknown_side_length_to_use_in_trig

    points_x = [0,1,x_unknown]
    points_y = [0,0,y_unknown]
    print(points_x,points_y)

    # plt.figure()
    plt.axis('equal')
    plt.fill(points_x, points_y)
    plt.savefig("triangle.png")

    plt.show()





triangle(get_angles())

