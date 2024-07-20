import openmc #type: ignore
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.ticker as mtick
import pandas as pd

statepoint = openmc.StatePoint('statepoint.5.h5')
tallies = statepoint.tallies
print(tallies)
tally = tallies[1] #2.5 depth {{{
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
#}}}

tally5 = tallies[2]#5 depth {{{

flux5 = tally5.get_slice(scores=['flux'])
data5 = flux5.mean.flatten()
x5 = np.linspace(-25, 25, len(data5))

max_index5=np.argmax(data5)
x_max5 = x5[max_index5]
y_max5 = np.max(data5)

#print(y_max5)
plt.axvline(x=x_max5,color='r',label='peak')
yflat5=data5/y_max5*100
#print(yflat5)

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
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.title('5 depth.png')
plt.savefig('5 depth.png')
plt.show()
#}}}

tally10 = tallies[3]#10 {{{
import matplotlib.pyplot as plt

flux10 = tally10.get_slice(scores=['flux'])
data10 = flux10.mean.flatten()
x10 = np.linspace(-25, 25, len(data10))

max_index10=np.argmax(data10)
x_max10 = x5[max_index10]
y_max10 = np.max(data10)

#print(y_max10)
plt.axvline(x=x_max10,color='r',label='peak')
yflat10=data10/y_max10*100
#print(yflat10)

fmt='%.0f%%' #changing into format
xticks = mtick.FormatStrFormatter(fmt)

#plt.yflat5.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(yflat)))
plt.plot(x10, yflat10,label="raw")

ysmooth10=np.interp(x10,x10,yflat10)
area_tofilter10=yflat10[start:end]
filtered10=savgol_filter(area_tofilter10,window_size,poly_order)
ysmooth10[start:end]=filtered10
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.plot(x10,ysmooth10,label="savgol filter")
plt.legend(loc='best')

plt.xlim(-25,25)
plt.ylim(0,105)
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.title('10 depth')
plt.savefig('10 depth.png')
plt.show()
#}}}

# lateral mixer {{{
plt.plot(x, yflat,label="2.5 cm raw")
plt.plot(x5, yflat5,label="5 cm raw")
plt.plot(x10, yflat10,label="10 cm raw")
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.xlim(-25,25)
plt.ylim(0,105)
plt.legend(loc='best')
plt.title("lateral unfiltered result")
plt.savefig("lateral unfiltered result")
plt.show()

plt.plot(x,ysmooth,label="2.5 cm filtered")
plt.plot(x5,ysmooth5,label="5 cm filtered")
plt.plot(x10,ysmooth10,label="10 cm filtered")
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.xlim(-25,25)
plt.ylim(0,105)
plt.legend(loc='best')
plt.title("filtered result comparison")
plt.savefig("filtered result comparison")
plt.show()
# }}}

tal = statepoint.tallies[4] # dpp 0.1 tally{{{
fluxv = tal.get_slice(scores=['flux'])
dosev = tal.mean.flatten()
datay = fluxv.mean.flatten()

datanew=(datay,dosev)
df=pd.DataFrame(datanew)
df.to_csv("fluxanddose123.csv")
x = np.linspace(-25, 25, len(datay))
max_index=np.argmax(datay)
y_max_con = np.max(datay)

v=0.1*0.1*0.1
wpdose=y_max_con
conversion = 36e7*v/wpdose
print("\n\n\nconversion = ",conversion,"\n\n\n")

#TODO: Search the value of flux on dose values
print("=========================")
print("search the value of flux")
print(datay)
print(np.max(datay))
print(np.argmax(datay))
maxdoseadress=np.argmax(datay)
print(maxdoseadress)
fluxymax=dosev[maxdoseadress]

print(fluxymax)

print("=========================")

xv=np.linspace(0,30,len(datay))
ymaxv=np.max(datay)
yflatv=datay/ymaxv*100
plt.plot(xv,yflatv,label="dpp")
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.legend(loc='best')
plt.title("depth dose raw")
plt.xlim(0,30)
plt.ylim(0,105)
plt.savefig("depth dose raw.png")
plt.show()

# }}}

tal = statepoint.tallies[5] # dpp wide tally {{{
fluxv = tal.get_slice(scores=['flux'])
#print("tal = ",tal)
datay = fluxv.mean.flatten()
xv=np.linspace(0,30,len(datay))
ymaxv=np.max(datay)
yflatv=datay/ymaxv*100
plt.plot(xv,yflatv,label="dpp")

n = len(datay)
#print(len(datay))
d=30
datax = np.linspace(0,d,n)
print("d/n = ",d/n)
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

#print(y_max)
plt.axvline(x=x_maxs,color='r',label=f'peak{x_maxs}')

plt.plot(datax, datay)
plt.xlim(0,30)
plt.ylim(0,105)
plt.legend(loc='best')
plt.ylabel("Relative Dose (%)")
plt.xlabel("Position (cm)")
plt.title("depth dose widetally.png")
plt.savefig("depth dose widetally.png",dpi=200)
plt.show()
# }}}
#
# 1 cGy = 1 MU =

#openmc output = pSv/cm2
#flux = particle-cm per source particle
#dose = pSv cm^2
#  1MU = 1cGy
# dose = celldosevalues *s_rate/ vcell #pSvcm3/src * (src/s) / cm3= pSv/s
# dose * flux * src_rate * t / V = [pSv cm²] [p-cm/src] [src/sec] [sec] / [cm³] = [pSv]
#https://openmc.discourse.group/t/openmc-data-dose-coefficients/1634/2
# 1cGy = 1e10 pSv
# 1e10pSv = dose * flux * src_rate * t / V
#
# 1e10pSv/s = dose * flux * src_rate / V
#  600 MU/min = 600 uSv/min = 6e12pSv/min
# 6e12pSv/min = dose * flux*src_rate /V
# 1e11 pSv/s =dose * flux*src_rate /V
# src_rate= (6e12pSv/min * V)/dose*flux5
# 
# 600 Mu/min = 600 cSv/min = 6e6uSv/min=36e7uSv/hr
# 36uSv/hr = conversion*dosein/ v
"""
src_rate= 1e11*volume_wp/(wpdose*fluxymax)
print(f"src_rate = 1e11 pSv/s * (volume_wp) cm3 / ({wpdose}pSv cm² * {fluxymax}p-cm/src) = {src_rate}src/sec")
print(f"src_rate={src_rate}src/sec")

# 6e12pSv/min = dose * flux*src_rate /V
# Cfactor = flux*src_rate
# 6e12pSv/min = dose * Cfac / V
# cfac = 6e12pSv*V/(dose)

mu=1e11 #600 MU/min = 10 cGy/s = 1e11 pSv/s 
#print( f"\ncfactor = 1e11 pSv/sec*{v}cm3/(dose({wpdose}))")
print( f"\ncfac= {1e11*v/wpdose}")
print( f"cres=cfac*cconv= {1e11*v/wpdose}*{3600/1e6} = ",1e11*v/wpdose*(3600/1e6),"\n")
cfac=1e11*v/wpdose
cconv=3600/1e6
cres= cfac*cconv
print("cres = ",cres)
print(f"\ndose = x*cfac/v={wpdose*cfac/v}uSv/s\n")
print(f"\ndose = (x*cfac/v)*(3.6e9)={wpdose*cfac/v}*{3600/1e6}={wpdose*cfac/v*3600/1e6}uSv/hr\n")
print(f"\ndose = (x*cfac/v)*(3.6e9)={wpdose*cfac/v}*{60/1e10}={wpdose*cfac/v*60/1e10}MU/min\n")
"""





"""
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


print(f"k smoothen = {volume_wp/y_maxs*36}")
"""
