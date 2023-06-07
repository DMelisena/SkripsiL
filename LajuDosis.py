import math
from math import *
from tabulate import tabulate

x=3500
TVL=389
W=700000
U=0.33
def B(x):
    return 10**(-x/TVL) #Sepertinya tidak ada nilai
def P(B,T,dsad):
    return (B*W*U*T)/(dsad**2)

print(B(3500))
print ("P(F) = ",P(B(3500),1,4.15),"mSv/week")
print ("P(F) = ",(P(B(3500),1,4.15))/40000,"Sv/hour")
print ("P(I) = ",P(B(3500),0.2,4.75),"mSv/week")
print ("P(I) = ",P(B(3500),0.2,4.75)/40000,"Sv/hour")

#dsad=
TVL2 = 305
def Ps(x,T,dsec):
    return ((10**(-x/TVL2)*W*T)/(1000*dsec*dsec))
x1=[1200,1550,1200,1550,1200]
T1=[1,0.0025,1,0.2,1]
dsec1=[3.15,4.8,6.75,4.35,4.05]
psek=[]
i=0
#while len(result)<len(x1):
#    psek.append(Ps(i))
#   i+=1
#for i in range()
print("Ps = ",Ps(1200,1,3.15),"mSv/week")
print("Ps = ",Ps(1550,0.025,4.8),"mSv/week")
print("Ps = ",Ps(1200,1,6.75),"mSv/week")
print("Ps = ",Ps(1550,0.2,4.35),"mSv/week")
print("Ps = ",Ps(1200,1,4.05),"mSv/week")

print("Ps = ",Ps(1200,1,3.15)/40000,"Sv/hour")
print("Ps = ",Ps(1550,0.025,4.8)/40000,"Sv/hour")
print("Ps = ",Ps(1200,1,6.75)/40000,"Sv/hour")
print("Ps = ",Ps(1550,0.2,4.35)/40000,"Sv/hour")
print("Ps = ",Ps(1200,1,4.05)/40000,"Sv/hour")