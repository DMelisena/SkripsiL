import openmc
import matplotlib.pyplot as plt
from math import *

air=openmc.Material(name='Air')
air.set_density('g/cm3',0.001205)
air.add_nuclide('N14',0.7)
air.add_nuclide('O16',0.3)
air.add_s_alpha_beta('c_H_in_Air')
air.add_element('C',0.002)
air.add_element('Fe',0.001)
air.add_element('Si',0.001)
air.add_element('Mn',0.001)

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

materials=openmc.Materials([air,soft,bpe,lead,concrete])
materials.export_to_xml()

################################################

############# Geometry ########################
#x
t1=openmc.XPlane(6320,boundary_type='transmission')
t2=openmc.XPlane(6320-765,boundary_type='transmission')
t3=openmc.XPlane(6320-765-1550,boundary_type='transmission')
t4=openmc.XPlane(6320-765-1550-765,boundary_type='transmission')
t5=openmc.XPlane(6320-765-1550-765,boundary_type='transmission')

b1=openmc.XPlane(-6320,boundary_type='transmission')
b2=openmc.XPlane(-6320+765,boundary_type='transmission')
b3=openmc.XPlane(-6320+765+1550,boundary_type='transmission')
b4=openmc.XPlane(-6320+765+1550+765,boundary_type='transmission')
b5=openmc.XPlane(-6320+765+2505,boundary_type='transmission')

#y #Di berkas 125, tapi ga make sense jadi diubah ke 1200 biar masuk angkanya
u1=openmc.YPlane(1900+2500+1200+1850+810,boundary_type='transmission')
u2=openmc.YPlane(1900+2500+1200+1850,boundary_type='transmission')
u3=openmc.YPlane(1900+2500+1200,boundary_type='transmission')
u4=openmc.YPlane(1900+2500,boundary_type='transmission')
u5=openmc.YPlane(1900,boundary_type='transmission')

s1=openmc.YPlane(-1900-1850-1280,boundary_type='transmission')
s2=openmc.YPlane(-1900-1850,boundary_type='transmission')
s3=openmc.YPlane(-1900,boundary_type='transmission')

#z
zm1=openmc.ZPlane(-1000,boundary_type='reflective')
z0=openmc.ZPlane(0,boundary_type='reflective')
z1=openmc.ZPlane(3100,boundary_type='reflective')
z2=openmc.ZPlane(3100+1170,boundary_type='reflective')
z3=openmc.ZPlane(3100+1170+1250,boundary_type='reflective')

#pintu utara, pintu barat, pintu selatan
pu=openmc.YPlane(1900+2500+1200+1850+400,boundary_type='transmission') #asumsi pintu lebih lebar 40cm dibandingkan lubang pintunya
pb0=b5
pb1=openmc.XPlane(-6320+765+2505-158,boundary_type='transmission') #Angkanya ini masih ngarang karena gatau tebal pintu, ada kemungkinan formulanya di RHSPintu.py salah
pb2=openmc.XPlane(-6320+765+2505-158-1020,boundary_type='transmission')
pb3=openmc.XPlane(-6320+765+2505-158-1020-158,boundary_type='transmission')
ps=u3

###############################################
dt1 = -t1 & +t2 & +s3 & -u5 & +z0 & -z2  
dt2 = -t2 & +t3 & +s1 & -u1 & +z0 & -z2
dt3 = -t3 & +t4 & +s3 & -u5 & +z0 & -z2

db1 = +b1 & -b2 & +s3 & -u5 & +z0 & -z2
db2 = +b2 & -b3 & +s1 & -u3 & +z0 & -z2
db3 = +b3 & -b4 & +s3 & -u5 & +z0 & -z2

du1 = +b5 & -t3 & -u1 & +u2 & +z0 & -z2
du2 = +b3 & -t5 & -u3 & +u4 & +z0 & -z2

ds1 = +b3 & -t3 & +s1 & -s2 & +z0 & -z2

datas= +b1 & -t1 & +s1 & -u1 & +z2 & -z3
dbaw= +b1 & -t1 & +s1 & -u1 & +zm1 & -z0
###############################################
ppb = -pu & +ps & -pb0 & +pb1 & +z0 & -z2#pintu Pb
pbpe= -pu & +ps & -pb1 & +pb2 & +z0 & -z2#pintu BPE
ppb2= -pu & +ps & -pb2 & +pb3 & +z0 & -z2#pintu Pb

#pintu =

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
dbawcell=openmc.Cell(fill=concrete,region=dbaw)

univ=openmc.Universe(cells=[dt1cell,dt2cell,dt3cell,
                            db1cell,db2cell,db3cell,
                            du1cell,du2cell,ds1cell
                            ,ppbcell,pbpecell,ppb2cell
                            ,datascell,dbawcell])
geometry=openmc.Geometry(univ)
geometry.export_to_xml()

univ.plot(width=(14000,14000),basis='xy',colors={ppb2cell:'fuchsia'})
univ.plot(width=(14000,14000),basis='xz')
univ.plot(width=(14000,14000),basis='yz')
plt.show()