import openmc  #type: ignore

import matplotlib.pyplot as plt
from math import * #type: ignore

particle=int(input('Particle number (\'twas 1e7)\n= '))

air=openmc.Material(name='Air')
air.set_density('g/cm3',0.001205)
air.add_nuclide('N14',0.7)
air.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air.add_element('C',0.002)
air.add_element('Fe',0.001)
air.add_element('Si',0.001)
air.add_element('Mn',0.001)

air2=openmc.Material(name='Air')
air2.set_density('g/cm3',0.001205)
air2.add_nuclide('N14',0.7)
air2.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air2.add_element('C',0.002)
air2.add_element('Fe',0.001)
air2.add_element('Si',0.001)
air2.add_element('Mn',0.001)

air3=openmc.Material(name='Air')
air3.set_density('g/cm3',0.001205)
air3.add_nuclide('N14',0.7)
air3.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air3.add_element('C',0.002)
air3.add_element('Fe',0.001)
air3.add_element('Si',0.001)
air3.add_element('Mn',0.001)

water=openmc.Material(name='Water')
water.set_density('g/cm3',1.0)
water.add_nuclide('H1',2.0)
water.add_nuclide('O16',1.0)
water.add_s_alpha_beta('c_H_in_H2O')

soft=openmc.Material(name='Soft Tissue')
soft.set_density('g/cm3',1.0)
soft.add_element('H', 10.4472, percent_type='ao')#1
soft.add_element('C', 23.219, percent_type='ao')#6
soft.add_element('N', 2.388, percent_type='ao')#7
soft.add_element('O', 63.0238, percent_type='ao')#8
soft.add_element('Na', 0.113, percent_type='ao')#11
soft.add_element('Mg', 0.013, percent_type='ao')#12
soft.add_element('S',  0.199, percent_type='ao')#16
soft.add_element('Cl', 0.134, percent_type='ao')#17
soft.add_element('K',  0.199, percent_type='ao')#19
soft.add_element('Ca', 0.023, percent_type='ao')#20
#https://physics.nist.gov/cgi-bin/Star/compos.pl?matno=261

bpe=openmc.Material(name='Borate Polyethylene')
bpe.set_density('g/cm3',1.0)
bpe.add_element('H', 0.111, percent_type='ao')#1
bpe.add_element('C', 0.856, percent_type='ao')#6
bpe.add_element('B', 0.143, percent_type='ao')#5
bpe.add_element('O', 0.889, percent_type='ao')#8

lead=openmc.Material(name='Lead')
lead.set_density('g/cm3',11.35)
lead.add_element('Pb',1.0)

concrete=openmc.Material(name='Concrete')
concrete.set_density('g/cm3',2.3) #Harus disesuaikan dengan uji beton
concrete.add_element('H', 0.01, percent_type='ao')#1
concrete.add_element('C', 0.01, percent_type='ao')#6
concrete.add_element('O', 0.52, percent_type='ao')#8
concrete.add_element('Na', 0.01, percent_type='ao')#11
concrete.add_element('Mg', 0.01, percent_type='ao')#12
concrete.add_element('Al', 0.01, percent_type='ao')#13
concrete.add_element('Si', 0.25, percent_type='ao')#14
concrete.add_element('S',  0.01, percent_type='ao')#16
concrete.add_element('K',  0.01, percent_type='ao')#19
concrete.add_element('Ca', 0.01, percent_type='ao')#20
concrete.add_element('Fe', 0.01, percent_type='ao')#26 
concrete.add_element('Pb', 0.01, percent_type='ao')#82

iron = openmc.Material(name="Iron")
iron.set_density('g/cm3',7.87) #Harus disesuaikan dengan uji beton
iron.add_element('Fe', 1.0)#1

materials=openmc.Materials([air,air2,air3,water,soft,bpe,lead,concrete,iron]) 
materials.export_to_xml()

################################################
rotationDegree=int(input("Harap masukkan sudut rotasi LINAC\n= "))
############# Geometry ########################
#x
t1=openmc.XPlane(632)
t2=openmc.XPlane(632-76.5)
t3=openmc.XPlane(632-76.5-155)
t3fe=openmc.XPlane(632-76.5-155-235)
t4=openmc.XPlane(632-76.5-155-76.5)
t5=openmc.XPlane(632-76.5-155-76.5)
t6=openmc.XPlane(632-76.5-155-235)

b1=openmc.XPlane(-632)
b2=openmc.XPlane(-632+76.5)
b3=openmc.XPlane(-632+76.5+155.0)
b4=openmc.XPlane(-632+76.5+155.0+76.5)
b5=openmc.XPlane(-632+76.5+250.5)

#y #Di berkas 125, tapi ga make sense jadi diubah ke 1200 biar masuk angkanya
u1=openmc.YPlane(190.0+250.0+120.0+185.0+81.0)
u2=openmc.YPlane(190.0+250.0+120.0+185.0)
ufe=openmc.YPlane(190.0+250.0+120.0+185.0-10)
u3=openmc.YPlane(190.0+250.0+120.0)
u4=openmc.YPlane(190.0+250.0)
u5=openmc.YPlane(190.0)

s1=openmc.YPlane(-190.0-185.0-128.0)
s2=openmc.YPlane(-190.0-185.0)
s3=openmc.YPlane(-190.0)

#z total tinggi = 6000, lantai 1 setebal 480

zm1=openmc.ZPlane(-300.0)
zmax=openmc.ZPlane(300.0)
z3=openmc.ZPlane(-300.0+48.0+124.0+186.0+117.0+125.0)#1250 ATO 2500???
z2=openmc.ZPlane(-300.0+48.0+124.0+186.0+117.0)
z1=openmc.ZPlane(-300.0+48.0+124.0+186.0)
z0=openmc.ZPlane(-300.0+48.0)

#pintu utara, pintu barat, pintu selatan geometri nya
pu=openmc.YPlane(190.0+250.0+120.0+185.0+40.0) 
#                                    ^^^ asumsi pintu lebih lebar 40cm dibandingkan lubang pintunya
pb0=b5
pb1=openmc.XPlane(-632.0+76.5+250.5-1) #Angkanya ini masih ngarang karena gatau tebal pintu, ada kemungkinan formulanya di RHSPintu.py salah
pb2=openmc.XPlane(-632.0+76.5+250.5-1-15)
pb3=openmc.XPlane(-632.0+76.5+250.5-1-15-1)

ps=u3


###############################################
dt1 = -t1 & +t2 & +s3 & -u5 & +z0 & -z2   
dt2 = -t2 & +t3 & +s1 & -u1 & +z0 & -z2
dt3 = -t3 & +t4 & +s3 & -u5 & +z0 & -z2

db1 = +b1 & -b2 & +s3 & -u5 & +z0 & -z2
db2 = +b2 & -b3 & +s1 & -u3 & +z0 & -z2
db3 = +b3 & -b4 & +s3 & -u5 & +z0 & -z2

du1 = +b5 & -t3 & -u1 & +u2 & +z0 & -z2
du2 = +b3 & -t6 & -u3 & +u4 & +z0 & -z2

ds1 = +b3 & -t3 & +s1 & -s2 & +z0 & -z2

fe1 = -t3 & +t3fe & -u1 & +ufe & +z0 & -z2

datas= +b1 & -t1 & +s1 & -u1 & +z2 & -z3 #celing
datte= +b4 & -t4 & -u5 & +s3 & +z1 & -z2 #linac's middle wall
dbaw = +b1 & -t1 & +s1 & -u1 & +zm1 & -z0 #flooring
###############################################
#pintu
ppb = -pu & +ps & -pb0 & +pb1 & +z0 & -z2#pintu Pb
pbpe= -pu & +ps & -pb1 & +pb2 & +z0 & -z2#pintu BPE
ppb2= -pu & +ps & -pb2 & +pb3 & +z0 & -z2#pintu Pb

#Udara
#void1= -dt1 & +dt2 & -dt3 & +db1 & -db2 & +db3 & -du1 & +du2 & -ds1 & +ppb & -pbpe & +ppb2 & +datas & -dbaw 
#void1cell=openmc.Cell(fill=air,region=void1)

#Cell =

dt1cell=openmc.Cell(fill=concrete,region=dt1)
dt2cell=openmc.Cell(fill=concrete,region=dt2)
dt3cell=openmc.Cell(fill=concrete,region=dt3)
db1cell=openmc.Cell(fill=concrete,region=db1)
db2cell=openmc.Cell(fill=concrete,region=db2)
db3cell=openmc.Cell(fill=concrete,region=db3)
du1cell=openmc.Cell(fill=concrete,region=du1)
du2cell=openmc.Cell(fill=concrete,region=du2)
ds1cell=openmc.Cell(fill=concrete,region=ds1)

ppbcell=openmc.Cell(fill=lead,region=ppb)
pbpecell=openmc.Cell(fill=bpe,region=pbpe)
ppb2cell=openmc.Cell(fill=lead,region=ppb2)

datascell=openmc.Cell(fill=concrete,region=datas)
dattecell=openmc.Cell(fill=concrete,region=datte)
dbawcell=openmc.Cell(fill=concrete,region=dbaw)

fecell=openmc.Cell(fill=iron, region=fe1)

###############################################
#                Detektor/Tally               #

detd= 4.5
detde=10
#                          Utara              #
deu1=openmc.YPlane  (190.0+250.0+120.0+185.0+81.0+30.0)
deu1t=openmc.YPlane (190.0+250.0+120.0+185.0+81.0+30.0+10.8) #+tebal detektor
deu1ts=openmc.YPlane(190.0+250.0+120.0+185.0+81.0+30.0+detde) #+tebal detektor
deu2=openmc.YPlane  (190.0+250.0+120.0+185.0+81.0+100.0)
deu2t=openmc.YPlane (190.0+250.0+120.0+185.0+81.0+100.0+10.8)
b5=openmc.XPlane(-632+76.5+250.5)
deu2ts=openmc.YPlane(190.0+250.0+120.0+185.0+81.0+100.0+detde)
deu3=openmc.YPlane  (190.0+250.0+120.0+185.0+81.0+200.0)
deu3t=openmc.YPlane (190.0+250.0+120.0+185.0+81.0+200.0+10.8)
deu3ts=openmc.YPlane(190.0+250.0+120.0+185.0+81.0+200.0+detde)

deuz0=openmc.ZPlane(-300.0+48.0+100.0)#Tinggi detektor, default untuk semua detektor kecuali atas
deuz1=openmc.ZPlane(-300.0+48.0+100.0+50.0)
deuz0s=openmc.ZPlane(-300.0+48.0+100.0-(detd/2))#Tinggi detektor, default untuk semua detektor kecuali atas
deuz1s=openmc.ZPlane(-300.0+48.0+100.0+(detd/2))

deubb=openmc.XPlane(-632.0+76.5+250.5+100.0) #Koordinat x nya masih ngasal
deubt=openmc.XPlane(-632.0+76.5+250.5+100.0+50.0)
deubbs=openmc.XPlane(-632.0+76.5+250.5+100.0-(detd/2)) #Koordinat x nya masih ngasal
deubts=openmc.XPlane(-632.0+76.5+250.5+100.0+(detd/2))

deucb=openmc.XPlane(250.0) #koordinat x nya masih ngasal
deuct=openmc.XPlane(250.0+50.0)
deucbs=openmc.XPlane(250.0-detd/2) #koordinat x nya masih ngasal
deucts=openmc.XPlane(250.0+detd/2)

detb1= +deu1 & -deu1t & +deuz0 & -deuz1 & +deubb & -deubt #detektor utara barat, x nya ngasal
detb2= +deu2 & -deu2t & +deuz0 & -deuz1 & +deubb & -deubt
detb3= +deu3 & -deu3t & +deuz0 & -deuz1 & +deubb & -deubt
dett1= +deu1 & -deu1t & +deuz0 & -deuz1 & +deucb & -deuct #detektor utara timur, x nya ngasal
dett2= +deu2 & -deu2t & +deuz0 & -deuz1 & +deucb & -deuct
dett3= +deu3 & -deu3t & +deuz0 & -deuz1 & +deucb & -deuct

detb1s= +deu1 & -deu1ts & +deuz0s & -deuz1s & +deubbs & -deubts #detektor utara barat, x nya ngasal
detb2s= +deu2 & -deu2ts & +deuz0s & -deuz1s & +deubbs & -deubts
detb3s= +deu3 & -deu3ts & +deuz0s & -deuz1s & +deubbs & -deubts
dett1s= +deu1 & -deu1ts & +deuz0s & -deuz1s & +deucbs & -deucts #detektor utara timur, x nya ngasal
dett2s= +deu2 & -deu2ts & +deuz0s & -deuz1s & +deucbs & -deucts
dett3s= +deu3 & -deu3ts & +deuz0s & -deuz1s & +deucbs & -deucts

#Detektor
detub1cell=openmc.Cell(fill=air2,region=detb1) #sel detektor barat 1
detub2cell=openmc.Cell(fill=air2,region=detb2)
detub3cell=openmc.Cell(fill=air2,region=detb3)
detut1cell=openmc.Cell(fill=air2,region=dett1)
detut2cell=openmc.Cell(fill=air2,region=dett2)
detut3cell=openmc.Cell(fill=air2,region=dett3)

detub1scell=openmc.Cell(region=detb1s) #sel detektor barat 1
detub2scell=openmc.Cell(region=detb2s)
detub3scell=openmc.Cell(region=detb3s)
detut1scell=openmc.Cell(region=dett1s)
detut2scell=openmc.Cell(region=dett2s)
detut3scell=openmc.Cell(region=dett3s)


#                          Timur              #
det1=openmc.XPlane(632.0+30.0)
det1t=openmc.XPlane(632.0+30.0+10.8)
det1ts=openmc.XPlane(632.0+30.0+detde)
det2=openmc.XPlane(632.0+100.0)
det2t=openmc.XPlane(632.0+100.0+10.8)
det2ts=openmc.XPlane(632.0+100.0+detde)
det3=openmc.XPlane(632.0+200.0)
det3t=openmc.XPlane(632.0+200.0+10.8)
det3ts=openmc.XPlane(632.0+200.0+detde)

detu=openmc.YPlane(25.0)
dets=openmc.YPlane(-25.0)
detus=openmc.YPlane((detd/2))
detss=openmc.YPlane(-(detd/2))

dett1= +det1 & -det1t & +deuz0 & -deuz1 & -detu & +dets
dett2= +det2 & -det2t & +deuz0 & -deuz1 & -detu & +dets
dett3= +det3 & -det3t & +deuz0 & -deuz1 & -detu & +dets
dett3s= +det3 & -det3t & +deuz0 & -deuz1 & -detu & +dets
dett1s= +det1 & -det1ts & +deuz0s & -deuz1s & -detus & +detss
dett2s= +det2 & -det2ts & +deuz0s & -deuz1s & -detus & +detss
dett3s= +det3 & -det3ts & +deuz0s & -deuz1s & -detus & +detss

dett1cell=openmc.Cell(fill=air2,region=dett1)
dett2cell=openmc.Cell(fill=air2,region=dett2)
dett3cell=openmc.Cell(fill=air2,region=dett3)
dett1scell=openmc.Cell(region=dett1s)
dett2scell=openmc.Cell(region=dett2s)
dett3scell=openmc.Cell(region=dett3s)

#                          Barat              #

deb1  =openmc.XPlane (-632.0+76.5+250.5-1-15-1-30.0)
deb1t =openmc.XPlane (-632.0+76.5+250.5-1-15-1-30.0-10.8)
deb1ts=openmc.XPlane (-632.0+76.5+250.5-1-15-1-30.0-detde)
deb2  =openmc.XPlane (-632.0+76.5+250.5-1-15-1-100)
deb2t =openmc.XPlane (-632.0+76.5+250.5-1-15-1-100-10.8)
deb2ts=openmc.XPlane (-632.0+76.5+250.5-1-15-1-100-detde)
deb3  =openmc.XPlane (-632.0+76.5+250.5-1-15-1-200.0)
deb3t =openmc.XPlane (-632.0+76.5+250.5-1-15-1-200-10.8)
deb3ts=openmc.XPlane (-632.0+76.5+250.5-1-15-1-200-detde)

debu =openmc.YPlane(190.0+250.0+120.0+185.0-67.5) 
debs =openmc.YPlane(190.0+250.0+120.0+185.0-67.5-50.0) 
debus=openmc.YPlane(190.0+250.0+120.0+185.0-67.5+(detd/2))
debss=openmc.YPlane(190.0+250.0+120.0+185.0-67.5-(detd/2)) 

detb1= -deb1 & +deb1t & +deuz0 & -deuz1 & -debu & +debs
detb2= -deb2 & +deb2t & +deuz0 & -deuz1 & -debu & +debs
detb3= -deb3 & +deb3t & +deuz0 & -deuz1 & -debu & +debs
detb1s= -deb1 & +deb1ts & +deuz0s & -deuz1s & -debus & +debss
detb2s= -deb2 & +deb2ts & +deuz0s & -deuz1s & -debus & +debss
detb3s= -deb3 & +deb3ts & +deuz0s & -deuz1s & -debus & +debss

detb1cell=openmc.Cell(fill=air2,region=detb1)
detb2cell=openmc.Cell(fill=air2,region=detb2)
detb3cell=openmc.Cell(fill=air2,region=detb3)

detb1scell=openmc.Cell(region=detb1s)
detb2scell=openmc.Cell(region=detb2s)
detb3scell=openmc.Cell(region=detb3s)

#                          Atas               #
deau=openmc.XPlane(25.0)
deas=openmc.XPlane(-25.0)
deaus=openmc.XPlane(detd/2)
deass=openmc.XPlane(-detd/2)

deat=openmc.YPlane(25.0)
deab=openmc.YPlane(-25.0)
deats=openmc.YPlane(detd/2)
deabs=openmc.YPlane(-detd/2)

dea1=openmc.ZPlane(300.0+50.0) #1250 ATO 2500???
dea1t=openmc.ZPlane(300.0+50.0+10.8) #1250 ATO 2500???
dea1ts=openmc.ZPlane(300.0+30.0+detde) #1250 ATO 2500???
dea2=openmc.ZPlane(300.0+100.0)
dea2t=openmc.ZPlane(300.0+100.0+10.8)
dea2ts=openmc.ZPlane(300.0+100.0+detde)
dea3=openmc.ZPlane(300.0+200.0) 
dea3t=openmc.ZPlane(300.0+200.0+10.8)
dea3ts=openmc.ZPlane(300.0+200.0+detde)

deta1= +dea1 & -dea1t & -deau & +deas & +deab & -deat
deta2= +dea2 & -dea2t & -deau & +deas & +deab & -deat
deta3= +dea3 & -dea3t & -deau & +deas & +deab & -deat
deta1s= +dea1 & -dea1ts & -deaus & +deass & +deabs & -deats
deta2s= +dea2 & -dea2ts & -deaus & +deass & +deabs & -deats
deta3s= +dea3 & -dea3ts & -deaus & +deass & +deabs & -deats

deta1cell=openmc.Cell(fill=air2,region=deta1)
deta2cell=openmc.Cell(fill=air2,region=deta2)
deta3cell=openmc.Cell(fill=air2,region=deta3)
deta1scell=openmc.Cell(region=deta1s)
deta2scell=openmc.Cell(region=deta2s)
deta3scell=openmc.Cell(region=deta3s)

#Water Phantom 10x10x5
#TODO: Water phantom dpp and lateral tallies, to get flux value and relative comparison to the dose.
#make tally, search for the dose, search the corresponding flux, use it as the conversion rate for searching dose(sv/h)

phantom_rotation=270 #phantom rotation
pr=phantom_rotation
detaxu=openmc.YPlane(5)
detaxs=openmc.YPlane(-5)

if pr==0 or pr==180:
    detaxt=openmc.XPlane(5)
    detaxb=openmc.XPlane(5)
    detaxza=openmc.ZPlane(-128+100+2.5)
    detaxzb=openmc.ZPlane(-128+100-2.5)
if pr==180:
    detaxt=openmc.XPlane(5)
    detaxb=openmc.XPlane(-5)
    detaxza=openmc.ZPlane(-128-100+2.5)
    detaxzb=openmc.ZPlane(-128-100-2.5)
elif pr==90 or pr==270:
    detaxza=openmc.XPlane(2.5)
    detaxzb=openmc.XPlane(-2.5)
    detaxt=openmc.ZPlane(-128+5)
    detaxb=openmc.ZPlane(-128-5)
    
else:
    print('Phantom Rotation Error, benarkan kode pr')

detax= -detaxu & +detaxs & -detaxt & +detaxb & -detaxza & +detaxzb # type: ignore

detaxcell=openmc.Cell(fill=water,region=detax)

#Kotak Udara Pembatas
ymax=openmc.YPlane(1100,boundary_type='vacuum')
ymin=openmc.YPlane(-1100,boundary_type='vacuum')
xmax=openmc.XPlane(945,boundary_type='vacuum')
xmin=openmc.XPlane(-945,boundary_type='vacuum')
zmin=openmc.ZPlane(-550,boundary_type='vacuum')
zmaxx=openmc.ZPlane(550,boundary_type='vacuum')

#void1cell = openmc.Cell(fill=air, region= (-datascell.region) & (-dt1cell.region) & (-dt2cell.region) & (-dt3cell.region) & (-db1cell.region) & (-db2cell.region) & (-db3cell.region) & (-du1cell.region) & (-du2cell.region) & (-ds1cell.region))

void1= +zmin & -zmaxx \
    & +ymin & -ymax & +xmin & -xmax\
    & ~dt1cell.region & ~dt2cell.region & ~dt3cell.region \
        & ~db1cell.region & ~db2cell.region & ~db3cell.region \
            & ~du1cell.region & ~du2cell.region & ~ds1cell.region\
            & ~ppbcell.region & ~pbpecell.region & ~ppb2cell.region\
            & ~datascell.region & ~dbawcell.region & ~dattecell.region\
            & ~fecell.region\
            & ~detb1scell.region & ~detb2scell.region & ~detb3scell.region\
            & ~detub1scell.region & ~detub2scell.region & ~detub3scell.region\
            & ~detut1scell.region & ~detut2scell.region & ~detut3scell.region\
            & ~dett1scell.region & ~dett2scell.region & ~dett3scell.region\
            & ~deta1scell.region & ~deta2scell.region & ~deta3scell.region\
            #& ~detb1cell.region & ~detb2cell.region & ~detb3cell.region\
            #& ~detub1cell.region & ~detub2cell.region & ~detub3cell.region\
            #& ~detut1cell.region & ~detut2cell.region & ~detut3cell.region\
            #& ~dett1cell.region & ~dett2cell.region & ~dett3cell.region\
            #& ~deta1cell.region & ~deta2cell.region & ~deta3cell.region\

void1cell = openmc.Cell(fill=air, region=void1)

univ=openmc.Universe(cells=[dt1cell,dt2cell,dt3cell,
                            db1cell,db2cell,db3cell,
                            du1cell,du2cell,ds1cell,
                            ppbcell,pbpecell,ppb2cell,
                            datascell,dbawcell,dattecell,
                            void1cell,
                            detb1cell,detb2cell,detb3cell,
                            detub1cell,detub2cell,detub3cell,
                            detut1cell,detut2cell,detut3cell,
                            dett1cell,dett2cell,dett3cell,
                            deta1cell,deta2cell,deta3cell,
                            detb1scell,detb2scell,detb3scell,
                            detub1scell,detub2scell,detub3scell,
                            detut1scell,detut2scell,detut3scell,
                            dett1scell,dett2scell,dett3scell,
                            deta1scell,deta2scell,deta3scell,
                            detaxcell,fecell])
geometry=openmc.Geometry(univ)
geometry.export_to_xml()

colors= {}
colors[lead]='black'
colors[bpe]='lightblue'
colors[concrete]='grey'
colors[air]='white'
colors[air2]='blue'
colors[iron]='black'

###############################################
#                Rotation
###############################################
def sposi(d,rot):
    u= (-sin(radians(rot)))
    v= 0
    w= (-cos(radians(rot))) #source position
    uvw = (u,v,w)
    xyz = ( d*(sin(radians(rot))) ), 0, -128+ ( d*(cos(radians(rot)) ))
    xyz = xyz
    if rot==0 or rot==180:
        xyz1= ( d*(sin(radians(rot))) )+20, 20, -128+ ( d*(cos(radians(rot)) )+0.1)
        xyz2= ( d*(sin(radians(rot))) )-20, -20, -128+ ( d*(cos(radians(rot)) ))
    else:
        xyz1= ( d*(sin(radians(rot))) )+0.1, 20, -128+ ( d*(cos(radians(rot)) )+20)
        xyz2= ( d*(sin(radians(rot))) ), -20, -128+ ( d*(cos(radians(rot)) )-20)
    return uvw, xyz,xyz1,xyz2 
    #asumsi tinggi pasien 75
###############################################
#        Input (linac distance,rotation)      #
linacuvw, linacxyz,linacxyzn1,linacxyzn2=sposi(100,rotationDegree)
###############################################
print("linacuvw,linacxyz,linacuvwn1,linacuvwn2",linacuvw, linacxyz,linacxyzn1,linacxyzn2)

###############################################
#            Penampil Geometri                #
###############################################
plot=openmc.Plot()
plot.basis='xy'
plot.origin=(0,200,-149)
plot.width=(3000,3000)
plot.pixles=(2000,2000)
plot.filename='xy_room'
plot.colors={
    lead:'black',
    bpe:'lightblue',
    concrete:'grey',
    air:'white',
    air2:'blue',
    air3:'red',
    iron:'yellow'
}
plot.color_by='material'
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.plot_geometry()
#!convert something.ppm something.png

plot.to_ipython_image()

plot.basis='yz'
plot.filename='yz_room'
plot.width=(2000,2000)
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.plot_geometry()
plot.to_ipython_image()

plot.basis='xz'
plot.filename='xz_room'
plot.pixles=(2000,2000)
plot.width=(2000,2000)
plot.origin=(0,0,0)
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.plot_geometry()
plot.to_ipython_image()
"""
plt.rcParams.update({'font.size': 5})
univ.plot(width=(2500,2700),basis='xy',color_by='material',colors=colors)
plt.savefig('xyRSHS.png',dpi=500, bbox_inches='tight')
plt.show()
univ.plot(width=(1400,1040),basis='xz',color_by='material',colors=colors)
plt.savefig('xzRSHS.png',dpi=500, bbox_inches='tight')
plt.show()
univ.plot(width=(1800,1040),basis='yz',color_by='material',colors=colors)
plt.savefig('yzRSHS.png',dpi=500, bbox_inches='tight')
plt.show()

"""
#Tidak terdapat library matplotlib pada server, sehingga  penampil geometri harus dimatikan untuk running server
###############################################
#                 Plot Grid                   #
###############################################
#ax.set_title('Distribusi Dosis Ruangan (uSv/hour)') #type: ignore
#univ.plot(width=(2000,2000),basis='xy',color_by='material',colors=colors)
#plt.savefig('DoseDistributionMap.png',dpi=500, bbox_inches='tight')

###############################################
#                 Setting                     #
###############################################
settings=openmc.Settings()
source  =openmc.Source()
"""
#source.space=openmc.stats.Points(xyz=)
source.space=openmc.stats.Point(xyz=linacxyz) # type: ignore
#phi2=openmc.stats.Isotropic() #isotropic ato uniform?
#phi1=openmc.stats.Monodirectional((0,0,1))
phi =openmc.stats.Uniform(0.0,2*pi) # type: ignore #phi=distribution of the azimuthal angle in radians
#mu= distribution of the cosine of the polar angle

#tan theta = r/SAD=20/1000; theta = atan(20/100)=0.19739555984988; cos theta=0.98058
mu=openmc.stats.Uniform(0.98058,1) # type: ignore #mu= distribution of the cosine of the polar angle

source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=linacuvw) # type: ignore
source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV # type: ignore
"""
#source.space=openmc.stats.Point(xyz=linacxyz) # type: ignore
#source.space = openmc.stats.Box((-PHANTOM_SIZE/2-d, -SOURCE_SIZE/2, -SOURCE_SIZE/2), (-PHANTOM_SIZE/2-d-t, SOURCE_SIZE/2, SOURCE_SIZE/2))
source.space = openmc.stats.Box((linacxyzn1), (linacxyzn2))
source.angle = openmc.stats.Monodirectional(linacuvw)
source.energy = openmc.stats.Discrete([10e6], [1])

source.particle = 'photon'
#source.particle = 'neutron'
settings.source = source
settings.batches= 3
settings.particles = particle
#Asumsi 36e7 partikel pada mula, pada 600MU=600cGy/m=6Gy/m=6Sv/m=6e6uSv/m=360e6uSv/h
settings.run_mode = 'fixed source'
settings.photon_transport = True
settings.export_to_xml()

###############################################
#                 Tallies                     #
###############################################
tally = openmc.Tallies()
#TODO: Change Tally size to smaller actual tally size value
#Tally Dose Distribution
mesh = openmc.RegularMesh() # type: ignore
mesh.dimension = [500, 500]
xlen = 2000;ylen = 2000
mesh.lower_left = [-xlen/2, -xlen/2]
mesh.upper_right = [ylen/2, ylen/2]
mesh_filter = openmc.MeshFilter(mesh)

tally1 = openmc.Tally(name = 'Room Dose Distribution')
tally1.scores = ['flux']
particle1 = openmc.ParticleFilter('photon')

energy, dose = openmc.data.dose_coefficients('photon', 'RLAT') #Data konve # type: ignore
dose_filter = openmc.EnergyFunctionFilter(energy, dose) #konvert partikel energi tertentu ke deskripsi icrp116 partikelcm/src->pSvcm3/srcwphantom_cell,particle3,dose_filter

tally1.filters=[mesh_filter,particle1,dose_filter]
tally.append(tally1)

#Tally Detektor
filter_cell = openmc.CellFilter((detb1cell,detb2cell,detb3cell,\
                            detub1cell,detub2cell,detub3cell,\
                            detut1cell,detut2cell,detut3cell,\
                            dett1cell,dett2cell,dett3cell,\
                            deta1cell,deta2cell,deta3cell))
tally2 = openmc.Tally(name = 'flux')
particle2 = openmc.ParticleFilter('photon')
tally2.filters = [filter_cell, particle2, dose_filter]
tally2.scores = ['flux']
tally.append(tally2)

filter_cell_small = openmc.CellFilter((detb1scell,detb2scell,detb3scell,\
                            detub1scell,detub2scell,detub3scell,\
                            detut1scell,detut2scell,detut3scell,\
                            dett1scell,dett2scell,dett3scell,\
                            deta1scell,deta2scell,deta3scell))
tally4 = openmc.Tally(name = 'flux detektor small')
tally4.filters = [filter_cell_small, particle2, dose_filter]
tally4.scores = ['flux']
tally.append(tally4)

energy2, dose2 = openmc.data.dose_coefficients('neutron', 'AP') #Data konve # type: ignore
dose_filter = openmc.EnergyFunctionFilter(energy2, dose2) #konvert partikel energi tertentu ke deskripsi icrp116 partikelcm/src->pSvcm3/srcwphantom_cell,particle3,dose_filter
particle3=openmc.ParticleFilter('neutron')
neutroncell = openmc.CellFilter((detb1cell,detb2cell,detb3cell))
tally3= openmc.Tally(name='neutron')
tally3.filters=[neutroncell,particle3,dose_filter]
tally3.scores=['flux']
tally.append(tally3)

"""
#Tally Water Phantom
wphantom_cell=openmc.CellFilter(detaxcell)
tally3=openmc.Tally(name='wphantom')
particle3= openmc.ParticleFilter('photon')
#tally3.filters=[wphantom_cell,particle3]
#Energy_filter = openmc.EnergyFilter([1e-3, 1e13])
tally3.filters=[wphantom_cell,particle3,dose_filter]  #output pSvcm3/src 
tally3.scores = ['flux']
tally.append(tally3)
"""

tally.export_to_xml()
openmc.run()
