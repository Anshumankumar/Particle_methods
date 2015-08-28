import sys
sys.path.insert(0, '../common')

import flows as f
import cmath
import math

class MatCreator:
    def __init__(self,pointlist):
        self.updatePointMat(pointlist)

    def updatePointMat(self.pointlist):
        self.pointMat = pointlist
        self.size = 0;
        for objects in self.pointMat:
            self.size = self.size + len(objects)
            matA = []
        for i in range(size+1):
            matA.append([0]*size)

    def createMatA():
        self.createVortexPanel()
        self.updateMatA()

    def createVortexPanel():
        self.vortexList = []
        for objects in self.pointMat:
            for currentp in range(len(objects)):
                nextp = (currentp+1)%len(objects)
                strength = [1,1]
                pos = [objects[currentp],objects[nextp]]
                self.vortexList.append(VortexPanel(pos,strength,0+0j,True))
        
    def updateMatA():
        for panel in self.vortexList:
            computeStrengthC(panel):
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
            velConst = velConst.real*cmath.exp(1j*angle).real+ \
                            velConst.imag*cmath.exp(1j*angle).imag
            matA[currentPointer+k][i] = matA[currentPointer+k][i] + \
                    velConst
            velConst =  getStrength2(tranZ,length,phase)
            velConst = velConst.real*cmath.exp(1j*angle).real+ \
                            velConst.imag*cmath.exp(1j*angle).imag
            matA[currentPointer+k][j] = matA[currentPointer+k][j]+  \
                velConst
        currentPointer = currentPointer +len(objects)

def getStrength1(tranZ,length,phase):
     return (complex(0,-0.5/math.pi)*((tranZ/length -1)*cmath.log((
         tranZ-length)/tranZ) +1)).conjugate()*cmath.exp(complex(0,1)*phase)

def getStrength2(tranZ,length,phase):
     return (complex(0,0.5/math.pi)*((tranZ/length)*cmath.log((
         tranZ-length)/tranZ) +1)).conjugate()*cmath.exp(complex(0,1)*phase)

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
            matB[k] = matB[k].real*cmath.exp(1j*angle).real+ \
                            matB[k].imag*cmath.exp(1j*angle).imag
    return matB
