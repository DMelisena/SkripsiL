import math
from math import *

#print(W)


#========Pembatas Dosis
brp=20/2/50#b atas radiasi pekerja, (20mSv/tahun)*setengah/50 minggu/tahun
brm=1/2/50#batas radiasi masyarakat, 1mSv/tahun*setengah/50 minggu/tahun

#========Beban Kerja
pasienperhari=70
gyperpasien=2
hariperminggu=5

#======== Variabel Asumsi Konstan
W=hariperminggu*gyperpasien*pasienperhari*1000
U=0.33
Tf=1

#======== Variabel TVL
TVL=389
HVL=TVL*log10(2)
print("HVL=",HVL)

#======== Variabel tambahan untuk instantenous Dose Rate
DR=2200*60/100#2200MU/min adalah dose rate maksimum pada LINAC. (1MU=1cGy)

def WeekDR(br,dsadf):
    b=(br*dsadf**2)/(W*U*Tf)
    n=-log10(b)
    return n*TVL

def InstDR(br,dsadf):
    b=(br/40/1000)*(dsadf**2)/DR #Dibagi 1000 karenna dirubah dari mSv ke Sv
    n=-log10(b)
    return n*TVL

print ("======Pada Dinding F========")
print ("Barrier primer =", WeekDR(brp,4.15)) 
print ("Barrier primer+2HVL =", WeekDR(brp,4.15)+(2*HVL)) #WeekDRF
print ("Barrier Primer InstDR =", InstDR(brp,4.15)) #InstDRF
print ("Barrier primer InstDR+2HVL =", InstDR(brp,4.15)+(2*HVL)) #WeekDRF

print ("======Pada Dinding H========")
print ("Barrier primer =", WeekDR(brm,4.75)) 
print ("Barrier primer+2HVL =", WeekDR(brm,4.75)+(2*HVL)) #WeekDRF
print ("Barrier Primer InstDR =", InstDR(brm,4.75)) #InstDRF
print ("Barrier primer InstDR+2HVL =", InstDR(brm,4.75)+(2*HVL)) #WeekDRF

