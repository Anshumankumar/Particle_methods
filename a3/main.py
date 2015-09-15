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
    for i in range(-20,20,5):
        pos = complex(-2,i/10.0)
        pFlowArray.append(f.Tracer(pos,1,1,False))

if __name__ == '__main__':
    print('Assignment 3')
    pFlowArray = []
    #pFlowArray.append(f.Uniform(complex(-100,0),1,1,True))
    pFlowArray.append(f.Vortex(complex(-1.25,0),4,1,False))
    #pFlowArray.append(f.Vortex(complex(1.25,1),100,1,False))
    pointlist = [[complex(1,1),complex(1,-1),complex(-1,-1),complex(-1,1)]]
    pointlist = cylinder()
    matCr=MatCreator(pointlist,pFlowArray)
   # addTracerPoint(pFlowArray)
    length = len(pFlowArray)
    pFlowArray.extend(matCr.getMatVP())
    sim = Simulator()
    sim.parse_from_file(pFlowArray)
    data,colors = sim.run(5,matCr.updateFlows)
    plotter = p.ParticlePlotter((-2,2),(-2,2))
    plotter.update(data,colors)
    filename = "temp"
    #plotter.run(filename,True,False,False)
    plotter.run(filename,False,True,True)

