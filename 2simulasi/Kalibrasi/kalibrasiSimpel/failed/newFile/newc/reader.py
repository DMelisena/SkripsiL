import openmc
import matplotlib.pyplot as plt
import numpy as np

##

sp = openmc.StatePoint('statepoint.500.h5')
##

n = 1000
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
plt.plot(datax, datay)

# draw line at x_max
plt.axvline(x=x_max, color='r')
# write x_max value on plot
plt.title(f'x_max = {x_max}')

plt.show()
result = 4.394e-7
phandosevalues=result
vol=6*6*30/1000
axvcell=5*10*10#cm3
mu=1e11#600 MU/min = 10 cGy/s = 1e11 pSv/s 
s_rate=mu*axvcell/phandosevalues #src/s
print( "\n========== Pencarian Nilai S rate ============")
print("s_rate=mu*axvcell/phandosevalues #src/s")
print(f"={mu}*{axvcell}/{phandosevalues}={s_rate}\n")
factorMU = 60/1e10 # pSv/s -> MU/min
factoruSv = 3600/1e6 # pSv/s -> uSv/h

k=vol/result
print(k)
#ddet=k*phandosevalues*600/vcell
#600 MU/min