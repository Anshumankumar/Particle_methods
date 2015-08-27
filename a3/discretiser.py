#This function take a conics parameter and discreatises it to points.
#So that its easy for them 

import math

def discretise(func,startx,endx):
    sign = 1;
    if (startx > endx):
        sign = -1;
    pointlist = []
    currentX = startx
    currentY = func(startx)
    pointlist.append(complex(currentX,currentY)) 
    while(sign*currentX < sign*endx):
        nextX = currentX + sign*0.0001
        if (sign*nextX > sign*endx):
            nextX = endx
        slope = abs(func(nextX)-func(currentX))/0.0001
        delx = 0.05/math.sqrt(1+pow(slope,2))
        currentX = currentX+ sign*delx
        if (sign*currentX > sign*endx):
            currentX = endx
        currentY = func(currentX)
        pointlist.append(complex(currentX,currentY))
    return pointlist


def circle(x):
    return  math.sqrt(1-pow(x,2))

def line(x):
    return 0

def circle2(x):
    return  -math.sqrt(1-pow(x,2))

def cylinder():
    listSet = []
    listSet.append(discretise(circle,-1,1))
#    listSet.append(discretise(circle,0,0.5))
 #   listSet.append(discretise(circle,0.5,1))
  #  listSet.append(discretise(line,1,-1))
    listSet.append(discretise(circle2,1,-1))
    k = len(listSet)-1
    i = 0
    while( i < k):
        if(listSet[i][-1] == listSet[i+1][0]):
            k = k-1
            del listSet[i+1][0]
            listSet[i] = listSet[i] +listSet [i+1]
            del listSet[i+1]
            if (listSet[i][0] == listSet[i][-1]):
                del listSet[i][-1]

    return listSet 

if __name__ == '__main__':
    cylinder()
