import math
from math import *
from tabulate import tabulate

#========Beban Kerja
pasienperhari=70
gyperpasien=2
hariperminggu=5

#======== Variabel Asumsi Konstan
W=hariperminggu*gyperpasien*pasienperhari
U=0.33

###############################################################
####### 1 Dosis Ekivalen Total scatter dan leakage ############
###############################################################

################ 1.a Hamburan Radiasi dari Dinding #############

#a0= #Koefisien refleksi pada hamburan pertama 
#az= #refleksi pada refleksi kedua dari permukaan Az
#A0= #Field size maksimum yang terproyeksi pada dinding A0(m2)
Az= 2.350*4.27#luas cross section labirin (m2)
dH= 3.24+0.1#Jarak isocenter ke dinding A0 [(dpp+1) pada gambar 3.6]
dr=1.9+4.625 #Jarak dari pusat sinar pada refleksi pertama ke garis tengah labirin
dz=7.105-2.350 #Panjang labirin ke pintu (m)

HS=(W*U*a0*A0*az*Az)/((dH*dr*dz)**2) 
printf("HS = {HS}")

################ 1.b Hamburan Pasien ###########################

A1=1.85*4.27 #Luas dinding yang dapat dilihat dari pintu masuk ruangan (m2)
dsec = sqrt((3.24+0.765)**2+((3.8/2)+6.360-1.735)**2)+#jarak dari isocenter ke garis tengah labirin di pintu (m)
dzz = 8.605-1.500#jarak garis tengah labirin ke pintu

a = #fraksi hamburan terhadap paparan pada target radiasi
F = #luas lapangan radiasi (cm2
a1= #Koefisien refleksi dinding beton untuk hamburan pasien pada sudut 45° untuk monoenergetic photon 0,5 MeV
dsca= 1   #Jarak pasien dan sumber
HPS = (W*U*a*(F/400)*a1*A1)/((dsca*dsec*dzz)**2)
print("HPS = ",HPS)

################ 1.c Kebocoran head dan dihamburkan oleh dinding

HLS = (0.001*W*U*a1*A1)/((dsec*dzz)**2)
print ("HLS = ",HLS(0.0051))

################ 1.d Transmisi Radiasi bocor melalui dinding labirin

HLT = (0.001*W*U*B)/(dl**2)

x3=1550+765+3240-2505
y3=1900+2500+125+925
r3=sqrt(x3**2+y3**2)
dl = r3#jarak dari sumber ke pintu masuk (m)

########################################
Htot = 2.64*(HLT+HLS+HPS+(0.28*(HS)))###
print("Htot = ",Htot)###################
########################################

##########################################################################
####### 2 Dosis Ekivalen total dari Neutron Capture Gamma Rays ###########
##########################################################################

qn=4.6*100000000000 #Kekuatan sumber neutron yang dipancarkan dari kepala, NCRP 151 = 4.6E11
#akselerator dan diserap isocenter per Gy sinar-X
B = 1#aktor transmisi

x=2.505+8.605-1.500-2.350
x1=x-(1.550+0.765+3.24)
y1=1.900+2.500
y2=y1+0.125+0.925
x2= y2*(x1/y1)
r2=sqrt(x2**2+y2**2)
d1=r2



dl = #jarak dari sumber ke pintu masuk (m)
HLT = (0.001*W*U*B)/(dl**2)

print("HLT = ",HLT(0.0000595,4.8))

#dsec= #jarak isocenter ke garis tengah labirin di pintu
#dzz = #jarak dari isocenter ke garis tengah labirin di pintu


#b  = #Faktor transmisi untuk neutron yang menembus head shielding, asumsi head sebagai timbal b=1
#d1 = #Jarak dari isocenter ke garis tengah labirin di pintu dengan arah sinar mengenai pinggir labirin


##########DAH SAMPE SINI HAHAHA, NYARI LUAS AJA TINGGALAN
####MESKIPUN NILAI a NYA BELOM TAU YA HEHE
#sr = #Total luas permukaan dalam bunker
#ya = 

#K  = #Nilai berdasarkan pengukuran : 6.9 * 10e-16 Sv m2 (NCRP report no. 151)
#hy = #Dosis ekivalen hasil tangkapan gamma oleh Neutron (Sv/Gy)
#d2 = #Jarak dari tengah labirin ke pintu (m)

#hcg= #Perhitungan LAju Dosis Neutron Capture Gamma Rays
#s0/s1 = #Rasio luas penampang pintu masuk labirin dalam dengan luas penampang sepanjang labirin
#TVD= Tenth Value Dose
#hnd = #laju dosis neutron di setiap beban kerja

#hn=W*hnd1 #Perhitungan laju dosis neutron

#hw=