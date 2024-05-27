
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

#create FF Cone
ffd=7.91 #FF Distance from target
ffr=1.905 #FF cone radius
ffh=1.89 #FF height
ffr2=1.905*1.905/1.89
ffconeShape=openmc.XCone(x0=-125+ffd,r2=ffr2)#FIX:Is this inward or outward, whats r2
ffcylup=openmc.XPlane(x0=-125+ffd+ffh)
ffconeup=openmc.XPlane(x0=-125+ffd)
ffconeGeo= -ffcylup & -ffconeShape & +ffconeup

roomRegion = roomTotalRegion & ~phantomRegion & ~secollRegion &~ffconeGeo

roomCell = openmc.Cell(region=roomRegion, fill=air)
phantomCell = openmc.Cell(region=phantomRegion, fill=water)
secoll=openmc.Cell(region=secollRegion,fill=tungsten)
ffcone=openmc.Cell(fill=copper,region=ffconeGeo)

#universe = openmc.Universe(cells=[roomCell, phantomCell, secoll, ffcone, ffcyl])
universe = openmc.Universe(cells=[roomCell,phantomCell,secoll,ffcone])
#universe = openmc.Universe(cells=[roomCell,phantomCell])

colors={}
colors[water]='lightblue'
colors[air]='green'
colors[copper]='black'
colors[tungsten]='grey'
print(colors)

universe.plot(width=(300,100),basis='xz',colors=colors)
plt.show()
