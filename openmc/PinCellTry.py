import openmc
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image


############# Material #######################
#Uranium Dioksida, Seperti H2O tapi pakai U bukannya H.
uo2 = openmc.Material(1,"uo2") 
uo2.add_nuclide('U235',0.03)
uo2.add_nuclide('U238',0.97)
uo2.add_nuclide('O16',2)
uo2.set_density('g/cm3',10)

#Just Water, H2O
water=openmc.Material(3,"H2O")
water.add_nuclide('H1',2)
water.add_nuclide('O16',1)
water.set_density('g/cc',1)
water.add_s_alpha_beta('c_H_in_H2O')

#Pure Zirconium
zirconium =  openmc.Material(2,"Zirconium")
zirconium.add_element('Zr',1.0)
zirconium.set_density('g/cm3',6.6)
print("Zirconium =",zirconium)

# zircaloy
zircaloy = openmc.Material(name='Zircaloy')
zircaloy.set_density('g/cm3', 6.55)
zircaloy.add_nuclide('Zr90', 7.2758e-3)
################################################
materials=openmc.Materials([uo2,zircaloy,water])
materials.export_to_xml()
################################################

################ Silinder ######################
fuel_or = openmc.ZCylinder(r=0.39)
clad_ir = openmc.ZCylinder(r=0.40)
clad_or = openmc.ZCylinder(r=0.46)
#fuel_region = -fuel_or #didalam fuel_or
#gap_region = +fuel_or & -clad_ir #diluar fuel_or, tetapi didalam clad_ir
#clad_region = +clad_ir & -clad_or #diluar clad_ir, tapi didalam clad_or

################ Bahan #########################
fuel = openmc.Cell(1,fill=uo2,region=-fuel_or)
#fuel.fill=uo2
#fuel.region = fuel_region

gap = openmc.Cell(2,region = +fuel_or & -clad_ir)
#gap.region = gap_region

clad=openmc.Cell(3,fill=zircaloy, region = +clad_ir & -clad_or)
#clad.fill= zircaloy
#clad.region = clad_region

################ Air ###########################
pitch = 1.26
#left = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
#right = openmc.XPlane(x0=pitch/2, boundary_type='reflective')
#bottom = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
#top = openmc.YPlane(y0=pitch/2, boundary_type='reflective')
box = openmc.rectangular_prism(width=pitch, height=pitch, boundary_type='reflective')
w_region = box & +clad_or
#w_region = +left & -right & +bottom & -top & + clad_or

moderator=openmc.Cell(fill=water,region=w_region)
moderator.fill = water
moderator.region=w_region
#Di luar clad or, adalah air. Tetapi didalam sumbu xy pitch

################################################
################################################
################################################
geom=openmc.Geometry([fuel,gap, clad, moderator])
geom.export_to_xml()

univ = openmc.Universe(cells=[fuel,gap, clad, moderator])
univ.plot(width=(3.0,3.0))
plt.savefig('pincell.png')
univ.plot(width=(3,3),basis='xz',colors={moderator:'fuchsia'})
plt.savefig('xzpincell.png')
#plt.show()

###### Starting Source and Setting ##############
#Define Problem Setting

point=openmc.stats.Point((0,0,0))
src=openmc.Source(space=point)

settings=openmc.Settings()
settings.source=src
settings.batches=100
settings.inactive = 10
settings.particles = 1000

settings.export_to_xml()
openmc.run()