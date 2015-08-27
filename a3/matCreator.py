import sys
sys.path.insert(0, '../common')

import flows as f
import cmath
import math


def matCreator(pointlist):
    size = 0;
    for objects in pointlist:
        size = size + len(objects)
    matA = []
    for i in range(size+1):
        matA.append([0]*size)
    currentPointer = 0
    for objects in pointlist:
        for i in range(len(objects)):
            nextPoint = (i+1)%len(objects)
            computeStregth(pointlist,objects[i], objects[nextPoint], matA,
                    currentPointer+i, currentPointer+nextPoint)
            j = i-1
            dist = abs(objects[i] - objects[j]) + abs(objects[i] 
                    -objects[nextPoint])
            matA[size][i]= dist/2
        currentPointer = currentPointer + len(objects)
    
    return matA

def computeStregth(pointlist,object1, object2, matA,i,j):
    length = abs(object1-object2)
    phase = cmath.phase(object2-object1)
    currentPointer = 0
    for objects in pointlist:
        for k in range(len(objects)):
            nextPoint = (k+1)%len(objects)
            midPoint = (objects[k] +objects[nextPoint])/2
            tranZ = (midPoint - object1)*cmath.exp(complex(0,-1)*phase)
            velConst =  getStrength1(tranZ,length,phase)
            angle = cmath.phase(objects[nextPoint]-objects[k])+cmath.pi/2
            velConst = abs(complex(velConst.real*(math.cos(angle)),
                            velConst.imag*(math.sin(angle))))
            matA[currentPointer+k][i] = matA[currentPointer+k][i] + \
                    velConst
            velConst =  getStrength2(tranZ,length,phase)
            angle = cmath.phase(objects[nextPoint]-objects[k])+cmath.pi/2
            velConst = abs(complex(velConst.real*(math.cos(angle)),
                            velConst.imag*(math.sin(angle))))
            matA[currentPointer+k][j] = matA[currentPointer+k][j]+  \
                velConst
        currentPointer = currentPointer +len(objects)

def getStrength1(tranZ,length,phase):
     return (complex(0,-0.5/math.pi)*((tranZ/length -1)*cmath.log((
         tranZ-length)/tranZ) +1)*-cmath.exp(complex(0,-1)*phase)) \
        .conjugate()

def getStrength2(tranZ,length,phase):
     return (complex(0,0.5/math.pi)*((tranZ/length)*cmath.log((
         tranZ-length)/tranZ) +1)*-cmath.exp(complex(0,-1)*phase)) \
         .conjugate()

def createMatb(pointlist,pFlowArray):
    size = 0;
    for objects in pointlist:
        size = size + len(objects)
    matB = [0]*(size+1)  
    for objects in pointlist:
        for k in range(len(objects)):
            nextPoint = (k+1)%len(objects)
            midPoint = (objects[k] +objects[nextPoint])/2
            matB[k] = 0;
            for element in pFlowArray:
                matB[k] = matB[k] + element.compute_vel(midPoint)
            angle = cmath.phase(objects[nextPoint]-objects[k])+cmath.pi/2
            matB[k] = abs(complex(matB[k].real*(math.cos(angle)),
                            matB[k].imag*(math.sin(angle))))
    return matB
