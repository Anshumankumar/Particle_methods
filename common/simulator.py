from flows import *
from copy import deepcopy

TIME_STEP = 0.01
UPDATE_FRAMES = 4
SIM_TIME = 5
MODE = 'RK'

def doNothing():
    pass

class Simulator:
    def __init__(self):
        self.pointArray = []
        self.elementArray = []
        self.counter = 0

    def parse_from_file(self,elemArray):
        self.elementArray = elemArray
    
    def get_elements(self):
        return self.elementArray
    def take_hard_code_value(self):
        pos = complex(1,0)
        pos2 = complex(-1,0)
        pos3 = complex(-1,1)
        self.elementArray =  [Source(pos,1) ,Sink(pos2,1)]
        self.elementArray =  [Vortex(pos,1) ,Vortex(pos2,1)]
        for i in range(-10,10,2):
            pos = complex(0,i)
            self.elementArray.append(tracer(pos,1))

    def run(self, timelimit, updateStrength=doNothing):
        print('Flow Simulator for Potential Flows')
        time = 0.0
        while (time < timelimit):
            self.runSingle(updateStrength)
            time = time + TIME_STEP
        return self.getFinal()
    
    def runSingle(self,updateStrength=doNothing):
        tempPointArray = []
        self.counter = self.counter+1;
        if MODE == 'EULER':
            self.update_euler()
            updateStrength()
        else:
            self.update_rk(updateStrength)
        if (self.counter%UPDATE_FRAMES == 0):
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
                tempVel = tempVel + element2.compute_vel(element.get_pos())
            tempVelArray.append(tempVel)
        return tempVelArray

    def update_rk(self,updateStrength):
        tempVelArray =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].change_pos(tempVelArray[i],TIME_STEP/2)
        updateStrength()
        tempVelArray2 =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].change_pos(tempVelArray2[i]-tempVelArray[i]/2,TIME_STEP) 
        updateStrength() 

    def update_euler(self):
        tempVelArray =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].change_pos(tempVelArray[i],TIME_STEP) 
