# vim:foldmethod=marker
import openmc
import matplotlib.pyplot as plt
import openmc.stats, openmc.data
from math import cos, atan2, pi

batches = 30
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

materials = openmc.Materials([air,water])
materials.export_to_xml()
# }}}


########### WATER CELLS #############
SSD = 100.0 #Source to Skin Distance
waterDepth = 50
watery= 50
waterz= 50

########### Vertical Tallies  ############
wpDepth = 50
padd = 10.0 #padding terhadap source dan detektor


#Slice for Depth Dose
n = 100
phantom_cells = []
s_water_cells = []
dx = watery/n #
lattaliesSide=watery/n
lattaliesDepth=2
for i in range(n):
    y0 = (-watery/2) + i*dx #slice begin
    y1 = (-watery/2) +(i+1)*dx #slice end
    r_y = +openmc.YPlane(y0) & -openmc.YPlane(y1) #area between slices 
    r_x = +openmc.XPlane(SSD+lattaliesDepth-(lattaliesSide/2.0)) & -openmc.XPlane(SSD+lattaliesDepth+(lattaliesSide/2.0)) #the length for area
    r_z = +openmc.ZPlane(-lattaliesSide/2.0) & -openmc.ZPlane(lattaliesSide/2.0) #the width for area
    cell = openmc.Cell(region=r_x & r_y & r_z)
    cell.fill=water
    phantom_cells.append(cell)
    

#NOTE: Create water phantom on 0 til (tallies depth-(1/2 tally height)) w/ 50x50 width
#NOTE: Create water phantom on (tallies depth + (1/2 tally height)) until 40 cm
wp_x1 = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+lattaliesDepth-(lattaliesSide/2.0))
wp_x3 = +openmc.XPlane(SSD+lattaliesDepth+(lattaliesSide/2.0)) & -openmc.XPlane(SSD+waterDepth)
wp_y = +openmc.YPlane(-watery/2.0) & -openmc.YPlane(watery/2.0)
wp_z = +openmc.ZPlane(-waterz/2.0) & -openmc.ZPlane(waterz/2.0)
wp1 = wp_x1 & wp_y & wp_z
wp3 = wp_x3 & wp_y & wp_z
wp1cell=openmc.Cell(fill=water,region=wp1)
wp3cell=openmc.Cell(fill=water,region=wp3)

#NOTE:create the one that overlaps with water phantom 
t_x = +openmc.XPlane(SSD+lattaliesDepth-(lattaliesSide/2.0)) & -openmc.XPlane(SSD+lattaliesDepth+(lattaliesSide/2.0)) #the length for area
t_y = +openmc.YPlane(-watery/2) & -openmc.YPlane(watery/2) #area between slices 
t_z = +openmc.ZPlane(-waterz/2) & -openmc.ZPlane(waterz/2) #area between slices 
t_z2 = +openmc.ZPlane(-lattaliesSide/2.0) & -openmc.ZPlane(lattaliesSide/2.0) #the width for area
tallyGeo= t_x & t_y & t_z2 #the geometry that would overlaps with tally
tallySurr = t_x & t_y & t_z #The whole water cells
rs_phantomcell=openmc.Cell(fill=water,region=tallySurr& ~tallyGeo)


r_x_air = +openmc.XPlane(-padd, boundary_type='vacuum')\
        & -openmc.XPlane(SSD+waterDepth+padd, boundary_type='vacuum')
r_y_air = +openmc.YPlane(-watery/2.0-padd, boundary_type='vacuum')\
        & -openmc.YPlane(watery/2.0+padd, boundary_type='vacuum')
r_z_air = +openmc.ZPlane(-waterz/2.0-padd, boundary_type='vacuum')\
        & -openmc.ZPlane(waterz/2.0+padd, boundary_type='vacuum')
r_air = r_x_air & r_y_air & r_z_air
wp_x4 = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+waterDepth)
waterphantom = wp_x4 & t_y & t_z #The whole water cells
c_air = openmc.Cell(fill=air,region=r_air & ~waterphantom)

#NOTE: optional : Make a dpp on the water tallies also
#Can also be only added for the 0 to (5-tallies_width/2)

#NOTE: Add all the added geometry into univ
univ = openmc.Universe(cells=[c_air]+phantom_cells+[rs_phantomcell]+[wp1cell]+[wp3cell])
geometry = openmc.Geometry()
geometry.root_universe = univ
geometry.export_to_xml()
# }}}

colors={}
colors[air]='lightblue'
colors[water]='blue'
"""
univ.plot(width=(300,300),basis='xy',color_by='material',colors=colors)
plt.savefig('xyCall.png')
plt.show()
univ.plot(width=(300,300),basis='yz',color_by='material',colors=colors)
plt.savefig('yzCall.png')
plt.show()
univ.plot(width=(300,300),basis='xz',color_by='material',colors=colors)
plt.savefig('xzCall.png')
plt.show()

# {{{
height = 300
plotXZ = openmc.Plot()
plotXZ.filename = f'img'
plotXZ.basis = 'xy'
plotXZ.width = ((SSD+water_depth+padd)*2, (SSD+water_depth+padd)*2)
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

#TODO: ADDING Mesh Tallies
mesh = openmc.RegularMesh() # type: ignore
mesh.dimension=[0,320,320]
meshlength=320
mesh.lower_left=[-meshlength/2,-meshlength/2]
mesh.upper_right=[meshlength/2,meshlength/2]

mesh_filter=openmc.MeshFilter(mesh)
meshtally = openmc.Tally(name='2d mesh dose distribution')
meshtally.scores=['flux']
meshtally.filters=[mesh_filter,particle_filter,dose_filter]
tallies_file.append(meshtally)

tallies_file.export_to_xml()

source = openmc.Source() #type: ignore
#source.space = openmc.stats.Point((0,0,0))
#phi = openmc.stats.Uniform(0, 2*pi)
#mu  = openmc.stats.Uniform(cos(atan2(10/2, SSD)), 1)
#source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
source.space=openmc.stats.Box(lower_left=[99.99,-10,-10],upper_right=[100,10,10])
source.angle=openmc.stats.Monodirectional(reference_uvw=(1.0,0,0))
source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV
source.particle = 'photon'

"""
mesh=openmc.RegularMesh()
mesh.dimension=[500,500]
xlen = 200;ylen=200;zlen=250
mesh.lower_left = [-xlen/2, -ylen/2, -zlen/2]
mesh.upper_right = [xlen/2, ylen/2, zlen/2]
mesh_filter = openmc.MeshFilter(mesh)

tally2=openmc.Tally(name='Room Dose Distribution')
tally2.scores=['flux']
particle2=openmc.ParticleFilter('photon')
tally2.filters=[mesh_filter,particle2,dose_filter]
"""


settings = openmc.Settings()
settings.batches = batches
settings.inactive = inactive
settings.particles = particles
settings.run_mode = 'fixed source'
settings.photon_transport = True
settings.export_to_xml()
# }}}

openmc.run()
