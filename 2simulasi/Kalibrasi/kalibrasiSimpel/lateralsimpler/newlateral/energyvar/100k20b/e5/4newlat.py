import openmc, openmc.model, openmc.stats, openmc.data
lenergy=1e5

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
tungsten.add_nuclide('W184', 1, 'ao')

materials = openmc.Materials([air, water,tungsten])
materials.export_to_xml()

# create the room
roomX0 = openmc.XPlane(x0=-LINAC_DIRECTION, boundary_type='vacuum')
roomX1 = openmc.XPlane(x0= ROOM_SIZE/2, boundary_type='vacuum')
roomY0 = openmc.YPlane(y0=-ROOM_SIZE/2, boundary_type='vacuum')
roomY1 = openmc.YPlane(y0= ROOM_SIZE/2, boundary_type='vacuum')
roomZ0 = openmc.ZPlane(z0=-ROOM_SIZE/2, boundary_type='vacuum')
roomZ1 = openmc.ZPlane(z0= ROOM_SIZE/2, boundary_type='vacuum')

# create the phantom
phantomX0 = openmc.XPlane(x0=-PHANTOM_SIZE/2)
phantomX1 = openmc.XPlane(x0= PHANTOM_SIZE/2)
phantomY0 = openmc.YPlane(y0=-PHANTOM_SIZE/2)
phantomY1 = openmc.YPlane(y0= PHANTOM_SIZE/2)
phantomZ0 = openmc.ZPlane(z0=-PHANTOM_SIZE/2)
phantomZ1 = openmc.ZPlane(z0= PHANTOM_SIZE/2)
phantomRegion = +phantomX0 & -phantomX1 & +phantomY0 & -phantomY1 & +phantomZ0 & -phantomZ1

secollDis= 47 #Secondary Collimator distance from target
secollLength = 7.8 #Secondary Collimator distance
s_x = +openmc.XPlane(secollDis-(secollLength/2.0)) & -openmc.XPlane(secollDis+(secollLength/2.0)) #the length for area
s_y = +openmc.YPlane(-PHANTOM_SIZE/2) & -openmc.YPlane(PHANTOM_SIZE) #area between slices 
s_z = +openmc.ZPlane(-PHANTOM_SIZE/2) & -openmc.ZPlane(PHANTOM_SIZE/2) #area between slices 

s_y2 = +openmc.YPlane(-SOURCE_SIZE/2.0) & -openmc.YPlane(SOURCE_SIZE/2.0) #the width for area
s_z2 = +openmc.ZPlane(-SOURCE_SIZE/2.0) & -openmc.ZPlane(SOURCE_SIZE/2.0) #the width for area
secollHole= s_x & s_y2 & s_z2 #the geometry that would overlaps with tally
secollSurr = s_x & s_y & s_z #The whole water cells
secollRegion = secollSurr & ~secollHole
secoll=openmc.Cell(fill=tungsten ,region=secollRegion)
roomTotalRegion = +roomX0 & -roomX1 & +roomY0 & -roomY1 & +roomZ0 & -roomZ1
roomRegion = roomTotalRegion & ~phantomRegion & ~secollRegion

roomCell = openmc.Cell(region=roomRegion, fill=air)
phantomCell = openmc.Cell(region=phantomRegion, fill=water)

universe = openmc.Universe(cells=[roomCell, phantomCell, secoll])
geom = openmc.Geometry(universe)
geom.export_to_xml()


## source
d = 100#distance between linac and water phantom
t = 1 #thickness
source = openmc.Source()
source.space = openmc.stats.Box((-PHANTOM_SIZE/2-d, -SOURCE_SIZE/2, -SOURCE_SIZE/2), (-PHANTOM_SIZE/2-d-t, SOURCE_SIZE/2, SOURCE_SIZE/2))
source.angle = openmc.stats.Monodirectional((1, 0, 0))
source.energy = openmc.stats.Discrete([lenergy], [1])
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

tallyL = openmc.Tally(name="depth dose (Bigger slice)")
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
