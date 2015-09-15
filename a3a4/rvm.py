#!/usr/bin/env python
import sys
sys.path.insert(0, '../common')

import numpy
import flows as f

def elemDivider(elem,maxStrength):
    strength = elem.strength
    elemList = []
    eClass = elem.__class__
    while (strength > maxStrength):
        strength = strength-maxStrength
        elemList.append(eClass(elem.position,maxStrength,radius=elem.radius))
        
    elemList.append(eClass(elem.position,strength,radius=elem.radius))
    return elemList

def testElemDivider():
    pos =  5+2j
    elemList = []
    v = f.VortexBlobKrasny(pos,2.5,radius=0.01)
    elemList.append(f.VortexBlobKrasny(pos,1.0,radius=0.01))
    elemList.append(f.VortexBlobKrasny(pos,1.0,radius=0.01))
    elemList.append(f.VortexBlobKrasny(pos,0.5,radius=0.01))
    elemList2 = elemDivider(v,1)
    assert(elemList == elemList2)

def randomWalk(element,sigma,timestep=0.1):
    mean = [0,0]
    covariance = [[sigma,0],[0,sigma]]
    vtemp = numpy.random.multivariate_normal(mean,covariance)
    v = vtemp[0] + 1j*vtemp[1]
    position = element.position+v*timestep
    posVector = position/abs(position)
    print (v) 
    if (abs(position) <= 1):
        v = v - 2*(posVector.real*v.real+v.imag*posVector.imag)*posVector
        print(v)
    if(abs( element.position+v*timestep) < 1):
        v =0
    element.change_pos(v,timestep)

def testRandomWalk():
    pos =  -0.7071067811865475+0.7071067811865475j
    v = f.VortexBlobKrasny(pos,2.5,radius=0.01)
    randomWalk(v,0.002,0.1 )
    print(v.position)
    assert(abs(v.position) >= 1)
