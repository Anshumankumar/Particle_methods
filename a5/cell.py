import sys
sys.path.insert(0, '../common')

import flows as f
from combination import nCr 
import math
import numpy as np
import matplotlib.pyplot as plt
import time

class Cell:
    def __init__(self,center,length,n):
        assert(n>=1)
        self.center = center
        self.position = center
        self.length = length
        self.maxNoOfParticle = n
        self.particleArray = []
        self.childs = []

    def addParticle(self,particle):
        self.particleArray.append(particle)

    def addChildCell(self):
        length = self.length
        n = self.maxNoOfParticle
        shift = -length/2 + 1j*length/2  #Left up
        self.childs.append(Cell(self.center+shift,length/2,n))
        shift =  length/2 + 1j*length/2  #Right up
        self.childs.append(Cell(self.center+shift,length/2,n))
        shift = -length/2 - 1j*length/2  #Left Down
        self.childs.append(Cell(self.center+shift,length/2,n))
        shift =  +length/2 - 1j*length/2  #Right Down
        self.childs.append(Cell(self.center+shift,length/2,n))

    def distributeParticle(self):
        for particle in self.particleArray:
            if (particle.position.real > self.center.real):
                if (particle.position.imag > self.center.imag):
                    self.childs[1].addParticle(particle)
                else:
                    self.childs[3].addParticle(particle)
            else:
                if (particle.position.imag > self.center.imag):
                    self.childs[0].addParticle(particle)
                else:
                    self.childs[2].addParticle(particle)

    def getMPCoef(self,n):
        self.mpCoef = [0]*n
        for child in self.childs:
            tempMpCoef = child.getMPCoef(n)
            dist =  child.position -self.position
            for i in range(n):
                for j in range(i+1):
                    self.mpCoef[i] = self.mpCoef[i]+(tempMpCoef[j]*
                            pow(dist,i-j)*nCr(i,j))
        return self.mpCoef


    def checkParticle(self):
        if (len(self.particleArray) > self.maxNoOfParticle):
            self.addChildCell()
            self.distributeParticle()
            for child in self.childs:
                child.checkParticle()
        else:
            for particle in self.particleArray:
                self.childs.append(particle)

    def evalMultipole(self,oPosition):
        vel  = 0+0j
        for i in range(len(self.mpCoef)):
            vel = vel + self.mpCoef[i]/pow((oPosition - self.position),
                    i+1)
        vel = -0.5j/math.pi*vel
        return vel.conjugate()

    def compute_vel(self,oPosition):
        if abs(oPosition - self.center) > 4*self.length:
            return self.evalMultipole(oPosition)
        else:
            vel = 0 + 0j
            for child in self.childs:
                vel = vel + child.compute_vel(oPosition)
            return vel


def test_cell():
    particleArray = []
    cell = Cell(0+0j,1,1)
    particleArray.append(f.Vortex(complex(0.2,0.2),1,1,False))
    particleArray.append(f.Vortex(complex(0.6,0.6),1,1,False))
    particleArray.append(f.Vortex(complex(-0.3,-0.4),1,1,False))
    particleArray.append(f.Vortex(complex(0.3,-0.4),1,1,False))
    particleArray.append(f.Vortex(complex(-0.4,0.5),1,1,False))
    for particle in particleArray:
        cell.addParticle(particle)
    cell.checkParticle()
    cell.getMPCoef(15)
    tempVel = []
    for particle in particleArray:
        tempVel.append(cell.compute_vel(particle.position))
    for vel in tempVel:
        print(vel)
    assert(cell.childs[0].childs[0] ==  particleArray[4])
    assert(cell.childs[1].childs[1].childs[0] == particleArray[1])
    assert(cell.childs[2].childs[0] == particleArray[2])
    assert(cell.childs[3].childs[0] == particleArray[3])
    print("creating  the quad tree test successful")

def tempTest():
    particleArray = []
    strength = 1
    noOfParticle = 500
    ran = np.random.random
    for i in range(noOfParticle):
        pos = 2*ran()-1 + (2*ran()-1)*1j
        particleArray.append(f.Vortex(pos,1,1,False))

    ctime = time.clock()
    cell = Cell(0+0j,1,5)
    for particle in particleArray:
        cell.addParticle(particle)
    cell.checkParticle()
    cell.getMPCoef(20)
    velArray = []
    for particle in particleArray:
        velArray.append(cell.compute_vel(particle.position))
    print(time.clock()-ctime)
    ctime = time.clock()
    velArray2 = f.velUpdate(particleArray)
    print(time.clock()-ctime)
    error = [0]*len(velArray)
    for i in range (len(velArray)):
        error[i] = abs(velArray[i] -velArray2[i])
    plt.plot(error)
    plt.show()

if __name__=='__main__':
    tempTest()
