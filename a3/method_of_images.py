#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

import flows as f
from simulator  import Simulator
import plotter as p
import cmath

def getImage(element):
    currentPos = element.get_pos()
    radius = abs(currentPos)
    angle = cmath.phase(currentPos)
    radius2 = 1/radius
    strength2 = -strength/radius
    pos2 = radius2*cmath.exp(1j*angle)
    rElement = f.Vortex(pos2,strength2,1,False)
    return rElement

if __name__ == '__main__':
    print('Assignment 3')
    strength = 4
    pFlowArray = []
    pFlowArray.append(f.Vortex(complex(-1.25,0),strength,1,False))
    length = 1 
    sim = Simulator()
    timelimit = 5
    time = 0
    while (time < timelimit):
        pFlowArray.append(getImage(pFlowArray[0]))
        sim.parse_from_file(pFlowArray)
        sim.runSingle()
        time = time +0.01
        pFlowArray = []
        pFlowArray.extend(sim.get_elements()[0:length])
    data,colors = sim.getFinal()
    plotter = p.ParticlePlotter((-2,2),(-2,2))
    plotter.update(data,colors)
    filename = "temp"
    plotter.run(filename,True,False,False)
    #plotter.run(filename,False,True,False)

