from flows import *
from copy import deepcopy

def doNothing():
    pass

class Simulator:
    def __init__(self,timestep =0.01,uFrames = 4,mode='RK'):
        self.timestep = timestep
        self.uFrames = uFrames
        self.mode = mode
        self.pointArray = []
        self.elementArray = []
        self.counter = 0

    def updateElements(self,elemArray):
        self.elementArray = elemArray
    
    def get_elements(self):
        return self.elementArray

    def run(self,timelimit,updateStrength=doNothing):
        print('Flow Simulator for Potential Flows')
        ctime = 0.0
        while (ctime < timelimit):
            ctime = ctime + self.timestep
            print("Simulation time", ctime)
            print("No of Particles",len(self.elementArray))
            self.runSingle(updateStrength)

        return self.getFinal()
    
    def runSingle(self,updateStrength=doNothing):
        tempPointArray = []
        self.counter = self.counter+1;
        if self.mode == 'EULER':
            self.update_euler()
            updateStrength()
        else:
            self.update_rk(updateStrength)
        if (self.counter%self.uFrames == 0):
            for element in self.elementArray:
                tempPointArray.append(element.get_pos())
            self.pointArray.append(tempPointArray)
    
    def getFinal(self):
        colors = []
        for element in self.elementArray:
            colors.append(element.get_color())
        return self.pointArray,colors
    
    def vel_update(self,elementArray):
        tempVelArray =  []
        for element in elementArray:
            tempVel = complex(0,0)
            if element.fixed == True:
                tempVelArray.append(tempVel)
                continue
            for element2 in elementArray:
                tempVel = tempVel + element2.compute_vel(
                            element.get_pos())
            tempVelArray.append(tempVel)
        return tempVelArray

    def update_rk(self,updateStrength):
        tempVelArray =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].change_pos(tempVelArray[i],self.timestep/2)
        updateStrength()
        tempVelArray2 =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].change_pos(tempVelArray2[i]-tempVelArray[i]/2,self.timestep) 
        updateStrength() 

    def update_euler(self):
        tempVelArray =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].change_pos(tempVelArray[i],self.timestep) 
