from IPython.display import Image
import numpy as np
import matplotlib.pyplot as plt
import openmc

fuel=openmc.Material(name=r'1.6% Fuel')
fuel=openmc.set_density('g/cm3',10.31341)
fuel=openmc.add_nuclide('U235',3.7503e-4)
fuel=openmc.add_nuclide('U238',2.2625E-2)
fuel=openmc.add_nuclide('O16',4.6007e-2)

water=openmc.Material(name='Borated Water')
water=openmc.set_density('g/cm3',0.740582)
water=openmc.add_nuclide('H1',4.9457e-2)
water=openmc.add_nuclide('O16',2.4732e-2)
water=openmc.add_nuclide('B10',8.0042e-6)

zircaloy=openmc.Material(name='Zircaloy')
zircaloy=openmc.set_density('g/cm3',6.55)
zircaloy=openmc.add_nuclide('Zr90',7.2758e-3)

materials=openmc.Materials([fuel,water,zircaloy])
materials.export_to_xml()

##################################################
fuelor=openmc.ZCylinder(r=0.39)#fuel
fuelir=openmc.ZCylinder(r=0.4) #gap
clador=openmc.ZCylinder(r=0.46)#clad

fuelor_region= -fuelor
fuelir_region= +fuelor & -fuelir
clador_region= +fuelir & -clador

len=1.26
box=openmc.rectangular_prism(len,len,boundary_type='reflective')
water= box & +clador

univ=openmc.Universe(name='1.6% Fuel Pin')

fuelcell=openmc.Cell(fill=fuel,region=fuelor_region)
gapcell=openmc.Cell(region=fuelir_region)
cladcell=openmc.Cell(fill=zircaloy,region=clador_region)
moderator=openmc.Cell(fill=water,region=water)

univ.add_cell(fuelcell,gapcell,cladcell,moderator)

geometry=openmc.Geometry(univ)
geometry.export_to_xml()