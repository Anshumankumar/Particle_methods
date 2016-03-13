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
            pArray3 = deepcopy(self.particleArray[self.sP:self.eP])
            self.computeNext(self.particleArray,pArray2,self.timeStep)
            self.particleArray[self.sP:self.eP] = pArray2
    
    def initParticle(self):
        self.particleArray = []
        x = -0.625; #Creating the boundary element
        rho = 1.0
        p = 1.0
        u =0
        delx = 0.0015625
        h =2*0.006250
        mass = delx 
        for i in range(400):
            self.particleArray.append(Particle(x,rho,u,p,mass,h))
            x = x+ delx
        x = 0
        delx = 0.00625
        p = 0.1
        mass = 0.00156250
        rho = 0.25;
        for i in range(100):
            x = x+ delx
            self.particleArray.append(Particle(x,rho,u,p,mass,h))
        self.sP = 80
        self.eP = 480
    def computeBins(self,sourceArray):
        binDict = {}
        for i in range(50):
            binDict[i] = []
        for particleB in sourceArray:
            binId = int((particleB.position+0.625)/0.025)
            binDict[binId].append(particleB)
        return binDict
    
    def computeNext(self,sourceArray,targetArray,tS):
        binDict = self.computeBins(sourceArray)    
        for particleA in targetArray:
            density = 0
            i = int((particleA.position+0.625)/0.025)
            currentArray = binDict[i] + binDict[i-1] + binDict[i+1]
            for particleB in currentArray:
                density = density +particleA.cDensity(particleB)
            particleA.density = density
            particleA.pressure = 0.4*particleA.density*particleA.energy

        sourceArray[self.sP:self.eP] = deepcopy(targetArray)
        binDict = self.computeBins(sourceArray)    
        for particleA in targetArray:
            accelV = 0
            accelE = 0
            i = int((particleA.position+0.625)/0.025)
            currentArray = binDict[i] + binDict[i-1] + binDict[i+1]
            for particleB in currentArray:
                dAccelV,dAccelE = particleA.cAccel(particleB)
                accelV = accelV + dAccelV
                accelE = accelE + dAccelE
            particleA.velocity = particleA.velocity + accelV*tS
            particleA.energy = particleA.energy + accelE*tS
        
        binDict = self.computeBins(targetArray)    
        for particleA in targetArray:
            v = particleA.velocity
            i = int((particleA.position+0.625)/0.025)
            currentArray = binDict[i] + binDict[i-1] + binDict[i+1]
            for particleB in currentArray:
                v = v+0.1*particleA.computeXsph(particleB) 
            particleA.position = particleA.position+v*tS


    def save(self):
        pressure = []
        position = []
        velocity = []
        density = []
        energy = []
        for p in self.particleArray:
            pressure.append(p.pressure)
            position.append(p.position)
            velocity.append(p.velocity)
            density.append(p.density)
            energy.append(p.energy)
        with open('data/pressure', 'wb') as f:
            pickle.dump(pressure, f)
        with open('data/position', 'wb') as f:
            pickle.dump(position, f)
        with open('data/velocity', 'wb') as f:
            pickle.dump(velocity, f)
        with open('data/density', 'wb') as f:
            pickle.dump(density, f)
        with open('data/energy', 'wb') as f:
            pickle.dump(energy, f)



if __name__ == '__main__':
    simulator = ShockTube(0.5,0.002)
    simulator.run()
    simulator.save()
