import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.5.h5')
meshtally = sp.tallies[1]


x=500#harus sama dengan resolusi pada file utama
y=500
s_rate=4.87805e7
v=(2000/x)*(2000/y)*300 #volume of room dose distribution
dosevalues=meshtally.get_values()
dosevalues.shape=(x,y)
dosevalues = dosevalues*s_rate/v #picosieverts/s
dose=dosevalues*1000*3600 #microsieverts/hour
fig, ax = plt.subplots()
cs = ax.imshow(dose, cmap='coolwarm', norm=LogNorm()) # type: ignore
cb = plt.colorbar(cs)
ax.set_title('Power density (kW/cm$^3$)') #type: ignore
plt.savefig('RoomDoseDistribution.png')
# plt.axis('off')


celltally = sp.tallies[2]
celldosevalues = celltally.get_values()
celldosestddev = celltally.std_dev 

celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

vcell=10.8*50*200

celldosevalues = celldosevalues * s_rate / vcell *1000*3600
celldosestddev = celldosestddev * s_rate / vcell

for v,s in zip(celldosevalues,celldosestddev):
    print(f'{v} +- {s}')
    

phantally = sp.tallies[3]
phandosevalues = phantally.get_values()
phandosestddev = phantally.std_dev 

phandosevalues.shape = phandosevalues.shape[0]
phandosestddev.shape = phandosestddev.shape[0]

vcell=10*40*40

phandosevalues = phandosevalues * s_rate / vcell *1000*3600
phandosestddev = phandosestddev * s_rate / vcell

for v,s in zip(phandosevalues,phandosestddev):
    print(f'{v} +- {s}')

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