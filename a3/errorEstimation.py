#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

from discretiser import cylinder
from matCreator import MatCreator
from matCreator import MatCreatorC
import flows as f
import math
import cmath
import matplotlib.pyplot as plt

def getPoint(delr):
    pointMat = []
    for i in range(720):
        angle = i*(math.pi)/360
        pointMat.append((1+delr)*cmath.exp(1j*angle))
    return pointMat

def getVel(currentPoints,pArray):
    VelMat = []
    for cPoint in currentPoints:
        tempVel = 0+0j
        for element in pArray:
            tempVel = tempVel + element.compute_vel(cPoint)
        VelMat.append(tempVel)
    return VelMat

def getError(velA,velB):
    error = 0
    for elem1,elem2 in zip(velA,velB):
        delv = abs(elem2 - elem1)
        if (delv > error):
            error = delv
    return error

if __name__ == '__main__':
    print('Assignment 3 Error Comparision')
    pFlowArray = []
    pFlowArray.append(f.Uniform(complex(-100,0),1,1,True))
    pointlist = cylinder()
    matCr=MatCreator(pointlist,pFlowArray)
    pFlowArray.extend(matCr.getMatVP())
    
    pFlowArray2 = []
    pFlowArray2.append(f.Uniform(complex(-100,0),1,1,True))
    matCrC=MatCreatorC(pointlist,pFlowArray2)
    pFlowArray2.extend(matCrC.getMatVP())
   
    pFlowArray3 = []
    pFlowArray3.append(f.Uniform(complex(-100,0),1,1,True))
    pFlowArray3.append(f.Doublet(complex(0,0),1,1,True))
    error1 =[]
    error2 =[]
    cp =[]
    for i in range(100):
        cp.append(i/100)
        currentPoints = getPoint(i/100.0)
        velA1 = getVel(currentPoints,pFlowArray)
        velA2 = getVel(currentPoints,pFlowArray2)
        velA3 = getVel(currentPoints,pFlowArray3)
        error1.append(getError(velA1,velA3))
        error2.append( getError(velA2,velA3))
    plt.loglog(cp,error1,'r',cp,error2,'b')
    plt.ylabel('Error in vel')
    plt.xlabel('delr (distance after 1 unit)')
    plt.show()
