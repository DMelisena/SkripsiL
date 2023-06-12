import math
from math import *
from tabulate import tabulate

W=700
U=0.33

###############################################################
####### 1 Dosis Ekivalen Total scatter dan leakage ############
###############################################################
dsec=6.75
dzz=6.45

#HS  =(W*U*a*A0*az*Az ) / (dH*dr*dz)^2
#HPS =(W*U*a*(F/400)*(a*A1))/(dsca*dsec*dzz)^2
#HLS =(E-3*W*U*a*A1)/(dsec*dzz)^2
#HLT =(E-3*W*U*B)/(dl)^2

################ 1.a Hamburan Radiasi dari Dinding #############
def HS(a0,az,A0,AZ,dH,dr,dz):
    return (W*U*a0*A0*az*AZ)/((dH*dr*dz)**2)

print("HS=",HS(0.0021,0.008,1.9044,12.069,2.65,4.2,4.35))

################ 1.b Hamburan Pasien ###########################
A1  =6.75
def HPS(a,F,a1,dsca):
    return (W*U*a*(F/400)*a1*A1)/((dsca*dsec*dzz)**2)
print("HPS = ",HPS(0.000381,1600,0.022,1))

################ 1.c Kebocoran head dan dihamburkan oleh dinding
def HLS(a1):
    return (0.001*W*U*a1*A1)/((dsec*dzz)**2)
print ("HLS = ",HLS(0.0051))
################ 1.d Transmisi Radiasi bocor melalui dinding labirin
def HLT(B,dl):
    return (0.001*W*U*B)/(dl**2)

print("HLT = ",HLT(0.0000595,4.8))

#################################################################

Htot = 2.64*(HLT(0.0000595,4.8)
        +HLS(0.0051)
        +HPS(0.000381,1600,0.022,1)
        +(0.28*(HS(0.0021,0.008,1.9044,12.069,2.65,4.2,4.35))))
print("Htot",Htot)

##########################################################################
####### 2 Dosis Ekivalen total dari Neutron Capture Gamma Rays ###########
##########################################################################
qn=4.6*100000000000
b=1
d1=4.56
sr=267.831

################ 2.a Fluens Neutron ##########################
ya=((b*qn)/(4*pi*d1*d1))+((5.4*b*qn)/(2*pi*sr))+((1.3*qn)/(2*pi*sr))
print("ya =",ya)

################ 2.b gamma capure di tiap beban kerja ########
K=6.9*10**(-16)
hy=K*ya*(10**(-5.85/3))
print("hy =",hy)
d2=5.85
################ 2.c Laju dosis neutron capture gamma rays####

hcg=W*hy
print ("hcg =", hcg)

##########################################################################
###### 3 Dosis Ekivalen Neutron Pada Pintu################################
##########################################################################
s1=5.364
s0=12.069
TVD= 2.06*sqrt(s1)
print("TVD = ", TVD)

################ 3.a Laju Dosis neutron di setiap beban kerja #

hnd0=2.4*(10**-15)*ya*sqrt(s0/s1)*(1.64*10**(-d2/1.9)+(10**-(d2/3.455)))
#Atas itu formulanya skripsi daftar pustaka andika, tapi ditulis di skripsinya salah tapi hasilnya bener
hnd1=2.4*10**-15*ya*sqrt(s0/s1)*(1.64*10**(-d2/1.9)+(10**-(d2/TVD)))
print("hnd = ",hnd1)

################ 3.b Laju Dosis neutron #######################
hn=W*hnd1
print("hn=",hn)

##########################################################################
#=============== Dosis EKivalen Total Pada Area Pintu ====================
##########################################################################
hw=Htot+hcg+hn
print("hw = ",hw)

##################### Perhitunggan Ketebalan BPE #########################
P=5*2
hn1=hn*10**6 #Dirubah dari Sv jadi uSv karena nilai P nya uSv
nbpe=log10(hn1/(P/2))
print("nbpe = ",nbpe)
TVLbpe = 45
xbpe=nbpe*TVLbpe
print ("xbpe",xbpe)

##################### Perhitunggan Ketebalan Pb ##########################
P=5*2
Hy=Htot+hcg
Hy1=Hy*10**6 #Karena P nya uSv, jadi ini dari Sv dirubah jadi uSv jg
print("Hy = ",Hy1)
nhy=log10(Hy1/(P/2))
print("nhy = ",nhy)
tvlbpe=6
xpb=nhy*tvlbpe
print("xpb = ",xpb)

