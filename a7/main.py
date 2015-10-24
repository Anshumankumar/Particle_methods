from particle import Particle
from copy import deepcopy
import pickle

class ShockTube():
    def __init__(self,tTime,timeStep):
        self.tTime  = tTime
        self.timeStep = timeStep
        particleArray = []

    def run(self):
        self.initParticle()
        simTime = 0;
        while(simTime < self.tTime):
            print('Sim Time:', simTime)
            simTime = simTime + self.timeStep
            pArray2 = deepcopy(self.particleArray[self.sP:self.eP])
            self.computeNext(self.particleArray,pArray2,self.timeStep)
            self.particleArray[self.sP:self.eP] = pArray2
    
    def initParticle(self):
        self.particleArray = []
        x = -0.6250; #Creating the boundary element 
        rho = 1.0
        p = 1.0
        u =0
        delx = 0.00156250
        h = 2*0.00625
        mass = rho*delx 
        for i in range(400):
            self.particleArray.append(Particle(x,rho,u,p,mass,h))
            x = x+ delx
        x = 0
        delx = 0.00625
        p = 0.1
        rho = 0.25;
        for i in range(100):
            x = x+ delx
            self.particleArray.append(Particle(x,rho,u,p,mass,h))
        self.sP = 80
        self.eP = 480
    def computeNext(self,sourceArray,targetArray,tS):
        for particleA in targetArray:
            density = 0
            accelV = 0
            accelE = 0
            for particleB in sourceArray:
                density = density +particleA.cDensity(particleB)
                dAccelV,dAccelE = particleA.cAccel(particleB)
               # print('dAccelV',dAccelV)
                accelV = accelV + dAccelV
                accelE = accelE + dAccelE
            particleA.density = density
            particleA.velocity = particleA.velocity + accelV*tS
            particleA.energy = particleA.energy + accelE*tS
            particleA.pressure = 0.4*particleA.density*particleA.energy
            particleA.position = particleA.position+particleA.velocity*tS
        print (targetArray[300].velocity)

    def plot(self):
        pressure = []
        position = []
        velocity = []
        density = []
        for p in self.particleArray:
            pressure.append(p.pressure)
            position.append(p.position)
            velocity.append(p.velocity)
            density.append(p.density)
        with open('pressure', 'wb') as f:
                pickle.dump(pressure, f)
        with open('position', 'wb') as f:
                pickle.dump(position, f)
        with open('velocity', 'wb') as f:
                pickle.dump(velocity, f)
        with open('density', 'wb') as f:
                pickle.dump(density, f)




if __name__ == '__main__':
    simulator = ShockTube(0.2,0.0001)
    simulator.run()
    simulator.plot()
