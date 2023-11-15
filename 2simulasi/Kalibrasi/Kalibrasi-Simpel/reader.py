import openmc
import matplotlib.pyplot as plt
import numpy as np

##

sp = openmc.StatePoint('statepoint.100.h5')
##

n = 1000
d = 10
tal = sp.tallies[1]
datay = tal.mean
# datax is linspace between 0 and 50
datax = np.linspace(0,d,n)
datay.shape = (n,)
# smooth datay
datay = np.convolve(datay, np.ones(10)/10, mode='same')
# find the index of the maximum value in datay
max_index = np.argmax(datay)
x_max = datax[max_index]
y_max = datay[datay.argmax()]
print(x_max,max_index,y_max)

y_max=datay[max_index]
plt.plot(datax, datay)

# draw line at x_max
plt.axvline(x=x_max, color='r')
# write x_max value on plot
plt.title(f'x_max = {x_max}')
#print(f"Y Value on xmax={_max}")
plt.show()

print(f"Dosis = {y_max}")
print(f"s_rate=mu*volume_wp/phandosevalues") # mu=
mu=1e11#600 MU/min = 10 cGy/s = 1e11 pSv/s 
volume_wp=(d/n)*6*6
phandosevalues=y_max
s_rate=mu*volume_wp/phandosevalues
print(f"s_rate={mu}*{volume_wp}/{phandosevalues}={s_rate}")