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

materials = openmc.Materials([air,water])
materials.export_to_xml()
# }}}


# {{{# TODO: Check the drop on PDD and the file that will be sent by Mbak Oksel to ensure the WP depth
 
# TODO: MAKE 50 X 50 X 40 Water Cells
# TODO: Line up tally on (depth : 5,10,20,30) for 10x10 and 40x30.
# TODO: Tally size = 0.5 x 0.5 x 0.1 cm
# TODO: Make Vertical tallies for PDD 
# TODO: Make y tallies for lateral
# TODO: Make x tallies for lateral
#}}}


########### WATER CELLS #############
SSD = 100.0 #Source to Skin Distance
water_depth = 10
watery= 50
waterz= 50

#{{{
wp_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+water_depth)
wp_y = +openmc.YPlane(-watery /2) & -openmc.XPlane(watery /2)
wp_z = +openmc.ZPlane(-waterz /2) & -openmc.ZPlane(waterz /2)
wp_cell=openmc.Cell(region=wp_x & wp_y & wp_z)
wp_cell.fill=water
#}}}
########### Vertical Tallies  ############
tallies_depth = 10
tallies_width= 1 # panjang dan lebar WP
padd = 10.0 #padding terhadap source dan detektor

#Slice for Depth Dose
n = 1000
phantom_cells = []
s_water_cells = []
dx = water_depth/n #
for i in range(n):
    x0 = SSD + i*dx #slice begin
    x1 = SSD +(i+1)*dx #slice end
    r_x = +openmc.XPlane(x0) & -openmc.XPlane(x1) #area between slices 
    r_y = +openmc.YPlane(-tallies_width/2.0) & -openmc.YPlane(tallies_width/2.0) #the length for area
    r_z = +openmc.ZPlane(-tallies_width/2.0) & -openmc.ZPlane(tallies_width/2.0) #the width for area
    cell = openmc.Cell(region=r_x & r_y & r_z)
    cell.fill=water
    phantom_cells.append(cell)
    


wp_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+water_depth)
wp_y = +openmc.YPlane(-watery/2.0) & -openmc.YPlane(watery/2.0)
wp_z = +openmc.ZPlane(-waterz/2.0) & -openmc.ZPlane(waterz/2.0)
tallies_y = +openmc.YPlane(-tallies_width/2.0) & -openmc.YPlane(tallies_width/2.0)
tallies_z = +openmc.ZPlane(-tallies_width/2.0) & -openmc.ZPlane(tallies_width/2.0)
rs_phantom = wp_x & wp_y & wp_z
r_phantom = wp_x & tallies_y & tallies_z 
#rs_phantom.fill=water
rs_phantomcell=openmc.Cell(fill=water,region=rs_phantom & ~r_phantom)

r_x_air = +openmc.XPlane(-padd, boundary_type='vacuum')\
        & -openmc.XPlane(SSD+water_depth+padd, boundary_type='vacuum')
r_y_air = +openmc.YPlane(-watery/2.0-padd, boundary_type='vacuum')\
        & -openmc.YPlane(watery/2.0+padd, boundary_type='vacuum')
r_z_air = +openmc.ZPlane(-waterz/2.0-padd, boundary_type='vacuum')\
        & -openmc.ZPlane(waterz/2.0+padd, boundary_type='vacuum')
r_air = r_x_air & r_y_air & r_z_air
c_air = openmc.Cell(region=r_air & ~r_phantom & ~rs_phantom)
c_air.fill = air

univ = openmc.Universe(cells=[c_air]+phantom_cells+[rs_phantomcell])
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
"""
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
mu  = openmc.stats.Uniform(cos(atan2(10/2, SSD)), 1)
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
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
