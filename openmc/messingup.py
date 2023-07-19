import openmc
import matplotlib.pyplot as plt
import numpy as np

fuel=openmc.Material()
fuel.set_density('g/cm3',10.31341)
fuel.add_nuclide('U235',3.7503e-4)
fuel.add_nuclide('U238',2.2625E-2)
fuel.add_nuclide('O16',4.6007e-2)

water=openmc.Material()
water.set_density('g/cm3',0.740582)
water.add_nuclide('H1',4.9457e-2)
water.add_nuclide('O16',2.4732e-2)

materials=openmc.Materials([fuel,water])
materials.export_to_xml()
##################################################################

##################################################################
bola=openmc.Sphere(r=1)
kotak=openmc.rectangular_prism(2,2,boundary_type='reflective')

matahari=-bola
moderator=+bola & kotak

fuelcell=openmc.Cell(fill=fuel,region=matahari)
moderatorcell=openmc.Cell(fill=water,region=moderator)

geouniv=openmc.Universe(name='Ball Box')

geouniv.add_cell(fuelcell)
geouniv.add_cell(moderatorcell)

geometry=openmc.Geometry(geouniv)
geometry.export_to_xml()
##################################################################

##################################################################
universe=openmc.Universe(cells=[fuelcell,moderatorcell])
universe.plot(width=(3,3))
universe.plot(width=(3,3),basis='xz')

plt.show()