import math
from math import *
from tabulate import tabulate

W=700
U=0.33
dsec=6.75
dzz=6.45

#HS  =(W*U*a*A0*az*Az ) / (dH*dr*dz)^2
#HPS =(W*U*a*(F/400)*(a*A1))/(dsca*dsec*dzz)^2
#HLS =(E-3*W*U*a*A1)/(dsec*dzz)^2
#HLT =(E-3*W*U*B)/(dl)^2

def HS(a0,az,A0,AZ,dH,dr,dz):
    return (W*U*a0*A0*az*AZ)/((dH*dr*dz)**2)

print(HS(0.0021,0.008,1.9044,12.069,2.65,4.2,4.35))

##############--HPS--#####
A1  =6.75
dsec=6.75
dzz =6.45
def HPS(a,F,a1,dsca):
    return (W*U*a*(F/400)*a1*A1)/((dsca*dsec*dzz)**2)
print("HPS = ",HPS(0.000381,1600,0.022,1))

def HLS(a1):
    return (0.001*W*U*a1*A1)/((dsec*dzz)**2)
print ("HLS = ",HLS(0.0051))

def HLT(B,dl):
    return (0.001*W*U*B)/(dl**2)

print("HLT = ",HLT(0.0000595,4.8))