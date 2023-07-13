import openmc
import matplotlib.pyplot as plt

mat = openmc.Material()
print(mat)

#Uranium Dioksida, Seperti H2O tapi pakai U bukannya H.
uo2 = openmc.Material(1,"uo2") 
uo2.add_nuclide('U235',0.03)
uo2.add_nuclide('U238',0.97)
uo2.add_nuclide('O16',2)
uo2.set_density('g/cm3',10)
print("uo2 =",uo2)

#Pure Zirconium
zirconium =  openmc.Material(2,"Zirconium")
zirconium.add_nuclide('Zr',1.0)
zirconium.set_density('g/cm3',6.6)
print("Zirconium =",zirconium)

#Just Water, H2O
water=openmc.Material(3,"H2O")
water.add_nuclide('H1',2)
water.add_nuclide('O16',1)
water.set_density('g/cc',1)
water.add_s_alpha_beta('c_H_in_H2O')

mats=openmc.Materials([uo2,zirconium,water])
#It's an array that could be used as this
#mats=openmc.Materials()
#mats.append(uo2)
#mats +=[zirconium,water]
#isinstance(mats,list)
mats.export_to_xml()

######################################

########### Material Mix #############
#mixture of 0.97 uo2 and 0.03 puo2

uo2_3 = openmc.Material()
uo2_3.add_element('U',1,enrichment=3)
uo2_3.add_element('O',2)
uo2_3.set_density('g/cm3',10) #g/cc = g/cm3

#instead of u or H, Here we use Pu
puo2=openmc.Material()
puo2.add_nuclide('Pu239',0.94)
puo2.add_nuclide('Pu240',0.06)
puo2.add_nuclide('O16',2)
puo2.set_density('g/cm3',11.5)

mox=openmc.Material.mix_materials([uo2,puo2],[0.97,0.03],'wo')
######################################


############# Geometry ###############
sph= openmc.Sphere(r=1.0)
isphere=-sph
osphere=+sph

#print((0,0,0) in isphere, (0,0,2) in isphere)

z_plane=openmc.ZPlane(z0=0)
n_hemisphere=-sph & +z_plane #What the hell does this even mean

n_hemisphere.bounding_box

cell=openmc.Cell()
cell.region=n_hemisphere #or cell = openmc.Cell(region=n_hemisphere)
cell.fill=water

######################################
univ=openmc.Universe(cells=[cell]) #univ=openmc.Universe() ;univ.add_cell(cell)

univ.plot(width=(2.0, 2.0))
plt.savefig('plot.png')
univ.plot(width=(2,2),basis='xz',colors={cell:'fuchsia'})

plt.savefig('xz.png')
plt.show()
######################################
######################################



fuel_or = openmc.ZCylinder(r=0.39)
clad_ir = openmc.ZCylinder(r=0.40)
clad_or = openmc.ZCylinder(r=0.46)
fuel_region = -fuel_or
gap_region = +fuel_or & -clad_ir
clad_region = +clad_ir & -clad_or

fuel = openmc.cell(1,'fuel')
fuel.fill=uo2
fuel.region = fuel_region

gap = openmc.Cell(2,'air gap')
gap.region = gap_region

clad=openmc.Cell(3,'clad')
clad.fill=zirconium
gap.region = clad_region

pitch = 1.26
left = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
right = openmc.XPlane(x0=pitch/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
top = openmc.YPlane(y0=pitch/2, boundary_type='reflective') 

w_region = +left & -right & +bottom & -top & + clad_or

moderator=openmc.Cell(4,'moderator')
moderator.fill = water
moderator.region=w_region

box = openmc.rectangular_prism(width=pitch, height=pitch, boundary_type='reflective')
type(box)

w_region = box & +clad_or