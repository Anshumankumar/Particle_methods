from flows import *

pos = complex(0,0)
pos2 = complex(-100,0)
pos3 = complex(-1,1)
Array =  [Doublet(pos,1,fixed = True) ,Uniform(pos2,1)]
for i in range(-10,10,2):
    pos = complex(-2,i/10.0)
    Array.append(tracer(pos,1))

TIME_STEP =  0.02
UPDATE_FRAMES = 2 
SIM_TIME = 5.0

