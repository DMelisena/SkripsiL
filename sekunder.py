import math
from math import *
from tabulate import tabulate
#========Beban Kerja
pasienperhari=70
gyperpasien=2
hariperminggu=5

#======== Variabel Asumsi Konstan
W=hariperminggu*gyperpasien*pasienperhari*1000
dsca=1
F=pi*((41/2)**2) #Kenapa 41? luas lapangan radiasi 41cm2, bukannya harusnya meter?

TVL=305
print("TVL = ",TVL)
HVL=TVL*log10(2)
print("HVL = ",HVL)
#=============Scatter=================

def scatter(P,dsec,a,T):
    B=(P*dsca**2*dsec**2*400)/(a*W*T*F)
    n=-log10(B)
    return n*TVL

print("Nilai Barrier",scatter(0.2,3.15,0.0005317,1))
print("Maka nilai barrier+HVL=",scatter(0.2,3.15,0.0005317,1)+HVL)


#(P,dsec,a,T)
#H=0.2,3.15,0.0005317,1
#G=0.01,4.8,0.0006028,0.025
#E=0.2,6.75,0.0006435,1
#I'=0.01,4.35,0.0005885,0.2
#F'=0.2,4.05,0.000577,1

#-=============LEAKAGE==============
def leakage(P,Dl,T):
    B=(P*(Dl**2))/(0.001*W*T)
    n=-log10(B)
    return n*TVL

def bleakcheck(P,Dl,T):
    return (P*(Dl**2))/(0.001*W*T)
def nleakcheck(P,Dl,T):
    B=(P*(Dl**2))/(0.001*W*T)
    return -log10(B)
print("B leakage nilai G = ",bleakcheck(0.01,4.8,0.025))

print("Nilai Leakage=", leakage(0.2,3.15,1))
#print("Nilai Leakage+HVL=", leakage(0.2,3.15,1)+HVL) #Ternyata leakage gaperlu ditambah HVL
#FORMULA INI SALAH KARENA FIRST IMPACT TVL AMA SETELAH2NYA GA DIBEDAIN
#HARUSNYA FIRST IMPACT (1HVL PERTAMA) 41cm, terus sisanya 37cm berdasarkan tabel


head = ["Dinding", "Scatter","Leakage"]
mydata = [
    ["H",scatter(0.2,3.15,0.0005317,1)+HVL,
     leakage(0.2,3.15,1)],
    ["G",scatter(0.01,4.8,0.0006028,0.025)+HVL,
     leakage(0.01,4.8,0.025)+HVL],
    ["E",scatter(0.2,6.75,0.0006435,1)+
     HVL,leakage(0.2,6.75,1)+HVL],
    ["I'",scatter(0.01,4.35,0.0005885,0.2)+
     HVL,leakage(0.01,4.35,0.2)+HVL],
    ["F'",scatter(0.2,4.05,0.000577,1)+
     HVL,leakage(0.2,4.05,1)+HVL]
        ]

print(tabulate(mydata, headers=head,tablefmt="grid"))
#H=0.2,3.15,1
#G=0.01,4.5,0.025
#E=0.2,6.75,1
#I'=0.01,4.35,0.2
#F'=0.2,3.075,1

#(P,Dl,T)