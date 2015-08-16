from flows import *

pos = complex(1,0)
pos2 = complex(-1,0)
pos3 = complex(-1,1)
Array =  [Vortex(pos,1,fixed = True) ,Vortex(pos2,1,fixed=True)]
for i in range(-10,10,1):
    pos = complex(0,i/10)
    Array.append(tracer(pos,1))

TIME_STEP =  0.02
UPDATE_FRAMES = 2
SIM_TIME = 5.0

