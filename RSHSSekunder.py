import math
from math import *
from tabulate import tabulate
#========Beban Kerja
pasienperhari=70
gyperpasien=4
hariperminggu=5

W=hariperminggu*gyperpasien*pasienperhari*1000
print("W = ",W)
dsca=1 #jarak sumber ke pasien 1 meter
F=pi*((41/2)**2) #Kenapa 41? luas lapangan radiasi 41cm2, bukannya harusnya meter?

TVL1= 41 #cm
TVLe= 37 #cm
TVL = 38.9 #cm
HVL=TVL*log10(2)
print("HVL = ",HVL)

def atanrad(dsec,dsca):
    return atan(dsec/dsca) 
    #atandeg = atan(atanrad)
    #return atanrad,atandeg
def atandeg(dsec,dsca):
    return degrees(atanrad(dsec,dsca))
#print("atan =",atanrad(3.15,1)) #Mengecek nilai atan
#print("Degree = ",atandeg(3.15,1)) #mengecek sudut yang dihasilkan berdasarkan nilai atan yang sebelumnya ditemukan

def scatter(P,dsec,a,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    B=(P*dsca**2*dsec**2*400)/(a*W*T*F)
    n=-log10(B)
    return n*TVL

