from flows import *
from plotter import *
from copy import deepcopy
import importlib
import sys

#filename = 'vortex'
#filename = 'doublet'
filename = 'source_sink'


if len(sys.argv) > 1:
    filename = str(sys.argv[1])
elemFile = importlib.import_module(filename, package=None)

#self.TIME_STEP = elemFile.self.TIME_STEP
UPDATE_FRAMES = elemFile.UPDATE_FRAMES
SIM_TIME = elemFile.SIM_TIME
try:
    MODE = elemFile.MODE
except AttributeError:
    MODE = 'RK'

def check_color(elem):
    if type(elem) == Source:
        return 'r'
    if type(elem) == Doublet:
        return 'g'
    if type(elem) == tracer:
        return 'r'
    if type(elem) == Sink:
        return 'm'
    if type(elem) == TestElement:
        return 'y'
    return 'k'

class Simulator:
    counter = 0
    def __init__(self):
        self.elementArray = []
        self.pointArray = []

    def parse_from_file(self):
        self.elementArray = deepcopy(elemFile.Array)

    def take_hard_code_value(self):
        pos = complex(1,0)
        pos2 = complex(-1,0)
        pos3 = complex(-1,1)
        self.elementArray =  [Source(pos,1) ,Sink(pos2,1)]
        self.elementArray =  [Vortex(pos,1) ,Vortex(pos2,1)]
        for i in range(-10,10,2):
            pos = complex(0,i)
            self.elementArray.append(tracer(pos,1))

    def run(self,   timelimit,TIME_STEP):
        self.TIME_STEP = TIME_STEP
        print('Flow Simulator for Potential Flows')
        time = 0.0
        while (time < timelimit):
            tempPointArray = []
            self.counter = self.counter+1;
            time = time + self.TIME_STEP
            if MODE == 'EULER':
                self.update_euler()
            else:
                self.update()
            if (self.counter%UPDATE_FRAMES == 0):
                for element in self.elementArray:
                    tempPointArray.append(element.get_pos())
                self.pointArray.append(tempPointArray)
        colors = []
        for element in self.elementArray:
            colors.append(check_color(element))
        return self.pointArray,colors
    
    def vel_update(self,elementArray):
        tempVelArray =  []
        for element in elementArray:
            tempVel = complex(0,0)
            for element2 in elementArray:
                if (element != element2):
                     tempVel = tempVel + element2.compute_vel(
                             element.get_pos())
            tempVelArray.append(tempVel)
        return tempVelArray

    def update(self):
        elementArray2 =  deepcopy(self.elementArray)
        tempVelArray =  self.vel_update(elementArray2)
        for i in range(len(elementArray2)):
            elementArray2[i].update_flow_euler(tempVelArray[i],self.TIME_STEP/2) 
        tempVelArray =  self.vel_update(elementArray2)
        for i in range(len(self.elementArray)):
            self.elementArray[i].update_flow_euler(tempVelArray[i],self.TIME_STEP) 
               
    def update_euler(self):
        tempVelArray =  self.vel_update(self.elementArray)
        for i in range(len(self.elementArray)):
            self.elementArray[i].update_flow_euler(tempVelArray[i],self.TIME_STEP) 
       
if __name__ == '__main__':
    error = []
    time = []
    for i in range(1,1000,1):
        TIME_STEP = i/1000
        print(TIME_STEP)
        sim = Simulator()
        sim.parse_from_file()
        data = []
        data,colors = sim.run(1*TIME_STEP,TIME_STEP)
        tempdata = data[0]
        print(tempdata)
        time.append(TIME_STEP)
        error.append(abs(tempdata[2]-tempdata[0]))
    plt.loglog(time,error)
    plt.show()
   # plotter = ParticlePlotter((-2,2),(-2,2))
   # plotter.update(data,colors)
   # plotter.run(filename)

