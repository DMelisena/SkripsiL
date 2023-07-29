import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.5.h5')
meshtally = sp.tallies[1]
dosevalues = meshtally.get_values()
dosestddev = meshtally.std_dev 

dosevalues.shape = dosevalues.shape[0]
dosestddev.shape = dosestddev.shape[0]


#print(dosevalues)
s_rate=4.87805e7
#v=(2000/x)*(2000/y)*300
vcell=10.8*50*200

dosevalues = dosevalues * s_rate / vcell *1000*3600
dosestddev = dosestddev * s_rate / vcell

for v,s in zip(dosevalues,dosestddev):
    print(f'{v} +- {s}')
    
#dosevalues = dosevalues*s_rate/v #picosieverts/s

"""
x=3#harus sama dengan resolusi pada file utama
y=5
dosevalues.shape = (x,y)
v=(2000/x)*(2000/y)*300
dosevalues = dosevalues*s_rate/v #picosieverts/s
dose=dosevalues*1000*3600 #microsieverts/hour
fig, ax = plt.subplots()
cs = ax.imshow(dose, cmap='coolwarm', norm=LogNorm()) # type: ignore
cb = plt.colorbar(cs)
ax.set_title('Power density (kW/cm$^3$)') #type: ignore
# plt.axis('off')
# plt.show()
plt.savefig('figlogdoseplot.png')
plt.show()
# plt.close()
# plt.clf()
"""
