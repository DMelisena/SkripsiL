import openmc
import numpy as np

statepoint = openmc.StatePoint('statepoint.20.h5')
tallies = statepoint.tallies
tally = tallies[1]

import matplotlib.pyplot as plt

flux = tally.get_slice(scores=['flux'])
data = flux.mean.flatten() #untuk mengubah data dari [[][][]],[[][... menjadi [ , , ,... ]
data_max=np.max(data)
scaled=data/data_max*100
x = np.linspace(-25, 25, len(scaled))
plt.plot(x, data)
plt.savefig('flux.png')
