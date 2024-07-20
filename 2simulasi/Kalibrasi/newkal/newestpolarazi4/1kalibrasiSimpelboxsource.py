

# vim:foldmethod=marker
import openmc
import matplotlib.pyplot as plt
import openmc.stats, openmc.data
from math import cos, atan2, pi,atan

batches = 5
inactive = 10
particles = int(input('Enter number of particle (It was 1e8)\n= ')) #1_000_000_000
PHANTOM_SIZE=40 
SOURCE_SIZE=10
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

materials = openmc.Materials([air,water])
materials.export_to_xml()
# }}}

SSD = 100.0 #Source to Skin Distance
ld= 40# panjang dan lebar WP
d = 30.0 #kedalaman WP
padd = 10.0 #padding terhadap source dan detektor

# {{{

n = 1
phantom_cells = []
dx = d/n
for i in range(n):
    x0 = SSD + i*dx
    x1 = SSD +(i+1)*dx
    r_x = +openmc.XPlane(x0) & -openmc.XPlane(x1)
    r_y = +openmc.YPlane(-ld/2.0) & -openmc.YPlane(ld/2.0)
    r_z = +openmc.ZPlane(-ld/2.0) & -openmc.ZPlane(ld/2.0)

    cell = openmc.Cell(region=r_x & r_y & r_z)
    cell.fill = water
    phantom_cells.append(cell)

r_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+d)
r_y = +openmc.YPlane(-ld/2.0) & -openmc.YPlane(ld/2.0)
r_z = +openmc.ZPlane(-ld/2.0) & -openmc.ZPlane(ld/2.0)
r_phantom = r_x & r_y & r_z

r_x_air = +openmc.XPlane(-padd, boundary_type='vacuum')\
    & -openmc.XPlane(SSD+d+padd, boundary_type='vacuum')
r_y_air = +openmc.YPlane(-ld/2.0-padd, boundary_type='vacuum')\
    & -openmc.YPlane(ld/2.0+padd, boundary_type='vacuum')
r_z_air = +openmc.ZPlane(-ld/2.0-padd, boundary_type='vacuum')\
    & -openmc.ZPlane(ld/2.0+padd, boundary_type='vacuum')
r_air = r_x_air & r_y_air & r_z_air
c_air = openmc.Cell(region=r_air & ~r_phantom)
c_air.fill = air

universe = openmc.Universe(cells=[c_air]+phantom_cells)
geometry = openmc.Geometry()
geometry.root_universe = universe
geometry.export_to_xml()
# }}}
plot= openmc.Plot()
plot.basis = 'xz'
plot.origin = (0, 0, 0)
plot.width = (200., 100.)
plot.pixels = (1200, 600)
plot.color_by='material'
plot.colors={
    water:'blue',
    air:'green'
}
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

cell_filter = openmc.CellFilter(phantom_cells)
tally = openmc.Tally(name='tally')
tally.filters = [cell_filter, particle_filter, dose_filter]
tally.scores = ['flux']

dpp1=0.1
dpp01=openmc.Mesh()
dpp01.dimension=[300,1,1]
dpp01.lower_left=[100,-dpp1/2,-dpp1/2]
dpp01.upper_right=[100+d,dpp1/2,dpp1/2]
dpp01_filter = openmc.MeshFilter(dpp01)

dpp10s=10
dpp10=openmc.Mesh()
dpp10.dimension=[300,1,1]
dpp10.lower_left=[100,-dpp10s/2,-dpp10s/2]
dpp10.upper_right=[100+d,dpp10s/2,dpp10s/2]
dpp10_filter= openmc.MeshFilter(dpp10)

tallysize=0.1
mesh = openmc.Mesh()
mesh.dimension = [1, 1, 400]
mesh.lower_left = [SSD, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
mesh.upper_right = [SSD+tallysize, tallysize/2, PHANTOM_SIZE/2] #type: ignore
mesh_filter = openmc.MeshFilter(mesh)

mesh25 = openmc.Mesh()
mesh25.dimension = [1, 1, 400]
mesh25.lower_left = [SSD+2.5, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
mesh25.upper_right = [SSD+2.5, tallysize/2, PHANTOM_SIZE/2] #type: ignore
mesh25_filter = openmc.MeshFilter(mesh25)

mesh5 = openmc.Mesh()
mesh5.dimension = [1, 1, 400]
mesh5.lower_left = [SSD+5, -tallysize/2,PHANTOM_SIZE/2] #type: ignore
mesh5.upper_right = [SSD+5+tallysize, tallysize/2,PHANTOM_SIZE/2] #type: ignore
mesh5_filter = openmc.MeshFilter(mesh5)

mesh10 = openmc.Mesh()
mesh10.dimension = [1, 1, 400]
mesh10.lower_left = [SSD+10, -tallysize/2,-PHANTOM_SIZE/2] #type: ignore
mesh10.upper_right = [SSD+10+tallysize, tallysize/2,PHANTOM_SIZE/2] #type: ignore
mesh10_filter = openmc.MeshFilter(mesh10)

heatmap=openmc.Mesh()
heatmap.dimension =[1300,1,500]
heatmap.lower_left = [0, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
heatmap.upper_right = [SSD+d, tallysize/2, PHANTOM_SIZE/2] #type: ignore
heatmap_filter = openmc.MeshFilter(heatmap)

tallydpp = openmc.Tally(name="dpp tally 0.1")
tallydpp.filters = [dpp01_filter, particle_filter, dose_filter]
tallydpp.scores = ['flux']

tallydpp10 = openmc.Tally(name="dpp tally 10")
tallydpp10.filters = [dpp10_filter, particle_filter, dose_filter]
tallydpp10.scores = ['flux']

tally01 = openmc.Tally(name="0 depth tally")
tally01.filters = [mesh_filter, particle_filter, dose_filter]
tally01.scores = ['flux']

tally25 = openmc.Tally(name="2.5 depth tally")
tally25.filters = [mesh25_filter, particle_filter, dose_filter]
tally25.scores = ['flux']

tally5 = openmc.Tally(name="5 depth tally")
tally5.filters = [mesh5_filter, particle_filter, dose_filter]
tally5.scores = ['flux']

tally10 = openmc.Tally(name="10 depth tally")
tally10.filters = [mesh10_filter, particle_filter, dose_filter]
tally10.scores = ['flux']

heatmaptally = openmc.Tally(name="depth dose tally")
heatmaptally.filters = [heatmap_filter, particle_filter, dose_filter]
heatmaptally.scores = ['flux']


tallies = openmc.Tallies()
tallies.append(tally)
tallies.append(tallydpp)
tallies.append(tallydpp10)
tallies.append(tally01)
#tallies.append(tally25)
#tallies.append(tally5)
#tallies.append(tally10)
#tallies.append(heatmaptally)

tallies.export_to_xml()







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
#tan theta = r/SAD=20/1000; theta = atan(20/100)=0.19739555984988; cos theta=0.98058
#mu=openmc.stats.Uniform(0.98058,1) # type: ignore #mu= distribution of the cosine of the polar angle

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
