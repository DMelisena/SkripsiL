import numpy as np
import math
from math import *
from tabulate import tabulate
import pandas as pd
##############################  Parameter Awal  ##################################
#========Beban Kerja==============================================================
pasienperhari=70
gyperpasien=4
hariperminggu=5
W=hariperminggu*gyperpasien*pasienperhari #1.400 Sv
print("\nPerhitungan Nilai - Nilai standar keamanan menurt SRS dan NCRP ",W)
print("W = ",W)
#============================================================

dsca=1 
#jarak sumber ke pasien 1 meter
#F=pi*((41/2)**2) #Kenapa 41? luas lapangan radiasi 41cm2, bukannya harusnya meter?
F=40*40

#========  Pembatas Dosis  ========================================================

#Dikali setengah agar aman menurut ncrp
brp=20/2/50/1000 #batas radiasi pekerja,   (20mSv/tahun)*setengah/50 minggu/tahun
brm=1/2/50/1000   #batas radiasi masyarakat,(1mSv/tahun*setengah/50 minggu/tahun
print("BRP = ",brp, "     brm = ",brm)

TVL1= 0.410 #m
TVLe= 0.370 #m
TVL = 0.305 #m
HVL=TVL*log10(2)
print("HVL = ",HVL)
#####################################################################################

############################# Sudut Radiasi #########################################
#Scatter Fraction sudut x pada energi 10MV  =========================================
x30, y30 = 30, 0.00318 #Data masing-masing derajat
x45, y45 = 45, 0.00135
x60, y60 = 60, 0.000746 
x90, y90 = 90, 0.000381 #Data berdasarkan sudut dan scatter fraction pada energi 10MV
#========  Mencari Fungsi ax+b   ====================================
# cari slope 60-90 dan 30-45
print (f"\n===========  Scatter Fractions  ==============")
slope = (y90 - y60) / (x90 - x60) ; print("slope 6090 = ",slope)
intercept = y60 - slope * x60 ; print("intercept 6090 = ",intercept)
slope2 = (y45 - y30) / (x45 - x30) ; print("slope 3045 = ",slope2)
intercept2 = y30 - slope2 * x30 ; print("intercept 3045 = ",intercept2)
# Karena nilai slopenya dah ketemu, degree tinggal dikaliin slope + intercept
print(f"Fungsi y = {slope}x +{intercept}")
print(f"Fungsi y2 = {slope2}x +{intercept2}")
print (f"==============================================\n")
#======= Pembuatan Fungsi ===========================================================
def atandeg(dsec): # Fungsi yang dipakek, terus scatter disudutnya di interpolasiin dari table b.4 antara 60 dan 90
    return degrees(atan(dsec/dsca)) #nyari derajat dari nilai pi
def a(dsec):
    degree = atandeg(dsec)
    #return slope * degree + intercept
    if 60 <= degree <= 90:
        return slope * degree + intercept
    elif 30 <= degree <= 45:
        return slope2 * degree + intercept2
    else:
        return 0
#####################################################################################

##################################  Perhitungan  ####################################
#================ Pembuatan Array =======================
arrname= ["Na\nme"]
arrdsec= ["dsec"]
arrdeg=["Scatter\nDegree"]
arra=["Scatter\nValue"]
arrb=["Bps"]
arrn=["n"]
arrsh=["Scatter\nShielding"]
arrdl=["dLeak"] #Harusnya dari sumber
arrbleak=["B leak"]
arrnbleak=["n leak"]
arrshleak=["Leakage\nShield"]

#================ 
with open("SekunderLatex.txt", "w") as file:
        file.write("==========Formula Latex========\n")

#================ Fungsi Scatter =========================
def scatter(Nama,P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    #print(f"\nPada dinding {Nama} dengan dsec = {dsec}")
    
    arrdsec.append("%.5f"%dsec)
    deg= atandeg(dsec) #nilai scatternya cukup dari dsec, karena dsca (Pasien ke sumber) pasti 1
    arrdeg.append("%.5f"%deg)
    #print(f"Sudut yang tercipta : {deg}")
    arrname.append(Nama)
    al = a(dsec)
    arra.append("%.5f"%al)
    #print(f"Scatter Fraction(a) dinding {Nama} =", al)
    #print("alpha = 0.0005317")
    B=(P*(dsca**2)*(dsec**2)*400)/(al*W*T*F)
    arrb.append("%.5f"%B)
    #print(f"Bscatter= {P} ( {dsca} **2)*( {dsec} **2)*400)/( {al} * {W} * {T} * {F} )= {B} ")
    #B=(P*(dsca**2)*(dsec**2)*400)/(0.0005317*700000*T*F)
    n=-log10(B)
    arrn.append("%.5f"%n)
    sh=(n*TVL)+HVL
    arrsh.append("%.6f"%sh)

    #print (f"n dari Bpri = {n}\nKetebalan dinding beton = {n*TVL}")
    print (f"================   {Nama}    =====================")
    print (f"===============  Scatter  ====================")
    print (f"dsec ={dsec} \ndeg = {deg} a = {al}\nB = {B}\nn ={n}\nShield = {n*TVL}")
    print ("$$B_{ps}=\ frac",P,"{",al,W, T,"}",dsca,"}^{2}",dsec,"^{2}\ frac{400}{",F,"} $$")
    # Expression
    bps = r"$$B_{ps}=\frac{" + str(P) + "}{" + str("%.5f"%al) + r"\times" + str(W) + r"\times" + str(T) + r"}\times{" + str(dsca) + r"}^{2}\times" + str("%.5f"%dsec) + r"^{2}\times\frac{400}{" + str(F) + "}="+ str(B) + "$$"
    nps = r"$$n=-log("+ str(B) + r")=" + str(n)+ r"$$"
    shps = r"$$Barrier ="+ str(n) +r"\times"+ str(TVL)+ r"+" +str(HVL) + "=" + str(sh) + r"$$"
    # Open a text file in write mode
    with open("SekunderLatex.txt", "a") as file:
        file.write(f"Nama={Nama} P={P} dsec={dsec}; T= {T}\n")
        file.write(bps+"\n first")
        file.write(nps+"\n second")
        file.write(shps+"\n\n third")
    return sh

#================ Fungsi Leakage ==========================
def leakage(P,Dl,T):
    arrdl.append("%.5f"%Dl)
    B=(P*(Dl**2))/(0.001*W*T)
    arrbleak.append("%.5f"%B)
    n=-log10(B)
    arrnbleak.append("%.5f"%n)
    print (f"===============  Leakage  ====================")
    print(f"B = {B} n = {n} \nShield = {n*TVL}\n")
    #print(f"leakage=({P}*({Dl}**2))/(0.001*{W}*{T})={n*TVL}")
    print("$$B_{L}=\ frac{",P,Dl,"^{2}}{10^{-3}",W,T,"}$$")
    #formulas.append("$$B_{L}=\ frac{",P,Dl,"^{2}}{10^{-3}",W,T,"}$$")
    shleak=n*TVL
    arrshleak.append("%.5f"%shleak)
    bl = r"$$B_{L}=\frac{" + str(P) + r"\times" + str("%.5f"%Dl) + r"^{2}}{10^{-3}\times"+ str(W)+ r"\times" +str(T)+"}="+str(B)+"$$"
    nl = r"$$n=-log("+ str(B) + r")=" + str(n)+ r"$$"
    shl= r"$$Barrier ="+ str(n) +r"\times"+ str(TVL) + "=" + str(shleak) + r"$$"
    # Open a text file in write mode
    with open("SekunderLatex.txt", "a") as file:
        file.write(bl+"\n")
        file.write(nl+"\n")
        file.write(shl+"\n")
    return shleak


#============= Fungsi Pythagoras ==============
def c(a1,b1): #pythagoras c kemudian diubah dari mm ke m
    a=a1/1000
    b=b1/1000
    return (sqrt(a*a+b*b))
#masih dalam mm, c nya diubah jadi bikin mm jadi m aja
#Perubahan orientasi karena salah, utara harusnya barat
#============= Statement Value Pythagoras =====
dsecbd = c(1550+765+3240,1900+1850)
dsecs = (1280+1900+1850)/1000
dsecte = c(1550+765+3240,1900+1850)
dsectl = c(1550+765+3240, 1900+2500+125+1850)
dsecu1 = (1900+2500+125)/1000
dsecu2 = (1900+2500+125+1850+810)/1000
dsecbl = c(1550+765+3240, 1900+2500+125)

dlbd = c(c(1550+765+3240,1900+1850),1)*1000
dls = c((1280+1900+1850)/1000,1)*1000
dlte = c(c(1550+765+3240,1900+1850),1)*1000
dltl = c(c(1550+765+3240, 1900+2500+125+1850),1)*1000
dlu1 = c((1900+2500+125)/1000,1)*1000
dlu2 = c((1900+2500+125+1850+810)/1000,1)*1000
dlbl = c(c(1550+765+3240, 1900+2500+125),1)*1000

#======= Deklarasi Fungsi Utama ========
def sekunder(Nama,P,dsec,Dl,T):
    scatter(Nama,P,dsec,T)
    leakage(P,Dl,T)
    return

# Penjalanan Fungsi
sekunder("BD",brp ,dsecbd,dlbd,1  )
sekunder("S" ,brm,dsecs ,dls ,0.2)
sekunder("Te",brp ,dsecte,dlte,1  )
sekunder("TL",brp ,dsectl,dltl,1  )
sekunder("U1",brp ,dsecu1,dlu1,1  )
sekunder("U2",brp ,dsecu2,dlu2,1  )
sekunder("BL",brp ,dsecbl,dlbl,1  )
print("BD P=",brp,"P = " ,dsecbd, "Dl= ",dlbd,"T = ",1  )
print("S  P=",brm,"P = " ,dsecs , "Dl= ",dls ,"T = ",0.2)
print("Te P=",brp,"P = " ,dsecte, "Dl= ",dlte,"T = ",1  )
print("TL P=",brp,"P = " ,dsectl, "Dl= ",dltl,"T = ",1  )
print("U1 P=",brp,"P = " ,dsecu1, "Dl= ",dlu1,"T = ",1  )
print("U2 P=",brp,"P = " ,dsecu2, "Dl= ",dlu2,"T = ",1  )
print("BL P=",brp,"P = " ,dsecbl, "Dl= ",dlbl,"T = ",1  )


#=============== Pembuatan Tabel===========================
array=[]
array.append(arrname)
array.append(arrdsec)
array.append(arrdeg)
array.append(arra)
array.append(arrb)
array.append(arrn)
array.append(arrsh)
array.append(arrdl)
array.append(arrbleak)
array.append(arrnbleak)
array.append(arrshleak)

#print(array)
nparray=np.array(array)
obarray=np.array(nparray,dtype=object)
tarray=obarray.T
trarray=np.transpose(obarray)
print("Data type:", trarray.dtype)
print(tabulate(trarray,tablefmt="grid"))
#================ Pencetakan Tabel pada .txt ================
with open("SekunderLatex.txt", "a") as file:
    file.write(tabulate(trarray,tablefmt="grid"))

#================ Pencetakan Tabel pada .csv ================
df = pd.DataFrame(trarray)

# Export the DataFrame to a CSV file
df.to_csv('hasilSekunder.csv', index=False, header=False)
