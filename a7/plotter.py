import pickle
import matplotlib.pyplot as plt

with open('pressure', 'rb') as f:
    pressure = pickle.load(f)
    
with open('position', 'rb') as f:
    position = pickle.load(f)

with open('velocity', 'rb') as f:
    velocity = pickle.load(f)

with open('density', 'rb') as f:
    density = pickle.load(f)

plt.plot(position,velocity)
plt.show()
