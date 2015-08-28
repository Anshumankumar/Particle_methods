import cmath
import math as m
class TestElement:
    def __init__(self,position,strength,vel=complex(0,0),fixed =False):
        self._position = position
        self._vel = vel
        self._strength = strength
        self.fixed = fixed
        self.time = 0

    def change_pos(self,vel,timestep):
        self._vel = vel;
        self.time = self.time + timestep
        if (self.fixed ==False):
            self._position = complex(m.cos(-1/2*self.time),m.sin(-1/2*self.time))

    def compute_vel(self,a):
        return complex(0,0)
    
    def get_pos(self):
        return self._position
    
    def get_color(self):
        return 'y'

class FlowElement:
    def __init__(self,position,strength,vel=complex(0,0),fixed =False):
        self._position = position
        self._vel = vel
        self._strength = strength
        self.fixed = fixed
    def change_pos(self,vel,timestep):
        self._vel = vel;
        if (self.fixed ==False):
            self._position = self._position + self._vel*timestep

    
    def get_pos(self):
        return self._position

    def print_pos(self):
        print(self._position)

    def get_color(self):
        return 'y'
    def decoVel(func):
        def vel(*arg,**kwargs):
            try:
                return func(*arg,**kwargs)
            except ZeroDivisionError:
                return complex(0,0)
        return vel
    
    def update_strength(self,strength):
        self._strength = strength

class tracer(FlowElement):
    def compute_potential(self,outputPosition):
        return complex(0,0)

    def compute_vel(self,outputPosition):
        return complex(0,0)

    def get_color(self):
        return 'r'

class Source(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    @FlowElement.decoVel
    def compute_vel(self,outputPosition):
            return (self._strength/(outputPosition-self._position)).conjugate()
    def get_color(self):
        return 'k'

class Sink(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    @FlowElement.decoVel
    def compute_vel(self,outputPosition):
        return (-self._strength/(outputPosition-self._position)).conjugate()
    def get_color(self):
        return 'm'



class Doublet(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    @FlowElement.decoVel
    def compute_vel(self,outputPosition):
        return (-self._strength/pow((outputPosition-self._position),2)).conjugate()

    def get_color(self):
        return 'g'


class Vortex(FlowElement):    
    def compute_potential(self,outputPosition):
        return self._strength*cmath.log(outputPosition -self._position)
    
    @FlowElement.decoVel
    def compute_vel(self,outputPosition):
        return 1/(2*m.pi)*(complex(0,-1)*self._strength/(
            outputPosition-self._position)).conjugate()

    def get_color(self):
        return 'b'


class VortexBlobKrasny(Vortex):
    def __init__(self,position,strength,vel=complex(0,0),fixed =False,
            delta = 0.1):
        self.delta = delta;
        super(Vortex,self).__init__(position,strength,vel,fixed)
    def compute_vel(self,outputPosition):
        radius = abs(outputPosition-self._position)
        kernelConst = pow(radius,2)/(pow(self.delta,2)+pow(radius,2))
        return kernelConst*super(
                VortexBlobKrasny,self).compute_vel(outputPosition)

class VortexPanel(FlowElement):
    def __init__(self,position,strength,vel=complex(0,0),fixed =False):
        self.length = abs(position[0]-position[1])
        self.phase = cmath.phase(position[1]-position[0])
        self.startPoint = position[0]
        self.endPoint = position[1]
        midPoint = (position[0]+position[1])/2
        super(VortexPanel,self).__init__(midPoint,strength,vel,fixed)

class VortexLPanel(VortexPanel):
    @FlowElement.decoVel
    def compute_vel(self,position):
        return self._strength[0]*self.getStrengthC1(position)+ \
               self._strength[1]*self.getStrengthC2(position)

    def getStrengthC1(self,position):
        tranZ = (position-self.startPoint)*cmath.exp(-1j*self.phase)
        return ((-0.5j/cmath.pi)*((tranZ/self.length -1)*cmath.log((
                tranZ-self.length)/tranZ) +1)) \
                .conjugate()*cmath.exp(1j*self.phase)

    def getStrengthC2(self,position):
        tranZ = (position-self.startPoint)*cmath.exp(-1j*self.phase)
        return ((0.5j/cmath.pi)*((tranZ/self.length)*cmath.log((
                tranZ-self.length)/tranZ) +1)) \
                .conjugate()*cmath.exp(1j*self.phase) 
    
class VortexCPanel(VortexPanel):
    @FlowElement.decoVel
    def compute_vel(self,position):
        tranZ = (position-self.startPoint)*cmath.exp(-1j*self.phase)
        return (self._strength*(0.5j/cmath.pi)*cmath.log((
            tranZ-self.length)/tranZ)).conjugate()* \
            cmath.exp(1j*self.phase)


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
