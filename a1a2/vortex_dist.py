from flows import Vortex
import math
def getStrength(y,distance):
        return 4*y/math.sqrt(1-4*pow(y,2))*distance/(2*math.pi)

Array = []
noOfPoints = 50
distance = 1/(noOfPoints)
for i in range(0,noOfPoints):
    y = i/(noOfPoints)-0.5+1/(2*noOfPoints)
    Array.append(Vortex(complex(0,y),getStrength(y,distance)))

TIME_STEP =  0.01
UPDATE_FRAMES = 4
SIM_TIME = 5


