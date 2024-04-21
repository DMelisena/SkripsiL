# vim:foldmethod=marker
import matplotlib.pyplot as plt
import openmc.stats, openmc.data
from math import cos, atan2, pi

batches = 10
inactive = 10
particles =10_000_000


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


SSD = 100.0 #Source to Skin Distance

# TODO: Check the drop on PDD and the file that will be sent by Mbak Oksel to ensure the WP depth
 
# TODO: MAKE 50 X 50 X 40 Water Cells
# TODO: Line up tally on (depth : 5,10,20,30) for 10x10 and 40x30.
# TODO: Tally size = 0.5 x 0.5 x 0.1 cm
# TODO: Make Vertical tallies for PDD 
# TODO: Make y tallies for lateral
# TODO: Make x tallies for lateral


########### WATER CELLS #############
watery= 50
waterz= 50
water_depth = 40
wp_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+water_depth)
wp_y = +openmc.YPlane(-watery /2) & -openmc.XPlane(watery /2)
wp_z = +openmc.ZPlane(-waterz /2) & -openmc.ZPlane(waterz /2)
wp_cell=openmc.Cell(region=wp_x & wp_y & wp_z)
wp_cell.fill=water

########### Vertical Tallies  ############
# TODO: check tallies appending on old codes
tallies_depth = 40
tallies_width= 0.5 # panjang dan lebar WP
padd = 10.0 #padding terhadap source dan detektor
r_x = +openmc.XPlane(SSD) & -openmc.XPlane(SSD+tallies_depth)
r_y = +openmc.YPlane(-tallies_width/2.0) & -openmc.YPlane(tallies_width/2.0)
r_z = +openmc.ZPlane(-tallies_width/2.0) & -openmc.ZPlane(tallies_width/2.0)
r_phantom = r_x & r_y & r_z

#Slice for Depth Dose
n = 400
dpp_cells = []
dx = tallies_depth/n
for i in range(n):
    x0 = SSD + i*dx #slice begin
    x1 = SSD +(i+1)*dx #slice end
    r_x = +openmc.XPlane(x0) & -openmc.XPlane(x1) #area between slices 
    r_y = +openmc.YPlane(-tallies_width/2.0) & -openmc.YPlane(tallies_width/2.0) #the length for area
    r_z = +openmc.ZPlane(-tallies_width/2.0) & -openmc.ZPlane(tallies_width/2.0) #the width for area
    cell = openmc.Cell(region=r_x & r_y & r_z)
    dpp_cells.append(cell)


########### Y Lateral Tallies ##########

ylat0= []
ylat5= []
ylat10= []
ylat15= []
ylat20= []
dy = 0.2
lattallies_width=0.5
lattallies_depth=0.2
ny = 100
dis5=SSD+5

for i in range(ny):
    y0 = -25+ i*dy #slice begin
    y1 = -25+(i+1)*dy #slice end

    r_x = +openmc.XPlane(SSD-lattallies_depth/2.0) & -openmc.XPlane(SSD+lattallies_depth/2.0) #the length for area
    r_y = +openmc.YPlane(y0) & -openmc.YPlane(y1) #area between slices 
    r_z = +openmc.ZPlane(-lattallies_width/2.0) & -openmc.ZPlane(lattallies_width/2.0) #the width for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    ylat0.append(cell)

    r_x = +openmc.XPlane(SSD+5-lattallies_depth/2.0) & -openmc.XPlane(SSD+5+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    ylat5.append(cell)

    r_x = +openmc.XPlane(SSD+10-lattallies_depth/2.0) & -openmc.XPlane(SSD+10+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    ylat10.append(cell)

    r_x = +openmc.XPlane(SSD+15-lattallies_depth/2.0) & -openmc.XPlane(SSD+15+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    ylat15.append(cell)

    r_x = +openmc.XPlane(SSD+20-lattallies_depth/2.0) & -openmc.XPlane(SSD+20+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    ylat20.append(cell)

########### Z Lateral Tallies ##########

zlat0= []
zlat5= []
zlat10= []
zlat15= []
zlat20= []
dz = 0.2
lattallies_width=0.5
lattallies_depth=0.2
nz = 100
dis5=SSD+5

for i in range(nz):
    z0 = -25+ i*dz #slice begin
    z1 = -25+(i+1)*dz #slice end

    r_x = +openmc.XPlane(SSD-lattallies_depth/2.0) & -openmc.XPlane(SSD+lattallies_depth/2.0) #the length for area
    r_y = +openmc.YPlane(-lattallies_width/2.0) & -openmc.YPlane(lattallies_width/2.0) #the width for area
    r_z = +openmc.ZPlane(z0) & -openmc.ZPlane(z1) #area between slices 
    cell= openmc.Cell(region=r_x & r_y & r_z)
    zlat0.append(cell)

    r_x = +openmc.XPlane(SSD+5-lattallies_depth/2.0) & -openmc.XPlane(SSD+5+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    zlat5.append(cell)

    r_x = +openmc.XPlane(SSD+10-lattallies_depth/2.0) & -openmc.XPlane(SSD+10+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    zlat10.append(cell)

    r_x = +openmc.XPlane(SSD+15-lattallies_depth/2.0) & -openmc.XPlane(SSD+15+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    zlat15.append(cell)

    r_x = +openmc.XPlane(SSD+20-lattallies_depth/2.0) & -openmc.XPlane(SSD+20+lattallies_depth/2.0) #the length for area
    cell= openmc.Cell(region=r_x & r_y & r_z)
    zlat20.append(cell)

# HACK: Air cells are unchecked

########### Air cells  ###########
r_x_air = +openmc.XPlane(-padd, boundary_type='vacuum')\
    & -openmc.XPlane(SSD+tallies_depth+padd, boundary_type='vacuum')
r_y_air = +openmc.YPlane(-tallies_width/2.0-padd, boundary_type='vacuum')\
    & -openmc.YPlane(tallies_width/2.0+padd, boundary_type='vacuum')
r_z_air = +openmc.ZPlane(-tallies_width/2.0-padd, boundary_type='vacuum')\
    & -openmc.ZPlane(tallies_width/2.0+padd, boundary_type='vacuum')
r_air = r_x_air & r_y_air & r_z_air
c_air = openmc.Cell(region=r_air & ~r_phantom)
c_air.fill = air

# HACK: Final geometry unchecked
################## FINAL GEOMETRY #####################
universe = openmc.Universe(cells=[c_air]+dpp_cells+ylat0+ylat5+ylat10+ylat15+ylat20+zlat5+zlat0+zlat10+zlat15+zlat20)
geometry = openmc.Geometry()
geometry.root_universe = universe
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
plotXZ.width = ((SSD+tallies_depth+padd)*2, (SSD+tallies_depth++padd)*2)
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

source = openmc.Source() #type: ignore
source.space = openmc.stats.Point((0,0,0))
phi = openmc.stats.Uniform(0, 2*pi)
#mu  = openmc.stats.Uniform(cos(atan2(l/2, SSD)), 1)
mu  = openmc.stats.Uniform(cos(atan2(40/2, SSD)), 1)
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV
source.particle = 'photon'

tallies_file = openmc.Tallies()
dpp_cell_filter= openmc.CellFilter(dpp_cells)
ylat0_cell_filter= openmc.CellFilter(ylat0)
ylat5_cell_filter= openmc.CellFilter(ylat5)
ylat10_cell_filter= openmc.CellFilter(ylat10)
ylat15_cell_filter= openmc.CellFilter(ylat15)
ylat20_cell_filter= openmc.CellFilter(ylat20)
zlat0_cell_filter= openmc.CellFilter(zlat0)
zlat5_cell_filter= openmc.CellFilter(zlat5)
zlat10_cell_filter= openmc.CellFilter(zlat10)
zlat15_cell_filter= openmc.CellFilter(zlat15)
zlat20_cell_filter= openmc.CellFilter(zlat20)

tally = openmc.Tally(name='tally')
#tally.filters = [ylat0_cell_filter, ylat5_cell_filter, ylat10_cell_filter, ylat15_cell_filter, ylat20_cell_filter, 
#                 zlat0_cell_filter, zlat5_cell_filter, zlat10_cell_filter, zlat15_cell_filter, zlat20_cell_filter, 
#                 dpp_cell_filter, particle_filter, dose_filter]
tally.filters = [dpp_cell_filter,ylat5_cell_filter,zlat5_cell_filter, particle_filter, dose_filter]

tally.scores = ['flux']
tallies_file.append(tally)
tallies_file.export_to_xml()
"""
mesh=openmc.RegularMesh()
mesh.dimension=[500,500]

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
