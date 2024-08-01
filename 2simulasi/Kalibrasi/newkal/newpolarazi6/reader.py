import openmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.ticker as mtick
##

sp = openmc.StatePoint('statepoint.5.h5')
##
print(sp.n_particles)

n = 300
d = 30
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
plt.axvline(x=x_max, color='r')
plt.legend(loc='best')
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.xlim(-0,30)
plt.ylim(0,105)
datay=datay/y_max*100
print(datay[max_index])
plt.plot(datax, datay)

tal = sp.tallies[1]
datay = tal.mean
print(tal.mean)
datay=datay/y_max*100
print(len(datay))
print(datay)
n = len(datay)
DF = pd.DataFrame(datay) 
DF.to_csv("data1.csv")
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
plt.plot(x_smooth, y_smooth)
plt.title(f'x_max = {x_max} cm \n xsmooth_max = {x_maxs} cm')
plt.savefig('pdd.png')
plt.show()
"""
tal = sp.tallies[2]
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
#plt.axvline(x=x_max, color='r')
plt.legend(loc='best')
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.xlim(-0,30)
plt.ylim(0,105)
datay=datay/y_max*100
plt.plot(datax, datay)

tal = sp.tallies[1]
datay = tal.mean
datay=datay/y_max*100
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
plt.plot(x_smooth, y_smooth)
# draw line at x_max
#plt.axvline(x=x_maxs, color='r')
# write x_max value on plot
plt.title(f'x_max = {x_max} cm \n xsmooth_max = {x_maxs} cm')
#print(f"Y Value on xmax={_max}")
plt.show()
plt.savefig('2.5 depth.png')

def rounde(unrounded):
    roundede="{:.4e}".format(unrounded)
    return roundede

print(f"\nDosis = {rounde(y_max)}pSvcm3/src") 
print(f"Dosis smoothen = {rounde(y_maxs)}pSvcm3/src\n")

print(f"s_rate=mu*volume_wp/phandosevalues") # mu=
mu=1e11#600 MU/min = 10 cGy/s = 1e11 pSv/s 
volume_wp=(d/n)*6*6
wpdose=y_max
s_rate=mu*volume_wp/wpdose

print(f"s_rate={mu}*{volume_wp}/{rounde(wpdose)}={s_rate}")
#600cGy/min=36000cGy/h=36uSv/h
print(f"600 cgy/min = 36uSv/h")
print(f"\n36uSv/h = k * {y_max} pSvcm3/src/{volume_wp}cm3\n")
k=volume_wp/y_max*36
print(f"k * {y_max} pSvcm3/src/{volume_wp}cm3 = {k*y_max/volume_wp}uSv/h")
print(f"36 uSv/h = {k*y_max/volume_wp} uSv/h")
print(f"k = {k}")


print(f"k smoothen = {volume_wp/y_maxs*36}")

tally = sp.tallies[3] #2.5 depth {{{
import matplotlib.pyplot as plt

flux = tally.get_slice(scores=['flux'])
data = tally.mean.flatten()
x = np.linspace(-25, 25, len(data))

max_index=np.argmax(data)
x_max = x[max_index]
y_max = np.max(data)
print("ymax = ", y_max)
plt.axvline(x=x_max,color='r',label='peak')
yflat=data/y_max*100
#print(yflat)

fmt='%.0f%%' #changing into format
xticks = mtick.FormatStrFormatter(fmt)

#plt.yflat.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(yflat)))
plt.plot(x, yflat,label="raw")

ysmooth=np.interp(x,x,yflat)
window_size=300
poly_order=10
start=100
end=400
area_tofilter=yflat[start:end]
filtered=savgol_filter(area_tofilter,window_size,poly_order)
ysmooth[start:end]=filtered
plt.plot(x,ysmooth,label="savgol filter")
plt.legend(loc='best')
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.xlim(-25,25)
plt.ylim(0,105)

plt.title('2.5 depth.png')
plt.savefig('2.5 depth.png')
plt.show()
"""
