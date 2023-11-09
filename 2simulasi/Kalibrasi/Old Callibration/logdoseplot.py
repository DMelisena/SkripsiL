import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.10000.h5')
meshtally = sp.tallies[1]
dosevalues = meshtally.get_values()
x=500 #harus sama dengan resolusi pada file utama
y=500
dosevalues.shape = (x,y)
s_rate=4.87805e7
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

