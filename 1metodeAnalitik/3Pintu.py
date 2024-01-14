import math
from math import *
from tabulate import tabulate

#========Beban Kerja
pasienperhari=70
gyperpasien=2
hariperminggu=5

#======== Variabel Asumsi Konstan
# W=hariperminggu*gyperpasien*pasienperhari
W=1744

U=0.33

txtwrite=open("Hasil3AnalitikPintu.txt","w")

def rounde(unrounded):
    roundede="{:.4e}".format(unrounded)
    return roundede

###############################################################
####### 1 Dosis Ekivalen Total scatter dan leakage ############
###############################################################

################ 1.a Hamburan Radiasi dari Dinding #############
a0= 0.0021#Koefisien refleksi pada hamburan pertama, berdasarkan NCRP 151 tabel 8a yaitu 0° incidence
az= 0.0080#refleksi pada refleksi kedua dari permukaan Az
FA0= 0.4*0.4
#Dengan jarak pasien ke primer sejarak 3.24 meter, dan luas field radiasi senilai 0.4*0.4
#maka nilai 3.24 dikalikan :jarak kuadrat. Ini adalah 
#A0=FA0*((3.24**2)) #Metode ini salah #Field size maksimum yang terproyeksi pada dinding A0(m2)
A0= (0.4*(1+3.24))**2
print("Nilai A0 =",A0)
Az= 2.350*4.27#luas cross section labirin (m2)
dH= 3.24+1#Jarak isocenter ke dinding A0 [(dpp+1) pada gambar 3.6]
dr=1.9+4.625 #Jarak dari pusat sinar pada refleksi pertama ke garis tengah labirin
dz=7.105-2.350 #Panjang labirin ke pintu (m)
##############################################################################################################################

HS=(W*U*a0*A0*az*Az)/((dH*dr*dz)**2) 
print("$$H_{S}=\\frac{",W,"\\cdot",U,"\\cdot", a0,"\\cdot","%.5f"%A0,"\\cdot",az,"\\cdot",Az,"}{(",dH,"\\cdot",dr,"\\cdot","%.5f"%dz,")^{2}}=",HS,"$$")
hsres = f"$$H_{{S}}=\\frac{{{W}\\cdot{U}\\cdot{a0}\\cdot{A0:.5f}\\cdot{az}\\cdot{Az}}}{{({dH}\\cdot{dr}\\cdot{dz:.5f})^{{2}}}}={HS}$$"
with open("Hasil3AnalitikPintu.txt","a") as file:
    file.write(hsres)

#print(hsres)
#txtwrite.write(hsres)
#print("HS = ",HS)

################ 1.b Hamburan Pasien ###########################
A1=1.85*4.27 #Luas dinding yang dapat dilihat dari pintu masuk ruangan (m2)
dsec = sqrt((3.24+0.765)**2+((3.8/2)+6.360-1.735)**2)#jarak dari isocenter ke garis tengah labirin di pintu (m)
print("$$d_{sec}= \sqrt {((3.24+0.765)^{2}+((3.8/2)+6.360-1.735)^{2})}$$")
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
##############################################################################################################################

HPS = (a*W*U*(F/400)*a1*A1)/((dsca*dsec*dzz)**2)
print(r"$$H_{ps}=\frac{",a,r"\cdot",W,r"\cdot",U,r"\cdot","(",F,"/400)",r"\cdot",a1,r"\cdot",A1,"}{(",dsca,r"\cdot",dsec,r"\cdot",dzz,")^{2}}=",HPS,"$$")
#print("HPS = ",HPS)

################ 1.c Kebocoran head dan dihamburkan oleh dinding

HLS = (0.001*W*U*a1*A1)/((dsec*dzz)**2)
print(r"$$H_{LS}=\frac{",0.001,r"\cdot",W,r"\cdot",U,r"\cdot",a1,r"\cdot",A1,"}{(",dsec,r"\cdot",dzz,")^{2}}=",HLS,"$$")
#print("HLS = ",HLS)

################ 1.d Transmisi Radiasi bocor melalui dinding labirin
B=0.0000595
x3=1550+765+3240-2505
y3=1900+2500+125+925
r3=sqrt(x3**2+y3**2)
dl = r3#jarak dari sumber ke pintu masuk (m)
###############################################################

HLT = (0.001*W*U*B)/(dl**2)
print(r"$$H_{LT}=\frac{",0.001,r"\cdot",W,r"\cdot",U,r"\cdot",B,r"}{",dl,"^{2}}=",HLT,"$$")

########################################
Htot = 2.64*(HLT+HLS+HPS+(0.28*(HS)))###
#print("Htot = ",Htot)###################
print(r"$$H_{tot}=2.64\cdot((",HS,r"\cdot","0.28)+",HLS,"+",HPS,"+",HLT,")=",Htot,"$$")
print("\n\n\n")

##########################################################################
####### 2 Dosis Ekivalen total dari Neutron Capture Gamma Rays ###########
##########################################################################
qn=4.6e11 #Kekuatan sumber neutron yang dipancarkan dari kepala, NCRP 151 = 4.6E11
#akselerator dan diserap isocenter per Gy sinar-X
B = 1 #Faktor transmisi untuk neutron yang menembus head shielding, asumsi head sebagai timbal b=1
x=2.505+8.605-1.500-2.350
x1=x-(1.550+0.765+3.24)
y1=1.900+2.500
y2=y1+0.125+0.925
x2= y2*(x1/y1)
r2=sqrt(x2**2+y2**2)
d1=r2
#d1 = #Jarak dari isocenter ke garis tengah labirin di pintu dengan arah sinar mengenai pinggir labirin
######################################################################
# LD1=1850*(8605-1500)
# LD2=125*2350
# LD3=2500*(6480+765+765)
# LD4=3800*6480
# LD5=1850*(6480+765+765)
# LDatas=(LD1+LD2+LD3+LD4+LD5)*2
# LDS=4270*(8605-1500+1850+125+2500+765+3800+765+1850+765+1850+6480
#           +765+1850+765+3800+765+2500+(2505+8605-1500-2350-1550)+125+11110-1500-2509+1850)
# sr=LDatas+LDS #Total luas permukaan dalam bunker, MINTOL SIAPA KEK, UDAH KEITUNG DI KERTAS
######################################################################
dl1=6.48
dw1=8.2
h=3.1
sr=2*((dl1*dw1)+(dl1*h)+(h*dw1))
print(r"$$S_{r}=2(d_{l}\times d_{w}+ d_{w}\times h+d_{l}\times h)")


################ 2.a Fluens Neutron ##########################
b=1
print("2a Fluens Neutron")
ya=((b*qn)/(4*pi*d1*d1))+((5.4*b*qn)/(2*pi*sr))+((1.3*qn)/(2*pi*sr))
print(r"$$\varphi_{A}=\frac{",b,r"\cdot",qn,r"}{4 \cdot \pi",d1,r"^{2}} \frac{5.4",b,r"\cdot",qn,"}{2\pi",r"\cdot",sr,r"} \frac{1.3 \cdot",qn,"}{2\pi",sr,"}=",ya,"$$")
#print("ya =",ya)

################ 2.b gamma capure di tiap beban kerja ########
print("2b Gamma Capture di tiap beban kerja")
TVD = 3 #(Tenth-Value Distance) jarak yang dibutuhkan untuk mereduksi
#photon fluence menjadi 1/10 kali semula (bernilai 3 untuk 10 MV)
d2 = 8.605-1.500-(2.350/2)#Jarak dari tengah labirin ke pintu (m)
K=6.9*10**(-16)#Nilai berdasarkan pengukuran : 6.9 * 10e-16 Sv m2 (NCRP report no. 151)
hy=K*ya*(10**(-d2/TVD)) #Dosis ekivalen hasil tangkapan gamma oleh Neutron (Sv/Gy)
print(r"$$h_{\varphi}=",K,r"\cdot",ya,r"\cdot(10^{-(\frac{",d2,"}{",TVD,"})}=",hy,"$$")
#print("hy =",hy)
################ 2.c Laju dosis neutron capture gamma rays####
hcg=W*hy #hcg= #Perhitungan LAju Dosis Neutron Capture Gamma Rays
print("$$H_{cg}=",W,r"\cdot",hy,"=",hcg,"$$")
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
print('3a Laju Dosis neutron di setiap beban kerja')
#s0/s1 = #Rasio luas penampang pintu masuk labirin dalam dengan luas penampang sepanjang labirin
#TVD= Tenth Value Dose
hnd1=2.4*10e-15*ya*sqrt(S0/S1)*(1.64*10**(-d2/1.9)+(10**-(d2/TVD)))#laju dosis neutron di setiap beban kerja
print("hnd = ",hnd1)
print(r"$$H_{n,D}=2.4 \cdot 10^{-15}",ya,r"\sqrt{\frac{",S0,"}{",S1,r"}}\begin{bmatrix}1.64 \cdot 10^{-\frac{",-d2,r"}{1.9}}+10^{-(\frac{",d2,"}{",TVD,"})}\end{bmatrix}=",hnd1,"$$")

################ 3.b Laju Dosis neutron #######################
print("3b laju dosis neutron")
hn=W*hnd1 #Perhitungan laju dosis neutron
print("$$H_{n}=",W,r"\cdot",hnd1,"=",hn,"$$")
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
print(r"$$n_{BPE}=log\frac{",hn1,"}{",P,"}=",nbpe,"$$")
print("nbpe = ",nbpe)
TVLbpe = 0.45
xbpe=nbpe*TVLbpe
print ("$$x_{bpe}=",nbpe,r"\cdot",TVLbpe,"=",xbpe,"$$")
print ("xbpe",xbpe)

##################### Perhitunggan Ketebalan Pb ##########################
P=5
Hy=Htot+hcg
print(r"$$h_{\varphi}=",Htot,"+",hcg,"=",Hy)
Hy1=Hy*10**6 #Karena P nya uSv, jadi ini dari Sv dirubah jadi uSv jg
print("Hy = ",Hy1)
nhy=log10(Hy1/(P))
print(r"$$n_{BPE}=log\frac{",Hy1,"}{",P,"}=",nhy,"$$")
print("nhy = ",nhy)
tvlpb=0.06
xpb=nhy*tvlpb
print ("$$x_{bpe}=",nbpe,r"\cdot",tvlpb,"=",xpb,"$$")
print("xpb = ",xpb)
