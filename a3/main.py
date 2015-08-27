#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

from discretiser import cylinder
from matCreator import matCreator,createMatb
import numpy.linalg as linalg
import flows as f
import numpy as np
from simulator  import Simulator
import plotter as p

def createVortexSheet(matC,pointlist,pFlowArray):
    for objects in pointlist:
        for k in range(len(objects)):
            nextPoint = (k+1)%len(objects)
            pos = [objects[k],objects[nextPoint]]
            strength = [matC[k],matC[nextPoint]]
            pFlowArray.append(f.VortexPanel(pos,strength,fixed = True))

def addTracerPoint(pFlowArray):
    pos = complex(-2,0)
  #  pFlowArray.append(f.Vortex(pos,1,1,False))

if __name__ == '__main__':
    print('Assignment 3')
    pFlowArray = []
    pFlowArray.append(f.Uniform(complex(-1,-1.5),1,1,False))
    pointlist = [[complex(1,1),complex(1,-1),complex(-1,-1),complex(-1,1)]]
   # pointlist = cylinder()
    matA = matCreator(pointlist)
    Inverse = linalg.pinv(matA)
    matB = createMatb(pointlist,pFlowArray)
    Inverse = np.matrix(Inverse)
    matB = np.matrix(matB).transpose()
    print("MATRICA")
    matC = Inverse*matB
    matC = np.array(matC.transpose())[0].tolist()
    print(matC)
    print(matC[0])
    print(pointlist[0][0])
    createVortexSheet(matC,pointlist,pFlowArray)
    addTracerPoint(pFlowArray)
    
    sim = Simulator()
    sim.parse_from_file(pFlowArray)
    data,colors = sim.run(1)
    plotter = p.ParticlePlotter((-2,2),(-2,2))
    plotter.update(data,colors)
    filename = "temp"
    plotter.run(filename,False,True,False)

