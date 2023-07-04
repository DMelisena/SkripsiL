import math
from math import *
from tabulate import tabulate
import numpy as np

#========Beban Kerja
pasienperhari=70
gyperpasien=4
hariperminggu=5

#======== Variabel Asumsi Konstan
W=hariperminggu*gyperpasien*pasienperhari #dalam Sv
print("W = ",W)
U=0.33 #karena dipakai 8 jam/24 jam??
#Tf=1

#==========Pembatas Dosis=====
brp=20/2/50 #Batas Radiasi Pekerja
brm=1/2/50 #Batas Radiasi Masyarakat 1mSv*setengah/(50 minggu/tahun)


#==========Variabel TVL======
TVL=0.389
HVL=TVL*log10(2)
print("HVL =", HVL)
TVL1=0.410 ; TVLe=0.370 #mm
#========Instantenous Dose Rate=====
DR=2200*60/100 #2200MU/min *jam/menit /100Gy/(MU=cGy)
#Apakah MU pada linac itu maksimalnya juga 2200?

arrdsad=["d+SAD"]
arrwb=["Weekly B"]
arrwn=["Weekly n"]
arrwsh=["Weekly \nShield"]
arrwshvl=["+2HVL"]
arrib=["Inst B"]
arrin=["Inst n"]
arrish=["inst \nShield"]


def WeekDR( P , dsad , T ): #W dan U dah ada, dsad ini di ncrp dpri, jarak dari xray target ke titik perlindungan, kok rasanya beda ama dsad yang kuitung ya?
    arrdsad.append(dsad)
    b=(P * dsad **2 ) / (W *U *T )
    arrwb.append(b)
    n=-log10(b)
    arrwn.append(n)
    #return n*TVL #return TVL1+(n-1)TVLe
    sh=TVL1+(TVLe*(n-1))
    arrwsh.append(sh)
    arrwshvl.append(sh+2*HVL)
    return sh

def bWeekDR( P , dsad , T ): #W dan U dah ada, dsad ini di ncrp dpri, jarak dari xray target ke titik perlindungan, kok rasanya beda ama dsad yang kuitung ya?
    b=(P * dsad **2 ) / (W *U *T )

    #return n*TVL #return TVL1+(n-1)TVLe
    return b

def nWeekDR( P , dsad , T ): #W dan U dah ada, dsad ini di ncrp dpri, jarak dari xray target ke titik perlindungan, kok rasanya beda ama dsad yang kuitung ya?
    b=(P * dsad **2 ) / (W *U *T )
    n=-log10(b)

    #return n*TVL #return TVL1+(n-1)TVLe
    return n


def InstDR(P,dsad):
    b=(P/40/1000)*(dsad**2)/DR #Dibagi 1000 karena dirubah dari mSv ke Sv
    arrib.append(b)
    n=-log10(b)
    arrin.append(n)
    #return n*TVL 
    sh =TVL1+(TVLe*(n-1)) 
    arrish.append(sh)
    return sh

def bInstDR(P,dsad):
    b=(P/40/1000)*(dsad**2)/DR #Dibagi 1000 karena dirubah dari mSv ke Sv
    print("$$B_{IDR}=\ frac {",P,"(",dsad,"^{2})}{",DR,"}=",b,"$$") #tinggal dihapus jarak \ dan f jadi langsung latex
    return b 
def nInstDR(P,dsad):
    b=(P/40/1000)*(dsad**2)/DR #Dibagi 1000 karena dirubah dari mSv ke Sv
    n=-log10(b)
    #return n*TVL 
    return n

data=[
     ["B",
      bWeekDR(brp,8.04,1),
      nWeekDR(brp,8.04,1),
      WeekDR(brp,8.04,1),
      WeekDR(brp,8.04,1)+(2*HVL),
      bInstDR(brp,8.04),
      nInstDR(brp,8.04),
      InstDR(brp,8.04),
      InstDR(brp,8.04)+(2*HVL)],
     ["T", 
      bWeekDR(brp,8.04,1),
      nWeekDR(brp,8.04,1),
      WeekDR(brp,8.04,1),
      WeekDR(brp,8.04,1)+(2*HVL),
      bInstDR(brp,8.04),
      nInstDR(brp,8.04),
      InstDR(brp,8.04),
      InstDR(brp,8.04)+(2*HVL)],
        ]
#Nilai dsad 7.32 = 1 + 3.240 + 3.080

head=["Dinding", "Bpri","n","WeekB", "WeekB+2HVL","bInstB","nInstB","InstB","InstB+2HVL"]
print(tabulate(data,headers=head,tablefmt="grid"))


array=[]
array.append(arrdsad)
array.append(arrwb)
array.append(arrwn)
array.append(arrwsh)
array.append(arrwshvl)
array.append(arrib)
array.append(arrin)
array.append(arrish)

"""
array=np.array(array)
print("Data type:", array.dtype)
tarray=np.transpose(array)
print(tabulate(tarray,tablefmt="grid"))
"""
nparray=np.array(array)
obarray=np.array(nparray,dtype=object)
tarray=obarray.T
trarray=np.transpose(obarray)
print("Data type:", trarray.dtype)
print(tabulate(trarray,tablefmt="grid"))