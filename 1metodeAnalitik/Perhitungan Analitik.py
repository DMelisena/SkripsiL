import math
from math import *
from tabulate import tabulate
import numpy as np

writePrimer=open("Analitik.txt","w")

def WeekDR( P , dsad , T ): #W dan U dah ada, dsad ini di ncrp dpri, jarak dari xray target ke titik perlindungan, kok rasanya beda ama dsad yang kuitung ya?
    b=(P * dsad **2 ) / (W *U *T )
    n=-log10(b)
    sh=TVL1+(TVLe*(n-1))
    shhvl=sh+2*HVL
    writePrimer.write("==================================================================")
    writePrimer.write("$$B_{pri}=\\frac{",P," \\times",dsad,"^{2}}{",W,"\\times",U,"\\times",T,"} =",b,"$$")
    writePrimer.write("$$n=-log(",b,")=",n,"$$")
    writePrimer.write("$$t_{barrier}=(",TVL1,"+(",n,"-1)\\times",TVLe,"=",sh,"$$")
    print("==================================================================")
    print("$$B_{pri}=\\frac{",P," \\times",dsad,"^{2}}{",W,"\\times",U,"\\times",T,"} =",b,"$$")
    print("$$n=-log(",b,")=",n,"$$")
    print ("$$t_{barrier}=(",TVL1,"+(",n,"-1)\\times",TVLe,"=",sh,"$$")
    return sh


def InstDR(P,dsad):
    b=(P/40/1000)*(dsad**2)/DR #Dibagi 1000 karena dirubah dari mSv ke Sv
    n=-log10(b)
    #return n*TVL 
    sh =TVL1+(TVLe*(n-1)) 
    writePrimer.write("==================================================================")
    writePrimer.write("$$B_{IDR}=\\frac {",P,"(",dsad,"^{2})}{",DR,"}=",b,"$$") #tinggal dihapus jarak \ dan f jadi langsung latex, formatting issues
    writePrimer.write("$$n=-log(",b,")=",n,"$$")
    writePrimer.write("$$t_{barrier}=(",TVL1,"+(",n,"-1)\\times",TVLe,"=",sh,"$$")
    print("==================================================================")
    print("$$B_{IDR}=\\frac {",P,"(",dsad,"^{2})}{",DR,"}=",b,"$$") #tinggal dihapus jarak \ dan f jadi langsung latex, formatting issues
    print("$$n=-log(",b,")=",n,"$$")
    print ("$$t_{barrier}=(",TVL1,"+(",n,"-1)\\times",TVLe,"=",sh,"$$")
    return sh

def primer(P,dsad,T):
    WeekDR(P,dsad,T)
    InstDR(P,dsad)

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

primer(brp,8.04,1)
primer(brp,8.04,1)
