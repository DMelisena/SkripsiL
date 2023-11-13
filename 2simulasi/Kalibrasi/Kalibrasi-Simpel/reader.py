import openmc
import matplotlib.pyplot as plt
import numpy as np

##

sp = openmc.StatePoint('statepoint.500.h5')
##

n = 1000
d = 50
tal = sp.tallies[1]
datay = tal.mean
# datax is linspace between 0 and 50
datax = np.linspace(0,d,n)
datay.shape = (n,)
# smooth datay
# datay = np.convolve(datay, np.ones(10)/10, mode='same')
# find the index of the maximum value in datay
max_index = np.argmax(datay)
x_max = datax[max_index]
plt.plot(datax, datay)

# draw line at x_max
plt.axvline(x=x_max, color='r')
# write x_max value on plot
plt.title(f'x_max = {x_max}')

plt.show()
