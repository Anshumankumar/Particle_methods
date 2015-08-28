#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

from discretiser import cylinder
from matCreator import MatCreator
from matCreator import MatCreatorC
import flows as f
from simulator  import Simulator
import plotter as p
import math

getPoint(delr)
    pointMat = []
    for i in range(720):
        angle = i*(cmath.pi)/360
        pointMat.append((1+delr)*cmath.exp(1j*angle))
    return pointMat

if __name__ == '__main__':
    print('Assignment 3 Error Comparision')
    pFlowArray = []
    pFlowArray.append(f.Uniform(complex(-100,0),1,1,True))
    pointlist = cylinder()
    matCr=MatCreator(pointlist,pFlowArray)
    pFlowArray.extend(matCr.getMatVP())
    
    pFlowArray = []
    pFlowArray2.append(f.Uniform(complex(-100,0),1,1,True))
    matCrC=MatCreator(pointlist,pFlowArray2)
    pFlowArray.extend(matCrC.getMatVP())
   
    pFlowArray3
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
    #plotter.run(filename,True,False,False)
    plotter.run(filename,False,True,False)

