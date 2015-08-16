import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

class ParticlePlotter:
    fig = plt.figure()
    def __init__(self,a,b):
        self.ax = plt.axes(xlim=a,ylim=b)
        self.particles =  self.ax.scatter([],[])
        self.counter = 0
    
    def update(self,data,colors):
        self.data = data
        self.colors = colors

    def plottrace(self):
        dataX = []
        dataY = []
        points = self.data[0]
        for  point in points:
            dataX.append([])
            dataY.append([])
        for points in self.data:
            for i in range(len(points)):
                dataX[i].append(points[i].real)
                dataY[i].append(points[i].imag)
        for i in range(len(dataX)):
            plt.plot(dataX[i],dataY[i])
    
    def init(self):
        if (self.counter >= len(self.data)):
            self.particles =  self.ax.scatter([],[])
            return self.particles
        dataArray = self.data[self.counter]
        self.counter = self.counter+1
        elemPointsX = []
        for elements in dataArray:
            elemPointsX.append([elements.real,elements.imag])

        particlesX = np.array(elemPointsX)
        self.particles.set_animated(True)
        self.particles =  self.ax.scatter(particlesX[:,0],particlesX[:,1],c = self.colors)
        return self.particles

    def animationupdate(self,count):
        if (self.counter >= len(self.data)):
            return self.particles
        dataArray = self.data[self.counter]
        self.counter = self.counter+1
        elemPointsX = []
        for elements in dataArray:
            elemPointsX.append([elements.real,elements.imag])
        particlesX = np.array(elemPointsX)
        self.particles.set_offsets(particlesX)
        return self.particles

    def run(self,filename):
        self.plottrace()
        """ 
        ani = animation.FuncAnimation(self.fig, self.animationupdate,
                save_count=150,blit=False, interval=1,init_func=self.init)
       
        # Set up formatting for the movie files
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        #ani.save(filename +'.mp4', writer=writer)
        """
        
        plt.show()

