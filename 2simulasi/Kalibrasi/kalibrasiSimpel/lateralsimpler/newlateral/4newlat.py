import openmc, openmc.model, openmc.stats, openmc.data

ROOM_SIZE = 100
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

materials = openmc.Materials([air, water])
materials.export_to_xml()

# create the room
roomX0 = openmc.XPlane(x0=-ROOM_SIZE/2, boundary_type='vacuum')
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

roomTotalRegion = +roomX0 & -roomX1 & +roomY0 & -roomY1 & +roomZ0 & -roomZ1
roomRegion = roomTotalRegion & ~phantomRegion

roomCell = openmc.Cell(region=roomRegion, fill=air)
phantomCell = openmc.Cell(region=phantomRegion, fill=water)

universe = openmc.Universe(cells=[roomCell, phantomCell])
geom = openmc.Geometry(universe)
geom.export_to_xml()


## source
d = 10
t = 1
source = openmc.Source()
source.space = openmc.stats.Box((-PHANTOM_SIZE/2-d, -SOURCE_SIZE/2, -SOURCE_SIZE/2), (-PHANTOM_SIZE/2-d-t, SOURCE_SIZE/2, SOURCE_SIZE/2))
source.angle = openmc.stats.Monodirectional((1, 0, 0))
source.energy = openmc.stats.Discrete([10e6], [1])
source.particle = 'photon'

## tally
mesh = openmc.Mesh()
mesh.dimension = [1, 1, 100]
mesh.lower_left = [-PHANTOM_SIZE/2, -PHANTOM_SIZE/2, -PHANTOM_SIZE/2] #type: ignore
mesh.upper_right = [PHANTOM_SIZE/2, PHANTOM_SIZE/2, PHANTOM_SIZE/2] #type: ignore
mesh_filter = openmc.MeshFilter(mesh)

particle_filter = openmc.ParticleFilter(['photon'])
energy, dose = openmc.data.dose_coefficients('photon', 'RLAT')
dose_filter = openmc.EnergyFunctionFilter(energy, dose)

tally = openmc.Tally()
tally.filters = [mesh_filter, particle_filter, dose_filter]
tally.scores = ['flux']

tallies = openmc.Tallies()
tallies.append(tally)
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
