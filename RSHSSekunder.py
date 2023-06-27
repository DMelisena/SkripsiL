import math
from math import *
from tabulate import tabulate
#========Beban Kerja
pasienperhari=70
gyperpasien=4
hariperminggu=5

W=hariperminggu*gyperpasien*pasienperhari*1000 #1.400.000 mSv
print("W = ",W)
dsca=1 #jarak sumber ke pasien 1 meter
#F=pi*((41/2)**2) #Kenapa 41? luas lapangan radiasi 41cm2, bukannya harusnya meter?
F=100
#========Pembatas Dosis======
#Dikali setengah agar aman menurut ncrp
brp=20/2/50  #batas radiasi pekerja,   (20mSv/tahun)*setengah/50 minggu/tahun
brm=1/2/50   #batas radiasi masyarakat,(1mSv/tahun*setengah/50 minggu/tahun
print("BRP = ",brp, "     brm = ",brm)

TVL1= 410 #mm
TVLe= 370 #mm
TVL = 305 #mm
HVL=TVL*log10(2)
print("HVL = ",HVL)

def atanrad(dsec,dsca): #Fungsi didalam atandeg, dipisahin biar gampang dibaca aja
    return atan(dsec/dsca) 
    #atandeg = atan(atanrad)
    #return atanrad,atandeg
def atandeg(dsec,dsca): # Fungsi yang dipakek, terus scatter disudutnya di interpolasiin dari table b.4 antara 60 dan 90
    return degrees(atanrad(dsec,dsca))

print("atanrad 2705,2025 = ",atanrad(2705,2025))
print("atandeg 2705,2025 = ",atandeg(2705,2025))
#print("atan =",atanrad(3.15,1)) #Mengecek nilai atan
#print("Degree = ",atandeg(3.15,1)) #mengecek sudut yang dihasilkan berdasarkan nilai atan yang sebelumnya ditemukan

#Scatter Fraction sudut x pada energi 10MV
x1, y1 = 60, 0.000746 #60 derajat
x2, y2 = 90, 0.000381 #90 derajat

#========Mencari Fungsi ax+b========
#Data berdasarkan sudut dan scatter fraction pada energi 10MV
# cari slope
slope = (y2 - y1) / (x2 - x1) ; print("slope = ",slope)
# cari intercept
intercept = y1 - slope *x1 ; print("intercept = ",intercept)
#fungsi ax+b
print(f"Fungsi y = {slope}x +{intercept}")


########## Karena nilai slopenya dah ketemu, degree tinggal dikaliin slope + intercept
print("Nilai a dari dsec 3.15",atandeg(3.15,1)*slope+intercept)
def a(dsec):
    degree = atandeg(dsec,dsca)
    return slope*degree+intercept
def adegree(dsec):
    degree = atandeg(dsec,dsca)
    return degree

print(f"Nilai scatter fraction(a) pada dsec 3.15 = {a(3.15)}")

def scatter(P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    al= a(dsec) #nilai scatternya cukup dari dsec, karena dsca (Pasien ke sumber) pasti 1
    print("alpha =", al)
    #print("alpha = 0.0005317")
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    #B=(P*(dsca**2)*(dsec**2)*400)/(0.0005317*700000*T*F)
    n=-log10(B)
    return n*TVL
def bscatter(P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    al= a(dsec) #nilai scatternya cukup dari dsec, karena dsca (Pasien ke sumber) pasti 1
    print("alpha =", al)
    #print("alpha = 0.0005317")
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    return B
def nscatter(P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    al= a(dsec) #nilai scatternya cukup dari dsec, karena dsca (Pasien ke sumber) pasti 1
    print("alpha =", al)
    #print("alpha = 0.0005317")
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    #B=(P*(dsca**2)*(dsec**2)*400)/(0.0005317*700000*T*F)
    n=-log10(B)
    return n

#print("P=0.2,dsec = 3.15, T= 1",scatter(0.2,3.15,1)+HVL,"mm")

def leakage(P,Dl,T):
    B=(P*(Dl**2))/(0.001*W*T)
    n=-log10(B)
    return n*TVL

def c(a,b): #pythagoras c kemudian diubah dari mm ke m
    return (sqrt(a*a+b*b))/10000

dsecbl = c(1550+765+3240,1900+1850)
dsecb = (1280+1900+1850)/1000
dsecbd = c(1550+765+3240,1900+1850)
dsecte = c(1550+765+3240, 1900+2500+125+1850)
dsect1 = 1900+2500+125
dsect2 = 1900+2500+125+1850+810
dsectl = c(1550+765+3240, 1900+2500+125)

head = ["Dinding", "adegree","Scatter","Leakage"]
mydata = [
    ["BL",adegree(dsecbl),scatter(0.2 ,dsecbl,1  )+HVL,    leakage (0.2 ,dsecbl,1  )],
    ["B" ,adegree(dsecb), scatter(0.01,dsecb ,0.2)+HVL,    leakage (0.01,dsecb ,0.2)+HVL],
    ["BD",adegree(dsecbd),scatter(0.2 ,dsecbd,1  )+HVL,    leakage (0.2 ,dsecbd,1  )+HVL],
    ["Te",adegree(dsecte),scatter(0.2 ,dsecte,1  )+HVL,    leakage (0.2 ,dsecte,1  )+HVL],
    ["T1",adegree(dsect1),scatter(0.2 ,dsect1,1  )+HVL,    leakage (0.2 ,dsect1,1  )+HVL],
    ["T2",adegree(dsect2),scatter(0.2 ,dsect2,1  )+HVL,    leakage (0.2 ,dsect2,1  )],
    ["TL",adegree(dsect1),scatter(0.2 ,dsectl,1  )+HVL,    leakage (0.2 ,dsectl,1  )],
        ]

print(tabulate(mydata, headers=head,tablefmt="grid"))