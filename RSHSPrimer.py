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

#========Instantenous Dose Rate=====
DR=2200*60/100 #2200MU/min *jam/menit /100Gy/(MU=cGy)
def WeekDR(br,dsadf,T) #
