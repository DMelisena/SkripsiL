import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

sp = openmc.StatePoint('./statepoint.10000.h5')

f=open("output.txt","w")
f.write(str(sp.tallies))
f.close()

meshtally = sp.tallies[1]
print(sp.tallies[1])
print(sp.tallies[2])
#print(sp.tallies[3])

"""
######## Hasil S_rate Simulasi ##################################

phantally = sp.tallies[3]
phandosevalues = phantally.get_values()#pSvcm3/src
phandosestddev = phantally.std_dev 

phandosevalues.shape = phandosevalues.shape[0]
phandosestddev.shape = phandosestddev.shape[0]

axvcell=5*10*10#cm3
mu=1e11#600 MU/min = 10 cGy/s = 1e11 pSv/s 
# Pencarian Faktor Konversi dengan 600 MU/m=1e11pSv/s, volume phantom (cm3) dan dosis simulasi (pSvcm3/src)
s_rate=mu*axvcell/phandosevalues #src/s
print( "\n========== Pencarian Nilai S rate ============")
print("s_rate=mu*axvcell/phandosevalues #src/s")
print(f"={mu}*{axvcell}/{phandosevalues}={s_rate}\n")
factorMU = 60/1e10 # pSv/s -> MU/min
factoruSv = 3600/1e6 # pSv/s -> uSv/h

print( "\n========== 600 MU/min sesuai S_rate? ============")
print(f"source rate *phantomdosevaluse/v cell axis= mu\n{s_rate}x{phandosevalues}/{axvcell}={mu}\n={phandosevalues*s_rate/axvcell} pSv/s")
print(f"={phandosevalues*s_rate/axvcell*60/1e10} MU\n")#pSv/sec*(src/s)/cm3
#phandosevalues = phandosevalues * s_rate / axvcell /1000000*3600 #

#################################################################
"""

######## Pembuatan Visualisasi Distribusi Dosis #################

x=500#harus sama dengan resolusi pada file utama
y=500
#s_rate=4.87805e7 #source rate ICRP 116
#s_rate=34.52580998
#dose=dosevalues*1000*3600 #microsieverts/hour

s_rate=3.293648066139751e+17
v=(2000/x)*(2000/y)*300 #volume of room dose distribution
dosevalues=meshtally.get_values() #Nilai perpixel dari grid 500x500
dosevalues.shape=(x,y)
#pSvcm3/src*(src/s)/cm3=pSv/s
s_rate=6.967475822858894e+18
dosevalues = dosevalues*s_rate/v #pSv/s
dose=(dosevalues/1_000_000)*3600 #pSv/s -> uSv/hour

fig, ax = plt.subplots()
cs = ax.imshow(dose, cmap='coolwarm', norm=LogNorm()) # type: ignore
cb = plt.colorbar(cs)
ax.set_title('Distribusi Dosis Ruangan (uSv/hour)') #type: ignore
plt.savefig('RoomDoseDistribution.png',dpi=900 )
plt.axis('off')

#################################################################

"""
phandosevalues *= factoruSv
phandosestddev *= factoruSv
for v,s in zip(phandosevalues,phandosestddev):
    f=open("output.txt","a")
    print(f'{v} +- {s}')
    f.write(str(f'\n{v} +- {s}'))
    f.close()
"""
celltally = sp.tallies[2]
celldosevalues = celltally.get_values() #pSvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 
print(celltally)
celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

vcell=10.8*50*200

#dose = celldosevalues *s_rate/ vcell #pSvcm3/src * (src/s) / cm3= pSv/s
#dose=(dose/1e6)*3600 #pSv/s -> uSv/h 3.6e9
#dosestddev = (celldosestddev * s_rate / vcell) *(1e6/3600) 
k=2457897.1324533457
dose=k*celldosevalues*600/vcell
dosestddev = (k*celldosevalues*600/vcell) *(1e6/3600) 


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