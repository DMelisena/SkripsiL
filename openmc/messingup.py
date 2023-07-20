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
alasb=openmc.ZPlane(z0=-2.5)
alasa=openmc.ZPlane(z0=2.5)
bola=openmc.Sphere(r=1)
kotak=openmc.rectangular_prism(3,3,boundary_type='reflective')


matahari=-bola
moderator=+bola & kotak & -alasa & +alasb

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
universe.plot(width=(6,6))
universe.plot(width=(6,6),basis='xz')

plt.show()

##################################################################

settings=openmc.Settings()
settings.batches=100
settings.inactive=10
settings.particles=5000


import matplotlib.pyplot as plt

bounds= [-0.64,-0.64,-0.64,0.64,0.64,0.64] #just an array of [x_min, y_min, z_min, x_max, y_max, z_max]
uniform_dist=openmc.stats.Box(bounds[:3],bounds[3:],only_fissionable=True)
settings_file.source=openmc.Source(space=uniform_dist)
# Extract coordinates from the bounds array
x_min, y_min, z_min, x_max, y_max, z_max = bounds

# Plot the lower-left corner as a red circle
plt.scatter(x_min, y_min, color='red', label='Lower-Left Corner')

# Plot the upper-right corner as a blue circle
plt.scatter(x_max, y_max, color='blue', label='Upper-Right Corner')

# Set axis labels and title
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Lower-Left and Upper-Right Corners of the Box')

# Add a legend
plt.legend()

# Show the plot
plt.show()
