import cmath
import math as m
class TestElement:
    def __init__(self,position,strength,vel=complex(0,0),fixed =False):
        self._position = position
        self._vel = vel
        self._strength = strength
        self.fixed = fixed
        self.time = 0
        
    def update_flow_euler(self,vel,timestep):
        self._vel = vel;
        self.time = self.time + timestep
        if (self.fixed ==False):
            self._position = complex(m.cos(-1/2*self.time),m.sin(-1/2*self.time))

    def compute_vel(self,a):
        return complex(0,0)
    
    def get_pos(self):
        return self._position


class FlowElement:
    def __init__(self,position,strength,vel=complex(0,0),fixed =False):
        self._position = position
        self._vel = vel
        self._strength = strength
        self.fixed = fixed
    def update_flow_euler(self,vel,timestep):
        self._vel = vel;
        if (self.fixed ==False):
            self._position = self._position + self._vel*timestep

    def update_flow_kutta(self,vel):
        pass
    
    def get_pos(self):
        return self._position

    def print_pos(self):
        print(self._position)

class tracer(FlowElement):
    def compute_potential(self,outputPosition):
        return complex(0,0)

    def compute_vel(self,outputPosition):
        return complex(0,0)

class Source(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    def compute_vel(self,outputPosition):
        return (self._strength/(outputPosition-self._position)).conjugate()

class Sink(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    def compute_vel(self,outputPosition):
        return (-self._strength/(outputPosition-self._position)).conjugate()

class Doublet(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    def compute_vel(self,outputPosition):
        return (-self._strength/pow((outputPosition-self._position),2)).conjugate()

class Vortex(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    def compute_vel(self,outputPosition):
        try:
            return (complex(0,1)*self._strength/(
                outputPosition-self._position)).conjugate()
        except ZeroDivisionError:
            return complex(0,0)

class Uniform(FlowElement):
    def compute_vel(self,outputPosition):
         return (complex(self._strength,0))


def update(test):
    for elements in test:
        tempVel = complex(0,0)
        for elements2 in test:
            if (elements != elements2):
                tempVel = tempVel + elements2.compute_vel(elements.get_pos())
        elements.update_flow_euler(tempVel,TIME_STEP)
