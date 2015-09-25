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
    return elemFile,filename

if __name__ == '__main__':
    elemFile,filename = importfile()
    sim = Simulator()
    sim.updateElements(elemFile.Array)
    data,colors = sim.run(3)
