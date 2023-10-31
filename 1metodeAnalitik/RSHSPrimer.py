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
brp=20/2/50/1000 #Batas Radiasi Pekerja
brm=1/2/50/1000 #Batas Radiasi Masyarakat 1mSv*setengah/(50 minggu/tahun)


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
    arrwb.append("%.5f"%b)
    n=-log10(b)
    arrwn.append("%.5f"%n)
    #return n*TVL #return TVL1+(n-1)TVLe
    sh=TVL1+(TVLe*(n-1))
    arrwsh.append("%.5f"%sh)
    shhvl=sh+2*HVL
    arrwshvl.append("%.5f"%shhvl)
    print("==================================================================")
    print("$$B_{pri}=\\frac{",P," \\times",dsad,"^{2}}{",W,"\\times",U,"\\times",T,"} =",b,"$$")
    print("$$n=-log(",b,")=",n,"$$")
    print ("$$t_{barrier}=(",TVL1,"+(",n,"-1)\\times",TVLe,"=",sh,"$$")
    return sh


def InstDR(P,dsad):
    b=(P/40/1000)*(dsad**2)/DR #Dibagi 1000 karena dirubah dari mSv ke Sv
    arrib.append(b)
    n=-log10(b)
    arrin.append("%.5f"%n)
    #return n*TVL 
    sh =TVL1+(TVLe*(n-1)) 
    arrish.append("%.5f"%sh)
    print("==================================================================")
    print("$$B_{IDR}=\\frac {",P,"(",dsad,"^{2})}{",DR,"}=",b,"$$") #tinggal dihapus jarak \ dan f jadi langsung latex, formatting issues
    print("$$n=-log(",b,")=",n,"$$")
    print ("$$t_{barrier}=(",TVL1,"+(",n,"-1)\\times",TVLe,"=",sh,"$$")
    return sh

def primer(P,dsad,T):
    WeekDR(P,dsad,T)
    InstDR(P,dsad)

primer(brp,8.04,1)
primer(brp,8.04,1)

array=[]
array.append(arrdsad)
array.append(arrwb)
array.append(arrwn)
array.append(arrwsh)
array.append(arrwshvl)
array.append(arrib)
array.append(arrin)
array.append(arrish)

nparray=np.array(array)
obarray=np.array(nparray,dtype=object)
tarray=obarray.T
trarray=np.transpose(obarray)
print("Data type:", trarray.dtype)
print(tabulate(trarray,tablefmt="grid"))