from particle import Particle

def initParticle():
    particleArray = []
    h = 0.0625
    x = -0.625; #Creating the boundary element 
    rho = 1.0
    p = 1.0
    u =0
    delx = 0.0015625
    mass = rho*delx 
    for i in range(400):
        particleArray.append(Particle(x,rho,u,p,mass))
        x = x+ delx
    x = 0
    delx = 0.0625
    p = 0.1
    rho = 0.25;
    for i in range(100):
        x = x+ 0.0625
        particleArray.append(Particle(x,rho,u,p,mass))

def computeNextTimeStep(particleArray):
    for (i in range(80,480))
        get
if __name__ == '__main__'
    startPoint =  80
    endPoint = 480
    particleArray = initParticle()
