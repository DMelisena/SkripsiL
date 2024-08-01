# vim:foldmethod=marker
import openmc
import matplotlib.pyplot as plt
import openmc.stats, openmc.data
from math import cos, atan2, pi

batches = 5
inactive = 10
particles = int(input('Enter number of particle (It was 1e8)\n= ')) #1_000_000_000
PHANTOM_SIZE=40 
SOURCE_SIZE=20
FIELD_SIZE=30
# Material 

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

water2=openmc.Material(name='Water2')
water2.set_density('g/cm3',1.0)
water2.add_nuclide('H1',2.0)
water2.add_nuclide('O16',1.0)
water2.add_s_alpha_beta('c_H_in_H2O')

materials = openmc.Materials([air,water2,water])
materials.export_to_xml()
# }}}

SSD = 100.0 #Source to Skin Distance
ld= 0.1# panjang dan lebar WP tally
d = 30.0 #kedalaman WP
padd = 10.0 #padding terhadap source dan detektor

# {{{
"""
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

"""
r_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+d)
"""
r_y = +openmc.YPlane(-ld/2.0) & -openmc.YPlane(ld/2.0)
r_z = +openmc.ZPlane(-ld/2.0) & -openmc.ZPlane(ld/2.0)
r_phantom_tally = r_x & r_y & r_z
"""

r_ys = +openmc.YPlane(-PHANTOM_SIZE/2.0) & -openmc.YPlane(PHANTOM_SIZE/2.0)
r_zs = +openmc.ZPlane(-PHANTOM_SIZE/2.0) & -openmc.ZPlane(PHANTOM_SIZE/2.0)

r_phantom =  r_x & r_ys & r_zs
#r_phantom_surround = r_phantom & ~r_phantom_tally
r_phantom_surround = r_phantom
r_phantom_surround_cell= openmc.Cell(region=r_phantom_surround)
r_phantom_surround_cell.fill = water

r_x_air = +openmc.XPlane(-padd, boundary_type='vacuum')\
    & -openmc.XPlane(SSD+d+padd, boundary_type='vacuum')
r_y_air = +openmc.YPlane(-PHANTOM_SIZE/2.0-padd, boundary_type='vacuum')\
    & -openmc.YPlane(PHANTOM_SIZE/2.0+padd, boundary_type='vacuum')
r_z_air = +openmc.ZPlane(-PHANTOM_SIZE/2.0-padd, boundary_type='vacuum')\
    & -openmc.ZPlane(PHANTOM_SIZE/2.0+padd, boundary_type='vacuum')
r_air = r_x_air & r_y_air & r_z_air
c_air = openmc.Cell(region=r_air & ~r_phantom_surround)
c_air.fill = air

#universe = openmc.Universe(cells=[c_air]+phantom_cells+[r_phantom_surround_cell])
universe = openmc.Universe(cells=[c_air]+[r_phantom_surround_cell])
geometry = openmc.Geometry()
geometry.root_universe = universe
geometry.export_to_xml()
# }}}
plot= openmc.Plot()
plot.basis = 'yz'
plot.filename='yz_cal'
plot.origin = (120, 0, 0)
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
plot.origin=(120,0,0)
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


#######         TALLY          #########
tallies_file = openmc.Tallies()
"""
cell_filter = openmc.CellFilter(phantom_cells)
tally = openmc.Tally(name='tally')
tally.filters = [cell_filter, particle_filter, dose_filter]
tally.scores = ['flux']
"""

#######       MESH TALLY       #########
tallysize=0.1
mesh = openmc.Mesh()
mesh.dimension = [1, 1, 400]
mesh.lower_left = [SSD, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
mesh.upper_right = [SSD+tallysize, tallysize/2, PHANTOM_SIZE/2] #type: ignore
mesh_filter = openmc.MeshFilter(mesh)

tally01 = openmc.Tally(name="0 depth tally")
tally01.filters = [mesh_filter, particle_filter, dose_filter]
tally01.scores = ['flux']

meshdpp01 = openmc.Mesh()
meshdpp01.dimension = [300, 1, 1]
meshdpp01.lower_left = [SSD, -tallysize/2, -tallysize/2] #type: ignore
meshdpp01.upper_right = [SSD+d, tallysize/2, tallysize/2] #type: ignore
meshdpp01_filter = openmc.MeshFilter(meshdpp01)

tallydpp01 = openmc.Tally(name="profile depth dose tally")
tallydpp01.filters = [meshdpp01_filter, particle_filter, dose_filter]
tallydpp01.scores = ['flux']

meshdpp5 = openmc.Mesh()
meshdpp5.dimension = [300, 1, 1]
meshdpp5.lower_left = [SSD, -tallysize/2, -tallysize/2] #type: ignore
meshdpp5.upper_right = [SSD+d, tallysize/2, tallysize/2] #type: ignore
meshdpp5_filter = openmc.MeshFilter(meshdpp5)

tallydpp5 = openmc.Tally(name="profile depth dose tally")
tallydpp5.filters = [meshdpp5_filter, particle_filter, dose_filter]
tallydpp5.scores = ['flux']

#tallies_file.append(tally)
tallies_file.append(tallydpp01)
tallies_file.append(tallydpp5)
tallies_file.append(tally01)

tallies_file.export_to_xml()



"""
source = openmc.Source() #type: ignore
source.space = openmc.stats.Point((0,0,0))
phi = openmc.stats.Uniform(0, 2*pi)
#mu  = openmc.stats.Uniform(cos(atan2(l/2, SSD)), 1)
mu  = openmc.stats.Uniform(cos(atan2(40/2, SSD)), 1)
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV
source.particle = 'photon'
"""
phi = openmc.stats.Uniform(0, 2*pi)

mu  = openmc.stats.Uniform(cos(atan2(((FIELD_SIZE-SOURCE_SIZE)/2),SSD)), 1) 
source = openmc.Source()
source.space = openmc.stats.Box((-0.1, -SOURCE_SIZE/2, -SOURCE_SIZE/2), (0, SOURCE_SIZE/2, SOURCE_SIZE/2))
#source.angle = openmc.stats.Monodirectional((1, 0, 0))
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
source.energy = openmc.stats.Discrete([10e6], [1])
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
