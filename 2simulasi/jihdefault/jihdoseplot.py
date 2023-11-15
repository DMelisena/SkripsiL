import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.11.h5')
meshtally = sp.tallies[1]
dosevalues = meshtally.get_values()

dosevalues.shape = (100,100)

fig, ax = plt.subplots()
cs = ax.imshow(dosevalues, cmap='coolwarm', norm=LogNorm()) # type: ignore
cb = plt.colorbar(cs)
ax.set_title('Power density (kW/cm$^3$)') #type: ignore
# plt.axis('off')
# plt.show()
plt.savefig('figlogdoseplot.png')
plt.show()
# plt.close()
# plt.clf()
