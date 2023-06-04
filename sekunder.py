import math
from math import *

#========Beban Kerja
pasienperhari=70
gyperpasien=2
hariperminggu=5

#======== Variabel Asumsi Konstan
W=hariperminggu*gyperpasien*pasienperhari*1000
dsca=1
F=pi*((41/2)**2)

TVL=305
HVL=TVL*log10(2)
def scatter(P,dsec,a,T):
    B=(P*dsca**2*dsec**2*400)/(a*W*T*F)
    n=-log10(B)
    return n*TVL
print("Nilai Barrier",scatter(0.2,3.15,0.0005317,1))
print("Maka nilai barrier+HVL=",scatter(0.2,3.15,0.0005317,1)+HVL)

def leakage(P,Dl,T):
    B=(P*Dl**2)/(0.001*W*T)
    n=-log10(B)
    return n*TVL

print("Nilai Leakage=", leakage(0.2,3.15,1))