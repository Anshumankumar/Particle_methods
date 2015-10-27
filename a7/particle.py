import math
def cubicSpline(q,h):
    q = abs(q)
    if (q>2):
        return 0
    elif (q>1 and q<=2):
        return 2/(12.0*h)*math.pow(2-q,3)
    else:
        return 2/(3.0*h)*(1-3/2.0*pow(q,2)+3/4.0*pow(q,3))


def cubicSplineD(q,h):
    if q == 0:
        return 0
    if (abs(q)>2):
        return 0;
    if (abs(q) > 1 and abs(q)<=2):
        return  -1/(2.0*pow(h,2))*pow(2-abs(q),2)*q/abs(q)
    else:
        return  2/(3.0*h)*( - 3*abs(q)/h +9/4.0*pow(q,2)/h)*q/abs(q)

class Particle:
    def __init__(self,position,density,velocity,pressure,mass,h):
        self.density = density
        self.position = position
        self.velocity = velocity
        self.pressure = pressure
        self.mass = mass
        self.h = h
        self.energy =  pressure/(density*0.4)

    def cDensity(self,p):
        q = abs(self.position-p.position)/self.h
        wabh1 = cubicSpline(q,self.h)
        q = abs(self.position-p.position)/p.h
        wabh2 = cubicSpline(q,p.h)
        return 0.5*p.mass*(wabh1+wabh2)

    def cAccel(self,p):
        aVis = self.computeAVis(p)
        k = self.pressure/pow(self.density,2) +  p.pressure/pow(p.density,2) + aVis
        q = (self.position-p.position)/self.h
        wabh1 = cubicSplineD(q,self.h)
        q = (self.position-p.position)/p.h
        wabh2 = cubicSplineD(q,p.h)
        vab = self.velocity - p.velocity
        return  -k*p.mass*(wabh1+wabh2)/2, 0.25*k*p.mass*vab*(wabh1+wabh2)

    def computeAVis(self,p):
        vab = self.velocity - p.velocity
        rab = self.position - p.position
        hab = (self.h+p.h)/2
        if (vab*rab > 0):
            return 0
        ca = pow(1.4*self.pressure/self.density,0.5)
        cb = pow(1.4*p.pressure/p.density,0.5)
        cab = (ca+cb)/2
        muab = hab*vab*rab/(pow(rab,2)+0.00001)
        rhoab = (self.density+p.density)/2
        piab = -(cab*muab-pow(muab,2))/rhoab
        return piab

    def computeXsph(self,p):
        vba = p.velocity-self.velocity
        rhoab = (self.density+p.density)/2
        q = abs(self.position-p.position)/self.h
        wabh1 = cubicSpline(q,self.h)
        q = abs(self.position-p.position)/p.h
        wabh2 = cubicSpline(q,p.h)

        return p.mass*vba/rhoab*(wabh1+wabh2)/2
