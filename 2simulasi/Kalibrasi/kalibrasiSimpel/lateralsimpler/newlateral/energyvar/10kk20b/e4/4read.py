import openmc
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.ticker as mtick

statepoint = openmc.StatePoint('statepoint.20.h5')
tallies = statepoint.tallies

tally = tallies[1]
import matplotlib.pyplot as plt

flux = tally.get_slice(scores=['flux'])
data = flux.mean.flatten()
x = np.linspace(-25, 25, len(data))

max_index=np.argmax(data)
x_max = x[max_index]
y_max = np.max(data)

print(y_max)
plt.axvline(x=x_max,color='r',label='peak')
yflat=data/y_max*100
print(yflat)

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

plt.title('2.5 depth.png')
plt.savefig('2.5 depth.png')
plt.show()

tally5 = tallies[2]
import matplotlib.pyplot as plt

flux5 = tally5.get_slice(scores=['flux'])
data5 = flux5.mean.flatten()
x5 = np.linspace(-25, 25, len(data5))

max_index5=np.argmax(data5)
x_max5 = x5[max_index5]
y_max5 = np.max(data5)

print(y_max5)
plt.axvline(x=x_max5,color='r',label='peak')
yflat5=data5/y_max5*100
print(yflat5)

fmt='%.0f%%' #changing into format
xticks = mtick.FormatStrFormatter(fmt)

#plt.yflat5.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(yflat)))
plt.plot(x5, yflat5,label="raw")

ysmooth5=np.interp(x5,x5,yflat5)
area_tofilter5=yflat5[start:end]
filtered5=savgol_filter(area_tofilter5,window_size,poly_order)
ysmooth5[start:end]=filtered5
plt.plot(x5,ysmooth5,label="savgol filter")
plt.legend(loc='best')
plt.xlim(-25,25)
plt.ylim(0,105)
plt.title('5 depth.png')
plt.savefig('5 depth.png')
plt.show()


tally10 = tallies[3]
import matplotlib.pyplot as plt

flux10 = tally10.get_slice(scores=['flux'])
data10 = flux10.mean.flatten()
x10 = np.linspace(-25, 25, len(data10))

max_index10=np.argmax(data10)
x_max10 = x5[max_index10]
y_max10 = np.max(data10)

print(y_max10)
plt.axvline(x=x_max10,color='r',label='peak')
yflat10=data10/y_max10*100
print(yflat10)

fmt='%.0f%%' #changing into format
xticks = mtick.FormatStrFormatter(fmt)

#plt.yflat5.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(yflat)))
plt.plot(x10, yflat10,label="raw")

ysmooth10=np.interp(x10,x10,yflat10)
area_tofilter10=yflat10[start:end]
filtered10=savgol_filter(area_tofilter10,window_size,poly_order)
ysmooth10[start:end]=filtered10
plt.plot(x10,ysmooth10,label="savgol filter")
plt.legend(loc='best')

plt.xlim(-25,25)
plt.ylim(0,105)
plt.title('10 depth.png')
plt.savefig('10 depth.png')
plt.show()

plt.plot(x, yflat,label="2.5 cm raw")
plt.plot(x5, yflat5,label="5 cm raw")
plt.plot(x10, yflat10,label="10 cm raw")
plt.xlim(-25,25)
plt.ylim(0,105)
plt.legend(loc='best')
plt.title("lateral unfiltered result")
plt.savefig("lateral unfiltered result")
plt.show()

plt.plot(x,ysmooth,label="2.5 cm filtered")
plt.plot(x5,ysmooth5,label="5 cm filtered")
plt.plot(x10,ysmooth10,label="10 cm filtered")
plt.xlim(-25,25)
plt.ylim(0,105)
plt.legend(loc='best')
plt.title("filtered result comparison")
plt.savefig("filtered result comparison")
plt.show()

tal = statepoint.tallies[4]
fluxv = tal.get_slice(scores=['flux'])
print("tal = ",tal)
datay = fluxv.mean.flatten()
xv=np.linspace(0,30,len(datay))
ymaxv=np.max(datay)
yflatv=datay/ymaxv*100
plt.plot(xv,yflatv,label="dpp")

n = len(datay)
print(len(datay))
d=30
datax = np.linspace(0,d,n)
x_smooth=datax
y_smooth = np.interp(x_smooth, datax, datay)
# print (f"datay =\n {datay}")
# print (f"ysmooth=\n{y_smooth}")

# Apply Savitzky-Golay filter for smoothing
window_size = 20
poly_order =5
#y_smooth = savgol_filter(y_smooth, window_size, poly_order)

max_index=np.argmax(y_smooth)
x_maxs = x_smooth[max_index]
y_maxs=y_smooth[max_index]
plt.plot(x_smooth, datay)
plt.savefig("depth dose.png")
plt.show()

# draw line at x_max
plt.axvline(x=x_maxs, color='r')
# write x_max value on plot
plt.title(f'Depth Dose\nx_max = {x_max}')
#print(f"Y Value on xmax={_max}")
plt.xlim(0,30)
#plt.ylim(0,105)
plt.legend(loc='best')
#plt.title("filtered result comparison")
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
