import sys
sys.path.insert(0, '../common')

import flows as f
import cmath
import math
import numpy as np

class MatCreator:
    def __init__(self,pointlist,flowArray=[]):
        self.vortexList = []
        self.updatePointMat(pointlist)
        self.updateFlows(flowArray)

    def updatePointMat(self,pointlist):
        self.pointMat = pointlist
        self.size = 0;
        for objects in self.pointMat:
            self.size = self.size + len(objects)
        self.matA = []
        for i in range(self.size+1):
            self.matA.append([0]*self.size)
        self.createVortexPanel()
        self.updateMatA()
        self.inverseA = np.matrix(np.linalg.pinv(self.matA))
    
    def updateFlows(self,flowArray):
        self.flowArray = flowArray
        self.updateMatB()
        self.matB2 = np.matrix(self.matB).transpose()
        self.updateMatS()
        self.updateMatVP()

    def getMatA(self):
        return self.matA

    def getMatB(self):
        return self.matB
    
    def getMatS(self):
        return self.matS
    
    def getMatVP(self):
        return self.vortexList

    def createVortexPanel(self):
        self.vortexList = []
        for objects in self.pointMat:
            for currentp in range(len(objects)):
                nextp = (currentp+1)%len(objects)
                strength = [1,1]
                pos = [objects[currentp],objects[nextp]]
                self.vortexList.append(f.VortexLPanel(pos,strength,0+0j,True))
        
    def updateMatA(self):
        start,current = 0,0
        for panel in self.vortexList:
            nextp = current+1
            if (self.vortexList[start].startPoint ==
                    self.vortexList[current].endPoint):
                nextp = start
                start = current+1
            self.computeStrengthC(panel,current,nextp)
            current = current+1
        for i in range(len(self.vortexList)):
            self.matA[self.size][i] = (self.vortexList[i].length+
                    self.vortexList[i-1].length)/2

    def computeStrengthC(self,currentPanel,i,j):
        for panel,row in zip(self.vortexList,self.matA):
            pVector = cmath.exp(1j*(panel.phase+cmath.pi/2))
            velConst = currentPanel.getStrengthC1(panel.get_pos())
            velConst = self.dotP(velConst,pVector)
            row[i] = row[i]+ velConst
            velConst = currentPanel.getStrengthC2(panel.get_pos())
            velConst = self.dotP(velConst,pVector)
            row[j] = row[j]+velConst

    def dotP(self,a,b):
        return a.real*b.real+a.imag*b.imag

    def updateMatB(self):
        self.matB = [0]*(self.size+1)  
        k = 0
        for panel in self.vortexList:
            for element in self.flowArray:
                self.matB[k] = self.matB[k] -  element.compute_vel(
                        panel.get_pos())
            pVector = cmath.exp(1j*(panel.phase+cmath.pi/2))
            self.matB[k] = self.dotP(self.matB[k],pVector)
            k = k+1
    
    def updateMatS(self):
        self.matS = self.inverseA*self.matB2
        self.matS = np.array(self.matS.transpose())[0].tolist()

    def updateMatVP(self):
        start,current = 0,0
        for panel in self.vortexList:
            nextp = current+1
            if (self.vortexList[start].startPoint ==
                    self.vortexList[current].endPoint):
                nextp = start
                start = current+1
            stren = [self.matS[current],self.matS[nextp]]
            self.vortexList[current].update_strength(stren)
            current = current+1

class MatCreatorC(MatCreator):
    def createVortexPanel(self):
        self.vortexList = []
        for objects in self.pointMat:
            for currentp in range(len(objects)):
                nextp = (currentp+1)%len(objects)
                strength = 1
                pos = [objects[currentp],objects[nextp]]
                self.vortexList.append(f.VortexCPanel(pos,strength,0+0j,True))
    
    def updateMatA(self):
        current = 0
        for panel in self.vortexList:
            self.computeStrengthC(panel,current)
            current = current+1
        for i in range(len(self.vortexList)):
            self.matA[self.size][i] = (self.vortexList[i].length)

    def computeStrengthC(self,currentPanel,i):
        for panel,row in zip(self.vortexList,self.matA):
            pVector = cmath.exp(1j*(panel.phase+cmath.pi/2))
            velConst = currentPanel.compute_vel(panel.get_pos())
            velConst = self.dotP(velConst,pVector)
            row[i] = row[i]+ velConst

    def updateMatVP(self):
        current = 0
        for panel in self.vortexList:
            stren = self.matS[current]
            self.vortexList[current].update_strength(stren)
            current = current+1
