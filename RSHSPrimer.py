import math
from math import *
from tabulate import tabulate

#========Beban Kerja
pasienperhari=70
gyperpasien=4
hariperminggu=5

#======== Variabel Asumsi Konstan
W=hariperminggu*gyperpasien*pasienperhari*1000
print("W = ",W)
U=0.33 #karena dipakai 8 jam/24 jam??
#Tf=1

#==========Pembatas Dosis=====
brp=20/2/50 #Batas Radiasi Pekerja
brm=1/2/50 #Batas Radiasi Masyarakat 1mSv*setengah/(50 minggu/tahun)

#==========Variabel TVL======
TVL=389
HVL=TVL*log10(2)
print("HVL =", HVL)

#========Instantenous Dose Rate=====
DR=2200*60/100 #2200MU/min *jam/menit /100Gy/(MU=cGy)
#Apakah MU pada linac itu maksimalnya juga 2200?
def WeekDR(P,dsad,T): #W dan U dah ada
    b=(P*dsad**2)/(W*U*T)
    n=-log10(b)
    return n*TVL

def InstDR(P,dsad):
    b=(P/40/1000)*(dsad**2)/DR #Dibagi 1000 karenna dirubah dari mSv ke Sv
    n=-log10(b)
    return n*TVL

data=[
     ["F",
      WeekDR(brp,7.32,1),
      WeekDR(brp,7.32,1)+(2*HVL),
      InstDR(brp,7.32),
      InstDR(brp,7.32)+(2*HVL)],
     ["I", 
      WeekDR(brp,7.32,1), 
      WeekDR(brp,7.32,1)+(2*HVL),
      InstDR(brp,7.32),
      InstDR(brp,7.32)+(2*HVL)]
        ]
#Nilai dsad 7.32 = 1 + 3.240 + 3.080

head=["Dinding", "WeekB", "WeekB+2HVL","InstB","InstB+2HVL"]
print(tabulate(data,headers=head,tablefmt="grid"))