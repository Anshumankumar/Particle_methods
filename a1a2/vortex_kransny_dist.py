import sys
sys.path.insert(0, '../common')

from flows import VortexBlobKrasny
import math
def getStrength(y,distance):
        return 4*y/math.sqrt(1-4*pow(y,2))*distance/(2*math.pi)

Array = []
noOfPoints = 100
delta_ = 6/noOfPoints;
distance = 1/(noOfPoints)
for i in range(0,noOfPoints):
    y = i/(noOfPoints)-0.5+1/(2*noOfPoints)
    Array.append(VortexBlobKrasny(complex(0,y),getStrength(y,distance),
        delta=delta_))

TIME_STEP =  0.01
UPDATE_FRAMES = 4
SIM_TIME = 10


