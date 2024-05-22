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
