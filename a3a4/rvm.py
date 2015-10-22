#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

from numpy import linspace,meshgrid,array,reshape,random
import math
import flows as f
from matCreator import MatCreator
from simulator import Simulator
from discretiser import cylinder2 as cylinder
import plotter as p
import matplotlib
from scipy import interpolate


def component(a,c):
    b= c/abs(c)
    k = (a.real*b.real+a.imag*b.imag)
    return k 

class Rvm(object):

    def __init__(self,flows,gammaMax = 0.1,plotFeildFlag = False):
        self.plotFeildFlag = plotFeildFlag
        self.flows = flows
        self.sim = Simulator(timestep = 0.1,uFrames = 1)
        self.gammaMax = gammaMax
        self.createPoints()
        self.momentArray =[]
        if (self.plotFeildFlag == True):
            self.initializeGrid()
        self.currentSim = "Advection"
        self.counter = 0

    def createPoints(self):
        pointList = cylinder(150)
        self.matCr = MatCreator(pointList,self.flows)
        self.vortexPList = self.matCr.getMatVP()
        self.vortexBlobPoints = []
        self.vortexPanelPoints = []
        for element in self.vortexPList:
            vPanel = element.position*(1+element.length/math.pi/abs(element.position))
            self.vortexBlobPoints.append(vPanel)
            self.vortexPanelPoints.append(1.01*element.position)
        self.currentFlowArray =[]
        self.currentFlowArray.extend(self.vortexPList)
        self.currentFlowArray.extend(self.flows)
        self.sim.updateElements([],self.currentFlowArray)
        
    def computeDrag(self,vFlows):
        moment = 0+0j
        for element in vFlows:
            moment = moment + (element.position.real*1j - element.position.imag)* \
                        element.strength
        return moment

    def getVortexMoment(self):
        return self.momentArray

    def initializeGrid(self):
        xx = linspace(0,2,20)
        yy = linspace(0,2,20)
        self.xx,self.yy = meshgrid(xx,yy)
        self.x,self.y = self.xx.ravel(),self.yy.ravel()
        self.z = self.x+1j*self.y
        self.x,self.y = meshgrid(xx,yy)
    
    def createVortexBlob(self):
        positions = self.vortexBlobPoints
        vortexPanels = self.vortexPList
        vPositions = self.vortexPanelPoints
        velArray = self.getVel(vPositions,self.currentFlowArray)
        VortexBlobArray = []
        for pos,element,vel in zip(positions,vortexPanels,velArray):
            distance = abs(element.position - pos)
            tangent = -element.position.imag +element.position.real*1j
            tangent = tangent/abs(tangent);
            strength = component(vel*element.length,tangent)
            vortexBlob = f.Vortex(pos,strength,radius = distance)
            VortexBlobArray.append(vortexBlob)
        return VortexBlobArray

    def saveQuiverPlot(self):
        self.counter = self.counter +1
        if (self.counter%10 == 0):
            t = self.getVel(self.z,self.currentFlowArray)
            t = array(t)
            t = reshape(t,[-1,len(self.y)])
            ux = t.real
            vy = t.imag
            matplotlib.pyplot.quiver(self.x,self.y,ux,vy)
            matplotlib.pyplot.savefig(str(self.sim.counter)+"quiver.png")
            matplotlib.pyplot.clf()

    def updateFlow(self):
        if (self.plotFeildFlag == True):
            self.saveQuiverPlot()
        if self.currentSim =="Advection":
            self.currentSim = "Diffusion"
            self.advectionRun()
        elif self.currentSim =="Diffusion":
            self.currentSim = "Advection"
            self.advectionRun()
            self.diffusionRun()
            self.advectionRun()
            
    def diffusionRun(self):
        
        vortexBlobArray = self.createVortexBlob()
        smallvortexBlobArray  = []
        for element in vortexBlobArray:
            maxStr =  self.vortexPList[0].length*self.gammaMax 
            smallvortexBlobArray.extend(self.elemDivider(element,maxStr))#self.gammaMax*self.vortexPList[0].length))
        self.currentFlowArray.extend(smallvortexBlobArray)
        self.flows = self.currentFlowArray[len(self.vortexPList):]
        self.matCr.updateFlows(self.flows)
        self.vortexPList = self.matCr.getMatVP()
        self.currentFlowArray[:len(self.vortexPList)] = self.vortexPList
        self.momentArray.append(self.computeDrag(self.flows[1:]))
        passiveElem = self.currentFlowArray[:(len(self.vortexPList)+1)]

        activeElem = self.currentFlowArray[(len(self.vortexPList)+1):]
        self.sim.updateElements(activeElem,passiveElem)
        for element in self.currentFlowArray:
            self.randomWalk(element,0.004,0.1)

    def advectionRun(self):
        self.matCr.updateFlows()

    def getVel(self,currentPoints,pArray):
        VelMat = []
        for cPoint in currentPoints:
            tempVel = 0+0j
            for element in pArray:
                tempVel = tempVel + element.compute_vel(cPoint)
            VelMat.append(tempVel)
        return VelMat

    def run(self,time = 3.0):
        data = self.sim.run(time,self.updateFlow)
        return data

    def elemDivider(self,elem,maxStrength):
        sign = elem.strength/abs(elem.strength)
        strength = abs(elem.strength)
        elemList = []
        eClass = elem.__class__
        while (strength > maxStrength):
            strength = strength-maxStrength
            elemList.append(eClass(elem.position,sign*maxStrength,
                radius=elem.radius))
        elemList.append(eClass(elem.position,sign*strength,
                radius=elem.radius))
        return elemList

    def randomWalk(self,element,sigma,timestep=0.1):
        if element.fixed == True:
            return
        # Take care of the error from Advection
        if abs(element.position) <1.03:
            element.position = 1.03*element.position/abs(element.position)
        
        mean = [0,0]
        cv = sigma/timestep
        covariance = [[cv,0],[0,cv]]
        vtemp = random.multivariate_normal(mean,covariance)
        v = vtemp[0] + 1j*vtemp[1]
        position = element.position+v*timestep
        posVector = position/abs(position)
        
        #Reflection the velocity
        if (abs(position) <= 1.03):
            v = v - 2*(posVector.real*v.real+v.imag*posVector.imag)*posVector
      
        #Very Rare Case But can happen, due to precesion
        if(abs( element.position) < 1.03):
            v =0
        element.change_pos(v,timestep)

def getDrag(mA):
    cA  = []
    dragArray = []
    for i in range(len(mA)-3):
        cA.append((mA[i]+mA[i+1]+mA[i+2]+mA[i+3])/4)
    for i in range(len(cA)-1):
        dragArray.append((cA[i+1].real -cA[i].real)/0.1)
    return dragArray

def plotDrag(momentArray,time):
    dragArray = getDrag(momentArray)
    print(dragArray)
    t = linspace(0.1,(time-0.3),len(dragArray))
    tck = interpolate.splrep(t,dragArray, s=0)
    t = linspace(0.1,(time-0.3),200)
    dNew = interpolate.splev(t, tck, der=0)
    matplotlib.pyplot.plot(t,dNew)
    matplotlib.pyplot.show()


if __name__ == '__main__':
    pFlowArray = []
    pFlowArray.append(f.Uniform(complex(-100,0),1,1,True))
    rvm = Rvm(pFlowArray,0.1,True)
    time = 3
    data,colors = rvm.run(time)
     ##Uncomment these to particles, It also stores a video 
    plotter = p.ParticlePlotter((-1.5,3.5),(-2,2))
    plotter.update(data,colors)
    filename = 'temp'
    plotter.run(filename,False,True,True)
    momentArray = rvm.getVortexMoment()
    plotDrag(momentArray,time)


def testElemDivider():
    pos =  5+2j
    elemList = []
    v = f.VortexBlobKrasny(pos,-2.5,radius=0.01)
    elemList.append(f.Vortex(pos,-1.0,radius=0.01))
    elemList.append(f.Vortex(pos,-1.0,radius=0.01))
    elemList.append(f.Vortex(pos,-0.5,radius=0.01))
    r = Rvm([])
    elemList2 = r.elemDivider(v,1.00)
    assert(elemList == elemList2)


def testRandomWalk():
    pos =  1.05*(-0.7071067811865475+0.7071067811865475j)
    v = f.Vortex(pos,2.5,radius=0.01)
    r = Rvm([])
    r.randomWalk(v,0.002,0.1 )
    assert(abs(v.position) >= 1.00)

