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
#universe=openmc.Universe(cells=[fuelcell,moderatorcell])
geouniv.plot(width=(6,6))
#plt.figure(figsize=(10,5))
#fig1=plt.subplot(121)
#fig1.imshow(geouniv.plot)
geouniv.plot(width=(6,6),basis='xz')
#fig2=plt.subplot(122)
#fig2.imshow(geouniv.plot)

plt.show()

##################################################################

settings=openmc.Settings()
settings.batches=200
settings.inactive=10
settings.particles=5000

#Why are these needed????
# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-0.63, -0.63, -0.63, 0.63, 0.63, 0.63]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings.source = openmc.Source(space=uniform_dist)


settings.export_to_xml()

##################################################################
tallies=openmc.Tallies()
#Ini konsentrasi Mesh maksudnya gimana? kaitannya apa sama detektor yang digunakan?
mesh=openmc.RegularMesh()
mesh.dimension=[100,100]
mesh.lower_left=(-2.9,-2.9)
mesh.upper_right=(2.9,2.9)

mesh_filter=openmc.MeshFilter(mesh)
#The alternatives are DistribcellFilter, EnergyFilter, MaterialFilter, MeshFilter, MuFilter, PolarFilter, SphHarmFilter, SurfaceFilter, UniverseFilter, and ZernikeFilter, UniverseFilter, EnergyFilter,MaterialFilter, CellbornFilter or CellFilter
#https://openmc.readthedocs.io/en/stable/usersguide/tallies.html

tally=openmc.Tally(name='flux')
tally.filters=[mesh_filter]
tally.scores=['flux','fission']

tallies.append(tally)

tallies.export_to_xml()

openmc.run()
##################################################################
##################################################################

sp=openmc.StatePoint('statepoint.20.h5') #20 is the number of batches, this function loads the tally results

tally=sp.get_tally(name='flux') #data yang diperlukan adalah flux, sehingga pakai itu. Fission belum dipakai
print("tally = \n",tally)

tally.sum

print(tally.mean.shape) #Mean dan standar deviasi dari nilai tally
(tally.mean, tally.std_dev)


flux=tally.get_slice(scores=['flux'])
fission=tally.get_slice(scores=['fission'])
print("flux = ",flux)
print("fission = ",fission)

flux.std_dev.shape=(100,100)
flux.mean.shape=(100,100)
fission.std_dev.shape=(100,100)
fission.mean.shape=(100,100)

fig3=plt.subplot(121) #1x2grid on first
fig3.imshow(flux.mean)
fig4=plt.subplot(122)
fig4.imshow(fission.mean)

plt.show()

relative_error=np.zeros_like(flux.std_dev)
nonzero=flux.mean>0
relative_error[nonzero]=flux.std_dev[nonzero]/flux.mean[nonzero]

ret=plt.hist(relative_error[nonzero],bins=50)
plt.show()



"""

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
"""
##################################################################