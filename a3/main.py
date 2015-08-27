#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

from discretiser import cylinder
from matCreator import matCreator,createMatb
import numpy.linalg as linalg
import flows as f
import numpy as np

def createVortexSheet(matC,pointlist,pFlowArray):
    for objects in pointlist:
        for k in range(len(objects)):
            nextPoint = (k+1)%len(objects)
            pos = [objects[k],objects[nextPoint]]
            strength = [matC[k],matC[nextPoint]]
            pFlowArray.append(f.VortexPanel(pos,strength,fixed = True))

def addTracerPoint(pFlowArray):
if __name__ == '__main__':
    print('Assignment 3')
    pFlowArray = [f.Uniform(complex(-100,-100),0,True)]
    pointlist = [[complex(1,1),complex(1,-1),complex(-1,-1),complex(-1,1)]]
    pointlist = cylinder()
    matA = matCreator(pointlist)
    Inverse = linalg.pinv(matA)
    matB = createMatb(pointlist,pFlowArray)
    print("INVERSE")
    print(Inverse)
    print(matB)
    Inverse = np.matrix(Inverse)
    matB = np.matrix(matB).transpose()
    print("MATRICA")
    matC = Inverse*matB
    createVortexSheet(matC,pointlist,pFlowArray)
    addTracerPoint(pFlowArray)
    
