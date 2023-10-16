import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.5.h5')

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
plt.savefig('RoomDoseDistribution.png',dpi=1200 )
# plt.axis('off')


celltally = sp.tallies[2]
celldosevalues = celltally.get_values()
celldosestddev = celltally.std_dev 

celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

vcell=10.8*50*200

celldosevalues = celldosevalues * s_rate / vcell /1000000*3600
celldosestddev = celldosestddev * s_rate / vcell

for v,s in zip(celldosevalues,celldosestddev):
    f=open("output.txt","a")
    print(f'{v} +- {s}')
    f.write(str(f'\n{v} +- {s}'))
    f.close()
    

neuttally = sp.tallies[3]
neutdosevalues = neuttally.get_values()
neutdosestddev = neuttally.std_dev 

neutdosevalues.shape = neutdosevalues.shape[0]
neutdosestddev.shape = neutdosestddev.shape[0]

#phandosevalues = phandosevalues * s_rate / vcell /1000000*3600
neutdosestddev = neutdosestddev * s_rate / vcell

for v,s in zip(neutdosevalues,neutdosestddev):
    f=open("output.txt","a")
    print(f'{v} +- {s}')
    f.write(str(f'\n{v} +- {s}'))
    f.close()
"""
plt.show()
#dosevalues = dosevalues*s_rate/v #picosieverts/s

"""
# plt.show()
plt.savefig('figlogdoseplot.png')
plt.show()
# plt.close()
# plt.clf()
