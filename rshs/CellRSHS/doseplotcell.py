import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.10000.h5')

f=open("output.txt","w")
f.write(str(sp.tallies))
f.close()

meshtally = sp.tallies[1]


x=500#harus sama dengan resolusi pada file utama
y=500
#s_rate=4.87805e7 #source rate ICRP 116
#s_rate=34.52580998
#dose=dosevalues*1000*3600 #microsieverts/hour

s_rate=34525809.98
v=(2000/x)*(2000/y)*300 #volume of room dose distribution
dosevalues=meshtally.get_values()
dosevalues.shape=(x,y)
dosevalues = dosevalues*s_rate/v #picosieverts/s
dose=(dosevalues/1000000)*3600 #microsieverts/hour


fig, ax = plt.subplots()
cs = ax.imshow(dose, cmap='coolwarm', norm=LogNorm()) # type: ignore
cb = plt.colorbar(cs)
ax.set_title('Power density (kW/cm$^3$)') #type: ignore
plt.savefig('RoomDoseDistribution.png',dpi=900 )
plt.axis('off')

phantally = sp.tallies[3]
phandosevalues = phantally.get_values()#pSvcm3/src
phandosestddev = phantally.std_dev 

phandosevalues.shape = phandosevalues.shape[0]
phandosestddev.shape = phandosestddev.shape[0]

axvcell=5*10*10#cm3
mu=1e11#pSv/s
s_rate=mu*axvcell/phandosevalues #src/s
factorMU = 60/1e10 # pSv/s -> MU/min
factoruSv = 3600/1e6 # pSv/s -> uSv/h

print(f"source rate *phantomdosevaluse/v cell axis= mu\n{s_rate}x{phandosevalues}/{axvcell}={mu}\n=")
print(f"{phandosevalues*s_rate/axvcell} pSv/s")
print(f"{phandosevalues*s_rate/axvcell*60/1e10} MU")#pSv/sec*(src/s)/cm3
#phandosevalues = phandosevalues * s_rate / axvcell /1000000*3600 #
#phandosestddev = phandosestddev * s_rate / axvcell

phandosevalues *= factoruSv
phandosestddev *= factoruSv
for v,s in zip(phandosevalues,phandosestddev):
    f=open("output.txt","a")
    print(f'{v} +- {s}')
    f.write(str(f'\n{v} +- {s}'))
    f.close()

celltally = sp.tallies[2]
celldosevalues = celltally.get_values() #pSvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 

celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

vcell=10.8*50*200

dose = celldosevalues *s_rate/ vcell #pSvcm3/src * (src/s) / cm3= pSv/s
dose=dose/1e6*3600 #pSv/s -> uSv/h
dosestddev = (celldosestddev * s_rate / vcell) *(1e6/3600) 

for v,s in zip(dose,dosestddev):
    f=open("output.txt","a")
    print(f'{v} +- {s}')
    f.write(str(f'\n{v} +- {s}'))
    f.close()
 
plt.show()
#dosevalues = dosevalues*s_rate/v #picosieverts/s

"""
# plt.show()
plt.savefig('figlogdoseplot.png')
plt.show()
# plt.close()
# plt.clf()
"""


# plt.clf()