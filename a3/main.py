#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

from discretiser import cylinder
from matCreator import MatCreator
from matCreator import MatCreatorC
import flows as f
from simulator  import Simulator
import plotter as p


def addTracerPoint(pFlowArray):
    for i in range(-20,20,4):
        pos = complex(-2,i/10.0)
        pFlowArray.append(f.tracer(pos,1,1,False))

if __name__ == '__main__':
    print('Assignment 3')
    pFlowArray = []
    #pFlowArray.append(f.Uniform(complex(-100,0),1,1,True))
    pFlowArray.append(f.Vortex(complex(-1.25,0),4,1,False))
    pointlist = [[complex(1,1),complex(1,-1),complex(-1,-1),complex(-1,1)]]
    pointlist = cylinder()
    matCr=MatCreator(pointlist,pFlowArray)
    #addTracerPoint(pFlowArray)
    length = len(pFlowArray)
    pFlowArray.extend(matCr.getMatVP())
    
    
    sim = Simulator()
    sim.parse_from_file(pFlowArray)
    timelimit = 5
    time = 0
    while (time < timelimit):
        sim.parse_from_file(pFlowArray)
        sim.runSingle()
        time = time +0.01
        pFlowArray = []
        pFlowArray.extend(sim.get_elements()[0:length])
        matCr.updateFlows(pFlowArray)
        pFlowArray.extend(matCr.getMatVP())
    data,colors = sim.getFinal()
    plotter = p.ParticlePlotter((-2,2),(-2,2))
    plotter.update(data,colors)
    filename = "temp"
    plotter.run(filename,True,False,False)
    #plotter.run(filename,False,True,False)

