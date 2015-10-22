from flows import *
from copy import deepcopy
from cell import Cell

def doNothing():
    pass

class Simulator:
    def __init__(self,timestep =0.1,uFrames = 400,mode='RK'):
        self.timestep = timestep
        self.uFrames = uFrames
        self.mode = mode
        self.pointArray = []
        self.activeElementArray = []
        self.passiveElementArray = []
        self.counter = 0

    def updateElements(self,activeElemArray,passiveElemArray):
        self.activeElementArray = activeElemArray
        self.passiveElementArray = passiveElemArray
    
    def get_elements(self):
        return self.activeElementArray

    def run(self,timelimit,updateStrength=doNothing):
        print('Flow Simulator for Potential Flows')
        ctime = 0.0
        while (ctime < timelimit):
            ctime = ctime + self.timestep
            print("Simulation time", ctime)
            print("No of Particles",len(self.activeElementArray))
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
            for element in self.passiveElementArray:
                tempPointArray.append(element.get_pos())
            for element in self.activeElementArray:
                tempPointArray.append(element.get_pos())
            self.pointArray.append(tempPointArray)
    
    def getFinal(self):
        colors = []
        for element in self.passiveElementArray:
            colors.append(element.get_color())
        for element in self.activeElementArray:
            colors.append(element.get_color())
        return self.pointArray,colors
    
    def vel_update(self,elementArray):
        return self.vel_update_multipole(elementArray)

    def vel_update_normal(self,elementArray):
        tempVelArray =  []
        for element in elementArray:
            tempVel = complex(0,0)
            if element.fixed == True:
                tempVelArray.append(tempVel)
                continue
            for element2 in elementArray:
                tempVel = tempVel + element2.compute_vel(
                            element.get_pos())
            for particle2 in self.passiveElementArray:
                tempVel = tempVel + particle2.compute_vel(
                        element.get_pos())
            tempVelArray.append(tempVel)
 
        return tempVelArray
    
    def vel_update_multipole(self,elementArray):
        velArray = []
        print("Cells Creation")
        cell = Cell(0+0j,3,6);
        cell.addParticleArray(elementArray)
        cell.checkParticle()
        cell.getMPCoef(12)
        print("Cells Completed")
        for particle in elementArray:
            vel = cell.compute_vel(particle.position)
            for particle2 in self.passiveElementArray:
                vel = vel + particle2.compute_vel(particle.position)
            velArray.append(vel)
        return velArray

    def update_rk(self,updateStrength):
        aElemNo = len(self.activeElementArray)
        tempVelArray =  self.vel_update(self.activeElementArray)
        for i in range(aElemNo):
            self.activeElementArray[i].change_pos(tempVelArray[i],self.timestep/2)
        updateStrength()
        tempVelArray2 =  self.vel_update(self.activeElementArray)
        for i in range(aElemNo):
            self.activeElementArray[i].change_pos(tempVelArray2[i]-tempVelArray[i]/2,self.timestep) 
        updateStrength() 

    def update_euler(self):
        aElemNo = len(self.activeElementArray)
        tempVelArray =  self.vel_update(self.activeElementArray)
        for i in range(aElemNo):
            self.activeElementArray[i].change_pos(tempVelArray[i],self.timestep) 
