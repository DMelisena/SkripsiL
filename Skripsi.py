import math
from math import *
pasienperhari=70
gyperpasien=2
hariperminggu=5
W=hariperminggu*gyperpasien*pasienperhari*1000
#print(W)

brp=20/2/50#b atas radiasi pekerja, (20mSv/tahun)*setengah/50 minggu/tahun
brm=1/2/50#batas radiasi masyarakat
#print(brp)
#print(brm)
#dsadf=4.15
U=0.33
Tf=1
TVL=389
HVL=TVL*log10(2)
print("HVL=",HVL)
DR=2200*60/100#2200MU/min adalah dose rate maksimum pada LINAC. (1MU=1cGy)
def WeekDR(br,dsadf):
    b=(br*dsadf**2)/(W*U*Tf)
    n=-log(b,10)
    return n*389

def InstDR(br,dsadf):
    return (br/40/1000)*(dsadf**2)/DR #Dibagi 1000 karenna dirubah dari mSv ke Sv
print ("Barrier primer =", WeekDR(brp,4.15)) 
print ("Barrier primer+2HVL =", WeekDR(brp,4.15)+(2*HVL)) #WeekDRF
print (InstDR(brp,4.15)) #InstDRF
print (WeekDR(brm,4.75)) #WeekDRF
print (InstDR(brm,4.75)) #InstDRF



