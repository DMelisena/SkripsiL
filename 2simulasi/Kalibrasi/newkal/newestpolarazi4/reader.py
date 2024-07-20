import openmc
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
##

sp = openmc.StatePoint('statepoint.5.h5')
tallies=sp.tallies
##
print(sp.n_particles)
print(sp.tallies)

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


tally5 = sp.tallies[3]#5 depth {{{

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

tally10 = sp.tallies[3]#10 {{{
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

