import openmc
import numpy as np

statepoint = openmc.StatePoint('statepoint.100.h5')
tallies = statepoint.tallies
tally = tallies[1]

import matplotlib.pyplot as plt

flux = tally.get_slice(scores=['flux'])
data = flux.mean.flatten()
x = np.linspace(-15, 15, len(data))
plt.plot(x, data)
plt.savefig('flux.png')