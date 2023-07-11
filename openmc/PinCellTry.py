import openmc

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
water.set_density('g/cm3',1)

water.add_s_alpha_beta('c_H_in_H20')

"""
zircaloy =  openmc.Material(name='Zircaloy')
zircaloy.set_density('g/cm3',6.55)
zircaloy.add_nuclide('Zr90',7.2758e-3)
"""

print(uo2)
"""
      ,"\n",zircaloy,"\n",zirconium
      
      )"""