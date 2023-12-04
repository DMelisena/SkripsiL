import openmc
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
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


tal = sp.tallies[1]
datay = tal.mean
n = len(datay)

# Generate x data
datax = np.linspace(0, 10, n)

# Increase the number of data points
n_smooth = 1000
x_smooth = np.linspace(0, 10, n_smooth)
y_smooth = np.interp(x_smooth, datax, datay)

# Apply Savitzky-Golay filter for smoothing
#window_size = 200
#poly_order =5
#y_smooth = savgol_filter(y_smooth, window_size, poly_order)

x_max = datax[max_index]
y_max = datay[datay.argmax()]
print(x_max,max_index,y_max)

""" #Smoothen Graphic
max_index=np.argmax(y_smooth)
x_max = x_smooth[max_index]
y_max=y_smooth[max_index]
plt.plot(x_smooth, y_smooth)
"""
# draw line at x_max
plt.axvline(x=x_max, color='r')
# write x_max value on plot
plt.title(f'x_max = {x_max}')
#print(f"Y Value on xmax={_max}")
plt.show()

print(f"Dosis = {y_max}pSvcm3/src")
print(f"s_rate=mu*volume_wp/phandosevalues") # mu=
mu=1e11#600 MU/min = 10 cGy/s = 1e11 pSv/s 
volume_wp=(d/n)*6*6
wpdose=y_max
s_rate=mu*volume_wp/wpdose

def rounde(unrounded):
    roundede="{:.4e}".format(unrounded)
    return roundede

print(f"s_rate={mu}*{volume_wp}/{rounde(wpdose)}={s_rate}")
#600cGy/min=36000cGy/h=36uSv/h
print(f"600 cgy/min = 36uSv/h")
print(f"\n36uSv/h = k * {y_max} pSvcm3/src/{volume_wp}cm3\n")
k=volume_wp/y_max*36
print(f"k * {y_max} pSvcm3/src/{volume_wp}cm3 = {k*y_max/volume_wp}uSv/h")
print(f"36 uSv/h = {k*y_max/volume_wp} uSv/h")
print(f"k = {k}")