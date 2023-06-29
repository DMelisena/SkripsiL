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

TVL1= 0.410 #m
TVLe= 0.370 #m
TVL = 0.305 #m
HVL=TVL*log10(2)
print("HVL = ",HVL)

#Scatter Fraction sudut x pada energi 10MV
x30, y30 = 30, 0.00318
x45, y45 = 45, 0.00135
x60, y60 = 60, 0.000746 #60 derajat
x90, y90 = 90, 0.000381 #90 derajat

#========Mencari Fungsi ax+b========
#Data berdasarkan sudut dan scatter fraction pada energi 10MV

# cari slope 60 90
slope = (y90 - y60) / (x90 - x60) ; print("slope = ",slope)
slope2 = (y45 - y30) / (x45 - x30) ; print("slope = ",slope)
# cari intercept
intercept = y60 - slope * x60 ; print("intercept = ",intercept)
intercept2 = y30 - slope2 * x30 ; print("intercept = ",intercept)
# Karena nilai slopenya dah ketemu, degree tinggal dikaliin slope + intercept
print(f"Fungsi y = {slope}x +{intercept}")
print(f"Fungsi y2 = {slope2}x +{intercept2}")



#print("Nilai a atau scatter fraction dari dsec = 3.15",atandeg(3.15,1)*slope+intercept)
def a(dsec):
    degree = atandeg(dsec)
    #return slope * degree + intercept
    if 60 <= degree <= 90:
        return slope * degree + intercept
    elif 30 <= degree <= 45:
        return slope2 * degree + intercept2
    else:
        return 0

def atanrad(dsec): #Fungsi didalam atandeg, dipisahin biar gampang dibaca aja
    return atan(dsec/dsca) #nyari nilai pi
def atandeg(dsec): # Fungsi yang dipakek, terus scatter disudutnya di interpolasiin dari table b.4 antara 60 dan 90
    return degrees(atanrad(dsec)) #nyari derajat dari nilai pi


print(f"Nilai scatter fraction(a) pada dsec 3.15 = {a(3.15)}")

def scatter(Nama,P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    print(f"\nPada dinding {Nama} dengan dsec = {dsec}")
    al= atandeg(dsec) #nilai scatternya cukup dari dsec, karena dsca (Pasien ke sumber) pasti 1
    print(f"Scatter Fraction (a) {Nama} =", al)
    #print("alpha = 0.0005317")
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    print(f"Bscatter= {P} ( {dsca} **2)*( {dsec} **2)*400)/( {al} * {W} * {T} * {F} )= {B} ")
    #B=(P*(dsca**2)*(dsec**2)*400)/(0.0005317*700000*T*F)
    n=-log10(B)
    print (f"n dari Bpri = {n}\nKetebalan dinding beton = {n*TVL}")

    return n*TVL


def bscatter(P,dsec,T): 
    al= a(dsec) 
    print("alpha =", al)
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    return B

def nscatter(P,dsec,T):
    al= a(dsec)
    print("alpha =", al)
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    n=-log10(B)
    return n


#print("P=0.2,dsec = 3.15, T= 1",scatter(0.2,3.15,1)+HVL,"mm")

def leakage(P,Dl,T):
    B=(P*(Dl**2))/(0.001*W*T)
    
    n=-log10(B)
    print(f"leakage=({P}*({Dl}**2))/(0.001*{W}*{T})={n*TVL}")
    return n*TVL

def c(a1,b1): #pythagoras c kemudian diubah dari mm ke m
    a=a1/1000
    b=b1/1000
    return (sqrt(a*a+b*b))


#masih dalam mm, c nya diubah jadi bikin mm jadi m aja
dsecbl = c(1550+765+3240,1900+1850)
dsecb  = (1280+1900+1850)/1000
dsecbd = c(1550+765+3240,1900+1850)
dsecte = c(1550+765+3240, 1900+2500+125+1850)
dsect1 = (1900+2500+125)/1000
dsect2 = (1900+2500+125+1850+810)/1000
dsectl = c(1550+765+3240, 1900+2500+125)


head = ["Dinding","dsec","Scatter\nDegree","Scatter","Leakage"]
mydata = [
    ["BL",dsecbl,atandeg(dsecbl),scatter("BL",0.2 ,dsecbl,1  )+HVL,   leakage (0.2 ,dsecbl,1  )],
    ["B" ,dsecb, atandeg(dsecb) ,scatter("B",0.01,dsecb ,0.2 )+HVL,   leakage (0.01,dsecb ,0.2)+HVL],
    ["BD",dsecbd,atandeg(dsecbd),scatter("BD",0.2 ,dsecbd,1  )+HVL,   leakage (0.2 ,dsecbd,1  )+HVL],
    ["Te",dsecte,atandeg(dsecte),scatter("Te",0.2 ,dsecte,1  )+HVL,   leakage (0.2 ,dsecte,1  )+HVL],
    ["T1",dsect1,atandeg(dsect1),scatter("T1",0.2 ,dsect1,1  )+HVL,   leakage (0.2 ,dsect1,1  )+HVL],
    ["T2",dsect2,atandeg(dsect2),scatter("T2",0.2 ,dsect2,1  )+HVL,   leakage (0.2 ,dsect2,1  )],
    ["TL",dsect1,atandeg(dsect1),scatter("TL",0.2 ,dsectl,1  )+HVL,   leakage (0.2 ,dsectl,1  )],
        ]

print(tabulate(mydata, headers=head,tablefmt="grid"))


head = ["Dinding","dsec","Scatter\nDegree","Scatter","Leakage"]
mydata = [
    ["BL",dsecbl,atandeg(dsecbl),scatter("BL",0.2 ,dsecbl,1  )+HVL,   leakage (0.2 ,dsecbl,1  )],
    ["B" ,dsecb, atandeg(dsecb) ,scatter("B",0.01,dsecb ,0.2 )+HVL,   leakage (0.01,dsecb ,0.2)+HVL],
    ["BD",dsecbd,atandeg(dsecbd),scatter("BD",0.2 ,dsecbd,1  )+HVL,   leakage (0.2 ,dsecbd,1  )+HVL],
    ["Te",dsecte,atandeg(dsecte),scatter("Te",0.2 ,dsecte,1  )+HVL,   leakage (0.2 ,dsecte,1  )+HVL],
    ["T1",dsect1,atandeg(dsect1),scatter("T1",0.2 ,dsect1,1  )+HVL,   leakage (0.2 ,dsect1,1  )+HVL],
    ["T2",dsect2,atandeg(dsect2),scatter("T2",0.2 ,dsect2,1  )+HVL,   leakage (0.2 ,dsect2,1  )],
    ["TL",dsect1,atandeg(dsect1),scatter("TL",0.2 ,dsectl,1  )+HVL,   leakage (0.2 ,dsectl,1  )],
        ]

print(tabulate(mydata, headers=head,tablefmt="grid"))