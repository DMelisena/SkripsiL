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

a0= 0.0021#Koefisien refleksi pada hamburan pertama, berdasarkan NCRP 151 tabel 8a yaitu 0° incidence
az= 0.0080#refleksi pada refleksi kedua dari permukaan Az
FA0= 0.4*0.4
#Dengan jarak pasien ke primer sejarak 3.24 meter, dan luas field radiasi senilai 0.4*0.4
#maka nilai 3.24 dikalikan jarak kuadrat. Ini adalah 
#A0=FA0*((3.24**2)) #Metode ini salah #Field size maksimum yang terproyeksi pada dinding A0(m2)
A0= (0.4*(1+3.24))**2
print("Nilai A0 =",A0)
Az= 2.350*4.27#luas cross section labirin (m2)
dH= 3.24+1#Jarak isocenter ke dinding A0 [(dpp+1) pada gambar 3.6]
dr=1.9+4.625 #Jarak dari pusat sinar pada refleksi pertama ke garis tengah labirin
dz=7.105-2.350 #Panjang labirin ke pintu (m)

HS=(W*U*a0*A0*az*Az)/((dH*dr*dz)**2) 
print("$$H_{S}=\\frac{",W,"\\times",U,"\\times", a0,"\\times","%.5f"%A0,"\\times",az,"\\times",Az,"}{(",dH,"\\times",dr,"\\times","%.5f"%dz,")^{2}}=",HS,"$$")
#print("HS = ",HS)

################ 1.b Hamburan Pasien ###########################

A1=1.85*4.27 #Luas dinding yang dapat dilihat dari pintu masuk ruangan (m2)
dsec = sqrt((3.24+0.765)**2+((3.8/2)+6.360-1.735)**2)#jarak dari isocenter ke garis tengah labirin di pintu (m)
dzz = 8.605-1.500#jarak garis tengah labirin ke pintu


#Scatter Fraction sudut x pada energi 10MV
x1, y1 = 60, 0.000746 #60 derajat
x2, y2 = 90, 0.000381 #90 derajat

#========Mencari Fungsi ax+b========
#Data berdasarkan sudut dan scatter fraction pada energi 10MV

dsca= 1   #Jarak pasien dan sumber
# cari slope
slope = (y2 - y1) / (x2 - x1)
# cari intercept
intercept = y1 - slope *x1
#fungsi ax+b
#print(f"Fungsi y = {slope}x +{intercept}")
#print("Nilai a dari dsec 3.15",atandeg(3.15,1)*slope+intercept)
atanrad = atan(dsec/dsca)
degree = degrees(atanrad)

a = slope*degree+intercept #fraksi hamburan terhadap paparan pada target radiasi

print("Nilai scatter fraction(a) pada dsec 3.15 =", a)

def scatter(P,dsec,T): # (dsec = jarak pasien ke titik pengukuran ; a= Fraksi hambur atau serapan dosis berkas primer yang terhambur dari pasien)
    al= a(dsec)
    print("alpha =", al)

F = FA0#luas lapangan radiasi (cm2
a1= 0.022#Koefisien refleksi dinding beton untuk hamburan pasien pada sudut 45° untuk monoenergetic photon 0,5 MeV

HPS = (a*W*U*(F/400)*a1*A1)/((dsca*dsec*dzz)**2)
print(r"$$H_{ps}=\frac{",a,r"\times",W,r"\times",U,r"\times","(",F,"/400)",r"\times",a1,r"\times",A1,"}{(",dsca,r"\times",dsec,r"\times",dzz,")^{2}}=",HPS,"$$")
#print("HPS = ",HPS)

################ 1.c Kebocoran head dan dihamburkan oleh dinding

HLS = (0.001*W*U*a1*A1)/((dsec*dzz)**2)
print(r"$$H_{LS}=\frac{",0.001,r"\times",W,r"\times",U,r"\times",a1,r"\times",A1,"}{(",dsec,r"\times",dzz,")^{2}}=",HLS,"$$")
#print("HLS = ",HLS)

################ 1.d Transmisi Radiasi bocor melalui dinding labirin
B=0.0000595

x3=1550+765+3240-2505
y3=1900+2500+125+925
r3=sqrt(x3**2+y3**2)
dl = r3#jarak dari sumber ke pintu masuk (m)

HLT = (0.001*W*U*B)/(dl**2)
print(r"$$H_{LT}=\frac{",0.001,r"\times",W,r"\times",U,r"\times",B,r"}{",dl,"^{2}}=",HLT,"$$")



########################################
Htot = 2.64*(HLT+HLS+HPS+(0.28*(HS)))###
#print("Htot = ",Htot)###################
print(r"$$H_{tot}=2.64\times((",HS,r"\times","0.28)+",HLS,"+",HPS,"+",HLT,")=",Htot,"$$")

##########################################################################
####### 2 Dosis Ekivalen total dari Neutron Capture Gamma Rays ###########
##########################################################################

qn=4.6e11 #Kekuatan sumber neutron yang dipancarkan dari kepala, NCRP 151 = 4.6E11
#akselerator dan diserap isocenter per Gy sinar-X
B = 1#aktor transmisi
#B  = #Faktor transmisi untuk neutron yang menembus head shielding, asumsi head sebagai timbal b=1

x=2.505+8.605-1.500-2.350
x1=x-(1.550+0.765+3.24)
y1=1.900+2.500
y2=y1+0.125+0.925
x2= y2*(x1/y1)
r2=sqrt(x2**2+y2**2)
d1=r2
#d1 = #Jarak dari isocenter ke garis tengah labirin di pintu dengan arah sinar mengenai pinggir labirin

######################################################################
LD1=1850*(8605-1500)
LD2=125*2350
LD3=2500*(6480+765+765)
LD4=3800*6480
LD5=1850*(6480+765+765)
LDatas=(LD1+LD2+LD3+LD4+LD5)*2
LDS=4270*(8605-1500+1850+125+2500+765+3800+765+1850+765+1850+6480
          +765+1850+765+3800+765+2500+(2505+8605-1500-2350-1550)+125+11110-1500-2509+1850)

sr=LDatas+LDS #Total luas permukaan dalam bunker, MINTOL SIAPA KEK, UDAH KEITUNG DI KERTAS

######################################################################


################ 2.a Fluens Neutron ##########################
b=1
ya=((b*qn)/(4*pi*d1*d1))+((5.4*b*qn)/(2*pi*sr))+((1.3*qn)/(2*pi*sr))
print(r"$$\varphi_{A}=\frac{",b,r"\times",qn,r"}{4 \times \pi",d1,r"^{2}} \frac{5.4",b,r"\times",qn,"}{2\pi",r"\times",sr,r"} \frac{1.3 \times",qn,"}{2\pi",sr,"}=",ya,"$$")
#print("ya =",ya)

################ 2.b gamma capure di tiap beban kerja ########

TVD = 3 #(Tenth-Value Distance) jarak yang dibutuhkan untuk mereduksi
#photon fluence menjadi 1/10 kali semula (bernilai 3 untuk 10 MV)
d2 = 8.605-1.500-(2.350/2)#Jarak dari tengah labirin ke pintu (m)
K=6.9*10**(-16)#Nilai berdasarkan pengukuran : 6.9 * 10e-16 Sv m2 (NCRP report no. 151)

hy=K*ya*(10**(-d2/TVD)) #Dosis ekivalen hasil tangkapan gamma oleh Neutron (Sv/Gy)
print(r"$$h_{\varphi}=",K,r"\times",ya,r"\times(10^{-(\frac{",d2,"}{",TVD,"})}=",hy,"$$")
#print("hy =",hy)

################ 2.c Laju dosis neutron capture gamma rays####

hcg=W*hy #hcg= #Perhitungan LAju Dosis Neutron Capture Gamma Rays
print("$$H_{cg}=",W,r"\times",hy,"=",hcg,"$$")
#print ("hcg =", hcg)

##########################################################################
###### 3 Dosis Ekivalen Neutron Pada Pintu################################
##########################################################################
s0s1 = 1850/2350 #Rasio luas penampang pintu masuk labirin dalam dengan luas penampang sepanjang labirin
S0=1850
S1=2350
s1=2.350*4.270
#TVD= Tenth Value Dose
TVD= 2.06*sqrt(s1) #ini maksudnya udaranya kan ya? atau tvd dari timbal?

################ 3.a Laju Dosis neutron di setiap beban kerja #

#s0/s1 = #Rasio luas penampang pintu masuk labirin dalam dengan luas penampang sepanjang labirin
#TVD= Tenth Value Dose
hnd1=2.4*10e-15*ya*sqrt(S0/S1)*(1.64*10**(-d2/1.9)+(10**-(d2/TVD)))#laju dosis neutron di setiap beban kerja
print("hnd = ",hnd1)
print(r"$$H_{n,D}=2.4 \times 10^{-15}",ya,r"\sqrt{\frac{",S0,"}{",S1,r"}}\begin{bmatrix}1.64 \times 10^{-\frac{",-d2,r"}{1.9}}+10^{-(\frac{",d2,"}{",TVD,"})}\end{bmatrix}=",hnd1,"$$")

################ 3.b Laju Dosis neutron #######################
hn=W*hnd1 #Perhitungan laju dosis neutron
print("$$H_{n}=",W,r"\times",hnd1,"=",hn,"$$")
print("hn=",hn)

##########################################################################
#=============== Dosis EKivalen Total Pada Area Pintu ====================
##########################################################################
hw=Htot+hcg+hn
print("$$H_{w}=",Htot,r"+",hcg,r"+",hn,"=",hw,"$$")
print("hw = ",hw)



##################### Perhitunggan Ketebalan BPE #########################
P=5 #10/2
hn1=hn*10e6#Dirubah dari Sv jadi uSv karena nilai P nya uSv
nbpe0=hn1/P
nbpe=log10(nbpe0)
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
