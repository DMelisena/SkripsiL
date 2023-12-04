import openmc
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
##

sp = openmc.StatePoint('statepoint.10.h5')
##

nx = 1000
d = 10
tal = sp.tallies[1]
datay = tal.mean
# datax is linspace between 0 and 50
datax = np.linspace(0,d,nx)
datay.shape = (nx,)
plt.plot(datax, datay, label='unpolished')
# smooth datay
datay = np.convolve(datay, np.ones(10)/10, mode='same')
# find the index of the maximum value in datay
max_index = np.argmax(datay)
x_max = datax[max_index]
y_max = datay[datay.argmax()]
print(x_max,max_index,y_max)

y_max=datay[max_index]
plt.axvline(x=x_max, color='r')
plt.plot(datax, datay, label='Convolved')
plt.xlabel('Distance (cm)')
plt.ylabel('Dose (pSvcm3/src)')


tal = sp.tallies[1]
datay = tal.mean
n = len(datay)

x_smooth=datax
y_smooth = np.interp(x_smooth, datax, datay)
# print (f"datay =\n {datay}")
# print (f"ysmooth=\n{y_smooth}")

# Apply Savitzky-Golay filter for smoothing
window_size = 200
poly_order =5
y_smooth = savgol_filter(y_smooth, window_size, poly_order)

max_index=np.argmax(y_smooth)
x_maxs = x_smooth[max_index]
y_maxs=y_smooth[max_index]
plt.plot(x_smooth, y_smooth,label='Smoothen')
# draw line at x_max
plt.axvline(x=x_maxs, color='r')
# write x_max value on plot
#print(f"Y Value on xmax={_max}")
plt.savefig('KalibrationResult.png',dpi=300)

def rounde(unrounded):
    roundede="{:.4e}".format(unrounded)
    return roundede

print(f"\nDosis = {rounde(y_max)}pSvcm3/src") 
print(f"Dosis smoothen = {rounde(y_maxs)}pSvcm3/src\n")
plt.title(f'x_max = {x_max}\ny_max = {y_max}')
print(f"s_rate=mu*volume_wp/phandosevalues") # mu=
#mu=1e11#600 MU/min = 10 cGy/s = 1e11 pSv/s 
volume_wp=(d/nx)*6*6
wpdose=y_max
#s_rate=mu*volume_wp/wpdose

#print(f"s_rate={mu}*{volume_wp}/{rounde(wpdose)}={s_rate}")
#600cGy/min=36000cGy/h=36uSv/h
print(f"600 cgy/min = 36000cGy/h=36000e4uSv/h")#600*60*10000
print(f"\n360000000uSv/h = k * {y_max} pSvcm3/src/{volume_wp}cm3\n")
k=volume_wp*36e7/y_max
print(f"k * {y_max} pSvcm3/src/{volume_wp}cm3 = {k*y_max/volume_wp}uSv/h")
print(f"36 uSv/h = {k*y_max/volume_wp} uSv/h")
print(f"k = {k}")

print(f"k smoothen = {volume_wp/y_maxs*36e7}")
plt.legend()
plt.show()