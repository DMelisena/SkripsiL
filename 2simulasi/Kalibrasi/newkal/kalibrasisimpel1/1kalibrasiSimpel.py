# vim:foldmethod=marker
import openmc
import matplotlib.pyplot as plt
import openmc.stats, openmc.data
from math import cos, atan2, pi

batches = 10
inactive = 10
particles = int(input('Enter number of particle (It was 1e8)\n= ')) #1_000_000_000


# Material 
# {{{
air=openmc.Material(name='Air')
air.set_density('g/cm3',0.001205)
air.add_nuclide('N14',0.7)
air.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air.add_element('C',0.002)
air.add_element('Fe',0.001)
air.add_element('Si',0.001)
air.add_element('Mn',0.001)

water=openmc.Material(name='Water')
water.set_density('g/cm3',1.0)
water.add_nuclide('H1',2.0)
water.add_nuclide('O16',1.0)
water.add_s_alpha_beta('c_H_in_H2O')

water2=openmc.Material(name='Water')
water2.set_density('g/cm3',1.0)
water2.add_nuclide('H1',2.0)
water2.add_nuclide('O16',1.0)
water2.add_s_alpha_beta('c_H_in_H2O')

materials = openmc.Materials([air,water,water2])
materials.export_to_xml()
# }}}

SSD = 100.0 #Source to Skin Distance
PHANTOM_WIDTH = 40 
ld= # panjang dan lebar WP
d = 30.0 #kedalaman WP
padd = 10.0 #padding terhadap source dan detektor

# {{{

n = 300
phantom_cells = []
dx = d/n
for i in range(n):
    x0 = SSD + i*dx
    x1 = SSD +(i+1)*dx
    r_x = +openmc.XPlane(x0) & -openmc.XPlane(x1)
    r_y = +openmc.YPlane(-ld/2.0) & -openmc.YPlane(ld/2.0)
    r_z = +openmc.ZPlane(-ld/2.0) & -openmc.ZPlane(ld/2.0)

    cell = openmc.Cell(region=r_x & r_y & r_z)
    cell.fill = water2
    phantom_cells.append(cell)

r_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+d)
r_y = +openmc.YPlane(-ld/2.0) & -openmc.YPlane(ld/2.0)
r_z = +openmc.ZPlane(-ld/2.0) & -openmc.ZPlane(ld/2.0)
r_phantally = r_x & r_y & r_z

r_y_wp= +openmc.YPlane(-PHANTOM_WIDTH/2.0)\
    & -openmc.YPlane(PHANTOM_WIDTH/2.0)
r_z_wp= +openmc.ZPlane(-PHANTOM_WIDTH/2.0)\
    & -openmc.ZPlane(PHANTOM_WIDTH/2.0)
r_wp= r_x & r_y_wp & r_z_wp
c_wp= openmc.Cell(region=r_wp& ~r_phantally)
c_wp.fill = water 

r_x_air = +openmc.XPlane(-padd, boundary_type='vacuum')\
    & -openmc.XPlane(SSD+d+padd, boundary_type='vacuum')
r_y_air = +openmc.YPlane(-PHANTOM_WIDTH/2.0-padd, boundary_type='vacuum')\
    & -openmc.YPlane(PHANTOM_WIDTH/2.0+padd, boundary_type='vacuum')
r_z_air = +openmc.ZPlane(-PHANTOM_WIDTH/2.0-padd, boundary_type='vacuum')\
    & -openmc.ZPlane(PHANTOM_WIDTH/2.0+padd, boundary_type='vacuum')
r_air = r_x_air & r_y_air & r_z_air
c_air = openmc.Cell(region=r_air & ~r_wp)
c_air.fill = air

universe = openmc.Universe(cells=[c_air]+phantom_cells+[c_wp])
geometry = openmc.Geometry()
geometry.root_universe = universe
geometry.export_to_xml()
# }}}
plot= openmc.Plot()
plot.basis = 'yz'
plot.filename='yz_cal'
plot.origin = (110, 0, 0)
plot.width = (100., 100.)
plot.pixels = (400, 400)
plot.color_by='material'
plot.colors={
    water:'blue',
    air:'green',
    water2:'black'
}
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.plot_geometry()
plot.to_ipython_image()

plot.basis='xz'
plot.filename='xz_cal'
plot.width=(100,100)
plot.pixels=(400,400)
plot.origin=(100,0,0)
plot_file=openmc.Plots([plot])
plot_file.export_to_xml()
openmc.plot_geometry()
plot.to_ipython_image()

# {{{
"""
height = 300
plotXZ = openmc.Plot()
plotXZ.filename = f'img'
plotXZ.basis = 'xy'
plotXZ.width = ((SSD+d+padd)*2, (SSD+d+padd)*2)
plotXZ.origin = (0,0,SSD)
plotXZ.color_by = 'material'
plotXZ.pixels = (200, 200)
plots = openmc.Plots([plotXZ])
plots.export_to_xml()
"""
# openmc.plot_geometry()
# }}}

# {{{
batches= batches
inactive = inactive 
particles = particles

particle_filter = openmc.ParticleFilter('photon')
# energy, dose = openmc.data.dose_coefficients('photon', 'AP')
energy, dose = openmc.data.dose_coefficients('photon', 'RLAT')
dose_filter = openmc.EnergyFunctionFilter(energy, dose) 

tallies_file = openmc.Tallies()
cell_filter = openmc.CellFilter(phantom_cells)
tally = openmc.Tally(name='tally')
tally.filters = [cell_filter, particle_filter, dose_filter]
tally.scores = ['flux']
tallies_file.append(tally)
tallies_file.export_to_xml()

source = openmc.Source() #type: ignore
source.space = openmc.stats.Point((0,0,0))
phi = openmc.stats.Uniform(0, 2*pi)
#mu  = openmc.stats.Uniform(cos(atan2(l/2, SSD)), 1)
mu  = openmc.stats.Uniform(cos(atan2(40/2, SSD)), 1)
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV
source.particle = 'photon'


settings = openmc.Settings()
settings.batches = batches
settings.inactive = inactive
settings.particles = particles
settings.run_mode = 'fixed source'
settings.photon_transport = True
settings.export_to_xml()
# }}}

openmc.run()
