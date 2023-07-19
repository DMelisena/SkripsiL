from IPython.display import Image
import numpy as np
import matplotlib.pyplot as plt
import openmc

fuel=openmc.Material(name=r'1.6% Fuel')
fuel.set_density('g/cm3',10.31341)
fuel.add_nuclide('U235',3.7503e-4)
fuel.add_nuclide('U238',2.2625E-2)
fuel.add_nuclide('O16',4.6007e-2)

water=openmc.Material(name='Borated Water')
water.set_density('g/cm3',0.740582)
water.add_nuclide('H1',4.9457e-2)
water.add_nuclide('O16',2.4732e-2)
water.add_nuclide('B10',8.0042e-6)

zircaloy=openmc.Material(name='Zircaloy')
zircaloy.set_density('g/cm3',6.55)
zircaloy.add_nuclide('Zr90',7.2758e-3)

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
water_region= box & +clador

fuelcell=openmc.Cell(fill=fuel,region=fuelor_region)
gapcell=openmc.Cell(region=fuelir_region)
cladcell=openmc.Cell(fill=zircaloy,region=clador_region)
moderator=openmc.Cell(fill=water,region=water_region)

univ=openmc.Universe(name='1.6% Fuel Pin')
univ.add_cell(fuelcell)
univ.add_cell(gapcell)
univ.add_cell(cladcell)
univ.add_cell(moderator)
geometry=openmc.Geometry(univ)
geometry.export_to_xml()

##################################################
universe=openmc.Universe(cells=[fuelcell,gapcell,cladcell,moderator])
universe.plot(width=(1.5,1.5))
universe.plot(width=(5,5),basis='xz')
plt.show
##################################################

settings_file=openmc.Settings()
settings_file.batches=100
settings_file.inactive=10
settings_file.particles = 5000

bounds= [-0.64,-0.64,-0.64,0.64,0.64,0.64] #just an array of [x_min, y_min, z_min, x_max, y_max, z_max]
uniform_dist=openmc.stats.Box(bounds[:3],bounds[3:],only_fissionable=True)
settings_file.source=openmc.Source(space=uniform_dist)

settings_file.export_to_xml()

##################################################

tallies=openmc.Tallies()
mesh = openmc.RegularMesh()
mesh.dimension = [100,100]
mesh.lower_left = -0.63, -0.63
mesh.upper_right = 0.63, 0.63
mesh_filter=openmc.MeshFilter(mesh)

tally=openmc.Tally(name='flux')
tally.filters=[mesh_filter]
tally.scores=['flux','fission']

tallies.append(tally)

tallies.export_to_xml()

openmc.run()
##################################################
sp = openmc.StatePoint('statepoint.100.h5')
sptally = sp.get_tally(scores=['flux'])
print(sptally)
tally.sum

print(sptally.mean.shape)
(sptally.mean,sptally.std_dev)

flux=sptally.get_slice(scores=['flux'])
fission = sptally.get_slice(scores=['fission'])
print(flux)

flux.std_dev.shape=(100,100)
flux.mean.shape=(100,100)
fission.std_dev.shape = (100,100)
fission.mean.shape=(100,100)

fig=plt.subplot(121)
fig.imshow(flux.mean)
fig2=plt.subplot(122)
fig2.imshow(fission.mean)

relative_error=np.zeros_like(flux.std_dev)
nonzero=flux.mean>0
relative_error[nonzero]=flux.std_dev[nonzero]/flux.mean[nonzero]

ret = plt.hist(relative_error[nonzero],bins=100)

sp.source
sp.source['E']

energy_bins=np.logspace(3,7)
probability,bin_edges=np.histogram(sp.source['E'],bins=energy_bins,density=True)

print(sum(probability*np.diff(energy_bins)))

plt.semilogx(energy_bins[:-1],probability*np.diff(energy_bins))
plt.xlabel('Energy(eV)')
plt.ylabel('probability/eV')

plt.quiver(sp.source['r']['x'],sp.source['r']['y'],
           sp.source['u']['x'],sp.source['u']['y'],
           np.log(sp.source['E']),cmap='jet',scale=20.0)

plt.colorbar()
plt.xlim((-0.5,0.5))
plt.ylim((-0.5,0.5))
plt.show()
