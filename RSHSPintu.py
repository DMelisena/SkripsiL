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
#dsec = #jarak dari isocenter ke garis tengah labirin di pintu (m)
#dzz = #jarak garis tengah labirin ke pintu

#a0= #Koefisien refleksi pada hamburan pertama 
#az= #refleksi pada refleksi kedua dari permukaan Az
#A0= #Field size maksimum yang terproyeksi pada dinding A0(m2)
#Az= #luas cross section labirin (m2)
#dH= #Jarak isocenter ke dinding A0 [(dpp+1) pada gambar 3.6]
#dr= #Jarak dari pusat sinar pada refleksi pertama ke garis tengah labirin
#dz= #Panjang labirin ke pintu (m)

#A1= #Luas dinding yang dapat dilihat dari pintu masuk ruangan (m2)
#dsec= #jarak isocenter ke garis tengah labirin di pintu
#dzz = #jarak dari isocenter ke garis tengah labirin di pintu

#qn = #Kekuatan sumber neutron yang dipancarkan dari kepala, NCRP 151 = 4.6E11
#akselerator dan diserap isocenter per Gy sinar-X

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