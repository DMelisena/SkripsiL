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
zircaloy=openmc.set_density('g/cm3',0.740582)
zircaloy=openmc.add_nuclide('Zr90',7.2758e-3)

materials=openmc.Materials([fuel,water,zircaloy])
materials.export_to_xml()