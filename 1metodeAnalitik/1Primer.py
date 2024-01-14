import math
from math import *
from tabulate import tabulate
import numpy as np
import pandas as pd

#========Beban Kerja
pasienperhari=70
gyperpasien=4
hariperminggu=5

#======== Variabel Asumsi Konstan
W1=hariperminggu*gyperpasien*pasienperhari #dalam Sv
print("W = ",W1)
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



def rounde(unrounded):
    roundede="{:.4e}".format(unrounded)
    return roundede

def WeekDR( W , P , dsad , T ): #W dan U dah ada, dsad ini di ncrp dpri, jarak dari xray target ke titik perlindungan, kok rasanya beda ama dsad yang kuitung ya?
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
    print("$$B_{pri}=\\frac{",P," \\times",dsad,"^{2}}{",W,"\\times",U,"\\times",T,"} =",rounde(b),"$$")
    print("$$n=-log(",rounde(b),")=",rounde(n),"$$")
    print ("$$t_{barrier}=(",TVL1,"+(",rounde(n),"-1)\\times",TVLe,"=",rounde(sh),"$$")
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
    print("$$B_{IDR}=\\frac {",P,"(",dsad,"^{2})}{",DR,"}=",rounde(b),"$$") #tinggal dihapus jarak \ dan f jadi langsung latex, formatting issues
    print("$$n=-log(",rounde(b),")=",rounde(n),"$$")
    print ("$$t_{barrier}=(",TVL1,"+(",rounde(n),"-1)\\times",TVLe,"=",rounde(sh),"$$")
    return sh
def primer(W, P,dsad,T):
    WeekDR(W, P,dsad,T)
    InstDR(P,dsad)

###### Nilai Input ###################
######################################
primer(1400,brp,7.32,1)  ##################
primer(1400,brp,7.32,1)  ##################
primer(3488,brp,7.62,0.5)
######################################



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

darrw=["W \nGy/week"] #dose array Workload
darrdsad=["dsad \nmeter"] #dose array length from center to detection point
darrsl=['Shield Length \n(meter)'] #shield length
darrtvl=['TVL \nmeter'] #Tenth Value Length
darrwhol=["Dose on length \nuSv/h"] #dose array workload per hour
darrwh=['W hourly \n uSv/h']
darrdoseop=['Dose After Shield\nuSv/h']
darrn=['n']
darrdoseop30=['on 30 cm']
darrdoseop50=['on 50 cm']
darrdoseop100=['on 100 cm']
darrdoseop200=['on 200 cm']
#sl=shieldLength
def lajudosis(W,dsad,sl,TVL):
    darrw.append(W)
    darrdsad.append(dsad)
    darrsl.append(sl)
    darrtvl.append(TVL)
    wh=W*1000000/40
    darrwh.append(wh)
    whol=wh/(dsad**2)
    darrwhol.append(whol)
    n1=sl/TVL
    darrn.append("%.5f"%n1)
    doseop=wh*(10**-(sl/TVL))
    darrdoseop.append(doseop)
    doseop30=doseop*((dsad**2)/((dsad+0.3)**2))
    darrdoseop30.append(doseop30)
    doseop50=doseop*((dsad**2)/((dsad+0.5)**2))
    darrdoseop50.append(doseop50)
    doseop100=doseop*((dsad**2)/((dsad+1)**2))
    darrdoseop100.append(doseop100)
    doseop200=doseop*((dsad**2)/((dsad+2)**2))
    darrdoseop200.append(doseop200)


darray=[]
darray.append(darrw)
darray.append(darrwh)
darray.append(darrdsad)
darray.append(darrwhol)
darray.append(darrsl)
darray.append(darrtvl)
darray.append(darrn)
darray.append(darrdoseop)
darray.append(darrdoseop30)
darray.append(darrdoseop50)
darray.append(darrdoseop100)
darray.append(darrdoseop200)

lajudosis(3488,7.32,3.08,0.389)
lajudosis(1744,4.78,2.42,0.389)

npdarray=np.array(darray)
obdarray=np.array(npdarray,dtype=object)
tdarray=obdarray.T
trdarray=np.transpose(obdarray)
print("Data type:", trdarray.dtype)
print(tabulate(trdarray,tablefmt="grid"))

#================ Pencetakan Tabel pada .csv ================
shieldcsv= pd.DataFrame(trarray)
doseprimarycsv=pd.DataFrame(trdarray)
# Export the DataFrame to a CSV file
shieldcsv.to_csv('hasilPrimer.csv', index=False, header=False)
doseprimarycsv.to_csv('dosisPrimer.csv',index=False,header=False)
P1=0.0002*(10**4.7)
print(f'ekspektasi dosis = {P1}')