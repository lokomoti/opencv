# various calculations with coordinates

import math

def test(x):
    out = "you entered: " + str(x)
    return out

def angle(x0, y0, x1, y1, x2, y2):
    print("nothing here so far")

def distance(x0, y0, x1, y1):
    a = (x1 - x0) ** 2
    b = (y1 - y0) ** 2
    return math.sqrt(a + b)

def center(x0, y0, x1, y1):
    a = (x1 - x0) ** 2
    b = (y1 - y0) ** 2
    return int(math.sqrt(a + b)/2)

def diagDiff(list): #list of 4 points

    #if (len(list) < 4):
    #    print("less than 4 pounts in the list")
    #    return
    #elif (len(list) > 4)
    #    print("more than 4 pounts in the list")
    #    return

    #diagonal A
    x1 = list.ravel()[0]
    y1 = list.ravel()[1]
    x3 = list.ravel()[4]
    y3 = list.ravel()[5]

    d1 = distance(x1, y1, x3, y3)

    # diagonal B
    x2 = list.ravel()[2]
    y2 = list.ravel()[3]
    x4 = list.ravel()[6]
    y4 = list.ravel()[7]

    d2 = distance(x2, y2, x4, y4)

    if(d1 > d2):
        dif =  d1 / d2
    else:
        dif = d2 / d1

    return round(dif, 2)
