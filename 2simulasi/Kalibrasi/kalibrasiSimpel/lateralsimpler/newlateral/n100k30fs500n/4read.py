import openmc
import numpy as np
from scipy.signal import savgol_filter

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

plt.plot(x, data,label="raw")

xsmooth=x
ysmooth=np.interp(x,x,data)
window_size=200
poly_order=5
ysmooth=savgol_filter(ysmooth,window_size,poly_order)

plt.plot(xsmooth,x,ysmooth,label="smooth")


plt.savefig('flux.png')
plt.show()
