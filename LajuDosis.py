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