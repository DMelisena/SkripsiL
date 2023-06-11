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

TVL1= 410 #mm
TVLe= 370 #mm
TVL = 305 #mm
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

#Scatter Fraction sudut x pada energi 10MV
x1, y1 = 60, 0.000746 #60 derajat
x2, y2 = 90, 0.000381 #90 derajat

#========Mencari Fungsi ax+b========
#Data berdasarkan sudut dan scatter fraction pada energi 10MV
# cari slope
slope = (y2 - y1) / (x2 - x1)
# cari intercept
intercept = y1 - slope *x1

#fungsi ax+b
print(f"Fungsi y = {slope}x +{intercept}")

print("Nilai a dari dsec 3.15",atandeg(3.15,1)*slope+intercept)
def a(dsec):
    degree = atandeg(dsec,dsca)
    return slope*degree+intercept

print(f"Nilai scatter fraction(a) pada dsec 3.15 = {a(3.15)}")

def scatter(P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    al= a(dsec)
    print("alpha =", al)
    #print("alpha = 0.0005317")
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    #B=(P*(dsca**2)*(dsec**2)*400)/(0.0005317*700000*T*F)
    n=-log10(B)
    return n*TVL

print("P=0.2,dsec = 3.15, T= 1",scatter(0.2,3.15,1)+HVL,"mm")
