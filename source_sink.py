from flows import *

pos = complex(-0.25,0)
pos2 = complex(0.25,0)
pos3 = complex(-1,1)
Array =  [Source(pos,1,fixed = True) ,Sink(pos2,1,fixed=True)]
for i in range(-10,10,1):
    pos = complex(0,i/10)
    Array.append(tracer(pos,1))

TIME_STEP =  0.005
UPDATE_FRAMES = 1
SIM_TIME = 2.0

