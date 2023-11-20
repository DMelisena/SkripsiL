import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.100.h5')

f=open("output.txt","w")
f.write(str(sp.tallies))
f.close()

meshtally = sp.tallies[1]
print(sp.tallies[1])
print(sp.tallies[2])
#print(sp.tallies[3])

######## Pembuatan Visualisasi Distribusi Dosis #################

x=500#harus sama dengan resolusi pada file utama
y=500

s_rate=3.293648066139751e+17 #src/s
v=(2000/x)*(2000/y)*1000 #volume of room dose distribution
dosevalues=meshtally.get_values() #Nilai perpixel dari grid 500x500
dosevalues.shape=(x,y)
#pSvcm3/src*(src/s)/cm3=pSv/s
dosevalues = dosevalues*s_rate/v #pSv/s = (pSv*cm3/src) *src/s /cm3
dose=(dosevalues/1_000_000)*3600 #pSv/s -> uSv/hour

fig, ax = plt.subplots()
cs = ax.imshow(dose, cmap='coolwarm', norm=LogNorm()) # type: ignore
cb = plt.colorbar(cs)
ax.set_title('Distribusi Dosis Ruangan (uSv/hour)') #type: ignore
plt.savefig('RoomDoseDistribution.png',dpi=900 )
plt.axis('off')

#################################################################

celltally = sp.tallies[2]
celldosevalues = celltally.get_values() #pSvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 
print(celltally)
celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

vcell=10.8*50*200 #cm3

dose_psvs=celldosevalues * s_rate / vcell
usvh_dose=(dose_psvs/1e6)*3600

stddev_psvs=celldosestddev*s_rate/vcell
usvh_stddev=(stddev_psvs/1e6)*3600

dose=usvh_dose
dosestddev=usvh_stddev

#dose = celldosevalues *s_rate/ vcell #pSvcm3/src * (src/s) / cm3= pSv/s
#dose=(dose/1e6)*3600 #pSv/s -> uSv/h 3.6e9
#dosestddev = (celldosestddev * s_rate / vcell) *(1e6/3600) 
#k=2457897.1324533457
#dose=k*celldosevalues*600/vcell
#dosestddev = (k*celldosevalues*600/vcell) *(1e6/3600) 


print(dose)
for v,s in zip(dose,dosestddev):
    f=open("output.txt","a")
    print(f'{v:.7e} +- {s:.7e}uSv/h')
    f.write(str(f'\n{v} +- {s} uSv/h'))
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