import openmc
import numpy as np

statepoint = openmc.StatePoint('statepoint.100.h5')
tallies = statepoint.tallies
tally = tallies[1]

import matplotlib.pyplot as plt

flux = tally.get_slice(scores=['flux'])
data = flux.mean.flatten()
x = np.linspace(-15, 15, len(data))

max_index=np.argmax(data)
x_max = x[max_index]
plt.axvline(x=x_max,color='r')

plt.plot(x, data)
plt.savefig('flux.png')
plt.show()
