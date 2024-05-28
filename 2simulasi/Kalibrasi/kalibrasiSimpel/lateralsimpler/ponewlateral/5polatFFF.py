import openmc, openmc.model, openmc.stats, openmc.data
from math import pi, atan2, cos
import matplotlib.pyplot as plt

ROOM_SIZE = 60 
LINAC_DIRECTION= 130 
SOURCE_SIZE = 30
PHANTOM_SIZE = 50

air = openmc.Material(name='air')
air.set_density('g/cm3', 0.001)
air.add_element('N', 0.7)
air.add_element('O', 0.3)

water = openmc.Material(name='water')
water.set_density('g/cm3', 1.0)
water.add_element('H', 2)
water.add_element('O', 1)
water.add_s_alpha_beta('c_H_in_H2O')

tungsten = openmc.Material(name='Collimator')
tungsten.set_density('g/cm3', 17)
tungsten.add_nuclide('W184', 0.905, 'ao')
tungsten.add_element('Ni', 0.065, 'ao')
tungsten.add_nuclide('Fe56', 0.03, 'ao')

copper=openmc.Material(name='Copper')
copper.add_nuclide('Cu63', 30.83, 'ao')
copper.add_nuclide('Cu65', 69.17, 'ao')
copper.set_density('g/cm3',8.92)
materials = openmc.Materials([air, water,tungsten,copper])
materials.export_to_xml()

# create the room
roomX0 = openmc.XPlane(x0=-LINAC_DIRECTION, boundary_type='vacuum')
roomX1 = openmc.XPlane(x0= ROOM_SIZE/2, boundary_type='vacuum')
roomY0 = openmc.YPlane(y0=-ROOM_SIZE/2, boundary_type='vacuum')
roomY1 = openmc.YPlane(y0= ROOM_SIZE/2, boundary_type='vacuum')
roomZ0 = openmc.ZPlane(z0=-ROOM_SIZE/2, boundary_type='vacuum')
roomZ1 = openmc.ZPlane(z0= ROOM_SIZE/2, boundary_type='vacuum')
roomTotalRegion = +roomX0 & -roomX1 & +roomY0 & -roomY1 & +roomZ0 & -roomZ1

# create the phantom
phantomX0 = openmc.XPlane(x0=-PHANTOM_SIZE/2)
phantomX1 = openmc.XPlane(x0= PHANTOM_SIZE/2)
phantomY0 = openmc.YPlane(y0=-PHANTOM_SIZE/2)
phantomY1 = openmc.YPlane(y0= PHANTOM_SIZE/2)
phantomZ0 = openmc.ZPlane(z0=-PHANTOM_SIZE/2)
phantomZ1 = openmc.ZPlane(z0= PHANTOM_SIZE/2)
phantomRegion = +phantomX0 & -phantomX1 & +phantomY0 & -phantomY1 & +phantomZ0 & -phantomZ1

# create secondary Collimator
secollDis= 47 #Secondary Collimator distance from target
secollLength = 7.8 #Secondary Collimator distance

sx0 = openmc.XPlane(-125+secollDis-(secollLength/2.0)) 
sx1 = openmc.XPlane(-125+secollDis+(secollLength/2.0)) #the length for area
secollOuter= +sx0 & -sx1 & +phantomY0 & -phantomY1 & +phantomZ0 & -phantomZ1

sy2 = +openmc.YPlane(-SOURCE_SIZE/2.0) & -openmc.YPlane(SOURCE_SIZE/2.0) #the width for area
sz2 = +openmc.ZPlane(-SOURCE_SIZE/2.0) & -openmc.ZPlane(SOURCE_SIZE/2.0) #the width for area
secollHole= +sx0 & -sx1 & sy2 & sz2
secollRegion= secollOuter & ~secollHole
"""
#create FF Cone
ffd=7.91 #FF Distance from target
ffr=1.905 #FF cone radius
ffh=1.89 #FF height
ffr2=1.905*1.905/1.89
ffconeShape=openmc.XCone(x0=-125+ffd,r2=ffr2)#FIX:Is this inward or outward, whats r2
ffconeup=openmc.XPlane(x0=-125+ffd)
ffcylup=openmc.XPlane(x0=-125+ffd+ffh)
ffconeGeo= -ffcylup & -ffconeShape & +ffconeup

# create FF Cylinderr
ffdr=3 #ffradius
ffdh=0.05 #ffdownheight FF cylinder down part height
ffcyl=openmc.XCylinder(r=ffdr) #FIX,: Is this inward or outward
ffcylup=openmc.XPlane(x0=-125+ffd+ffh)
ffcyldown=openmc.XPlane(x0=-125+ffd+ffh+ffdh)
ffcylGeo = -ffcyl & +ffcylup & -ffcyldown

# Create Jaw
jawThick=7.8
jawLength=20
"""
#roomRegion = roomTotalRegion & ~phantomRegion & ~secollRegion &~ffconeGeo & ~ffcylGeo
roomRegion = roomTotalRegion & ~phantomRegion & ~secollRegion

roomCell = openmc.Cell(region=roomRegion, fill=air)
phantomCell = openmc.Cell(region=phantomRegion, fill=water)
secoll=openmc.Cell(region=secollRegion,fill=tungsten)
#ffcone=openmc.Cell(fill=copper,region=ffconeGeo)
#ffcyl=openmc.Cell(fill=copper,region=ffcylGeo)

#universe = openmc.Universe(cells=[roomCell, phantomCell, secoll, ffcone, ffcyl])
universe = openmc.Universe(cells=[roomCell, phantomCell, secoll])
geom = openmc.Geometry(universe)
geom.export_to_xml()

colors={}
colors[water]='lightblue'
colors[air]='green'
#colors[copper]='black'
colors[tungsten]='grey'
print(colors)

universe.plot(width=(300,100),basis='xz',colors=colors)
plt.show()

plot= openmc.Plot()
plot.basis = 'xz'
plot.origin = (-60, 0, 0)
plot.width = (200., 100.)
plot.pixels = (1200, 600)
plot.color_by='material'
plot.colors={
    water:'blue',
    air:'green'
}
plot.to_ipython_image()

## source
d = 100#distance between linac and water phantom
t = 1 #thickness
source = openmc.Source()
source.space = openmc.stats.Point((-PHANTOM_SIZE/2-d,0,0))
phi = openmc.stats.Uniform(0,2*pi)
mu  = openmc.stats.Uniform(cos(atan2(50/2, 100)), 1)
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(1,0,0))
#source.space = openmc.stats.Box((-PHANTOM_SIZE/2-d, -SOURCE_SIZE/2, -SOURCE_SIZE/2), (-PHANTOM_SIZE/2-d-t, SOURCE_SIZE/2, SOURCE_SIZE/2))
#source.angle = openmc.stats.Monodirectional((1, 0, 0))
source.energy = openmc.stats.Discrete([10e6], [1])
source.particle = 'photon'

## tally
tallysize=0.1
mesh = openmc.Mesh()
mesh.dimension = [1, 1, 500]
mesh.lower_left = [(-PHANTOM_SIZE/2)+2.5, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
mesh.upper_right = [(-PHANTOM_SIZE/2)+2.5+tallysize, tallysize/2, PHANTOM_SIZE/2] #type: ignore
mesh_filter = openmc.MeshFilter(mesh)

mesh5 = openmc.Mesh()
mesh5.dimension = [1, 1, 500]
mesh5.lower_left = [(-PHANTOM_SIZE/2)+5, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
mesh5.upper_right = [(-PHANTOM_SIZE/2)+5+tallysize, tallysize/2, PHANTOM_SIZE/2] #type: ignore
mesh5_filter = openmc.MeshFilter(mesh5)

mesh10 = openmc.Mesh()
mesh10.dimension = [1, 1, 500]
mesh10.lower_left = [(-PHANTOM_SIZE/2)+10, -tallysize/2, -PHANTOM_SIZE/2] #type: ignore
mesh10.upper_right = [(-PHANTOM_SIZE/2)+10+tallysize, tallysize/2, PHANTOM_SIZE/2] #type: ignore
mesh10_filter = openmc.MeshFilter(mesh10)

meshv = openmc.Mesh()
meshv.dimension = [300, 1, 1]
meshv.lower_left = [(-PHANTOM_SIZE/2), -tallysize/2, -tallysize/2] #type: ignore
meshv.upper_right = [(-PHANTOM_SIZE/2)+30, tallysize/2, tallysize/2] #type: ignore
meshv_filter = openmc.MeshFilter(meshv)

meshvLarge = openmc.Mesh()
meshvLarge.dimension = [300, 1, 1]
meshvLarge.lower_left = [(-PHANTOM_SIZE/2), -PHANTOM_SIZE/2, -PHANTOM_SIZE/2] #type: ignore
meshvLarge.upper_right = [(-PHANTOM_SIZE/2)+30, PHANTOM_SIZE/2, PHANTOM_SIZE/2] #type: ignore
meshvLarge_filter = openmc.MeshFilter(meshvLarge)

meshL = openmc.Mesh()
meshL.dimension = [1, 1, 500]
meshL.lower_left = [(-PHANTOM_SIZE/2), -PHANTOM_SIZE/2, -PHANTOM_SIZE/2] #type: ignore
meshL.upper_right = [(-PHANTOM_SIZE/2)+PHANTOM_SIZE, PHANTOM_SIZE/2, PHANTOM_SIZE/2] #type: ignore
meshL_filter = openmc.MeshFilter(meshL)

particle_filter = openmc.ParticleFilter(['photon'])
energy, dose = openmc.data.dose_coefficients('photon', 'RLAT')
dose_filter = openmc.EnergyFunctionFilter(energy, dose)

tally = openmc.Tally(name="2.5 depth tally")
tally.filters = [mesh_filter, particle_filter, dose_filter]
tally.scores = ['flux']

tally5 = openmc.Tally(name="5 depth tally")
tally5.filters = [mesh5_filter, particle_filter, dose_filter]
tally5.scores = ['flux']

tally10 = openmc.Tally(name="10 depth tally")
tally10.filters = [mesh10_filter, particle_filter, dose_filter]
tally10.scores = ['flux']

tallyv = openmc.Tally(name="depth dose tally")
tallyv.filters = [meshv_filter, particle_filter, dose_filter]
tallyv.scores = ['flux']

tallyvLarge = openmc.Tally(name="depth dose (Bigger slice)")
tallyvLarge.filters = [meshvLarge_filter, particle_filter, dose_filter]
tallyvLarge.scores = ['flux']

tallyL = openmc.Tally(name="lateral (Bigger slice)")
tallyL.filters = [meshL_filter, particle_filter, dose_filter]
tallyL.scores = ['flux']

tallies = openmc.Tallies()
tallies.append(tally)
tallies.append(tally5)
tallies.append(tally10)
tallies.append(tallyv)
tallies.append(tallyvLarge)
tallies.append(tallyL)

tallies.export_to_xml()

particles = int(input('Enter number of particle (It was 1e8)\n= ')) #1_000_000_000

## settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.particles = particles
settings.batches = 20
settings.inactive = 0
settings.source = source
settings.export_to_xml()

openmc.run()
