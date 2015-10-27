import pickle
import matplotlib.pyplot as plt


with open('data/pressure', 'rb') as f:
    pressure = pickle.load(f)
    
with open('data/position', 'rb') as f:
    position = pickle.load(f)

with open('data/velocity', 'rb') as f:
    velocity = pickle.load(f)

with open('data/density', 'rb') as f:
    density = pickle.load(f)

with open('data/energy', 'rb') as f:
    energy = pickle.load(f)


with open('data/ae', 'rb') as f:
    ae =  [float(x) for x in  f.read().splitlines()]
with open('data/ax', 'rb') as f:
    ax =  [float(x) for x in  f.read().splitlines()]
with open('data/ap', 'rb') as f:
    ap =  [float(x) for x in  f.read().splitlines()]
with open('data/ad', 'rb') as f:
    ad =  [float(x) for x in  f.read().splitlines()]
with open('data/au', 'rb') as f:
    au =  [float(x) for x in  f.read().splitlines()]



plt.subplot(2,2,1)
plt.plot(position,velocity,label="velocity")
plt.plot(ax,au,label="analytical")
plt.legend()
plt.subplot(2,2,2)
plt.plot(position,pressure,label="pressure")
plt.plot(ax,ap,label="analytical")
plt.legend()
plt.subplot(2,2,3)
plt.plot(position,energy,label="energy")
plt.plot(ax,ae,label="analytical")
plt.legend()
plt.subplot(2,2,4)
plt.plot(position,density,label="density")
plt.plot(ax,ad,label="analytical")
plt.legend()
plt.show()
