import sys
sys.path.insert(0, '../common')

from simulator  import Simulator
import plotter as p
import simulator
import importlib

#Import the file to be simulated
def importfile():
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])
    else:
        print("Give the name of import file")
        exit()

    try:
        elemFile = importlib.import_module(filename, package=None)
    except ImportError:
        print("No such Import exist")
        exit()

#Overriding the Simulator Variables
    simulator.TIME_STEP = elemFile.TIME_STEP
    simulator.UPDATE_FRAMES = elemFile.UPDATE_FRAMES
    simulator.SIM_TIME = elemFile.SIM_TIME
    try:
        simulator.MODE = elemFile.MODE
    except AttributeError:
        simulator.MODE = 'RK'
    return elemFile,filename

if __name__ == '__main__':
    elemFile,filename = importfile()
    sim = Simulator()
    sim.parse_from_file(elemFile.Array)
    data,colors = sim.run(simulator.SIM_TIME)
    plotter = p.ParticlePlotter((-2,2),(-2,2))
    plotter.update(data,colors)
    plotter.run(filename,False,True,False)
