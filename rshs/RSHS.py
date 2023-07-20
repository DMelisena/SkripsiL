import openmc
import matplotlib.pyplot as pltt
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
#y
t1=openmc.YPlane(6320,boundary_type='transmission')
t2=openmc.YPlane(6320-765,boundary_type='transmission')
t3=openmc.YPlane(6320-765-1550,boundary_type='transmission')
t4=openmc.YPlane(6320-765-1550-765,boundary_type='transmission')
t5=openmc.YPlane(6320-765-1550-765,boundary_type='transmission')

b1=openmc.YPlane(-6320,boundary_type='transmission')
b2=openmc.YPlane(-6320+765,boundary_type='transmission')
b3=openmc.YPlane(-6320+765+1550,boundary_type='transmission')
b4=openmc.YPlane(-6320+765+2505,boundary_type='transmission')

#x
u1=openmc.XPlane(1900+2500+125+1850+810,boundary_type='transmission')
u2=openmc.XPlane(1900+2500+125+1850,boundary_type='transmission')
u3=openmc.XPlane(1900+2500+125,boundary_type='transmission')
u4=openmc.XPlane(1900+2500,boundary_type='transmission')
u5=openmc.XPlane(1900,boundary_type='transmission')

s1=openmc.XPlane(-1900-1850-1280,boundary_type='transmission')
s2=openmc.XPlane(-1900-1850,boundary_type='transmission')
s3=openmc.XPlane(-1900,boundary_type='transmission')

