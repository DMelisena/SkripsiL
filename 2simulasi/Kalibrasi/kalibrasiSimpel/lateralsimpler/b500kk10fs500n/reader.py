import openmc
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import pandas as pd
##

sp = openmc.StatePoint('statepoint.30.h5')
##

n = 500
d = 50
tal = sp.tallies[1]
print(sp.tallies[1])
#print(sp.tallies[2])

datay = tal.mean
talstd= tal.std_dev
datay.shape=datay.shape[0]
talstd.shape=talstd.shape[0]
stdpercent=talstd/datay
print(stdpercent," %")
#print("std mean = ",)
DF = pd.DataFrame(stdpercent) 
# save the dataframe as a csv file 
DF.to_csv("data1.csv")
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
plt.plot(datax, datay)

#TODO: Add program to printout std dev
talval=tal.get_values()
talstd=tal.std_dev
#making it into an array
talval.shape=talval.shape[0]
talstd.shape=talstd.shape[0]
print("tal std dev = ",talstd)
dose =talval
dosestddev=talstd

for v,s in zip(dose,dosestddev):
    f=open("output.txt","a")
    print(f'{v:.7e} +- {s:.7e}uSv/h')
    f.write(str(f'\n{v} +- {s} uSv/h'))
    f.close()

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
plt.plot(x_smooth, y_smooth)

# draw line at x_max
plt.axvline(x=x_maxs, color='r')
# write x_max value on plot
plt.title(f'x_max = {x_max}')
#print(f"Y Value on xmax={_max}")
plt.show()

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
