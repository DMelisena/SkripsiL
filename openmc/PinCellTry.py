import openmc
import matplotlib.pyplot as plt


fuel_or = openmc.ZCylinder(r=0.39)
clad_ir = openmc.ZCylinder(r=0.40)
clad_or = openmc.ZCylinder(r=0.46)
fuel_region = -fuel_or #didalam fuel_or
gap_region = +fuel_or & -clad_ir #diluar fuel_or, tetapi didalam clad_ir
clad_region = +clad_ir & -clad_or #diluar clad_ir, tapi didalam clad_or

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
#Di luar clad or, adalah air. Tetapi didalam sumbu xy pitch

#box = openmc.rectangular_prism(width=pitch, height=pitch, boundary_type='reflective')
#type(box) ; w_region = box & +clad_or

univ = openmc.Universe(cells=(fuel,gap, clad, moderator))
univ.plot(width=(3.0,3.0))
plt.savefig('pincell.png')
univ.plot(width=(3,3),basis='xz',colors={cell:'fuchsia'})
plt.savefig('xzpincell.png')
plt.show()