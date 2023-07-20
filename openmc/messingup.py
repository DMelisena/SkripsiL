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
alasb=openmc.ZPlane(z0=-2.5,boundary_type='reflective')
alasa=openmc.ZPlane(z0=2.5,boundary_type='reflective')
bola=openmc.Sphere(r=1,boundary_type='reflective')
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

settings.export_to_xml()

##################################################################

tallies=openmc.Tallies()

mesh=openmc.RegularMesh()
mesh.dimension=[100,100]
mesh.lower_left=(-2.9,-2.9)
mesh.upper_right=(2.9,2.9)
mesh_filter=openmc.MeshFilter(mesh)

tally=openmc.Tally(name='flux')
tally.filters=[mesh_filter]
tally.scores=['flux','fission']

tallies.append(tally)

tallies.export_to_xml()



openmc.run()

##################################################################


# Step 1: Get the tally data from the simulation results
sp = openmc.StatePoint('statepoint.100.h5')
tally = sp.get_tally(name='flux')  # Replace 'flux' with the name of your tally

# Step 2: Get the dose coefficients for the corresponding particle and geometry
particle = 'neutron'  # Replace with the incident particle type used in the simulation
geometry = 'AP'       # Replace with the irradiation geometry used in the simulation
energy, dose_coeffs = openmc.data.dose_coefficients(particle, geometry)

# Interpolate dose coefficients to the tally energy grid
tally_energy = tally.filters[0].bins[0].edges

dose_coeffs_interp = np.interp(tally_energy, energy, dose_coeffs)

# Convert tally results to effective dose
effective_dose = tally.mean[:, 0, 0] * dose_coeffs_interp  # pSv cm^2 * flux (or air kerma)

# Calculate the total effective dose by summing over all energy bins
total_effective_dose = np.sum(effective_dose)

print("Total Effective Dose (pSv):", total_effective_dose)