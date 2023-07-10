import openmc
uo2 = openmc.Material(1,"uo2")
print(uo2)

mat = openmc.Material()
print(mat)

uo2.add_nuclide('U235',0.03)
uo2.add_nuclide('U238',0.97)
uo2.add_nuclide('O16',2)
uo2 = openmc.Material(1, "uo2")
print(uo2)
"""
zircaloy =  openmc.Material(name='Zircaloy')
zircaloy.set_density('g/cm3',6.55)
zircaloy.add_nuclide('Zr90',7.2758e-3)

zirconium =  openmc.Material("Zirconium")
zirconium.set_density('g/cm3')
zirconium.add_nuclide('Zr',1)
"""
print(uo2)
"""
      ,"\n",zircaloy,"\n",zirconium
      
      )"""